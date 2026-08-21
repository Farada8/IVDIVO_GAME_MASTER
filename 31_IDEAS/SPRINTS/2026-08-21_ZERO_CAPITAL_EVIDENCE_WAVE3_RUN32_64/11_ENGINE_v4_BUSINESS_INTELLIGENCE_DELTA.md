# ZERO-CAPITAL OPPORTUNITY ENGINE v4 — BUSINESS INTELLIGENCE DELTA

## Status
WORKING ENGINEERING DELTA / PUBLIC-EVIDENCE CEILING E2+ / NO OUTREACH

## Mission
Upgrade the existing Zero-Capital / Regulatory Shock engine with the best production-proven architectural mechanisms observed across 2026 business AI systems.

## New modules

### M17 BusinessOntology
Canonical objects:
`MARKET`, `REGULATION`, `COMPANY`, `BUYER_ROLE`, `PRODUCT`, `PROCESS`, `CAPABILITY`, `PAIN`, `TRIGGER`, `CAPITAL_FLOW`, `CONTRACT`, `ACTION`, `PROOF_EVENT`, `OUTCOME`.
Relationships are first-class and versioned.

### M18 SignalFusionBus
Ingests heterogeneous signals and preserves provenance instead of flattening them into one score.
Signal families:
- law/regulation;
- budget/procurement;
- funding/M&A;
- hiring;
- patents/research;
- infrastructure;
- company product/site change;
- prices/supply chain;
- demand/search/traffic where available;
- public customer/competitor evidence.

### M19 EntityResolutionGraph
Resolves multiple references to the same company/actor/sector/project. No scoring until entity confidence clears threshold.

### M20 EnrichmentWaterfall
For a missing field, query source classes in priority order; preserve source disagreement. Never replace unknown with guessed data.

### M21 WhyNowEngine
Every opportunity must answer:
1. What changed?
2. Why now rather than six months ago?
3. Who is forced/incentivized to act?
4. What is the deadline or economic trigger?
5. What budget/capital flow can pay?
6. What evidence would falsify urgency?

### M22 OpportunityGraph
Links signal -> affected actor -> pain -> mandatory/valuable action -> zero-cash wedge -> buyer -> channel -> proof route -> scale route.

### M23 EvidenceDecomposedScore
No opaque 0-100 score. Output contains components:
`signal_strength`, `source_quality`, `urgency`, `buyer_specificity`, `zero_cash_deliverability`, `competition_pressure`, `liability`, `channel_leverage`, `repeatability`, `proof_ceiling`.
Every component cites evidence and uncertainty.

### M24 WatchlistGrid
Run the same evidence questions across N markets/companies/regulations so comparisons are consistent rather than narrative.

### M25 ContinuousSignalMonitor
Tracks selected opportunity theses and creates deltas only when evidence changes materially.
No duplicate briefs when nothing changed.

### M26 InteractionEvidenceGraph
When real human/customer evidence is eventually authorized, objections, questions, requests, losses and payments become structured events. Model simulations never populate this graph.

### M27 ObjectionTaxonomy
Classifies external objections into demand, timing, trust, authority, budget, scope, price, channel, legal, delivery, incumbent, no-pain.
Repairs only the observed category.

### M28 DeterministicSpine
Deterministic state machine controls authority, gates, writes, money and irreversible actions.
LLM nodes are allowed for interpretation/synthesis but cannot bypass gates.

### M29 JudgementNode
Bounded agentic reasoning node with explicit input schema, allowed tools, output schema, uncertainty and escalation condition.

### M30 OutcomeMeter
Tracks real outputs separately from activity:
- opportunity found != buyer interest;
- buyer interest != payment;
- payment != repeatability;
- repeatability != profitable unit economics;
- vendor adoption != our proof.

### M31 BusinessProcessGraph
Maps how the target company currently performs the job, where friction occurs, what information crosses roles, and where our wedge integrates without demanding wholesale transformation.

