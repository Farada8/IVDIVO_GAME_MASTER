# EARLY-WAVE RED TEAM — DELTA 02 TOP THREE

**Date:** 2026-08-22  
**Status:** INTERNAL RED TEAM / PUBLIC-EVIDENCE ONLY / NO WIP PROMOTION / NO MARKET WINNER

Parent: `25_EARLY_WAVE_RADAR_DELTA02_2026-08-22.md`

## Purpose
Attack the three highest-scoring Delta02 candidates before any build, spend or WIP promotion.

Mandatory laws:

`EARLY_SIGNAL != BUYER_DEMAND`
`PUBLIC_INFRASTRUCTURE_GROWTH != SMALL_VENDOR_WEDGE`
`OPEN_SOURCE_REFERENCE_IMPLEMENTATION != OUR_PRODUCT`
`INCUMBENT_PRODUCT_CATEGORY != UNCONTESTED_MARKET`
`TECHNICAL_PREFLIGHT != LEGAL_CERTIFICATION`
`WTP = UNKNOWN`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

# Executive result

The original ranking survives only after major wedge mutation.

| Candidate | Radar score | Red-Team adjusted score | Decision |
|---|---:|---:|---|
| Agent Identity / Discovery / Trust | 89 | 79 | KEEP_OPTIONALITY_MUTATE_WEDGE |
| AI Tokenomics / Cost-to-Value | 87 | 73 | KEEP_WATCH_KILL_GENERIC_DASHBOARD |
| Appia Conformity Evidence | 87 | 62 | HOLD_UNTIL_PUBLIC_MODULES_AND_ROLE_BOUNDARY |

**No candidate is promoted to WIP.**

---

# RT-01 — Agent Identity / Discovery / Trust

## What changed under attack
The wave is real, but much of the obvious implementation layer is already being supplied.

Public evidence now shows:
- DNS-AID ships a reference implementation, Python SDK, CLI, MCP tooling, DNS-provider integrations, publication/resolution and metadata tooling.
- Agent Name Service ships registry/transparency-log/offline-verifier work and multiple SDKs.
- Okta for AI Agents is already a commercial identity/governance control plane with discovery, registration, access policy, credentials and lifecycle governance.
- Ping Identity for AI reached general availability on 2026-03-31 with first-class agent identity, delegated access and MCP gateway enforcement.
- Rubrik announced Agent Identity on 2026-08-04, adding another enterprise incumbent.

Primary sources / product evidence:
- https://github.com/dns-aid/dns-aid-core
- https://github.com/agentnameservice
- https://www.okta.com/products/govern-ai-agent-identity/
- https://developer.pingidentity.com/identity-for-ai/release-notes/idai-whats-new.html
- https://www.rubrik.com/company/newsroom/press-releases/26/rubrik-unveils-agent-identity-to-secure-agentic-actions-in-real-time

## KILL now
Do **not** build or sell:
- generic agent registration;
- generic DNS-AID publishing;
- generic ANS onboarding;
- generic agent inventory/dashboard;
- generic MCP identity gateway;
- generic enterprise agent IAM.

Those layers are already open-source, platform-native or incumbent territory.

## Surviving wedge
`CROSS_STANDARD_AGENT_IDENTITY_DISCOVERY_INTEROP_AND_DRIFT`

Possible reusable internal asset:
- frozen compatibility corpus across DNS-AID / ANS / A2A agent cards / MCP discovery metadata;
- semantic diff and drift detector as drafts/specs change;
- cross-standard manifest linter;
- migration/compatibility fixtures;
- negative-control suite for identity/discovery claims;
- provider-neutral publication/readiness regression tests.

This is narrower than “agent identity” and intentionally avoids becoming IAM.

## Identifiable buyer roles
Potential, not proven:
- AI platform engineering;
- developer platform / internal developer portal teams;
- AI infrastructure teams;
- security architecture teams managing multi-vendor agent stacks;
- SaaS vendors exposing public agents across more than one protocol.

