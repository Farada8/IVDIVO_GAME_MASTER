# CYCLE 8 — ENGINEERING CONTRACTS / PROOFS / PROTOCOLS

## EC8-01 Registry Reservation Contract
Inputs: complete committed registry family, open reservations, freshness token.  
PASS only with complete visibility and zero committed↔reserved collision.  
Output may compute a next-unreserved label but MUST NOT allocate it automatically.

## EC8-02 Durable Action Contract
Order: `FRESH_AUTHORITY -> CHECKPOINT -> BLOCKER/DRIFT -> EFFECT_RECONCILIATION -> READBACK -> SAFE_MISSING_ACTIONS -> PROOF/TELEMETRY -> LEARNING`.  
`STARTED_UNKNOWN` + paid/irreversible => `QUARANTINE_NO_REPLAY`.

## EC8-03 Recovery Evidence Contract
A recovery event requires: fresh authority, pre-interruption checkpoint, post-restart authority readback, recovery readback, project identity match, source-hash match.  
Checkpoint main drift => `REBASE_FIRST`.

## EC8-04 Evidence Firewall Contract
Every material claim carries `evidence_class` + `root_source`.  
Derived reports inherit the same evidence family.  
Machine/model/provider artifacts cannot be upgraded to `HUMAN_SIGNAL`.

## EC8-05 Economics Contract
Unknown numeric values are `null`.  
`0` is legal only when measurement is explicit.  
Forecasts and missing telemetry never become measured spend or labor.

## EC8-06 Prompt IR Parity Contract
Protected facts, prohibitions and evidence gates are semantic obligations.  
Any omitted/changed protected obligation => `PARITY_FAIL`.  
Token-count similarity is irrelevant.

## EC8-07 Book Sensor Scope Contract
Scope widening requires: independent replication clean, healthy-control false positives = 0, and at least one real human/editor adjudication.  
Any healthy-control hit => HOLD.

## EC8-08 Production Lock Ladder
`PROVIDER_ACCEPTED < PRODUCTION_ACCEPTED < TAKE_LOCKED < VOICE_LOCKED < RELEASE_LOCKED`.  
No lower state implies a higher lock.

## EC8-09 Portfolio Information Governor
Select the lowest-numbered priority among admissible work, then highest information gain.  
If P1/P2 real evidence is admissible, meta expansion must yield.

## EC8-10 Recovery Promotion Contract
Promotion review requires >=3 genuine interruption recoveries across >=2 projects and zero false resume.  
Controlled/synthetic recovery never counts as genuine evidence.

## Proof obligations
- 24 deterministic tests must pass.
- No story/canon file may be modified.
- No new SI identity may be allocated.
- Any external evidence gap remains explicit HOLD.
- Fresh-main compare is required before PR creation and again before merge.
- Drive write-through requires post-write readback.
