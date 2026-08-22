# P-EW03 — AI ACT ARTICLE 50 TECHNICAL TRANSPARENCY PACK v0

**Date:** 2026-08-22  
**Lane:** `CF-01 AI Act Article 50 Technical Transparency Pack`  
**Parent authority:** `16_EARLY_WAVE_RADAR_STATE.json`  
**Status:** INTERNAL ENGINEERING SAMPLE / NOT LEGAL ADVICE / NO COMPLIANCE CERTIFICATION

## 1. Purpose
Compile a concrete Article 50 implementation packet from role + use case + evidence, rather than selling generic “AI compliance consulting”.

Pipeline:
`ROLE -> SYSTEM/CONTENT USE -> ARTICLE 50 ROUTE -> EXCEPTION/SPECIAL REGIME -> CONTROL OBJECT -> EVIDENCE OBJECT -> UNRESOLVED ITEM -> REVIEW`

## 2. Current legal/source baseline
Article 50 obligations apply from **2 August 2026**. The Commission published final Article 50 implementation Guidelines on 20 July 2026 and the final Code of Practice on Transparency of AI-generated Content in June 2026. In July 2026 the Commission and AI Board assessed the Code as an adequate voluntary tool for Articles 50(2), (4) and (5). Adherence is voluntary and is not conclusive evidence of compliance.

This pack therefore separates:
- statutory obligation;
- Commission guideline interpretation;
- voluntary Code route;
- organisation-specific implementation evidence;
- unresolved legal judgement.

## 3. Core laws
`ROLE_UNKNOWN -> HOLD_SCOPE`

`PROVIDER_OBLIGATION != DEPLOYER_OBLIGATION`

`CODE_SIGNATORY != AUTOMATIC_COMPLIANCE`

`NOT_CODE_SIGNATORY != NON_COMPLIANCE`

`MACHINE_READABLE_MARKING != HUMAN_FACING_DISCLOSURE`

`PROVIDER_MARKING != DEPLOYER_LABEL`

`HUMAN_REVIEW != EDITORIAL_RESPONSIBILITY`

`CREATIVE_CONTEXT != NO_DISCLOSURE`

`OBVIOUS_AI_INTERACTION_EXCEPTION -> RESTRICTIVE_REVIEW_NOT_SILENT_SKIP`

`ARTICLE50_EVIDENCE != GDPR_COMPLIANCE`

`IMPLEMENTATION_PACK != LEGAL_OPINION`

## 4. Routed obligations
### A50-1 — Provider / direct AI interaction
Provider systems intended to interact directly with natural persons must be designed so people are informed they are interacting with AI, unless this is obvious in context. The Guidelines describe the obviousness exception restrictively. Disclosure should be clear from the start of the first interaction and meet accessibility requirements.

Evidence object: `InteractionDisclosureEvidence`.

### A50-2 — Provider / synthetic audio-image-video-text generation
Providers of AI systems, including GPAI systems, that generate synthetic audio, image, video or text must ensure outputs are marked in a machine-readable format and detectable as artificially generated/manipulated, subject to the Act and clarified scope/exclusions. Technical measures must be effective, interoperable, robust and reliable as far as technically feasible.

The pack does **not** automatically infer an exclusion from vague labels such as “editing”, “B2B”, or “industrial”. Potential exclusions are routed to review unless inputs establish the Guidelines' conditions.

Evidence object: `MachineReadableMarkingEvidence`.

### A50-3 — Deployer / emotion recognition or biometric categorisation
Deployers must inform natural persons exposed to operation of emotion-recognition or biometric-categorisation systems. Personal-data obligations remain a separate legal plane and are not proven by this pack.

Evidence object: `ExposureNoticeEvidence`.

### A50-4A — Deployer / deepfake
Deployers using AI to generate/manipulate deepfake image/audio/video must disclose artificial generation/manipulation. Evidently artistic, creative, satirical, fictional or analogous works receive a special presentation regime: disclosure remains required but may be made appropriately so it does not hamper display/enjoyment.

Evidence object: `ContentDisclosureEvidence`.

### A50-4B — Deployer / public-interest text
Deployers publishing AI-generated/manipulated text to inform the public on matters of public interest must disclose it unless the text underwent human review/editorial control **and** a natural or legal person holds editorial responsibility for publication.

