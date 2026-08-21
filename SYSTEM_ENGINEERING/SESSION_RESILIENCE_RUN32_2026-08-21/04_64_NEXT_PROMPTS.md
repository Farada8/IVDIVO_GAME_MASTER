# SESSION RESILIENCE — 64 NEXT PROMPTS
Date: 2026-08-21
Status: DESIGNED FOR SUBSEQUENT WORK; NOT EXECUTED IN THIS RUN.

These prompts are derived from the 32-run findings. They are ordered to generate discriminating evidence rather than more architecture for its own sake.

## A — Runtime / CI / contract hardening

01. Run the new checkpoint suite inside repository CI from fresh main and record exact workflow/run/job evidence.
02. Add malformed-schema fixtures: missing main SHA, missing state revision, non-dict next action, invalid write status.
03. Add deterministic checkpoint serialization test proving canonical payload hash is stable across key order.
04. Add backward-compatibility reader for future schema minor versions without accepting unknown critical semantics.
05. Test clock/timestamp independence: resume decision must not trust wall-clock freshness alone.
06. Add checkpoint size ceiling and reject transcript-sized payloads to preserve anti-bloat law.
07. Test Unicode/project IDs/paths across Russian/English content without hash drift.
08. Add explicit schema validation to CLI before checkpoint write and fail closed on invalid payload.

## B — Drive / GitHub / durable-store transactions

09. Design a generic multi-store write transaction record for GitHub + Drive + File Library pointers without introducing distributed-lock complexity.
10. Pilot partial transaction: GitHub write succeeds, Drive write fails; verify recovery writes only Drive.
11. Pilot inverse partial transaction: Drive mirror succeeds, GitHub write fails; verify no duplicate Drive artifact.
12. Add readback identity fields for GitHub blob SHA/commit and Drive file ID/modified revision.
13. Define idempotency key derivation from work unit + target store + artifact identity.
14. Test renamed Drive file/folder and stale pointer classification.
15. Test GitHub branch deleted/PR closed while checkpoint still points to it; route rebase/recovery correctly.
16. Add durable-write reconciliation report that lists VERIFIED / PENDING / CONFLICT / SUPERSEDED per store.

## C — Concurrency / sibling-dialog rebase

17. Simulate two dialogs checkpointing same project state revision then advancing independent branches; verify mergeable classification.
18. Simulate two dialogs advancing same dependency frontier; verify second checkpoint cannot RESUME_EXACT.
19. Define dependency-overlap fingerprint so unrelated sibling writes do not force expensive full-project reread.
20. Test main SHA drift caused only by unrelated project commit; measure whether selective delta read can safely resume.
21. Add optimistic concurrency token for project-state write when supported.
22. Test stale checkpoint after a project authority pointer changed; require AUTHORITY re-resolution, not simple source rebase.
23. Test a newer sibling checkpoint superseding an older checkpoint for the same work unit.
24. Design checkpoint lineage/parent_checkpoint_id so recovery history is auditable without becoming a new authority chain.

## D — Assets / providers / paid and irreversible boundaries

25. Integrate checkpoint hook with v17 chat-local asset escrow: critical artifact must be durable before checkpoint can declare clean resume.
26. Test provider request accepted but production asset not accepted; checkpoint must preserve the two states separately.
27. Test ambiguous paid POST response; checkpoint must defer to spend/idempotency reconciler and never replay automatically.
28. Add explicit `external_side_effect_state` vocabulary: NOT_STARTED / STARTED_UNKNOWN / CONFIRMED / RECONCILED.
29. Test irreversible GitHub merge/write approval metadata so checkpoint restart cannot repeat it.
30. Test local/generated file pointer that expires between sessions; classify as RECOVER_VOLATILE_FIRST, not MISSING.
31. Pilot checkpoint around ElevenLabs canary boundary without spending credits; verify dispatch remains gated elsewhere.
32. Add provider/asset recovery adapter interface but keep actual provider logic outside checkpoint engine.

## E — Self-improvement telemetry / evidence

33. Add Learning Ledger observation schema for abrupt-session recovery events.
34. Measure duplicate-work avoided in a controlled interruption simulation.
35. Measure checkpoint overhead in writes/bytes/tool calls across a normal 30-minute work block.
36. Track false STOP rate: cases that could safely resume but checkpoint blocked.
37. Track false RESUME adversarially: attempt to make stale/blocked state resume; target zero.
38. Compare checkpoint cadence A/B: every material artifact vs coarse stage boundary; choose lower overhead at equal recovery safety.
39. Mine three projects for recurring interruption/persistence failures before universal VERIFIED_CURRENT promotion.
40. Define promotion gate for SI-0010 based on production evidence rather than test count.

## F — Transcript / cross-AI / manual recovery

41. Compose 18B transcript recovery with 18C checkpoint: transcript newer than checkpoint, checkpoint newer than transcript, and conflicting cases.
42. Test recovery when user supplies only a screenshot/summary of lost page; keep unavailable exact details UNKNOWN.
43. Design cross-AI handoff packet field for latest checkpoint ID and durable store pointers.
44. Test Claude/Grok/GPT return artifact claim that was never persisted; checkpoint must not self-verify it.
45. Add recovery precedence table: project authority > verified durable write > checkpoint > transcript claim > chat memory.
46. Test secret redaction across checkpoint + pasted transcript combined flow.
47. Create a minimal user-facing emergency recovery instruction that does not require manual technical diagnosis.
48. Verify that a new model can resume from project state + checkpoint without receiving the old chat.

## G — Production integration / anti-bloat

49. Pilot checkpoint hooks in one narrative writing workflow at Story Gate and chapter-batch boundaries.
50. Pilot checkpoint hooks in one audio workflow at render/alignment/mix repair boundaries.
51. Measure whether checkpointing causes duplicate status files or router proliferation; merge/narrow if yes.
52. Add garbage-collection policy for superseded checkpoints while retaining audit-needed recovery evidence.
53. Define one CURRENT checkpoint pointer per active work unit instead of timestamp-file explosion.
54. Add checkpoint retention classes: EPHEMERAL_RECOVERY / AUDIT_KEEP / INCIDENT_EVIDENCE.
55. Test that locked story/canon hashes are copied as references only and never mutated by checkpoint tool.
56. Run anti-bloat review after two pilots and delete fields that never change a recovery decision.

## H — Packaging / rollout / next release

57. Reconcile 18C into the next engine package only after full-package regression; do not relabel v11.2.
58. Add checkpoint capability to machine execution pointer with exact tool/schema/test blob SHAs after merge.
59. Create migration note for systems using old SAFE/ZERO_COST/REVERSIBLE pointer semantics.
60. Run full engine regression after machine-pointer correction and checkpoint inclusion.
61. Create a Drive CURRENT mirror only after GitHub canonical integration readback.
62. Add START_HERE recovery card linking 13/17/18B/18C and explaining routing boundaries.
63. Run independent Red Team on real incident evidence after first actual abrupt-session recovery.
64. Promotion decision: VERIFIED_CURRENT / NARROW / HOLD / ROLLBACK based on real recovery evidence and measured overhead.
