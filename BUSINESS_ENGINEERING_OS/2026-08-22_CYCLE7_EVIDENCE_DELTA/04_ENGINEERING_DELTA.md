# CYCLE7 EVIDENCE DELTA — ENGINEERING CONTRACTS / PROOFS / PROTOCOLS

## Reuse from merged P97–P128 authority
Historical resource `8176962`, `BenchmarkPackFixtureRouter`, `TenderLineageObject` and `NonCarryoverGuard` are already current authority. This delta does **not** create a second historical/benchmark engine.

## Bounded modules
- C7D-M01 FormationEvidenceBinder
- C7D-M02 SplitBlockerStateRouter
- C7D-M03 SupplierEvidenceDossierCompiler
- C7D-M04 VersionedFormationFieldResolver
- C7D-M05 RegistryPresenceStatusGuard

They extend the existing Cycle7/P97–P128 readiness and authority-recovery runtimes.

## Contracts
- C7D-C01 `PRIVATE_PRIMARY_IDENTITY_EVIDENCE_NEQ_CAPABILITY_EVIDENCE`
- C7D-C02 `FORMATION_ACTIVITY_CODE_NEQ_CURRENT_DELIVERY_CAPABILITY`
- C7D-C03 `BLOCKER_DECOMPOSITION_SPLITS_AUTHORITY_SIDE_AND_SUPPLIER_SIDE`
- C7D-C04 `NO_DOCUMENT_PROVENANCE -> SUPPLIER_FIELD_STAYS_NULL`
- C7D-C05 `PARTIAL_IDENTITY_ONLY_NEQ_VERIFIED_SUPPLIER_PACKET`
- C7D-C06 `FORMATION_METADATA_IS_VERSIONED`
- C7D-C07 `CONFLICTING_FORMATION_VERSIONS_REQUIRE_FINAL_AUTHORITY`
- C7D-C08 `LATEST_RECOVERED_FORM_NEQ_FINAL_REGISTRY_RECORD`
- C7D-C09 `PUBLIC_REGISTRY_PRESENCE_NEQ_ACTIVE_STATUS`

Existing authority continues to own `PRIOR_PACK != CURRENT_REQUIREMENTS` and benchmark non-carryover.

## Proof obligations
- C7D-P01 legal identity fields are bound only to private primary formation evidence;
- C7D-P02 unsupported capability fields remain null;
- C7D-P03 authority-side and supplier-side blockers remain separately observable;
- C7D-P04 requirement join remains locked while either decisive side is incomplete;
- C7D-P05 no PA4/PA5/E3/E4 promotion from identity/status evidence;
- C7D-P06 conflicting A1 versions cannot collapse into one current registry value;
- C7D-P07 public registry/index presence cannot silently become ACTIVE status.

## Protocol
`FRESH_CURRENT_AUTHORITY -> CLASSIFY_SOURCE -> PRESERVE_FORMATION_VERSION_ID -> BIND_IDENTITY_ONLY -> RESOLVE_CONFLICT_OR_NULL -> SEPARATE_REGISTRY_PRESENCE_FROM_STATUS -> SPLIT_AUTHORITY/SUPPLIER_BLOCKERS -> RECOMPUTE_TYPED_HOLD -> REGRESSION -> GITHUB/DRIVE_READBACK`.

## Regression
Eight deterministic supplier/legal-status guards:
1. formation document can verify legal name;
2. formation document cannot verify insurance/capability;
3. conflicting formation versions require final authority and produce null current value;
4. one recovered formation version is still not current registry proof;
5. public registry presence does not imply ACTIVE status;
6. partial identity + missing current pack stays `HOLD_MISSING_AUTHORITY`;
7. complete current pack + incomplete supplier capability stays `HOLD_CAPABILITY_EVIDENCE`;
8. BID decision requires both current authority and supplier capability completeness.

Historical non-carryover is covered by the already-merged P97–P128 regression/runtime and is not recounted here as new proof.

## Self-Improvement disposition
New scoped candidates: `PRIVATE_PRIMARY_IDENTITY_EVIDENCE_NEQ_CAPABILITY_EVIDENCE`, `SPLIT_BLOCKERS_BY_EVIDENCE_OWNER`, `FORMATION_METADATA_IS_VERSIONED`, and `PUBLIC_REGISTRY_PRESENCE_NEQ_ACTIVE_STATUS`. No global Self-Improvement promotion is authorized by this supplier evidence slice.
