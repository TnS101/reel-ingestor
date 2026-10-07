# TRACKER_POLICY.md — Live Google Sheet + Git State

The user's live Google Sheet is the human-facing project tracker.

It is intentionally **not copied into this Git repository** as a second spreadsheet because two manually maintained tracker files would drift.

## State authority

When facts conflict, use:

1. actual local repository + Git diff/status/commit;
2. direct verification evidence;
3. `ARCHITECTURE.md` for approved stable boundaries;
4. `PROJECT_STATE.md` for current accepted technical reality;
5. current/last `plan.md` for the partition boundary;
6. live Google Sheet as the human-readable mirror;
7. chat history last.

## Plan close

After an accepted plan:

- Git checkpoint first;
- update `PROJECT_STATE.md`;
- update/archive `plan.md`;
- human updates the live Google Sheet when the product progress row/state changed.

If a future app/API can synchronize the tracker automatically, this policy can be revisited.
