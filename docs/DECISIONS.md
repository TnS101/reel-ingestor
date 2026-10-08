# DECISIONS.md — Consequential Decisions

Only decisions worth revisiting belong here.

### D001 — Keep local Instagram acquisition/evidence pipeline v0.2 frozen

- DATE: 2026-10-07 (decision predates bootstrap; recorded now)
- STATUS: VALIDATED
- TYPE: ARCHITECTURE
- DECISION: Preserve the validated v0.2 ingestion/evidence behavior unless a proven production bug or explicit new requirement appears.
- WHY: Mixed-batch validation reached the accepted success/coverage gates; unnecessary tuning risks regression.
- REVISIT TRIGGER: reproducible ingestion/evidence defect or new platform requirement.

### D002 — Remove Google Sheets from the data pipeline

- STATUS: VALIDATED
- TYPE: ARCHITECTURE
- DECISION: Google Sheets is not an intermediate data store. A future local UI/app will operate over local corpus/storage.
- WHY: Sheets added no necessary mechanism and would create an avoidable intermediate layer.
- REVISIT TRIGGER: none unless a real collaboration/reporting requirement appears.

### D003 — Freeze canonical knowledge schema v1.0.0

- STATUS: VALIDATED
- TYPE: DATA CONTRACT
- DECISION: `contracts/knowledge_schema_v1.json` is Production v1 and remains frozen.
- WHY: Ten diverse human-approved GOLD artifacts exposed no structural blocker; fresh production runs also passed.
- REVISIT TRIGGER: a real production Reel contains knowledge that cannot be represented without a structural change.

### D004 — Use Browser GPT-5.6 Sol as current production Knowledge Extractor

- STATUS: VALIDATED
- TYPE: MODEL / OPERATIONS
- DECISION: Manual Browser Sol extraction is accepted for now; API/local-model automation is deferred.
- WHY: Browser Sol delivered satisfactory quality, speed, and budget profile; automation is not yet the bottleneck.
- REVISIT TRIGGER: manual transfer becomes a measurable throughput bottleneck or API automation becomes materially superior.

### D005 — Freeze Browser production prompt v1.1

- STATUS: VALIDATED
- TYPE: DATA / MODEL CONTRACT
- DECISION: `contracts/BROWSER_SOL_PRODUCTION_PROMPT_v1_1.txt` is Production v1.
- WHY: Fresh non-GOLD validation passed; v1.1 adds only listicle de-duplication and deterministic verification-status semantics.
- REVISIT TRIGGER: repeated production error/omission that is plausibly prompt-fixable.

### D006 — Adopt Browser Architect + Browser Worker while repository is small

- STATUS: VALIDATED
- TYPE: DEVELOPMENT WORKFLOW
- DECISION: Use fresh Browser Architect and Browser Worker chats with local Git/evidence verification instead of requiring a local Codex agent for each plan.
- WHY: Current repository is small; browser implementation is sufficient and lower-friction. Architecture/worker separation is retained.
- DOWNSIDE: Browser Worker cannot operate the live Windows environment.
- MITIGATION: local verification is mandatory before acceptance.
- REVISIT TRIGGER: patch application/context transfer becomes the development bottleneck, likely during mini web app growth.

### D007 — Replace FREE-ONLY with explicit approval for new recurring paid dependencies

- STATUS: VALIDATED
- TYPE: COST POLICY
- DECISION: Existing approved ChatGPT use is allowed. New recurring paid runtime/service dependencies require explicit human approval; free/local remains preferred when adequate.
- WHY: Absolute FREE-ONLY contradicts the already accepted Browser Sol workflow and can reject strategically superior options for the wrong reason.
- REVISIT TRIGGER: budget policy changes.

### D008 — Make OSS/reuse research conditional

- STATUS: VALIDATED
- TYPE: RESEARCH POLICY
- DECISION: Trigger targeted research only for new mechanisms, dependencies, architecture components, or meaningful build-vs-reuse choices.
- WHY: A mandatory 5–10 project scan on every bounded plan creates process cost without changing decisions.
- REVISIT TRIGGER: repeated custom-build waste or missed existing mechanisms.

### D009 — Keep live Google Sheet as human tracker; do not duplicate it in Git

- STATUS: SUPERSEDED BY D011
- TYPE: STATE MANAGEMENT
- DECISION: Git stores technical state/plan/decisions; the user's live Google Sheet remains the human progress mirror.
- WHY: This was the previous tracker policy before the repository-tracked workbook was adopted.
- REVISIT TRIGGER: none; see D011.

### D010 — Git root is the actual code folder, not the evidence workspace

- STATUS: VALIDATED
- TYPE: REPOSITORY BOUNDARY
- DECISION: Git root is `Extract Reel Data`; generated `runs`, `results.jsonl`, Gold results and browser-pack exports remain in the parent workspace.
- WHY: Keeps source/control history small and avoids tracking bulky generated evidence.
- REVISIT TRIGGER: future app architecture requires a monorepo or versioned fixtures/data subset.

### D011 — Use repo-tracked PROJECT_TRACKER.xlsx as the human progress/control mirror

- DATE: 2026-10-07
- STATUS: VALIDATED
- TYPE: STATE MANAGEMENT
- DECISION: `PROJECT_TRACKER.xlsx` is the versioned human-facing tracker. Git/direct evidence remain technical truth; the workbook is updated at accepted Plan/material roadmap boundaries rather than continuously.
- WHY: The project now has a small Git repository and can tie tracker state to accepted checkpoints without maintaining a separate Google Sheet authority.
- REVISIT TRIGGER: tracker synchronization becomes automated elsewhere or binary workbook churn becomes materially costly.

### D012 — Use standard-library SQLite for the first local corpus layer

- DATE: 2026-10-08
- STATUS: APPROVED FOR P002
- TYPE: ARCHITECTURE / STORAGE
- DECISION: P002 uses Python standard-library `sqlite3` plus filesystem provenance/artifact paths. Runtime corpus data stays outside Git. Artifact identity is exact imported-file SHA-256; different hashes for the same Reel ID coexist immutably.
- WHY: It satisfies the current durability/query/versioning boundary without a server, ORM, third-party package, recurring cost, or premature semantic-search infrastructure.
- REJECTED FOR P002: loose-file-only scanning as the durable index; external DB/server; ORM; FTS/vector/embedding service; general-purpose JSON Schema dependency.
- REVISIT TRIGGER: measured corpus size, search quality/latency, concurrency, or app requirements make the simple local SQLite boundary insufficient.
