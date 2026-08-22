# CYCLE9 — PRE-P235 TEST-FIXTURE BIDDER DESIGNATION LAYER

**Date:** 2026-08-22  
**Case:** `PROC-BALLYBUNION-8872468`  
**State:** INTERNAL FIXTURE READY / P235 STILL HOLD

## Why this layer exists
Current connected evidence identifies `SYNTHESIS-IVDIVO LIMITED` and registration number `796820`, but company identity/context is not an explicit case-specific bidder designation.

The engine therefore needs a way to exercise bidder-bound code without laundering internal context into real bid intent.

## New control-plane modes
`TEST_FIXTURE_ONLY`
- may bind evidence-backed identity fields for internal regression/engineering;
- is never an actual bidder designation;
- cannot authorize requirement join, BID/HOLD/NO-BID, submission, outreach or procurement claims.

`ACTUAL_BIDDER`
- requires resource ID;
- legal entity;
- authorized designator;
- designation timestamp;
- explicit designation scope;
- active state.

Missing any required provenance returns `HOLD_INCOMPLETE_EXPLICIT_DESIGNATION`.

## New contracts
`TEST_FIXTURE_ENTITY_NEQ_EXPLICIT_BIDDER_DESIGNATION`

`COMPANY_CONTEXT_NEQ_EXPLICIT_BIDDER_DESIGNATION`

`BIDDER_DESIGNATION_REQUIRES_AUTHORIZED_ACTOR_TIMESTAMP_SCOPE_AND_ACTIVE_STATE`

`EXPLICIT_DESIGNATION_ALONE_NEQ_REQUIREMENT_JOIN_AUTHORITY`

Even a valid ACTUAL_BIDDER designation cannot unlock requirement join unless:
1. complete authoritative target pack is frozen; and
2. complete authoritative bidder capability packet is frozen.

## Current fixture
The stored fixture binds:
- resource `8872468`;
- legal entity `SYNTHESIS-IVDIVO LIMITED`;
- registration number `796820`;
- mode `TEST_FIXTURE_ONLY`;
- authorized designator `null`;
- active `false`.

Therefore:
`P235 = HOLD_NO_EXPLICIT_BIDDER_DESIGNATION`.

This is intentional and correct.

## Regression
Five additive deterministic guards cover:
1. fixture mode never becomes real bidder;
2. company context alone cannot designate bidder;
3. ACTUAL_BIDDER requires authorized actor/timestamp/scope/active state;
4. complete explicit designation may pass only the designation gate;
5. designation alone cannot unlock requirement join without both target and capability packets.

These tests are additive and do not alter the existing Cycle9 exact-32 count or the separate 3-case workspace award-state regression.

## Next causal gate
This layer reduces future P235 work to one explicit control-plane event if and only if the Founder actually intends the entity to be evaluated as bidder for this specific resource. Until then the engine may use only TEST_FIXTURE_ONLY mode.

P225 target-pack acquisition remains independently blocked on authenticated or user-provided official export.
