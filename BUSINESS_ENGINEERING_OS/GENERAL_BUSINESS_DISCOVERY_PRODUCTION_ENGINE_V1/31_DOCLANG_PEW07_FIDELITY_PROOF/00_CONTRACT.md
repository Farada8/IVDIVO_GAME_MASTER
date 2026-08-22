# P-EW07 — DOCLANG FIDELITY REGRESSION PROOF CONTRACT

**Date:** 2026-08-22  
**Status:** INTERNAL BOUNDED PROOF / NO WIP PROMOTION / NO EXTERNAL ACTION

Parent decision:
- `29_EARLY_WAVE_REMAINING5_RED_TEAM_2026-08-22.md`
- `30_EARLY_WAVE_REMAINING5_RED_TEAM_STATE.json`

## Question
Does the current Docling -> DocLang -> Docling round-trip create measurable semantic/structural loss on a bounded stress fixture, independently of DocLang XSD validity?

Two separate proofs are required and must not be conflated:
1. **Orthogonality control:** a manually drifted but schema-valid DocLang document proves only `SCHEMA_VALID != SOURCE_FAITHFUL`.
2. **Real converter round-trip:** current pinned Docling generates DocLang from a source document, re-imports it, and compares bounded semantic/structural invariants against the pre-DocLang DoclingDocument baseline.

`SCHEMA_VALID != SEMANTICALLY_FAITHFUL`
`MANUALLY_INJECTED_DRIFT != CONVERTER_GENERATED_LOSS`
`PUBLIC_BUG_CLASS != CURRENT_REPRODUCTION`
`TECHNICAL_GAP != BUYER_DEMAND`

## Public basis
Current Docling documentation states:
- Docling JSON is the lossless serialization of a DoclingDocument;
- DocLang XML is a supported output serialization;
- DocLang XML is also a supported input format;
- DocLang preserves table spans using OTSL continuation tokens.

Current pinned runtime for the real test: `docling==2.121.0` (released 2026-08-20).
Official structural validator remains pinned at `doclang==0.7.0`.

Public issue history establishes that DocLang/conversion fidelity defects are plausible, not that this fixture currently reproduces them:
- issue #3864: PDF -> DocLang ampersand/syntax failure on Docling 2.87.1;
- issue #3780: poetic line misclassified as formula with missing required text in exported structured data.

Sources:
- https://docling-project.github.io/docling/usage/supported_formats/
- https://docling-project.github.io/docling/concepts/serialization/
- https://docling-project.github.io/docling/reference/docling_document/
- https://github.com/docling-project/docling/issues/3864
- https://github.com/docling-project/docling/issues/3780
- https://pypi.org/project/docling/

## A — orthogonality control
The existing pair remains intentionally synthetic:
- `good.dclg.xml` preserves logical source text `Peter Thomas & Christian Johnston`;
- `semantic_drift.dclg.xml` manually changes it to `Peter Thomas and Christian Johnston` while remaining structurally valid.

This may conclude at most:
`PASS_ORTHOGONALITY_CONTROL`

It is forbidden to relabel this pair as a real converter defect.

## B — real converter-generated round-trip
Input:
`fixtures/roundtrip_stress.html`

Path:
`HTML SOURCE -> DOCLING DOCUMENT -> LOSSLESS JSON BASELINE + DOCLANG XML -> DOCLANG RE-IMPORT -> DOCLING DOCUMENT`

The stress fixture includes:
- XML-sensitive ampersands and angle-bracket text;
- Unicode / punctuation / currency;
- headings and ordered-list structure;
- a table containing colspan and rowspan;
- code-like text with `<`, `>`, `&&`, quotes and ampersands.

The independent signature compares only bounded semantics that matter downstream:
- reading-order item type;
- item label;
- hierarchy level;
- logical text;
- table dimensions;
- table cell text and row/column span coordinates.

Volatile source provenance/hashes and source-specific geometry are deliberately excluded.

## Data-dependent result
There is no predeclared requirement that the converter must fail.

If generated DocLang passes official XSD and one or more bounded semantic/structural invariants change after re-import:
`PASS_REAL_FIDELITY_GAP_TECHNICAL_ONLY`

If generated DocLang passes official XSD and all bounded invariants survive:
`HOLD_NO_REAL_GAP_IN_BOUNDED_FIXTURES`

If conversion/re-import/XSD validation cannot complete deterministically:
`HOLD_TEST_INFRASTRUCTURE_OR_COMPATIBILITY_FAILURE`

A green CI run means the experiment executed under its declared boundary; it does **not** mean a market gap was found.

## Commercial overlap gate
Regardless of technical result:
- generic DocLang conversion remains killed;
- generic schema/XSD validation remains killed;
- no DocLang product is promoted into WIP;
- any surviving hypothesis is only `INDEPENDENT_CONVERSION_FIDELITY_REGRESSION_QA_M1_ONLY` and still requires real external evidence of costly regressions not already handled by converter-native tests.

## Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`
