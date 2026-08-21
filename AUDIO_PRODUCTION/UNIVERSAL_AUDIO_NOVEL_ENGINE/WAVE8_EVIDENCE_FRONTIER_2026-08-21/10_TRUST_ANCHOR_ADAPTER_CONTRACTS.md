# WAVE8 — TRUST ANCHOR ADAPTER CONTRACTS

Status: ENGINEERING CONTRACT / NO NEW CENTRAL AUTHORITY

Purpose: close the gap between **record integrity** and **external evidence truth** without creating another recovery/evidence operating system inside Audio Studio.

## 1. Evidence assurance levels

Ordered, non-interchangeable:

1. `INTEGRITY_ONLY` — deterministic record/hash is internally consistent.
2. `SOURCE_BOUND` — record is bound to a named source artifact/ref/hash and a class-specific validator.
3. `CONTENT_VERIFIED` — durable source bytes/content were read back and match expected identity.
4. `EXTERNAL_ATTESTED` — an external human/provider/authority submission has a trusted capture/receipt path and content verification.
5. `TRANSACTION_RECOVERABLE` — all required transaction artifacts can be reconstructed after restart with no irreversible replay.

A higher claim may require multiple levels/classes. A lower level can never be renamed into a higher one.

## 2. ProviderAuthReceipt adapter

Required fields:

- `provider`
- `preflight_ref`
- `preflight_sha256`
- `snapshot_sha256`
- `validator_id`
- `validator_version`
- `authentication_state`
- `inventory_scope`
- `observed_at`
- `readback_status`
- `secret_persisted=false`

Laws:

- `provider_snapshot.stable_snapshot_hash` alone is `INTEGRITY_ONLY`.
- `AUTH_PROVIDER` requires a source-bound authenticated preflight receipt.
- ACCOUNT_WIDE requires source-side enumeration proof; caller request does not raise scope.
- no secret/token/API-key field may enter the receipt.

## 3. HumanAttestationReceipt adapter

Required fields:

- `review_event_sha256`
- `candidate_binding_sha256`
- `source_sha256`
- `artifact_sha256`
- `reviewer_type`
- `reviewer_ref`
- `capture_surface`
- `submission_ref`
- `submission_sha256`
- `submitted_at`
- `readback_status`
- `synthetic_fixture=false`

Laws:

- hash-chain membership proves immutable review-record lineage, not human presence.
- production `HUMAN_REVIEW` requires externally witnessed/captured submission provenance.
- synthetic fixtures must set a different evidence class/status and may never satisfy human quality/lock gates.
- machine may validate coverage but cannot produce final voice/artistic lock.

## 4. DurableArtifactReceipt adapter

Required fields per artifact:

- `artifact_kind` = REQUEST / RESPONSE / FAILURE_META / AUDIO / ALIGNMENT / SPEND_LEDGER_ENTRY / CHARGE / REVIEW / TIMELINE / OTHER_DECLARED
- `durable_ref`
- `expected_sha256`
- `observed_sha256`
- `byte_length` or canonical content length where applicable
- `readback_at`
- `validator_id`
- `status`

Statuses:

- `POINTER_PRESENT`
- `POINTER_READABLE`
- `CONTENT_HASH_VERIFIED`
- `MISMATCH`
- `MISSING`

Only `CONTENT_HASH_VERIFIED` can satisfy a content-verified recovery prerequisite.

## 5. TransactionRecoveryReceipt adapter

Input:
- Wave8 exact-N lineage/escrow;
- DurableArtifactReceipts;
- when authoritative, SI-0014 durable-write reconciliation/checkpoint lineage output.

Required output:

- exact transaction identity;
- expected artifact set;
- verified artifact set;
- missing/mismatched set;
- ambiguous irreversible operations;
- `provider_replay_allowed=false` by default;
- `recovery_status` = PASS_RECOVERABLE / RECOVER_VOLATILE_FIRST / QUARANTINE_AMBIGUOUS / FAIL_IDENTITY;
- recovery receipt hash/ref.

Law: pointer membership is not recovery proof. A paid request is never replayed merely because a local artifact is missing.

## 6. ExternalEvidenceBinding adapter

Required fields:

- `evidence_class`
- `subject`
- `source_receipt_kind`
- `source_receipt_sha256`
- `class_validator_id`
- `class_validator_version`
- `assurance_level`
- `validated_at`
- `status`

Allowed examples:

- AUTH_PROVIDER -> ProviderAuthReceipt / SOURCE_BOUND or stronger.
- LIVE_AUDIO -> DurableArtifactReceipt(AUDIO) / CONTENT_VERIFIED.
- REAL_ALIGNMENT -> DurableArtifactReceipt(ALIGNMENT) + matching live audio lineage / CONTENT_VERIFIED.
- HUMAN_REVIEW -> HumanAttestationReceipt / EXTERNAL_ATTESTED.
- DURABLE_RECOVERY -> TransactionRecoveryReceipt / TRANSACTION_RECOVERABLE.
- MEASURED_ECONOMICS -> content-verified spend/time ledger receipts.
- CROSS_PROJECT_REAL -> two project-specific evidence packages with contamination scan PASS.

## 7. Proof-manifest rule

`evidence_proof.py` remains a claim-coverage compiler, but external evidence rows are admissible only after an ExternalEvidenceBinding validator passes.

Therefore:

`manifest hash PASS` != `external truth PASS`.

Suggested future API boundary:

`compile_proof_manifest(claim, subject, validated_evidence_bindings)`

not arbitrary caller dictionaries with self-declared `verified=true`.

Do not change the runtime API until fresh-main reconciliation determines the correct Cycle5 integration surface.

## 8. Cycle5 integration

Reuse, do not duplicate:

- `EVIDENCE_CLAIM_CEILING`
- `EVIDENCE_FAMILY`
- `SHARED_FACT_CAS`
- `MUTATION_INTENT`
- `MULTI_SURFACE_TRANSACTION`
- `TRANSACTION_RECOVERY`
- `STATE_SHAPE_GUARD`
- `SELF_IMPROVEMENT_GOVERNOR`

Wave8 contributes audio-specific adapters and receipts only.

## 9. SI-0014 / Run33 integration

If/when SI-0014 is accepted as current recovery authority, Wave8 exact-N live escrow must call/adapt to its durable reconciliation/checkpoint outputs instead of defining a second independent recovery truth.

## 10. Acceptance proof set

Before implementing runtime glue, require tests demonstrating:

1. fake `verified=true` cannot create HUMAN_QUALITY/V1 proof;
2. machine-created review event cannot satisfy HUMAN_REVIEW without trusted submission receipt;
3. provider snapshot without bound authenticated preflight cannot satisfy AUTH_PROVIDER;
4. durable pointer without content readback cannot satisfy DURABLE_RECOVERY;
5. audio hash mismatch blocks recovery;
6. spend-ledger/charge mismatch quarantines irreversible state;
7. external evidence from wrong candidate binding/project is ignored/blocked;
8. complete class coverage still does not auto-authorize Founder/domain release.

## 11. Self-Improvement disposition

This contract is a **convergence interface**, not a promoted universal mechanism. Promotion requires real provider + human + restart recovery + second-project evidence and explicit Self-Improvement/Founder review.
