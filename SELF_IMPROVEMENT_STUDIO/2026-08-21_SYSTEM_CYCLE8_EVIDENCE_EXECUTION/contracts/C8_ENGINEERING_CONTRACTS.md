# SYSTEM CYCLE 8 — ENGINEERING CONTRACTS / PROOFS / PROTOCOLS

**Scope:** adversarial/evidence-validation layer. Reuse current writing-Cycle8/Cycle7/Run35/SI authorities where semantics already exist; do not create a competing engine.

## EC8-01 Registry Reservation Contract
Inputs: complete committed registry family, open reservations, freshness token.  
PASS only with complete visibility and zero committed↔reserved collision.  
Output may compute a next-unreserved label but MUST NOT allocate it automatically.  
**Disposition:** REUSE existing reservation law + adversarial canary.

## EC8-02 Durable Action Contract
Order: `FRESH_AUTHORITY -> CHECKPOINT -> BLOCKER/DRIFT -> EFFECT_RECONCILIATION -> READBACK -> SAFE_MISSING_ACTIONS -> PROOF/TELEMETRY -> LEARNING`.  
`STARTED_UNKNOWN` + paid/irreversible => `QUARANTINE_NO_REPLAY`.  
**Disposition:** REUSE Cycle7/Run35 + partial-write/paid-unknown canaries.

## EC8-03 Recovery Evidence Contract
A recovery event requires: fresh authority, pre-interruption checkpoint, post-restart authority readback, recovery readback, project identity match, source-hash match.  
Checkpoint main drift => `REBASE_FIRST`.  
**Disposition:** REUSE Run35 + identity/stale-main canaries.

## EC8-04 Evidence Firewall Contract
Every material claim carries `evidence_class` + `root_source`. Derived reports inherit the same evidence family. Machine/model/provider artifacts cannot be upgraded to `HUMAN_SIGNAL`.  
**Additional bounded value:** root-source family counting prevents derivative-report inflation.

## EC8-05 Economics Contract
Unknown numeric values are `null`. `0` is legal only when measurement is explicit. Forecasts and missing telemetry never become measured spend or labor.  
**Disposition:** REUSE writing-Cycle8/Cycle7 telemetry + false-zero canary.

## EC8-06 Prompt IR Parity Contract
Protected facts, prohibitions and evidence gates are semantic obligations. Any omitted/changed protected obligation => `PARITY_FAIL`. Token-count similarity is irrelevant.  
**Bounded unique assertion:** semantic protected-obligation parity surface.

## EC8-07 Book Sensor Scope Contract
Scope widening requires: independent replication clean, healthy-control false positives = 0, and at least one real human/editor adjudication. Any healthy-control hit => HOLD.  
**Bounded unique assertion:** MF-C03 promotion/scope guard.

## EC8-08 Production Lock Ladder
`PROVIDER_ACCEPTED < PRODUCTION_ACCEPTED < TAKE_LOCKED < VOICE_LOCKED < RELEASE_LOCKED`. No lower state implies a higher lock.  
**Bounded unique assertion:** typed non-substitutability across production locks.

## EC8-09 Portfolio Information Governor
Select the lowest-numbered priority among admissible work, then highest information gain. If P1/P2 real evidence is admissible, meta expansion must yield.  
**Disposition:** REUSE writing-Cycle8/self-improvement governor + starvation canary.

## EC8-10 Recovery Promotion Contract
Promotion review requires >=3 genuine interruption recoveries across >=2 projects and zero false resume. Controlled/synthetic recovery never counts as genuine evidence.  
**Additional bounded value:** explicit `false_resume_count > 0` promotion blocker.

## Proof obligations
- 24 deterministic tests must pass.
- No story/canon file may be modified.
- No new SI identity may be allocated.
- Any external evidence gap remains explicit HOLD.
- Direct `main` branch-ref + content readback is the freshness authority; recent-commit search alone is insufficient.
- Fresh-main compare is required before PR creation and again before merge.
- Drive write-through requires post-write readback.
- Mechanism overlap with writing-Cycle8/Cycle7/Run35/SI-0015 must be marked REUSE, not renamed as novelty.
