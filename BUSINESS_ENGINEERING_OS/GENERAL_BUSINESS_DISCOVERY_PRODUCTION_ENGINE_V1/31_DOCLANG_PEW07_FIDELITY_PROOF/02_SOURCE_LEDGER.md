# P-EW07 — PUBLIC SOURCE LEDGER

**Date inspected:** 2026-08-22

## S1 — DocLang reference toolkit
Source: `doclang-project/doclang` toolkit README.
Observed:
- official Python toolkit;
- `doclang validate` CLI;
- XSD-only validation via `--xsd-only`;
- full validation may include Schematron;
- structural XSD validation covers hierarchy, data types, attributes and element ordering.

## S2 — DocLang toolkit version
Source: `doclang-project/doclang/pyproject.toml` on inspected main.
Observed project version: `0.7.3`.
P-EW07 pins `doclang==0.7.3` in CI so the structural validator is reproducible.

## S3 — Docling issue #3864
Title: `PDF Document Conversion to DocLang and syntax error`.
Created: 2026-07-24. Closed: 2026-07-27.
Reported class: conversion/validation trouble around an ampersand in ordinary text.
Boundary: this issue is a public bug report, not proof that the defect remains current or prevalent. P-EW07 does not copy the user's attachment and does not claim its minimal fixture reproduces the original bug.

## S4 — Docling issue #3780
Title: `Layout misclassifies dotted poetic line as formula, export leaves text empty`.
Created: 2026-07-09. Observed open on 2026-08-22; last update shown 2026-08-18.
Reported class: semantic/layout misclassification plus missing exported text leading to invalid downstream document/chunking.
Boundary: public issue evidence establishes a disclosed failure class only; it does not establish prevalence or buyer pain.

## Proof use
S1/S2 define the commodity structural-validation boundary.
S3/S4 motivate testing whether an independent fidelity regression invariant can catch source-to-output semantic change that structural validation alone need not detect.

`PUBLIC_ISSUE != CURRENT_PREVALENCE`
`SCHEMA_VALIDATION != SOURCE_TRUTH_COMPARISON`
`PUBLIC_FAILURE_CLASS != COMMERCIAL_DEMAND`
