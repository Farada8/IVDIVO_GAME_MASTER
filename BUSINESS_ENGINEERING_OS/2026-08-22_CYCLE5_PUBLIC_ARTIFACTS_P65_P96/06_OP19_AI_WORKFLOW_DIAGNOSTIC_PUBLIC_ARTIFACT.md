# OP19 PUBLIC ARTIFACT — Construction-Specific AI Workflow Implementation Diagnostic
**Observed:** 2026-08-22
**Cycle5 reshape:** generic `AI adoption diagnostic` -> **construction workflow implementation diagnostic**.

## Why the reshape is necessary
The official National Enterprise Hub `Digital for Business` already provides an expert digital consultant who analyses existing digital systems, identifies gaps and recommends improvements. A generic paid "digital/AI assessment" therefore risks duplicating a public support.
Source: https://www.neh.gov.ie/business-supports/digital-for-business-

DETE's July 2026 consultation identifies construction, manufacturing and tourism as target sectors where government is studying AI adoption, opportunities, barriers, skills/capability needs and supports. This proves policy attention, not buyer demand.
Source: https://www.enterprise.gov.ie/en/consultations/targeted-sectoral-consultation-on-enterprise-adoption-of-ai.html

## Test workflow: enquiry -> estimate -> quote -> job pack -> variation log

### Baseline fields
- incoming enquiry format(s): phone/email/WhatsApp/form;
- current time from enquiry to first quote: `null until observed`;
- how scope/site notes are captured;
- where quantities/rates come from;
- duplicate re-keying between notes, quote, spreadsheet, invoice/job system;
- standard clauses/templates already used;
- how photos/drawings are stored;
- who approves final price/scope;
- error/rework examples: `null until observed`;
- sensitive/personal data involved;
- current software stack.

### Candidate workflow
1. Capture enquiry/site notes into a structured job record.
2. AI-assisted extraction proposes scope items and missing-information questions.
3. Human estimator verifies quantities, rates, exclusions and assumptions.
4. System drafts quote from approved template — no autonomous acceptance or price commitment.
5. Accepted scope produces job pack/checklist.
6. Variations are logged against original scope with human approval.
7. Outcome metrics are measured: quote-cycle time, missing-info loops, re-key events, rework/variation-document completeness.

## Public support / implementation boundary
`Grow Digital Voucher` supports eligible NEW off-the-shelf software for up to one year and lists job tracking, field-service/workflow management, BIM/3D modelling and analytics including AI among examples. The business must incur the annual subscription cost before the grant can be paid; training/configuration combined can be no more than 50% of overall project cost.
Source: https://www.neh.gov.ie/business-supports/grow-digital-voucher

`Digital for Business` can provide the upstream digital gap analysis. Therefore a differentiated service hypothesis is:
> **implementation-ready construction workflow specification + configured manual pilot + acceptance metrics**, not another generic "AI readiness report".

## Fatal unknowns before E3
- Does a construction SME consider the current quote/job-document workflow painful enough to change?
- Is existing public consultant support sufficient, making a separate diagnostic unnecessary?
- Will the SME permit use of its data/tools?
- Which integrations are technically feasible?
- How much human review is required per quote/job?
- Will anyone pay? `null / unproven`.

## Safety / compliance boundary
This artifact is operational design, not legal advice. EU AI Act, data-protection, employment, contract and procurement obligations must be handled by authoritative guidance/human specialists when material.

## Artifact result
`RESHAPED_SURVIVES_PUBLIC_TEST`: general AI diagnostic is weakly differentiated; construction-specific workflow implementation remains a plausible pilot, still capped at E2+ until external buyer behavior exists.
