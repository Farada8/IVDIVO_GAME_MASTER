# BOOK INTELLIGENCE ENGINE — DEEP SOURCE PASS
## NASA Systems Engineering Handbook — v1.0

**Date:** 2026-08-22  
**Source ID:** `OPEN-NASA-SE-HANDBOOK`  
**Document:** NASA/SP-2016-6105 Rev 2, *NASA Systems Engineering Handbook*  
**Official source:** NASA / NASA Technical Reports Server  
**Rights:** public distribution / public use permitted; third-party notices still require care for redistribution of included assets  
**Lifecycle result:** `MECHANISMS_EXTRACTED` for the inspected sections; **NOT FULL_READ** and not whole-book synthesized.

## Integrity / access
- Official NASA PDF inspected directly from nasa.gov.
- NASA NTRS record identifies document 20170001761 and `NASA/SP-2016-6105 Rev 2`.
- The book is 297 PDF pages.
- Binary transfer into the current model runtime failed through the available download channel; no claim is made that the raw PDF was copied into Drive.
- Official web source remains the source locator.

## Structure map
The inspected table of contents establishes these major layers:
1. Introduction.
2. Fundamentals of Systems Engineering.
3. NASA Program/Project Life Cycle.
4. System Design Processes.
5. Product Realization.
6. Crosscutting Technical Management.

High-value sections for Book Intelligence:
- §2.4 distinctions between Product Verification and Product Validation;
- §5.3 Product Verification;
- §5.4 Product Validation;
- §6.2 Requirements Management;
- §6.4 Technical Risk Management;
- §6.5 Configuration Management;
- §6.6 Technical Data Management;
- §6.7 Technical Assessment;
- §6.8 Decision Analysis;
- Appendix D Requirements Verification Matrix;
- Appendix E Validation Requirements Matrix;
- Appendix I Verification and Validation Plan Outline.

## Claim cards

### NASA-C01 — Verification and validation are distinct evidence questions
**Locator:** PDF p.97 (printed handbook p.88), §5.3 opening.  
**Claim type:** NORMATIVE / FORMAL PROCESS DISTINCTION.  
**Abstracted claim:** Verification asks whether the realized product conforms to requirements/specifications; validation asks whether the realized product is the right product for intended use/customer expectations. Similar methods do not make the evidence questions interchangeable.

**IVDIVO consequence:**
`ENGINEERING_TEST_PASS != REAL_PROJECT_VALIDATION`.

Automated/unit/contract tests can prove implementation conformance; they cannot alone prove project usefulness, human quality, provider performance or market value.

### NASA-C02 — Requirements need bidirectional traceability
**Locator:** PDF pp.139–141, §6.2 Requirements Management.  
**Claim type:** NORMATIVE PROCESS CONTROL.  
**Abstracted claim:** Requirements management identifies/controls/decomposes/allocates requirements, maintains bidirectional traceability, manages baseline changes, and connects requirements to design/test artifacts.

**IVDIVO consequence:**
Book-derived changes require a traversable chain both forward and backward:
`SOURCE -> CLAIM -> MECHANISM -> ADAPTER -> PROJECT APPLICATION -> TEST -> RESULT -> LEARNING/RULE`.
A rule must be traceable back to source/evidence; a source claim must be traceable forward to what it actually changed.

### NASA-C03 — Assessment outputs must preserve rationale and assumptions
**Locator:** PDF pp.166–169, §6.7 Technical Assessment.  
**Claim type:** NORMATIVE PROCESS CONTROL.  
**Abstracted claim:** Periodic technical assessment uses defined measures and should capture findings, recommendations, key decisions, supporting rationale, assumptions and lessons learned.

**IVDIVO consequence:**
A `PASS` label without decision rationale, assumptions, evidence class and artifact locator is insufficient for reusable learning.

### NASA-C04 — Decision analysis starts from the decision and criteria
**Locator:** PDF pp.169–176, §6.8 Decision Analysis.  
**Claim type:** NORMATIVE DECISION PROCESS.  
**Abstracted claim:** Decision analysis begins by defining the decision and intended outcome, then decision criteria, alternatives, evaluation methods/results and the final recommendation/decision; rigor is tailored to complexity, uncertainty and stakes.

**IVDIVO consequence:**
Research depth and prompt depth must be proportional to the decision. Do not full-read a library merely because sources exist. Define the decision first, then retrieve only evidence capable of changing it.

