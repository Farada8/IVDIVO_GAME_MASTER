# R01–R08 — STATE CONVERGENCE PILOT — EXECUTION REPORT

Status: EXECUTED / WORKING EVIDENCE / NO STORY CANON MUTATION.

## R01 — State-convergence auditor
PASS. Added `tools/ivdivo_state_convergence.py`. It compares persisted authority class, terminal state, next action and source revision. It is advisory only and never mutates canon/state.

Real pilot result:
- B02: ISSUES_FOUND. `DRAFT_STATUS` still routes `READER_ADVOCATE_CONTINUOUS_READ`; accepted `BOOK2_FINAL_STORY_GATE_v1.0` routes external feedback / Founder-specific change only. Disposition: PATCH_POINTER_ONLY / do not reopen prose.
- D09: PASS. Founder lock decision remains the real stop gate; no E25.
- D10 BLOODBOUND: PASS after fresh rebase. Final Season Story Gate now exists and current project authority has already converged to `FOUNDER_LOCK_DECISION_GATE`.
- D04 SEVEN NIGHTS: PASS. Current execution state correctly stops live progress at real candidate voice IDs/provider access.
- Concurrency fixture: ISSUES_FOUND / `REBASE_DO_NOT_OVERWRITE` when source revision advances.

## R02 — Precedence resolver
PASS. Implemented explicit authority ranking for routing comparison. Negative same-precedence disagreement fails closed as `AUTHORITY_UNRESOLVED_SAME_PRECEDENCE` rather than choosing by timestamp.

## R03 — Stale-pointer detector
PASS. Positive fixture catches B02 stale routing. Healthy D09/D10/D04 cases do not produce false stale-pointer findings. Tool does not treat the newest timestamp alone as stronger authority.

## R04 — Machine pointer reconciliation
PATCHED ON THIS BRANCH. `CURRENT_IVDIVO_ENGINE_MACHINE_EXECUTION.json` candidate schema 1.2 now states Autopilot v1.2 real-gate semantics. `safe`, `zero_cost`, and `reversible` are explicitly NOT universal continuation prerequisites. Legacy ambiguous risk metadata still fails closed. Existing v11.2 package identity and post-package-extension boundary are preserved; no package relabel is claimed.

## R05 — Cross-dialog collision test
PASS. Auditor supports expected-vs-observed source revision and returns `STALE_SOURCE_REVISION -> REBASE_DO_NOT_OVERWRITE`. The current run also observed main advancing after branch creation; no direct overwrite of main was attempted.

## R06 — Advisory work-claim ledger
PASS AS BOUNDED RUN ARTIFACT. A run-local claim ledger records scope, starting source SHA, branch, ownership role, expiry/rebase condition and `authority_lock=false`. It is not a canonical project lock.

## R07 — Aggregate-router audit
ISSUES FOUND.
1. Drive `CURRENT_WORKSTATE` v2.6 still routes BOOK 2 to Pass C Reader Advocate despite the accepted Final Story Gate GREEN / external-feedback-ready stop.
2. Machine pointer legacy continuation wording confirmed and patched on branch under R04.
3. D09 aggregate routing is correct: Founder approval/lock only.
4. BLOODBOUND project-specific authority is now current and correctly routes Founder lock decision; older text frontier paragraphs inside the same document are explicitly superseded by its final update.
5. D04 project-specific state is correct and must outrank aggregate summaries.

Repair law: surgical routing/state correction only; no manuscript rewrite.

## R08 — Canon/firewall adversarial pass
PASS.
- Attempt: auto-lock D09 from Final Story Gate PASS -> REJECTED, explicit Founder lock required.
- Attempt: reopen Book 2 because a new tool exists -> REJECTED, final gate + no-new-evidence stop wins.
- Attempt: treat model agreement as Human Signal -> REJECTED by evidence-separation law.
- Attempt: let machine-execution pointer override story canon -> REJECTED; pointer is execution evidence only.
- Attempt: continue D04 live render without provider/voice IDs -> REJECTED as `EXTERNAL_PROVIDER_REQUIRED`.

## Verification
Local pre-integration pytest for the new convergence auditor: 6/6 PASS.
Coverage includes B02 stale pointer, D09 stop gate, D04 provider gate, same-precedence conflict, stale source revision and healthy active state.

## R01–R08 verdict
FATAL 0.
MAJOR confirmed: B02 stale local pointer; machine-pointer/resolver contract mismatch.
Both are routing/integrity defects, not story defects.
Next story pilot must not reopen completed text merely to exercise the tools.
