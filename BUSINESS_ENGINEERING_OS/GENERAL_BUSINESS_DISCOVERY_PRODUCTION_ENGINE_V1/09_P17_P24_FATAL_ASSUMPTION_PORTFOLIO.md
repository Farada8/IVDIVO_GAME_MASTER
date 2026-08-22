# GENERAL BUSINESS ENGINE — P17–P24 FATAL-ASSUMPTION PORTFOLIO

**Date:** 2026-08-22  
**Execution scope:** current WIP only: OPP-33 PRIMARY, OPP-36 PILOT, OPP-37 PILOT.  
**Evidence effect:** internal engineering / test readiness only. No outreach, buyer behavior, WTP, transaction, legal assurance, spend, contract or proof promotion is created by this block.

## Fresh source floor

The block is grounded in current first-party signals, not old opportunity prose:

- SEAI Business Energy Upgrade Scheme: companies/installers must register; the company is the contracted entity and measure-specific registered installers/certifications are required. Source: https://www.seai.ie/contractors-and-suppliers/register-with-seai/business-energy-upgrade-scheme
- European Commission Article 50 transparency guidance: published 20 July 2026; transparency duties apply from 2 August 2026. Source: https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
- Fáilte Ireland Corporate Strategy 2026–2029: digital/AI adoption, AI discoverability, bookability, conversion and measurable commercial impact are explicit priorities. Source: https://www.failteireland.ie/en/about/corporate-strategy

Source existence remains a signal only:
`OFFICIAL_SIGNAL != BUYER_DEMAND != WTP != TRANSACTION`.

---

## P17 — seven assumptions per active lane

### OPP-33 — SME Business Retrofit Grant-Ready Delivery / Partner Network

A33-1 **Buyer coordination gap exists:** an owner-managed SME without an internal project manager experiences enough grant/installer/quote/sequence friction that a single coordinator changes action or timing.  
A33-2 **Reachable eligible projects exist:** the reachable micro-market contains enough wall/roof/linked energy-upgrade cases compatible with current SEAI measures.  
A33-3 **Partner route is feasible:** suitable registered companies/installers/engineers will cooperate under a transparent coordination model with acceptable response time.  
A33-4 **Scheme boundary can be respected:** the service can remain inside the coordinator/broker role unless and until company/installer registration, tax, insurance and competence evidence support a wider role.  
A33-5 **Grant does not erase buyer friction:** immediate/available grant support still leaves a meaningful coordination job rather than a fully self-service journey.  
A33-6 **Decision value is measurable:** the coordinator pack can reduce decision time, missing steps, quote ambiguity, rework or abandoned applications.  
A33-7 **Economics may eventually work:** acquisition + coordination + partner handoff effort could fit inside a future fee/margin; this remains UNKNOWN until measured.

### OPP-36 — AI Transparency Implementation Pack for Irish SMEs

A36-1 **In-scope operational gap exists:** reachable SMEs already deploy Article-50-relevant customer-facing/generative AI and have unresolved practical transparency tasks.  
A36-2 **Vendor/free guidance is incomplete at implementation layer:** official/vendor materials do not by themselves convert into a complete business-specific inventory, disclosure, labelling and workflow implementation.  
A36-3 **Non-legal boundary is commercially usable:** a practical implementation pack can be valuable while explicitly excluding legal advice, legal interpretation and assurance.  
A36-4 **Source volatility is manageable:** the pack can be versioned and refreshed as Commission/national guidance evolves without making stale compliance claims.  
A36-5 **Qualified review is accessible:** specialist/legal review can be routed when required without making the product uneconomic. Cost remains UNKNOWN.  
A36-6 **Buyer urgency is behavioral:** affected SMEs will allocate staff/system information or request implementation rather than merely acknowledge the new rule.  
A36-7 **Outcome is measurable:** the pack can reduce unresolved transparency actions, undocumented AI uses, disclosure gaps or implementation time.

### OPP-37 — Tourism AI Discoverability & Bookability Audit + Implementation

A37-1 **AI-specific gap exists beyond ordinary SEO:** tourism operators have discoverability/bookability defects visible in AI-enabled discovery that a conventional SEO/web audit would miss or underweight.  
A37-2 **Audit is reproducible enough:** baseline visibility/bookability findings can be reproduced across a declared query set and time window rather than anecdotal prompts.  
A37-3 **Operator controls relevant surfaces:** website/content/structured data/booking path or listing changes can actually be implemented by the operator or its vendor.  
A37-4 **Changes can affect commercial path:** recommendations can plausibly reduce comparison/booking friction or increase qualified direct discovery; revenue effect remains unproven until observed.  
A37-5 **Free/agency substitution is incomplete:** Fáilte Ireland supports and ordinary SEO/web agencies do not fully substitute the specific decision artifact.  
A37-6 **Buyer behavior can be elicited:** an operator will provide analytics/access, approve a change or request implementation after seeing the audit.  
A37-7 **Delivery can be bounded:** a useful first audit can be produced without uncontrolled multi-platform monitoring or expensive API dependency.

