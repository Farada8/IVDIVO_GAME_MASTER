# P-EW08 — DOCLANG REAL ROUND-TRIP FIDELITY / COMPATIBILITY GATE

**Date:** 2026-08-22
**Status:** INTERNAL FALSIFICATION PROOF / NO WIP PROMOTION / NO EXTERNAL ACTION

## Why this gate exists
Controlling P-EW07 (PR #447) correctly proved only that DocLang XSD structural validity and source-fidelity are different verification planes. It did not run Docling conversion and therefore did not establish a real current converter-generated fidelity defect.

`P-EW07 = PASS_ORTHOGONALITY_CONTROL_ONLY`
`MANUAL_DRIFT != CONVERTER_GENERATED_LOSS`

P-EW08 is the smallest correction gate that executes the current converter path.

## Runtime pins
- `docling==2.121.0` — current PyPI release observed 2026-08-22, released 2026-08-20.
- `doclang==0.7.3` — current official DocLang toolkit used by controlling P-EW07.
- Python 3.12.

## Public basis
Current Docling documentation states:
- Docling JSON is lossless serialization of `DoclingDocument`;
- DocLang XML is a supported output format;
- DocLang XML is a supported input format;
- DocLang preserves table row/column spans using OTSL continuation tokens.

Public issue history proves that document conversion/serialization defects are plausible, but does not predeclare this run's result:
- Docling #3864: disclosed PDF->DocLang ampersand/syntax problem on an older runtime;
- Docling #3780: disclosed text-loss / misclassification path in structured output.

## Real path under test
`HTML SOURCE -> DOCLING DOCUMENT -> LOSSLESS JSON BASELINE + DOCLANG XML -> OFFICIAL DOCLANG XSD -> DOCLANG RE-IMPORT -> DOCLING DOCUMENT`

The HTML stress fixture contains:
- ampersands and angle-bracket literals;
- Unicode, punctuation and currency;
- heading hierarchy;
- ordered list;
- table with colspan + rowspan;
- code-like text containing `<`, `>`, `&&`, quotes and ampersands.

## Bounded invariants
The comparison deliberately excludes volatile source hashes, provenance and source-specific geometry. It compares:
1. reading-order item type;
2. item label;
3. hierarchy level;
4. logical text;
5. group name when present;
6. table dimensions;
7. table-cell logical text;
8. row/column span coordinates.

## Data-dependent routes
No failure is predeclared.

### A — producer / validator incompatibility
If current Docling emits DocLang that current official DocLang XSD rejects:
`PASS_REAL_STRUCTURAL_COMPATIBILITY_GAP_TECHNICAL_ONLY`

### B — schema-valid semantic/structural loss
If XSD accepts generated DocLang, re-import completes, and one or more bounded invariants change:
`PASS_REAL_FIDELITY_GAP_TECHNICAL_ONLY`

### C — bounded fixtures survive
If XSD accepts generated DocLang and all bounded invariants survive:
`HOLD_NO_REAL_GAP_IN_BOUNDED_FIXTURES`

### D — test infrastructure cannot execute
If source conversion / export / re-import cannot execute because of environment/API/runtime failure unrelated to the measured DocLang path:
`HOLD_TEST_INFRASTRUCTURE_FAILURE`

A green CI means only that the experiment executed and classified itself under this contract. Green does not mean a gap was found.

## Commercial boundary
Whatever the technical route:
- `GENERIC_DOCLANG_CONVERSION = KILLED_AS_PRIMARY_WEDGE`
- `GENERIC_XSD_VALIDATION = KILLED_AS_PRIMARY_WEDGE`
- buyer demand remains unproven;
- WTP remains unknown;
- no market winner;
- no WIP promotion;
- no outreach, spend, contract, listing or customer interaction.

Only if A or B occurs does the narrow M1 hypothesis remain technically alive:
`INDEPENDENT_CONVERSION_FIDELITY_REGRESSION_QA_M1_ONLY`

Even then, commercial proof would still require real buyer evidence that costly regressions escape converter-native tests.

## Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`
