# PROJECT_STATE.md — Reel Ingestor

- STATE VERSION: S1
- LAST UPDATED: 2026-10-07
- REPO ROOT: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor\Extract Reel Data`
- LIVE HUMAN TRACKER: Google Sheet maintained by the human; not duplicated in Git

## Objective

Build a lightweight, reliable short-form knowledge system:

`Reel URL -> local evidence -> canonical knowledge -> searchable corpus -> derived manipulations -> later mini web app`

## Win Condition

A saved Reel can be ingested safely, converted into high-quality evidence-grounded canonical knowledge, stored/queryable locally, and transformed into useful outputs without rewatching the Reel or mutating the canonical artifact.

## Accepted current position

### Acquisition / evidence

- Local Reel Ingestor v0.2 is the frozen known-good acquisition/evidence baseline.
- Whole-timeline visual coverage regression was fixed and validated.
- Valid batch test reached 21/21 successful valid Reels; deleted/unavailable items were handled separately.
- Circuit-breaker behavior for auth/rate-limit remains part of the safety contract.
- GPU/Whisper/Paddle environment verification is closed work; do not reopen casually.

### Knowledge layer

- Step 5.1: `knowledge_schema_v1.0.0` LOCKED.
- Step 5.2: 10-Reel human-approved GOLD benchmark COMPLETE / LOCKED.
- Step 5.3: Browser Sol production extractor COMPLETE / 100%.
- `browser_production_v1.1` is frozen Production v1.
- Fresh non-GOLD production validation passed on four diverse Reels, including bad-ASR visual/caption-heavy and complex multimodal workflows.
- Prompt/schema may be upgraded later **only when production evidence requires it**.

## Current Critical Path

Before any Step 5.4 product code change:

**P001_GIT_BASELINE -> establish a clean Git repository/checkpoint around the existing working code + this control overlay.**

After P001 is accepted, the next product Plan will begin Step 5.4:

**local corpus storage/query + manipulation record contract using real production knowledge JSONs.**

## Current Plan

- PLAN ID: `P001_GIT_BASELINE`
- ARCHITECT SESSION: `ARCH-P001_GIT_BASELINE`
- WORKER: HUMAN LOCAL / no Browser Worker required
- STATUS: READY_FOR_HUMAN_EXECUTION
- ACCEPTED COMMIT: NONE — repository not initialized yet

## Main constraint

The technical model/extraction quality is no longer the bottleneck. The current control-plane constraint is that the working code has no Git baseline, so future Browser-generated patches would be harder to review, roll back, and attribute safely.

## Known stable contracts

- Ingestion status semantics and circuit breakers from Architecture A1.
- Visual coverage thresholds 0.90 end / 0.85 span.
- Canonical knowledge schema v1.0.0 frozen.
- Browser production prompt v1.1 frozen.
- Canonical knowledge is immutable relative to derived manipulations.
- Runtime evidence stays outside the code repo.

## Current external workspace

Parent workspace: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor`

Known runtime/support areas outside repo include:

- `runs/`
- `results.jsonl`
- `Gold Results/`
- `browser_production_pack_v1/`

## Current risks / SPOFs

- Instagram auth/cookies can expire and halt acquisition.
- Browser Sol extraction is manual and therefore not unattended automation yet; this is accepted for now.
- The project currently depends on existing Video Cloner Python environments; cleanup is deferred until usage is audited.
- Without the Git baseline, browser patch application would have weak rollback/diff control — P001 fixes this.

## Deferred / not current

- mini web app/UI;
- automated Browser/API extraction;
- scheduling/queue automation;
- health dashboard;
- disk-retention cleanup beyond current successful source-video deletion;
- duplicate venv cleanup;
- multi-platform adapters.

## Intended next Plan after P001

Not yet created. Purpose only:

`Define and prove the smallest local corpus + manipulation-record storage/query boundary for Step 5.4, using real production knowledge JSONs.`

The fresh Architect session after P001 acceptance chooses the exact plan.
