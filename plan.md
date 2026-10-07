# plan.md — P002_CORPUS_STORAGE

- PLAN ID: `P002_CORPUS_STORAGE`
- ARCHITECT SESSION: `ARCH-P002_CORPUS_STORAGE`
- WORKER SESSION: `BWORK-P002_CORPUS_STORAGE`
- STATUS: `PLANNED — FRESH ARCHITECT MUST RECONCILE/APPROVE BEFORE WORKER`
- PLAN TYPE: PRODUCT / KNOWLEDGE LAYER
- ROADMAP STEP: `5.4 — Build manipulation + local corpus layer`
- BASELINE BRANCH: `main`
- BASELINE RULE: Worker must start from the clean `main` HEAD created after the P001-close/control-sync commit. The exact SHA is captured in `GIT_BASELINE.txt` by `make_browser_worker_context.ps1`.

## 1. Objective

Build and prove the **smallest viable local corpus/storage + query layer** for real Production v1 canonical knowledge JSONs.

Observable result:

> Several real `knowledge_*.json` artifacts can be imported locally, retained immutably with source/hash provenance, listed/retrieved, and searched across Reels without modifying the canonical source files.

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

The first query implementation may use ordinary indexed columns + deterministic flattened searchable text / SQL `LIKE`. Add FTS/vector search only when real corpus usage proves it is the bottleneck.

## 4. Storage boundary

Runtime corpus data must remain outside the Git code/control root.

Default runtime location:

`<config.paths.workspace>\corpus\`

Expected database:

`<config.paths.workspace>\corpus\reel_corpus.sqlite3`

Git tracks the corpus **code/contracts/tests**, not the live database or imported knowledge artifacts.

Add defensive ignores for local SQLite/runtime corpus files if needed.

## 5. Canonical artifact rules

Production v1 knowledge JSON remains canonical input.

The corpus layer must:

- never rewrite the input `knowledge_*.json`;
- compute and retain SHA-256 for every imported artifact;
- retain the source file path when available;
- retain the full canonical JSON snapshot or an equivalently lossless representation;
- preserve `schema_version`, Reel ID/URL, creator when present, model, prompt version, and generation/input metadata when present;
- keep imported versions immutable;
- make duplicate import of the exact same artifact/hash idempotent;
- avoid silently replacing a different artifact for the same Reel ID.

A different hash for the same Reel may coexist as a separate immutable artifact version or be rejected clearly if the implementation cannot support version history safely. Silent overwrite is forbidden.

## 6. Minimum query/use surface

Provide a small local CLI/module surface sufficient to prove the corpus contract.

Required capabilities:

1. initialize/create corpus DB;
2. import one canonical JSON;
3. import several canonical JSONs / a directory of matching JSONs;
4. list imported artifacts;
5. retrieve an artifact deterministically by Reel ID and/or artifact hash;
6. keyword-search useful canonical knowledge across multiple Reels;
7. emit machine-readable JSON output for query commands where practical.

The exact command names are Worker-owned implementation details as long as the acceptance criteria are met.

## 7. Search document

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

## 8. In scope

- new corpus/storage module(s);
- local SQLite schema initialization/migration-at-version-1;
- import/index logic for Production v1 canonical JSON;
- deterministic hash/provenance handling;
- basic list/get/search query surface;
- tests for corpus behavior;
- docs needed to run/verify the new corpus layer;
- safe runtime-path handling;
- `.gitignore` additions only if needed for corpus runtime files.

## 9. Out of scope

- `HOW_TO`, `STEP_BY_STEP`, `REVERSE_ENGINEER`, `READ_BETWEEN_LINES`, `RECREATE_REEL`, `ADAPT_FORMAT` generation;
- manipulation prompt/history tables beyond what is strictly necessary to avoid blocking the future boundary;
- embeddings/vector search;
- external DB/server;
- ORM;
- web app/UI;
- queue/scheduling/dashboard;
- Browser/API automation;
- ingestion changes;
- schema v1.0.0 changes;
- Browser production prompt v1.1 changes;
- moving `runs/`, GOLD files, source media, keyframes, or contact sheets into SQLite;
- refactoring unrelated ingestion code.

## 10. Preserve

Do not change behavior in:

- `reel_ingestor.py`;
- `transcribe.py`;
- `visual_evidence.py`;
- `run_one.ps1`;
- `run_batch.ps1`;
- acquisition/circuit-breaker semantics;
- frozen Knowledge Extractor contracts.

If corpus implementation appears to require changing ingestion or frozen contracts, STOP and return to the Architect.

## 11. Worker decision boundary

Browser Worker may choose:

- module/file names;
- small internal SQLite table/index details;
- CLI syntax;
- test organization;
- how searchable text is flattened.

Browser Worker may **not** choose:

- a different database/runtime architecture;
- a new paid/external service;
- new third-party dependencies;
- manipulation architecture;
- schema/prompt changes;
- UI/API scope;
- ingestion refactors.

If the accepted SQLite/filesystem route is materially blocked, report `BLOCKED`; do not silently redesign.

## 12. Real production evidence requirement

Local acceptance must use **at least 3 real Production v1 canonical knowledge JSONs**, preferably different content archetypes.

Do not use GOLD outputs as normal production corpus inputs for this acceptance test unless the Architect explicitly needs a regression fixture. The point is to prove the corpus against the actual current production workflow.

## 13. Acceptance criteria

PASS only if all are true:

1. Corpus DB initializes at the intended local runtime location without adding a paid/external dependency.
2. At least 3 real Production v1 canonical JSON artifacts import successfully.
3. Exact re-import of the same artifact is idempotent and does not create accidental duplicates.
4. Input canonical JSON files are byte-for-byte unchanged after import.
5. Each stored artifact can be traced to exact Reel ID + SHA-256 + schema version + source path when available.
6. Full canonical content is not materially lost by import/storage.
7. List/retrieve works deterministically.
8. Keyword search returns relevant results across more than one Reel and every result points back to the exact artifact.
9. Malformed JSON / unsupported schema / missing required identity fails clearly without corrupting the corpus.
10. Existing ingestion files/behavior are unchanged.
11. No live SQLite DB, imported canonical artifact corpus, run evidence, cookies, media, or handoff bundles are staged for Git.
12. Automated tests + real local verification pass.

## 14. Local verification

Worker must produce exact commands in `LOCAL_VERIFY.md`.

Minimum verification boundary should include:

```powershell
git status --short
git rev-parse HEAD

