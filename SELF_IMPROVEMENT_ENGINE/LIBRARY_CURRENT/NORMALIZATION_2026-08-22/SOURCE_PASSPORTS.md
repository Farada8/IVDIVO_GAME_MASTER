# SYSTEMS / SELF-IMPROVEMENT SOURCE PASSPORTS — N14
**Date:** 2026-08-22  
**Status:** DERIVED REFERENCE MECHANISMS / REFERENCE ONLY / NO AUTHORITY PROMOTION

Raw works remain private in Google Drive. This file stores only bibliographic identity, abstract mechanisms, decision value and anti-misuse constraints. It does not reproduce source text.

## SP-01 — Stafford Beer / Viable Systems & Cybernetic Control
**Sources:** *Brain of the Firm*; *Decision and Control*; *Diagnosing the System for Organizations*.

**Derived mechanisms**
- Model an organization as interacting regulatory functions rather than a flat org chart.
- Require local operational autonomy inside explicit coordination and policy constraints.
- Treat variety/complexity mismatch as an engineering problem: a controller needs enough effective response variety for the disturbances it regulates.
- Diagnose failure by tracing information, control and escalation paths instead of blaming the person at the visible failure point.
- Recursion matters: a viable subsystem must preserve regulatory capability at its own scale.

**Engine mapping:** `AUTHORITY_ROUTING`, `LOCAL_AUTONOMY`, `ESCALATION`, `FEEDBACK_CONTROL`, `SYSTEM_DIAGNOSIS`, `ANTI_SINGLE_POINT_OF_COMMAND`.

**Anti-misuse:** three Beer works share one author/theoretical lineage. Do not count them as three independent replications.

## SP-02 — Senge / Learning Organization
**Families represented:** *The Fifth Discipline* (English + Spanish edition family); *The Fifth Discipline Fieldbook*; *Presence*; *The Necessary Revolution*.

**Derived mechanisms**
- Examine recurring behavior through feedback patterns, delays and structures, not isolated events.
- Surface assumptions/mental models that constrain decisions.
- Separate individual learning from team/organizational learning.
- Shared direction only matters when connected to decision and feedback loops.
- Reflection is not learning until it changes action or the operating model.

**Engine mapping:** `LEARNING_LOOP`, `ASSUMPTION_LEDGER`, `TEAM_MODEL_ALIGNMENT`, `SYSTEMS_VIEW`, `ACTION_AFTER_REFLECTION`.

**Anti-misuse:** this library is Senge-heavy. Formats, translations and related books must not masquerade as independent evidence. `Presence` is a reflective mechanism source, not technical proof.

## SP-03 — Meadows + Sterman / System Dynamics
**Sources:** Donella Meadows, *Thinking in Systems*; John Sterman, *Business Dynamics*.

**Derived mechanisms**
- Represent systems through stocks, flows, feedback loops, delays and nonlinear responses.
- Separate visible events from structures generating recurring behavior.
- Before intervention identify accumulation, rates, reinforcing/balancing feedback and delay.
- Test policies against delayed consequences and side effects, not only immediate output.
- Prefer leverage-point hypotheses that can be tested over sweeping system-change claims.

**Engine mapping:** `CAUSAL_GRAPH`, `FEEDBACK_LOOP_DETECTOR`, `DELAY_LEDGER`, `STOCK_FLOW_STATE`, `POLICY_STRESS_TEST`.

**Anti-misuse:** a causal diagram is a hypothesis, not proof. It needs observable variables and falsifiable consequences.

## SP-04 — Reinertsen / Product Development Flow
**Source:** *The Principles of Product Development Flow*.

**Derived mechanisms**
- Queue size and WIP are first-class system variables.
- Batch size changes feedback speed, risk and transaction overhead.
- Prioritization should account for economic delay, not task age or stakeholder volume alone.
- Some variability carries information/option value; variability is not universally bad.
- Decentralized control can improve flow when boundaries and decision rules are explicit.

**Engine mapping:** `WIP_LIMIT`, `COST_OF_DELAY`, `BATCH_SIZE_CONTROLLER`, `QUEUE_AGING`, `DECENTRALIZED_DECISION_RULES`.

**Anti-misuse:** currently a high-concentration source family; require prospective IVDIVO production evidence before hard global policy.

## SP-05 — Hubbard / Measurement & Value of Information
**Source:** *How to Measure Anything*, 2nd ed.

