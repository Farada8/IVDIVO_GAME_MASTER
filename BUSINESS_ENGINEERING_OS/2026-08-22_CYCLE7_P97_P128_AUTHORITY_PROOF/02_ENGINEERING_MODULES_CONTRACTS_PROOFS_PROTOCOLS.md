# CYCLE7 ENGINEERING — MODULES / CONTRACTS / PROOFS / PROTOCOLS

## Modules C7M01–C7M18
1. `C7M01 OfficialPackAcquisitionGate` — distinguishes public notice from complete authoritative tender pack.
2. `C7M02 AttachmentInventoryHasher` — hashes every attachment/revision/addendum only when bytes are present.
3. `C7M03 RevisionDeltaLedger` — append-only revision/addendum provenance.
4. `C7M04 SupplierProfileProvenanceGate` — required supplier fields remain null/UNKNOWN without source.
5. `C7M05 RequirementEvidenceJoiner` — requirement → supplier value → evidence source → gap state.
6. `C7M06 BidDecisionFailClosedRouter` — HOLD/NO_BID/BID_CANDIDATE only after pack/profile gates.
7. `C7M07 TenderCriticalPathClock` — submission/clarification/site-visit/internal deadlines with missing-field visibility.
8. `C7M08 TenderFinanceNullObject` — payment/retention/bond/insurance/working-capital terms without fake defaults.
9. `C7M09 SimilarReferenceMatrix` — actual requirement categories vs sourced supplier references.
10. `C7M10 PA4BlindPacketBuilder` — same-packet hash, hidden first decision, independent reviewer envelope.
11. `C7M11 PA4DivergenceCompiler` — decision, fatal-gap and criteria divergence.
12. `C7M12 RealObservationGate` — rejects synthetic timing/error/transaction evidence.
13. `C7M13 ResidualPaidJobDetector` — free/native substitute coverage first; zero residual => HOLD/RESHAPE.
14. `C7M14 FieldHalfLifeEngine` — TTL/revalidation per artifact field.
15. `C7M15 AppendOnlyRefreshHistory` — deterministic refresh with idempotent hash history.
16. `C7M16 ProofTransitionObjects` — PA5/E3/E4 typed receipts with artifact lineage.
17. `C7M17 RepeatedDefectSIRouter` — one case = discovery; repeated evidenced defect = candidate only.
18. `C7M18 CycleClosureReconciler` — merged core + reconciled parallel delta + Drive readback + authority reconciliation.

## Contracts C7C01–C7C24
- **C7C01** `PUBLIC_NOTICE_NEQ_COMPLETE_OFFICIAL_PACK`.
- **C7C02** `NONAUTHORITATIVE_COPY_CANNOT_COMPLETE_PACK`.
- **C7C03** `NO_BYTES_NO_ATTACHMENT_HASH`.
- **C7C04** `NO_REVISION_SET_NO_SUPERSESSION_ASSERTION`.
- **C7C05** `SUPPLIER_FIELD_WITHOUT_PROVENANCE_IS_UNVERIFIED`.
- **C7C06** `MISSING_SUPPLIER_FIELD_STAYS_NULL_OR_UNKNOWN`.
- **C7C07** `NO_PACK_OR_PROFILE_NO_BID_RECOMMENDATION`.
- **C7C08** `UNKNOWN_REQUIREMENT_GAP_ROUTES_HOLD`.
- **C7C09** `NONCURABLE_VERIFIED_GAP_CAN_ROUTE_NO_BID`.
- **C7C10** `BID_CANDIDATE_NEQ_PROCUREMENT_ELIGIBILITY_PROOF`.
- **C7C11** `MISSING_DEADLINE_FIELD_IS_VISIBLE`.
- **C7C12** `MEAT_LABEL_NEQ_MEAT_WEIGHTS`.
- **C7C13** `UNKNOWN_FINANCE_TERM_NEQ_ZERO`.
- **C7C14** `REFERENCE_MATCH_REQUIRES_SOURCED_REFERENCE`.
- **C7C15** `PA4_REVIEW_REQUIRES_SAME_PACKET_HASH`.
- **C7C16** `PA4_REQUIRES_INDEPENDENCE_AND_BLINDNESS`.
- **C7C17** `SYNTHETIC_USER_NEQ_DECISION_DELTA`.
- **C7C18** `SYNTHETIC_TIME_NEQ_OBSERVED_DELIVERY_TIME`.
- **C7C19** `FREE_NATIVE_COVERAGE_REMOVES_PAID_JOB_COMPONENTS`.
- **C7C20** `DEADLINE_STATUS_CONTRADICTION_REQUIRES_REVALIDATION`.
- **C7C21** `REFRESH_PRESERVES_HISTORY`.
- **C7C22** `PA5_NEQ_E3_NEQ_E4`.
- **C7C23** `ONE_DEFECT_CASE_CANNOT_PROMOTE_SELF_IMPROVEMENT`.
- **C7C24** `STALE_PARALLEL_BRANCH_NEVER_FORCE_MERGED_OVER_NEWER_MAIN`.

