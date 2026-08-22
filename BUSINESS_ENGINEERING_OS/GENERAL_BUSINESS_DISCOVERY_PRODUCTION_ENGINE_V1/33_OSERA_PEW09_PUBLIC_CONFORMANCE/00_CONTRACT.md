# P-EW09 — OSERA PUBLIC BACKPATCH CONFORMANCE / COMPLETENESS FALSIFICATION GATE

**Date:** 2026-08-22  
**Status:** WORKING INTERNAL PROOF / NO WIP PROMOTION / NO EXTERNAL ACTION  
**Parent handoff:** post-P-EW08 early-wave radar  
**State reconciliation:** this proof does **not** overwrite the earlier unmerged `DELTA03 = PROTECT_NO_CHANGE` recovery branch. It tests whether later OSERA evidence is strong enough to justify a superseding delta.

## Hypothesis under test

`OSERA_DRAFT_RELEASE_EVIDENCE_CONFORMANCE_AND_COMPLETENESS_QA`

The business hypothesis survives only if public evidence exposes at least **two independent, substantial, reproducible evidence-gap classes** that a low-capital independent checker can detect without providing legal certification, vulnerability scanning, SBOM dashboards, or patch production.

`ONE_GAP_CLASS_ONLY -> KILL_AS_CURRENT_NEW_WIP`

## Frozen public sample

The sample was frozen before interpreting results from the first ten repositories returned by the public `finos-osera` `backpatch-` repository search:

1. `backpatch-gson`
2. `backpatch-jetty`
3. `backpatch-camel`
4. `backpatch-commons-lang`
5. `backpatch-bouncycastle`
6. `backpatch-activemq`
7. `backpatch-okhttp`
8. `backpatch-tapestry`
9. `backpatch-cxf`
10. `backpatch-graphql-java`

Expected baseline and release tags are pinned from OSERA's own July 2026 public release-tag inventory.

## Machine-checkable controls

For each frozen repository the live scanner checks six bounded controls:

1. `FORK-001` repository name begins `backpatch-`;
2. `FORK-002` at least one current `refs/heads/backpatch/<version>` ref is visible;
3. `FORK-003` the expected `v<VERSION>+backpatch.baseline` ref resolves;
4. `REL-003A` at least one expected `+backpatch.NNN` release ref resolves;
5. `REL-003B` release base version matches the baseline base version;
6. `REL-003C` observed release ordinals for the line are positive and strictly increasing.

`REL-001` is **not** failed merely because public GitHub Actions are absent: the draft explicitly allows provider-private build/test execution.  
`REL-002` is tracked as a standards/tooling gap, not counted as a frozen-repo release defect unless published artifact evidence is actually measured. The draft itself says an automated publish-time bytecode comparison still should be defined.  
`EVD-001` is Pre-Draft and therefore cannot be used as a hard current conformance failure.

## Classification rules

A repository control is `PASS`, `GAP_TARGET_STANDARD`, or `UNKNOWN`; the scanner must not silently convert missing public evidence into a mandatory failure when the draft does not support that inference.

Gap classes are counted independently:

- `CURRENT_BACKPATCH_BRANCH_CONVENTION_GAP`: reproducible only when release/baseline refs resolve but no current `backpatch/*` branch is visible. Because OSERA says not every historical repository uses the target convention, this is a target-standard gap, not a claim that the release is invalid.
- `BASELINE_TAG_GAP`: expected baseline ref absent.
- `RELEASE_TAG_GAP`: expected published release ref absent.
- `VERSION_LINEAGE_GAP`: baseline/release base versions or release ordinals conflict.

The explicit `REL-002_AUTOMATED_ACCEPTANCE_CHECK_NOT_YET_DEFINED` standards gap is recorded separately and **does not** become a second release-defect class by rhetoric.

### Business route

- `>=2` independent frozen public gap classes -> `PASS_TECHNICAL_WEDGE_SURVIVES_M1_ONLY`
- `<2` independent frozen public gap classes -> `KILL_AS_CURRENT_NEW_WIP_WATCH_STANDARD_EVOLUTION`

Green CI means only that the live public experiment executed and classified itself under this contract.

## Commercial boundary

Whatever the technical result:

- `BUYER_DEMAND = UNPROVEN`
- `WTP = UNKNOWN`
- `PRICE = NULL`
- `TRANSACTIONS = 0`
- `PROFITABILITY = UNPROVEN`
- `WIP_PROMOTION = FALSE`
- `EXTERNAL_ACTION_AUTHORIZED = FALSE`

No claim of CRA compliance, software safety, certification, or buyer demand is authorized by this gate.