# WAVE8 — CI / DRIVE READBACK / FRONTIER

Date: 2026-08-21

## CI chronology

### Run #63 — failure that exposed contract drift
- dedicated Audio Novel runtime: 4/4 PASS;
- full Audio Studio: 194 tests;
- result: 2 failures + 21 errors.

Root causes were stale fixtures/expectations after stricter Wave8 contracts:
1. `candidate_binding_sha256` became mandatory for human-review evidence;
2. `spend_ledger_state` and durable references became mandatory for live escrow;
3. V1 proof requirements added `REAL_ALIGNMENT` and `DURABLE_RECOVERY`;
4. ACCOUNT_WIDE inventory could no longer be upgraded by caller assertion alone.

The repair updated tests/contracts without weakening these safeguards.

### Run #74 — current green evidence observed
- dedicated runtime: 4/4 PASS;
- full Audio Studio: 199/199 PASS;
- GitHub Actions conclusion: SUCCESS.

Evidence ceiling: CI proves tested code behavior on the tested merge result. It does not prove provider authentication, human listening, live audio, real alignment, measured economics, durable real recovery, cross-project portability or artistic release.

## Drive mirror

Folder: `WAVE8_32_EXECUTIONS_2026-08-21`
Drive ID: `1ytMxCtllxyVfqiRTyRb_wjgfRbppcw0y`

Original mirror documents:
- 00 START HERE
- 01 Wave8 prompts 01–32 execution report
- 02 Engineering contracts and Self-Improvement
- 03 Synthesis and path to V1
- 04 64 next prompts Wave9

Added during independent convergence pass:
- 05 MACHINE STATE AND CI READBACK — `1blsvYU_VZWpEVZukgUTiojppye5an0xYs5l9YZ25AiA`
- 06 INDEPENDENT RED TEAM CONVERGENCE — `1n46c4YrTjtFPflsV2AN0kOlijqm6Zi00zRLX6CsvgdE`

Both added documents were moved into the Wave8 folder and their parent IDs read back successfully.

## Parallel state

Wave7 and PR103 are merged/current and should be reused.
Session Resilience Run33 / SI-0014 remains a candidate dependency for durable transaction recovery; Wave8 must not duplicate it.
System Cycle5 controls are represented on current main and should govern claim ceilings/evidence families/CAS/mutation/multi-surface/self-improvement semantics.

## Freshness

At the last explicit comparison, Wave8 was diverged from current main: 34 commits ahead / 26 behind, merge-base `b4c29e4a81fc368f440f39827df0adda46b4c897`. Current main observed SHA was `55c69de4f19aec1c2b408020c1447cbd38beef5b`.

Therefore **fresh-main reconciliation is still a required integration gate**, even after CI #74.

## Current exact frontier

Internal:
`RED_TEAM_BOUNDARIES -> FRESH_MAIN_RECONCILE -> FRESH_MERGE_RESULT_CI -> PACKAGE_READBACK -> SI_DISPOSITION`

External:
`AUTHENTICATED_SECRET_FREE_PROVIDER_PREFLIGHT -> TYPED PROVIDER SNAPSHOT -> REAL CAST/PRONUNCIATION/HUMAN EVIDENCE -> PRESPEND -> EXACT LIVE CANARY`.

No external provider/human/live/economics claims are made by this Wave8 engineering cycle.
