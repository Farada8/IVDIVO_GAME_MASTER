# RUN33 — NEXT 64 PROMPTS

Date: 2026-08-21
Status: DESIGNED FOR SUBSEQUENT WORK; NOT CLAIMED EXECUTED IN RUN33.

## A — Transaction contract hardening
1. Add explicit transaction-level status vocabulary derived from action states without hiding per-action ambiguity.
2. Add malformed transaction schema fixtures for missing authority, empty actions, unknown store/effect/state and invalid identities.
3. Prove user-supplied idempotency keys cannot collide silently within one transaction.
4. Define stable cross-session transaction IDs and rules for when a new logical transaction must use a new ID.
5. Add content-hash identity profile for raw files where provider/store revision IDs are unavailable.
6. Add structured reason codes for STOP/QUARANTINE/VERIFY decisions and freeze them as API contract.
7. Test SUPERSEDED action semantics combined with active actions and ensure superseded work is never replayed.
8. Add transaction size/action-count ceilings and anti-bloat rejection.

## B — Real GitHub + Drive partial-write pilots
9. Execute a reversible pilot where GitHub write completes and Drive mirror is intentionally left NOT_STARTED; prove only Drive is planned next.
10. Execute inverse pilot: Drive write completes and GitHub is missing; prove only GitHub is planned next.
11. Simulate lost Drive response after create; search/readback and bind existing file instead of duplicate creation.
12. Simulate GitHub branch commit followed by stale-main advance; prove REBASE_FIRST outranks missing Drive action.
13. Record exact GitHub commit/blob identity and Drive ID/revision in transaction evidence.
14. Add a duplicate-name Drive fixture showing filename is insufficient identity.
15. Measure tool calls and elapsed recovery operations for normal vs interrupted two-store write.
16. Produce first real reversible partial-write production evidence event for SI-0014.

## C — Concurrency / optimistic control
17. Run two concurrent work units targeting independent files and prove unrelated main drift can be rebased without false conflict.
18. Run two concurrent work units targeting the same machine pointer and prove same-frontier conflict fails closed.
19. Add dependency fingerprint so rebase can distinguish overlapping vs unrelated main changes.
20. Define optimistic concurrency token contract for Drive revisions where available.
21. Define exact-head/expected-SHA write contract for GitHub mutations as a universal adapter requirement.
22. Test branch force-update prohibition outside explicitly reconstructed fresh-main rebase flows.
23. Add transaction parent/base SHA to prove which authority snapshot generated an intended write.
24. Measure false REBASE rate under high parallel commit frequency and propose selective freshness sweeps.

## D — Provider / paid / irreversible reconciliation
25. Define generic provider adapter interface for lookup-by-idempotency-key/request-ID without embedding provider-specific APIs in 18D.
26. Model `REQUEST_ACCEPTED`, `ASSET_CREATED`, `ASSET_VERIFIED`, `ASSET_ACCEPTED` as provider-domain evidence layers outside generic side-effect state.
27. Test lost paid-response fixture and prove no automatic retry even when local checkpoint says pending.
28. Test provider reports request failed before charge and define evidence required to safely permit a new dispatch.
29. Add spend-ledger reconciliation pointer to transaction action without storing credentials.
30. Model irreversible GitHub merge as IRREVERSIBLE_WRITE and prove STARTED_UNKNOWN quarantines.
31. Test external action confirmed but intended artifact identity missing; require identity acquisition before completion.
32. Draft adapters for ElevenLabs/other audio providers using current provider authority without making live calls.

## E — Checkpoint lineage / retention / incident evidence
33. Add explicit `parent_checkpoint_sha256` cross-check between 18C checkpoint envelope and lineage entry.
34. Add one CURRENT pointer per active work unit that references lineage head rather than duplicating checkpoint content.
35. Define safe GC algorithm that refuses deletion of AUDIT_KEEP or current head.
36. Test lineage branch/conflict import from two crashed sessions and create explicit reconciliation outcome.
37. Add incident bundle linking checkpoint, transaction record, CI/readback evidence and learning event by incident ID.
38. Add retention policy for incidents that become superseded by verified root-cause fixes.
39. Measure storage growth for 100/1,000 material checkpoints under compact lineage policy.
40. Run anti-bloat review and remove any lineage field that never changes a recovery decision or audit obligation.

## F — Self-Improvement evidence / telemetry
41. Emit a real interruption-learning event from the next genuine session/store interruption.
42. Separate recovery effectiveness metrics from engineering test metrics in Self-Improvement state.
43. Add confidence/evidence-class field that prevents synthetic event counts from being mistaken for production evidence.
44. Define duplicate-work-avoided measurement precisely enough to prevent inflated claims.
45. Define recovery-overhead ratio: checkpoint+recovery tool calls versus uninterrupted baseline.
46. Compare two checkpoint cadences on the same workflow and select the Pareto-better cadence.
47. Add regression that any real false-resume event automatically creates HOLD signal for SI-0014.
48. Add registry movement proposal generator that produces evidence but never mutates candidate lifecycle automatically.

## G — Cross-project integration / system convergence
49. Pilot SI-0014 on one narrative/story-engine work unit without changing story canon.
50. Pilot SI-0014 on one audio-production work unit at a reversible asset/write boundary.
51. Compare recovery needs of narrative text artifacts versus audio binary/provider artifacts and keep universal core minimal.
52. Map PR #104 Cycle4 transaction/evidence helpers onto 18D interfaces after #104 status is resolved.
53. Map PR #103 post-render artifact evidence onto generic transaction identity without moving audio QC into core.
54. Integrate project-state coverage gate with checkpoint availability: resumable project state should expose recovery pointer when active.
55. Add cross-AI handoff field for transaction/checkpoint IDs and explicit unknown side effects.
56. Test a new model/session can reconstruct safe next actions using only persisted authority + checkpoint + transaction evidence.

## H — Packaging / promotion / release
57. Create SI-0014 production pilot acceptance matrix with PASS/FAIL evidence per promotion condition.
58. Run full repository regression after final Run33 merge and record exact test counts.
59. Build deterministic proof manifest with blob SHAs for 18C/18D/tools/schemas/tests.
60. Decide whether 18C+18D remain separate protocols or converge only after two real project pilots.
61. Define next engine-package inclusion contract; do not relabel v11.2.
62. Build migration note for any candidate-local transaction journals that should adopt 18D semantics.
63. Independent Red Team real incident evidence after minimum three real recoveries, including cost/overhead and false-stop analysis.
64. Final SI-0014 decision: `PROMOTION_REVIEW / NARROW / HOLD / ROLLBACK`, with explicit proof bundle and no automatic promotion.