## Public pain that can be demonstrated without outreach
Yes, partially. Multiple overlapping discovery/identity mechanisms coexist and their own documentation describes different layers and interoperability relationships. That creates observable schema/protocol drift risk.

## Smallest internal proof
Build a **read-only compatibility corpus** from public specs/reference examples and prove whether one normalized manifest can detect:
1. missing identity fields;
2. incompatible endpoint/discovery semantics;
3. version drift;
4. conflicting trust claims;
5. migration breakage across at least three protocol families.

No external customer, credentials or production system required.

## Fatal risks
- one standard wins and absorbs the others;
- platform vendors provide cross-standard compatibility automatically;
- the remaining interoperability pain is only relevant to large IAM vendors;
- public specs churn faster than a small team can maintain economically;
- no buyer pays separately for validation because it is bundled into platform procurement.

## Red-Team decision
`KEEP_OPTIONALITY_MUTATE_WEDGE`

Adjusted score: **79/100**.

Reason: strongest asymmetric learning/asset-compounding candidate, but only if we stay above the commodity publication/IAM layer.

---

# RT-02 — AI Tokenomics / Cost-to-Value

## What changed under attack
The forcing function is strong, but the obvious product category is already crowded.

Public evidence:
- Tokenomics Foundation launched 2026-08-04 with 30 industry members and explicitly targets full AI cost, cost-to-serve, ROI/value and FOCUS token telemetry.
- Finout already normalizes AI spend across OpenAI, Anthropic, Bedrock, SageMaker, Vertex, Cursor and others, allocates spend by team/feature/model/customer/agent, and provides budget/anomaly controls.
- Vantage already markets AI cost observability, allocation and agent/developer-level ROI workflows.
- Major Tokenomics Foundation participants include companies that already sell FinOps/cost tooling, creating fast standard-absorption risk.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-launches-the-tokenomics-foundation-to-define-the-economics-and-roi-of-ai-value
- https://www.finout.io/artificial-intelligence
- https://www.vantage.sh/lp/ai-cost-observability-webinar-series-recording

## KILL now
Do **not** build or sell:
- another generic token dashboard;
- generic multi-provider AI spend monitor;
- generic budget alerts;
- generic cost allocation by team/model;
- “AI FinOps” narrative consulting without a measurable technical delta.

## Surviving wedge
`FOCUS_ALIGNED_AI_COST_TO_OUTCOME_NORMALIZATION_AND_REGRESSION`

Only interesting if it measures a layer incumbents do not trivially commoditize:
- cost per resolved task / accepted output / successful workflow;
- cache/reasoning/tool-call/retry cost decomposition;
- provider-switch regression with cost **and outcome quality** held together;
- FOCUS export/conformance tests when AI telemetry fields stabilize;
- reproducible evidence pack proving cost changes are not purchased by hidden quality/rework losses.

## Identifiable buyer roles
Potential:
- FinOps practitioners;
- CTO/CFO office for AI-intensive SMEs;
- AI product owners;
- platform engineering;
- engineering managers operating multi-model workflows.

## Public pain demonstrability
Strong. Vendors themselves now market the difficulty of attributing AI spend and justifying ROI. The Linux Foundation created a dedicated foundation around the problem.

## Smallest internal proof
Use our own multi-provider AI workflow fixtures and create a provider-neutral ledger that joins:
`REQUEST -> MODEL/TOOLS -> COST -> RETRIES -> ACCEPTANCE/OUTCOME -> COST_PER_ACCEPTED_WORK`

Success is engineering reproducibility, **not market proof**.

## Fatal risks
- Finout/Vantage/Flexera/ServiceNow/other members ship the standard before a small wedge forms;
- outcome measurement remains organization-specific and consulting-heavy;
- reliable business-value attribution requires private enterprise data unavailable to a low-capital entrant;
- FOCUS makes raw normalization commodity plumbing;
- buyer willingness to pay is captured by existing FinOps contracts.

## Red-Team decision
`KEEP_WATCH_KILL_GENERIC_DASHBOARD`

Adjusted score: **73/100**.

Commercially closer than identity, but competitively much more crowded than the first radar score implied.

---

