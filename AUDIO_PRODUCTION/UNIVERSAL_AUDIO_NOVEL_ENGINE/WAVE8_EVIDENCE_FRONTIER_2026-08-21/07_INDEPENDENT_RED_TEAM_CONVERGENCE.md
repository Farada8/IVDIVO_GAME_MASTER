# WAVE8 — INDEPENDENT RED TEAM + PARALLEL CONVERGENCE

Date: 2026-08-21

## Verdict

- FATAL: 0 confirmed under current safeguards.
- MAJOR: 5 integration / provenance-strength gaps.
- MEDIUM: 2 documentation / duplication risks.
- Architecture disposition: **KEEP BOUNDED WAVE8 EXTENSION; HOLD MERGE/PROMOTION UNTIL FRESHNESS + TRUST BOUNDARIES ARE CLOSED.**

This is not a new Audio OS. It audits the four bounded Wave8 modules against current `main`, Wave7/PR103, Session Resilience Run33/SI-0014, and System Cycle5 controls.

## RT-W8-01 — CURRENT-MAIN DIVERGENCE — MAJOR

Fresh compare observed Wave8 diverged from current `main`; branch was 34 commits ahead and 26 behind with merge-base `b4c29e4a81fc368f440f39827df0adda46b4c897` while current main had advanced to `55c69de4f19aec1c2b408020c1447cbd38beef5b`.

**Risk:** green CI on an older merge result can coexist with newer authority/control changes on main.

**Required:** fresh-main delta/rebase review, no force overwrite, then full Audio Studio CI on the fresh merge result.

## RT-W8-02 — PROOF MANIFEST CLAIM CEILING — MAJOR

`evidence_proof.py` correctly hashes the manifest and requires typed evidence classes. However `verified=true` is still caller-supplied input.

**Law:** `PROOF_INTEGRITY != EXTERNAL_TRUTH`.

A proof hash proves that a compiled record has not changed. It does not independently prove a human listened, a provider authenticated, a payment occurred, a real alignment exists, or a recovery succeeded.

**Required:** every external evidence class must bind to a durable source artifact/receipt whose class-specific validator/readback has passed. Human-quality/V1 release remain external-authority decisions even if class coverage is complete.

## RT-W8-03 — HUMAN REVIEW TRUST ANCHOR — MAJOR

`human_review_evidence.py` correctly forbids `reviewer_type=MACHINE`, binds evidence to `candidate_binding_sha256`, maintains an append-only hash chain, and never auto-locks. But `compile_event()` is machine-callable and constructs `machine_generated=false`.

Therefore the event hash proves record integrity, not human presence.

**Required:** production HUMAN_REVIEW evidence additionally needs an externally witnessed reviewer submission/attestation reference (or equivalent trusted capture surface) with durable hash/readback. Synthetic fixtures must be a distinct non-human evidence class and can never satisfy production human gates.

Positive safeguard retained: terminal machine result is at most `ELIGIBLE_FOR_HUMAN_LOCK_DECISION`; `voice_lock=false` and `machine_may_auto_lock=false`.

## RT-W8-04 — LIVE ESCROW CONTENT READBACK — MAJOR

`live_evidence_escrow.py` binds source/request/capability/provider/spend/audio/alignment identities and prevents provider replay. Accepted audio/alignment carry hashes. However recovery currently accepts a caller-supplied set of durable refs and checks pointer membership.

**Law:** `POINTER_PRESENT != CONTENT_READBACK_VERIFIED`.

**Required:** durable recovery proof must include content identity/readback acknowledgement for request, response/failure metadata, audio, alignment when present, spend-ledger entry, and charge evidence. Pointer-only success may be called `RECOVERY_POINTERS_PRESENT`, not `DURABLE_RECOVERY_PASS`.

When SI-0014/Run33 is accepted, Wave8 should adapt to its durable transaction reconciler/checkpoint lineage rather than duplicate recovery semantics.

## RT-W8-05 — PROVIDER SNAPSHOT SOURCE PROVENANCE — MAJOR

`provider_snapshot.py` correctly separates stable/volatile fields, rejects credential-like durable fields, prevents caller-only ACCOUNT_WIDE upgrades, and blocks auto-substitution.

But snapshot hashing alone proves snapshot integrity, not that the source preflight came from a real authenticated provider session.

**Required:** AUTH_PROVIDER proof binds the snapshot to the original preflight artifact/ref/hash and authenticated readback. Snapshot alone is capability-record evidence.

## RT-W8-06 — DOCUMENTATION VERSION / CLASS DRIFT — MEDIUM

Engineering prose still references provider snapshot output `1.0` in places while runtime is `1.1`, and older prose omits `REAL_ALIGNMENT` and `DURABLE_RECOVERY` from V1 proof requirements.

**Required:** synchronize docs with runtime/schema before merge; code is source for current contract behavior until documentation is corrected.

## RT-W8-07 — SELF-IMPROVEMENT DUPLICATION RISK — MEDIUM

Current parallel systems already provide candidate/general control semantics:

- Wave7 + PR103: merged Audio post-render controls.
- Run33 / SI-0014: durable transaction recovery/checkpoint/interruption-learning candidate.
- System Cycle5: claim ceilings, evidence-family lineage, CAS, mutation intent, multi-surface transaction/recovery, state-shape guard, Self-Improvement Governor.

Wave8 should expose adapters/hooks and reuse these semantics; it should not create a second central recovery or authority plane.

Candidate mechanism remains `TYPED_EVIDENCE_FRONTIER_PROVENANCE_BRIDGE` with status `PILOT_CODE / HOLD_REAL_EVIDENCE`; no new central SI ID is justified yet.

## CI proof

An earlier Wave8 merge-ref run exposed real contract/test drift: 194 tests produced 2 failures + 21 errors after stricter binding/spend/proof/scope contracts were introduced. Those failures were repaired without relaxing the contracts.

Latest observed GitHub Actions run #74:

- dedicated Audio Novel runtime: 4/4 PASS;
- full Audio Studio suite: 199/199 PASS;
- conclusion: SUCCESS.

This proves tested engineering behavior on that merge result only. It does **not** prove provider access, human quality, live audio, real alignment, economics, durable real recovery, cross-project portability, or V1 release.

## Path to goal

1. Freeze evidence semantics above.
2. Fresh-main reconcile/rebase.
3. Fresh merge-result full CI.
4. GitHub + Drive readback.
5. Keep Wave8 bounded; no automatic SI promotion.
6. First external experiment = authenticated secret-free provider preflight/snapshot.
7. Actual human review must use trusted external submission/attestation provenance.
8. Paid canary only after provider/cast/pronunciation/pre-spend gates.
9. Live escrow must prove content readback, not pointer presence.
10. V1 needs real two-project evidence + measured economics + human quality + authorized release decision.

## Merge decision now

**HOLD / NO-GO for immediate main merge** until current-main freshness and documentation/claim-boundary requirements are closed and a fresh merge-result CI passes. This is an integration hold, not an architecture rejection.
