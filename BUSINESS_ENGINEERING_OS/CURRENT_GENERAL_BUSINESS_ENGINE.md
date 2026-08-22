# CURRENT — GENERAL BUSINESS ENGINE

**Date:** 2026-08-22  
**Authority:** `BUSINESS_ENGINEERING_OS/GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/`  
**Status:** FOUNDER PROFILE ACTIVE / EARLY-WAVE WIP3 / P-EW01–P-EW05 INTERNAL ENGINEERING CLOSED / OW-01 WEDGE CORRECTED AFTER RULESET03 / ALL THREE M1 / BUYER EVIDENCE NEXT BUT NOT AUTHORIZED

## Restore order
1. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/00_MASTER.md`
2. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/14_FOUNDER_OPPORTUNITY_PROFILE_AND_EARLY_WAVE_GATE.md`
3. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/15_EARLY_WAVE_RADAR_2026-08-22.md`
4. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/16_EARLY_WAVE_RADAR_STATE.json`
5. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/17_AGENT_COMMERCE_READINESS_SCANNER_V0/01_MACHINE_STATE.json`
6. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/23_OW01_AGENTIC_COMMERCE_WEDGE_CORRECTION.md`
7. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/19_AI_ACT_ART50_TECHNICAL_TRANSPARENCY_PACK/03_MACHINE_STATE.json`
8. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/20_DPP_REGISTRY_PREFLIGHT/03_MACHINE_STATE.json`
9. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/20_MONETIZATION_LADDER_STATE.json`
10. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/21_PEW05_WIP3_ENGINEERING_DECISION.md`
11. `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/22_PEW05_WIP3_MACHINE_STATE.json`
12. current Business evidence authority + relevant vertical state.
13. fresh GitHub/Drive reconciliation before mutating authority.

## Founder opportunity profile
- REMOTE-FIRST;
- founder physical participation zero/near-zero preferred;
- founder cash at risk EUR0–500 preferred / EUR3,000 default hard ceiling unless structurally de-risked;
- test before build/spend;
- no warehouse/equipment/inventory/payroll/large working-capital exposure before proof;
- maintain separate `CASHFLOW NOW` and `OPTIONALITY NEXT`;
- early-wave signal never equals guaranteed winner.

## Current WIP = 3
**OW-01:** Agentic Commerce — corrected wedge: cross-protocol/custom-stack/data-quality readiness, not generic Shopify/BigCommerce UCP setup.  
**CF-01:** AI Act Article 50 Technical Transparency Pack.  
**CF-03:** DPP Supplier-Data / Registry Readiness.

These remain the bounded technical WIP set. No candidate is the market winner.

## Engineering closure
### P-EW01 — PASS
Agent Commerce Readiness Scanner merged via PR #348.

### P-EW02 — PASS_TEST AFTER RULESET03 CORRECTION
Initial blind-10 merged via PR #353. A later evidence review found that ruleset 0.2 could falsely fail public MCP/embedded merchant profiles by requiring signing keys and REST/OAuth evidence outside the actually observed path.

Corrective ruleset `2026-08-22.3` merged via PR #387, merge `75cc0f5b15b3a7199839626cea299a7f781c0d56`.

Same frozen 10 merchants, no substitution:
- 10/10 evaluated;
- 0 network errors;
- 0 generic-advice outputs;
- 0 readiness/platform false promotions;
- 6 public `/.well-known/ucp` responses = 404/410;
- 4 public UCP 2026-04-08 profiles = `elverys.ie`, `allbirds.com`, `glossier.com`, `gymshark.com`;
- those four advertise usable `mcp + embedded` bindings, checkout/order capabilities and payment-handler registries;
- those four now correctly classify `HOLD_UNRESOLVED_EVIDENCE`, not deterministic FAIL, because private feed/webhook/order conformance remains unproven.

Exact-head CI:
- scanner `32568940358` SUCCESS;
- frozen blind-10 `32568940347` SUCCESS;
- postmerge closure `32568940386` SUCCESS;
- regression canaries `20/20` PASS.

### OW-01 business mutation after P-EW02
Current first-party platform evidence weakens the original merchant-setup wedge:
- Shopify states Catalog + UCP are enabled by default for Shopify merchants and eligible products are placed into Catalog by default;
- Commerce/BigCommerce states it has fully built to UCP;
- WooCommerce has native MCP in developer preview and is moving quickly through abilities/agent-commerce integrations, while native UCP remains a moving gap.

Therefore:
`GENERIC SHOPIFY UCP SETUP = KILL AS PRIMARY WEDGE`
`GENERIC BIGCOMMERCE UCP SETUP = KILL AS PRIMARY WEDGE`
`GENERIC AI-READY NARRATIVE AUDIT = KILL`

