# Cycle9 — Next 64 Evidence-Driven Prompts

These are derived from the 32-run residual uncertainty. They are a dependency-aware backlog, not an autoplay ritual.

1. **C9N01** — Recover one explicitly named closed-chat project from persisted GitHub/Drive state and produce a verified frontier card.
2. **C9N02** — For that project, compare reconstructed frontier with the newest controlling project state; classify exact matches, stale fields, and unknowns.
3. **C9N03** — Run a false-resume adversarial test: feed one superseded frontier and prove it is rejected.
4. **C9N04** — Run a missing-chat-only-work test and prove absence is reported rather than reconstructed.
5. **C9N05** — Measure time-to-authoritative-resume for the first recovered project; record measured seconds/minutes, not estimates.
6. **C9N06** — Record every manual Founder intervention required during recovery and classify avoidable vs irreducible.
7. **C9N07** — Complete readback of the first recovered project slice and decide whether the observed browser incident becomes one qualifying SI-0014 recovery event.
8. **C9N08** — If C9N07 qualifies, append exact evidence to the learning ledger; otherwise persist failure reason and remediation.
9. **C9N09** — Recover a second project from the same browser interruption using only persisted sources; no chat-memory authority.
10. **C9N10** — Compare recovery performance between project 1 and project 2 and identify shared vs project-specific failure modes.
11. **C9N11** — Run project-slice freshness assertion on both recovered projects using SI-0015 READY_FOR_PILOT semantics.
12. **C9N12** — Prove stale embedded CURRENT slices route REBASE_FIRST rather than overwrite current project state.
13. **C9N13** — Test a project with multiple parallel branches and construct one non-destructive semantic salvage plan.
14. **C9N14** — Test a project whose latest work exists only in Drive and verify GitHub absence does not get normalized away.
15. **C9N15** — Test a project whose latest work exists only in GitHub and verify Drive absence becomes PARTIAL_PERSISTENCE.
16. **C9N16** — After two project recoveries, decide whether the incident provides cross-project evidence while still counting as only one interruption event.
17. **C9N17** — Build an exact GitHub↔Drive persistence manifest schema with artifact id, path, revision/blob SHA, authority role, and readback status.
18. **C9N18** — Generate the manifest for Cycle9 and verify every material artifact is present in at least one controlling store plus its mirror role.
19. **C9N19** — Create a same-path concurrent-write canary and prove stale writer is blocked without force update.
20. **C9N20** — Create a different-path concurrent-write canary and prove compatible additive writes can coexist.
21. **C9N21** — Test a branch that is ahead and behind main; classify REBASE/SALVAGE/HOLD using semantic scope, not commit count alone.
22. **C9N22** — Test Drive document revision drift during a GitHub write and require post-write Drive reread before closure.
23. **C9N23** — Define deterministic partial-persistence repair order for GitHub-only, Drive-only, stale-router, and stale-index cases.
24. **C9N24** — Run a full cross-store closure canary and prove COMPLETE only after both store readbacks.
25. **C9N25** — Create Recovery Incident Ledger schema v1 with event, project slices, evidence stages, false-resume outcome, and qualification state.
26. **C9N26** — Add current browser interruption as OBSERVED_REAL_EVENT without qualifying it prematurely.
27. **C9N27** — Create a dedupe key so one interruption affecting many projects is not miscounted as many interruption events.
28. **C9N28** — Define independent interruption-event identity rules: timestamp window, session/browser event, project scope, and provenance.
29. **C9N29** — Add null-safe recovery telemetry fields to the learning ledger adapter without converting unknown to zero.
30. **C9N30** — Build a promotion counter for SI-0014 that counts only QUALIFIED events and enforces >=3 events across >=2 projects.
31. **C9N31** — Run adversarial fixtures for duplicate events, partial recovery, false resume, and missing readback.
32. **C9N32** — Decide whether SI-0014 needs contract extension or only new evidence records; no new SI ID unless dedupe proves novelty.
33. **C9N33** — Apply v3 S5 authority layer to one real cross-dialog recovery and list concrete decisions improved vs v2.
34. **C9N34** — Apply v3 S4 value-of-information layer and compare chosen recovery action with FIFO/prompt-order baseline.
35. **C9N35** — Apply v3 S3 reliability layer and define error budget for false resume and unresolved persistence mismatches.
36. **C9N36** — Apply v3 S2 flow layer and measure WIP/queue reduction from dependency-aware selection.
37. **C9N37** — Apply v3 S1 production-return layer and prove meta-work hands control back to a product/project frontier.
38. **C9N38** — Run a double-loop escalation test on a recurring recovery defect; determine whether the causal model or local patch should change.
39. **C9N39** — Compare v3 candidate mechanisms to existing v2/SI-0014/SI-0015 implementations and remove duplicate layers.
40. **C9N40** — Hold a v3 bounded tribunal: KEEP_LOCAL / MERGE_INTO_V2 / HOLD / REJECT for each surviving mechanism.
41. **C9N41** — Pilot SOURCE_ADEQUACY_GATE on a recovery summary that lacks scene/project details and prove no invented defect.
42. **C9N42** — Pilot evidence-family dedupe on multiple model summaries of the same recovery corpus.
43. **C9N43** — Pilot approval-event typing on RESUME vs FOUNDER_LOCK vs CANON_APPROVAL vs RELEASE_APPROVAL in one real project.
44. **C9N44** — Pilot registry reservation view against current main plus open PRs before any new SI number allocation.
45. **C9N45** — Pilot transaction recovery after a deliberately interrupted reversible write in a non-authority test path.
46. **C9N46** — Pilot irreversible-side-effect quarantine on a dry fixture; no real paid/provider action.
47. **C9N47** — Pilot engine-worthiness gate on a proposal that restates transcript recovery; require EXTEND/REJECT instead of BUILD.
48. **C9N48** — Pilot library completeness gate after adding one new uploaded reference source; update metadata without copying copyrighted raw bytes to public GitHub.
49. **C9N49** — Select one currently active book/story project and verify its project state can be resumed after browser closure without reopening locked prose.
50. **C9N50** — Select one audio project and verify source-lock + audio state can be resumed without treating machine QC as Human Signal.
51. **C9N51** — Select one business-engineering project and verify stale-branch salvage law after recent parallel main advances.
52. **C9N52** — Select the Discovery Engine draft lane and classify current branch as current/salvage/stale without merging by age alone.
53. **C9N53** — For each of the four project classes, record which self-improvement mechanisms transfer cleanly and which remain domain-specific.
54. **C9N54** — Measure false-positive rate of recovery/freshness guards on healthy current project slices.
55. **C9N55** — Measure false-negative cases where stale or incomplete state incorrectly appears resumable.
56. **C9N56** — Use the results to prune or tighten contracts before any universal promotion.
57. **C9N57** — Design minimal real Human Signal plan for one story/audio output; do not simulate listener/editor responses.
58. **C9N58** — If provider evidence is available, capture authenticated provider result separately from model interpretation; otherwise HOLD.
59. **C9N59** — Measure actual manual recovery burden over at least two real resume operations; keep unknown values null.
60. **C9N60** — Measure avoided duplicated work from stale-queue detection using actual before/after actions, not hypothetical savings.
61. **C9N61** — Record one real external dependency failure and test whether the engine routes to HOLD rather than fake completion.
62. **C9N62** — Compare real recovery evidence with synthetic canary evidence and keep promotion weights/classes separate.
63. **C9N63** — After enough real evidence, review SI-0014 promotion conditions; if unmet, persist exact missing conditions.
64. **C9N64** — Cycle9/10 governor closure: read newest main/Drive authority, prune low-information backlog, choose one highest-information next action, and stop meta expansion unless Founder explicitly continues it.

## Governor
Stop or reorder the backlog whenever a newer authority, real Founder decision, genuine Human/provider evidence, or a higher-information production gate supersedes the current sequence.
