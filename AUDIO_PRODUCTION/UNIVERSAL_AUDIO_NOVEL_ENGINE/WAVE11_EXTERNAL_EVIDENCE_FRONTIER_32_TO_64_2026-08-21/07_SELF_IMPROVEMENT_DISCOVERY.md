# Wave11 — Self-Improvement Discovery

## Candidate mechanism
`DEPENDENCY_AWARE_EXTERNAL_EVIDENCE_FRONTIER`

Status: **DISCOVERY_REPLICATED_IN_ENGINEERING_ONLY / NO NEW SI ID / NO CURRENT PROMOTION**.

## Problem it addresses
Complex production cycles can create false progress when downstream engineering tasks are completed or described as PASS while an upstream provider/human/live evidence event never occurred. This creates evidence laundering, wasted implementation and sometimes premature paid work.

## Abstract mechanism
1. Express externally dependent production work as a causal DAG.
2. Separate action class from evidence class.
3. A prompt becomes READY only after all declared dependencies are completed through their authoritative execution path.
4. Missing real evidence produces a precise `HOLD_EXTERNAL_*` at the first edge.
5. Descendants receive `BLOCKED_DEPENDENCY`, not synthetic completion.
6. Internal engineering may continue only if it does not pretend the missing external event occurred.
7. Destructive/paid actions require explicit human GO plus current revalidation.
8. Persist the first blocker and the highest-information next experiment.

## Evidence available now
### Replication A — NMM Cycle5
A separate project-specific audio cycle independently reached the same conclusion. It dispositioned 32/32 prompts while provider credential/human rows were absent, using explicit external holds instead of fictional execution.

### Replication B — Audio Wave11
Generic Audio Novel Engine Wave11 repeats the mechanism on a different prompt graph. 32/32 prompts are dispositioned; prompt 01 is the real authenticated-provider frontier and prompts 02–32 are causally blocked. A new routing-only evaluator and tests encode the DAG without granting external authority.

## What this DOES prove
- the mechanism is implementable as deterministic engineering routing;
- it can prevent out-of-order paid-dispatch readiness in two independently structured audio worklines;
- it makes missing evidence machine-visible rather than silently inferred.

## What this DOES NOT prove
- fewer real production defects in live runs;
- lower spend or faster delivery;
- better human audio quality;
- universal applicability outside these engineering cycles;
- correctness of caller-supplied completion evidence.

## Why no new SI ID
Current evidence is engineering-only replication. Existing SI-0014 recovery and SI-0015 freshness/approval-event primitives cover adjacent responsibilities and must not be duplicated. Universal promotion would be premature.

## Promotion requirements
1. Run on at least two projects with genuine external provider + human evidence.
2. Compare against a predeclared baseline for false completion, skipped gate, duplicate spend and recovery ambiguity.
3. Demonstrate at least one real case where the frontier prevents an invalid downstream action without creating excessive false blocking.
4. Demonstrate a protected no-change/control case where it correctly permits progression.
5. Pass regression against SI-0014/SI-0015 and current Audio Studio contracts.
6. Independent Red Team finds FATAL 0 / MAJOR 0 for authority escalation and paid-action safety.
7. Human/Founder review approves any universal routing promotion.

## Reuse conditions if later promoted
- prompts must have explicit causal dependencies;
- authoritative evidence validators remain external to the routing graph;
- the router may never convert a planning flag into external truth;
- paid/destructive actions need typed authorization edges;
- a HOLD must identify the exact missing evidence and highest-information next experiment.

## Current decision
Keep as **CANDIDATE_FOR_REVIEW_ENGINEERING_ONLY** inside Wave11 evidence. Do not modify the global Self-Improvement registry identity set in this cycle.
