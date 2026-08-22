# P-EW03 — ARTICLE 50 TECHNICAL TRANSPARENCY SAMPLE PACK

**Date:** 2026-08-22  
**Status:** INTERNAL ENGINEERING SAMPLE / NON-LEGAL / NO COMPLIANCE CERTIFICATION / NO MARKET-PROOF PROMOTION  
**Parent:** `CF-01 AI Act Article 50 Technical Transparency Pack`

## Purpose
Turn current EU Article 50 transparency authority into one bounded technical preflight that can be executed on declared system/content facts without silently making legal applicability, compliance, buyer-demand, WTP or transaction claims.

The engineering question is:

> Given a provenance-labelled system/content fixture, can we deterministically identify missing transparency controls while preserving `UNKNOWN`, exception-review states and role uncertainty?

## Current authority surfaces
Primary/current official sources used for this engineering interpretation:

1. Regulation (EU) 2024/1689, Article 50 — current consolidated EUR-Lex text.
   - https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en
2. European Commission — Guidelines on transparency obligations for providers and deployers of AI systems, published 2026-07-20; Article 50 applies from 2026-08-02.
   - https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
3. European Commission — Article 50 transparency Q&A, updated July 2026.
   - https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
4. European Commission — Code of Practice on Transparency of AI-generated Content, final June 2026.
   - https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
5. Commission opinion / AI Board adequacy assessment of that voluntary Code.
   - https://digital-strategy.ec.europa.eu/en/library/commission-opinion-assessment-code-practice-transparency-ai-generated-content

## Authority interpretation boundary
The Code of Practice is a voluntary implementation route for Article 50(2), (4) and (5). Commission/AI Board adequacy does not make signature or implementation conclusive evidence of compliance.

The preflight therefore never emits `COMPLIANT`, `LEGAL_PASS`, `CERTIFIED`, `APPROVED`, or equivalent.

## Technical controls represented
- `A50-1-DISCLOSURE`: direct AI-human interaction disclosure from the start of first interaction when provider-side facts declare this case.
- `A50-2-MACHINE-MARK`: machine-readable marking/detectability of provider-side generative audio/image/video/text outputs when relevant declared facts are present.
- `A50-3-EXPOSURE-NOTICE`: deployer notice for emotion-recognition / biometric-categorisation exposure.
- `A50-4-DEEPFAKE-LABEL`: human-perceivable disclosure for declared deepfake exposure; machine-readable marking alone is not treated as sufficient deployer disclosure.
- `A50-4-PUBLIC-INTEREST-TEXT`: disclosure route versus declared substantive-human-review + editorial-control + editorial-responsibility exception route.
- `A50-5-ACCESSIBILITY`: cross-cutting accessibility/readability timing control when disclosure applies.

## State model
`PASS` — the synthetic fixture explicitly contains the technical control.

`FAIL_CONTROL` — the fixture declares facts activating a technical control, but that control is absent.

`UNKNOWN` — role/system/content/exposure facts are insufficient; absence is not converted into FAIL.

`REVIEW_REQUIRED` — a transitional rule or exception is asserted and requires human legal/applicability review.

`NOT_APPLICABLE_TECHNICAL_SCOPE` — the synthetic case deliberately models a Commission-described non-final/closed-loop/machine-only output class.

`NOT_APPLICABLE_DECLARED_EXCEPTION` — factual predicates of an exception path are declared. This records routing only and is not a legal conclusion.

## Negative controls
`MACHINE_READABLE_MARK != HUMAN_PERCEIVABLE_DISCLOSURE`

`ARTICLE50_TECHNICAL_PREFLIGHT != LEGAL_COMPLIANCE_CERTIFICATION`

`CODE_OF_PRACTICE_SIGNING != CONCLUSIVE_COMPLIANCE_PROOF`

`PUBLIC_GUIDANCE != CASE_SPECIFIC_LEGAL_ADVICE`

`DECLARED_EXCEPTION != VERIFIED_EXCEPTION`

`UNKNOWN != FAIL`

`UNKNOWN != PASS`

`SUPERFICIAL_REVIEW != SUBSTANTIVE_HUMAN_REVIEW`

`CONTENT_MARKING != PLATFORM_APPROVAL`

`TECHNICAL_SAMPLE != BUYER_DEMAND`

`TECHNICAL_SAMPLE != WTP`

`TECHNICAL_SAMPLE != TRANSACTION`

## Proof boundary
`PUBLIC_EVIDENCE_CEILING = E2+ ENGINEERING`

`CUSTOMER_OUTREACH = 0`

`BUYER_DEMAND = UNPROVEN`

`WTP = UNKNOWN`

`TRANSACTION = NONE`

`PROFITABILITY = UNPROVEN`

`LEGAL_COMPLIANCE_CERTIFIED = FALSE`

## Drive persistence
Folder: `15N2xm8iEYe5MBg7Jp3W1qazgLAdkD9Qp`  
Document: `1zG-MB0LZ64hOkh4NXOQgP6phWo0p-uFcZ6pJjaXqo60`

Expected semantic marker:
`ARTICLE50-P-EW03-TECHNICAL-PREFLIGHT-NONLEGAL-NO-COMPLIANCE-CERT-NO-MARKET-PROOF`
