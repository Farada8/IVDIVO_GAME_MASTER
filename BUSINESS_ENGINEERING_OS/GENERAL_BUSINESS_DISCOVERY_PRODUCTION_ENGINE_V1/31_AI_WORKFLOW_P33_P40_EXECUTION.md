# MONEY MECHANISMS — P33–P40 AI/NO-CODE WORKFLOW IMPLEMENTATION

Date: 2026-08-22
Status: INTERNAL_R&D_NON_WIP_CANDIDATE / NO_PRODUCTION_TOUCH / NO_WTP

## P33 — Select one repeated SME workflow
Selected workflow: **trade inquiry -> scope prequalification -> quote-prep** for a small painting/maintenance contractor.

Problem boundary:
- incoming enquiries are often incomplete;
- access/preparation uncertainty makes instant quoting unsafe;
- structural/specialist work must not be silently treated as ordinary painting;
- repeated copying between messages/forms/notes/quote drafts creates double handling.

This is deliberately narrower than a CRM/job-management suite.

**P33: PASS_ENGINEERING.**

## P34 — Baseline steps/minutes/errors/handoffs
Synthetic/manual SOP for internal comparison only:
1. read inquiry;
2. copy customer/property details;
3. identify property/surface;
4. inspect condition statement;
5. inspect access statement;
6. request/inspect photos;
7. confirm authority/consent;
8. decide more-info vs survey vs specialist;
9. create survey checklist;
10. create quote-prep checklist;
11. record follow-up state.

Error opportunities: omitted access, omitted condition, structural work accepted as cosmetic, consent/authority omission, missing-photo ambiguity, premature price/quote drafting.

Modeled baseline: 12 minutes for a complete ordinary inquiry, plus 2 minutes per missing field and additional ambiguity allowances. **This is a synthetic model, not observed operator time.**

**P34: PASS_ENGINEERING_SYNTHETIC_BASELINE_ONLY.**

## P35 — Manual/AI/no-code prototype
Implemented deterministic prequalification prototype:
- structured intake schema;
- required-field detector;
- routes: NEED_MORE_INFO / SITE_SURVEY_REQUIRED / OUT_OF_SCOPE_SPECIALIST / HOLD_OUTSIDE_AREA / HOLD_CONSENT_OR_AUTHORITY / PREQUALIFIED_FOR_SURVEY_QUOTE_PREP;
- quote-prep checklist generated only for admissible cases;
- no automatic binding price.

The prototype is deterministic/rule-based and can later be placed behind Forms/Sheets/no-code or an LLM extraction layer. LLM extraction is optional; decision rules remain testable.

**P35: PASS_ENGINEERING.**

## P36 — DecisionDelta on synthetic cases
Regression corpus covers ordinary complete inquiry, missing surface, missing photos, unknown/difficult access, heavy failure, structural issue, specialist access, outside area, consent failure and authority failure.

Expected behavior is deterministic. Critical negative controls:
- structural/specialist case never receives quote-prep checklist;
- uncertain access/prep forces survey rather than automatic quote.

Modeled assisted review time = 3 minutes base + missing-field/survey adjustments. Modeled time delta is positive on the standard case, but **REAL_TIME_SAVING remains UNPROVEN** until paired observations exist on >=20 real inquiries.

**P36: PASS_ENGINEERING_SYNTHETIC_DECISION_DELTA / REAL_TIME_DELTA_UNPROVEN.**

## P37 — Privacy/security/compliance boundary
Minimum data principle:
- collect only fields needed for scope qualification/contact;
- do not collect unnecessary identity documents;
- property photos can contain faces, addresses, vehicles or other personal data;
- access to intake/photo stores must be restricted;
- retention/deletion policy required before production;
- no customer data may be used to train external models without an explicit lawful/contractual basis;
- no automated legal, structural or safety certification;
- structural/access uncertainty routes to human/specialist review;
- consent to be contacted is separate from permission for unrelated marketing.

**P37: PASS_ENGINEERING_BOUNDARY.**

## P38 — Productized implementation package
Working product specification: **Trade Inquiry Prequalification Pack**.

Deliverables:
1. intake-field map;
2. configured qualification rules;
3. missing-information templates;
4. survey-required rules;
5. out-of-scope/specialist rules;
6. quote-prep checklist;
7. handoff into existing CRM/Sheets/job software;
8. 10–20 regression cases;
9. operator handover guide;
10. privacy/security configuration checklist.

Explicit exclusions:
- no replacement of accounting/job-management suite;
- no structural/safety judgment;
- no automatic binding quotation where material uncertainty exists;
- no paid ads/lead generation included by default.

PRICE = NULL. WTP = NULL.

**P38: PASS_ENGINEERING_SPEC_ONLY.**

## P39 — Free/native/grant-funded alternatives
### DIY
Google Forms can collect structured responses and write them to Sheets. This is a real low-cost substitute for intake + basic workflow.

### SaaS-native
Tradify already supports enquiries, customer records, quotes, price lists, jobs, invoices and automated follow-up. A generic “trade CRM/quoting app” would therefore be weak differentiation.

### Public support
LEO Digital for Business provides eligible small firms access to digital consultants to analyse systems, optimise/integrate solutions and guide implementation; it explicitly targets paperwork reduction, CRM integration and process streamlining.

### Implication
The candidate survives only if it produces a measurable configuration/integration/qualification delta beyond DIY and native SaaS. It must not sell “AI” as the value proposition.

**P39: PASS_ENGINEERING / GENERIC_CRM_POSITIONING_REJECTED.**

## P40 — One-off vs recurring contract
### One-off implementation is plausible only after buyer evidence
Configuration, intake design, rule setup, integration, regression pack and handover.

### Recurring maintenance is NOT assumed
A retainer would need observed recurring work such as:
- frequent rule/service-area changes;
- price-list/template maintenance;
- monthly false-route review;
- intake-quality monitoring;
- integration break/failure handling;
- new service package onboarding.

`ONE_IMPLEMENTATION != RECURRING_REVENUE`.

Software/SaaS is not justified from one implementation.

**P40: PASS_ENGINEERING / RECURRING_UNPROVEN.**

## Run result
P33–P40 = **8/8 PASS_ENGINEERING**, with explicit evidence ceilings.

What was proven:
- narrow workflow can be represented deterministically;
- synthetic cases distinguish ordinary, ambiguous, specialist and invalid routes;
- quote-prep is blocked on critical uncertainty;
- differentiation must be configuration/integration/decision quality, not a generic CRM claim.

What was NOT proven:
- real operator minutes saved;
- buyer pain severity;
- WTP;
- price;
- conversion;
- transaction;
- recurring demand;
- profitability.

## Next evidence gate
Before promotion into active WIP:
1. obtain >=20 real historical/current inquiry cases with privacy-safe handling;
2. observe manual operator time/route on the same cases;
3. run assisted workflow and compare route completeness/error/time;
4. identify an actual buyer role;
5. only after explicit authorization run a bounded WTP test.

Until then: **R&D_CANDIDATE_NOT_ACTIVE_WIP**.

READBACK_MARKER: `MONEY-MECHANISMS-P33-P40-TRADE-PREQUAL-RD-8OF8-NO-WTP-20260822`
