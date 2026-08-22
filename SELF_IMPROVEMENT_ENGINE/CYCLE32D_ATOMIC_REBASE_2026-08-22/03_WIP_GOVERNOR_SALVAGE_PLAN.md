# Cycle32D WIP Governor — Atomic Salvage Plan

Status: CANDIDATE / NOT YET MERGED

Source: stale Cycle32D executable branch `self-improvement/cycle32d-executable-decision-yield-registry-race-2026-08-22`.
Target: CURRENT Cycle10 runtime on fresh main.

Unique mechanism to salvage: `meta_wip_limiter` only.

Do not salvage duplicate mechanisms already represented in CURRENT Cycle10, including production-return control, VOI routing, prompt dedupe, registry collision checks, rollback routing and asset registry validation.

Bounded semantics:
- normal meta envelope: `primary_meta <= 1` and `pilots <= 2`;
- overflow -> `STOP_WIP_LIMIT`;
- explicit Founder switch, prerequisite work, or production-blocked state may permit a bounded exception;
- exception must be observable as an exception, not silently normalized;
- this controls meta/self-improvement WIP, not normal production chapter/episode concurrency.

Acceptance tests:
1. (1 primary, 2 pilots) => PASS;
2. (2 primary, 3 pilots) => STOP_WIP_LIMIT;
3. same overflow + Founder switch => PASS exception;
4. same overflow + prerequisite => PASS exception;
5. same overflow + production_blocked => PASS exception;
6. no new global SI ID;
7. no whole Cycle32D promotion;
8. fresh-main dedupe/rebase check immediately before merge.
