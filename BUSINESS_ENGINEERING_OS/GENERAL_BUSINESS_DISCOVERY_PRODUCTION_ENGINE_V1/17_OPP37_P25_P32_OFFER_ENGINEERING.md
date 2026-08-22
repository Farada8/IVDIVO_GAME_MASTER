# OPP-37 — P25–P32 OFFER / ARTIFACT / PRICING ENGINEERING

**Date:** 2026-08-22  
**Scope:** internal engineering only for OPP-37 Tourism AI Discoverability & Bookability.  
**Dependency:** merged TEST-37 internal differential PASS 2/3.  
**Evidence ceiling:** no buyer behavior, WTP, transaction, conversion uplift, unit economics or repeatability proof.

## Market-control finding before P25

The broad label “AI SEO audit” is already highly substitutable:
- free automated SEO/AI-readiness checks exist;
- QueryLantern offers a free page audit and a written up-to-5-page audit for €149;
- BeaconSites advertises an Irish AI Visibility Audit from €299 and explicitly competes with free automated reports;
- other providers bundle ongoing SEO/AEO/GEO services.

Therefore the current offer MUST NOT claim differentiation merely from “AI”, “GEO”, a score, a PDF, or prompt testing.

Mutation:
`GENERIC_AI_SEO_AUDIT -> FIRST_PARTY_FACT_CONSISTENCY_ANSWERABILITY_DIRECT_BOOKING_DECISION_PACK`.

The product is a decision artifact: identify answer-critical first-party contradictions/ambiguities, nominate a canonical source of truth, assign ownership/effective date, map affected direct-booking surfaces, and provide a bounded synchronization plan plus verification queries.

## P25 — measurable value hypothesis

### Hypothesis
For a tourism operator that already has a usable public site/direct-booking path, a fact-consistency + answerability decision pack can reduce ambiguity and rework before the operator or web/booking vendor edits multiple surfaces.

### What can be measured internally now
- `contradictions_found`
- `ambiguous_canonical_facts`
- `affected_first_party_surfaces`
- `facts_resolved_to_one_canonical_rule`
- `specific_decisions_created`
- `generic_recommendations_rejected`
- `pre_vs_post_answer_consistency_test_cases`
- `estimated_implementation_steps` (count only, not invented labour cost)

### What remains NULL until real evidence
- booking uplift;
- direct-revenue uplift;
- avoided OTA commission;
- conversion change;
- buyer time saved;
- WTP;
- delivery cost;
- contribution margin.

Value hypothesis is therefore `DECISION_CLARITY_AND_REWORK_REDUCTION`, not “more bookings”.

## P26 — minimum decision-valuable artifact

Product name (working): **First-Party Fact Consistency & Answerability Decision Pack**.

Minimum one-site artifact:
1. **Ordinary-control summary** — what is merely normal SEO/web hygiene and must not be sold as special AI work.
2. **Canonical Fact Ledger** — fact ID, question, all current first-party statements, source URL/location, conflict/ambiguity class, proposed canonical wording/rule, owner, effective date, confidence/evidence state.
3. **Direct-booking surface map** — homepage/product/FAQ/terms/booking/contact/confirmation surfaces affected by each fact.
4. **Prioritized repair queue** — maximum 10 material issues; every row source-linked and actionable.
5. **Negative findings** — explicitly record where no AI-specific issue is proven.
6. **Answerability verification set** — bounded factual questions before/after repair; no promise that any external AI engine will cite the business.
7. **Implementation handoff checklist** — page/surface, change, owner, dependency, verification method.

Artifact acceptance requires a decision, not a score. An output containing only percentages/scores/generic recommendations is rejected.

## P27 — scope, exclusions and acceptance criteria

### Included
- public first-party website pages;
- direct-booking/contact surfaces publicly reachable without account access;
- first-party fact contradictions/ambiguities relevant to a customer decision;
- ordinary-web negative control;
- canonicalization proposal and synchronization plan;
- bounded verification question set.

### Optional later, only if explicitly supplied/authorized
- private analytics;
- booking-engine admin data;
- CRM/enquiry logs;
- customer-supplied policies or operating documents;
- implementation access.

