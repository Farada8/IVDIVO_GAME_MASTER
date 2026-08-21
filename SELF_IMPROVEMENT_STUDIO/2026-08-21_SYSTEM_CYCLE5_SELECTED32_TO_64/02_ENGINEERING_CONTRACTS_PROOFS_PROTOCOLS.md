# CYCLE 5 — ENGINEERING CONTRACTS + PROOFS + PROTOCOLS

## Contracts
**EC-C5-01 CURRENT_SURFACE_RESOLUTION** — choose within explicit scope; equal-rank differing hashes require declared supersession or SPLIT_BRAIN_STOP. Timestamp alone cannot win.

**EC-C5-02 SCOPE_READINESS_VECTOR** — story, Founder, provider, human and market readiness are independent dimensions. Advancing one MUST NOT mutate another.

**EC-C5-03 EVIDENCE_CLAIM_CEILING** — NONE < MODEL < DRY < MACHINE < PROVIDER < HUMAN < FOUNDER. A claim cannot exceed its minimum evidence class.

**EC-C5-04 SHARED_FACT_CAS** — protected/shared working facts commit only with exact expected `value_hash + version`; stale writers rebase.

**EC-C5-05 EVIDENCE_FAMILY** — derived summaries/translations/model reports inherit the originating evidence `family_id`; transformations do not multiply independent evidence.

**EC-C5-06 MUTATION_INTENT** — every mutable write declares target, expected hash, intended new hash, reversibility and approval requirement before execution.

**EC-C5-07 MULTI_SURFACE_TRANSACTION** — GitHub + Drive + state pointer are not one success until all declared surfaces are read back and acknowledged. Partial success is PARTIAL/REPAIR_REQUIRED, never COMPLETE.

**EC-C5-08 TRANSACTION_RECOVERY** — persist applied targets/acks, retry idempotently, resume only unapplied targets, reject ambiguous replay.

**EC-C5-09 STATE_SHAPE_GUARD** — minimum route-state semantics include schema_version/status/authority_order/resume_algorithm. Missing semantic fields fail closed; adapters may translate known versions but never invent authority.

**EC-C5-10 SELF_IMPROVEMENT_GOVERNOR** — ready P1/P2 real production preempts meta unless a system FATAL blocks it. Bounded P0 integrity may proceed when P1/P2 are genuinely Founder/external blocked.

**EC-C5-11 ANTI_BLOAT_REUSE** — named policies sharing one primitive reuse it. False Progress + Evidence Inflation share evidence-class ceilings; no parallel mini-engines.

**EC-C5-12 PROMOTION_BOUNDARY** — engineering PASS can create GO_FOR_REVIEW eligibility only. CURRENT, Founder, human, provider, market and release decisions retain their own gates.

## Live proofs
**PROOF-C5-001 STALE BRANCH:** PR #104 is OPEN/DRAFT/NON-MERGEABLE and main advanced after its base. Therefore green-at-creation != safe-to-merge-now.

**PROOF-C5-002 SCOPE SEPARATION:** D09 Final Story Gate PASS but Founder lock absent. D10 Founder story lock exists while provider/human/market claims remain absent. Readiness is a vector.

**PROOF-C5-003 STALE MUTATION:** persisted prior live evidence records exact-SHA write success followed by intentional stale old-SHA rejection while committed bytes survived. Stale failure is safety success.

**PROOF-C5-004 PARTIAL WRITE:** persisted prior fault injection produced payload success + later state-write failure; readback set REPAIR_REQUIRED instead of false PASS.

**PROOF-C5-005 AGREEMENT IS NOT EVIDENCE:** current system law already sets duplicate evidence weight=0 and model agreement without independent evidence=false; candidate test confirms three derivatives of one source family count as one.

**PROOF-C5-006 GOVERNOR:** current D01/D09 are Founder-decision gated and current decisive audio steps require external/human evidence, so this bounded P0 pass does not starve ready P1/P2. Negative test proves a ready P1 task preempts meta.

## Write-through protocol
1 fresh-read exact target revision/hash; 2 declare mutation intent/scope; 3 authority/protected-fact/approval check; 4 write one surface; 5 exact readback; 6 journal acknowledgement; 7 continue remaining surfaces; 8 if later failure after any success => REPAIR_REQUIRED; 9 recover idempotently; 10 COMMITTED only after all required readbacks; 11 fresh-read again because sibling work may have advanced.

## Evidence protocol
same source summarized by N models = one family; deterministic test != literary/human proof; dry != provider; provider != human artistic acceptance; human != Founder canon decision; Story Gate PASS != Founder lock; metrics != market behavior.
