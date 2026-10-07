# LOCAL_VERIFY.md — Plan Local Verification

- PLAN ID: [P###]
- BASELINE COMMIT: [SHA]
- EXPECTED WORKTREE BEFORE APPLY: CLEAN

## Before applying Worker bundle

```powershell
git status --short
git rev-parse HEAD
```

Expected: clean status and exact baseline commit from the plan.

## Apply

[Exact safe instructions for placing the returned repo-relative files.]

Do not commit before Architect acceptance.

## Verification commands

```powershell
[COMMANDS]
```

## Expected observable results

- [RESULT]

## Affected regression

```powershell
[COMMAND / NOT REQUIRED + WHY]
```

## Evidence to save

- command output;
- `git status --short`;
- `git diff --stat`;
- `git diff` or review bundle;
- any required output file/screenshot/log.

## Failure meaning

- [WHEN TO STOP / WHAT COUNTS AS FAIL]
