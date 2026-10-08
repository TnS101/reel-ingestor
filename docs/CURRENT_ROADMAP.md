# CURRENT_ROADMAP.md — Stable Phase Skeleton

- LAST UPDATED: 2026-10-08

This is not a low-level permanent master plan. It preserves the currently accepted phase skeleton from `PROJECT_TRACKER.xlsx`.

## Completed

### 5.3 — Operationalize Browser Sol production extractor + human quality loop

- STATUS: DONE / 100%
- RESULT: Browser Sol production workflow validated on 4 fresh non-GOLD Reels.
- AUDIT: 2 representative raw-evidence spot audits passed.
- FROZEN: knowledge schema v1.0.0 + Browser production prompt v1.1.

### P001_GIT_BASELINE — Project control prerequisite

- STATUS: ACCEPTED / CLOSED
- BASELINE: `f077a4a30ace95aa91936a46f42a506bd30a9ee3`
- RESULT: private Git repository on `main`, clean rollback checkpoint, remote pushed.

## Current Critical Product Step

### 5.4 — Build manipulation + local corpus layer — P0

Current Plan:

`P002_CORPUS_STORAGE`

- STATUS: `APPROVED — READY_FOR_BROWSER_WORKER`
- IMPLEMENTATION BASELINE: exact approved Plan checkpoint SHA supplied in the Architect Worker handoff

First proof boundary:

- local corpus/storage + query over real Production v1 canonical knowledge JSONs;
- Python standard-library SQLite + filesystem provenance;
- immutable SHA-256-addressed artifact versions;
- same Reel ID may retain multiple different immutable hashes;
- deterministic list/get/search with machine-readable JSON;
- canonical inputs remain immutable;
- runtime corpus stays outside Git;
- Worker implementation patch is limited to `corpus_store.py` + `tests/test_corpus_store.py`.

Manipulation generation is deliberately **after** P002 acceptance.

Expected next Plan after P002:

`P003_MANIPULATION_RECORDS`

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

Document cookie refresh, yt-dlp update, rollback and common recovery when useful; not current Critical Path.

### 7.1 — Measure useful-insight yield by platform — P3 — Deferred

Do after stable corpus exists.

### 7.2 — Add TikTok / YouTube Shorts / X adapters — P3 — Deferred

Only after Instagram workflow is stable and a real use case exists.
