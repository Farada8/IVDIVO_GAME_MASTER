# CYCLE7 — ENGINEERING / CONTRACTS / PROOFS / PROTOCOLS

## Modules C7M01–C7M16
1. **C7M01 TargetAttachmentAuthorityGate** — separates current workspace metadata from current attachment-pack authority.
2. **C7M02 AuthorityGapCertificate** — emits explicit missing-evidence object with dependent decisions blocked.
3. **C7M03 AttachmentInventoryCompiler** — compiles document id/title/file/version/addendum/hash where available.
4. **C7M04 TenderLineageObject** — links related public procedures without importing requirements.
5. **C7M05 NonCarryoverGuard** — prior/benchmark facts cannot satisfy current tender requirements.
6. **C7M06 BenchmarkPackFixtureRouter** — allows real older/other packs to test parsers while preserving target isolation.
7. **C7M07 CriticalPathClockV2** — clarification/submission/opening/internal decision dates with null-safe missing events.
8. **C7M08 RequirementGapRouterV2** — MET/UNKNOWN/CURABLE/NONCURABLE/N/A based on verified evidence only.
9. **C7M09 SupplierClaimBinderV2** — every supplier capability claim requires a source/provenance pointer.
10. **C7M10 RequirementSupplierJoinGate** — requires complete target requirements + verified supplier profile before qualification routing.
11. **C7M11 TenderFinanceNullSafeObject** — payment/retention/bond/insurance/cash timing remain null until sourced.
12. **C7M12 IndependentPA4PacketGate** — exact packet identity + independent reviewer + blindness check.
13. **C7M13 ArtifactVersionRefreshEngine** — refresh creates a new immutable observation/version; never edits history.
14. **C7M14 DecisionUseEvidenceObjects** — PA5/E3/E4 schemas tied to real external artifacts.
15. **C7M15 CurrentAuthorityFreshnessGuard** — fresh-main state must match human-readable pointer before promotion.
16. **C7M16 AuthorityGapSelfImprovementBridge** — repeated missing-authority defects become scoped SI candidates only.

## Contracts C7C01–C7C32
- **C7C01** target workspace metadata != target full attachment pack.
- **C7C02** no current attachment inventory -> pack_complete=false.
- **C7C03** pack_complete=false -> no target-specific qualification assertion.
- **C7C04** prior tender pack != current target pack.
- **C7C05** same contracting authority != same requirements.
- **C7C06** project lineage is provenance/hypothesis, not requirement inheritance.
- **C7C07** benchmark pack may test parser behavior only.
- **C7C08** benchmark success cannot set target pack complete.
- **C7C09** every target attachment requires current-target provenance before use.
- **C7C10** revision/addendum history is append-only.
- **C7C11** missing supplier capability field remains null.
- **C7C12** supplier claim without source binding is rejected.
- **C7C13** requirement join needs both sourced requirement and sourced supplier evidence.
- **C7C14** missing evidence routes UNKNOWN, never MET.
- **C7C15** CURABLE requires a feasible action before the applicable deadline.
- **C7C16** deadline/clarification window is decision-resource evidence, not demand/WTP.
- **C7C17** MEAT label != criteria weights/price formula.
- **C7C18** unknown evaluation detail creates clarification/pack dependency, never invented score.
- **C7C19** headline estimated contract value != supplier revenue/margin/cash timing.
- **C7C20** generic regulatory/construction knowledge cannot replace exact tender requirements.
- **C7C21** bid effort hours/cost require observed team/document inputs.
- **C7C22** PA4 requires same complete packet and an independent blinded reviewer.
- **C7C23** self-review != independent PA4.
- **C7C24** real target-user interaction is required for PA5.
- **C7C25** E3 requires external behavioral cost/commitment, not compliments.
- **C7C26** E4 requires cash + binding transaction evidence.
- **C7C27** polished prose, scope similarity and large contract value cannot upgrade proof grade.
- **C7C28** WIP remains one PRIMARY + at most two PILOTs.
- **C7C29** historical artifact versions are immutable; refresh emits new version.
- **C7C30** main/head advancement after authority pointer write triggers reconciliation before promotion.
- **C7C31** repeated missing-authority failures may create an SI candidate but not global authority.
- **C7C32** missing decisive external input may legitimately produce PROTECT_NO_CHANGE/HOLD.

