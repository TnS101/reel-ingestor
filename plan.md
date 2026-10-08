# plan.md — P002_CORPUS_STORAGE

- PLAN ID: `P002_CORPUS_STORAGE`
- ARCHITECT SESSION: `ARCH-P002_CORPUS_STORAGE`
- WORKER SESSION: `BWORK-P002_CORPUS_STORAGE`
- STATUS: `APPROVED — READY_FOR_BROWSER_WORKER`
- PLAN TYPE: PRODUCT / KNOWLEDGE LAYER
- ROADMAP STEP: `5.4 — Build manipulation + local corpus layer`
- BASELINE BRANCH: `main`
- BASELINE COMMIT: supplied by the Architect in the Worker handoff; it must be the commit that contains this approved Plan and synchronized control state.
- BASELINE RULE: Browser Worker must read and implement from that exact handoff SHA, not a later moving `main` HEAD. `GIT_BASELINE.txt` is optional handoff evidence and is not required when GitHub provides the canonical files directly.

## 1. Objective

Build and prove the **smallest viable local corpus/storage + query layer** for real Production v1 canonical knowledge JSONs.

Observable result:

> Several real `knowledge_*.json` artifacts can be imported locally, retained immutably with source/hash provenance, listed/retrieved, versioned safely, and searched across Reels without modifying the canonical source files.

This Plan intentionally stops **before manipulation generation**.

## 2. Why this is the current bottleneck

Step 5.3 is complete and frozen:

- `knowledge_schema_v1.0.0` is Production v1;
- `browser_production_v1.1` is Production v1;
- fresh-Reel validation passed;
- representative raw-evidence spot audits passed.

The next constraint is no longer extraction quality. It is the lack of a durable local corpus/index that can accept real canonical outputs and support later manipulation/query work.

Building manipulation logic before this boundary exists would couple derived outputs to ad-hoc files and create avoidable migration work.

## 3. Accepted storage route

Use **Python standard-library `sqlite3` + filesystem evidence/artifact paths** for the first corpus layer.

Why:

- zero new runtime/service cost;
- no new third-party dependency;
- mature native mechanism;
- easy local backup/inspection;
- sufficient for the current corpus size;
- compatible with a later local web app;
- avoids storing images/media as database BLOBs.

Do **not** add an external database, ORM, vector database, embedding service, or FTS dependency in this Plan.

The first query implementation may use ordinary indexed columns + deterministic flattened searchable text / SQL `LIKE`. Add FTS/vector search only when measured corpus usage proves ordinary search is the bottleneck.

## 4. Storage boundary

Runtime corpus data must remain outside the Git code/control root.

Default runtime location:

