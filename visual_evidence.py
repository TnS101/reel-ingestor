import argparse
import json
import math
import os
import re
import warnings
from difflib import SequenceMatcher
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
from paddleocr import PaddleOCR

warnings.filterwarnings("ignore", message=".*No ccache found.*")


def norm_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def signature(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (180, 320), interpolation=cv2.INTER_AREA)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray


def frame_scores(frame, prev_sig):
    sig = signature(frame)
    if prev_sig is None:
        change = 1.0
    else:
        change = float(np.mean(cv2.absdiff(sig, prev_sig)) / 255.0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (270, 480), interpolation=cv2.INTER_AREA)
    edges = cv2.Canny(small, 80, 160)
    edge_density = float(np.mean(edges > 0))
    sharpness = float(cv2.Laplacian(small, cv2.CV_64F).var())
    sharp_norm = min(sharpness / 1000.0, 1.0)

    # Change favors transitions; edge density/sharpness favors UI/text/screenshots.
    info_score = 0.60 * change + 0.25 * edge_density + 0.15 * sharp_norm
    return sig, change, edge_density, sharpness, info_score


def extract_keyframes(video_path, keyframe_dir, cfg):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS))
    count = float(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps <= 0 or count <= 0:
        raise RuntimeError("Invalid video FPS/frame count")
    duration = count / fps

    target = int(round(duration / float(cfg["target_spacing_seconds"])))
    target = max(int(cfg["min_target_frames"]), min(int(cfg["max_target_frames"]), target))
    target = max(1, target)
    window = duration / target
    scan_interval = float(cfg["scan_interval_seconds"])

    candidates = [[] for _ in range(target)]
    prev_sig = None
    t = 0.0
    while t <= duration + 1e-6:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
        ok, frame = cap.read()
        if ok:
            sig, change, edge_density, sharpness, info_score = frame_scores(frame, prev_sig)
            prev_sig = sig
            idx = min(target - 1, int(t / window)) if window > 0 else 0
            candidates[idx].append(
                {
                    "timestamp": t,
                    "frame": frame.copy(),
                    "change_score": change,
                    "edge_density": edge_density,
                    "sharpness": sharpness,
                    "info_score": info_score,
                }
            )
        t += scan_interval
    cap.release()

    selected = []
    keyframe_dir.mkdir(parents=True, exist_ok=True)
    for i, bucket in enumerate(candidates):
        if not bucket:
            continue
        # Prefer informative frames, but add a mild center-of-window bonus so cuts at boundaries
        # do not systematically dominate every selection.
        center = (i + 0.5) * window
        def rank(c):
            distance = abs(c["timestamp"] - center) / max(window, 0.001)
            center_bonus = max(0.0, 1.0 - distance) * 0.04
            return c["info_score"] + center_bonus
        best = max(bucket, key=rank)
        name = f"kf_{len(selected):03d}_{best['timestamp']:07.2f}s.jpg"
        path = keyframe_dir / name
        cv2.imwrite(str(path), best["frame"], [cv2.IMWRITE_JPEG_QUALITY, 95])
        selected.append(
            {
                "index": len(selected),
                "timestamp": round(float(best["timestamp"]), 2),
                "change_score": round(float(best["change_score"]), 4),
                "edge_density": round(float(best["edge_density"]), 4),
                "sharpness": round(float(best["sharpness"]), 2),
                "info_score": round(float(best["info_score"]), 4),
                "file": str(path),
            }
        )

    if not selected:
        raise RuntimeError("No keyframes selected")

    first_ts = selected[0]["timestamp"]
    last_ts = selected[-1]["timestamp"]
    span_ratio = max(0.0, (last_ts - first_ts) / duration) if duration else 0.0
    end_ratio = max(0.0, last_ts / duration) if duration else 0.0
    start_ratio = max(0.0, 1.0 - first_ts / duration) if duration else 0.0
    return duration, selected, span_ratio, end_ratio, start_ratio


def run_ocr(frames, cfg):
    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True, show_log=False)
    results = []
    previous_norm = ""
    unique_chars = set()
    text_rich = 0

    for item in frames:
        image = cv2.imread(item["file"])
        if image is None:
            continue
        scale = float(cfg["ocr_upscale"])
        if scale != 1.0:
            image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        raw = ocr.ocr(image, cls=True)
        lines = []
        if raw:
            for page in raw:
                if not page:
                    continue
                for line in page:
                    try:
                        text = str(line[1][0]).strip()
                        conf = float(line[1][1])
                    except Exception:
                        continue
                    if text and conf >= float(cfg["ocr_confidence"]):
                        lines.append({"text": text, "confidence": round(conf, 3)})

        combined = " | ".join(x["text"] for x in lines).strip()
        current_norm = norm_text(combined)
        similarity = SequenceMatcher(None, previous_norm, current_norm).ratio() if previous_norm and current_norm else 0.0
        duplicate = bool(current_norm and similarity >= float(cfg["dedupe_similarity"]))

        if current_norm:
            unique_chars.update(current_norm)
            if len(current_norm) >= 30 or len(lines) >= 4:
                text_rich += 1
        if current_norm and not duplicate:
            previous_norm = current_norm

        results.append(
            {
                **{k: v for k, v in item.items() if k != "index"},
                "text": combined,
                "lines": lines,
                "duplicate_text": duplicate,
            }
        )

    return results, len(unique_chars), text_rich


