# BOOK INTELLIGENCE ENGINE — v1.1 UPGRADE
## ORTHOGONAL SOURCE LIFECYCLE + TRACEABILITY + V/V SPLIT

**Date:** 2026-08-22  
**Status:** ENGINEERING UPGRADE AUTHORIZED; deterministic prototype 9/9 PASS; repository runtime/tests still part of this same closure.

## Observed defect
v1.0 represented source progress as one linear field:
`REGISTERED -> INTEGRITY_VERIFIED -> STRUCTURE_MAPPED -> FULL_READ -> CLAIMS_EXTRACTED -> MECHANISMS_EXTRACTED -> ...`

That model conflicts with problem-targeted research. A source can be integrity-verified, read only in exact relevant sections, and still yield properly located local mechanisms. The linear model would force either a false `FULL_READ` claim or rejection of legitimate targeted extraction.

NASA Systems Engineering deep-source work exposed this defect concretely: inspected sections support local mechanisms with exact locators, but the 297-page handbook was not read cover-to-cover.

## v1.1 source state
Replace the single epistemic axis with three orthogonal dimensions:

### integrity_status
`UNKNOWN | VERIFIED | FAILED | QUARANTINED`

### read_coverage
`NONE | STRUCTURE_ONLY | PARTIAL_TARGETED | FULL_READ`

### extraction_stage
`NONE | CLAIMS_EXTRACTED | MECHANISMS_EXTRACTED | FAILURE_MODES_MAPPED | CROSS_SOURCE_COMPARED | OPERATIONALIZED | PROJECT_VALIDATED | SYNTHESIZED`

`lifecycle_stage` remains accepted only as a legacy compatibility field.

### Guard
`EXTRACTION_STAGE DOES NOT IMPLY FULL_READ`.

Claims/mechanisms require `PARTIAL_TARGETED` or `FULL_READ` plus a locator. Failed/quarantined sources cannot support extracted mechanisms.

## Verification vs Validation split
Engineering conformance and intended-use evidence are non-substitutable.

Evidence classes:
- ENGINEERING_VERIFICATION
- REAL_PROJECT_VALIDATION
- HUMAN_VALIDATION
- PROVIDER_VALIDATION
- MARKET_VALIDATION
- FACTUAL_SPECIALIST_VALIDATION
- LEGACY_UNCLASSIFIED

Only real validation classes count toward reusable-mechanism promotion. Engineering PASS can move implementation to local testing, not prove project usefulness.

## Bidirectional traceability
Required provenance path:
`SOURCE -> SECTION -> CLAIM -> MECHANISM -> ADAPTER -> PROJECT_APPLICATION -> TEST -> RESULT -> LEARNING -> ENGINE_RULE`

Promotion requires that a result can be traced backward to its source/claim/mechanism and a source-derived mechanism can be traced forward to what it actually changed.

New runtime audit must fail closed on:
- orphan node/edge;
- relation/type mismatch;
- result not traceable back to a source;
- promoted rule with missing application/result lineage.

## Change impact
Before changing a baseline source-derived rule, compute downstream descendants of the changed node. Use the result to identify affected adapters, project applications, tests, learnings and engine rules before write-through.

This extends the existing stale-write/rebase law; it does not authorize global rewrites.

## Legacy migration
Legacy records are not silently reclassified as newly observed evidence.
- REGISTERED -> UNKNOWN / NONE / NONE
- INTEGRITY_VERIFIED -> VERIFIED / NONE / NONE
- STRUCTURE_MAPPED -> VERIFIED / STRUCTURE_ONLY / NONE
- FULL_READ -> VERIFIED / FULL_READ / NONE
- legacy post-FULL_READ extraction stages preserve the old schema's implied FULL_READ for compatibility only.

Legacy pilot evidence without an explicit evidence class becomes `LEGACY_UNCLASSIFIED` and does not count as real project validation until classified from an actual artifact.

## Regression contract
Minimum deterministic tests:
1. targeted partial read + mechanism extraction validates without FULL_READ;
2. legacy STRUCTURE_MAPPED migrates without mechanism eligibility;
3. complete traceability chain PASS;
4. broken source-to-result chain FAIL;
5. change-impact descendants propagate correctly;
6. engineering verification alone cannot promote;
7. one real validation project => PILOT_READY, not PROMOTABLE;
8. two real validation projects + measurable gain => PROMOTABLE;
9. failed/quarantined source cannot support mechanism extraction.

## Promotion boundary
This upgrade can become `ENGINEERING_CURRENT` after exact runtime + deterministic regression PASS. It remains `PROJECT_VALIDATION_PENDING` until the upgraded traceability/evidence classification is applied to real current projects without regression.

No additional prompts are authorized merely to increase prompt count.