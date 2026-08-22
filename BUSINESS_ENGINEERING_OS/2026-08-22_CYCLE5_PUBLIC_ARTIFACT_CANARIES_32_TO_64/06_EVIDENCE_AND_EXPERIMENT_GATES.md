# CYCLE5 — EVIDENCE + EXPERIMENT GATES

## N45 — voluntary buyer-interview card — DRAFT ONLY

Goal: test whether the exact sample artifact changes a real buyer's decision/workload.

Questions:
1. Walk me through the last time you decided whether to pursue a tender / qualify a retrofit lead / automate a workflow.
2. What did you actually do, in what order, and who was involved?
3. Which step consumed the most time or caused avoidable rework?
4. What information did you have to collect from different places?
5. What did you almost miss?
6. What happens when the decision is wrong or late?
7. What do you use today instead of this sample?
8. Looking at this exact artifact, which section would you ignore? Which section changes a real decision?
9. What would have to be true for this to be useful repeatedly?
10. If it is not useful, what is the earliest reason?

Do not ask leading questions such as “Would you pay for this?” as primary evidence. Capture concrete past behaviour and a real next commitment when voluntarily offered.

## N46 — outreach drafts — NOT SENT

**Email draft**
Subject: 10-minute review of a contractor decision brief

I built a one-page public-data tender decision brief intended to reduce the time spent deciding whether a competition deserves deeper estimating work. I am not selling software in this message. Would you be willing to review one concrete example for 10 minutes and tell me where it fails compared with how you currently work?

**LinkedIn draft**
I’m testing a one-page tender-screening brief for Irish contractors. I need criticism from someone who actually makes bid/no-bid decisions. Would you be open to a short review of one sample?

**Phone opener draft**
I’m testing a manual tender-screening brief, not asking you to buy anything on this call. I’m trying to learn whether it removes real work or just repackages public information. Who would be the right role to critique one sample?

`SEND_STATUS = NOT_SENT`.

## N47 — E3 promotion gate

E3 requires a durable receipt containing:
- kind=`BUYER_INTERACTION`;
- source_type=`REAL_HUMAN`;
- exact public artifact hash;
- observed_at timestamp/date;
- buyer role;
- interaction outcome;
- source/readback pointer where allowed.

Synthetic review, public source, AI score, “verified=true”, founder belief, inferred interest, opened email or target-list presence cannot satisfy E3.

Current Cycle5 E3 receipts: **0**.

## N48 — E4 promotion gate

E4 requires real positive-value commercial commitment bound to the artifact lineage:
- payment; or
- deposit; or
- purchase order.

Required fields: real transaction class, exact artifact hash, transaction/PO identity, observed date/time, positive amount, durable evidence pointer/readback where allowed.

Current Cycle5 E4 receipts: **0**.

## N49 — response taxonomy

- `BOUNCE_TECHNICAL` — invalid/unreachable channel; no value signal.
- `NO_RESPONSE` — non-response; weak/ambiguous evidence only.
- `DECLINE_NO_TIME` — access/priority issue; not automatically value failure.
- `DECLINE_NOT_ROLE` — targeting failure.
- `DECLINE_NO_PROBLEM` — problem hypothesis evidence against.
- `DECLINE_INTERNAL_SOLUTION` — substitute/alternative evidence.
- `REVIEW_ACCEPTED` — interaction opportunity, not value proof until review occurs.
- `REVIEWED_NO_VALUE` — direct negative E3-class evidence.
- `REVIEWED_VALUE_NO_BUY` — value evidence but no E4.
- `PAID_OR_PO` — E4 candidate subject to receipt validation.

## N50 — objections taxonomy

- problem not painful;
- existing portal/process good enough;
- internal estimator/QS already performs function;
- information is too generic;
- trust/provenance insufficient;
- update frequency too slow;
- false-positive/false-negative risk too high;
- liability/compliance concern;
- data/privacy/security concern;
- integration/admin burden;
- price/value mismatch;
- no budget owner;
- procurement/vendor onboarding barrier;
- timing/no current need.

