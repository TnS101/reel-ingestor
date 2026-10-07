# Browser Context Legend — Reel Ingestor

## Architect session

Generate with `scripts/make_browser_context.ps1`.

Core contents:

- `ARCHITECT_RULES.md`
- `PROJECT_STATE.md`
- `ARCHITECTURE.md`
- `plan.md`
- `docs/CURRENT_ROADMAP.md`
- `docs/TRACKER_POLICY.md`
- local Git state snapshot when available

Attach `docs/DECISIONS.md`, research, reports, or artifacts only when they can change the current decision.

## Worker session

Generate with `scripts/make_browser_worker_context.ps1` after the plan is approved and Git worktree is clean.

Core contents:

- `BROWSER_WORKER_RULES.md`
- `plan.md`
- `ARCHITECTURE.md`
- `PROJECT_STATE.md`
- `docs/TEST_STRATEGY.md`
- `GIT_BASELINE.txt`
- only the source/contracts explicitly relevant to the plan

Do not upload secrets, cookies, `.git`, venvs, run folders, source video, Gold benchmark corpora, or unrelated repository files.

## Review session

Review stays in the **same Architect chat that created the plan**. Generate `review_context.zip` with `scripts/make_review_context.ps1` after applying the Worker bundle and running local verification.

The review context contains actual `git diff`, status, the implementation report, and local verification evidence.

## ChatGPT Project knowledge warning

Do not permanently upload evolving `PROJECT_STATE.md`, `plan.md`, `ARCHITECTURE.md`, or similar state files into Project Knowledge unless they are continuously replaced. Stale injected context is more dangerous than a fresh small handoff ZIP.
