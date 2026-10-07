import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_cfg(path=None):
    p = Path(path) if path else HERE / "config.json"
    return json.loads(p.read_text(encoding="utf-8")), p


def now_stamp():
    return datetime.now().astimezone().isoformat()


def reel_id(url):
    m = re.search(r"instagram\.com/(?:reel|p)/([^/?#]+)", url)
    return m.group(1) if m else "unknown"


def classify_ytdlp_failure(text):
    low = text.lower()
    auth_terms = ["cookies are no longer valid", "cookie", "login required", "checkpoint", "challenge_required"]
    rate_terms = ["rate-limit", "rate limit", "http error 429", "too many requests"]
    unavailable_terms = ["http error 400", "not available", "page isn't available", "requested content is not available", "unable to extract video url"]
    if any(x in low for x in rate_terms):
        return "RATE_LIMITED", True
    if any(x in low for x in auth_terms) and ("login" in low or "invalid" in low or "challenge" in low or "checkpoint" in low):
        return "AUTH_EXPIRED", True
    if any(x in low for x in unavailable_terms):
        return "UNAVAILABLE_OR_BROKEN", False
    return "DOWNLOAD_FAILED", False


def run_cmd(cmd, log_path, env=None):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    log_path.write_text(proc.stdout or "", encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout or ""


def find_source(run_dir):
    exact = run_dir / "source.mp4"
    if exact.exists():
        return exact
    candidates = sorted(run_dir.glob("source.*"))
    for p in candidates:
        if p.suffix.lower() in {".mp4", ".mkv", ".webm", ".mov"} and ".fdash-" not in p.name:
            return p
    return None


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def write_record(run_dir, record, workspace):
    rec = run_dir / "record.json"
    rec.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    results = workspace / "results.jsonl"
    with results.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return rec


def process_one(url, cfg, cfg_path):
    paths = cfg["paths"]
    workspace = Path(paths["workspace"])
    runs = workspace / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    rid = reel_id(url)
    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    run_dir = runs / f"{rid}_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    ylog = run_dir / "yt_dlp.log.txt"
    tlog = run_dir / "transcribe.log.txt"
    vlog = run_dir / "visual.log.txt"
    transcript_path = run_dir / "transcript.json"
    visual_path = run_dir / "visual.json"
    keyframes = run_dir / "keyframes"
    contact = run_dir / "contact_sheet.jpg"

    y = cfg["yt_dlp"]
    cmd = [
        "yt-dlp",
        "--cookies", paths["cookies"],
        "--sleep-requests", str(y["sleep_requests"]),
        "--sleep-interval", str(y["sleep_interval"]),
        "--max-sleep-interval", str(y["max_sleep_interval"]),
        "--no-abort-on-error",
        "--no-playlist",
        "--match-filters", "playlist_count <=? 1",
        "--write-info-json",
        "-f", y["format"],
        "--merge-output-format", y["merge_output_format"],
        "-o", str(run_dir / "source.%(ext)s"),
        url,
    ]
    rc, output = run_cmd(cmd, ylog)

    source = find_source(run_dir)
    if not source:
        low = output.lower()
        if "downloading playlist" in low and "does not pass filter" in low:
            status, halt = "SKIPPED_CAROUSEL", False
        else:
            status, halt = classify_ytdlp_failure(output)
        record = {
            "url": url, "id": rid, "status": status, "halt_batch": halt,
            "processed_at": now_stamp(), "creator": None, "caption": None,
            "duration": None, "language": None, "language_probability": None,
            "transcript": "", "ocr_text": "", "visual_class": None,
            "visual_coverage_pass": None, "visual_span_coverage_ratio": None,
            "visual_end_coverage_ratio": None, "keyframe_count": 0,
            "contact_sheet": None, "error": output.strip()[-1500:] if output else status,
            "evidence_dir": str(run_dir),
        }
        write_record(run_dir, record, workspace)
        return record

    # Transcription
    w = cfg["whisper"]
    tcmd = [
        paths["whisper_python"], str(HERE / "transcribe.py"),
        "--input", str(source), "--output", str(transcript_path), "--log", str(tlog),
        "--model", w["model"], "--device", w["device"], "--compute-type", w["compute_type"],
        "--beam-size", str(w["beam_size"]),
    ]
    if w.get("vad_filter", True):
        tcmd.append("--vad-filter")
    trc = subprocess.run(tcmd).returncode

    # Visual evidence. Exit code 3 means partial coverage, not a crash.
    vcmd = [
        paths["ocr_python"], str(HERE / "visual_evidence.py"),
        "--input", str(source), "--output", str(visual_path), "--log", str(vlog),
        "--keyframe-dir", str(keyframes), "--contact-sheet", str(contact),
        "--config-json", str(cfg_path),
    ]
    vrc = subprocess.run(vcmd).returncode

    info_candidates = list(run_dir.glob("source.info.json"))
    info = read_json(info_candidates[0], {}) if info_candidates else {}
    transcript = read_json(transcript_path, {})
    visual = read_json(visual_path, {})

    if trc != 0 or not transcript:
        status = "TRANSCRIPTION_FAILED"
        err = tlog.read_text(encoding="utf-8", errors="replace") if tlog.exists() else "Transcription process failed"
    elif vrc not in (0, 3) or not visual:
        status = "VISUAL_FAILED"
        err = vlog.read_text(encoding="utf-8", errors="replace") if vlog.exists() else "Visual process failed"
    elif not visual.get("visual_coverage_pass", False):
        status = "PARTIAL_VISUAL"
        err = "Visual coverage validation failed; source retained for diagnosis."
    else:
        status = "SUCCESS"
        err = None

    record = {
        "url": url,
        "id": info.get("id", rid),
        "status": status,
        "halt_batch": False,
        "processed_at": now_stamp(),
        "creator": info.get("uploader") or info.get("channel"),
        "caption": info.get("description"),
        "duration": info.get("duration") or visual.get("duration"),
        "language": transcript.get("language"),
        "language_probability": transcript.get("language_probability"),
        "transcript": transcript.get("text", ""),
        "ocr_text": visual.get("ocr_text", ""),
        "visual_class": visual.get("visual_class"),
        "visual_coverage_pass": visual.get("visual_coverage_pass"),
        "visual_span_coverage_ratio": visual.get("visual_span_coverage_ratio"),
        "visual_end_coverage_ratio": visual.get("visual_end_coverage_ratio"),
        "first_keyframe_timestamp": visual.get("first_keyframe_timestamp"),
        "last_keyframe_timestamp": visual.get("last_keyframe_timestamp"),
        "keyframe_count": visual.get("keyframe_count", 0),
        "contact_sheet": visual.get("contact_sheet"),
        "error": err,
        "evidence_dir": str(run_dir),
    }
    write_record(run_dir, record, workspace)

    cleanup = cfg.get("cleanup", {})
    if status == "SUCCESS" and cleanup.get("delete_source_video_after_success", True):
        try:
            source.unlink()
        except OSError:
            pass
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--batch-file")
    ap.add_argument("--config")
    args = ap.parse_args()
    if not args.url and not args.batch_file:
        ap.error("Provide --url or --batch-file")

    cfg, cfg_path = load_cfg(args.config)
    urls = []
    if args.url:
        urls.append(args.url.strip())
    if args.batch_file:
        for line in Path(args.batch_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)

    any_fail = False
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        rec = process_one(url, cfg, cfg_path)
        print(json.dumps({k: rec.get(k) for k in ["id", "status", "visual_end_coverage_ratio", "evidence_dir"]}, ensure_ascii=False))
        if rec.get("halt_batch"):
            print(f"CIRCUIT BREAKER: {rec['status']}. Batch halted.")
            raise SystemExit(20)
        if rec["status"] not in {"SUCCESS", "UNAVAILABLE_OR_BROKEN", "SKIPPED_CAROUSEL"}:
            any_fail = True
    raise SystemExit(2 if any_fail else 0)


if __name__ == "__main__":
    main()
