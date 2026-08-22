# EARLY-WAVE REMAINING-5 RED TEAM

**Date:** 2026-08-22  
**Status:** INTERNAL RED TEAM / PUBLIC-EVIDENCE ONLY / NO WIP PROMOTION / NO EXTERNAL ACTION

Parent radar:
`25_EARLY_WAVE_RADAR_DELTA02_2026-08-22.md`

Purpose: red-team the five Delta02 candidates not included in the first top-three pass. The question is not whether the wave is real; it is whether a small, non-obvious, low-capital wedge remains after first-party tooling and regulatory/security burden are counted.

`REAL_WAVE != ENTRY_WEDGE`
`REFERENCE_IMPLEMENTATION != BUYER_WTP`
`PLATFORM_NATIVE != INDEPENDENT_SERVICE_MARKET`
`OPEN_SOURCE_BUG != COMMERCIAL_DEMAND`

---

# 1. DOCLANG / AI-NATIVE DOCUMENT INTEROPERABILITY

## Red-Team verdict
**Rank among remaining five:** #1  
**Revised score:** `73/100`  
**Route:** `ADVANCE_TO_SMALLEST_PUBLIC_FIXTURE_PROOF_ONLY`  
**WIP:** `RADAR_ONLY`

### Public evidence
- LF AI & Data launched DocLang Specification Working Group on 9 Jun 2026, founded by IBM, NVIDIA, Red Hat and others.
- The official DocLang project already publishes the normative specification and a reference Python toolkit with XSD + Schematron validation and packaging.
- Docling already reads and writes DocLang XML/archive as native supported formats.
- Real public issue reports in July 2026 show conversion/semantic fidelity failures can still occur: PDF->DocLang output failing syntax validation on `&`, and layout misclassification that leaves invalid/missing semantic text.

Sources:
- https://www.linuxfoundation.org/press/lf-ai-data-foundation-launches-doclang-specification-working-group-to-advance-an-open-standard-for-ai-native-documents
- https://github.com/doclang-project/doclang
- https://github.com/doclang-project/doclang/blob/main/doclang/README.md
- https://docling-project.github.io/docling/usage/supported_formats/
- https://github.com/docling-project/docling/issues/3864
- https://github.com/docling-project/docling/issues/3780

### Generic wedges killed
`GENERIC_DOCLANG_CONVERTER = KILL`
`GENERIC_SCHEMA_VALIDATOR = KILL`
`GENERIC_DOCLANG_PACKAGER = KILL`

Reason: official/reference tooling already supplies these functions.

### Surviving hypothesis
`DOCUMENT_CONVERSION_FIDELITY_REGRESSION_QA = KEEP_TESTABLE`

Potential independent layer:
- compare source semantics/layout against converted DocLang;
- detect structurally valid but semantically damaged conversions;
- preserve a corpus of adversarial document fixtures and version-to-version regression history;
- test conversion across Docling/other exporters without replacing the reference validator.

### Why this survives Red Team
Syntax conformance and conversion existence are already commodity/open-source capabilities, but **fidelity after conversion is a separate problem**. Public bug reports show the distinction is not theoretical.

### Buyer roles, if later evidenced
- document-AI / RAG engineering;
- enterprise document ingestion teams;
- AI platform/data engineering;
- vendors shipping conversion pipelines.

Buyer pain/WTP remain unproven.

### Smallest internal proof
Use only public/minimal fixtures derived from disclosed failure classes. Show that:
1. schema-valid output can still lose/misclassify semantic content, or that a converter can produce invalid output;
2. a deterministic fidelity check catches the defect not represented by plain schema validation;
3. the checker remains independent of one converter implementation.

### Fatal conditions
- Docling/reference toolkit adds robust semantic fidelity/regression checks that absorb the gap;
- public defects are rare edge cases with no operational consequence;
- a test cannot distinguish fidelity QA from ordinary schema validation.

`WTP = UNKNOWN`

---

# 2. EU AGE VERIFICATION — RELYING-PARTY READINESS

## Red-Team verdict
**Rank among remaining five:** #2  
**Revised score:** `69/100`  
**Route:** `SPECIALIST_HOLD / REFERENCE-IMPLEMENTATION GAP WATCH`  
**WIP:** `RADAR_ONLY`

### Public forcing function
- Commission expects EU-wide availability by end-2026 and works with seven frontrunners including Ireland.
- The feature-ready solution became available 15 Apr 2026 and is aligned with future EUDI Wallets.
- Technical specifications include normative requirements for Age Verification Apps, Attestation Providers, Relying Parties and Trusted Lists.
- The EU project already publishes a reference verifier endpoint implementing OpenID4VP and a verifier UI/reference flow.
- The white-label/reference implementation still requires integration/customisation for production use.

