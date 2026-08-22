# Cycle32D — Executable Decision-Yield Utility Convergence

Date: 2026-08-22
Status: ADDITIVE CONVERGENCE / LOCAL CANDIDATE / NO AUTHORITY PROMOTION

## Why this file exists
Two Cycle32D implementation branches were created concurrently:
- PR #206: canonical Cycle32D persistence/readback + real-project stale-router/resume-gate line;
- PR #218: separate executable utility/conformance line.

Keeping both as competing merge candidates would violate Cycle32D's own duplicate-build and freshness laws. PR #206 is therefore selected as the convergence target because it already contains real D01/D10/D09/D04 canaries, stale-router runtime, heterogeneous regression, v2 resume-gate integration and the global candidate `tools/ivdivo_resume_guard.py`.

PR #218 is reduced to provenance after unique utility functions are salvaged here.

## Unique executable delta salvaged from PR #218
`tools/cycle32d_decision_yield_utilities.py` adds deterministic implementations for:
1. active-surface SI-ID extraction and read-only collision detection;
2. explicit `NO_ALLOCATION` when no ID should be issued;
3. multi-dimension freshness vector with stale/missing surfaces;
4. prompt functional fingerprinting and duplicate-bank detection;
5. decision/evidence yield with `REJECT_NO_EFFECT`;
6. ordinal Value-of-Information routing with no fake money/time precision;
7. evidence-class ceiling classification;
8. selective descendant rollback while preserving locked nodes;
9. input-asset registry validation.

These functions operationalize existing Cycle32D contracts C02/C04/C05/C06/C08/C09/C13/C21 instead of creating a new authority.

## Regression
Local exact-source test before persistence:
- `19 passed in 0.04s`.
- Real SI-0016 open-PR collision case returns `STOP_COLLISION`.
- No-ID path returns `NO_ALLOCATION`.
- E5 claim from E2 evidence returns `NOT_PROVEN_EVIDENCE_CEILING`.
- no-effect meta step returns `REJECT_NO_EFFECT`.
- locked dependency is excluded from selective rollback.

GitHub path:
- `SELF_IMPROVEMENT_DELTAS/CYCLE32D_2026-08-22/tests/test_cycle32d_decision_yield_utilities.py`

## Interaction with existing Cycle32D runtime
This utility layer does not replace:
- `tools/cycle32d_stale_router_validator.py`;
- `tools/cycle32d_resume_gate.py`;
- `tools/ivdivo_resume_guard.py`;
- v2 registry lifecycle;
- SI-0014 interruption recovery;
- SI-0015 slice freshness.

Instead it supplies lower-level deterministic checks used before or around those routers.

## Evidence / promotion boundary
- read-only collision detection != transactional reservation;
- test pass != Human Signal/provider/market evidence;
- prompt dedupe != literary/product improvement proof;
- local canary != universal promotion;
- Self-Improvement v2 remains VERIFIED_CURRENT;
- v3 remains candidate/HOLD;
- Cycle32D remains bounded/local candidate pending normal v2 lifecycle evidence.

## Convergence decision
- PR #206 = KEEP as primary Cycle32D convergence surface.
- PR #218 = CLOSE UNMERGED / SUPERSEDED, preserve branch for provenance only.
- No second Run32 or second Next64 is counted from PR #218.
