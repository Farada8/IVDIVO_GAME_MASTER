# ARTICLE 50 TECHNICAL PREFLIGHT — CONTROL SPEC v0.1

**Purpose:** deterministic engineering preflight over declared facts.  
**Non-goal:** legal applicability decision, certification, conformity assessment, legal advice, buyer proof or market proof.

## Input contract
Every case is a JSON object with:
- `case_id`
- `facts.role`: `provider | deployer | provider_and_deployer | unknown`
- optional direct-interaction facts
- optional generative-content facts
- optional deployer-use facts
- optional review/editorial facts
- provenance/source metadata when available

Missing facts stay missing. The engine must not backfill them from assumptions.

## Output contract
Every result contains:
- `case_id`
- `overall`
- `findings[]`
- `legal_compliance_certified=false`
- `market_proof_promoted=false`

Allowed finding states:
- `PASS`
- `FAIL_CONTROL`
- `UNKNOWN`
- `REVIEW_REQUIRED`
- `NOT_APPLICABLE_TECHNICAL_SCOPE`
- `NOT_APPLICABLE_DECLARED_EXCEPTION`

Forbidden output claims:
- `COMPLIANT`
- `CERTIFIED`
- `LEGAL_PASS`
- `LEGAL_FAIL`
- `APPROVED`
- `BUYER_DEMAND_PROVEN`
- `WTP_PROVEN`

## Control A50-1-DISCLOSURE
Trigger candidate facts:
- `direct_human_interaction=true`
- role includes provider

Technical PASS requires:
- `interaction_disclosure_present=true`
- `interaction_disclosure_first_interaction=true`

Accessibility is evaluated separately under `A50-5-ACCESSIBILITY`.

The engine does not automatically rely on the statutory “obvious to a reasonably well-informed, observant and circumspect person” exception. If a product owner wants to rely on that path, it must be documented outside this engine and routed to human review.

## Control A50-2-MACHINE-MARK
Trigger candidate facts:
- `generates_synthetic_content=true`
- `content_type` in `audio | image | video | text`
- role includes provider

Technical PASS requires:
- final/human-exposed output facts established; and
- `machine_readable_mark=true`.

Special routing:
- `final_output=false` AND `human_exposed=false` -> `NOT_APPLICABLE_TECHNICAL_SCOPE` for the preflight fixture.
- `standard_editing_exception=true` -> `REVIEW_REQUIRED`.
- `placed_on_market_before_2026_08_02=true` AND no mark -> `REVIEW_REQUIRED` because current Commission Q&A describes a limited Article 50(2) transition to 2026-12-02 for systems placed on the market before 2026-08-02.
- provider role unknown -> `UNKNOWN`.

The engine does not prescribe one marking technology. Metadata, provenance schemes, watermarking and other mechanisms are implementation choices subject to current standards/state of the art and the voluntary Code of Practice route.

## Control A50-3-EXPOSURE-NOTICE
Trigger candidate facts:
- `emotion_recognition_or_biometric_categorisation=true`
- role includes deployer

Technical PASS requires:
- `exposure_notice_present=true`.

Purpose, data-protection and other legal obligations are outside this narrow control.

## Control A50-4-DEEPFAKE-LABEL
Trigger candidate facts:
- `deepfake=true`
- role includes deployer

Technical PASS requires:
- `visible_or_audible_label_first_exposure=true`.

Negative control:
`machine_readable_mark=true` does not satisfy this deployer-facing human-perceivable disclosure control by itself.

Artistic/creative/satirical/fictional treatment may affect manner of disclosure, but the engine does not certify that exception/manner. Such cases route to `REVIEW_REQUIRED` unless the requested human-perceivable control is explicitly supplied.

## Control A50-4-PUBLIC-INTEREST-TEXT
Trigger candidate facts:
- `content_type=text`
- `published_to_inform_public=true`
- `matter_of_public_interest=true`
- role includes deployer

Technical disclosure PASS:
- `visible_label_first_exposure=true`.

Declared exception route:
- `substantive_human_review=true`
- `editorial_control=true`
- `editorial_responsibility=true`

If all three are declared, output `NOT_APPLICABLE_DECLARED_EXCEPTION`; never emit legal compliance/certification.

If any of those is explicitly false and the label is absent -> `FAIL_CONTROL`.
If facts are incomplete -> `UNKNOWN`.

A spelling/grammar-only check is not represented as substantive review.

## Control A50-5-ACCESSIBILITY
When a first-interaction/exposure disclosure control is evaluated, accessibility must be independently recorded.

- `disclosure_accessible=true` -> `PASS`
- `disclosure_accessible=false` -> `FAIL_CONTROL`
- missing -> `UNKNOWN`

## Overall result aggregation
Priority:
1. Any `FAIL_CONTROL` -> `CONTROL_GAPS_FOUND`
2. Else any `UNKNOWN` or `REVIEW_REQUIRED` -> `REVIEW_REQUIRED`
3. Else -> `PASS_TECHNICAL_SAMPLE`

`PASS_TECHNICAL_SAMPLE` means only that the declared synthetic facts contain all controls evaluated by this narrow preflight. It is not a compliance claim.

## Regression invariants
1. A deepfake with a machine-readable mark but no visible/audible label must fail the deployer disclosure control.
2. A legacy provider marking case must not become PASS merely because the date is before 2026-08-02.
3. Missing provider/deployer role must remain UNKNOWN.
4. Public-interest text with explicit no-review/no-editorial-responsibility and no label must expose a control gap.
5. Public-interest text with all three review/editorial predicates may route to declared exception, but legal certification stays false.
6. Closed-loop non-final machine-only content must not be promoted into a human-facing marking failure in this fixture.
7. No result may contain forbidden legal or market-proof promotion language.
