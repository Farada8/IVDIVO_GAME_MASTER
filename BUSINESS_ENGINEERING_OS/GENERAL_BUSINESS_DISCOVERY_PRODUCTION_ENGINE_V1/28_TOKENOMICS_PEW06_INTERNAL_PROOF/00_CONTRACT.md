# P-EW06 — TOKENOMICS OUTCOME-ATTRIBUTION INTERNAL PROOF CONTRACT

**Date:** 2026-08-22  
**Status:** INTERNAL PROOF / NO PRODUCT BUILD / NO WIP PROMOTION / NO EXTERNAL ACTION

Parent decision:
- `26_EARLY_WAVE_TOP3_RED_TEAM_2026-08-22.md`
- `27_EARLY_WAVE_TOP3_RED_TEAM_STATE.json`

## Question
Does a measurable decision-quality gap remain between standardized AI cost/usage data and business-outcome attribution after accounting for the current public direction of FOCUS 1.5 and incumbent FinOps products?

This proof is intentionally narrower than a FinOps product.

`SYNTHETIC_PROOF != BUYER_DEMAND`
`TECHNICAL_GAP != COMMERCIAL_WEDGE`
`DECISION_ERROR_DEMONSTRATION != WTP`

## Public baseline
### FOCUS
FOCUS 1.4 is the current ratified specification. Public FOCUS 1.5 scope is expected to add native AI support including model identity and input/output token consumption plus a Price Sheet dataset. The public preview reviewed for this proof describes cost/usage normalization, not a complete business-outcome ontology.

Sources:
- https://focus.finops.org/focus-specification/
- https://www.finops.org/insights/introducing-focus-1-4/

### Incumbent products
The obvious software layer is already crowded:
- Finout: normalized AI cost monitoring, allocation, virtual tags, unit economics;
- CloudZero: AI outcome attribution and cost per customer/product/feature;
- Vantage: LLM token allocation to metadata such as team/user/application.

Sources:
- https://www.finout.io/artificial-intelligence
- https://www.cloudzero.com/
- https://www.vantage.sh/blog/llm-token-allocation-preview

Therefore this proof does **not** test whether another cost dashboard can be built.

## Allowed surviving hypothesis
`INDEPENDENT_OUTCOME_ATTRIBUTION_EVIDENCE_QUALITY_QA`

Question: can a deterministic checker expose when apparently normalized AI cost data is still not decision-ready because cost cannot be traced reproducibly to the work unit and business outcome used for margin/pricing/go-no-go decisions?

## Synthetic fixture design
No real provider prices are used. Provider labels and costs are synthetic.

Required fields:
- record_id
- provider
- model
- cost_eur
- work_unit_id
- outcome_id
- observed_segment
- fixture_ground_truth_segment

The fixture deliberately contains missing outcome attribution while retaining enough hidden ground truth to test whether the omission flips a business decision.

## Metrics
1. `work_unit_cost_coverage_pct` = cost with work_unit_id / total cost.
2. `outcome_cost_coverage_pct` = cost with outcome_id / total cost.
3. `unattributed_outcome_cost_eur` = total cost without outcome_id.
4. `decision_error_detected` = whether an operating decision flips after restoring fixture ground-truth attribution.

Decision-ready threshold for this proof only:
`outcome_cost_coverage_pct >= 95%`

This is a test threshold, not an industry standard.

## Predeclared expected fixture result
- total synthetic AI cost = EUR 100
- work-unit coverage = 95%
- outcome coverage = 78%
- unattributed outcome cost = EUR 22
- observed BETA AI cost = EUR 13
- ground-truth BETA AI cost = EUR 35
- BETA revenue = EUR 100
- BETA non-AI variable cost = EUR 80
- reported margin before restored attribution = +EUR 7
- corrected margin after restored attribution = -EUR 15
- decision flips from positive-margin to negative-margin

## Commercial overlap test
After the numerical proof, classify the surviving wedge against the current baseline:

### If the only value is:
- provider normalization;
- token tracking;
- cost allocation;
- unit economics dashboard;
- FOCUS conformance;
then `KILL_AS_COMMODITY_OR_INCUMBENT_COVERED`.

### Only retain as M1 hypothesis if the value is specifically:
- independent completeness/traceability QA across exported cost + business-outcome mappings;
- decision-error detection caused by missing attribution;
- evidence-quality regression independent of the system that generated the mapping.

Even then:
`COMMERCIAL_DIFFERENTIATION = UNPROVEN`

## Pass/hold/kill semantics
- `PASS_TECHNICAL_GAP_ONLY`: numerical decision error is demonstrated and the gap is not identical to FOCUS cost/usage fields.
- `HOLD_COMMERCIAL`: incumbents already solve much of the adjacent problem and no buyer/WTP evidence exists for an independent QA layer.
- `KILL`: no distinct technical gap remains after overlap review.

P-EW06 may not promote WIP, buyer demand, WTP, price, transaction or profitability.

## Proof boundary
`PUBLIC_EVIDENCE_CEILING = E2_PLUS`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`
