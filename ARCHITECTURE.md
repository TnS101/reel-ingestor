# ARCHITECTURE.md — Reel Ingestor

- STATUS: APPROVED CURRENT ARCHITECTURE
- ARCHITECTURE VERSION: A1
- LAST UPDATED: 2026-10-07
- REPO ROOT: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor\Extract Reel Data`
- EVIDENCE WORKSPACE: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor`

## 1. System purpose

Turn saved Instagram Reel URLs into durable local evidence, then convert that evidence into structured canonical knowledge that can later be searched, manipulated, compared, and served through a lightweight local app.

Current end-to-end shape:

```text
Instagram Reel URL(s)
  -> local acquisition / transcript / visual evidence
  -> local evidence run folder
  -> manual Browser GPT-5.6 Sol Knowledge Extractor
  -> schema-valid canonical knowledge JSON
  -> [CURRENT NEXT LAYER] local corpus + manipulation records
  -> [LATER] mini web app / queue / search UI / optional API automation
```

## 2. Repository boundary

The Git repository is the **code/control root only**:

`C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor\Extract Reel Data`

The parent Reel Ingestor workspace intentionally remains outside the Git repo and contains generated/runtime material such as:

- `runs/`
- `results.jsonl`
- `Gold Results/`
- `browser_production_pack_v1/`

Do not move generated evidence into Git merely for convenience.

## 3. Current code components

| Component | Responsibility | Stability |
|---|---|---|
| `reel_ingestor.py` | Orchestrates URL/batch processing, yt-dlp acquisition, statuses, record writing, cleanup and circuit-breaker behavior. | FROZEN KNOWN-GOOD unless a proven bug/change requires a plan. |
| `transcribe.py` | faster-whisper transcription using the existing Video Cloner Python environment. | STABLE |
| `visual_evidence.py` | Whole-timeline scan, temporal-window frame selection, OCR, keyframes/contact sheet, visual coverage validation. | FROZEN KNOWN-GOOD unless a proven bug/change requires a plan. |
| `run_one.ps1` | One-Reel launcher. | STABLE |
| `run_batch.ps1` | Sequential batch launcher from a text file. | STABLE |
| `config.json` | Local runtime paths + yt-dlp/Whisper/visual thresholds/cleanup policy. | MACHINE-SPECIFIC CURRENT CONFIG; do not casually generalize during unrelated plans. |

## 4. External/runtime dependencies already accepted

- global `yt-dlp`
- global `ffmpeg` / `ffprobe`
- existing Video Cloner `venv` for faster-whisper/OpenCV
- existing Video Cloner `venv_ocr` for PaddleOCR
- authenticated Instagram cookie file stored outside the repo
- Browser GPT-5.6 Sol for manual canonical knowledge extraction

Do not replace or upgrade these merely for cleanliness.

## 5. Stable ingestion contracts to preserve

### Status semantics

- `SUCCESS`
- `PARTIAL_VISUAL`
- `TRANSCRIPTION_FAILED`
- `VISUAL_FAILED`
- `UNAVAILABLE_OR_BROKEN`
- `SKIPPED_CAROUSEL`
- `RATE_LIMITED` -> halt batch
- `AUTH_EXPIRED` -> halt batch

### Coverage gate

Current known-good thresholds:

- `visual_end_coverage_ratio >= 0.90`
- `visual_span_coverage_ratio >= 0.85`

### Safety/cleanup

- Instagram processing remains sequential.
- No proxy/account rotation/evasion mechanism.
- Source media is deleted after fully successful extraction.
- Source media is retained on partial/failure for diagnosis.
- Runtime evidence remains outside the Git code root.

## 6. Frozen Knowledge Extractor contracts

Git-tracked source-of-truth copies live under `contracts/`:

- `knowledge_schema_v1.json` — schema version `1.0.0`, frozen Production v1.
- `BROWSER_SOL_PRODUCTION_PROMPT_v1_1.txt` — prompt version `browser_production_v1.1`, frozen Production v1.
- `FROZEN_CONTRACTS.json` — hashes/status.

Upgrade these only when production evidence exposes a real blocker. Do not version-bump for cosmetic cleanup or theoretical future-proofing.

Canonical knowledge and raw evidence are separate. **Derived manipulations never overwrite canonical knowledge.**

## 7. Current architecture work: Step 5.4

The next product layer must support:

1. local corpus storage/query over real production `knowledge_*.json` outputs;
2. derived manipulation outputs such as `HOW_TO`, `STEP_BY_STEP`, `REVERSE_ENGINEER`, `READ_BETWEEN_LINES`, `RECREATE_REEL`, `ADAPT_FORMAT`, and custom outputs;
3. retention of manipulation prompt/user intent/context/output history;
4. immutable linkage to the exact canonical knowledge version/hash used;
5. separation of derived outputs from canonical knowledge.

The exact storage implementation is **not yet approved by this architecture file**. It belongs to a bounded Step 5.4 Plan, with reuse/native mechanisms checked only if that Plan introduces a genuine build-vs-reuse decision.

## 8. Current non-goals

Do not start these until a later accepted Plan makes them Critical Path:

- automate Browser ChatGPT extraction;
- build the mini web app/UI;
- scheduling/local queue automation;
- health/status dashboard;
- TikTok/YouTube Shorts/X adapters;
- environment cleanup/venv deletion;
- ingestion tuning without a proven regression;
- multi-account/proxy evasion;
- arbitrary schema/prompt redesign.

## 9. Security / secrets boundary

- Cookie/auth files stay outside Git.
- Never include cookies or credentials in browser context ZIPs or reports.
- Do not commit `.env`, credentials, secrets, source media, generated run folders, or handoff bundles.
- Local absolute paths are not secrets, but avoid propagating them into unrelated artifacts when unnecessary.

## 10. Architecture-change triggers

Open an explicit architecture decision before:

- changing the canonical knowledge schema;
- moving generated run evidence into a database or repo;
- introducing a persistent database/app server;
- automating Browser model calls through APIs;
- adding a new platform adapter;
- replacing the evidence extraction stack;
- changing security/auth handling;
- introducing a new recurring paid runtime/service dependency.
