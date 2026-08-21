# RUN35 — PROMPTS 01–32 EXECUTION REPORT

Status: EXECUTED SEQUENTIALLY; final CI/Drive/freshness disposition appended after gates.

01. Restore current main / SI authorities. — PASS. Cycle6 is current review surface; SI-0012 PILOTING; SI-0014 READY_FOR_PILOT.
02. Inspect SI-0012 transaction semantics. — PASS. Legacy stale/no-effect/ready/readback contract isolated.
03. Inspect SI-0014 recovery semantics. — PASS. Multi-store reconciler retained as richer recovery owner.
04. Dedupe the two mechanisms. — PASS. Decision: converge at interface; no third durable writer.
05. Define common decision vocabulary. — PASS. STOP/REBASE/quarantine/verify/dispatch/safe-action/complete vocabulary established.
06. Protect backward compatibility. — PASS. Existing direct SI-0012 and SI-0014 callers remain valid.
07. Design SI-0012 adapter. — PASS. Legacy READY maps to EXECUTE_MISSING_SAFE_ACTIONS; stale/no-effect remain STOP.
08. Design SI-0012 readback mapping. — PASS. exact readback -> TRANSACTION_COMPLETE; mismatch -> STOP.
09. Design SI-0014 delegation. — PASS. Facade calls existing reconciler; no planner copy.
10. Separate provider authorization from replay safety. — PASS. Domain/provider gate remains independent and upstream of paid dispatch.
11. Audit interruption-learning evidence model. — MAJOR_FOUND. Raw real_interruption bool could be self-asserted.
12. Define evidence qualification classes. — PASS. QUALIFIED_REAL / controlled / synthetic / unverified.
13. Exclude controlled evidence. — PASS. Controlled packets forced real_interruption=false.
14. Exclude synthetic evidence. — PASS. Synthetic packets forced false.
15. Downgrade incomplete raw-real claims. — PASS. Missing proof packet -> UNVERIFIED_REAL_CLAIM.
16. Define genuine unplanned origins. — PASS. UI session loss/process termination/runtime restart/network-platform disconnect.
17. Require restart observation. — PASS.
18. Require pre-interruption checkpoint identity. — PASS.
19. Require post-restart authority readback. — PASS.
20. Require recovery readback. — PASS.
21. Require before/after project-state identifiers. — PASS.
22. Require multiple durable evidence references. — PASS, with limitation: interface does not yet authenticate ref existence.
23. Preserve cross-project threshold. — PASS. 3 qualified real events / 2 projects remains minimum review threshold.
24. Preserve false-resume hard stop. — PASS. Any false resume -> HOLD.
25. Create regression design. — PASS. 17 targeted tests cover adapters, delegation, masquerade, threshold and false resume.
26. Sweep parallel open work for integrity conflicts. — FATAL_FOUND. PR #130 reused live SI-0014 for Project-slice Freshness from stale registry view.
27. Recompute candidate reservation state. — PASS. Full family + open PR search found SI-0015 unallocated; Cycle6 had not allocated it.
28. Repair PR #130 identity without touching story gate. — PASS. Project-slice moved SI-0015, colliding SI-0014 file deleted, redirect/family/PR metadata repaired; B03 prose remains blocked by separate Founder decision.
29. Implement interface/schema/contract/tests/workflow. — PASS. Additive Run35 surface created.
30. Execute CI and repair defects. — IN_PROGRESS HISTORY: run #1 = 16/17 new tests PASS; Python 3.12 dynamic-import harness defect fixed. Run #2 = 17/17 new tests PASS; inherited workflow path was wrong (`tests/test_session_resilience.py` nonexistent); repaired from authoritative Run32/Run33 workflow definitions. Final run pending.
31. Persist Drive evidence mirror and semantic readback. — IN_PROGRESS. Run35 folder created; 00/01/03/04 written; 02/05 final docs wait for final CI state.
32. Synthesize final disposition, derive 64 next prompts, freshness/rebase/merge gate. — IN_PROGRESS. 64 next prompts already derived; final disposition awaits CI + Drive + latest-main diff.

## Red Team severity summary
FATAL: PR130 duplicate SI-0014 identity — repaired before merge.
MAJOR: raw real-interruption self-certification — patched by qualification layer.
MAJOR: source-ref existence is not yet authenticated by interface — explicit limitation and next prompt.
MAJOR: CI inherited test path invented rather than read from authority — found on run #2 and repaired.
MEDIUM: measure packet/interface overhead on genuine incidents before promotion.

## Non-negotiable evidence boundary
Prompt completion count is not promotion evidence. Controlled/synthetic tests may expose defects and block promotion but cannot satisfy genuine interruption evidence.