### NASA-C05 — Replanning is triggered by assessment/risk/decision results
**Locator:** PDF pp.124–125, §6.1 Technical Planning.  
**Claim type:** NORMATIVE FEEDBACK LOOP.  
**Abstracted claim:** Technical planning is updated based on assessment, risk and decision-analysis results rather than treated as a one-time plan.

**IVDIVO consequence:**
Engine plans are baselines, not scripture. Observed failure/success can trigger bounded change, but change must be impact-assessed and written through controlling state.

## Mechanism cards

### BI-NASA-M01 — VERIFY_VALIDATE_SPLIT
**Statement:** Separate conformance evidence from intended-use/outcome evidence; never promote a mechanism because implementation tests passed if real-project validation is absent.
**Failure modes:** test-count theater; CI success misreported as product quality; simulated user/market evidence; dry-run/provider substitution.
**Targets:** SELF_IMPROVEMENT, OPERATIONS, STORY, AUDIO, BUSINESS, GENERAL.
**Disposition:** PILOT_READY after implementation regression.

### BI-NASA-M02 — BIDIRECTIONAL_TRACEABILITY_GRAPH
**Statement:** Any reusable rule or promoted mechanism must trace backward to source/claim/evidence and forward to its application/test/result; unresolved orphan nodes fail promotion closed.
**Failure modes:** orphan rules; stale superseded evidence; source cited but never applied; result claimed with no source/mechanism lineage; duplicate parallel authority.
**Targets:** SELF_IMPROVEMENT, OPERATIONS, GENERAL.
**Disposition:** PILOT_READY after runtime implementation tests.

### BI-NASA-M03 — CHANGE_IMPACT_SET
**Statement:** Before changing a baseline mechanism/contract, compute downstream descendants and affected project/router/test surfaces; do not assume a local edit is local.
**Failure modes:** stale routers; partial write-through; project-state mismatch; hidden regression; sibling-dialog overwrite.
**Targets:** SELF_IMPROVEMENT, OPERATIONS, GENERAL.
**Disposition:** LOCAL_TEST.

### BI-NASA-M04 — DECISION_FIRST_RESEARCH_DEPTH
**Statement:** Define decision, criteria, alternatives, uncertainty and stakes before choosing research depth; use targeted retrieval when another source is less informative than a pilot.
**Failure modes:** whole-library reread; prompt proliferation; research without decision; false precision; ceremonial documentation.
**Targets:** RESEARCH, SELF_IMPROVEMENT, BUSINESS, STORY, AUDIO, GENERAL.
**Disposition:** already compatible with current Book Intelligence retrieval law; treat as cross-source reinforcement, not a new top-level engine.

## Contradiction / compatibility check
NASA uses mission/program engineering vocabulary and formal review processes. IVDIVO is not a spacecraft program. Transfer only the abstract control mechanisms, not NASA-specific bureaucracy.

Compatibility with current IVDIVO law:
- `VERIFY_SEPARATE_FROM_VALIDATE` already exists conceptually -> NASA gives stronger provenance and schema pressure.
- current provenance edges already form a forward chain -> NASA adds an explicit **bidirectional audit** requirement.
- current stale-write/rebase rule already protects concurrent changes -> `CHANGE_IMPACT_SET` adds systematic descendant discovery before writes.
- current problem-targeted retrieval already defines bounded research -> NASA Decision Analysis independently reinforces decision-first depth.

## Implementation authorization
Authorized bounded upgrade:
1. Add evidence-class distinction to pilot evidence.
2. Add `TraceabilityBundle` schema.
3. Add runtime `audit_traceability_bundle()`.
4. Add runtime `change_impact_set()`.
5. Promotion must ignore engineering verification as a substitute for real-project validation.
6. Preserve backward compatibility by classifying legacy pilot evidence explicitly rather than silently treating unknown evidence as validation.
7. Add regression fixtures for complete chain, orphan node, broken edge, missing real validation and impact propagation.

## What this pass does NOT prove
- It is not a cover-to-cover full read.
- It does not prove NASA process is optimal for every IVDIVO domain.
- It does not promote NASA terminology into creative/business canon.
- It does not prove the proposed runtime upgrade is better until tests and project pilots pass.

## Next gate
Implement the bounded traceability + V/V split upgrade, run deterministic regression, then apply it to the already-completed Pilot 1 and Pilot 2 evidence packages. If it exposes no lineage break and correctly refuses to count engineering-only evidence as validation, mark the upgrade `ENGINEERING_PASS / PROJECT_VALIDATION_PENDING`.