# automated corpus tests
python -m unittest discover -s tests -p "test_corpus*.py"

# initialize corpus
# [exact command chosen by Worker]

# import >=3 real Production v1 knowledge JSON files
# [exact command(s)]

# list/retrieve
# [exact command(s)]

# keyword search producing cross-Reel results
# [exact command(s)]

# verify source artifact hashes before/after import
# [exact command(s)]

git diff --stat
git diff
git status --short
```

If the project's active Python interpreter must be specified explicitly, Worker must state it rather than assuming.

## 15. Affected regression

No Instagram/GPU regression run is required **if ingestion code remains untouched**.

Regression proof is:

- relevant existing source files show no diff;
- bootstrap/frozen contract verification still passes;
- corpus tests and real artifact import/query pass.

If Worker touches ingestion code unexpectedly, STOP; the verification boundary is invalid.

## 16. Evidence required for Architect review

Return:

- `IMPLEMENTATION_REPORT.md`;
- `LOCAL_VERIFY.md`;
- actual local verification output;
- `git diff --stat`;
- `git diff`;
- `git status --short`;
- corpus test output;
- import/list/get/search outputs;
- evidence that source JSON hashes did not change;
- database path and a concise schema/table summary;
- confirmation that runtime DB/artifacts are not tracked by Git.

## 17. Repair limit

One focused repair is allowed.

If a second similar failure appears, or the design requires a new dependency/architecture change, stop and create a smaller investigation/decision Plan rather than patch stacking.

## 18. Human gate

- HUMAN INTERVENTION REQUIRED: YES, for local application and verification.
- Human supplies paths to 3+ real Production v1 canonical JSONs if the Browser Worker cannot see them.
- Human runs the local verification because Browser ChatGPT cannot operate the live Windows/runtime filesystem.
- No destructive action or paid dependency is authorized by this Plan.

## 19. Rollback

Before acceptance:

```powershell
git restore .
git clean -fd
```

Only use `git clean -fd` after reviewing what is untracked and ensuring no local evidence/runtime artifacts that must be preserved sit inside the repo.

After acceptance, the accepted Git checkpoint is the rollback boundary. Runtime corpus DB can be deleted/rebuilt from canonical knowledge inputs during this early phase.

## 20. Stop conditions

STOP and return to Architect if:

- required schema/prompt changes appear necessary;
- ingestion code must change;
- a third-party DB/ORM/vector dependency appears necessary;
- corpus data would need to live inside Git;
- the Worker cannot guarantee canonical inputs remain immutable;
- repository baseline is not clean/identifiable;
- a real Production v1 artifact reveals a structural blocker not represented by schema v1.0.0;
- local verification contradicts Browser Worker assumptions.

## 21. Plan close

On Architect `ACCEPT`:

1. create the accepted Git checkpoint;
2. record accepted commit in `PROJECT_STATE.md`;
3. update `PROJECT_TRACKER.xlsx` Step 5.4 / Plan Control;
4. archive this plan under `docs/plans/archive/P002_CORPUS_STORAGE.md`;
5. push the accepted checkpoint;
6. close Architect + Worker sessions;
7. only then create the next independent Plan, expected to address manipulation records/outputs.
