# CPMRP CYCLE 1 — CREATIVE PROVENANCE & MICRO-ROYALTY PROTOCOL

**Status:** BOUNDED R&D / ENGINEERING PROTOTYPE / NOT LEGAL AUTHORITY / NOT SI-PROMOTED  
**Date:** 2026-08-21  
**Founder instruction:** turn the "if AI/another creator actually uses my protected creative work, pay a tiny royalty such as €0.10" idea into a civilized machine-readable mechanism; analyze GitHub/Drive parallels; create engineering modules/contracts/proofs/protocols; execute 32 prompts; persist results; derive 64 next prompts.

## Core thesis
CPMRP is **not an ownership system for abstract ideas, styles or tropes**. It is an interoperability and accounting layer for:
1. identifying concrete creative assets and versions;
2. publishing the claimant's rights basis and machine-readable usage policy;
3. offering or requiring a licence for defined actions;
4. recording accepted licences and usage receipts;
5. aggregating micro-royalties in an auditable ledger;
6. attaching provenance evidence without letting similarity scores become legal judgments.

## External standards / current direction
- EU Commission, 13 July 2026: feasibility study for an EU-level TDM opt-out registry; work-based identifiers, fingerprinting and metadata are explicitly examined.
  https://digital-strategy.ec.europa.eu/en/library/new-feasibility-study-introducing-eu-level-registry-text-and-data-mining-opt-out
- EU GPAI Code / Commission work: machine-readable rights reservations are part of the copyright compliance path.
  https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai
- W3C Community Group TDM Reservation Protocol: `tdm-reservation`, `tdm-policy`, ODRL policy profile, including financial-compensation duty.
  https://www.w3.org/community/reports/tdmrep/CG-FINAL-tdmrep-20240510/
- C2PA: training/mining assertion supports `allowed`, `notAllowed`, `constrained`.
  https://spec.c2pa.org/
- W3C ODRL 2.2: reusable policy vocabulary for permissions, prohibitions, duties and constraints.
  https://www.w3.org/TR/odrl-model/
- Public prior art noted: AI Provenance Protocol (APP) is primarily output provenance; CPMRP's distinct R&D focus is rights-policy/licence/royalty provenance.
  https://github.com/AI-Provenance-Protocol/ai-provenance-protocol

## IVDIVO integration law
`RESTORE -> DEDUPE -> EVIDENCE CONTRACT -> HIGHEST-INFO BOUNDED TEST -> GATE -> PROVENANCE -> INVALIDATION/ROLLBACK -> WRITE-THROUGH`

Reuse existing IVDIVO durable/self-improvement infrastructure. Do not create a second durable transaction runtime. Do not create or promote a new SI ID in this cycle.

## Cycle 1 deliverables
- `01_PROMPTS_32.md`
- `02_EXECUTION_RESULTS_32.md`
- `03_ARCHITECTURE_CONTRACTS_PROOFS_PROTOCOLS.md`
- `04_NEXT_PROMPTS_64.md`
- `05_CYCLE_STATE.json`
- `runtime/cpmrp_core.py`
- `tests/test_cpmrp_core.py`
- `schemas/CPMRP_ASSET_PASSPORT_v0.1.schema.json`
- `schemas/CPMRP_USAGE_AND_RECEIPT_v0.1.schema.json`

## Evidence ceiling
This cycle proves only bounded architecture and deterministic prototype behaviour. It does **not** prove:
- that every AI-reference use is legally chargeable;
- copyright ownership of a claimant;
- infringement;
- market willingness to pay;
- payment/KYC/tax readiness;
- enforceability in every jurisdiction;
- platform adoption.

The protocol must preserve those unknowns explicitly.
