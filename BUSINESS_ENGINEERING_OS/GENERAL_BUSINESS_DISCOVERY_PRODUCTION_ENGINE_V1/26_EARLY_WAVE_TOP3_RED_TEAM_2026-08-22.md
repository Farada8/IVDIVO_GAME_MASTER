# EARLY-WAVE TOP-3 RED TEAM

**Date:** 2026-08-22  
**Status:** INTERNAL RED TEAM / PUBLIC-EVIDENCE ONLY / NO WIP PROMOTION / NO EXTERNAL ACTION

Parent radar:
`25_EARLY_WAVE_RADAR_DELTA02_2026-08-22.md`

## Question
Of the three highest-ranked early-wave candidates, which still has a non-obvious, low-capital bottleneck after accounting for incumbent products, likely platform commoditization, buyer role, specialist burden and standards absorption?

This pass does **not** ask whether the wave is real. It asks whether there is any credible wedge left for us.

`REAL_WAVE != GOOD_ENTRY_WEDGE`
`BUYER_PAIN != BUYER_WILL_PAY_US`
`INCUMBENT_PRODUCT != IMPOSSIBLE_ENTRY`
`OPEN_STANDARD != INDEPENDENT_SERVICE_MARKET`
`INTERNAL_PROOF != WIP_PROMOTION`

---

# 1. AI TOKENOMICS / COST-TO-VALUE

## Red-Team verdict
**RANK AFTER RED TEAM: #1**  
**Route:** `ADVANCE_TO_SMALLEST_INTERNAL_PROOF_ONLY`  
**Revised strategic score:** `80/100`  
**WIP:** `RADAR_ONLY`

The wave is real and the pain is already commercial, but the obvious product is crowded.

### Public evidence
- Linux Foundation launched the Tokenomics Foundation on 4 Aug 2026 with 30 initial members to define vendor-neutral AI cost, cost-to-serve and ROI frameworks and add token-cost telemetry to FOCUS.
- FOCUS 1.4 was ratified 4 Jun 2026. FOCUS 1.5 work is already scoped to add AI model identity, input/output token consumption and a standardized Price Sheet.
- Finout already markets normalized AI cost monitoring, allocation and governance across OpenAI, Anthropic, Bedrock, Vertex AI, Cursor and cloud providers.
- CloudZero already markets AI outcome attribution, cost-per-customer/product/feature and a financial control plane for AI economics.
- Vantage already has LLM Token Allocation and multi-provider AI cost reporting.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-launches-the-tokenomics-foundation-to-define-the-economics-and-roi-of-ai-value
- https://focus.finops.org/
- https://www.finops.org/insights/introducing-focus-1-4/
- https://www.finout.io/artificial-intelligence
- https://www.cloudzero.com/
- https://www.vantage.sh/blog/llm-token-allocation-preview

### Generic wedges killed
`GENERIC_AI_COST_DASHBOARD = KILL`
`GENERIC_TOKEN_SPEND_TRACKER = KILL`
`GENERIC_MULTI_PROVIDER_COST_AGGREGATOR = KILL`
`FOCUS_SCHEMA_VALIDATOR_AS_PRIMARY_WEDGE = KILL_OR_STRONGLY_DISCOUNT`

Reason: incumbent FinOps platforms already do the first three, while the FOCUS project itself is building conformance/validator infrastructure.

### Surviving narrow wedge
`AI_COST_TO_BUSINESS_OUTCOME_EVIDENCE_QUALITY = KEEP_TESTABLE`

A bounded independent layer may still exist between raw cost normalization and the operating decision:
- Was usage actually attributable to a task/customer/work unit?
- Is cost-to-serve measured consistently across providers/models/tool calls/cache/reasoning?
- Are business-outcome mappings complete enough to support a pricing/margin/go-no-go decision?
- Does the organization have a reproducible evidence trail from model usage -> normalized cost -> work unit -> business outcome?

This is **not** another SaaS dashboard thesis. It is a data-quality / decision-evidence thesis.

### Identifiable buyer roles
- FinOps practitioner / FinOps lead;
- AI platform / platform engineering lead;
- engineering leader owning model spend;
- FP&A / finance partner for AI products;
- CFO/controller only at the decision layer, not as primary technical operator.

