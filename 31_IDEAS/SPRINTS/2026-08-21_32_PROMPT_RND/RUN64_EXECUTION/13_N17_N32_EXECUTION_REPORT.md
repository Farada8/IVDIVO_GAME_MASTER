# IVDIVO RUN64 — N17–N32 EXECUTION REPORT

**Date:** 2026-08-21  
**Status:** EXECUTED SEQUENTIALLY / INTERNAL FIXTURES WHERE PROJECT-SPECIFIC SOURCE NOT REQUIRED / NOT STORY CANON

## N17 — Protagonist state-change ledger
PASS IMPLEMENTATION. Added `schemas/PROTAGONIST_STATE_CHANGE_LEDGER_v1.json` tracking present want, action/tactic, world/partner response, changed state, price, next adaptation and agency-effect class.

## N18 — Agency without aggression bias
PASS INTERNAL FIXTURES. `05_N18_AGENCY_VALIDATION_FIXTURES.json` proves quiet refusal, relational boundary, investigative restraint and action rescue can all be agency when they change state; loud inconsequential behavior fails.

## N19 — Opposition adaptation ledger
PASS IMPLEMENTATION. Added `schemas/OPPOSITION_ADAPTATION_LEDGER_v1.json`: protagonist move -> opposition observation/inference -> counter-move -> new constraint -> adaptation -> price.

## N20 — Causal escalation across genres
PASS INTERNAL CROSS-GENRE FIXTURES. `06_N20_OPPOSITION_GENRE_VALIDATION.json` covers mystery, romance/melodrama, orbital youth and Smith/OES, plus arbitrary-cruelty negative control.

## N21 — Behavioral contradiction card
PASS IMPLEMENTATION. Added `schemas/CHARACTER_BEHAVIORAL_CONTRADICTION_CARD_v1.json`, requiring pressure events where competing values alter chosen action/cost/later pattern. Private rehearsal biography remains private by default.

## N22 — Contradictions in behavior
PASS INTERNAL FIXTURES. `07_N22_CONTRADICTION_BEHAVIOR_VALIDATION.json`: adjective-only and exposition-only contradictions fail; choice-altering contradiction passes.

## N23 — Social Reality Pressure Card
PASS IMPLEMENTATION. Added `schemas/SOCIAL_REALITY_PRESSURE_CARD_v1.json` for money/work/housing/status/family/bureaucracy/law/community/institution/education/transport etc only when they change strategy/access/risk/relationship/status/time/price.

## N24 — Sociology without exposition
PASS INTERNAL CROSS-DOMAIN FIXTURES. `08_N24_SOCIAL_REALITY_VALIDATION.json` demonstrates action-bearing pressure in commercial romance, Orbital Youth and Smith/OES; exposition-only control fails.

## N25 — Ensemble Relationship Authority Graph
PASS IMPLEMENTATION. Added `schemas/RELATIONSHIP_AUTHORITY_GRAPH_v1.json` with trust/boundary/power/debt/knowledge asymmetry/vulnerability/rupture/repair/consent/unresolved obligation and explicit `privileged_knowledge_is_not_consent` control.

## N26 — Consent/power timeline variants
PASS INTERNAL STRESS TEST. `09_N26_RELATIONSHIP_CONSENT_POWER_STRESS_TEST.json` covers erased-memory/time-loop, boss/employee, rescuer/rescued, wealthy/powerful and professional-investigative cases. Prior intimacy/knowledge/rescue/power never becomes automatic present consent.

## N27 — Pair-state dialogue card
PASS IMPLEMENTATION. Added `schemas/PAIR_STATE_DIALOGUE_CARD_v1.json` with pair objectives, resistance, status, withheld fact, tactics, listening, interruption, subtext and final state delta; P51/P52/P53 remain conditional.

## N28 — Dialogue rewrite causality
PASS INTERNAL A/B FUNCTION TEST. `10_N28_DIALOGUE_CAUSALITY_AB_TEST.json` compares witty-information exchange with pair-state action dialogue; only the latter changes action/status/relationship through listening-triggered tactic shifts. Human naturalism preference not claimed.

## N29 — Scene delete/swap tests
PASS IMPLEMENTATION. Added `tools/scene_modularity_audit.py`; diagnoses deletion dependencies and adjacent swaps, while protecting declared parallel/montage structures from false failure.

## N30 — Modularity detection
PASS TEST DESIGN. Added `tests/test_scene_modularity_audit.py`: strong causal chain detects broken dependencies; filler block surfaces REVIEW; legitimate parallel montage remains reorderable.

## N31 — Universal evidence-ledger schema
PASS IMPLEMENTATION. Added `schemas/IVDIVO_MYSTERY_EVIDENCE_LEDGER_v1.json`: fact/source/lineage/access/reliability/surface meaning/true meaning/alternative model/corroboration/current-timeline availability/action/payoff/final-proof support.

## N32 — Final-proof fairness
PASS INTERNAL FIXTURES. `11_N32_FINAL_PROOF_FAIRNESS_VALIDATION.json`: current-timeline converging proof passes; erased-timeline author-only proof fails; retrospective reinterpretation passes only with an earlier accessible trace.

## RESULT
This tranche moves several recurring craft principles from prose advice into explicit, inspectable contracts while preserving the Human Signal and project-specific application boundaries.
