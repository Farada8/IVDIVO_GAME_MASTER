# EARLY-WAVE RADAR — DELTA 03

**Date:** 2026-08-22  
**Status:** HORIZON SCAN / FALSIFICATION-FIRST / NO WIP PROMOTION / NO MARKET WINNER  
**Founder profile:** REMOTE-FIRST / EUR0–500 preferred / EUR3,000 default ceiling / near-zero physical load / test-before-spend

## Purpose
Continue the search for infrastructure/regulatory waves forming now, but reject any opportunity whose supposed wedge is already supplied by the protocol, platform, regulator, or a mature incumbent.

`NEW_STANDARD != NEW_BUSINESS`
`FORCING_FUNCTION != OUR_CAPABILITY`
`OPEN_TOOLING_GAP != WTP`
`SECURITY_PAIN != SAFE_FOUNDER_FIT`

# Ranked Delta03 candidates

## D03-01 — OSERA / CRA machine-readable patch-consumption evidence conformance — 84/100
**Stage:** `FORMATION_WITH_REAL_BANK_PILOT`  
**Route:** `SMALLEST_INTERNAL_PROOF_CANDIDATE`  
**WIP:** `RADAR_ONLY`

### Fresh signal stack
FINOS announced OSERA on 26 June 2026 after an end-to-end pilot with major banks. OSERA is explicitly building an open, vendor-neutral layer for downstream consumption of backpatched open-source dependencies in regulated enterprises.

Current public OSERA evidence is unusually concrete:
- a Risk Navigator already exists for exposure/prioritization;
- public backpatch repositories and release tags exist;
- draft patching standards cover fork naming, baseline tags, provenance links, build evidence, bytecode compatibility, `+backpatch.NNN` metadata, OpenVEX/CycloneDX feeds and recipient test-surface evidence;
- OSERA explicitly proposes a machine-readable consumption evidence pack mapped to DORA/NIS2/CRA;
- some draft requirements still call for future automated acceptance checks.

First-party sources:
- https://osera.finos.org/
- https://standards.osera.finos.org/
- https://standards.osera.finos.org/standards/rel-001-build-process/
- https://standards.osera.finos.org/standards/rel-002-bytecode-compatibility/
- https://standards.osera.finos.org/standards/feed-001-openvex-cyclonedx/
- https://standards.osera.finos.org/standards/evd-001-change-and-test-surface/
- https://standards.osera.finos.org/governance/

### Generic wedges killed immediately
- vulnerability scanner;
- OSS risk dashboard;
- CVE prioritization dashboard;
- SBOM viewer;
- patch-production/security consultancy;
- generic CRA legal/compliance advisory.

Reason: Risk Navigator, OpenSSF/GUAC/SBOM ecosystems, commercial SCA vendors and the OSERA participant model already occupy these layers.

### Narrow surviving hypothesis
`OSERA_DRAFT_RELEASE_EVIDENCE_CONFORMANCE_AND_COMPLETENESS_QA`

A bounded tool could check public patch-provider artifacts against machine-checkable parts of the emerging draft without deciding whether software is secure or legally compliant:
- repository/branch/release naming;
- baseline tags;
- provenance-link presence;
- release evidence completeness;
- bytecode evidence presence/consistency;
- OpenVEX/CycloneDX cross-feed identity consistency;
- recipient-guidance completeness;
- version drift as draft standards evolve.

### Why it is early
OSERA says the current standard is provisional/evaluation material. Its governance specifically asks for acceptance checks for bytecode level, baseline tags, provenance links and version metadata. This is a visible tooling surface before the standard is mature.

### Founder-fit risk
The underlying domain is cybersecurity/regulatory supply-chain engineering. We must remain at evidence/conformance mechanics, not vulnerability judgement, remediation assurance or legal compliance.

### Kill conditions
- OSERA ships first-party conformance tooling covering the same checks;
- draft requirements churn too rapidly for useful stable fixtures;
- practical value requires private bank estates or paid OSERA membership;
- the only valuable checks require security expert judgement rather than deterministic evidence validation;
- no meaningful defects are found across public backpatch repos.

`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`

---

## D03-02 — SAFE Shared AI Findings Exchange interoperability — 74/100
**Stage:** `RFC / PRE-STANDARD`  
**Route:** `CHEAP_OPTIONALITY_WATCH`  
**WIP:** `RADAR_ONLY`

### Fresh signal
On 4 August 2026 the Open Secure AI Alliance published an RFC for the Shared AI Findings Exchange (SAFE), intended to collect AI incidents and near misses and turn them into shared defensive controls.

The current RFC already requires/anticipates:
- incident reporting timelines;
- preserved prompts, traces, tool calls, configurations, model/safeguard versions and dependencies;
- agent/workload identities, permissions, human approvals and incident timelines;
- weekly machine-readable updates while material risk remains unresolved;
- reusable tests, machine-readable policies, detection rules and versioned defensive recommendations where safe.

First-party sources:
- https://www.linuxfoundation.org/blog/proposing-the-safe-working-group-an-open-community-effort-to-improve-ai-security
- https://github.com/OpenSecureAIAlliance/RFCs/blob/main/rfc-safe-proposal.md

### Why not build now
The RFC does **not yet define a stable public schema/taxonomy**. Confidential incident handling, disclosure, security and legal obligations dominate the operational layer.

Killed:
- incident-response consultancy;
- security assurance service;
- confidential incident exchange operator;
- generic AI security dashboard.

Only allowed current action:
`SCHEMA_TAXONOMY_DRIFT_WATCH_ONLY`

Promotion condition: a stable/open machine-readable incident/control schema emerges and exposes a deterministic interoperability or validation gap that can be tested without handling confidential incidents.

`WTP = UNKNOWN`

---

