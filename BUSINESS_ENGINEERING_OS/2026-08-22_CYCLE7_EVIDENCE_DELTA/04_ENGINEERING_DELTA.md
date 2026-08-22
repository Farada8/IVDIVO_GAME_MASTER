# CYCLE7 EVIDENCE DELTA — ENGINEERING CONTRACTS / PROOFS / PROTOCOLS

## Reuse from merged P97–P128 authority
Historical resource `8176962`, `BenchmarkPackFixtureRouter`, `TenderLineageObject` and `NonCarryoverGuard` are already current authority. This delta does **not** create a second historical/benchmark engine.

## New bounded modules
- C7D-M01 FormationEvidenceBinder
- C7D-M02 SplitBlockerStateRouter
- C7D-M03 SupplierEvidenceDossierCompiler

They extend the existing Cycle7/P97–P128 readiness and authority-recovery runtimes.

## New contracts
- C7D-C01 `PRIVATE_PRIMARY_IDENTITY_EVIDENCE_NEQ_CAPABILITY_EVIDENCE`
- C7D-C02 `FORMATION_ACTIVITY_CODE_NEQ_CURRENT_DELIVERY_CAPABILITY`
- C7D-C03 `BLOCKER_DECOMPOSITION_SPLITS_AUTHORITY_SIDE_AND_SUPPLIER_SIDE`
- C7D-C04 `NO_DOCUMENT_PROVENANCE -> SUPPLIER_FIELD_STAYS_NULL`
- C7D-C05 `PARTIAL_IDENTITY_ONLY_NEQ_VERIFIED_SUPPLIER_PACKET`

Existing authority continues to own `PRIOR_PACK != CURRENT_REQUIREMENTS` and benchmark non-carryover.

## Proof obligations
- C7D-P01 legal identity fields are bound only to private primary formation evidence;
- C7D-P02 unsupported capability fields remain null;
- C7D-P03 authority-side and supplier-side blockers remain separately observable;
- C7D-P04 requirement join remains locked while either decisive side is incomplete;
- C7D-P05 no PA4/PA5/E3/E4 promotion from this identity delta.

## Protocol
`FRESH_CURRENT_AUTHORITY -> CLASSIFY_PRIVATE_SOURCE -> BIND_ONLY_ADMISSIBLE_IDENTITY_FIELDS -> SPLIT_AUTHORITY/SUPPLIER_BLOCKERS -> RECOMPUTE_TYPED_HOLD -> REGRESSION -> GITHUB/DRIVE_READBACK`.

## Regression
Five unique deterministic supplier-side guards pass locally 5/5:
1. formation document can verify legal name;
2. formation document cannot verify insurance/capability;
3. partial identity + missing current pack stays `HOLD_MISSING_AUTHORITY`;
4. complete current pack + incomplete supplier capability stays `HOLD_CAPABILITY_EVIDENCE`;
5. BID decision requires both current authority and supplier capability completeness.

Historical non-carryover is covered by the already-merged P97–P128 regression/runtime and is not recounted here as new proof.

## Self-Improvement disposition
New candidates only: `PRIVATE_PRIMARY_IDENTITY_EVIDENCE_NEQ_CAPABILITY_EVIDENCE` and `SPLIT_BLOCKERS_BY_EVIDENCE_OWNER`. No global Self-Improvement promotion is authorized by this single supplier-side delta.
