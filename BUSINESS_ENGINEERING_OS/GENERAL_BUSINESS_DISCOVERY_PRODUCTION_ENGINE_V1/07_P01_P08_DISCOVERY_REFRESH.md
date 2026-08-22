# GENERAL BUSINESS ENGINE — P01–P08 DISCOVERY & AUTHORITY REFRESH

**Date:** 2026-08-22  
**Scope:** fresh non-procurement discovery pass.  
**Evidence effect:** public/current signal only; no WTP, transaction, buyer intent or unit economics created.

## P01 — authority reconciliation
Read before discovery:
- `CURRENT_GENERAL_BUSINESS_ENGINE.md`;
- General Business Engine master/spec/machine state;
- existing Cycle4 32-opportunity register;
- current Business evidence/vertical state;
- fresh `main` and Drive authority.

Existing 32 opportunities are retained as history/current candidates. Procurement remains a vertical rather than the top-level default.

## P02 — registry freshness rule
The old 32-opportunity register is not deleted. Time-sensitive signals not revalidated in this pass become `REVALIDATION_REQUIRED`, not assumed current.

Revalidated/adjacent existing lanes from current first-party sources:
- OPP-17 energy advisory — SEAI business-energy ecosystem remains active;
- OPP-19 roof/insulation retrofit — SEAI Business Energy Upgrades building-fabric measures remain active;
- OPP-22 accessibility — Fáilte Ireland current accessible/inclusive tourism supports confirm a live need;
- OPP-27 Grow Digital — current LEO Grow Digital support remains live;
- OPP-28 Digital for Business — current LEO support remains live;
- OPP-29 SME AI/digital implementation — current LEO digital supports + Irish AI Act implementation confirm the general need, but generic diagnostic remains weak because funded/free diagnostics exist.

All other time-sensitive Cycle4 signals require fresh revalidation before they can drive a new decision.

## P03 — ten fresh non-procurement signals

### SIG-GEN-01 — SEAI Business Energy Upgrade Scheme company/installer registration
First-party signal: SEAI is actively registering companies/installers for business energy upgrades. A company must be registered before the client requests grant payment; registered installers must satisfy measure-specific requirements.
Derived opportunity: **OPP-33 — SME Business Retrofit Grant-Ready Delivery / Partner Network**.
Route: `BROKER_TO_CREATE` until registration/certification/insurance/tax prerequisites are proven.
Buyer: Irish SMEs/business premises seeking grant-supported building upgrades.
Why now: live scheme + immediate grant pathway + company/installer registration route.
Fatal assumption: reachable businesses will value a single coordinator enough to pay beyond underlying contractor margin.
Cheapest decisive test: build one grant-ready project route from a real SME building and compare buyer decision/time saved vs direct self-navigation.
Gate: `DISCOVER_PRIMARY_CANDIDATE`.

### SIG-GEN-02 — SEAI Technical Assistance Grant
First-party signal: up to 50% of a building-specific design package, up to €25,000; package must be signed by a chartered building-services/mechanical/electrical engineer.
Derived opportunity: **OPP-34 — SME Energy Design Coordination + Chartered-Engineer Broker**.
Route: `BROKER`.
Buyer: SMEs wanting a decarbonisation/upgrade plan before capital works.
Why now: live grant materially lowers buyer cost of expert design.
Fatal assumption: buyers/engineers need an intermediary rather than finding each other directly.
Cheapest decisive test: one project brief + three qualified engineer routes + documented decision-time delta.
Gate: `HOLD_SPECIALIST_PARTNER_REQUIRED`.

### SIG-GEN-03 — LEO Energy Efficiency Grant
First-party signal: current LEO support can fund 75% of eligible energy-efficiency equipment/technology costs from €750 to €10,000 following a qualifying Green for Business/SEAI audit route.
Derived opportunity: **OPP-35 — Green-to-Grant Implementation Pack for Micro Businesses**.
Route: `CREATE_BROKER`.
Buyer: micro/small businesses that already have a qualifying report/audit but have not converted recommendations into purchases/installation.
Why now: live funding creates a concrete implementation trigger.
Fatal assumption: the post-report implementation gap is large enough to pay for coordination.
Cheapest decisive test: take one real Green/SEAI recommendation list and produce a purchase/quote/grant execution pack; measure decision delta.
Gate: `DISCOVER_MERGE_TEST_WITH_OPP33`.

### SIG-GEN-04 — EU AI Act Article 50 transparency obligations
First-party signal: Article 50 transparency duties apply from 2 August 2026; Commission guidelines were published 20 July 2026. Ireland's AI Office is operational and coordinates national implementation.
Derived opportunity: **OPP-36 — AI Transparency Implementation Pack for Irish SMEs**.
Route: `CREATE_WITH_LEGAL_BOUNDARY`.
Buyer: SMEs using customer-facing AI/chatbots, synthetic media or AI-generated public-interest content.
Why now: obligations have just become applicable.
Fatal assumption: SMEs will pay for practical implementation rather than rely on vendors/free guidance.
Cheapest decisive test: build a non-legal inventory/disclosure/label/workflow pack for one real SME AI stack and test decision usefulness with a qualified reviewer/business user.
Gate: `DISCOVER_PILOT_CANDIDATE`.

