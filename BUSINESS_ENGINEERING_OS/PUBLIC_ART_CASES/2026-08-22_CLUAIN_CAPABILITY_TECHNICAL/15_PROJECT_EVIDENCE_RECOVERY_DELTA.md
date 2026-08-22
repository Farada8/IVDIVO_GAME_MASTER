# PAC8 — PROJECT EVIDENCE RECOVERY DELTA

**Date:** 2026-08-22  
**Scope:** Clúain na Coillte prior-work evidence recovery only.  
**Authority effect:** additive evidence; does not authorize submission or change Business Engineering market proof.

## Result
Persistent evidence supports stronger provenance for two previously weakly identified camera-photo files and one additional selected-work object. The recovery improves artistic/professional evidence but **does not close Roscommon's three-project requirement** because project-level budget, delivery context and/or timeframe remain missing for most objects.

`THREE_PROJECT_EVIDENCE_PACK = HOLD_CURABLE_PROJECT_LEVEL_PROVENANCE`

## PE-01 — Guelder Rose Paths / Калинові шляхи
**Classification:** `CLASS_B_DOCUMENTED_PROFESSIONAL_WORK`  
**Identity confidence:** HIGH.

Documented:
- archival artist name: Yaroslav Zadvornyi / Ярослав Задворний;
- current professional name continuity: Yaromyr Farada;
- title: `Guelder Rose Paths (Kalynovi shliakhy)`;
- year: 2011;
- medium: board, ivory ground, oil;
- dimensions: 49 × 91 cm;
- context: Fine Art Ukraine 2011, Mystetskyi Arsenal, Kyiv;
- catalogue: p. 140;
- surviving direct artwork photograph: `495186926_2821173898270473_1658099110807270165_n.jpg`;
- catalogue-page photograph: `photo_2026-08-10_15-04-39.jpg`.

Still UNKNOWN / not claimed: overall project budget, commissioning client, public-art delivery contract, community-engagement process, project-management/maintenance scope.

**Roscommon use:** strong artistic-quality/professional-record evidence, not a Class-A public-art delivery case.

## PE-02 — Ukraine (diptych; working title)
**Classification:** `CLASS_B_SELECTED_PORTFOLIO_WORK`.

Documented:
- RHA selected-work title: `Ukraine (diptych; working title)`;
- medium: oil on canvas, diptych;
- full surviving image: `498514436_2834382206949642_773398228116738999_n.jpg`;
- detail image: `494666738_2821156808272182_1288430423051351283_n.jpg`;
- RHA application reproduces the same two-panel composition as Selected Work 6.

Still UNKNOWN / not claimed: original title beyond working title, date, dimensions, client/context, overall budget, public-art delivery, community-engagement/project-management/maintenance scope.

## PE-03 — Untitled — historical composition
**Classification:** `CLASS_C_SELECTED_WORK_WITH_PARTIAL_METADATA`.

Documented: RHA selected-work label; prepared panel, oil, gilding / mixed media; artwork image is reproduced as Selected Work 2 in the RHA complete application.

Still UNKNOWN / not claimed: date, dimensions, client/context, overall budget, commission/public-art status, community-engagement/project-management/maintenance scope.

## Professional-context evidence retained separately
Stored CV / application evidence supports professional monumental/decorative-art practice, Steel Art Studio (2003–2010), Bureau of Monumental Art / National Union of Artists of Ukraine (2009–2017), earlier private Kyiv wall-painting/mural/site-specific practice, and archive loss. This **must not be converted into named completed commissions** without project-level provenance.

## Evidence-completeness contract
A Roscommon prior-project object is `CLASS_A_SUBMISSION_READY` only when documentary evidence supports:
1. distinct project/work identity;
2. relevant context/client/venue;
3. timeframe;
4. overall budget or an explicit authority-bound acceptable N/A basis;
5. photographs/work images;
6. applicant role;
7. enough delivery context to support the claimed relevant experience.

Missing values remain `UNKNOWN`.

## Case-scoped engineering rules
- `IMAGE_SIMILARITY_NEQ_PROJECT_IDENTITY_WITHOUT_DOCUMENT_BINDING`
- `PORTFOLIO_WORK_NEQ_PUBLIC_ART_DELIVERY_CASE`
- `EMPLOYMENT_HISTORY_NEQ_THREE_NAMED_PROJECTS`
- `UNKNOWN_PROJECT_BUDGET_STAYS_UNKNOWN`
- `WORKING_TITLE_MUST_REMAIN_LABELED_WORKING_TITLE`
- `ARCHIVE_LOSS_EXPLAINS_GAP_BUT_DOES_NOT_PROVE_MISSING_FIELDS`

## Current decision
`GO_TO_SUBMIT = false`.

Current causal gate:
`RECOVER_3_PROJECT_RECORDS_WITH_REQUIRED_FIELDS -> CLUAIN_SPECIFIC_VISUALS -> FINAL_CRITERIA_READBACK -> SUBMIT_OR_HOLD`.

## Highest-value next evidence actions
1. Search surviving social/cloud/email/catalogue records for captions, venue, year and project context.
2. Recover invoices/quotes/contracts/project sheets that can bind actual project budgets.
3. Recover named Steel Art / Bureau / private-commission projects only where project-level provenance exists.
4. Do not substitute submission polish for missing evidence.