Retained testable OW-01 wedges:
1. cross-protocol conformance/drift diagnostics;
2. custom/non-managed-stack readiness;
3. WooCommerce transition tooling only while a real current gap exists;
4. product-data / agent-discovery quality diagnostics;
5. developer regression/version-migration tooling.

This is documented in `23_OW01_AGENTIC_COMMERCE_WEDGE_CORRECTION.md`.

### P-EW03 — PASS_ENGINEERING
Article 50 Technical Transparency Pack merged via PR #367, merge `3f65b522c59a7cdc988cbae893c1d54651eab6e6`.
- 6 synthetic cases;
- 14 canaries;
- dedicated CI `32561576738` SUCCESS;
- no legal opinion/certification/compliance proof.

### P-EW04 — PASS_ENGINEERING
Controlling DPP preflight merged via PR #375, merge `8797476c45ac38bc9eb9bfbe8a3b1d9c27f1a7d7`.
- 6 synthetic cases;
- 16 canaries;
- correction/revalidation loop;
- dedicated CI `32562001036` SUCCESS;
- no live Registry action or legal applicability proof.

Superseded PR #376 is provenance only and must not count as a second P-EW04.

### P-EW05 — INTERNAL DECISION
All three routes remain:
`M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN`

No route reaches M2 because paid diagnostic transactions = 0.

## Next-real-world-test sequence — NOT market ranking
**A — OW-01 Cross-Protocol / Custom-Stack Agent Commerce Diagnostic**  
First future bounded WTP-test candidate because real public fixture discrimination is demonstrated, but the offer MUST exclude generic Shopify/BigCommerce UCP enablement.

**B — CF-01 Article 50 Technical Transparency Pack**  
Second future test candidate. Live regulatory forcing function, but delivery requires a strict legal-scope/referral boundary.

**C — CF-03 DPP Supplier-Data Readiness Diagnostic**  
Third future test candidate. Strong data/preflight workflow, but urgency/applicability depends more on product-specific acts and buyer context.

`TEST_SEQUENCE != MARKET_WINNER`

## Self-improvement laws
`ENGINEERING_PASS_ALL != MARKET_WINNER`  
`REGULATORY_FORCING_FUNCTION != BUYER_BUDGET`  
`SYNTHETIC_IMPLEMENTATION_DELTA != PAID_DEMAND`  
`REAL_FIXTURE_DISCRIMINATION != WTP`  
`PLATFORM_DEFAULTS_CAN_ERASE_A_SERVICE_WEDGE`  
`EARLY_WAVE_REAL != FIRST_SERVICE_IDEA_GOOD`  
`SCANNER_FALSE_POSITIVE != MERCHANT_DEFECT`  
`CORRECTED_ENGINEERING_EVIDENCE_CAN_MUTATE_THE_BUSINESS_MODEL`  
`DO_NOT_SELL_WHAT_THE_PLATFORM_ALREADY_AUTOMATES`  
`P-EW05_PRIORITY = NEXT_TEST_SEQUENCE != MARKET_RANKING`  
`M1 != M2`

## Next causal frontier
Do **not** create more internal features for these three solely to increase document count.

The next useful evidence is buyer evidence.

External outreach, spend or price testing remains blocked. If external testing is explicitly authorized, first write a predeclared WTP-test contract for the corrected OW-01 wedge with scope, buyer role, sample, success/fail thresholds, stop-loss, evidence capture and no-proof-overreach rules. Only then execute it.

If external testing is not authorized, return to Early-Wave Radar and maintain protocol/platform/regulatory drift monitoring. New radar candidates must still pass REMOTE-FIRST / EUR0–3000 / low-physical-load / early-wave gates before deep work.

## Evidence boundary
`WILLINGNESS_TO_PAY = UNKNOWN`  
`PRICE = NULL`  
`CAC = UNKNOWN`  
`CONVERSION = UNKNOWN`  
`TRANSACTION = NONE`  
`PROFITABILITY = UNPROVEN`  
`EARLY_WAVE_WINNER = UNPROVEN`  
`P-EW01 = PASS`  
`P-EW02 = PASS_TEST_RULESET03_CORRECTED`  
`P-EW03 = PASS_ENGINEERING`  
`P-EW04 = PASS_ENGINEERING`  
`P-EW05 = INTERNAL_DECISION_ALL_M1`  
`OW01_GENERIC_PLATFORM_UCP_SETUP = KILL_AS_PRIMARY_WEDGE`  
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

No autonomous outreach, listings, ads, purchases, speculation, spend, contracts or proof promotion are authorized by this pointer.

READBACK_MARKER: `CURRENT-GENERAL-BUSINESS-OW01-WEDGE-CORRECTED-RULESET03-NO-WTP-20260822`