### SIG-GEN-05 — Fáilte Ireland 2026–2029: AI-enabled discoverability and bookability
First-party signal: Fáilte Ireland's current strategy explicitly targets digital/AI capability, AI-driven discovery, easier comparison/booking and upgraded booking/payment/CRM/inventory systems.
Derived opportunity: **OPP-37 — Tourism AI Discoverability & Bookability Audit + Implementation**.
Route: `CREATE`.
Buyer: independent hotels, B&Bs, attractions and activity operators.
Why now: sector strategy explicitly identifies AI discoverability/bookability as a competitiveness issue.
Fatal assumption: owners see measurable booking/revenue/admin value beyond normal SEO/web agencies.
Cheapest decisive test: one property/attraction audit comparing AI-search visibility, booking friction and implementation actions before/after.
Gate: `DISCOVER_PILOT_CANDIDATE`.

### SIG-GEN-06 — Fáilte Ireland 2026–2029: labour cost, workflow and cost-to-serve pressure
First-party signal: the strategy identifies rising labour costs, operational inefficiency and inconsistent service standards; it calls for workflow design, process efficiency, lean operations and AI-assisted optimisation.
Derived opportunity: **OPP-38 — Hospitality Workflow & Cost-to-Serve Optimisation Sprint**.
Route: `CREATE`.
Buyer: owner-managed hotels, restaurants, pubs and attractions.
Why now: structural labour/productivity constraint is explicitly recognised by the sector authority.
Fatal assumption: a small operator can realise enough measurable savings in 2–4 workflows to justify the fee.
Cheapest decisive test: map one real workflow (booking/check-in/housekeeping/F&B/admin) and quantify manual touches/time/rework before proposing automation.
Gate: `WATCH_TO_TEST`.

### SIG-GEN-07 — Fáilte Ireland Access for Success / accessible tourism
First-party signal: current programme provides accessibility audits, training and Access Welcome Guides; current resources target hotels/B&Bs, food & beverage and venues.
Derived disposition: **MERGE INTO OPP-22 — Tourism Accessibility Implementation Vertical** rather than create a duplicate opportunity.
Route: `MERGE`.
Why now: current July/2026 resources and active programme.
Fatal assumption: there is paid implementation work beyond free Fáilte audit/training.
Cheapest decisive test: compare audit findings to actual implementation backlog at one venue.
Gate: `MERGE_EXISTING`.

### SIG-GEN-08 — LEO Market Explorer Grant
First-party signal: qualifying 1–50 employee firms can receive up to €10,000 / 50% for market research, in-market consultancy, trade fairs and overseas market exploration; applications must precede project expenditure.
Derived opportunity: **OPP-39 — Export Market Evidence & Entry Pack**.
Route: `CREATE_BROKER`.
Buyer: small manufacturing/eligible internationally traded service firms entering a new geography/market.
Why now: current grant lowers the cost of structured market exploration.
Fatal assumption: firms will pay for evidence-driven market research/entry preparation and the service fits eligible consultancy rules.
Cheapest decisive test: one narrow country/customer-segment research pack with explicit go/no-go criteria, reviewed by one export-ready SME.
Gate: `WATCH_TO_TEST`.

### SIG-GEN-09 — LEO tariff-response supports
First-party signal: multiple LEOs currently advertise supports for small businesses affected by recent US import-tariff increases.
Derived opportunity: **OPP-40 — US Tariff Exposure & Market Diversification Decision Pack**.
Route: `CREATE_BROKER`.
Buyer: Irish small exporters/manufacturers exposed to US tariff changes.
Why now: active tariff shock/support response.
Fatal assumption: enough affected firms need paid analysis beyond LEO/export-advisor support.
Cheapest decisive test: one product/SKU exposure map + alternative-market decision tree using public tariff/market data, then compare with export-advisor feedback.
Gate: `WATCH_HIGH_FREE_SUPPORT_SUBSTITUTION_RISK`.

### SIG-GEN-10 — Makers Academy / creative-brand scale signal
First-party signal: LEO + Kilkenny Design launched a national Makers Academy specifically to move makers/designers from creative talent to commercially scalable brands; 25 finalists were announced in July 2026. The inaugural application window is closed, so this is a demand signal, not a live grant opportunity.
Derived opportunity: **OPP-41 — Creative Maker Retail Scale Pack**.
Route: `CREATE`.
Buyer: Irish makers/designers with validated products but weak retail/commercial systems.
Why now: strong institutional signal that commercialisation is a recognised bottleneck, but no current application window.
Fatal assumption: makers will pay privately for commercialisation support outside funded programmes.
Cheapest decisive test: one product-line retail readiness pack (pricing, margin, packaging, wholesale terms, photography/listing, retail pitch) and decision-delta review.
Gate: `WATCH_SIGNAL_STRONG_URGENCY_LOW`.