**Derived mechanisms**
- Replace “immeasurable” with an explicit decision, uncertainty range and observation that could reduce decision-relevant uncertainty.
- Judge measurement by whether it changes uncertainty enough to improve a decision, not by dataset size.
- Preserve unknowns; do not convert absent evidence to zero.
- Use value-of-information reasoning to select the smallest evidence acquisition likely to change a decision.
- Stop measuring when expected decision value falls below measurement cost.

**Engine mapping:** `EVIDENCE_GAP_VECTOR`, `VALUE_OF_INFORMATION`, `UNCERTAINTY_RANGE`, `SMALLEST_DECISIVE_TEST`, `STOP_RULE`.

**Anti-misuse:** numeric estimates remain assumptions unless calibration/source quality is proven.

## SP-06 — SRE Workbook + Accelerate + Software Engineering at Google
**Sources:** *The Site Reliability Workbook*; *Accelerate*; *Software Engineering at Google*.

**Derived mechanisms**
- Define reliability/service expectations before deciding whether failure is tolerable.
- Error-budget style logic balances change velocity and reliability rather than maximizing either alone.
- Measure delivery/feedback through operational outcomes and cycle time, not activity counts.
- Make ownership, rollback, review and maintainability explicit in engineering contracts.
- Incidents/regressions should change controls, tests or architecture.

**Engine mapping:** `SLO_GATE`, `ERROR_BUDGET`, `ROLLBACK_CONTRACT`, `CHANGE_FAILURE_FEEDBACK`, `MAINTAINABILITY_OWNER`, `CI_REGRESSION`.

**Anti-misuse:** these sources come from related software-engineering ecosystems; they are not three fully independent causal proofs. Domain metrics must be translated rather than copied literally.

## SP-07 — Toyota Kata / Iterative Improvement
**Source:** Mike Rother, *Toyota Kata*.

**Derived mechanisms**
- Move from current condition toward a bounded target condition through repeated experiments.
- Unknown obstacles are discovered through execution, not removed by planning alone.
- Each experiment needs an expected outcome and observed actual outcome.
- Coaching improves the learner’s problem-solving routine rather than supplying all answers.
- Progress is changed condition, not the number of improvement documents.

**Engine mapping:** `CURRENT_CONDITION`, `TARGET_CONDITION`, `EXPERIMENT_CARD`, `EXPECTATION_VS_ACTUAL`, `LEARNING_LEDGER`.

**Anti-misuse:** do not turn kata into ritual prompt iteration; if there is no target-condition delta or new evidence, stop.

## SP-08 — Sutton & Barto / Reinforcement Learning — cross-domain reference
**Source:** *Reinforcement Learning: An Introduction*, 2nd-edition complete draft, 2018.

**Derived mechanisms**
- Separate state, action, feedback/reward and policy; otherwise “learning” is undefined.
- Balance exploitation of known actions with bounded exploration when uncertainty warrants it.
- Credit assignment matters: later outcomes cannot be naively attributed to the most recent action.
- Learned policy is environment-dependent and needs regression when state distribution changes.

**Engine mapping:** `STATE_ACTION_OUTCOME_LEDGER`, `EXPLORATION_BUDGET`, `CREDIT_ASSIGNMENT_CAUTION`, `DISTRIBUTION_SHIFT_REGRESSION`.

**Anti-misuse:** analogy/control vocabulary only; do not reduce human readers, markets or creative quality to a single reward function.

## Additional decision sources
- Dörner, *The Logic of Failure*: delayed feedback, goal conflicts, complex-situation errors.
- Chip & Dan Heath, *Decisive*: narrow framing and confirmation-bias process checks.
- Fitzpatrick, *The Mom Test*: evidence collection that resists leading/complimentary responses.
- Abby Covert, *How to Make Sense of Any Mess*: information architecture and structure discovery.
- Chip Huyen, *AI Engineering*: production AI architecture/evaluation reference.
- Chancellor, *Devil Take the Hindmost*: historical speculation/bubble caution, not prediction authority.
- Rossman, *The Worry Solution*: outside the core systems-engineering lane; low-priority reference only.

## Combined pattern
`STATE -> DECISION -> UNCERTAINTY -> SMALLEST TEST -> FEEDBACK -> UPDATED MODEL -> CONTROL/ROLLBACK -> NEXT DECISION`.

Presence in the library never makes a mechanism canon or `VERIFIED_CURRENT`.
