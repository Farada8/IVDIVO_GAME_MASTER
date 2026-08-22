# IVDIVO Self-Improvement — Production Launch Pack

Status: `REAL_PRODUCTION_ACTIVE`
Date: 2026-08-22
Authority effect: **NONE on Self-Improvement version authority**. Self-Improvement v2 remains `VERIFIED_CURRENT`.

## Purpose

Convert the laptop-first Personal AI / Business / Books / Projects concept into executable engineering. Every run card must produce concrete files/code/state/tests or an explicit `DESIGN_ONLY` / `BLOCKED` result.

## Controlling law

`PROMPT != ENGINE`

A prompt becomes engineering only when its required artifact, test, state transition and readback exist.

## Restore authority

Read these in order:
1. `CURRENT_PRODUCTION_LAUNCH_STATE.json` — authoritative current status/frontier overlay.
2. `PRODUCTION_LAUNCH_QUEUE_v0.1.json` — base dependencies and acceptance criteria.
3. `CURRENT_HANDOFF.md` — current restart instructions and evidence boundaries.
4. Relevant `PLxx_VERIFICATION_RECEIPT.json` files.
5. `PRODUCTION_LAUNCH_PROMPTS_v0.1.md` — original 25 production run cards.
6. `ENGINEERING_INTEGRATION_CONTRACT_v0.1.md` — execution/regression/authority contract.

The CURRENT overlay supersedes status/frontier fields only. Dependency edges and acceptance text remain owned by the base queue.

## Wave order

1. Wave 1 / Foundation: PL-00, PL-01, PL-02, PL-04, PL-05, PL-11.
2. Wave 2 / Real production: PL-06, PL-07, PL-08, PL-09, PL-13, PL-14.
3. Wave 3 / Reliability: PL-03, PL-10, PL-12, PL-16, PL-17, PL-18.
4. Wave 4 / Optimization: PL-15, PL-19, PL-20.
5. Wave 5 / Real pilots + release: PL-21, PL-22, PL-23, PL-24.

## Current executable frontier

`PL-07 BUSINESS RESEARCH`

PL-09 is already DONE_VERIFIED in the base queue. PL-03 is now DONE_VERIFIED through PR #416 and Drive readback, satisfying the remaining PL-07 dependency because PL-04 was already verified.

PL-13 remains independently READY; PL-07 is selected because completing the evidence layer now unlocks provenance-first business research directly.

## Completion semantics

- `READY`: admissible to execute now.
- `WAITING_DEPENDENCY`: not yet admissible.
- `RUNNING`: active execution with state/log.
- `BLOCKED`: real external/technical blocker recorded.
- `DONE_VERIFIED`: implementation + required tests/readback passed.
- `DESIGN_ONLY`: specification exists but runnable implementation does not.
- `FAILED`: execution attempted and acceptance gate failed.

No card may be marked `DONE_VERIFIED` merely because an assistant described what should exist.