---

## P18 — fatal ordering by information value and downside

No scalar score is authoritative. Ordering is ordinal and causal.

### OPP-33
1. A33-1 Buyer coordination gap exists — **FATAL-1**. If false, do not build coordinator business.  
2. A33-3 Partner route feasible — **FATAL-2**. If false, broker/create route cannot deliver.  
3. A33-4 Scheme boundary respected — **FATAL-3 / COMPLIANCE**.  
4. A33-2 Reachable eligible projects — **FATAL-4 / MARKET ACCESS**.  
5. A33-6 Measurable decision value — **FATAL-5 / DIFFERENTIATION**.  
6. A33-5 Grant still leaves friction — **WATCH**.  
7. A33-7 Economics — **DEFER UNTIL EFFORT OBSERVED**.

### OPP-36
1. A36-1 In-scope unresolved operational gap — **FATAL-1**.  
2. A36-2 Free/vendor substitution incomplete — **FATAL-2**.  
3. A36-3 Non-legal boundary commercially usable — **FATAL-3**.  
4. A36-6 Behavioral urgency — **FATAL-4 / DEMAND**.  
5. A36-4 Source volatility manageable — **FATAL-5 / QUALITY**.  
6. A36-7 Measurable outcome — **WATCH**.  
7. A36-5 Qualified-review economics — **DEFER UNTIL QUOTED/USED**.

### OPP-37
1. A37-1 AI-specific incremental gap beyond SEO — **FATAL-1**.  
2. A37-2 Reproducible audit — **FATAL-2**.  
3. A37-3 Operator controls surfaces — **FATAL-3**.  
4. A37-5 Free/agency substitution incomplete — **FATAL-4**.  
5. A37-6 Behavioral buyer response — **FATAL-5 / DEMAND**.  
6. A37-7 Bounded delivery — **WATCH**.  
7. A37-4 Revenue/commercial effect — **DEFER; DO NOT FABRICATE**.

---

## P19 — cheapest decisive test for FATAL-1

### TEST-33 — Grant-route decision-delta test
Input: one real SME premises/project candidate with owner permission and enough building/project facts to route the case.  
Artifact: one-page grant/measure/partner/quote/sequence decision route, explicitly distinguishing what SEAI, installer, engineer, coordinator and owner must do.  
Decisive behavior: owner supplies missing project data, requests partner/quote progression, or authorizes next project step after seeing the route.  
Current state: `READY_REQUIRES_EXPLICIT_EXTERNAL_ACTION_AUTHORIZATION`.

### TEST-36 — In-scope gap + implementation-delta test
Input: one real SME AI stack with an actual customer-facing/generative use.  
Artifact: non-legal Article-50 operational inventory + disclosure/label/workflow gap list + owner/action matrix.  
Decisive behavior: business provides system/process evidence, assigns an owner, or requests implementation/reviewer handoff.  
Current state: `READY_REQUIRES_EXPLICIT_EXTERNAL_ACTION_AUTHORIZATION`.

### TEST-37 — AI-vs-SEO differential audit
Input: one real independent tourism operator with public website/direct-booking path; implementation access is not required for baseline stage.  
Artifact A: conventional SEO/web friction checklist.  
Artifact B: declared AI-discoverability/bookability checklist using the same business facts.  
Decisive internal result: B must identify at least one material, reproducible, actionable defect not already captured by A.  
Buyer-behavior stage after internal differential: operator provides analytics/access, approves a fix, or requests implementation.  
Current state: `INTERNAL_NEGATIVE_CONTROL_READY`; external stage requires authorization.

---

## P20 — thresholds fixed before execution

### TEST-33 thresholds
- **PASS:** in a bounded sample of 3 real eligible/relevant SME cases, at least 2 produce a behavior stronger than verbal interest (project data release, site/quote progression, partner-introduction request or explicit next-step authorization) attributable to the route artifact.  
- **FAIL:** 0/3 show behavior change, or owners can complete the same next step from official/self-service material with no meaningful coordination gain.  
- **AMBIGUOUS:** 1/3 behavior change or project eligibility dominates the result.