## Proof gates C7P01–C7P16
1. **TargetIdentityProof** — exact resource id + official current workspace.
2. **AttachmentInventoryProof** — current target document inventory, not guessed names.
3. **NonCarryoverProof** — prior/benchmark requirement leakage is rejected.
4. **BenchmarkFixtureProof** — real indexed older pack can be parsed without target promotion.
5. **RevisionProvenanceProof** — version/addendum history never overwritten.
6. **SupplierClaimProof** — each capability claim bound to evidence.
7. **RequirementJoinProof** — sourced requirement + sourced supplier capability.
8. **GapRoutingProof** — missing evidence -> UNKNOWN/HOLD.
9. **CriticalPathProof** — official public dates separated from internal/null dates.
10. **EvaluationNullSafetyProof** — MEAT without weights cannot generate a numeric score.
11. **FinanceNullSafetyProof** — estimated value cannot manufacture terms/margin/cash need.
12. **IndependentPA4Proof** — exact same packet + independent blind reviewer.
13. **PA5RealUseProof** — real user before/after decision artifact.
14. **E3BehaviorProof** — observable external behavioral commitment.
15. **E4TransactionProof** — cash + binding provenance.
16. **AuthorityFreshnessProof** — CURRENT pointer reconciled with fresh main before promotion.

## Protocols C7R01–C7R10
- **C7R01 Target Authority Recovery:** `WORKSPACE -> DOCUMENT ENDPOINT -> INVENTORY/HOLD -> HASH/VERSION -> PACK_COMPLETE`.
- **C7R02 Benchmark Isolation:** `BENCHMARK PACK -> PARSER FIXTURE -> EXPECTED INVENTORY -> NONCARRYOVER -> ZERO TARGET PROMOTION`.
- **C7R03 Tender Lineage:** `RELATED PROCEDURES -> SOURCE-BIND -> RELATION HYPOTHESIS -> NO REQUIREMENT INHERITANCE`.
- **C7R04 Supplier Evidence:** `PACKET -> CLAIMS -> SOURCE BIND -> EXPIRY -> VERIFIED/NULL`.
- **C7R05 Requirement Join:** `TARGET REQUIREMENT -> SUPPLIER EVIDENCE -> MET/UNKNOWN/CURABLE/NONCURABLE/N/A`.
- **C7R06 Critical Path:** `OFFICIAL DATES -> INTERNAL DATES/NULL -> TIME LEFT -> ACTION/HOLD`.
- **C7R07 PA4:** `FULL TARGET PACK + VERIFIED SUPPLIER -> FIRST OUTPUT -> BLIND SAME-PACKET REVIEW -> DIVERGENCE -> PA4/HOLD`.
- **C7R08 PA5/E3/E4:** `REAL USER -> BEFORE -> ARTIFACT USE -> AFTER -> BEHAVIOR -> TRANSACTION -> EVIDENCE GATE`.
- **C7R09 Refresh:** `NEW OBSERVATION -> NEW VERSION -> SOURCE/HASH -> SUPERSESSION RELATION -> READBACK`.
- **C7R10 Authority Promotion:** `FRESH MAIN -> POINTER DIFF -> CI -> DRIVE READBACK -> PROMOTE/HOLD`.

## Self-Improvement candidates
- `MISSING_AUTHORITY_IS_A_FIRST_CLASS_RESULT` — reinforced, not globally promoted.
- `BENCHMARK_MUST_NOT_FILL_TARGET_GAP` — new scoped candidate.
- `AUTHORITY_POINTER_LAG_GATE` — new scoped candidate after merged work outpaced the human-readable pointer.

No SI candidate auto-promotes from this cycle.
