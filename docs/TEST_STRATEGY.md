# TEST_STRATEGY.md — Reel Ingestor Stable Verification Policy

- STATUS: APPROVED
- LAST UPDATED: 2026-10-07

Exact verification belongs in each `plan.md`. This file defines stable project-wide rules.

## Verification order

1. syntax/import/schema/static checks;
2. focused automated test for changed behavior;
3. reproduction using the smallest real/supplied fixture/input;
4. affected regression only;
5. artifact/output validation;
6. real local Windows/GPU/Instagram verification when the changed behavior depends on that environment;
7. human subjective/visual approval only when relevant.

## Principles

- Test behavior, not only exit code zero.
- Browser Worker sandbox success is not local production proof.
- Do not weaken validators/thresholds to manufacture PASS.
- Do not run Instagram/network/GPU regression for pure docs/control-plane changes.
- Do not run a giant full regression when a smaller affected boundary proves the change.
- Preserve frozen ingestion behavior unless the plan explicitly changes it.
- Preserve schema/prompt hashes unless the plan explicitly opens a version change.

## Stable lightweight checks

For Python-source plans, use the available project Python or system Python as appropriate:

```powershell
python -m py_compile .\reel_ingestor.py .\transcribe.py .\visual_evidence.py
python .\reel_ingestor.py --help
```

Do not assume these checks prove GPU/OCR/Instagram behavior.

## Ingestion regression gate

Required only when a plan changes acquisition, transcription, visual selection/OCR, status logic, circuit breakers, cleanup, or configuration semantics.

Minimum behavioral evidence should cover the changed boundary and verify relevant stable contracts, including where applicable:

- expected status;
- `visual_coverage_pass`;
- `visual_end_coverage_ratio >= 0.90`;
- `visual_span_coverage_ratio >= 0.85`;
- circuit-breaker semantics;
- source media cleanup/retention behavior.

Avoid repeated live Instagram calls when a local fixture can prove the same code path.

## Knowledge/corpus regression gate

For Step 5.4+ local knowledge work:

- canonical input JSON must remain unchanged by derived operations;
- schema-valid canonical artifacts must load deterministically;
- manipulation records must retain source knowledge identity/hash and user/prompt/context/output history as defined by the accepted plan;
- search/query behavior must be proven against real production knowledge artifacts, not benchmark-only assumptions;
- derived outputs must remain separate from canonical knowledge.

## Browser Worker local verification contract

Every implementation Plan returns `LOCAL_VERIFY.md` with:

- exact command(s);
- expected observable result;
- affected files/output paths;
- failure interpretation;
- any required human judgment.

The human runs it on the real project and returns evidence to the Architect before acceptance.
