# 03 — ENGINEERING CONTRACTS + PROOF LADDER v1.0

## Core contracts

### `OpportunityCandidate_v1`
Required: `id, name, buyer, pain, offer, deliverable, payment_trigger, founder_cash_pre_proof_eur, source_ids, evidence_grade, next_gate, kill_rule`.

### `EvidencePacket_v1`
Required: `evidence_id, claim, evidence_type, source, observed_at, what_it_proves, what_it_does_not_prove, provenance, invalidation_rule`.

### `ExperimentCard_v1`
Required: `hypothesis, cheapest_test, target_segment, success_event, failure_event, max_cash_eur=0 pre-E4, duration, evidence_capture, next_action`.

### `ProofEvent_v1`
Required: `proof_level, external_actor, artifact, amount_if_paid, timestamp, source_reference, verification_state`. Buyer/payment levels require external evidence.

### `FundingPath_v1`
Classify capital as `CLIENT_DEPOSIT | PO | RETAINER | COMMISSION | SUPPLIER_TERMS | INVOICE_FINANCE | LOAN | GRANT_UPFRONT | GRANT_REIMBURSABLE | INVESTOR`. Never collapse these into one 'funding available' flag.

### `ExecutionState_v1`
One `PRIMARY`, up to two `PILOT`s, explicit next gate, blocked evidence, kill conditions, source freshness and persistence pointers.

## Proof ladder
1. P0 SOURCE_PROOF — authoritative external signal exists
2. P1 PROBLEM_PROOF — specific buyer pain observed
3. P2 INTEREST_PROOF — buyer asks for proposal/LOI/call
4. P3 PAYMENT_PROOF — paid pilot/deposit/PO/commission trigger
5. P4 DELIVERY_PROOF — delivered outcome with actual cost/time
6. P5 REPEATABILITY_PROOF — repeated paid delivery to >=3 buyers
7. P6 FINANCEABILITY_PROOF — bank/grant/invoice finance or investor can underwrite evidence
8. P7 SCALE_PROOF — acquisition + delivery + margin survive increased volume

## Fail-closed contracts
- Macro programme or budget ≠ customer demand.
- Open tender ≠ target SME willing to pay for intelligence.
- Grant eligibility ≠ grant award.
- Loan product ≠ credit approval.
- Prospect reply ≠ payment.
- One payment ≠ repeatability.
- Model score ≠ valuation.
- Free tool availability ≠ scalable delivery economics.