def make_contact_sheet(frames, output_path, cols):
    if not frames:
        return None
    thumb_w, thumb_h, label_h = 300, 534, 34
    rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "black")
    draw = ImageDraw.Draw(sheet)
    for i, item in enumerate(frames):
        img = Image.open(item["file"]).convert("RGB")
        img.thumbnail((thumb_w, thumb_h))
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        px = x + (thumb_w - img.width) // 2
        py = y + (thumb_h - img.height) // 2
        sheet.paste(img, (px, py))
        label = f"{item['timestamp']:.2f}s | change {item['change_score']:.3f}"
        draw.text((x + 5, y + thumb_h + 7), label, fill="white")
    sheet.save(output_path, quality=92)
    return str(output_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--keyframe-dir", required=True)
    ap.add_argument("--contact-sheet", required=True)
    ap.add_argument("--config-json", required=True)
    args = ap.parse_args()

    video = Path(args.input)
    output = Path(args.output)
    log = Path(args.log)
    keyframe_dir = Path(args.keyframe_dir)
    contact_sheet = Path(args.contact_sheet)
    cfg = json.loads(Path(args.config_json).read_text(encoding="utf-8"))["visual"]

    duration, selected, span_ratio, end_ratio, start_ratio = extract_keyframes(video, keyframe_dir, cfg)
    ocr_frames, unique_chars, text_rich = run_ocr(selected, cfg)
    contact = make_contact_sheet(selected, contact_sheet, int(cfg["contact_sheet_columns"]))

    nondup = [x for x in ocr_frames if x.get("text") and not x.get("duplicate_text")]
    ocr_text = "\n".join(f"[{x['timestamp']:07.2f}] {x['text']}" for x in nondup)

    coverage_pass = (
        end_ratio >= float(cfg["min_end_coverage_ratio"])
        and span_ratio >= float(cfg["min_span_coverage_ratio"])
    )
    # Conservative heuristic. It is evidence classification, not semantic understanding.
    visual_class = "VISUAL_RICH" if text_rich >= max(3, len(selected) // 5) else "VISUAL_LIGHT"

    payload = {
        "duration": round(duration, 3),
        "keyframe_count": len(selected),
        "ocr_frame_count": len(nondup),
        "ocr_unique_characters": unique_chars,
        "text_rich_frames": text_rich,
        "visual_class": visual_class,
        "visual_coverage_pass": coverage_pass,
        "visual_span_coverage_ratio": round(span_ratio, 4),
        "visual_end_coverage_ratio": round(end_ratio, 4),
        "visual_start_coverage_ratio": round(start_ratio, 4),
        "first_keyframe_timestamp": selected[0]["timestamp"],
        "last_keyframe_timestamp": selected[-1]["timestamp"],
        "ocr_text": ocr_text,
        "frames": ocr_frames,
        "contact_sheet": contact,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    status = "VISUAL PASS" if coverage_pass else "VISUAL PARTIAL"
    log.write_text(
        f"{status} | duration={duration:.2f}s | keyframes={len(selected)} | "
        f"first={selected[0]['timestamp']:.2f}s | last={selected[-1]['timestamp']:.2f}s | "
        f"span_coverage={span_ratio:.3f} | end_coverage={end_ratio:.3f} | "
        f"ocr_frames={len(nondup)} | class={visual_class} | device=gpu:0\n",
        encoding="utf-8",
    )
    print(log.read_text(encoding="utf-8").strip())
    sys_exit = 0 if coverage_pass else 3
    raise SystemExit(sys_exit)


if __name__ == "__main__":
    main()