### Smallest reusable internal proof
Build no platform. Create one deterministic proof harness over public/synthetic cost records:
1. normalize provider/model usage into one ledger;
2. preserve input/output/cache/tool-call distinctions where available;
3. attach work-unit/business-outcome IDs;
4. calculate cost-to-serve and missing-attribution rate;
5. emit PASS/HOLD/FAIL for decision-evidence completeness;
6. compare against what FOCUS 1.4/1.5 will standardize so we do not duplicate the standard.

### Fatal test before spend
If all surviving value collapses to fields that FOCUS 1.5 plus incumbent FinOps products produce automatically, **kill the wedge**.

If public examples cannot demonstrate a material decision error caused by missing outcome attribution, **hold**.

### Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`

---

# 2. AGENT IDENTITY / DISCOVERY / TRUST

## Red-Team verdict
**RANK AFTER RED TEAM: #2**  
**Route:** `LONG_HORIZON_OPTIONALITY_HOLD`  
**Revised strategic score:** `74/100`  
**WIP:** `RADAR_ONLY`

The infrastructure wave is strong, but the obvious enterprise product layer is being occupied very quickly by identity/network incumbents.

### Public evidence
- DNS-AID uses DNS for decentralized AI-agent/MCP discovery and verification.
- Agent Name Service (ANS) targets portable trusted identity, verification and discovery through DNS/PKI.
- A2A passed 150 supporting organizations and reported production deployments by Apr 2026.
- Agentic AI Foundation reached 247 organizations by 13 Aug 2026.
- Okta now provides generally available AI-agent discovery, centralized agent identity, access governance and kill-switch capabilities.
- Auth0 for AI Agents already provides agent identity/access management and Auth for MCP is GA.
- Infoblox and GoDaddy are themselves advancing DNS-AID/ANS.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-announces-dns-aid-project-to-advance-decentralized-ai-agent-discovery
- https://www.linuxfoundation.org/press/linux-foundation-announces-intent-to-launch-agent-name-service-to-establish-trusted-identity-infrastructure-for-ai-agents
- https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
- https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-57-new-members-gaining-major-financial-services-players-and-apac-leaders
- https://www.okta.com/products/govern-ai-agent-identity/
- https://auth0.com/ai
- https://auth0.com/blog/auth0-auth-for-mcp-servers-generally-available/
- https://www.infoblox.com/news/news-events/press-releases/infoblox-and-godaddy-support-open-standards-for-ai-agent-discovery-identity-and-verification/

### Generic wedges killed
`GENERIC_AGENT_IDENTITY_PLATFORM = KILL`
`GENERIC_MCP_AUTH_SETUP = KILL`
`GENERIC_SHADOW_AGENT_DISCOVERY = KILL_AS_PRIMARY_WEDGE`

These are already directly in Okta/Auth0/identity-security product territory.

### Surviving narrow wedge
`OPEN_CROSS_STANDARD_CONFORMANCE_CORPUS = KEEP_AS_OPTIONALITY`

Potentially reusable asset:
- DNS-AID / ANS publication fixtures;
- A2A/MCP discovery/identity compatibility matrix;
- manifest drift detector;
- negative fixtures for broken discovery/trust metadata;
- protocol-version migration history.

The asset value would be an independent compatibility corpus, **not** an identity control plane.

### Identifiable buyer roles
- identity/security architect;
- IAM/NHI engineering;
- agent platform engineering;
- developer-platform or protocol interoperability teams.

### Smallest internal proof
A read-only validator against public/test DNS and manifests. No credential handling, no identity issuance, no enterprise deployment.

### Fatal test before spend
If Okta/Auth0/Infoblox/GoDaddy/cloud platforms publish complete cross-standard validators or the standards converge into one platform-native flow, the independent wedge becomes too thin. Keep only the learning corpus.

### Proof boundary
`NEAR_TERM_CASHFLOW = WEAK_UNPROVEN`
`WTP = UNKNOWN`

---

# 3. APPIA AI CONFORMITY EVIDENCE

## Red-Team verdict
**RANK AFTER RED TEAM: #3**  
**Route:** `DEFER_BUILD / STANDARDS_WATCH`  
**Revised strategic score:** `66/100`  
**WIP:** `RADAR_ONLY`

