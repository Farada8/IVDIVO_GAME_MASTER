# EARLY-WAVE DELTA02 — REMAINING FIVE RED TEAM

**Date:** 2026-08-22  
**Status:** INTERNAL HORIZON RED TEAM / PUBLIC EVIDENCE ONLY / NO WIP PROMOTION

This pass follows the latest `CURRENT_GENERAL_BUSINESS_ENGINE.md` instruction: scan the remaining Delta02 candidates and kill generic/platform-native wedges before any new proof build.

Candidates attacked:
- x402
- DocLang
- OpenSharing
- EU Age Verification
- European Business Wallet

## Result after commoditization / implementation review

| Rank | Candidate | Prior radar | Red-Team score | Route |
|---|---|---:|---:|---|
| 1 | DocLang / AI-native documents | 80 | 76 | ADVANCE_TO_SMALLEST_INTERNAL_FIDELITY_PROOF_ONLY |
| 2 | EU Age Verification relying-party layer | 76 | 72 | HOLD_STRONG_FORCING_FUNCTION / NO_GENERIC_INTEGRATION |
| 3 | x402 internet-native payments | 82 | 65 | HOLD_WAVE_REAL / GENERIC_INTEGRATION_COMMODITIZED |
| 4 | OpenSharing AI asset exchange | 76 | 60 | HOLD_PLATFORM_NATIVE_BETA / WATCH_CROSS_PLATFORM |
| 5 | European Business Wallet | 64 | 56 | WATCH_PRE_SPEC / DO_NOT_BUILD |

`RED_TEAM_SCORE != MARKET_RANK`
`RED_TEAM_SCORE != BUYER_WTP`

---

# R1 — DocLang

## Public forcing / formation evidence
- LF AI & Data launched the DocLang Specification Working Group on 2026-06-09 with IBM, NVIDIA, Red Hat, ABBYY, HumanSignal and others.
- The DocLang project already publishes the normative specification **and** a reference toolkit.
- The toolkit already validates DocLang with XSD/Schematron and packages `.dclg/.dclx`; therefore plain validation/packaging is not a wedge.
- Docling already supports DocLang input/output.
- Recent Docling Core releases contain repeated DocLang-specific fixes: deep section headers, illegal XML text, XML-sensitive table content, archive size/depth budgets, chemistry serialization and other serializer/deserializer issues.

Sources:
- https://www.linuxfoundation.org/press/lf-ai-data-foundation-launches-doclang-specification-working-group-to-advance-an-open-standard-for-ai-native-documents
- https://github.com/doclang-project/doclang
- https://github.com/docling-project/docling
- https://github.com/docling-project/docling-core/blob/main/CHANGELOG.md

## KILL now
Do not build/sell:
- generic DocLang validator;
- generic DocLang packer;
- simple PDF/Word -> DocLang conversion wrapper;
- basic Docling setup;
- “AI-native document conversion” narrative service without measurable fidelity delta.

Those layers are already reference-toolkit / Docling territory.

## Surviving hypothesis
`DOCLANG_CROSS_CONVERTER_ROUNDTRIP_FIDELITY_AND_REGRESSION_QA`

Potential engineering asset:
- frozen document stress corpus;
- source -> canonical Docling JSON -> DocLang -> re-import comparison;
- structure/layout/geometry/table/formula/inline-format fidelity metrics;
- token-cost delta as a secondary metric, never as sole quality metric;
- version-to-version regression detector;
- explicit loss map rather than binary valid/invalid.

Why this survives: validity is not the same as semantic/layout fidelity. Public changelogs show active serialization/deserialization edge-case correction even while the reference validator exists.

## Smallest next internal proof
`P-EW07_DOCLANG_FIDELITY_PROOF`

Use only synthetic/public-safe fixtures. Predeclare 6 stress cases:
1. nested headings/lists;
2. merged/rich table cells;
3. formulas/code;
4. inline formatting/links;
5. page geometry + image references;
6. XML-sensitive / boundary text.

