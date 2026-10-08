# PROJECT_STATE.md — Reel Ingestor

- STATE VERSION: S3
- LAST UPDATED: 2026-10-08
- REPO ROOT: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor\Extract Reel Data`
- HUMAN TRACKER: `PROJECT_TRACKER.xlsx` in the Git repository
- TRACKER UPDATE RULE: update/commit at accepted Plan boundaries, not continuously during implementation

## Objective

Build a lightweight, reliable short-form knowledge system:

`Reel URL -> local evidence -> canonical knowledge -> searchable local corpus -> derived manipulations -> later mini web app`

## Win Condition

A saved Reel can be ingested safely, converted into high-quality evidence-grounded canonical knowledge, stored/queryable locally, and transformed into useful outputs without rewatching the Reel or mutating the canonical artifact.

## Accepted current position

### Acquisition / evidence

- Local Reel Ingestor v0.2 is the frozen known-good acquisition/evidence baseline.
- Whole-timeline visual coverage regression was fixed and validated.
- Mixed validation reached 21/21 successful accessible Reels; deleted/unavailable items were handled separately.
- Circuit-breaker behavior for auth/rate-limit remains part of the safety contract.
- GPU/Whisper/Paddle environment verification is closed work; do not reopen casually.

### Knowledge layer

- Step 5.1: `knowledge_schema_v1.0.0` LOCKED.
- Step 5.2: 10-Reel human-approved GOLD benchmark COMPLETE / LOCKED.
- Step 5.3: Browser Sol production extractor COMPLETE / 100%.
- `browser_production_v1.1` is frozen Production v1.
- Four fresh non-GOLD production validations passed.
- Two representative raw-evidence spot audits passed.
- Prompt/schema may be upgraded later only when production evidence requires it.

### Project control

- `P001_GIT_BASELINE`: ACCEPTED / CLOSED.
- P001 accepted baseline commit: `f077a4a30ace95aa91936a46f42a506bd30a9ee3`.
- P002 implementation baseline: exact approved Plan checkpoint SHA supplied in the Browser Worker handoff; do not use moving `main`.
- Branch: `main`.
- Private GitHub remote: `TnS101/reel-ingestor`.
- `be51d4800320edc2bfdcca075fbfb358bc137013` is the historical P001-close/control-sync commit on which the P002 draft was prepared; it is not the Worker implementation baseline after Plan approval.
- Git + direct verification evidence are technical truth.
- `PROJECT_TRACKER.xlsx` is the versioned human-facing project tracker.

## Current Critical Path

Step 5.4 is active.

Current bounded target:

**P002_CORPUS_STORAGE -> prove the smallest local corpus/storage + query layer using real Production v1 canonical knowledge JSONs.**

Manipulation generation comes only after this storage/query boundary passes.

## Current Plan

- PLAN ID: `P002_CORPUS_STORAGE`
- ARCHITECT SESSION: `ARCH-P002_CORPUS_STORAGE`
- WORKER SESSION: `BWORK-P002_CORPUS_STORAGE`
- STATUS: `APPROVED — READY_FOR_BROWSER_WORKER`
- BASELINE BRANCH: `main`
- BASELINE COMMIT: exact approved Plan checkpoint SHA supplied in the Architect Worker handoff
- WORKER REPO PATCH BOUNDARY: `corpus_store.py` + `tests/test_corpus_store.py` only

## Main constraint

Canonical extraction quality is no longer the bottleneck.

The current constraint is the absence of a durable local corpus/index for real Production v1 knowledge artifacts. Manipulation functionality should not be built on ad-hoc loose-file assumptions.

## Accepted storage direction for P002

- Python standard-library `sqlite3`.
- Runtime corpus DB under the parent Reel Ingestor workspace, outside Git.
- Filesystem paths + SHA-256 provenance retained.
- Artifact identity is exact imported-file SHA-256.
- Exact re-import is idempotent.
- Different hashes for the same Reel ID coexist as separate immutable versions.
- Canonical knowledge remains immutable.
- List/get/search expose machine-readable JSON and exact Reel ID + artifact hash identity.
- No media/image BLOB storage.
- No external DB/ORM/vector/FTS/validation dependency unless a later measured need justifies it.

## Known stable contracts

- Ingestion status semantics and circuit breakers from Architecture A1.
- Visual coverage thresholds 0.90 end / 0.85 span.
- Canonical knowledge schema v1.0.0 frozen.
- Browser production prompt v1.1 frozen.
- Canonical knowledge is immutable relative to derived manipulations.
- Runtime evidence/corpus data stays outside the code repo.
- P002 does not modify ingestion/config/frozen-contract files.

## Current external workspace

Parent workspace:

`C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor`

Known runtime/support areas outside repo include:

- `runs/`
- `results.jsonl`
- `Gold Results/`
- `browser_production_pack_v1/`
- future `corpus/`

## Current risks / SPOFs

- Instagram auth/cookies can expire and halt acquisition.
- Browser Sol extraction is manual; accepted until manual transfer becomes a measured bottleneck.
- Existing Video Cloner Python environments remain dependencies; cleanup is deferred pending usage audit.
- Corpus design must not create a second mutable source of truth or silently overwrite canonical artifact versions.
- Same-Reel version retrieval must remain deterministic so future manipulations can link to an exact canonical hash.
- Project-state drift is controlled through Git checkpoints, bounded Plans, fresh Browser sessions and the repo-tracked tracker.

## Deferred / not current

- manipulation generation until P002 passes;
- FTS/vector/semantic search until measured need;
- mini web app/UI;
- automated Browser/API extraction;
- scheduling/queue automation;
- health dashboard;
- broader disk-retention cleanup;
- duplicate venv cleanup;
- multi-platform adapters.