## D03-03 — FINOS Governance-as-Code evidence lineage — 69/100
**Stage:** `EARLY_PRODUCTION_ECOSYSTEM`  
**Route:** `WATCH / KILL_GENERIC_VALIDATION`  
**WIP:** `RADAR_ONLY`

### Signal
FINOS is explicitly developing Governance-as-Code pipelines combining AI Governance Framework, CALM, Common Controls and Fluxnova. CALM already supports schema/pattern/control validation, diffing, a validation server and AI tooling.

First-party sources:
- https://www.finos.org/this-week-at-finos/this-week-at-finos-week-of-august-10-2026
- https://calm.finos.org/
- https://calm.finos.org/working-with-calm/cli/
- https://calm.finos.org/working-with-calm/validation-server/

### Generic wedges killed
- CALM validator;
- CALM schema setup;
- architecture diagram generator;
- generic compliance-as-code dashboard.

### Possible later surface
Only cross-artifact evidence lineage/drift across multiple governance components could be differentiated, but that is currently too close to existing platform direction and enterprise-specific integration.

Route:
`WATCH_FOR_CROSS_TOOL_EVIDENCE_HANDOFF_GAP`

---

## D03-04 — CRA machine-readable due-diligence signal correlation — 66/100
**Stage:** `DEADLINE_DRIVEN / TOOLING_ALREADY_FORMING`  
**Route:** `WATCH / DO_NOT_BUILD_GENERIC_AGGREGATOR`  
**WIP:** `RADAR_ONLY`

### Signal
EU CRA guidance was published 27 July 2026. OpenSSF argues that machine-readable continuously generated signals are the practical basis for due diligence at scale. CRA reporting obligations begin in September 2026 and full obligations arrive December 2027.

Existing open tooling already covers much of the plumbing: SBOM/VEX, in-toto, Protobom, Bomctl, OpenSSF Scorecard and GUAC.

First-party sources:
- https://digital-strategy.ec.europa.eu/en/news/commission-publishes-new-guidance-support-businesses-implementation-cyber-resilience-act
- https://openssf.org/blog/2026/05/29/aligning-on-machine-readable-signals-as-the-foundation-for-due-diligence/
- https://openssf.org/resources/publications/2026-cra-awareness-and-readiness-report/

Killed:
- generic CRA checklist;
- SBOM aggregator;
- generic due-diligence dashboard;
- legal compliance report generator.

A future candidate must be narrower and prove a cross-format evidence defect not already handled by GUAC/Protobom/Bomctl/SCA vendors.

---

## D03-05 — FDC3 3.0 + MCP financial-agent interoperability — 63/100
**Stage:** `EARLY_PRODUCTION / INDUSTRY-SPECIFIC`  
**Route:** `ADJACENT_WATCH`  
**WIP:** `RADAR_ONLY`

FINOS reports FDC3 3.0 and Fluxnova 3.0 adding AI/MCP-oriented capabilities, security and observability. This is real adoption, but it substantially overlaps our already-active cross-protocol Agentic Commerce/identity work and requires finance-specific domain context.

Sources:
- https://www.finos.org/newsletter/2026-07
- https://fdc3.finos.org/docs/next/fdc3-standard
- https://www.linuxfoundation.org/blog/linux-foundation-newsletter-august-2026

No separate WIP. Reuse only as an external stress domain if current OW-01/T-ID compatibility tooling later needs cross-industry fixtures.

---

## D03-06 — AI-generated infrastructure governance/drift — 58/100
**Stage:** `ACTIVE COMMERCIAL CATEGORY`  
**Route:** `KILL_GENERIC_WEDGE`  
**WIP:** `RADAR_ONLY`

The problem is real: AI can generate infrastructure code faster than organizations can govern, validate and reconcile real-world drift. But established infrastructure/governance vendors already market policy, drift and remediation layers.

Source signal:
- https://www.linuxfoundation.org/webinars/ai-can-write-your-infrastructure-code.-can-it-govern-and-heal-what-it-builds

Killed:
- generic IaC drift dashboard;
- AI infrastructure governance wrapper;
- generic policy checker.

No proof build.

# Delta03 routing conclusion

## Highest-information next internal proof candidate
`D03-01_OSERA_DRAFT_RELEASE_EVIDENCE_CONFORMANCE_AND_COMPLETENESS_QA`

Why:
- wave is only weeks old;
- real bank pilot exists;
- public artifacts exist now;
- public draft standards contain explicit deterministic requirements;
- governance asks for acceptance checks that are not yet fully supplied;
- a proof can be read-only, remote, zero-cost and based entirely on public repositories;
- failure can kill the hypothesis quickly if public OSERA repositories already satisfy everything or existing tools cover the layer.

## Predeclared smallest proof
Before any build, freeze 8–12 public OSERA backpatch repositories and 5–7 machine-checkable draft rules. A minimal validator may only classify observable evidence:
- PASS;
- FAIL_OBSERVED;
- UNKNOWN_NOT_PUBLIC;
- NOT_APPLICABLE.

It must not classify software as secure, compliant or safe.

### Kill threshold
If fewer than **2 independent, non-trivial, reproducible conformance/evidence gaps** are found across the frozen public sample, or if all findings reduce to documentation/naming cosmetics with no recipient decision value:
`KILL_OSERA_QA_AS_PRODUCT_HYPOTHESIS`

If >=2 meaningful independent gaps exist:
`PASS_TECHNICAL_GAP_ONLY`

Even then:
`WTP = UNKNOWN`
`WIP_PROMOTION = FALSE`

# Proof boundary
`DELTA03 = RADAR_ONLY`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `EARLY-WAVE-DELTA03-OSERA84-SAFE74-GOVCODE69-CRA66-FDC363-IAC58-NO-WIP-NO-WTP-20260822`
