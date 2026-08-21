# PR #103 — CI REPAIR + MERGE READBACK

## Initial condition
Post-render hardening PR #103 was a valid unique-delta candidate but its first full Audio Studio CI failed 1 of 158 tests.

## Failure 1
Test name: `test_two_real_projects_create_founder_review_candidate_not_auto_authority`.
Stale assertion expected `DOMAIN_PROMOTED` while the current safety contract correctly returned `DOMAIN_PROMOTION_ELIGIBLE`.
Repair commit: `3af4de34e59f420da54d1c22bfa749cc5725fc2d`.

## Failure 2 exposed after repair 1
The status assertion then passed, revealing a second semantic mismatch: `post_render_learning.domain_promotion_review()` only converted impossible `DOMAIN_PROMOTED` into Founder-review acceptance. Since the lower contract intentionally returns `DOMAIN_PROMOTION_ELIGIBLE`, the bridge always emitted `HOLD_FOR_REAL_INDEPENDENT_REPLICATION` even when minimum evidence was met.
Repair: recognize `DOMAIN_PROMOTION_ELIGIBLE` and emit `ACCEPT_DOMAIN_MECHANISM_CANDIDATE_FOR_FOUNDER_REVIEW`; keep `machine_may_change_current_authority=false`.
Repair commit: `f2c77514bc3a21f105e1eb5d3294db20dd544634`.

## Final CI
Workflow: `Audio Studio Runtime Tests`
Run: `32513420831`
Job: `96869536778`
Merge-result base included current session-resilience main.
Dedicated runtime: 4/4 PASS.
Full Audio Studio discovery: 158/158 PASS.

## Merge
PR #103 was marked Ready and merged with expected head SHA protection.
Final main merge commit: `0219586858797bf646ca2e7f020bf6a9ff662fc0`.

## Governance result
The final semantics are intentionally asymmetric:
- insufficient/one-project evidence -> HOLD;
- two independently qualified real projects -> DOMAIN_PROMOTION_ELIGIBLE;
- Self-Improvement may create a Founder-review candidate;
- machine may not change current authority;
- Founder review remains required for promotion.

This is both stricter and more internally consistent than the pre-Wave7 candidate.