### Excluded by default
- ranking guarantee;
- ChatGPT/Google/Perplexity citation guarantee;
- revenue or conversion forecast;
- legal/compliance opinion;
- OTA redesign or representation;
- reputation management;
- paid ads;
- implementation in third-party accounts;
- outreach to vendors/customers;
- continuous monitoring unless separately evidenced/scoped.

### Acceptance criteria
A pack is acceptable only if:
- every counted finding has first-party provenance;
- ordinary SEO vs incremental answerability is explicitly separated;
- conflict/ambiguity is reproducible;
- every material finding has a concrete repair;
- UNKNOWN remains UNKNOWN;
- negative findings are allowed;
- no revenue/WTP claim is inferred;
- no external action occurs without authorization.

## P28 — three offer architectures

### A. Productized service — preferred next test
**One-Site Fact Consistency & Answerability Decision Pack**.
Fixed bounded scope, human-reviewed evidence ledger, max 10 material issues, repair queue, verification set, short findings walkthrough if externally authorized later.

Why first: cheapest manual way to test whether the artifact changes a real operator decision before software is built.

### B. Implementation coordinator / broker — conditional
Audit plus coordination of website/booking vendor synchronization, change acceptance and re-check.

Why conditional: potentially more valuable but introduces vendor interaction, delivery liability and labour. Requires explicit authorization, contract scope and observed buyer behavior first.

### C. Tool / SaaS — HOLD before repeat evidence
Scheduled crawler/registry that compares answer-critical facts across first-party surfaces, versions canonical facts and flags drift.

Why HOLD: a tool can be built, but software before repeated manual demand would be solution-first. Minimum prerequisite: repeated manual use showing the same fact-governance problem and willingness to allocate resources.

## P29 — pricing hypothesis, not WTP

### Fresh market anchors
- free automated AI/SEO scans: €0;
- QueryLantern written review up to 5 pages: €149;
- BeaconSites Irish AI Visibility Audit: from €299.

These anchors prove available alternatives, not our own WTP.

### Initial hypothesis corridor for a small bounded one-site pack
- **€249 ex VAT** — low hypothesis / commodity-pressure control;
- **€349 ex VAT** — central hypothesis for human-reviewed decision pack;
- **€490 ex VAT** — upper hypothesis only if scope includes larger multi-surface ledger and decision walkthrough.

`PRICE_HYPOTHESIS != WTP`.

No minimum viable price is yet authorized because actual delivery hours/cost are unmeasured. No profitability claim is allowed. P33–P40 must measure delivery economics before a price floor can be accepted.

Implementation coordination is not bundled into these prices; later fixed/hourly pricing must follow observed effort and scope.

## P30 — objection / evidence-response matrix

### “I can paste my site into ChatGPT/free audit.”
Valid objection. Response only if we can show a reproducible cross-page contradiction ledger, first-party provenance, canonical source decision and synchronization map. Never claim proprietary AI magic.

### “My SEO/web agency already does this.”
Ask whether their process already reconciles answer-critical facts across first-party pages/terms/booking surfaces with provenance and canonical ownership. If yes at acceptable cost, substitution is real and this offer may be unnecessary.

### “There is no proof this gets me bookings.”
Agree. Do not claim booking uplift. Current test supports only decision/fact consistency. Revenue claims stay NULL until measured.

### “Fáilte Ireland/free tools already help with digital performance.”
Treat them as incumbents/substitutes. The offer survives only if the decision artifact closes a narrower operational gap faster or more rigorously; otherwise PARK.

### “My booking engine/vendor owns the information.”
Map ownership. Public-only audit can identify mismatch; any private-system change requires access authorization and separate implementation scope.

### “AI changes too fast.”
Avoid unstable hacks. Focus on channel-stable source governance: one factual rule, provenance, owner, effective date and synchronized first-party surfaces.

### “Why pay €349 when a €149 audit exists?”
There is no proven answer yet. The hypothesis is that a contradiction/canonicalization decision artifact is more decision-useful than a broad score/report. P31 tests this internally; external WTP remains untested.

## P31 — internal decision-change test before external use

Test uses the same three TEST-37 sites. No contact or account access.

### Pre-artifact decision baseline
Generic action: “run SEO/AI-readiness improvements”. This is rejected as non-decision-specific.