Classifier law: objections diagnose the earliest failing layer; they do not trigger automatic persuasion or feature expansion.

## N51 — bounded paid-pilot contract template — DRAFT ONLY

**Scope**: one named buyer, one named workflow, one bounded artifact/deliverable, fixed duration.

**Must specify**:
- exact deliverable and acceptance criteria;
- source/data responsibilities;
- exclusions and professional/legal boundaries;
- revision limit;
- delivery date;
- price/deposit/payment terms;
- refund/stop boundary;
- confidentiality/data handling;
- no guarantee of grant, tender, revenue or ROI outcome;
- evidence permission: whether anonymised process metrics may be retained.

Stop if scope expands beyond the tested hypothesis or regulated advice is required.

## N52 — corporate sender trust gate

Before scaled B2B outreach, require:
- controlled business domain/email identity;
- accurate company identity/contact details;
- lawful contact basis and suppression handling;
- unsubscribe/opt-out handling where required;
- no deceptive personalisation;
- volume/rate limits;
- reply monitoring;
- bounce hygiene;
- evidence that message/channel is appropriate for the target market.

Current scaled-sender status: `NOT_PROVEN / NO_SCALED_SEND`.

## N53 — evidence ledger schema

Every material claim must bind:
`claim_id → claim_text → source_ref → observed_at → authority → evidence_grade → artifact_hash/opportunity_id → uncertainty/null fields → supersession status`.

Duplicate/syndicated sources count as one evidence family where correlation is known.

## N54–N56 — predictor calibration and double-loop learning

For each Cycle4/5 predictor record:
- prediction date;
- predictor/mechanism;
- predicted outcome;
- later E3/E4 result;
- calibration error;
- repair/demotion decision.

No predictor is demoted merely because no later market evidence exists. Demotion requires observed mismatch.

Trigger double-loop review after three independent failures in the same hypothesis family. Review not only the offer but the assumption/rule that repeatedly generated the offer.

Current repeated real failure families: **0**.

## N57–N59 dependency holds

- CREATE/BROKER/ACQUIRE comparison: `HOLD_DEPENDENCY_E3`.
- customer-funded/supplier-funded/grant-loan/investor topology comparison: `HOLD_DEPENDENCY_E4`.
- acquisition downside screen: `NOT_APPLICABLE_CURRENT_WIP`; no cash-flowing acquisition target is active.

## N60 — portfolio anti-correlation map

Current WIP intentionally spans three mechanism families:
1. PRIMARY OP01 — procurement/tender intelligence — B2B information/decision support.
2. PILOT A OP03 — retrofit qualification/orchestration — rules + workflow coordination.
3. PILOT B OP19 — SME AI workflow diagnostic — implementation/readiness diagnostic.

Shared risk: all could fail because free/public guidance plus internal staff are “good enough”.
Independent information: they differ in buyer workflow, regulation/support environment and deliverable mechanics.

## N61 — adversarial review findings

1. CIF directory presence is not buyer fit or SME proof.
2. Current tender flow proves workload, not willingness-to-pay for a curated brief.
3. Free eTenders search or an internal estimator may dominate the proposed PRIMARY.
4. Public tender metadata cannot prove a contractor's procurement eligibility.
5. Public SEAI rules cannot provide legal/official grant clearance for a specific property.
6. Government AI support does not prove a company should adopt AI or buy a diagnostic.
7. Sample quality may be overestimated because the researcher knows the hypothesis; real buyer comprehension may differ.
8. Public source freshness can decay faster than the artifact if deadlines/addenda change.
9. Price ranges in Cycle5 are hypotheses only and may be materially wrong.
10. “No outreach” protects against premature selling but also caps evidence at E2+; engineering must not mistake preparation for market validation.
