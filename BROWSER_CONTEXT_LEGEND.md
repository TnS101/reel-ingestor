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
- `PROJECT_TRACKER.xlsx`
- local Git state snapshot when available

Attach `docs/DECISIONS.md`, research, reports, or artifacts only when they can change the current decision.

## Worker session

Generate with `scripts/make_browser_worker_context.ps1` after the Plan is approved and Git worktree is clean.

Core contents:

- `BROWSER_WORKER_RULES.md`
- `plan.md`
- `ARCHITECTURE.md`
- `PROJECT_STATE.md`
- `docs/TEST_STRATEGY.md`
- `GIT_BASELINE.txt`
- only the source/contracts explicitly relevant to the Plan

The Worker does not need the spreadsheet tracker unless a Plan explicitly concerns tracker automation.

Do not upload secrets, cookies, `.git`, venvs, run folders, source video, GOLD benchmark corpora, live corpus DBs, or unrelated repository files.

## Review session

Review stays in the **same Architect chat that owns the Plan**. Generate `review_context.zip` with `scripts/make_review_context.ps1` after applying the Worker bundle and running local verification.

The review context contains actual `git diff`, status, the implementation report, and local verification evidence.

## ChatGPT Project knowledge warning

Do not permanently upload evolving `PROJECT_STATE.md`, `plan.md`, `PROJECT_TRACKER.xlsx`, `ARCHITECTURE.md`, or similar state files into Project Knowledge unless they are continuously replaced.

Stale injected context is more dangerous than a fresh small handoff ZIP.