`<config.paths.workspace>\corpus\`

Expected database:

`<config.paths.workspace>\corpus\reel_corpus.sqlite3`

Git tracks corpus **code/contracts/tests**, not the live database or imported knowledge artifacts.

No corpus SQLite database may be created under the Git repository during normal runtime or tests.

Tests must use temporary directories/databases.

Do **not** modify `.gitignore` merely to hide SQLite/database artifacts. A repo-local runtime database is a boundary failure, not something to ignore.

## 5. Canonical artifact and version rules

Production v1 knowledge JSON remains canonical input.

Artifact identity is the **SHA-256 of the exact imported canonical JSON bytes**.

The corpus layer must:

- never rewrite the input `knowledge_*.json`;
- compute and retain SHA-256 for every imported artifact;
- retain the source file path when available;
- retain the full canonical JSON snapshot or an equivalently lossless representation;
- preserve `schema_version`, Reel ID/URL, creator when present, model, prompt version, and generation/input metadata when present;
- keep imported artifact versions immutable;
- treat exact re-import of the same artifact hash as idempotent;
- allow the same Reel ID with a different artifact hash to coexist as a separate immutable artifact version;
- never silently replace one artifact version with another.

Do not use destructive SQLite `REPLACE` semantics for artifact idempotence/version handling.

## 6. Import admission boundary

This Plan does **not** add a general-purpose JSON Schema validation subsystem.

Before inserting an artifact, the importer must minimally verify:

- valid JSON object;
- `schema_version == "1.0.0"`;
- `source.reel_id` exists and is non-empty;
- `source.url` exists and is non-empty;
- `generation.model`, `generation.prompt_version`, `generation.generated_at`, and `generation.input_mode` exist and are non-empty where applicable to their schema types.

Malformed JSON, unsupported schema version, or missing required identity/provenance must fail before artifact insertion.

Do not add a `jsonschema` package or other validation dependency in this Plan. Full Production v1 schema validation remains an upstream Knowledge Extractor contract.

## 7. Minimum query/use surface

Provide a small local CLI/module surface sufficient to prove the corpus contract.

Required capabilities:

1. initialize/create corpus DB;
2. import one canonical JSON;
3. import several canonical JSONs / a directory of matching JSONs;
4. list imported artifacts;
5. retrieve by artifact SHA-256;
6. retrieve all stored versions for a Reel ID;
7. keyword-search useful canonical knowledge across multiple Reels;
8. emit valid machine-readable JSON for list/get/search commands.

Retrieval semantics are fixed:

- lookup by artifact SHA-256 returns exactly that version or `NOT_FOUND`;
- lookup by Reel ID returns **all** stored versions for that Reel in deterministic order;
- the implementation must never silently choose an arbitrary/latest version when multiple hashes exist;
- every search result exposes at minimum Reel ID + artifact hash so the exact canonical version is addressable.

Human-readable output is optional.

## 8. Search document

For the first version, create a deterministic searchable representation from useful canonical text such as:

- core value / summary / key takeaways;
- knowledge units;
- claims;
- actionable steps;
- mechanisms;
- hidden value;
- taxonomy;
- entities/tools where available.

Search is a **retrieval convenience**, not a second canonical truth. Returned results must link back to the exact artifact/reel/hash.

Do not build ranking, embeddings, semantic search, or a query language in P002.

## 9. In scope

- one focused corpus/storage module;
- local SQLite schema initialization at version 1;
- import/index logic for Production v1 canonical JSON;
- deterministic hash/provenance/version handling;
- basic list/get/search query surface;
- focused automated tests;
- safe runtime-path handling.

## 10. Out of scope

- `HOW_TO`, `STEP_BY_STEP`, `REVERSE_ENGINEER`, `READ_BETWEEN_LINES`, `RECREATE_REEL`, `ADAPT_FORMAT` generation;
- manipulation prompt/history tables;
- embeddings/vector search;
- FTS;
- external DB/server;
- ORM;
- web app/UI;
- queue/scheduling/dashboard;
- Browser/API automation;
- ingestion changes;
- schema v1.0.0 changes;
- Browser production prompt v1.1 changes;
- moving `runs/`, GOLD files, source media, keyframes, or contact sheets into SQLite;
- refactoring unrelated ingestion code;
- general-purpose JSON Schema validation infrastructure;
- `.gitignore` changes.

## 11. Preserve

Do not change behavior or source in:

- `reel_ingestor.py`;
- `transcribe.py`;
- `visual_evidence.py`;
- `run_one.ps1`;
- `run_batch.ps1`;
- `config.json`;
- acquisition/circuit-breaker semantics;
- frozen Knowledge Extractor contracts.

If corpus implementation appears to require changing ingestion, config semantics, repository boundaries, or frozen contracts, STOP and return to the Architect.

## 12. Worker decision and file boundary

Browser Worker may choose:

- internal Python functions/classes;
- small internal SQLite table/index details consistent with this Plan;
- CLI subcommand/argument syntax;
- deterministic flattening details for searchable text;
- test implementation details.

Browser Worker may **not** choose:

- a different database/runtime architecture;
- a new paid/external service;
- new third-party dependencies;
- manipulation architecture;
- schema/prompt changes;
- UI/API scope;
- ingestion/config refactors;
- broader repository cleanup.

The only repo files the Worker is allowed to add/change are:

- `corpus_store.py`
- `tests/test_corpus_store.py`

No other repo file may change during P002 implementation.

If the accepted SQLite/filesystem route or this two-file implementation boundary is materially blocked, report `BLOCKED`; do not silently redesign or broaden scope.

Worker handoff artifacts remain outside product/repo scope:

- `PATCH_BUNDLE.zip`
- `IMPLEMENTATION_REPORT.md`
- `LOCAL_VERIFY.md`

## 13. Real production evidence requirement

Local acceptance must use **at least 3 real Production v1 canonical knowledge JSONs**, preferably different content archetypes.

Do not use GOLD outputs as normal production corpus inputs for this acceptance test unless the Architect explicitly needs a regression fixture. The point is to prove the corpus against the actual current production workflow.

The real source artifacts must remain untouched. Synthetic/temp copies may be used only for negative/versioning tests.

## 14. Acceptance criteria

PASS only if all are true:

1. Corpus DB initializes at the intended local runtime location without adding a paid/external dependency.
2. At least 3 real Production v1 canonical JSON artifacts import successfully.
3. Exact re-import of the same artifact is idempotent and does not create accidental duplicates.
4. Input canonical JSON files are byte-for-byte unchanged after import.
5. Each stored artifact can be traced to exact Reel ID + SHA-256 + schema version + source path when available.
6. Full canonical content is not materially lost by import/storage.
7. List and retrieval work deterministically, including retrieval of all versions for a Reel ID.
8. Keyword search returns relevant results across more than one Reel and every result exposes exact Reel ID + artifact hash.
9. Malformed JSON / unsupported schema / missing required identity or generation provenance fails clearly before insertion and does not corrupt the corpus.
10. Existing ingestion/config/frozen-contract files and behavior are unchanged.
11. No live SQLite DB, imported canonical artifact corpus, run evidence, cookies, media, or handoff bundles exist as tracked/staged repo content.
12. Automated tests + real local verification pass.
13. Same Reel ID with a different artifact SHA-256 is retained as a separate immutable version; neither version is overwritten.
14. Only the two Plan-authorized repo files changed during Worker implementation.

## 15. Local verification

Worker must produce exact runnable commands in `LOCAL_VERIFY.md` using the actual CLI syntax it implements.

### Phase A — baseline gate before applying Worker files

Run on the human's clean local repository:

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
.\scripts\verify_bootstrap.ps1
```