Pass only if one or more reproducible information-loss or version-regression classes are found **outside simple schema validation**.

Kill/deprioritize if the output reduces to “run the official validator”.

## Fatal risks
- Docling/reference toolkit absorbs fidelity regression quickly;
- no independent buyer budget for QA because conversion is bundled into larger document-AI platforms;
- round-trip loss is acceptable for target workflows and not decision-relevant;
- standard changes too rapidly for a small independent tool to maintain.

Decision: `ADVANCE_TO_SMALLEST_INTERNAL_FIDELITY_PROOF_ONLY`
Score: **76/100**.

---

# R2 — EU Age Verification

## Public forcing / implementation evidence
- The Commission says the age-verification solution is technically ready in 2026 and urges rollout by end-2026.
- The technical portal exposes architecture/specifications and open-source reference implementation.
- Official toolbox already includes a basic verifier UI, verifier backend, Cinema demo verifier, issuer service, Android/iOS components.
- Ireland is among the front-runner Member States listed by the technical portal.

Sources:
- https://commission.europa.eu/news-and-media/news/commission-urges-fast-rollout-age-verification-app-2026-04-29_en
- https://docs.ageverification.dev/
- https://ageverification.dev/Setup/
- https://github.com/eu-digital-identity-wallet/av-web-verifier-ui

## KILL now
Do not build/sell:
- generic “add EU age verification” setup;
- clone of the official verifier UI/backend;
- generic QR verifier demo;
- legal compliance certification;
- claims that integrating the blueprint alone proves DSA compliance.

## Surviving hypothesis
`EU_AV_RELYING_PARTY_PROFILE_VERSION_AND_DEPLOYMENT_EVIDENCE_QA`

Possible future layer:
- profile/version compatibility tests;
- verifier config completeness;
- privacy/security deployment evidence checklist bound to exact technical artifacts;
- national-profile drift checks;
- acceptance-path regression tests.

## Why not advance now
The official reference stack is already substantial, and the remaining work sits closer to security, privacy, national implementation and legal applicability. Error cost is materially higher than DocLang.

Decision: `HOLD_STRONG_FORCING_FUNCTION_NO_GENERIC_INTEGRATION`
Score: **72/100**.

Revisit on a real Ireland/national relying-party profile, implementation deadline, or externally visible integration gap.

---

# R3 — x402

## Public forcing / adoption evidence
- x402 Foundation became operational under Linux Foundation governance on 2026-07-14 with 40 members.
- x402.org currently reports very large real activity and many buyers/sellers.
- The reference project already ships TypeScript, Python and Go SDKs, framework middleware and multiple facilitator options.
- Seller integration is explicitly designed to be minimal; reference docs provide testnet and production flows.
- v2 already includes discovery, extensions, multiple schemes/networks and transport representations including HTTP/MCP/A2A.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications
- https://x402.org/
- https://github.com/x402-foundation/x402
- https://docs.x402.org/getting-started/quickstart-for-sellers

## KILL now
Do not build/sell:
- basic x402 middleware setup;
- generic seller integration;
- generic facilitator directory;
- another SDK wrapper;
- wallet/payment custody;
- speculative token/crypto strategy.

## Surviving hypothesis
`X402_CROSS_TRANSPORT_SCHEME_VERSION_CONFORMANCE_AND_RECEIPT_EVIDENCE_QA`

The spec has real extension/network/version complexity, but the ecosystem is already moving fast and payment correctness has high consequence.

## Why HOLD
- obvious integration is already commodity SDK work;
- multiple production facilitators exist;
- financial protocol/security burden is high;
- any useful wedge must remain non-custodial and evidence/testing only;
- adoption is already large enough that this is less like an unnoticed “Bitcoin at pennies” entry point and more like entering an active ecosystem with sophisticated incumbents.

