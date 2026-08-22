# P-EW07 — DOCLANG FIDELITY REGRESSION PROOF CONTRACT

**Date:** 2026-08-22  
**Status:** INTERNAL PUBLIC/MINIMAL-FIXTURE PROOF / NO WIP PROMOTION / NO EXTERNAL ACTION

Parent decision:
- `29_EARLY_WAVE_REMAINING5_RED_TEAM_2026-08-22.md`
- `30_EARLY_WAVE_REMAINING5_RED_TEAM_STATE.json`

## Question
Can a DocLang document remain structurally valid under the official reference validator while still containing a conversion-fidelity defect that changes source text?

This deliberately separates two contracts:
1. **DocLang structural conformance** — official DocLang XSD/reference toolkit;
2. **source-to-output fidelity** — independent invariant comparing source truth to converted semantic text.

`SCHEMA_VALID != SEMANTICALLY_FAITHFUL`
`PUBLIC_BUG_CLASS != PREVALENCE`
`FIDELITY_PROOF != BUYER_DEMAND`

## Public basis
The DocLang project publishes the normative specification and reference toolkit including XSD/Schematron validation. Docling already supports DocLang as input/output.

Public July 2026 Docling issues report conversion defects including:
- PDF->DocLang syntax trouble involving an ampersand in ordinary text;
- a poetic text line misclassified as a formula, with downstream schema/chunking failure until required text is restored.

Sources:
- https://github.com/doclang-project/doclang
- https://github.com/doclang-project/doclang/blob/main/doclang/README.md
- https://docling-project.github.io/docling/usage/supported_formats/
- https://github.com/docling-project/docling/issues/3864
- https://github.com/docling-project/docling/issues/3780

## Official structural fixture basis
The XML shape is derived from the official DocLang `examples/archive-demo/document.xml` reference example.

Two test documents use the same valid DocLang structure:
- `good.dclg.xml` preserves logical source text `Peter Thomas & Christian Johnston` (encoded in XML as `&amp;`);
- `semantic_drift.dclg.xml` changes the logical text to `Peter Thomas and Christian Johnston` while keeping the same DocLang structure.

The expected source truth is stored separately in `01_SOURCE_TRUTH.json`.

## Predeclared proof
The proof passes only if:
1. the official pinned DocLang reference toolkit accepts **both** XML files under XSD validation;
2. our independent fidelity checker passes `good.dclg.xml`;
3. the same checker fails `semantic_drift.dclg.xml` for a content mismatch;
4. the fidelity result does not depend on treating the drifted XML as structurally invalid.

If the official validator rejects the drift fixture, this exact test does not establish orthogonality and must be repaired or classified HOLD.

## What this can prove
At most:
`PASS_MECHANISM_ORTHOGONAL_TO_SCHEMA`

It can show there exists a class of structurally valid semantic drift that a schema validator cannot detect because both strings are legal document content.

It cannot prove:
- prevalence in production DocLang pipelines;
- buyer pain;
- WTP;
- superiority over existing document QA products;
- that the public issue itself produces this exact fixture.

## Commercial overlap gate
Even if the mechanism passes, generic DocLang conversion/validation remains killed. A future wedge survives only as:
`INDEPENDENT_CONVERSION_FIDELITY_REGRESSION_QA_M1_ONLY`

Before any promotion, evidence would still be needed that document-AI/RAG teams experience costly fidelity regressions not adequately caught by converter-native tests.

## Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`
