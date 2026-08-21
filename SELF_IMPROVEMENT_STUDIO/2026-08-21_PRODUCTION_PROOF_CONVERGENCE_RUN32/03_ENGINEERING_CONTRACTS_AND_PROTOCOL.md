# ENGINEERING CONTRACTS + PROTOCOL v1.0

Status: WORKING CANDIDATE / NOT CURRENT AUTHORITY

## 1. Production Proof Chain
**Module:** `tools/ivdivo_proof_chain.py`  
**Schema:** `schemas/IVDIVO_PRODUCTION_PROOF_CHAIN_SCHEMA_v1.json`

Pipeline:
`AUTHORITY SNAPSHOT -> EVIDENCE OBJECTS -> CLAIMS -> GATE COMPUTATION -> ARTIFACT READBACK -> PROOF_ID`

Contracts:
- Evidence IDs are unique.
- FAIL/REJECTED evidence cannot silently support PASS.
- Required source classes must be explicitly present.
- Human evidence must originate from a human source class; provider-live claims require live external source class.
- Founder approval must be an explicit PASS evidence object of source `FOUNDER` (or allowed human class), never a model inference.
- Required artifact identities must exist; declared hash/readback mismatch is FAIL.
- Declared gate verdict differing from computed verdict is FAIL_CLOSED.
- `proof_id` is deterministic over authority snapshot + computed claims/gates + artifact identities.

Compatibility: consumes concepts from P53 `IVDIVO_EVIDENCE_CONTRACT_v1` and `IVDIVO_GATE_CONTRACT_v1`; does not replace them.

## 2. GitHub↔Drive Mirror Integrity
**Module:** `tools/ivdivo_mirror_integrity.py`  
**Schema:** `schemas/IVDIVO_MIRROR_INTEGRITY_MANIFEST_SCHEMA_v1.json`

Modes:
- `EXACT_BYTES`: raw SHA-256 required on both peers.
- `SEMANTIC`: compare declared authority epoch, frontier, status and optional semantic fingerprint.

Hard law: **mtime/revision date is freshness evidence only, never an authority selector**.

Failure classes:
`MISSING_*_MIRROR`, `AUTHORITY_EPOCH_DIVERGENCE`, `FRONTIER_DIVERGENCE`, `STATUS_DIVERGENCE`, `RAW_HASH_REQUIRED`, `RAW_HASH_MISMATCH`, `SEMANTIC_FINGERPRINT_MISMATCH`, stale expected peer revision.

## 3. Routing Write-Through Consistency
**Module:** `tools/ivdivo_routing_consistency.py`  
**Schema:** `schemas/IVDIVO_ROUTING_CONSISTENCY_SCHEMA_v1.json`

Terminal events currently modeled:
- FOUNDER_LOCK
- FINAL_STORY_GATE_PASS
- EXTERNAL_PROVIDER_REQUIRED
- HUMAN_EVIDENCE_REQUIRED

Contract:
- required routing layers must exist;
- status/event provenance must match the terminal event artifact;
- optional `SYSTEM_AGGREGATE` layers may declare `track_event=true` + `normalized_event`; they are not forced to carry project-style `observed_status`; stale normalized event is detected even when a higher-precedence overlay currently protects routing;
- locked projects cannot route to more prose;
- repair output is `PATCH_ROUTING_ONLY`, never story rewrite;
- module never creates Founder authority.

## 4. Candidate Value / Pruning Guard
**Module:** `tools/ivdivo_value_guard.py`  
**Schema:** `schemas/IVDIVO_CANDIDATE_VALUE_TELEMETRY_SCHEMA_v1.json`

Consumes measured telemetry from existing SI-0012/production telemetry; it does not invent measurements.

Measurement contract:
- `measurement_state = COMPLETE | PARTIAL | UNMEASURED`.
- No real project pilot -> `HOLD_FOR_REAL_PILOT`.
- Real pilot but incomplete value telemetry -> `HOLD_FOR_MEASUREMENT`.
- Regression introduced -> `REVISE_OR_ROLLBACK`.
- Low measured precision or negative measured net -> `PRUNE_OR_REVISE`.
- Multi-project + independent human evidence + positive measured net -> only `PROMOTION_REVIEW_ELIGIBLE`, never automatic promotion.

## 5. Proof protocol for production use
1. Fresh-read project authority and current main/Drive state.
2. Bind source revision/authority epoch.
3. Build evidence records without upgrading model/inference evidence.
4. Run proof chain.
5. Run mirror integrity for duplicated durable artifacts.
6. Run routing consistency for terminal state changes.
7. Persist results/read back.
8. Feed measured operational telemetry to value guard only after real usage.
9. Promote/merge only through existing Self-Improvement authority and review gates.

## 6. Rollback
All four modules are additive candidate utilities. Rollback = remove their code/schema/tests and candidate run records. Existing SI-0012, P53, Session Resilience, Writing and Audio authorities remain intact.

## 7. Schema/runtime conformance gate
Before candidate promotion or merge, schema syntax validation must be followed by real-instance validation for each materially different payload role. This run caught and repaired two routing schema drifts only at instance level.
