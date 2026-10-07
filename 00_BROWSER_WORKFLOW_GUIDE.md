# Reel Ingestor — Browser Architect / Browser Worker Workflow

## Why this exists

The Reel Ingestor is still small enough to control manually, but it now has enough moving parts that chat history and ad-hoc edits will eventually create drift. This workflow installs the control system **before** the mini web app makes the repository larger.

The useful parts of the original UNFAIR ADVANTAGE bootstrap are preserved: bounded Plan Partitions, explicit authority, Git checkpoints, evidence gates, fresh context, rollback, and separation between architecture and implementation. Codex-specific rules, permanent FREE-ONLY restrictions, mandatory research on every plan, Ponytail gates, and duplicate local tracker files are intentionally removed.

## Core loop

```text
Fresh Browser Architect
  -> creates/approves one plan.md
  -> generate worker_context.zip
Fresh Browser Worker
  -> implements only that plan
  -> returns PATCH_BUNDLE.zip + IMPLEMENTATION_REPORT.md + LOCAL_VERIFY instructions
Human/local machine
  -> applies files to a clean Git worktree
  -> runs the exact local verification
  -> generate review_context.zip
Same Browser Architect
  -> reviews diff + verification + report
  -> ACCEPT / REJECT / BLOCK
  -> accepted work becomes a Git checkpoint
  -> state is synchronized and plan archived
Fresh Browser Architect for the next plan
```

## Authority

- **Human:** real objective, material risk/cost approval, credentials, destructive actions, final subjective approval, local execution where Browser ChatGPT cannot access the machine.
- **Browser Architect:** architecture, sequencing, Plan Partition creation, acceptance criteria, review, project-state synchronization, next-plan selection.
- **Browser Worker:** bounded code/document implementation for the current approved plan only. It does not choose architecture or the next step.
- **Git + local evidence:** technical truth.
- **Google Sheet:** human-facing progress mirror. It is deliberately not duplicated into this repository because a stale local spreadsheet is worse than a single live tracker.

## Hard gates

1. **NO PLAN -> NO IMPLEMENTATION.**
2. **NO CLEAN GIT BASELINE -> NO PRODUCT CODE CHANGE.**
3. **NO EVIDENCE -> NOT DONE.** Browser-generated code is only `IMPLEMENTED_PENDING_LOCAL_VERIFY` until local verification exists.
4. **NO ACCEPTED CHECKPOINT -> NO NEXT INDEPENDENT PLAN.**
5. **ONE PLAN -> ONE OBSERVABLE RESULT -> ONE VERIFICATION BOUNDARY** unless tightly coupled work genuinely shares the same proof boundary.
6. Preserve known-good behavior. Do not refactor because a cleaner abstraction is attractive.
7. One focused repair is the default. Repeated similar failure becomes an investigation, not patch stacking.

## Cost policy — adapted for this project

Existing approved Browser ChatGPT usage is part of the current workflow.

**No new recurring paid runtime/service dependency may be introduced without explicit human approval. Prefer free/local mechanisms when they satisfy the Win Condition.**

The architect must surface a paid dependency before it is added; it is not automatically rejected if the human explicitly approves it.

## Research/reuse gate — conditional

Do not perform a ritual 5–10 project OSS scan for every plan.

Run a targeted reuse/OSS scan **only when the current plan introduces a new mechanism, dependency, architecture component, or meaningful build-vs-reuse decision**. Research stops when more information is unlikely to change the route. Prefer native features, standard libraries, mature libraries, existing internal assets, and proven OSS over custom mechanisms.

## Browser Worker limitation

The Browser Worker does not operate the live Windows repository. Therefore it cannot truthfully claim a production `PASS` based only on generated code or sandbox checks.

Its strongest normal success state is:

`IMPLEMENTED_PENDING_LOCAL_VERIFY`

The human applies the returned files to the clean local Git worktree and runs the exact verification defined in `plan.md` / `LOCAL_VERIFY.md`. The Architect accepts only after reviewing the real local diff and evidence.

## Plan lifecycle

### 1. New Architect chat

From the project root:

```powershell
.\scripts\make_browser_context.ps1 -PlanId "P###_NAME"
```

Upload the generated `.handoffs\P###_NAME_architect_context.zip` to a **fresh Browser chat** and paste `prompts\BROWSER_ARCHITECT_START_PROMPT.txt`.

The Architect creates/repairs exactly one `plan.md`, synchronizes project state, and returns changed canonical files. It does not implement product code.

### 2. New Worker chat

Once the plan is approved and the worktree is clean, the Architect tells you which source files are relevant. Generate a worker context, for example:

```powershell
.\scripts\make_browser_worker_context.ps1 `
  -PlanId "P002_CORPUS_STORAGE" `
  -IncludePaths @("reel_ingestor.py", "contracts", "docs\TEST_STRATEGY.md")
```

Upload that ZIP to a **fresh Browser chat** and paste `prompts\BROWSER_WORKER_START_PROMPT.txt`.

The Worker returns a repo-relative patch bundle plus report and local verification instructions. It must stop after the current plan.

### 3. Apply + verify locally

Only apply a Worker bundle when the Git worktree still matches the plan baseline and is clean.

After applying the files:

- inspect `git diff`;
- run the exact local verification;
- save the output to a text/Markdown file, normally `.local_verify\<PLAN_ID>.md`;
- do not commit yet.

### 4. Review in the same Architect chat

Create the review bundle:

```powershell
.\scripts\make_review_context.ps1 `
  -PlanId "P002_CORPUS_STORAGE" `
  -ImplementationReport ".\IMPLEMENTATION_REPORT.md" `
  -LocalVerify ".\.local_verify\P002_CORPUS_STORAGE.md"
```

Upload the review ZIP to the **same Architect chat that created the Plan** and paste `prompts\BROWSER_ARCHITECT_REVIEW_PROMPT.txt`.

The Architect must inspect the actual diff/evidence and return `ACCEPT`, `REJECT`, or `BLOCK`.

### 5. Accept + checkpoint

Only after `ACCEPT`:

```powershell
git add -A
git commit -m "<accepted plan checkpoint>"
.\scripts\archive_plan.ps1 -PlanId "P002_CORPUS_STORAGE"
```

Then update `PROJECT_STATE.md` and the live Google Sheet, close both chats, and start the next plan in a fresh Architect chat.

## Project-specific rule

The frozen Knowledge Extractor contracts are tracked inside this repo under `contracts/` so Git can prove exactly which schema and Browser Sol prompt are production v1. The sibling `browser_production_pack_v1` folder remains a convenience/export location, not the technical source of truth.

## Do not over-engineer this operating system

If the manual Browser Worker loop is fast enough, keep it manual. Reintroduce Codex or a local coding agent only when repository size, patch volume, or repeated local application becomes the real bottleneck—most likely during the mini web app phase.
