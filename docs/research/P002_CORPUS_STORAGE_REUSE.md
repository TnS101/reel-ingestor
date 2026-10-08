# P002_CORPUS_STORAGE — Reuse / Storage Mechanism Check

- DATE: 2026-10-08
- PLAN: `P002_CORPUS_STORAGE`
- STATUS: RESOLVED
- DECISION: use Python standard-library `sqlite3` + filesystem provenance paths for the first corpus layer.

## Decision being resolved

What is the smallest durable local mechanism that can:

- import real Production v1 canonical knowledge JSONs;
- preserve exact artifact identity/provenance;
- retain multiple immutable versions safely;
- support deterministic list/get/keyword search;
- remain local, cheap, inspectable, and compatible with a later mini web app?

## Necessity check

A durable corpus/index cannot be removed without blocking Step 5.4. Manipulation records need a stable source-artifact identity rather than ad-hoc loose-file assumptions.

The mechanism should still be minimized: P002 needs storage + basic retrieval, not a search platform.

## Candidates checked

### 1. Loose JSON files + directory scanning

**Reject as the durable corpus index.**

Useful as canonical source artifacts, but repeated directory scanning alone gives weak indexing/version/query semantics and pushes ad-hoc file assumptions into future manipulation/app work.

Canonical JSON files remain valid inputs; they are not the query/index mechanism.

### 2. Python standard-library `sqlite3`

**Choose.**

Fits the current boundary:

- local/serverless;
- no new package/service;
- transactions and uniqueness constraints;
- deterministic structured queries;
- easy backup/inspection;
- adequate for current corpus scale;
- later local-app compatible.

Keep media/evidence files outside the DB and retain paths/provenance.

### 3. External database/server or ORM

**Reject for P002.**

Adds deployment/runtime/dependency complexity without a demonstrated concurrency, scale, or portability need.

### 4. FTS/vector database/embeddings

**Reject for P002.**

Current Win Condition only needs useful keyword retrieval across a small corpus. Ordinary deterministic searchable text + SQL `LIKE` is sufficient to prove value.

Add stronger search only after measured corpus usage shows search quality or latency is the bottleneck.

### 5. General-purpose JSON Schema validation dependency

**Reject for P002.**

The canonical schema is already an upstream frozen Production v1 contract. P002 only needs minimal import admission checks required to protect storage identity/provenance. Duplicating full schema validation downstream adds dependency and scope without changing the current Win Condition.

## Implementation constraints

- runtime DB outside Git;
- source canonical JSON never mutated;
- SHA-256 over exact imported bytes is artifact identity;
- exact same hash import is idempotent;
- same Reel ID + different hash coexists as a separate immutable version;
- retrieval/search always exposes the exact artifact hash;
- no destructive overwrite semantics for version handling;
- no new third-party or recurring paid dependency.

## Revisit trigger

Re-open the storage/search mechanism only if real evidence shows one of these:

- corpus scale causes material query latency;
- keyword retrieval quality is insufficient for actual use;
- concurrent writers/readers become a real requirement;
- the future app requires a server/deployment shape SQLite cannot satisfy cleanly;
- schema evolution/migration requirements materially exceed the simple local model.

Until then, additional database/search infrastructure is overengineering.
