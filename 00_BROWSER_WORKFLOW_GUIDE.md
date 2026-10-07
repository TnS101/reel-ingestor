# Reel Ingestor — Browser Architect / Browser Worker Workflow

## Why this exists

The Reel Ingestor is still small enough to control manually, but it now has enough moving parts that chat history and ad-hoc edits will eventually create drift. This workflow installs the control system before the mini web app makes the repository larger.

The useful parts of the original UNFAIR ADVANTAGE bootstrap are preserved: bounded Plan Partitions, explicit authority, Git checkpoints, evidence gates, fresh context, rollback, and separation between architecture and implementation.

Codex-specific rules, permanent FREE-ONLY restrictions, mandatory OSS research on every Plan, and Ponytail gates are intentionally removed.

## Core loop

```text
Fresh Browser Architect
  -> reconciles/approves one plan.md
  -> generate worker_context.zip
Fresh Browser Worker
  -> implements only that Plan
  -> returns PATCH_BUNDLE.zip + IMPLEMENTATION_REPORT.md + LOCAL_VERIFY.md
Human/local machine
  -> applies files to clean Git worktree
  -> runs exact local verification
  -> generate review_context.zip
Same Browser Architect
  -> ACCEPT / REJECT / BLOCK
  -> accepted work becomes Git checkpoint
  -> PROJECT_STATE + PROJECT_TRACKER + roadmap/plan synchronized
  -> Plan archived
Fresh Browser Architect for next Plan
```

## Authority

- **Human:** objective, material risk/cost approval, credentials, destructive actions, subjective approval, local execution.
- **Browser Architect:** architecture, sequencing, Plan creation/approval, acceptance criteria, review, state synchronization, next-Plan selection.
- **Browser Worker:** bounded implementation for the current approved Plan only.
- **Git + local evidence:** technical truth.
- **`PROJECT_TRACKER.xlsx`:** repo-tracked human-facing progress/control mirror.

## Hard gates

1. **NO PLAN -> NO IMPLEMENTATION.**
2. **NO CLEAN GIT BASELINE -> NO PRODUCT CODE CHANGE.**
3. **NO EVIDENCE -> NOT DONE.**
4. **NO ACCEPTED CHECKPOINT -> NO NEXT INDEPENDENT PLAN.**
5. **ONE PLAN -> ONE OBSERVABLE RESULT -> ONE VERIFICATION BOUNDARY** unless tightly coupled work genuinely shares proof.
6. Preserve known-good behavior.
7. One focused repair is default; repeated similar failure becomes investigation.

## Cost policy

Existing approved Browser ChatGPT usage is part of the workflow.

**No new recurring paid runtime/service dependency without explicit human approval. Prefer free/local mechanisms when adequate.**

## Research/reuse gate

Do not perform a ritual fixed-count OSS scan for every Plan.

Run a targeted reuse/OSS scan only when the Plan introduces a new mechanism, dependency, architecture component, or meaningful build-vs-reuse decision. Stop when more research is unlikely to change the route.

## Browser Worker limitation

Browser Worker does not operate the live Windows repository. It cannot truthfully claim production PASS from generated code alone.

Normal strongest Worker state:

`IMPLEMENTED_PENDING_LOCAL_VERIFY`

Human applies the returned files and runs the exact local verification. Architect accepts only after reviewing real local diff/evidence.

## Tracker rule

`PROJECT_TRACKER.xlsx` is intentionally stored in Git now that the Google Sheet mirror is retired.

Because XLSX is binary:

- update it only at accepted Plan boundaries or accepted material roadmap changes;
- do not commit cosmetic tracker edits continuously;
- technical truth still comes from Git + verification evidence.

## Plan lifecycle

### 1. Fresh Architect chat

From repo root:

```powershell
.\scripts\make_browser_context.ps1 -PlanId "P###_NAME"
```

Upload `.handoffs\<PLAN>_architect_context.zip` to a fresh Browser chat and paste `prompts\BROWSER_ARCHITECT_START_PROMPT.txt`.

The bundle includes the current tracker. Architect reconciles/approves exactly one Plan and does not implement product code.

### 2. Fresh Worker chat

When Plan is approved and worktree is clean:

```powershell
.\scripts\make_browser_worker_context.ps1 `
  -PlanId "P002_CORPUS_STORAGE" `
  -IncludePaths @("contracts", "docs\TEST_STRATEGY.md")
```

Add only Plan-relevant source files to `IncludePaths`.

Upload Worker context ZIP to a fresh Browser chat and paste `prompts\BROWSER_WORKER_START_PROMPT.txt`.

### 3. Apply + verify locally

Before applying Worker output, ensure local HEAD matches the Worker baseline and worktree is clean.

After applying:

- inspect `git diff`;
- run exact local verification;
- save output under `.local_verify\<PLAN_ID>.md`;
- do not commit product changes yet.

### 4. Review in same Architect chat

Generate review bundle:

```powershell
.\scripts\make_review_context.ps1 `
  -PlanId "P002_CORPUS_STORAGE" `
  -ImplementationReport ".\IMPLEMENTATION_REPORT.md" `
  -LocalVerify ".\.local_verify\P002_CORPUS_STORAGE.md"
```

Upload to the same Architect chat that owns the Plan. Architect returns `ACCEPT`, `REJECT`, or `BLOCK`.

### 5. Accept + checkpoint

Only after ACCEPT:

```powershell
git add -A
git commit -m "<accepted plan checkpoint>"
```

Then synchronize `PROJECT_STATE.md`, `PROJECT_TRACKER.xlsx`, roadmap/decisions if needed, archive the Plan, and push the accepted state.

## Project-specific rule

Frozen Knowledge Extractor contracts under `contracts/` are Git-tracked technical source-of-truth copies. Sibling browser production pack is a convenience/export location.

Runtime evidence and future corpus DB stay outside the Git root.

## Do not over-engineer this operating system

Keep Browser Worker manual while it remains fast enough. Reintroduce Codex/local coding agent only when repository size/patch volume/local application becomes the measured bottleneck.