### TEST-36 thresholds
- **PASS:** among 5 screened real SME AI stacks, at least 2 have unresolved in-scope operational gaps and at least 1 performs a concrete implementation behavior (shares system/process evidence, assigns action owner, requests pack completion or qualified review).  
- **FAIL:** no unresolved implementation gap beyond vendor/official material, or all cases are out of scope.  
- **AMBIGUOUS:** gaps exist but no behavior follows, or scope cannot be established without specialist interpretation.

### TEST-37 thresholds
- **PASS INTERNAL DIFFERENTIAL:** across 3 declared tourism-site cases, the AI-specific audit finds at least one material actionable defect per at least 2 cases that is not already present in the conventional SEO control and is reproducible on a second pass.  
- **FAIL INTERNAL DIFFERENTIAL:** no material incremental finding in 3/3, or results cannot be reproduced.  
- **PASS EXTERNAL:** after a differential pass, at least 1 operator provides analytics/access, approves a change, or requests implementation.  
- **AMBIGUOUS:** incremental findings exist but are weak, non-actionable or platform-noise sensitive.

---

## P21 — negative controls

- **CONTROL-33:** official SEAI self-navigation + direct registered-installer route with no coordinator artifact. If it produces the same decision speed/completeness, the paid coordination hypothesis weakens materially.  
- **CONTROL-36:** European Commission Article 50 guidance + existing vendor documentation only. If the SME can map and close the same operational actions without the implementation pack, differentiation fails.  
- **CONTROL-37:** ordinary SEO/web audit using the same site and time window. AI-specific claims count only when they add reproducible material action beyond that control.

---

## P22 — experiment time/cash envelope

These are experiment budgets, not business economics.

| Test | Founder-time envelope | External cash before authorization | Explicit unknowns |
|---|---:|---:|---|
| TEST-33 | 4–8 h/case for route construction + evidence capture | €0 | travel, specialist/partner time, quote/admin costs |
| TEST-36 | 3–6 h/stack for inventory + implementation matrix | €0 | qualified reviewer/legal-review cost if required |
| TEST-37 | 3–5 h/site baseline/control/differential audit | €0 | paid AI/SEO/API/tool cost if later needed |

No paid service, travel, reviewer, software purchase or outreach spend is authorized by this document.

---

## P23 — stop-loss and no-loop conditions

Global:
- `NO_NEW_BEHAVIOR_EVIDENCE -> NO_PROOF_PROMOTION`.
- Two consecutive test iterations with no new decision-changing evidence => PARK/REPLACE lane before polishing more artifacts.
- One artifact-polish iteration maximum without new evidence.
- No expansion above WIP=3.
- No paid experiment or third-party contact without explicit authorization.
- Any source/eligibility contradiction invalidates the affected test and requires source refresh.

Lane-specific:
- OPP-33: park if direct/self-service control matches coordinator route in 3 bounded cases or partner/compliance route cannot be formed.  
- OPP-36: park if 5 screened stacks yield no unresolved in-scope operational gap or free/vendor materials fully close the same actions.  
- OPP-37: park if AI-specific audit adds no reproducible material finding beyond SEO in 3 cases.

---

## P24 — next-test portfolio / WIP=3

1. **PRIMARY / OPP-33 / TEST-33** — status `READY_REQUIRES_AUTHORIZATION`; highest commercial proximity to physical delivery and active grant spending.  
2. **PILOT / OPP-36 / TEST-36** — status `READY_REQUIRES_AUTHORIZATION`; high regulatory freshness, low prototype cost, strict non-legal boundary.  
3. **PILOT / OPP-37 / TEST-37** — status `INTERNAL_NEGATIVE_CONTROL_READY`; execute internal SEO-vs-AI differential before seeking external behavior.

No lane is GO-to-market. Current engine state is `S3_FATAL_TEST_READY` for the three WIP lanes, not `S8_EXTERNAL_SIGNAL`.

## Execution accounting

- P01–P08: executed previously.  
- P17–P24: executed in this block.  
- P09–P16: not yet executed; now should be applied only to the surviving 3 WIP and their predeclared tests.  
- Next64 total: **16/64 executed; 48 remaining**.

## Result

`KEEP WIP=3 / NO PROOF PROMOTION / NO OUTREACH / NO SPEND`.

The next admissible internal block is **P09–P16 targeted to OPP-33/36/37**, using the P17–P24 tests above to constrain buyer/problem/access/evidence definitions. External execution remains gated.