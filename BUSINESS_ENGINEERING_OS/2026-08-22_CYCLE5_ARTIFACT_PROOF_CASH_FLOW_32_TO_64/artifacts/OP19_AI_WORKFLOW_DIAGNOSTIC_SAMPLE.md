# OP19 SAMPLE — AI WORKFLOW DIAGNOSTIC FOR A SMALL CONSTRUCTION BUSINESS

**Evidence class:** PUBLIC SUPPORT + WORKFLOW ARTIFACT / E2+ ceiling  
**Workflow tested:** lead → site notes → estimate → quote → client approval → job pack → variation record → invoice.  
**Purpose:** identify one bounded AI/digital pilot with an explicit human-control boundary. No claim that a real contractor wants or will pay for this service.

## 1. Friction map

| Stage | Typical manual friction hypothesis | Automation candidate | AI necessary? |
|---|---|---|---|
| Lead intake | WhatsApp/email/site notes fragmented | structured intake form + CRM/job record | Mostly NO |
| Estimate | repeated copy/paste, missing quantities | template/checklist, historical item library | AI only for assistive extraction, not autonomous pricing |
| Quote | inconsistent wording/version | document assembly from approved estimate | Optional AI drafting with human review |
| Client approval | unclear latest version | e-sign/versioned approval | NO |
| Job pack | quote, scope, photos, safety/admin docs scattered | automatic pack assembly | Mostly NO |
| Variations | verbal changes not captured | structured variation log + approval | NO |
| Invoice | duplicate data entry | approved-job-data → invoice draft | NO/low-risk assistive |

## 2. Recommended first pilot
**Do not begin with “AI estimates the job.”** Begin with a bounded **Quote + Job-Pack Assistant**:
- structured source fields are authoritative;
- AI may extract/summarise notes and draft scope language;
- price/quantity/tax/client identity remain human-approved structured values;
- every generated document shows source revision and approval state;
- no autonomous sending, purchasing or contractual commitment.

## 3. Current Irish support path
Ireland's 2026 Digital and AI Strategy describes phased adoption: awareness → experiment/pilot → planning/capacity → implementation. `AI – Good for Business` explicitly promotes gradual adoption and “start small and scale.” Public supports include Digital for Business, Grow Digital/Grow Digital Voucher, and EDIHs. Current Grow Digital Voucher information includes workflow/job-tracking, e-signature, accounting and analytics/AI software among eligible examples subject to programme rules.

## 4. Regulatory boundary
EU AI Act Article 50 transparency obligations apply from 2 August 2026 for relevant transparency-risk systems. This artifact does not decide whether a particular contractor workflow is legally in scope. A deployed customer/worker-facing use must be classified against current law/guidance before release.

## 5. 14-day bounded pilot specification
- Days 1–2: map current quote/job-pack flow and baseline error/rework counts.
- Days 3–5: create structured intake + quote template.
- Days 6–8: add AI assist only for note extraction/scope drafting.
- Days 9–11: run historical jobs, no customer sending.
- Days 12–14: compare cycle time, omissions, revision errors; human decides GO/HOLD.

**Success metric:** fewer missing fields/revisions and lower admin time without pricing/control errors.  
**Kill condition:** AI introduces untraceable values, hidden scope changes, or admin time rises.

## Canonical sources
- https://www.gov.ie/en/department-of-enterprise-tourism-and-employment/policy-information/digital-and-ai-strategy/
- https://www.gov.ie/en/department-of-enterprise-tourism-and-employment/press-releases/ai-good-for-business-helping-irish-businesses-take-the-first-steps-with-ai/
- https://www.neh.gov.ie/business-supports/digital-for-business-
- https://www.neh.gov.ie/business-supports/grow-digital-voucher
- https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems

## Artifact-test verdict
`BOUNDED_PILOT_SPEC_PASS / FREE_SUPPORT_OVERLAP_IDENTIFIED / DIFFERENTIATED_VALUE_AND_WTP_HOLD / E2+ ONLY`
