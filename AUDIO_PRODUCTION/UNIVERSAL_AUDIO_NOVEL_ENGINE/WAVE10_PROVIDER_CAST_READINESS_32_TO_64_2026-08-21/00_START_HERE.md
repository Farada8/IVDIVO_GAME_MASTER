# IVDIVO AUDIO NOVEL ENGINE — WAVE10 PROVIDER→CAST READINESS 32→64

Status: WORKING until fresh CI + merge/readback. Date: 2026-08-21.

## Why this cycle exists
The shared Audio Studio runtime, production control, external-evidence trust, provider snapshot acquisition, human evidence and durable live-lineage systems already exist. The real empirical frontier is provider/cast evidence. Wave10 therefore does **not** create another Audio Engine. It closes the deterministic handoff from a real authenticated ProviderSnapshot to a versioned provisional cast/audition package, while preserving all external evidence gates.

## New bounded modules
- `audio/studio/runtime/provider_snapshot_diff.py`
- `audio/studio/runtime/provider_inventory_compiler.py`
- `audio/studio/runtime/cast_readiness.py`

## Contracts / protocols
- `contracts/PROVIDER_SNAPSHOT_REPEATABILITY_CONTRACT_v1.md`
- `contracts/PROVIDER_INVENTORY_COMPILATION_CONTRACT_v1.md`
- `contracts/CAST_CANDIDATE_READINESS_CONTRACT_v1.md`
- `protocols/PROVIDER_TO_CAST_SELF_IMPROVEMENT_PROTOCOL_v1.md`

## Research / proof package
- `01_32_PROMPTS_AND_EXECUTION_RESULTS.md` — sequential 32-prompt disposition.
- `02_SYNTHESIS_PATH_TO_GOAL.md` — integrated findings and next causal path.
- `03_PARALLEL_DEVELOPMENT_ANALYSIS.md` — GitHub/Drive dedupe and reuse decisions.
- `04_PROOF_LEDGER.json` — proof classes and evidence ceilings.
- `05_MACHINE_STATE.json` — resumable machine frontier.
- `06_NEXT_64_PROMPTS.md` — exactly 64 evidence-driven next prompts, not blindly auto-authorized.

## Exact external frontier
`AUTH_PROVIDER real snapshot -> repeatability -> real inventory -> NARRATOR/ETHAN/AOIFE candidates -> heard Ифа/Контакт -> multi-state/pair/fatigue -> human lock -> pre-spend GO -> RB001/RB002/RB003`.

## Evidence ceiling
This engineering cycle performs no provider read, no paid synthesis, no real voice lock, no human listening, no real Lesson Zero alignment and no measured provider economics. Fixtures prove code behavior only.
