# IVDIVO Self-Improvement — Production Launch Pack

Status: `PRODUCTION_BACKLOG_READY`
Date: 2026-08-22
Authority effect: **NONE on Self-Improvement version authority**. Self-Improvement v2 remains `VERIFIED_CURRENT`.

## Purpose

Convert the laptop-first Personal AI / Business / Books / Projects concept into an executable engineering backlog. This pack is intentionally anti-theatrical: every run card must produce files/code/state/tests or an explicit `DESIGN_ONLY` / `BLOCKED` result.

## Controlling law

`PROMPT != ENGINE`

A prompt becomes engineering only when its required artifact, test, state transition and readback exist.

## Files

- `PRODUCTION_LAUNCH_PROMPTS_v0.1.md` — 25 production run cards, PL-00..PL-24.
- `PRODUCTION_LAUNCH_QUEUE_v0.1.json` — machine-readable ordered queue and dependencies.
- `ENGINEERING_INTEGRATION_CONTRACT_v0.1.md` — execution, acceptance, regression and authority contract.
- `HANDOFF.md` — exact restart/continuation instructions.

## Wave order

1. Wave 1 / Foundation: PL-00, PL-01, PL-02, PL-04, PL-05, PL-11.
2. Wave 2 / Real production: PL-06, PL-08, PL-09, PL-13, PL-14.
3. Wave 3 / Reliability: PL-03, PL-10, PL-12, PL-16, PL-17, PL-18.
4. Wave 4 / Optimization: PL-15, PL-19, PL-20.
5. Wave 5 / Real pilots + release: PL-21, PL-22, PL-23, PL-24.

## Current executable frontier

`PL-00 MASTER PRODUCTION BOOTSTRAP`

Do not jump to later cards unless dependencies are already proven by persisted/read-back artifacts.

## Completion semantics

- `READY`: admissible to execute now.
- `WAITING_DEPENDENCY`: not yet admissible.
- `RUNNING`: active execution with state/log.
- `BLOCKED`: real external/technical blocker recorded.
- `DONE_VERIFIED`: implementation + required tests/readback passed.
- `DESIGN_ONLY`: specification exists but runnable implementation does not.
- `FAILED`: execution attempted and acceptance gate failed.

No card may be marked `DONE_VERIFIED` merely because an assistant described what should exist.