## Proof gates C7P01–C7P12
1. `C7P01 PACK_AUTHORITY_PROOF` — authoritative acquisition path + complete inventory + revision coverage.
2. `C7P02 SUPPLIER_PROFILE_PROOF` — all required fields sourced and current.
3. `C7P03 REQUIREMENT_JOIN_PROOF` — every tender requirement mapped to supplier evidence state.
4. `C7P04 DECISION_ROUTING_PROOF` — no BID/NO_BID before C7P01+C7P02.
5. `C7P05 CRITICAL_PATH_PROOF` — known deadlines sourced; missing deadlines visible.
6. `C7P06 FINANCE_NULL_SAFETY_PROOF` — unknown terms remain null.
7. `C7P07 PA4_PROTOCOL_PROOF` — independent, blind, same packet hash, first decision hidden.
8. `C7P08 REAL_OBSERVATION_PROOF` — human timing/error/behavior provenance required.
9. `C7P09 SUBSTITUTE_RESIDUAL_PROOF` — paid residual job survives free/native substitute subtraction.
10. `C7P10 PROOF_TRANSITION_PROOF` — PA5/E3/E4 receipts cannot substitute for one another.
11. `C7P11 SELF_IMPROVEMENT_REPEAT_PROOF` — candidate only after repeated evidenced defect + repair.
12. `C7P12 CROSS_STORE_CLOSURE_PROOF` — GitHub merge/readback + Drive content readback + authority reconciliation.

## Protocols C7R01–C7R10
- **C7R01 Authority Restore Before Work** — fresh CURRENT + merged PR + Drive state read.
- **C7R02 Official Pack Acquisition** — authenticated/exportable route or user-provided authoritative pack; third-party mirror is discovery only.
- **C7R03 Supplier Packet Ingest** — minimize data; hash/source each field; null absent facts.
- **C7R04 Requirement Join + Gap Routing** — requirement-by-requirement, no scalar magic score.
- **C7R05 Blind PA4 Review** — freeze packet hash, hide first decision, record reviewer class/independence, compare outputs.
- **C7R06 Real DecisionDelta** — capture before/after decision from actual target user; no synthetic stand-in.
- **C7R07 Refresh + Supersession** — append snapshot history, revalidate stale/contradictory fields.
- **C7R08 Proof Transition** — PA5 real use → E3 real external behavior → E4 real transaction; each separately evidenced.
- **C7R09 Self-Improvement Canary** — candidate scoped, repeat-case threshold, no auto-promotion.
- **C7R10 Two-Surface Persistence** — GitHub branch/PR/CI + Drive mirror/readback; 409/stale state triggers re-read/reconcile.

## Test accounting
Cycle7 deterministic suite: **32/32 PASS locally**. This proves software invariants only; it does not upgrade PA3, prove a supplier is eligible, or create buyer/market evidence.