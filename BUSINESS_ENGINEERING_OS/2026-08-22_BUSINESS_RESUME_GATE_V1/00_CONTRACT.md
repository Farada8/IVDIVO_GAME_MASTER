# BUSINESS RESUME GATE v1

**Date:** 2026-08-22  
**Scope:** Business-local reliability/control-plane mechanism.  
**Backlog effect:** NONE — this is not P289 and does not consume a P225–P288 card.  
**Market-proof effect:** NONE.

## Problem
The Business CURRENT authority is now correct at 17/64 executed after P288, but a future chat/agent can still waste work by manually replaying blocked cards or interpreting “continue” as permission to invent missing tender/bidder evidence.

`BusinessResumeGate v1` makes the resume decision deterministic from authoritative state only.

## Canonical unlock intake
Current input contract:
`BUSINESS_ENGINEERING_OS/UNLOCK_INTAKE/PROC_BALLYBUNION_8872468_P225_P235_UNLOCK.md`.

The intake and Resume Gate are complementary, not competing:

`UNLOCK_INTAKE -> ADMISSIBLE AUTHORITY EVENT -> BUSINESS RESUME GATE -> EXACT ALLOWED NEXT CHAIN`.

The intake defines what can legitimately move P225 or P235. The gate decides what may run after that event. Intake text by itself has zero authority effect until the specified input/declaration is actually supplied and read back.

## Allowed routes
- `PROTECT_NO_CHANGE` — neither independent root has a new admissible authority event.
- `RESUME_P226_P234` — authentic target pack exists; process target authority.
- `RESUME_P225` — a real bidder designation exists but target pack is still missing.
- `RESUME_P235` — exact target registry exists but real bidder designation is missing.
- `RESUME_P236_P251` — real bidder designation exists; authoritative bidder packet is incomplete.
- `HOLD_FREEZE_BOTH_MANIFESTS` — authority exists but atomic frozen manifests are incomplete.
- `RESUME_P252_P280` — both frozen manifests exist; atomic requirement join/bounded decision layer may proceed.
- `HOLD_P281_P283_REVIEWER` — bounded decision packet exists but independent reviewer is not proven.
- `RESUME_P281_P283_THEN_HOLD_EXTERNAL` — independent reviewer can run internal PA4 layer; external action remains unauthorized.
- `RESUME_P284_P287` — explicit external-interaction authorization exists and real-use path may proceed under its own contracts.
- `DERIVE_NEW_FRONTIER_AFTER_REAL_EVIDENCE` — all prior state plus real use exists; P288 is NOT replayed.
- `HOLD_INCONSISTENT_STATE` — impossible downstream/upstream combinations fail closed.

## Core contracts
`CONTINUE_TEXT_NEQ_NEW_EVIDENCE_EVENT`

`UNLOCK_INTAKE_TEXT_NEQ_UNLOCK_EVENT`

`NO_NEW_ROOT_EVENT -> PROTECT_NO_CHANGE`

`TARGET_PACK_EVENT -> PROCESS_TARGET_AUTHORITY_ONLY`

`COMPANY_CONTEXT_NEQ_ACTUAL_BIDDER_DESIGNATION`

`ACTUAL_BIDDER_DESIGNATION_NEQ_COMPLETE_BIDDER_PACKET`

`BOTH_FROZEN_MANIFESTS_REQUIRED_BEFORE_ATOMIC_JOIN`

`INDEPENDENT_REVIEW_NEQ_EXTERNAL_ACTION_AUTHORIZATION`

`EXTERNAL_AUTHORIZATION_NEQ_REAL_USE_EVIDENCE`

`P288_EXECUTED_ONCE_NEQ_REPLAYABLE_CLOSURE_LOOP`

`RESUME_ROUTE_NEVER_PROMOTES_PROOF_GRADE`

`RESUME_ROUTE_NEVER_AUTHORIZES_EXTERNAL_ACTION_BY_ITSELF`

## Current real fixture
At the present canonical state:
- target_pack_acquired = false;
- actual_bidder_designation = false;
- all downstream readiness flags = false;
- unlock intake status = `AWAITING_AUTHORIZED_INPUT`.

Expected route:
`PROTECT_NO_CHANGE`

Reason:
`NO_NEW_ADMISSIBLE_ROOT_EVENT; WAIT_FOR_P225_OR_P235_AUTHORITY`.

This is consistent with canonical CURRENT and P288, not a new stop decision.

## Self-improvement classification
`LOCAL_KEEP_CANDIDATE` only.

Promotion beyond Business-local use requires at least one real resume event where the gate correctly changes route after new P225 or P235 authority, plus one negative control where a non-authoritative context change does not switch the frontier.