## P04 — deduplication
- SIG-GEN-07 merges into existing OPP-22.
- OPP-35 is adjacent to OPP-19/OPP-33 and must be tested as a post-audit implementation submodule rather than allowed to become a duplicate company.
- OPP-36 is distinct from generic OPP-29 because the trigger is Article 50 operational transparency and the product excludes legal assurance.
- OPP-37/38 are verticalised tourism offers, distinct from generic OPP-28/29 only if they demonstrate tourism-specific value and workflow evidence.
- OPP-39/40 are distinct export decision products but face strong substitution from free/public LEO supports.
- OPP-41 is a commercialization vertical, not another arts-funding application service.

## P05 — top-five authority/freshness passports

| Candidate | Authority | Freshness | Strong source signal | Main boundary |
|---|---|---|---|---|
| OPP-33 Business retrofit delivery/partner network | SEAI first-party | current | active BEUS company/installer registration + business upgrade measures | registration, tax, insurance, measure-specific installer competence |
| OPP-36 AI transparency implementation | EU Commission + Irish DETE/AI Office | July–Aug 2026 | Article 50 applicable 2 Aug 2026 | operational support only; legal interpretation/review separate |
| OPP-37 Tourism AI discoverability/bookability | Fáilte Ireland first-party | strategy published Aug 2026 | explicit AI discovery/bookability/digital operating-system priority | must beat normal SEO/web agency alternative |
| OPP-38 Hospitality workflow optimisation | Fáilte Ireland first-party | strategy published Aug 2026 | explicit labour-cost/process/lean/AI productivity problem | measurable savings must be demonstrated |
| OPP-39 Export market evidence pack | LEO first-party | current | up to €10k / 50% Market Explorer Grant | eligibility/export expertise/free-support substitution |

## P06 — micro-markets
- OPP-33: owner-managed Irish SMEs with commercial premises needing wall/roof fabric or linked energy upgrades and no internal project manager.
- OPP-36: Irish SMEs already deploying customer-facing generative/interactive AI, not firms merely experimenting internally.
- OPP-37: independent tourism operators with direct booking paths and weak AI-search discoverability/bookability.
- OPP-38: hospitality businesses with 10–100+ repetitive admin/service workflow hours per week and visible labour pressure.
- OPP-39: 1–50 employee eligible exporters with an identified new market decision pending, not firms seeking generic marketing.

## P07 — why-now / expiry
- OPP-33: live scheme; registration and active grant-funded upgrade demand. Revalidate scheme requirements before each client case.
- OPP-36: Article 50 already applicable since 2 Aug 2026; urgency high. Guidance/regulatory interpretation can evolve, so source refresh is mandatory.
- OPP-37/38: Fáilte Ireland 2026–2029 strategy is fresh and durable; urgency is commercial rather than deadline-based.
- OPP-39: current LEO grant; applicant must apply before incurring project spend. Revalidate eligibility/budget before use.
- OPP-40: tariff shock is time-sensitive; refresh actual tariffs and supports before any client-facing claim.
- OPP-41: inaugural programme intake closed; signal remains useful but urgency low.

## P08 — decision vector / candidate portfolio
No scalar total score is authoritative.

### Candidate PRIMARY
**OPP-33 — SME Business Retrofit Grant-Ready Delivery / Partner Network**
Reason: direct connection to active capital spending, current first-party grant infrastructure and a concrete route from coordination to installation margin. Fatal prerequisites remain registration/certification/tax/insurance/partner capacity; therefore this is a PRIMARY **discovery/test candidate**, not a proven business.

### Candidate PILOT 1
**OPP-36 — AI Transparency Implementation Pack**
Reason: very fresh regulatory trigger and low-cost prototype path. Must remain non-legal implementation support with legal/regulatory review boundaries.

### Candidate PILOT 2
**OPP-37 — Tourism AI Discoverability & Bookability**
Reason: fresh sector strategy, clear buyer population and a testable before/after artifact. Must prove incremental value over ordinary web/SEO agencies.

### WATCH / HOLD
- OPP-38 WATCH_TO_TEST — attractive but savings must be measured on a real workflow.
- OPP-39 WATCH_TO_TEST — grant exists, but free-support substitution risk is material.
- OPP-40 WATCH — tariff support market may be crowded/free.
- OPP-41 WATCH — market problem credible, immediate trigger weak.
- OPP-34 HOLD — chartered/specialist partner required.
- OPP-35 MERGE/TEST under energy-upgrade lane.
- OPP-22 accessibility vertical MERGE, not new WIP.

## Evidence boundary
For every candidate:
`WILLINGNESS_TO_PAY = UNKNOWN`
`UNIT_ECONOMICS = UNKNOWN`
`TRANSACTION_EVIDENCE = NONE`
`REPEATABILITY = UNPROVEN`

Government/agency support is a market/problem signal, not evidence that buyers will pay this engine/operator.

## Next causal frontier
Do **not** execute P09–P16 across all candidates. First run P17–P24-style fatal-assumption logic on the 3-candidate WIP and identify the cheapest decision-changing test for each. If a candidate fails its fatal, replace it from WATCH rather than increasing WIP.