### M32 DecisionLineageLedger
For every KEEP/MUTATE/KILL decision retain:
`input evidence -> interpretation -> competing hypothesis -> gate -> decision -> expected observable consequence -> later actual consequence`.

## New engineering contracts

### C17 PUBLIC_EVIDENCE_CEILING
Public/web/vendor evidence may raise an opportunity to E2+ only. It cannot create E3/E4.

### C18 ONTOLOGY_BEFORE_AGENT_SWARM
No multi-agent expansion until canonical business objects, relationships, authority and state transitions are defined.

### C19 SIGNAL_PROVENANCE
Every signal keeps source, observation date, effective/event date, extraction confidence and contradiction status.

### C20 WHY_NOW_REQUIRED
No opportunity becomes PRIMARY without a specific trigger and falsifiable urgency thesis.

### C21 SCORE_DECOMPOSABLE
Every ranking must expose its components. Black-box single-number ranking is forbidden as authority.

### C22 UNKNOWN_IS_NULL
Unknown economics, buyer intent, human minutes, costs or conversion remain null, never 0 and never estimated as fact.

### C23 WORKFLOW_OVER_FREE_AUTONOMY
Deterministic workflow owns irreversible operations; agent reasoning is inserted only where ambiguity adds value.

### C24 ACTION_OUTCOME_SEPARATION
Activity is logged separately from outcome and cannot promote proof status.

### C25 NO_VENDOR_CASE_LAUNDERING
Competitor/customer success claims can justify mechanism investigation but never prove our market/ROI.

### C26 OUTCOME_BASED_PRODUCTIZATION
When repeated proof exists, prefer pricing/packaging linked to delivered unit of work or measurable outcome where commercially/legal feasible.

### C27 OBSERVABILITY_REQUIRED
Any automated agent must expose source set, decision/result, error state, cost/spend where measurable and rollback/version identity.

### C28 HUMAN_HANDOFF
If risk, confidence or policy boundary is exceeded, route to human/specialist rather than fabricate certainty.

## Protocol stack v4

`AUTHORITY_REBASE`
-> `SIGNAL_INGEST`
-> `ENTITY_RESOLUTION`
-> `BUSINESS_ONTOLOGY_BIND`
-> `SOURCE_TRIANGULATION`
-> `WHY_NOW`
-> `OPPORTUNITY_GRAPH`
-> `ZERO_CASH_GATE`
-> `LIABILITY_GATE`
-> `EVIDENCE_DECOMPOSED_RANK`
-> `WATCHLIST/DELTA`
-> `KEEP | MUTATE | KILL`
-> external proof only when explicitly authorized
-> `OUTCOME`
-> `DECISION_LINEAGE`
-> `SELF_IMPROVEMENT_DELTA`

## Self-improvement rules
1. Do not add a module because another vendor has it; add only when it closes an identified system gap.
2. A new module starts WORKING, not CURRENT.
3. Require regression against at least one positive case, negative case, stale-evidence case and contradiction case.
4. Prefer merging with an existing mechanism over creating a parallel engine.
5. No architectural cycle should continue when a higher-information external proof gate is available and authorized.

## Immediate effect on current Wave3 research
- AI Governance Handoff: DEMOTED from PRIMARY; keep as regulatory-data subcase.
- Tender radar: ARCHIVE/RESEARCH PROVENANCE; reusable Signal/Opportunity extraction only.
- Product Compliance Change Pack: KEEP as research PRIMARY because it has specific regulatory/event triggers and data/process work that can be delivered without inventory.
- DPP/Compliance-as-Data: KEEP as strategic platform thesis, but proof ceiling remains E2+.
- Broad 'AI agency': KILL as undifferentiated category.

## Current proof state
`PUBLIC_RESEARCH = ACTIVE`
`OUTREACH = OFF`
`HUMAN_SIGNAL = NOT_RUN`
`PAYMENT_PROOF = NOT_RUN`
`MARKET_PROOF = NOT_RUN`
`FOUNDER_NEW_CASH_SPENT = €0`
