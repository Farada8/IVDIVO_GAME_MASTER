# PAC8 — PROJECT EVIDENCE RECOVERY DELTA

**Date:** 2026-08-22  
**Scope:** Clúain na Coillte prior-work evidence recovery only.  
**Authority effect:** additive evidence; does not authorize submission or change Business Engineering market proof.

## Result
The persistent File Library now supports stronger provenance for two previously weakly identified camera-photo files and one additional selected-work object. The recovery improves artistic/professional evidence but **does not close Roscommon's three-project requirement** because project-level budget, delivery context and/or timeframe remain missing for most objects.

`THREE_PROJECT_EVIDENCE_PACK = HOLD_CURABLE_PROJECT_LEVEL_PROVENANCE`

## Object PE-01 — Guelder Rose Paths / Калинові шляхи
**Classification:** CLASS_B_DOCUMENTED_PROFESSIONAL_WORK  
**Identity confidence:** HIGH.

Documented facts:
- archival artist name: Yaroslav Zadvornyi / Ярослав Задворний;
- current professional name continuity: Yaromyr Farada;
- title: `Guelder Rose Paths (Kalynovi shliakhy)`;
- year: `2011`;
- medium: board, ivory ground, oil;
- dimensions: `49 × 91 cm`;
- context: `Fine Art Ukraine 2011`, Mystetskyi Arsenal, Kyiv;
- catalogue: p. 140;
- surviving direct artwork photograph: `495186926_2821173898270473_1658099110807270165_n.jpg`;
- independent catalogue-page photograph: `photo_2026-08-10_15-04-39.jpg`;
- the direct artwork image and catalogue reproduction depict the same composition.

Still unknown / not claimed:
- overall project budget;
- commissioning client;
- public-art delivery contract;
- community-engagement process;
- project-management/maintenance scope.

**Roscommon use:** strong artistic-quality/professional-record evidence. Not a full Class-A public-art delivery case while budget/project-delivery fields remain unknown.

## Object PE-02 — Ukraine (diptych; working title)
**Classification:** CLASS_B_SELECTED_PORTFOLIO_WORK  
**Identity confidence:** HIGH for image↔RHA-list mapping.

Documented facts:
- RHA selected-work title: `Ukraine (diptych; working title)`;
- medium: oil on canvas, diptych;
- full surviving image: `498514436_2834382206949642_773398228116738999_n.jpg`;
- surviving detail image: `494666738_2821156808272182_1288430423051351283_n.jpg`;
- the detail image is visibly a crop/detail of the left panel of the full diptych;
- the RHA application reproduces the same two-panel composition as Selected Work 6.

Still unknown / not claimed:
- original title beyond working title;
- date;
- dimensions;
- client/context;
- overall budget;
- public-art delivery status;
- community-engagement/project-management/maintenance scope.

**Roscommon use:** portfolio-quality evidence only. Does not independently satisfy the requested project-case fields.

## Object PE-03 — Untitled — historical composition
**Classification:** CLASS_C_SELECTED_WORK_WITH_PARTIAL_METADATA  
**Identity confidence:** HIGH within RHA selected-work pack.

Documented facts:
- RHA selected-work label: `Untitled — historical composition`;
- medium: prepared panel, oil, gilding / mixed media;
- artwork image is reproduced as Selected Work 2 in the RHA complete application.

Still unknown / not claimed:
- date;
- dimensions;
- client/context;
- overall budget;
- commission/public-art status;
- community-engagement/project-management/maintenance scope.

**Roscommon use:** supporting artistic-practice evidence, not a qualifying Class-A project record.

## Professional-context evidence retained separately
The stored CV / Shillelagh application supports:
- professional monumental/decorative-art practice;
- Steel Art Studio, Kyiv, 2003–2010: artistic development/production and team coordination for decorative/architectural projects;
- Bureau of Monumental Art, National Union of Artists of Ukraine, 2009–2017: coordination/development of monumental and decorative art projects;
- earlier private Kyiv interior wall paintings, decorative murals and site-specific compositions;
- documented loss of a substantial part of the earlier mural photographic archive during the war.

This **must not be converted into named completed commissions** without project-level provenance.

## Evidence-completeness rule
A Roscommon prior-project object is `CLASS_A_SUBMISSION_READY` only if documentary evidence supports, at minimum:
1. distinct work/project identity;
2. relevant context/client/venue;
3. timeframe;
4. overall budget or an explicit authoritative `NOT_APPLICABLE/NOT_RECORDED` basis acceptable under the brief;
5. photographs/work images;
6. applicant role;
7. enough delivery context to support claims about relevant experience.

Missing fields remain `UNKNOWN`; they are not repaired by CV-level employment history, stylistic similarity, AI imagery or memory alone.

## New case-scoped engineering rules
- `IMAGE_SIMILARITY_NEQ_PROJECT_IDENTITY_WITHOUT_DOCUMENT_BINDING`
- `PORTFOLIO_WORK_NEQ_PUBLIC_ART_DELIVERY_CASE`
- `EMPLOYMENT_HISTORY_NEQ_THREE_NAMED_PROJECTS`
- `UNKNOWN_PROJECT_BUDGET_STAYS_UNKNOWN`
- `WORKING_TITLE_MUST_REMAIN_LABELED_WORKING_TITLE`
- `ARCHIVE_LOSS_EXPLAINS_GAP_BUT_DOES_NOT_PROVE_MISSING_FIELDS`

## Current decision
`GO_TO_SUBMIT = false`.

The evidence recovery improved N1 materially but does not clear the primary Red-Team hold. Current causal gate remains:

`RECOVER_3_PROJECT_RECORDS_WITH_REQUIRED_FIELDS -> CLUAIN_SPECIFIC_VISUALS -> FINAL_CRITERIA_READBACK -> SUBMIT_OR_HOLD`.

## Highest-value next evidence actions
1. Search surviving social/cloud/email/catalogue records around the known camera-photo cluster for captions, venue, year and project context.
2. Recover any invoice/quote/contract/project sheet that can provide a real overall budget for a completed work.
3. Recover one or more named Steel Art / Bureau / private-commission projects only where project-level provenance exists.
4. Do not spend more time polishing the submission until at least three project objects meet the brief's mandatory evidence fields or the brief is re-read and shown to permit an alternative evidence format.