Sources:
- https://digital-strategy.ec.europa.eu/en/faqs/eu-age-verification-solution
- https://digital-strategy.ec.europa.eu/en/policies/eu-age-verification
- https://github.com/eu-digital-identity-wallet/av-doc-technical-specification
- https://github.com/eu-digital-identity-wallet/av-srv-verifier-endpoint
- https://github.com/eu-digital-identity-wallet/av-web-verifier-ui

### Generic wedges killed
`GENERIC_AGE_VERIFICATION_APP = KILL`
`GENERIC_REFERENCE_VERIFIER_BUILD = KILL`
`IDENTITY_PROVIDER_OR_ISSUER_ROLE = OUT_OF_SCOPE`
`SECURITY_OR_LEGAL_CERTIFICATION = OUT_OF_SCOPE`

### Surviving hypothesis
`RELYING_PARTY_CONFORMANCE_AND_INTEGRATION_REGRESSION_QA = WATCH_TESTABLE`

Potential bounded layer:
- RP request/profile conformance;
- OpenID4VP flow regression against the EU reference implementation;
- privacy/data-minimisation checks expressed only as machine-checkable technical invariants from published specs;
- compatibility drift across AV mini-wallet -> EUDI Wallet evolution.

### Why not promote
Security/privacy/liability burden is materially higher than DocLang. The Commission itself is creating trusted lists/scheme governance and public reference implementations. Any value may concentrate in established identity/security integrators.

### Fatal conditions
- RP integration becomes effectively plug-and-play in major identity/platform SDKs;
- useful value requires legal opinion, formal certification, penetration testing or identity-provider operation;
- EUDI Wallet absorbs the standalone AV integration path before a separate wedge forms.

`WTP = UNKNOWN`

---

# 3. EUROPEAN BUSINESS WALLET INTEROPERABILITY

## Red-Team verdict
**Rank among remaining five:** #3  
**Revised score:** `64/100`  
**Route:** `CHEAP_OPTIONALITY_WATCH`  
**WIP:** `RADAR_ONLY`

### Public evidence
- European Business Wallet is already a legislative proposal and part of the EU digital simplification agenda.
- On 24 Apr 2026 the Commission sought technical experts specifically to shape secure communication, authentication/access control, trust, discovery, interoperability and the European Digital Directory.
- The EESC July 2026 opinion explicitly calls for clearer identity matching, mandate structures, security/accountability and international operability.
- EU Inc. proposals expect Business Wallets to link to official business-register identity and support verified company documents and cross-border processes.

Sources:
- https://digital-strategy.ec.europa.eu/en/news/european-commission-seeks-participants-european-business-wallet-technical-work-sub-group
- https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52025AE3899
- https://digital-strategy.ec.europa.eu/en/news/eu-inc-new-digital-company-framework-simplify-cross-border-business-europe

### Generic wedge status
`GENERIC_EBW_INTEGRATION_SERVICE = TOO_EARLY`
`GENERIC_WALLET_PRODUCT = KILL_FOR_FOUNDER_PROFILE`

### Surviving optionality
`EBW_INTEROPERABILITY_FIXTURE_CORPUS = WATCH_ONLY`

Monitor:
- business identity/mandate representation;
- relying-party protocols;
- Digital Directory discovery;
- document/signature/seal interoperability;
- EUDI/BRIS/OOTS interaction.

Do not build before the technical architecture/implementing specifications settle enough to create a falsifiable interoperability test.

`WTP = UNKNOWN`

---

# 4. x402 NON-CUSTODIAL AGENT PAYMENT TOOLING

## Red-Team verdict
**Rank among remaining five:** #4  
**Revised score:** `61/100`  
**Route:** `LONG-HORIZON_PROTOCOL_WATCH / NO BUILD`  
**WIP:** `RADAR_ONLY`

### Public evidence
- x402 Foundation operationally launched 14 Jul 2026 with 40 members under Linux Foundation governance.
- Coinbase already offers a hosted facilitator with verify/settle, KYT screening, many networks and a free tier of 1,000 transactions/month.
- Cloudflare Agents SDK already provides first-class x402 client/server integration for HTTP and MCP tools.
- Cloudflare now supports both x402 and Machine Payments Protocol (MPP) under one agentic-payments layer.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications
- https://docs.cdp.coinbase.com/x402/core-concepts/facilitator
- https://developers.cloudflare.com/agents/tools/payments/x402/
- https://developers.cloudflare.com/agents/tools/payments/

