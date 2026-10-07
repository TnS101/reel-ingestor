# CURRENT_ROADMAP.md — Stable Phase Skeleton

- LAST UPDATED: 2026-10-07

This is not a low-level permanent master plan. It only preserves the currently accepted phase skeleton from the live tracker.

## Completed

### 5.3 — Operationalize Browser Sol production extractor + human quality loop

- STATUS: DONE / 100%
- RESULT: Browser Sol production workflow validated on fresh non-GOLD Reels.
- FROZEN: knowledge schema v1.0.0 + Browser production prompt v1.1.

## Current Critical Product Step

### 5.4 — Build manipulation + local corpus layer — P0

Acceptance target:

Canonical knowledge can be transformed into `HOW_TO`, `STEP_BY_STEP`, `REVERSE_ENGINEER`, `READ_BETWEEN_LINES`, `RECREATE_REEL`, `ADAPT_FORMAT`, and custom outputs, with prompt/context/output history retained. Derived outputs stay separate from canonical knowledge.

Current prerequisite: complete `P001_GIT_BASELINE` before product implementation.

## Deferred / later

### 6.1 — Automate local queue / scheduling — P2 — Deferred

Do with the future local app/queue only after 5.4 proves downstream value.

### 6.2 — Health / status dashboard — P2 — Deferred

Implement naturally with the future UI.

### 6.3 — Finalize disk-retention policy — P1 — Not Started

Current v0.2 already deletes source media after SUCCESS. Later decide bounded retention for keyframes/contact sheets/logs/old runs.

### 6.4 — Audit duplicate Video Cloner environments — P2 — Not Started

Read-only usage/dependency audit before deleting anything.

### 6.5 — Recovery / operations playbook — P1 — Not Started

Document cookie refresh, yt-dlp update, rollback and common recovery when it becomes useful; not current Critical Path.

### 7.1 — Measure useful-insight yield by platform — P3 — Deferred

Do after stable corpus exists.

### 7.2 — Add TikTok / YouTube Shorts / X adapters — P3 — Deferred

Only after Instagram workflow is stable and a real use case exists.
