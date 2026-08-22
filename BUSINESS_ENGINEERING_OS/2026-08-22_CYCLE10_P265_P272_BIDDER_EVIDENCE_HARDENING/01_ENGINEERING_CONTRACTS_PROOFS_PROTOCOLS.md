# BUSINESS CYCLE10 — P265–P272 ENGINEERING

## 8 modules
1. `C10B-M01 BidderDesignationV2Gate` — explicit resource/entity/designator/time/scope/active provenance.
2. `C10B-M02 LegalIdentityReconciler` — ranked evidence with equal-top conflict fail-closed.
3. `C10B-M03 CredentialExpiryRegistry` — current/expired/undated states remain explicit.
4. `C10B-M04 CapabilityClaimBinder` — each capability bound to evidence/source/time/context/review state.
5. `C10B-M05 TargetSpecificNegativeControl` — generic scope cannot satisfy target-specific capability.
6. `C10B-M06 ReferenceLookbackValidator` — date/scope/role/value/client evidence remain separate dimensions.
7. `C10B-M07 WorkforceCapacityEvidence` — named people, subcontractor intent, workload and speculative hiring separated.
8. `C10B-M08 PrivacyMinimizedBidderPacket` — decision-required fields + hashes, no raw sensitive values.

## 16 contracts
- `C10B-C01 TEST_FIXTURE_NEQ_ACTUAL_BIDDER`
- `C10B-C02 ACTUAL_BIDDER_REQUIRES_AUTHORIZED_DESIGNATOR_TIMESTAMP_SCOPE_ACTIVE`
- `C10B-C03 LOWER_IDENTITY_SOURCE_CANNOT_OVERRIDE_HIGHER_AUTHORITY`
- `C10B-C04 EQUAL_TOP_IDENTITY_CONFLICT_FAILS_CLOSED`
- `C10B-C05 EXPIRED_CREDENTIAL_NEQ_CURRENT_CREDENTIAL`
- `C10B-C06 UNDATED_EXPIRY_NEQ_CURRENT_CREDENTIAL`
- `C10B-C07 CAPABILITY_WITHOUT_EVIDENCE_ID_STAYS_UNKNOWN`
- `C10B-C08 EVIDENCE_BOUND_NEQ_INDEPENDENTLY_CORROBORATED`
- `C10B-C09 GENERIC_CONSTRUCTION_NEQ_TARGET_SPECIFIC_ROOFING_CAPABILITY`
- `C10B-C10 SCOPE_MATCH_NEQ_OTHER_REQUIREMENTS_MET`
- `C10B-C11 REFERENCE_DIMENSIONS_MUST_NOT_COLLAPSE_TO_ONE_SCORE`
- `C10B-C12 SELF_ISSUED_REFERENCE_NEQ_CLIENT_COMPLETION_EVIDENCE`
- `C10B-C13 SPECULATIVE_FUTURE_HIRE_NEQ_CURRENT_CAPACITY`
- `C10B-C14 SUBCONTRACTOR_INTENT_NEQ_NAMED_AVAILABLE_PERSONNEL`
- `C10B-C15 PRIVATE_RAW_EVIDENCE_NEQ_DECISION_PACKET`
- `C10B-C16 PRIVACY_MINIMIZATION_MUST_PRESERVE_HASHED_PROVENANCE`

## 8 proof gates
1. `C10B-P01 ExplicitDesignationProvenanceProof`
2. `C10B-P02 LegalIdentityAuthorityProof`
3. `C10B-P03 CredentialCurrentnessProof`
4. `C10B-P04 CapabilityEvidenceBindingProof`
5. `C10B-P05 TargetSpecificScopeProof`
6. `C10B-P06 ReferenceDimensionProof`
7. `C10B-P07 WorkforceCurrentCapacityProof`
8. `C10B-P08 PrivacyMinimizedPacketProof`

## 6 protocols
- `C10B-R01 DESIGNATION -> PROVENANCE_FIELDS -> EXPLICIT/HOLD`
- `C10B-R02 IDENTITY_EVIDENCE -> SOURCE_RANK -> CONFLICT_RECONCILIATION -> VALUE/NULL`
- `C10B-R03 CREDENTIAL -> EVIDENCE_ID + EXPIRY -> CURRENT/EXPIRED/UNKNOWN`
- `C10B-R04 CAPABILITY -> EVIDENCE_BINDING -> TARGET_SCOPE_NEGATIVE_CONTROL -> REVIEW_STATE`
- `C10B-R05 REFERENCE + WORKFORCE -> DIMENSIONAL_EVIDENCE -> NO_SCALAR_COLLAPSE`
- `C10B-R06 PRIVATE_EVIDENCE -> ALLOWED_DECISION_FIELDS + HASHED_PROVENANCE -> MINIMIZED_PACKET`

## Regression surface
`tests/test_bidder_evidence_hardening.py`: **16 deterministic canaries**, exactly 2 per P265–P272 module.

The canaries validate engineering invariants only. They are not PA4, PA5 or market evidence.

## Self-improvement candidates
- `CONTROL_PLANE_INTENT_REQUIRES_EXPLICIT_PROVENANCE`
- `CURRENTNESS_IS_A_SEPARATE_DIMENSION_FROM_DOCUMENT_PRESENCE`
- `CAPABILITY_REQUIRES_TARGET_SPECIFIC_NEGATIVE_CONTROLS`
- `REFERENCE_QUALITY_IS_DIMENSIONAL_NOT_SCALAR`
- `SPECULATIVE_CAPACITY_MUST_NOT_BECOME_CURRENT_CAPACITY`
- `PRIVACY_MINIMIZATION_MUST_PRESERVE_AUDITABLE_PROVENANCE`

No global self-improvement promotion is authorized by this Run8 alone.
