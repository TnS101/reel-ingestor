import argparse
import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--compute-type", default="float16")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--vad-filter", action="store_true")
    args = ap.parse_args()

    inp = Path(args.input)
    out = Path(args.output)
    log = Path(args.log)
    out.parent.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(
        str(inp), beam_size=args.beam_size, vad_filter=args.vad_filter
    )

    items = []
    text_parts = []
    max_end = 0.0
    for s in segments:
        t = s.text.strip()
        if not t:
            continue
        items.append({"start": round(float(s.start), 3), "end": round(float(s.end), 3), "text": t})
        text_parts.append(t)
        max_end = max(max_end, float(s.end))

    payload = {
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "text": " ".join(text_parts),
        "segments": items,
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    log.write_text(
        f"WHISPER PASS | audio_end={max_end:.2f}s | language={info.language} "
        f"| p={float(info.language_probability):.4f} | segments={len(items)} "
        f"| device={args.device} | compute={args.compute_type}\n",
        encoding="utf-8",
    )
    print(log.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
