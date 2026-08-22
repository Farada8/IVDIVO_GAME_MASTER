# CURRENT — GENERAL BUSINESS ENGINE

**Date:** 2026-08-22  
**Authority:** `BUSINESS_ENGINEERING_OS/GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/`  
**Status:** FOUNDER PROFILE ACTIVE / EARLY-WAVE WIP3 / P-EW01 + P-EW02 CLOSED / P-EW03 NEXT

## Restore order
1. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/00_MASTER.md`
2. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/14_FOUNDER_OPPORTUNITY_PROFILE_AND_EARLY_WAVE_GATE.md`
3. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/15_EARLY_WAVE_RADAR_2026-08-22.md`
4. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/16_EARLY_WAVE_RADAR_STATE.json`
5. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/17_AGENT_COMMERCE_READINESS_SCANNER_V0/01_MACHINE_STATE.json`
6. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/17_AGENT_COMMERCE_READINESS_SCANNER_V0/00_SPEC.md`
7. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/18_AGENT_COMMERCE_PEW02_BLIND10/03_MACHINE_STATE.json`
8. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/18_AGENT_COMMERCE_PEW02_BLIND10/02_BLIND10_RESULTS_AND_SCANNER_PATCH.md`
9. current Business evidence authority + relevant vertical state.
10. fresh GitHub/Drive reconciliation before mutating authority.

## Founder opportunity profile
- REMOTE-FIRST;
- founder physical participation zero/near-zero preferred;
- founder cash at risk EUR0–500 preferred / EUR3,000 default hard ceiling unless structurally de-risked;
- test before build/spend;
- avoid warehouse/equipment/inventory/payroll/large working-capital exposure before proof;
- maintain separate `CASHFLOW NOW` and `OPTIONALITY NEXT` portfolios;
- early-wave signal never equals guaranteed winner.

## Current WIP = 3
**PRIMARY:** `OW-01 Agentic Commerce Merchant Readiness`  
**PILOT A:** `CF-01 AI Act Article 50 Technical Transparency Pack`  
**PILOT B:** `CF-03 DPP Supplier-Data / Registry Readiness`

## P-EW01 — CLOSED
Agent Commerce Readiness Scanner v0 merged through PR #348, merge `926964d791f41fbd133a5d7e2247c1226365e15b`.

The scanner now uses real-fixture-calibrated ruleset `2026-08-22.2` and preserves `PASS / FAIL / UNKNOWN / NOT_APPLICABLE` without magic scoring.

Core laws remain:
`READINESS != PLATFORM_APPROVAL`  
`PRODUCT_FEED_READY != UCP_READY`  
`PUBLIC_PAGE_OBSERVATION != MERCHANT_DECLARATION`  
`UNKNOWN != FAIL`  
`UNKNOWN != PASS`  
`PROTOCOL_SPEC_CHANGE -> VERSIONED_RULESET`

## P-EW02 — CLOSED / PASS_TEST
P-EW02 merged through PR #353, merge `0f83a4b223b8355b7163616d2a2cec527ec228db`.

Frozen 10-real-public-merchant test:
- 10/10 evaluated without sample substitution;
- 0 generic-advice outputs;
- 0 false readiness/platform-approval promotions;
- 4/10 exposed public UCP `2026-04-08` profiles: `elverys.ie`, `allbirds.com`, `glossier.com`, `gymshark.com`;
- the four profiles advertised `mcp + embedded`, Checkout and Order;
- six merchants returned 404/410 at public UCP discovery;
- private OpenAI product-feed state remained UNKNOWN for all merchants.

Real fixtures forced two scanner corrections:
1. MCP/embedded must not be rejected by a REST-only rule.
2. Unprobed order-event implementation must remain UNKNOWN, not be collapsed into a missing-event FAIL.

Eight false-negative findings were removed across the four UCP-200 merchants. A separate profile-level gate remains: Order capability is declared but public `signing_keys` were not observed in the captured profiles. Under the pinned UCP Order spec this remains `UCP-10 FAIL`, bounded to the observed public profile and not promoted into a global merchant-compliance claim.

P-EW02 exact-head evidence:
- head `14a950014cfd3a98b6ab340d9ea82e4ef8a9ca9e`;
- CI `SUCCESS_7_OF_7`;
- Actions artifact `9472016122`;
- artifact digest `sha256:7a9a413460d1f2f154b10a15ce0746bd1d07f7df57975641288aa4e09349dcf9`;
- Drive document `1DFWMaKoQVVceCv7rRViz_Or7sxAN_pG4azV9O0iLzJE` with semantic readback PASS.

P-EW02 creates stronger engineering evidence, not market proof.

## Candidate interpretation after P-EW02
### OW-01 — Agentic Commerce Merchant Readiness — PRIMARY
KEEP as technical early-wave candidate. The blind test demonstrates real public adoption of UCP discovery on part of a heterogeneous sample and confirms that a deterministic scanner can find specific implementation/profile issues while learning from false negatives.

Still unproven:
- merchant urgency;
- buyer/budget owner;
- WTP;
- platform approval value;
- paid remediation demand;
- transaction or profitability.

Do **not** jump directly to sales/economics merely because P-EW02 passed.

### CF-01 — AI Act Article 50 Technical Transparency — PILOT
Immediate live forcing function. Its bounded technical sample artifact is now the next WIP turn.

### CF-03 — DPP Supplier-Data / Registry Readiness — PILOT
Synthetic registry-preflight remains queued after P-EW03 unless newer authority changes ordering.

## Next causal frontier
### `P-EW03` — ARTICLE 50 TECHNICAL TRANSPARENCY SAMPLE PACK
Build one internal non-legal technical transparency implementation sample grounded in current Commission/EU authority.

Required boundaries:
1. separate legal applicability/advice from technical implementation evidence;
2. map concrete technical disclosure/label/workflow controls, not generic AI-governance prose;
3. use a synthetic or internal fixture — no customer outreach required;
4. include evidence/provenance, failure states and regression checks;
5. preserve UNKNOWN where applicability or system facts are absent;
6. no compliance certification claim;
7. no WTP/demand/profit promotion.

After P-EW03, execute P-EW04 DPP synthetic supplier object/preflight unless a fresher portfolio decision changes the frontier.

## Evidence boundary
`PUBLIC_EVIDENCE_CEILING = E2+ ENGINEERING`  
`WILLINGNESS_TO_PAY = UNKNOWN`  
`CAC = UNKNOWN`  
`CONVERSION = UNKNOWN`  
`TRANSACTION = NONE`  
`PROFITABILITY = UNPROVEN`  
`EARLY_WAVE_WINNER = UNPROVEN`  
`P-EW01 = EXECUTED`  
`P-EW02 = EXECUTED / PASS_TEST`  
`P-EW03 = NEXT`

No autonomous outreach, listings, ads, purchases, speculation, spend, contracts or proof promotion are authorized by this pointer.

READBACK_MARKER: `CURRENT-GENERAL-BUSINESS-PEW02-CLOSED-PEW03-NEXT-20260822`
