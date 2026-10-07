# RESEARCH_POLICY.md — Conditional Reuse / Existing-Solution Gate

- STATUS: APPROVED
- LAST UPDATED: 2026-10-07

## Trigger

Research is required only when the current plan introduces a meaningful decision about:

- a new mechanism;
- a new library/dependency/service/API;
- a new architecture component;
- build vs reuse/adapt/combine;
- a mechanism likely solved well by the standard library, native platform, existing internal code, or mature OSS.

## Method

1. Test whether the mechanism can be removed entirely without harming the Win Condition.
2. Check native/standard-library capability first.
3. Check existing internal project assets/mechanisms.
4. Compare a small number of high-fit mature alternatives; expand only if the choice remains uncertain.
5. Use community/issues evidence to expose friction, not as sole truth.
6. Stop when additional research is unlikely to change the decision.

There is **no ritual minimum of 5–10 projects** for every plan.

## Cost rule

Existing approved ChatGPT usage is allowed.

Prefer free/local mechanisms when adequate. Any **new recurring paid runtime/service dependency** requires explicit human approval before implementation.

## Record

When triggered, create a short file under `docs/research/<PLAN_ID>_*.md` containing:

- decision being resolved;
- candidates/mechanisms checked;
- reuse/adapt/build recommendation;
- maintenance/license/cost/runtime constraints that matter;
- rejected alternatives and why;
- final decision and revisit trigger.

Consequential outcomes also go in `docs/DECISIONS.md`.
