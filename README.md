# Reel Ingestor v0.2

Local Instagram Reel evidence ingestor for the current UNFAIR ADVANTAGE workflow.

## What changed from v0.1 behavior

The validated v0.1 run exposed a critical bug: the visual selector could exhaust its fixed keyframe budget in the first part of a fast-cut Reel. An 81.6s Reel produced 24 keyframes but the last one was at 26s, so the run was incorrectly marked SUCCESS while missing the tutorial section.

v0.2 fixes that by:

- scanning the ENTIRE timeline;
- dividing the whole duration into temporal windows;
- selecting one informative representative frame per window;
- using change + edge density + sharpness to rank frames inside each window;
- validating start/end/span timeline coverage;
- returning PARTIAL_VISUAL rather than SUCCESS if coverage is insufficient;
- writing useful Whisper and visual logs;
- suppressing the harmless Paddle `ccache` warning;
- keeping the source video when visual/transcription fails or is partial;
- deleting the source MP4 after a fully successful run to conserve disk space;
- preserving sequential processing and the acquisition circuit breaker.

## Existing components reused

No new Python environment is required.

- global yt-dlp
- existing Video Cloner `venv` for faster-whisper/OpenCV
- existing Video Cloner `venv_ocr` for PaddleOCR
- global ffmpeg/ffprobe

## First regression test

In PowerShell:

```powershell
Get-ChildItem -Path . -Recurse -File | Unblock-File
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\run_one.ps1 "https://www.instagram.com/p/DeDeeQ7x0dV/"
```

Expected acceptance criteria:

- status = SUCCESS
- `visual_coverage_pass = true`
- `visual_end_coverage_ratio >= 0.90`
- `visual_span_coverage_ratio >= 0.85`
- last keyframe reaches the final ~10% of the Reel, not ~26s
- tutorial-stage frames after 35s are present in `contact_sheet.jpg`

## Output

Default workspace:

`C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor`

Per-run evidence:

- `record.json`
- `source.info.json`
- `transcript.json`
- `transcribe.log.txt`
- `visual.json`
- `visual.log.txt`
- `keyframes\...`
- `contact_sheet.jpg`

Global append-only result stream:

- `results.jsonl`

## Status semantics

- `SUCCESS`: download + transcript + visual evidence passed timeline coverage.
- `PARTIAL_VISUAL`: transcript succeeded, but visual timeline coverage failed; source retained.
- `TRANSCRIPTION_FAILED`: Whisper failed; source retained.
- `VISUAL_FAILED`: OCR/keyframe pipeline failed; source retained.
- `UNAVAILABLE_OR_BROKEN`: deleted/private/broken Reel-like failure; safe to continue.
- `SKIPPED_CAROUSEL`: carousel rejected; safe to continue.
- `RATE_LIMITED`: circuit breaker; halt batch.
- `AUTH_EXPIRED`: circuit breaker; halt batch.

## Important

The uploaded `reel_ingestor_v0_1.zip` available to the patching environment contained only an empty directory, so this v0.2 package is a compatibility reconstruction based on the validated v0.1 run artifacts and the interface used in this project. It is not a literal line-by-line diff of your local v0.1 source tree.