Evidence object: `PublicInterestTextDisclosureEvidence` or `EditorialExceptionEvidence`.

### A50-5 — Cross-cutting presentation
Information/disclosures under Article 50 must be clear and distinguishable, provided at the latest at first interaction/exposure, and comply with accessibility requirements. Machine-readable provider marking alone does not satisfy a deployer's human-facing disclosure duty.

Evidence object: `PresentationAccessibilityEvidence`.

## 5. Evidence object contract
Every claimed implemented control MUST bind:
- obligation id;
- actor role;
- system/content id;
- version/release;
- deployment surface;
- disclosure/marking mechanism;
- timing/placement;
- accessibility treatment;
- content types;
- test method and result;
- limitations/failure modes;
- evidence artifact hash/reference;
- owner;
- review date;
- unresolved items.

A field marked `DESIGN_ONLY`, `UNKNOWN`, or `NOT_TESTED` cannot be reported as implemented.

## 6. Machine-readable marking pack
For A50-2, record at minimum:
- marking/provenance mechanism and version;
- which content types are covered;
- where the mark is inserted;
- detector/verifier interface;
- machine-readability test;
- interoperability evidence;
- robustness/reliability test;
- known removal/degradation conditions;
- technical feasibility limitations;
- logging/change control;
- Code commitment mapping if the organisation is a signatory.

The pack does not mandate one technology merely because it is fashionable. The actual mechanism must be evidence-bound to the provider's system and current state of the art.

## 7. Human-facing disclosure pack
For A50-1, A50-3 and A50-4:
- exact plain-language disclosure text;
- channel/surface;
- event triggering disclosure;
- first-interaction/first-exposure timing;
- visible/audible placement;
- language variants;
- accessibility/assistive-technology treatment;
- optional EU icon use where relevant;
- screenshot/audio/render evidence;
- version and owner.

The Commission's EU icons are optional; Article 50 labelling obligations are not. Icon use alone does not prove compliance.

## 8. Exception/special-regime object
No exception is accepted from an unlabeled boolean alone. Store:
- candidate exception;
- exact facts;
- legal/guideline source;
- cumulative conditions;
- reviewer;
- decision: `CONFIRMED`, `REJECTED`, `PENDING_REVIEW`;
- expiry/review trigger.

Sensitive examples:
- “obvious AI interaction” -> restrictive review;
- standard editing / machine-only / closed-loop output -> scope review;
- creative deepfake -> special disclosure regime, not automatic exemption;
- public-interest text -> human review/editorial control plus editorial responsibility must both be evidenced.

## 9. Voluntary Code route
`code_adherence` accepts `SIGNED`, `NOT_SIGNED`, `UNKNOWN`.

- `SIGNED`: map evidence to relevant Code section/commitments; still no automatic compliance claim.
- `NOT_SIGNED`: require an alternative-measures evidence map; do not classify as non-compliant solely because the Code was not signed.
- `UNKNOWN`: hold Code-route claim.

## 10. P-EW03 synthetic sample
The sample packet contains six synthetic cases designed to exercise all main routes:
1. provider chatbot, non-obvious direct interaction;
2. provider generative image/text system;
3. deployer emotion-recognition system;
4. deployer deepfake marketing video;
5. deployer public-interest AI text without editorial exception;
6. same public-interest text with documented human review/editorial control + editorial responsibility.

No synthetic case is presented as evidence about a real customer.

## 11. Acceptance
P-EW03 passes engineering only if:
- provider/deployer roles stay distinct;
- all Article 50 branches route deterministically;
- uncertain exceptions fail closed;
- creative deepfake stays disclosure-bound;
- public-interest text exception requires both review/control and editorial responsibility;
- Article 50(5) attaches to applicable routes;
- Code adherence does not become a compliance shortcut;
- sample evidence clearly separates `DESIGN_ONLY` from implemented/tested;
- no external action or legal certification is emitted.

## 12. Proof boundary
`P-EW03_PASS != CUSTOMER_DEMAND`

`P-EW03_PASS != WTP`

`P-EW03_PASS != LEGAL_CLEARANCE`

`P-EW03_PASS != CERTIFICATION`

`P-EW03_PASS != PROFITABILITY`
