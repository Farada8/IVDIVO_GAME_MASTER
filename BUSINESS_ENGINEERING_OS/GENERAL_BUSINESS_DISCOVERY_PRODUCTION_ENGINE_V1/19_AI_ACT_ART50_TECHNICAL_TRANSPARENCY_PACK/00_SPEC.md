# P-EW03 — AI ACT ARTICLE 50 TECHNICAL TRANSPARENCY PACK v0.1

**Date:** 2026-08-22  
**Lane:** `CF-01 AI Act Article 50 Technical Transparency Pack`  
**Parent authority:** `16_EARLY_WAVE_RADAR_STATE.json`  
**Status:** INTERNAL ENGINEERING SAMPLE / REGULATORY DRIFT PATCH / NOT LEGAL ADVICE / NO COMPLIANCE CERTIFICATION

## 1. Purpose
Compile a concrete Article 50 implementation packet from role + use case + evidence, rather than selling generic “AI compliance consulting”.

Pipeline:
`ROLE -> SYSTEM/CONTENT USE -> ARTICLE 50 ROUTE -> EXCEPTION/SPECIAL/TRANSITION REGIME -> CONTROL OBJECT -> EVIDENCE OBJECT -> UNRESOLVED ITEM -> REVIEW`

## 2. Current legal/source baseline
Article 50 obligations generally apply from **2 August 2026**. The Commission published final Article 50 implementation Guidelines on 20 July 2026 and the final Code of Practice on Transparency of AI-generated Content in June 2026. In July 2026 the Commission and AI Board assessed the Code as an adequate voluntary tool for Articles 50(2), (4) and (5). Adherence is voluntary and is not conclusive evidence of compliance.

**Regulation (EU) 2026/1744** adds one narrow transition: providers of AI systems, including GPAI systems, generating synthetic audio, image, video or text content **placed on the market before 2 August 2026** must take the necessary steps to comply with **Article 50(2) by 2 December 2026**. This is not an exemption, not a general Article 50 grace period, and does not defer Article 50(1), (3), or (4).

This pack therefore separates:
- statutory obligation;
- binding transition deadline;
- Commission guideline/Q&A interpretation;
- voluntary Code route;
- organisation-specific implementation evidence;
- unresolved legal judgement.

## 3. Core laws
`ROLE_UNKNOWN -> HOLD_SCOPE`

`PROVIDER_OBLIGATION != DEPLOYER_OBLIGATION`

`A50_2_TRANSITION != A50_2_EXEMPTION`

`A50_2_TRANSITION != GENERAL_ARTICLE50_GRACE_PERIOD`

`LEGACY_MARKET_PLACEMENT_CLAIM_WITHOUT_DATE_EVIDENCE -> UNKNOWN`

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

#### A50-2 transitional route — Regulation (EU) 2026/1744
The router may emit `APPLIES_TRANSITIONAL_DEADLINE` only when all of the following are evidenced:
1. actor is a provider;
2. the system generates synthetic audio/image/video/text within the A50-2 route;
3. the system was placed on the market before `2026-08-02`;
4. an explicit assessment date is supplied and is before `2026-12-02`;
5. no separate scope exception has already forced review.

Required evidence includes `LegacyMarketPlacementEvidence`, `TransitionRemediationPlan`, and `MachineReadableMarkingEvidenceBy2026_12_02`.

At or after `2026-12-02`, the transition no longer changes the routing state and ordinary A50-2 implementation evidence is required. If legacy market placement is claimed but assessment date is absent, the router fails closed to `UNKNOWN` rather than silently granting extra time.

Evidence object: `MachineReadableMarkingEvidence` plus transition evidence where applicable.

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

For transition claims also bind:
- market-placement date/source;
- assessment date;
- transition deadline;
- remediation owner and plan;
- evidence expected by the deadline.

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

## 8. Exception/special/transition object
No exception or transition is accepted from an unlabeled boolean alone. Store:
- candidate route;
- exact facts;
- legal/guideline source;
- cumulative conditions;
- reviewer;
- decision: `CONFIRMED`, `REJECTED`, `PENDING_REVIEW`, or `TRANSITION_ACTIVE`;
- deadline/expiry/review trigger.

Sensitive examples:
- “obvious AI interaction” -> restrictive review;
- standard editing / machine-only / closed-loop output -> scope review;
- creative deepfake -> special disclosure regime, not automatic exemption;
- public-interest text -> human review/editorial control plus editorial responsibility must both be evidenced;
- pre-2-August market placement -> narrow A50-2 transition only, never a blanket Article 50 delay.

## 9. Voluntary Code route
`code_adherence` accepts `SIGNED`, `NOT_SIGNED`, `UNKNOWN`.

- `SIGNED`: map evidence to relevant Code section/commitments; still no automatic compliance claim.
- `NOT_SIGNED`: require an alternative-measures evidence map; do not classify as non-compliant solely because the Code was not signed.
- `UNKNOWN`: hold Code-route claim.

## 10. P-EW03 synthetic sample
The original sample packet contains six synthetic cases designed to exercise the main substantive routes. The regulatory-drift regression adds derived transition variants in tests without rewriting the frozen six-case packet:
1. provider chatbot, non-obvious direct interaction;
2. provider generative image/text system;
3. deployer emotion-recognition system;
4. deployer deepfake marketing video;
5. deployer public-interest AI text without editorial exception;
6. same public-interest text with documented human review/editorial control + editorial responsibility.

Derived transition canaries test pre-deadline, deadline-expired, and missing-assessment-date states. No synthetic case is presented as evidence about a real customer.

## 11. Acceptance
P-EW03 remains engineering-only and passes the drift regression only if:
- provider/deployer roles stay distinct;
- all Article 50 branches route deterministically;
- the A50-2 transition is bounded to pre-2-August market placement and pre-2-December assessment;
- transition is never converted into exemption/compliance proof;
- uncertain transition facts fail closed;
- uncertain exceptions fail closed;
- creative deepfake stays disclosure-bound;
- public-interest text exception requires both review/control and editorial responsibility;
- Article 50(5) attachment remains deterministic under applicable routes;
- Code adherence does not become a compliance shortcut;
- sample evidence clearly separates `DESIGN_ONLY` from implemented/tested;
- no external action or legal certification is emitted.

## 12. Proof boundary
`P-EW03_PASS != CUSTOMER_DEMAND`

`P-EW03_PASS != WTP`

`P-EW03_PASS != LEGAL_CLEARANCE`

`P-EW03_PASS != CERTIFICATION`

`TRANSITION_ROUTE != COMPLIANCE_PROOF`

`P-EW03_PASS != PROFITABILITY`

READBACK_MARKER: `PEW03-ARTICLE50-OMNIBUS-TRANSITION-PATCH-NO-MARKET-PROMOTION-20260822`