Required:

- branch = `main`;
- HEAD = the exact baseline SHA supplied in the Architect Worker handoff;
- worktree clean;
- bootstrap result = `READY_FOR_WORK`.

If any baseline condition fails, STOP before applying Worker files.

### Phase B — after applying Worker files, before acceptance

Minimum verification boundary:

```powershell
git rev-parse HEAD

# Intent-to-add only: makes new Worker files visible to git diff for Architect review.
# This does not stage their contents for commit.
git add -N -- corpus_store.py tests/test_corpus_store.py

python -c "import sqlite3; print(sqlite3.sqlite_version)"
python -m py_compile .\corpus_store.py
python -m unittest discover -s tests -p "test_corpus_store.py"
python .\corpus_store.py --help

# Worker must provide exact commands for:
# - initialize target corpus outside the repo;
# - capture SHA-256 of >=3 real Production v1 source JSONs BEFORE import;
# - import those >=3 real artifacts;
# - exact re-import/idempotence proof;
# - list JSON output;
# - get by artifact hash JSON output;
# - get all versions by Reel ID JSON output;
# - cross-Reel keyword search JSON output;
# - same-Reel/different-hash version proof using a TEMPORARY COPY only;
# - malformed/unsupported/missing-identity failure proof;
# - capture SHA-256 of the same real source JSONs AFTER import and compare.
```

Protected-file regression check:

```powershell
git diff --exit-code -- `
  reel_ingestor.py `
  transcribe.py `
  visual_evidence.py `
  run_one.ps1 `
  run_batch.ps1 `
  config.json `
  contracts/knowledge_schema_v1.json `
  contracts/BROWSER_SOL_PRODUCTION_PROMPT_v1_1.txt `
  contracts/FROZEN_CONTRACTS.json
