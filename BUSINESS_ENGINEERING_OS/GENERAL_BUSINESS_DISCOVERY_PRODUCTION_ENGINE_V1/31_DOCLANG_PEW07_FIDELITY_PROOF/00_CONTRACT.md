# P-EW07 — DOCLANG FIDELITY REGRESSION PROOF CONTRACT

**Date:** 2026-08-22  
**Status:** INTERNAL PUBLIC/MINIMAL-FIXTURE PROOF / NO WIP PROMOTION / NO EXTERNAL ACTION  
**Fresh replay:** unique contract salvaged from stale branch `business-engineering/pew07-doclang-fidelity-proof-20260822`; no duplicate execution count.

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
The DocLang project publishes the normative specification and reference toolkit including XSD/Schematron validation. The official toolkit README documents `doclang validate`, including `--xsd-only`. Current project metadata on the inspected main branch reports toolkit version `0.7.3`.

Public July 2026 Docling issues report conversion defects including:
- issue #3864: PDF->DocLang syntax trouble involving an ampersand in ordinary text; issue is closed and is used only as a disclosed failure class, not as evidence of current prevalence;
- issue #3780: a poetic text line misclassified as a formula, with missing text and downstream schema/chunking failure; the issue was open when inspected on 2026-08-22.

Sources are recorded in `02_SOURCE_LEDGER.md`.

## Official structural fixture basis
The XML shape is a minimal DocLang document in the official namespace and is intentionally separated from source truth.

Two test documents use the same DocLang structure:
- `good.dclg.xml` preserves logical source text `Peter Thomas & Christian Johnston` (encoded in XML as `&amp;`);
- `semantic_drift.dclg.xml` changes the logical text to `Peter Thomas and Christian Johnston` while keeping the same DocLang structure.

The expected source truth is stored separately in `01_SOURCE_TRUTH.json`.

## Predeclared proof
The proof passes only if:
1. the official pinned DocLang reference toolkit accepts **both** XML files under XSD validation;
2. our independent fidelity checker passes `good.dclg.xml`;
3. the same checker fails `semantic_drift.dclg.xml` for a content mismatch;
4. the fidelity result does not depend on treating the drifted XML as structurally invalid;
5. UNKNOWN/missing source-truth inputs fail closed rather than being converted into PASS.

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
- that the public issue itself produces this exact fixture;
- current Docling defect rates;
- converter quality in general.

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
