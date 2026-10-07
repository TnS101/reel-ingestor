# TRACKER_POLICY.md — Repo-Tracked Project Tracker + Git State

`PROJECT_TRACKER.xlsx` is the human-facing project tracker for Reel Ingestor.

The Google Sheet mirror has been retired. The workbook now lives in the Git repository so the tracker version can be tied to accepted project checkpoints.

## Update policy

Do **not** edit/commit the workbook continuously during implementation.

Update it at accepted Plan boundaries or when a material roadmap/decision change is formally accepted. This limits binary-file Git churn and keeps the tracker aligned with technical truth.

## State authority

When facts conflict, use:

1. actual local repository + Git diff/status/commit;
2. direct verification evidence;
3. `ARCHITECTURE.md` for approved stable boundaries;
4. `PROJECT_STATE.md` for current accepted technical reality;
5. current/last `plan.md` for the Plan boundary;
6. `PROJECT_TRACKER.xlsx` as the human-readable progress/control mirror;
7. chat history last.

## Plan close

After an accepted Plan:

1. create/identify the accepted Git checkpoint;
2. update `PROJECT_STATE.md`;
3. update `PROJECT_TRACKER.xlsx`;
4. archive/replace `plan.md`;
5. commit the synchronized control-state update if it is not already part of the accepted checkpoint;
6. push the accepted state.

The tracker must never claim a Plan is complete before the technical acceptance evidence exists.
