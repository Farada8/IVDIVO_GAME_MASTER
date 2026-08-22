# IVDIVO — NEXT64 R25–R32 — EVIDENCE + APPROVAL SEMANTICS v1.0

**Status:** 8/8 EXECUTED / CANDIDATE ENGINEERING EVIDENCE  
**Date:** 2026-08-21  
**Story mutation:** NONE.

## R25 — Founder-evidence contract adapter
**Result:** IMPLEMENTED / FAIL-CLOSED.

`tools/ivdivo_evidence_adapters.py::founder_evidence` binds explicit Founder evidence to `project_id + frontier + gate_id + locator`. `explicit=false` returns HOLD; Final Story Gate PASS cannot create Founder evidence.

## R26 — Human Listener evidence adapter
**Result:** IMPLEMENTED / FAIL-CLOSED.

Human listener evidence requires an actual reviewer identity and response locator. `model_generated=true` is rejected with `MODEL_OUTPUT_CANNOT_BE_ADAPTED_AS_HUMAN_SIGNAL`. Blind-listener evidence remains distinct from model review.

## R27 — Provider-response evidence adapter
**Result:** IMPLEMENTED / FAIL-CLOSED.

Dry-run/machine provider checks are emitted as `MACHINE_TEST` and explicitly cannot prove live provider execution. A claimed live response without a response locator becomes HOLD. Only an actual live response may use `PROVIDER_RESPONSE`.

## R28 — External-AI evidence ceiling
**Result:** IMPLEMENTED / FAIL-CLOSED.

External AI/model review authority is capped at 40 in the adapter and explicitly cannot prove Founder approval, Human Signal or live provider output.

## R29 — Conflicting-evidence resolver
**Result:** IMPLEMENTED.

Coexisting PASS and FAIL evidence returns `UNRESOLVED_CONFLICT` plus an explicit reconciliation/repair disposition. The resolver does not silently average, vote or choose a convenient result.

## R30 — Artifact readback proof
**Result:** IMPLEMENTED.

Expected/readback SHA identity is exact. Match => PASS; mismatch => FAIL. This complements the existing Production Proof Chain artifact mismatch gate.

## R31 — Approval-token binding
**Result:** IMPLEMENTED.

Approval token is deterministically bound to `project_id + frontier + gate_id + evidence_id`. A D10 Founder lock token cannot unlock D01 or D09.

## R32 — Gate mismatch Red Team
**Result:** PASS_CONTRACT / CI REQUIRED.

Integration test declares a Human gate PASS while supplying only EXTERNAL_AI evidence. Production Proof Chain computes HOLD and returns `FAIL_CLOSED` on the declared/computed gate mismatch.

## Regression surface

Added:
- `tools/ivdivo_evidence_adapters.py`
- `tests/test_evidence_adapters_r25_r32.py`
- Production Proof CI expanded to include the eight new tests.

Expected aggregate regression after CI: previous 37 tests + 8 = **45 tests**.

## Evidence boundaries

No new Founder approval was inferred.  
No Human Signal was fabricated.  
No provider call/result was fabricated.  
No market evidence was fabricated.  
No candidate is promoted to CURRENT by this block.

**Next block after green CI:** R33–R40 value/telemetry/pruning using measured data only; unknown cost/time fields remain null rather than false zero.