The standards signal is real, but the commercial wedge is squeezed between enterprise GRC platforms and professional/accredited assurance roles.

### Public evidence
- Appia Foundation launched 17 Jun 2026 to translate global AI standards into modular, assessable criteria and conformity evidence.
- IBM watsonx.governance already offers obligation mapping, compliance evidence, governance graphs and broad framework support including EU AI Act/NIST/ISO.
- Credo AI already cross-walks regulations, risks and controls and sells governance/advisory workflows.
- Holistic AI markets automated testing, EU AI Act/NIST/ISO mapping, continuous evidence collection and enforcement.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-launches-appia-foundation-to-establish-standardized-conformity-specifications-across-the-ai-value-chain
- https://www.ibm.com/products/watsonx-governance
- https://www.credo.ai/products/ai-governance-insights-hub
- https://www.holisticai.com/

### Generic wedges killed
`GENERIC_AI_ACT_GAP_ANALYSIS = KILL`
`GENERIC_FRAMEWORK_CROSSWALK = KILL`
`GENERIC_COMPLIANCE_EVIDENCE_DASHBOARD = KILL`

The market already has mature vendors with much broader scope, integrations and assurance credibility.

### Surviving narrow wedge
`DEVELOPER_SIDE_MACHINE_CHECKABLE_APPIA_ARTIFACT_QA = WATCH_ONLY`

Only reconsider if Appia publishes machine-checkable modules that create a developer/CI artifact-validation layer poorly served by enterprise GRC products.

### Specialist/legal boundary
Do not represent technical tooling as legal compliance, certification, accredited conformity assessment or assurance opinion.

### Fatal test before spend
If Appia output is primarily consumed through existing GRC/assurance vendors or requires accredited assessment context for buyer value, **do not build**.

### Proof boundary
`WTP = UNKNOWN`
`LEGAL_ASSURANCE_ROLE = NOT_AUTHORIZED`

---

# Comparative decision

| Candidate | Wave strength | Obvious product crowding | Small independent wedge | Regulatory/specialist burden | Decision |
|---|---:|---:|---:|---:|---|
| AI Tokenomics / Cost-to-Value | High | High | Medium | Low | `ADVANCE_INTERNAL_PROOF_ONLY` |
| Agent Identity / Discovery / Trust | Very high | Very high | Medium-low | Medium security burden | `OPTIONALITY_HOLD` |
| Appia conformity evidence | High | Very high | Low | High | `DEFER_BUILD` |

## Why Tokenomics wins this Red Team
Not because it is uncrowded. It is not.

It wins because:
1. buyer roles are clearer;
2. spend/attribution pain is already operational rather than hypothetical;
3. a deterministic internal proof is possible without legal/security custody;
4. a narrow evidence-quality layer can be tested without building a SaaS product;
5. failure can be detected cheaply if FOCUS/incumbents absorb the remaining gap.

## New ordering
1. `EW-D02-02 TOKENOMICS_COST_TO_VALUE` -> smallest internal proof only.
2. `EW-D02-01 AGENT_IDENTITY_DISCOVERY_TRUST` -> long-horizon compatibility corpus / monitor.
3. `EW-D02-03 APPIA_CONFORMITY_EVIDENCE` -> standards watch, no build.

This **does not** alter WIP3 and does not create a market winner.

## Next causal gate
`P-EW06 = TOKENOMICS_OUTCOME_ATTRIBUTION_PROOF_CONTRACT`

P-EW06 must be a bounded internal proof, not a product build:
- one normalized ledger schema;
- one small public/synthetic multi-provider fixture set;
- one outcome-attribution completeness metric;
- one decision-error demonstration;
- one explicit overlap test against FOCUS 1.5 + Finout/CloudZero/Vantage;
- kill if no non-commodity gap remains.

No outreach, sales, paid tooling, production integration or WIP promotion is authorized by this decision.

## Proof boundary
`PUBLIC_EVIDENCE_CEILING = E2_PLUS`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `EARLY-WAVE-TOP3-REDTEAM-TOKENOMICS-INTERNAL-PROOF-IDENTITY-HOLD-APPIA-DEFER-20260822`
