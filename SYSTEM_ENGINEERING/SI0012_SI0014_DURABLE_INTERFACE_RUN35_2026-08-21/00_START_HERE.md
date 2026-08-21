# RUN35 — SI-0012 ↔ SI-0014 DURABLE INTERFACE CONVERGENCE

Status: WORKING ENGINEERING / CI AND DRIVE EVIDENCE REQUIRED BEFORE MERGE
Date: 2026-08-21

## Goal
Converge the already-existing SI-0012 single-store transaction semantics and SI-0014 multi-store recovery semantics behind one versioned compatibility interface, without creating another top-level engine.

## Current authorities preserved
- SI-0012 = Prompt Router / Meta-Orchestrator minimum compatibility runtime (`PILOTING`).
- SI-0014 = Session Resilience + Durable Recovery Stack (`READY_FOR_PILOT`).
- SI-0014 genuine-interruption promotion gate remains unmodified: qualified real recovery evidence across projects, zero false resume, review only.
- Project/canon/Founder authority outranks every checkpoint, transaction or telemetry record.

## New bounded artifacts
- `tools/ivdivo_durable_transaction_interface.py`
- `schemas/IVDIVO_DURABLE_TRANSACTION_INTERFACE_SCHEMA_v1.json`
- `tests/test_durable_transaction_interface.py`
- `ENGINEERING_CONTRACTS/DURABLE_TRANSACTION_INTERFACE_v1.0.md`
- `.github/workflows/durable-interface-run35-tests.yml`

## FATAL parallel-integrity repair
Fresh review of open PR #130 found a registry identity collision: its Project-slice Freshness candidate reused live `SI-0014`. The branch was repaired before merge:
- Session Resilience remains SI-0014;
- Project-slice Freshness moved to SI-0015 after full-family + open-PR reservation search;
- stale SI-0014 project-slice file deleted;
- historical redirect and PR metadata repaired;
- candidate-allocation law extended to open-PR reservations.

This repair is not evidence that SI-0015 is promoted or production-ready.

## New evidence law
`real_interruption=true` is not self-verifying evidence.
Only a qualified packet with unplanned origin, restart observation, pre-interruption checkpoint, post-restart authority readback, recovery readback, before/after project state and multiple durable evidence refs may enter the genuine threshold.

Controlled, synthetic and incomplete claims are normalized to `real_interruption=false`.

## Stop gates
- FATAL/MAJOR regression in old SI-0012/SI-0014 semantics;
- registry collision;
- false resume;
- controlled/synthetic evidence inflation;
- main/frontier drift with overlapping writes;
- provider/Founder/Human gate where external evidence is actually required.
