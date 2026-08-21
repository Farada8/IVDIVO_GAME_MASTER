# CPMRP CYCLE 2 — SELECTED32 INTEROP + ADVERSARIAL

**Status:** BOUNDED ENGINEERING / STACKED ON CYCLE1 / NOT LEGAL AUTHORITY / NOT SI-PROMOTED  
**Parent:** CPMRP Cycle1 head `f552d97ef70c32747b48d6cae49ce5155524ca8b`  
**Selected from prior Next64:** N05–N12, N17, N21, N29–N44, N49–N52, N61–N62 = exactly 32 prompts.

## Objective
Move CPMRP from architecture-only proof to interoperable bounded execution:

`RIGHTS PASSPORT -> TDMREP/ODRL + C2PA EXPORT -> AGENT CAN_USE -> ACCEPT/FALLBACK -> RECEIPT -> LEDGER -> DURABLE WRITE PLAN -> PROVENANCE GRAPH -> CLAIM INTEGRITY -> ADVERSARIAL GATE`

## Current external standard facts used by this cycle
- TDMRep final report 10 May 2024: `tdm-reservation=1` means TDM rights reserved; `tdm-policy` points to a machine-readable policy; the policy is an ODRL 2.2 profile and may include `obtainConsent` and `compensate` duties.
- C2PA training/mining: `allowed`, `notAllowed`, `constrained`; predefined uses include data mining, AI inference, non-generative AI training and generative AI training. `constrained` must be treated as `notAllowed` if the consumer cannot resolve the constraint.
- EU Commission feasibility study, 13 July 2026: an EU-level TDM opt-out registry could complement existing solutions using work-based identifiers, fingerprints and metadata.

## Reuse law
Do not create a new durable transaction engine. Cross-store plans use the existing IVDIVO `ivdivo_durable_transaction_interface/1.0` + SI-0014 reconciler semantics.

## Cycle2 hard invariants
1. Similarity never directly creates debt.
2. `constrained` is fail-closed unless the linked licence condition is resolved.
3. TDMRep normative policy remains profile-conformant; CPMRP price metadata is a separate linked sidecar rather than silently changing TDMRep semantics.
4. Receipt corrections append/supersede; history is not deleted.
5. Claim reputation is evidence metadata, not ownership proof.
6. Durable registry/ledger writes are reversible and readback-gated in this cycle; no payment dispatch.
7. Agent fallback chooses another source when permission is unresolved or rejected.
8. No public enforcement claim, no legal adjudication, no real money.

## Deliverables
- `01_SELECTED32_EXECUTION.md`
- `02_CONTRACTS_AND_FINDINGS.md`
- `03_NEXT64_CYCLE3.md`
- `04_CYCLE2_STATE.json`
- `runtime/cpmrp_cycle2.py`
- `schemas/CPMRP_ASSET_PASSPORT_v0.2.schema.json`
- `tests/test_cpmrp_cycle2.py`
- dedicated CI workflow

## Evidence ceiling
Engineering and standards-conformance fixtures only. No counsel, market, platform adoption, KYC/tax, production signing or real-money evidence is fabricated.