# RT-03 — Appia AI Conformity Evidence

## What changed under attack
The regulatory/procurement pain is plausible, but the independent commercial layer is not yet sufficiently bounded.

Public evidence:
- Appia Foundation is explicitly building open specifications that translate standards/regulations into assessable criteria and conformity evidence.
- Its coalition includes platform companies and conformity/assurance participants.
- Appia itself describes specifications and tools as outputs of the ecosystem, creating a real risk that generic evidence mapping becomes the public/common layer rather than a defensible service.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-launches-appia-foundation-to-establish-standardized-conformity-specifications-across-the-ai-value-chain
- https://appiafoundation.org/
- https://openai.com/index/helping-build-shared-standards-for-advanced-ai/

## KILL now
Do **not** claim or sell:
- certification;
- accredited conformity assessment;
- legal compliance determination;
- “Appia compliant” status before the relevant specifications and role are actually defined;
- generic checklist consulting based on announcement-level material.

## Surviving wedge
Only a future technical layer:
`PUBLIC_APPIA_MODULE_TO_TECHNICAL_EVIDENCE_GRAPH_PREFLIGHT`

Possible components, once modules are public/stable enough:
- criteria-to-artifact graph;
- evidence completeness checker;
- provider/deployer evidence pass-through validation;
- version drift/regression;
- explicit distinction between technical evidence preparation and third-party conformity judgment.

## Identifiable buyer roles
Potential:
- AI governance / responsible AI teams;
- supplier assurance / procurement;
- product compliance engineering;
- model/application providers preparing evidence packages.

## Public pain demonstrability
Moderate-to-strong at the category level, weak at the exact Appia-tooling wedge level today.

## Smallest internal proof
**Do not build yet** unless at least one sufficiently concrete public Appia specification/module is available. When available, map one module into a typed evidence graph and test it against public/synthetic artifacts.

## Fatal risks
- practical value belongs primarily to accredited assessors/test labs;
- foundation/member tools automate mapping;
- liability expectations make low-cost independent work unattractive;
- buyers require ISO/IEC or sector credentials beyond our present evidence;
- specifications remain immature or change materially.

## Red-Team decision
`HOLD_UNTIL_PUBLIC_MODULES_AND_ROLE_BOUNDARY`

Adjusted score: **62/100**.

This is no longer a top candidate for immediate internal build despite the strong macro forcing function.

---

# Cross-candidate conclusion

## 1. Best long-horizon asymmetric learning asset
`AGENT_IDENTITY_DISCOVERY_CROSS_STANDARD_INTEROP`

Not agent IAM. Not registration. Not a DNS-AID setup service.

## 2. Best near-term internal cashflow hypothesis to test later
`AI_COST_TO_OUTCOME_NORMALIZATION`

Not a token dashboard. It survives only if cost is joined to accepted work/outcome quality in a way existing FinOps tools do not make trivial.

## 3. Hold
`APPIA_TECHNICAL_EVIDENCE_PREFLIGHT`

Wait for sufficiently concrete public modules and a clean technical-vs-assessment role boundary.

# WIP decision

`NO_NEW_WIP_PROMOTION`

Reasons:
- current WIP limit remains binding;
- buyer demand/WTP remain unproven;
- RT-01 and RT-02 both require one more bounded internal proof before they deserve replacement consideration;
- RT-03 is not build-ready.

# Next internal tests

**T-ID01 — Cross-standard identity/discovery compatibility corpus**
- 3+ protocol families;
- read-only public fixtures;
- deterministic normalize/diff/lint output;
- at least one real incompatibility/drift finding required to remain interesting.

**T-TOK01 — Cost-to-accepted-work ledger**
- 2+ providers/models;
- cost, retries, tool calls and acceptance outcome joined;
- compare against what generic FinOps dashboards already expose;
- kill if output reduces to ordinary cost allocation.

Do not start Appia implementation until its module gate clears.

# Proof boundary

`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTED = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `EARLY-WAVE-REDTEAM-TOP3-IDENTITY79-TOKENOMICS73-APPIA62-NO-WIP-20260822`