### Generic wedges killed
`GENERIC_X402_ENABLEMENT = KILL`
`GENERIC_X402_FACILITATOR = KILL_FOR_FOUNDER_PROFILE`
`GENERIC_MCP_PAID_TOOL_WRAPPER = KILL`

Reason: platform/reference SDKs already cover integration and facilitator operation; facilitator/payment execution introduces security/compliance/payment liability disproportionate to the Founder profile.

### Thin surviving optionality
`CROSS_PROTOCOL_PAYMENT_RECEIPT_RETRY_ACCOUNTING_CONFORMANCE = WATCH_ONLY`

Potential future corpus across x402/MPP:
- challenge/credential/receipt semantics;
- idempotency and retry behavior;
- accounting/reconciliation metadata;
- failure classification.

No custody, wallet-key handling, settlement, facilitator operation or production payments.

### Fatal conditions
- Cloudflare/other platforms normalize x402/MPP interoperability and receipts completely;
- useful testing requires live funds/keys or regulated activity;
- the protocol remains crypto-heavy rather than broad enterprise machine payments.

`WTP = UNKNOWN`

---

# 5. OPENSHARING AGENT SKILLS / AI ASSET EXCHANGE

## Red-Team verdict
**Rank among remaining five:** #5  
**Revised score:** `54/100`  
**Route:** `PLATFORM_WATCH / DO_NOT_BUILD`  
**WIP:** `RADAR_ONLY`

### Public evidence
- Linux Foundation launched OpenSharing 10 Jun 2026 from a Databricks contribution, extending Delta Sharing to agent skills, models and unstructured data.
- Databricks has already productised OpenSharing in Unity Catalog, Marketplace/Clean Rooms and cross-platform sharing.
- Current Databricks documentation covers provider setup, OIDC/bearer authentication, auditing, recipient flows and sharing data, AI models, notebooks and Genie Agents.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange
- https://docs.databricks.com/aws/en/opensharing
- https://docs.databricks.com/aws/en/data-sharing/
- https://docs.databricks.com/aws/en/opensharing/create-share

### Generic wedges killed
`GENERIC_OPENSHARING_SETUP = KILL`
`GENERIC_DATABRICKS_PROVIDER_CONFIGURATION = KILL`
`GENERIC_RECIPIENT_CONNECTOR_SETUP = KILL`

### Residual hypothesis
`NON_DATABRICKS_CROSS_PLATFORM_CONFORMANCE = WATCH_ONLY`

Only reconsider if independent open-source providers/recipients proliferate and demonstrate interoperability failures not already handled by Databricks/open-source reference connectors.

### Fatal condition
If practical adoption remains Databricks-led and native tooling covers the lifecycle, there is no independent low-capital wedge worth pursuing.

`WTP = UNKNOWN`

---

# Remaining-five comparative result

| Rank | Candidate | Revised score | Primary decision |
|---|---|---:|---|
| 1 | DocLang fidelity regression QA | 73 | `ADVANCE_SMALLEST_INTERNAL_PUBLIC_FIXTURE_PROOF_ONLY` |
| 2 | EU Age Verification RP conformance | 69 | `SPECIALIST_HOLD` |
| 3 | European Business Wallet interoperability | 64 | `CHEAP_OPTIONALITY_WATCH` |
| 4 | x402 machine payments | 61 | `PROTOCOL_WATCH_NO_BUILD` |
| 5 | OpenSharing | 54 | `PLATFORM_WATCH_DO_NOT_BUILD` |

## Cross-Delta conclusion after both Red Teams
No new candidate is promoted into WIP.

Most useful **next internal falsification**, while external buyer testing remains unauthorized:
`P-EW07 = DOCLANG_FIDELITY_REGRESSION_PROOF`

Why DocLang, despite a lower original radar score:
- no custody/payment/legal-assurance role;
- official conversion/validation tooling makes commodity boundaries clear;
- real public defect classes already exist;
- a small public-fixture proof can cheaply determine whether a distinct fidelity QA layer exists.

P-EW07 must be killed if it merely duplicates the official DocLang validator or one converter's unit tests.

## Proof boundary
`PUBLIC_EVIDENCE_CEILING = E2_PLUS`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `EARLY-WAVE-REMAINING5-REDTEAM-DOCLANG-PROOF-NEXT-AGE-HOLD-EBW-WATCH-X402-WATCH-OPENSHARING-KILL-20260822`
