# plan.md — P001_GIT_BASELINE

- PLAN ID: `P001_GIT_BASELINE`
- ARCHITECT SESSION: `ARCH-P001_GIT_BASELINE`
- WORKER SESSION: `HUMAN-LOCAL`
- STATUS: `READY_FOR_HUMAN_EXECUTION`
- PLAN TYPE: INFRASTRUCTURE / CONTROL PLANE

## 1. Objective

Create a safe Git repository and baseline commit for the existing working Reel Ingestor code plus the Browser-workflow control overlay, without changing product behavior.

## 2. Why now

Step 5.3 is complete and Step 5.4 will introduce new local corpus/manipulation code. Git must become the diff ledger, rollback boundary, and acceptance checkpoint **before** those edits begin.

## 3. Baseline

- Current product code is working locally but the project root has no accepted Git baseline yet.
- Product root: `C:\Users\User\Downloads\Projects\Instagram Automations\Reel Ingestor\Extract Reel Data`
- Ingestion v0.2 behavior is known-good and must not change in this Plan.

## 4. Dependencies / prerequisites

- Git installed and available from PowerShell.
- Bootstrap ZIP extracted into the project root.
- No intentional product-code edits made between extraction and baseline creation.

## 5. In scope

- initialize `.git` if absent;
- establish `main` as the baseline branch;
- install/use the project `.gitignore`;
- verify secrets/generated/runtime data are not staged;
- stage the existing product code + project-control files;
- create one baseline commit after human inspection;
- verify clean worktree and commit SHA;
- run `scripts/verify_bootstrap.ps1`.

## 6. Out of scope

- any change to `reel_ingestor.py`, `transcribe.py`, `visual_evidence.py`, `run_one.ps1`, `run_batch.ps1`, or `config.json` behavior;
- dependency upgrades;
- Step 5.4 corpus/manipulation implementation;
- moving `runs`, `Gold Results`, `results.jsonl`, or browser package data into the repo;
- generalizing machine-specific runtime config;
- UI/app/API work.

## 7. Preserve

- current local ingestion behavior;
- current paths/configuration;
- current runtime output locations;
- frozen schema v1.0.0 and Browser Sol prompt v1.1 contents.

## 8. Human execution

First preview what would be committed:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\init_git_baseline.ps1
```

The preview initializes Git if needed, stages candidate files temporarily, checks forbidden/suspicious paths, prints the candidate baseline, then unstages the preview.

If the preview is correct, create the baseline commit:

```powershell
.\scripts\init_git_baseline.ps1 -Commit
```

Then run:

```powershell
.\scripts\verify_bootstrap.ps1

git branch --show-current
git log -1 --oneline
git status --short
git ls-files
```

Return the command output to the Architect chat for acceptance.

## 9. Acceptance criteria

PASS only if all are true:

1. Git repository exists at the exact product root.
2. Baseline branch is `main`.
3. One baseline commit exists and its SHA is known.
4. `git status --short` is empty after the commit.
5. Product source/control files are tracked.
6. No cookie file, `.env`, credentials, source media, `runs/`, `results.jsonl`, handoff ZIP, local verification evidence, cache, venv, or generated runtime evidence is tracked.
7. Frozen contract hashes pass `verify_bootstrap.ps1`.
8. No product behavior/source code was intentionally modified by this Plan.

## 10. Verification boundary

This Plan proves repository/control hygiene only. It does **not** require an Instagram regression run because product code must remain unchanged.

## 11. Evidence required

Return:

- full output of `scripts/init_git_baseline.ps1 -Commit`;
- full output of `scripts/verify_bootstrap.ps1`;
- `git log -1 --oneline`;
- `git status --short`;
- `git ls-files`.

## 12. Human gate

- HUMAN INTERVENTION REQUIRED: YES
- ACTION: inspect staged-file preview, then authorize/create the local baseline commit.
- WHY: Browser ChatGPT cannot operate the user's live local Git repository.
- RETURN: command outputs listed above.

## 13. Repair limit

One focused correction to `.gitignore` / baseline staging is allowed. If unexplained files or pre-existing Git history appear, stop and investigate rather than forcing the baseline.

## 14. Rollback

No product code is changed. Before acceptance, Git initialization can be rolled back by deleting the newly created `.git` directory. After acceptance, normal Git history becomes the rollback mechanism.

## 15. Stop conditions

Stop and return evidence if:

- a `.git` repository already exists unexpectedly;
- staged files include secrets/auth files or generated runtime evidence;
- existing product files show unexplained changes;
- Git cannot establish a clean baseline;
- frozen contract hash verification fails.

## 16. Plan close

On Architect `ACCEPT`:

1. record baseline commit SHA in `PROJECT_STATE.md`;
2. mark P001 accepted;
3. archive this plan under `docs/plans/archive/P001_GIT_BASELINE.md`;
4. update the live Google Sheet to reflect the Git/control-plane checkpoint if desired;
5. close this Architect partition;
6. start a fresh Architect chat for the first Step 5.4 plan.