```

Repository-boundary check:

```powershell
git diff --name-only
git ls-files "*.sqlite" "*.sqlite3" "*.db"
Get-ChildItem -Path . -Recurse -File | Where-Object { $_.Extension -in ".sqlite", ".sqlite3", ".db" }
git diff --stat
git diff
git status --short
```

Expected:

- `git diff --name-only` contains exactly the two authorized Worker files;
- `git ls-files` returns no database files;
- recursive database-file scan returns no database files inside the repo.

Expected changed repo files are exactly:

```text
corpus_store.py
tests/test_corpus_store.py
```

The Worker must state the Python interpreter explicitly if plain `python` is not the correct local interpreter.

## 16. Affected regression

No Instagram/GPU regression run is required because P002 must not touch acquisition, transcription, OCR, visual selection, status logic, circuit breakers, cleanup, or config semantics.

Regression proof is:

- clean exact baseline was verified before application;
- protected files show zero diff afterward;
- frozen contract files show zero diff;
- corpus tests and real artifact import/query pass;
- runtime corpus data remains outside Git.

If Worker touches any protected file unexpectedly, STOP; the verification boundary is invalid.

## 17. Evidence required for Architect review

Return:

- `IMPLEMENTATION_REPORT.md`;
- `LOCAL_VERIFY.md`;
- actual local verification output;
- `git diff --stat`;
- full `git diff`;
- `git status --short`;
- corpus test output;
- import/list/get/search JSON outputs;
- same-Reel/different-hash versioning proof;
- evidence that the real source JSON hashes did not change;
- database path and concise schema/table/index summary;
- `git ls-files "*.sqlite" "*.sqlite3" "*.db"` output;
- confirmation that only `corpus_store.py` and `tests/test_corpus_store.py` changed.

The 3 real source JSONs themselves need not be uploaded unless evidence exposes a structural/schema anomaly that cannot be reviewed otherwise.

## 18. Repair limit

One focused repair is allowed.

If a second similar failure appears, or the design requires a dependency, architecture change, protected-file edit, or wider patch surface, stop and create a smaller investigation/decision Plan rather than patch stacking.

## 19. Human gate

- HUMAN INTERVENTION REQUIRED: YES, for local application and verification.
- Human supplies paths to 3+ real Production v1 canonical JSONs if the Browser Worker cannot see them.
- Human runs local verification because Browser ChatGPT cannot operate the live Windows/runtime filesystem.
- No destructive action or paid dependency is authorized by this Plan.

## 20. Rollback

Before acceptance, remove only the two Worker files/changes after reviewing them:

```powershell
git reset -- corpus_store.py tests/test_corpus_store.py
git clean -f -- corpus_store.py tests/test_corpus_store.py
```

Do not use broad `git clean -fd` as the default rollback for this Plan.

After acceptance, the accepted Git checkpoint is the rollback boundary. Runtime corpus DB can be deleted/rebuilt from canonical knowledge inputs during this early phase.

## 21. Stop conditions

STOP and return to Architect if:

- baseline is not exactly `main` at the handoff SHA before Worker application;
- required schema/prompt changes appear necessary;
- ingestion/config/protected files must change;
- a third-party DB/ORM/vector/validation dependency appears necessary;
- corpus data would need to live inside Git;
- the Worker cannot guarantee canonical inputs remain immutable;
- the Worker cannot safely retain multiple immutable hashes for the same Reel ID;
- a real Production v1 artifact reveals a structural blocker not represented by schema v1.0.0;
- local verification contradicts Browser Worker assumptions;
- more than the two authorized repo files appear necessary.

## 22. Plan close

On Architect `ACCEPT`:

1. create the accepted Git checkpoint for P002 implementation;
2. record the accepted commit in `PROJECT_STATE.md`;
3. update `PROJECT_TRACKER.xlsx` Step 5.4 / Plan Control;
4. archive this plan under `docs/plans/archive/P002_CORPUS_STORAGE.md`;
5. push the accepted checkpoint/control-state synchronization;
6. close Architect + Worker sessions;
7. only then create the next independent Plan, expected to address manipulation records/outputs.