Decision: `HOLD_WAVE_REAL_GENERIC_INTEGRATION_COMMODITIZED`
Score: **65/100**.

---

# R4 — OpenSharing

## Public forcing / implementation evidence
- Linux Foundation launched OpenSharing on 2026-06-10, contributed by Databricks as evolution of Delta Sharing.
- It targets cross-platform sharing of data, AI models, unstructured assets and agent skills.
- Databricks already renamed/extended Delta Sharing to OpenSharing and exposes native product workflows.
- Sharing/mounting Genie Agents through OpenSharing is already in Beta with defined Unity Catalog privileges.

Sources:
- https://www.linuxfoundation.org/press/linux-foundation-announces-opensharing-project-to-standardize-ai-asset-and-data-exchange
- https://docs.databricks.com/aws/en/data-sharing/
- https://docs.databricks.com/gcp/en/opensharing/share-genie-space

## KILL now
Do not build/sell:
- generic Databricks OpenSharing setup;
- generic provider/recipient walkthrough;
- duplicate marketplace UI;
- basic agent-share packaging on Databricks.

## Surviving hypothesis
`OPENSHARING_CROSS_PLATFORM_RECIPIENT_COMPATIBILITY_AND_ASSET_FIDELITY_QA`

But current independent non-Databricks implementation evidence is not strong enough in this pass to justify a build.

Decision: `HOLD_PLATFORM_NATIVE_BETA_WATCH_CROSS_PLATFORM`
Score: **60/100**.

Revisit when at least two materially independent provider/recipient implementations expose compatibility surfaces outside a single vendor stack.

---

# R5 — European Business Wallet

## Public forcing / formation evidence
- Regulation remains at proposal/legislative/implementation-design stage.
- Commission technical subgroup is still shaping security, authentication, secure communications, trust, discovery and interoperability.
- Proposal includes a future European Digital Directory with a machine-readable interface and contemplates future agentic-AI use cases.

Sources:
- https://digital-strategy.ec.europa.eu/en/news/european-commission-seeks-participants-european-business-wallet-technical-work-sub-group
- https://digital-strategy.ec.europa.eu/en/library/proposal-regulation-establishment-european-business-wallets
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:52025PC0838

## KILL now
Do not build:
- EBW connector before stable technical requirements;
- identity/directory client against guessed APIs;
- compliance product based on proposal text;
- “agentic business wallet” product before actual protocol surfaces exist.

## Surviving hypothesis
`EBW_TECHNICAL_STANDARD_AND_EUROPEAN_DIGITAL_DIRECTORY_WATCH`

Decision: `WATCH_PRE_SPEC_DO_NOT_BUILD`
Score: **56/100**.

---

# Portfolio conclusion

## Candidate allowed to move one internal step
`DOCLANG_CROSS_CONVERTER_ROUNDTRIP_FIDELITY_AND_REGRESSION_QA`

Reason:
- standard is genuinely young;
- obvious validator/converter wedge is already killed;
- public implementation history demonstrates active fidelity/serialization edge cases;
- test can be fully local/read-only and near-zero cost;
- a negative result can kill the hypothesis cheaply.

## Strong watch, no build
`EU_AV_RELYING_PARTY_PROFILE_VERSION_AND_DEPLOYMENT_EVIDENCE_QA`

## Hold
- x402 cross-transport/scheme conformance;
- OpenSharing cross-platform compatibility.

## Watch only
- European Business Wallet.

# Next internal gate
`P-EW07_DOCLANG_FIDELITY_PROOF`

Precondition:
- no external outreach;
- no customer documents;
- no paid tooling;
- synthetic/public-safe stress fixtures only;
- must measure information loss/regression beyond official schema validity;
- kill if it reduces to official validator functionality.

# Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTED = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `DELTA02-REMAINING-REDTEAM-DOCLANG76-EUAV72-X40265-OPENSHARING60-EBW56-NO-WIP-20260822`
