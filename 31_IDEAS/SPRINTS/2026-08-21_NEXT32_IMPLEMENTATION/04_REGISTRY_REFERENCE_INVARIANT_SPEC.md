# REGISTRY REFERENCE INVARIANT — CANDIDATE SPEC

**Purpose:** N06 implementation candidate. Prevent system/self-improvement state from referencing SI candidates absent from the central Improvement Registry or claiming VERIFIED_CURRENT without evidence.

## Scan surfaces
1. `CURRENT_IVDIVO_SYSTEM_STATE.json`
2. `CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE.json`
3. `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json`

## Required invariants
For every token matching `SI-[0-9]{4}` in current state surfaces:
- candidate exists exactly once in central registry;
- candidate_id matches registry key/value;
- lifecycle status is allowed;
- ACTIVE/HOLD/VERIFIED states have owner_role, next_action and next_gate;
- VERIFIED_CURRENT has non-empty `verification_evidence` and `application_targets`;
- HOLD_WITH_TRIGGER has a reopen/hold trigger;
- REJECTED/SUPERSEDED/ROLLED_BACK has reason/terminal_reason;
- duplicate candidate IDs fail;
- state may not invent a newer candidate by reference only.

## Negative fixtures
- state references `SI-9999`, registry absent -> FAIL `MISSING_CANDIDATE`;
- registry candidate VERIFIED_CURRENT with empty verification_evidence -> FAIL `UNVERIFIED_VERIFIED_CURRENT`;
- ACTIVE candidate missing owner_role -> FAIL `MISSING_OWNER`;
- HOLD candidate missing hold_trigger -> FAIL `MISSING_REOPEN_TRIGGER`;
- duplicate SI-0008 records -> FAIL `DUPLICATE_CANDIDATE_ID`.

## Current observed defect
`CURRENT_IVDIVO_SELF_IMPROVEMENT_STATE.json` schema 2.7 states that transcript-recovery extension should be registered as SI-0008; repository search did not resolve SI-0008 in the central registry during this sprint. Expected invariant outcome before repair: FAIL `MISSING_CANDIDATE: SI-0008`.

## Promotion gate
The invariant becomes CURRENT only after:
1. exact-current registry mutation adds/reconciles SI-0008;
2. positive scan passes;
3. all negative fixtures fail as expected;
4. test is wired into the self-improvement audit/CI surface without breaking current registry candidates;
5. readback proves main and Drive mirrors no longer disagree.

**Evidence class:** INTERNAL/MACHINE VALIDATION. It does not prove story quality, human signal, provider success or market demand.