### Post-artifact decisions
**Pallas:** do not recommend a generic AI/SEO package first. Specific decision: reconcile advanced/family kart speed and equipment statements across homepage, karting, terms and booking-facing surfaces; establish one canonical spec owner/effective date; re-check factual answers.

**Clissmann:** do not recommend generic AI optimization first. Specific decision: resolve whether glamping `16:00` is a fixed check-in time or whether `14:00–18:00` is the authoritative arrival window; synchronize FAQ, product and booking-confirmation wording; re-check factual answers.

**Townsend House:** do not sell an AI-specific remediation finding from current evidence. Route current observed issues to conventional content/index hygiene unless a later bounded test proves a distinct answerability defect.

### Internal threshold
PASS if:
- >=2/3 cases move from a generic recommendation to a specific source-grounded decision; AND
- >=1 case is allowed to remain a negative finding rather than being forced into an AI upsell.

Observed internal result:
- specific decision: Pallas YES;
- specific decision: Clissmann YES;
- protected negative control: Townsend YES.

`P31_INTERNAL_DECISION_CHANGE = PASS_2_OF_3_PLUS_1_NEGATIVE_CONTROL`.

This proves artifact decision discrimination internally only. It is NOT buyer value evidence.

## P32 — commodity/free-substitution red team

### Attacks
1. Free scan substitutes for generic technical checks — TRUE.
2. €149 broad written audit creates price pressure — TRUE.
3. €299 Irish AI visibility audit creates direct category competition — TRUE.
4. Competent SEO agency can manually inspect contradictions — TRUE.
5. General-purpose LLM can help compare copied page text — TRUE.
6. Method itself is not defensible IP merely because it is rigorous — TRUE.
7. No proven buyer urgency or WTP — TRUE.
8. No measured delivery cost or margin — TRUE.
9. No evidence recurring monitoring is needed — TRUE.

### Surviving narrow hypothesis
What survives is not a generic audit or proprietary algorithm. It is a bounded service hypothesis based on **decision-grade fact governance**:
- cross-page first-party provenance;
- contradiction/ambiguity register;
- canonical fact decision;
- owner/effective date;
- affected direct-booking surfaces;
- negative-control discipline;
- verification set after repair.

### P32 disposition
`MUTATE_AND_TEST`, not PASS-to-market.

- Productized manual service: TESTABLE INTERNALLY / external buyer test later requires authorization.
- Broker/coordinator: HOLD until behavior and delivery scope exist.
- SaaS/tool: HOLD until repeated manual need exists.
- Generic AI SEO audit: KILL as the differentiated core offer.

## P25–P32 result

P25–P32 are engineering-complete for OPP-37.

Old-WIP Next64 accounting after this block:
- executed: **32/64**;
- remaining: **32**;
- executed ranges: P01–P32;
- state: `S5_OFFER_TESTABLE_INTERNAL_ONLY`;
- buyer behavior: FALSE;
- WTP: NULL;
- transaction: NULL;
- unit economics: NULL;
- profitability: UNKNOWN;
- external action: NOT AUTHORIZED.

Next admissible internal block: **P33–P40 economics and cash**, with null-safe models and one internal manual-delivery timing sample. External sales/use remains gated.

## Market source ledger
- BeaconSites, “Best AI Visibility Audit Service Ireland 2026” — https://beaconsites.ie/articles/best-ai-visibility-audit-service-ireland-2026/ — from €299; describes free automated reports as substitutes at the low end.
- QueryLantern — https://querylantern.com/ — free page audit; written up-to-5-page full audit €149.
- seo.irish — https://www.seo.irish/free-seo-ai-visibility-check.html — free SEO & AI visibility check.
- Ranked AI — https://www.ranked.ai/free-tools/ai-seo-audit — free AI SEO readiness audit.
- BeaconSites services — https://beaconsites.ie/services/ — AI Visibility Audit from €299 and ongoing AEO/visibility services.

SOURCE_SIGNAL != MARKET_PROOF. COMPETITOR_PRICE != OUR_WTP.

READBACK_MARKER: `GENERAL-BUSINESS-OPP37-P25-P32-OFFER-ENGINEERING-32OF64-NO-MARKET-PROOF`
