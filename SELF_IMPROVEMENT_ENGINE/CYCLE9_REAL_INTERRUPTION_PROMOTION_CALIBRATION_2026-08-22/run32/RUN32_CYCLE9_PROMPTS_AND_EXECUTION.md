# Cycle9 — 32 sequential prompts and execution

Ledger SHA-256: `42904e011c8e1ab98c4254e58d7469b968e41c68411b2a7892fd835c4610b4ff`

1. **C9-01 Restore CURRENT authority.** Prompt: restore exact CURRENT Self-Improvement authority, main SHA, registry and learning ledger. Result: **PASS** — v2 remains VERIFIED_CURRENT.
2. **C9-02 Fresh-main reconciliation.** Prompt: reconcile stale/parallel Cycle9 branches without force overwrite. Result: **PASS** — stale branch rejected; fresh writer path required.
3. **C9-03 Build Self-Improvement library index.** Prompt: normalize authority, private raw pointers, prior cycles and generated artifacts. Result: **PASS**.
4. **C9-04 Candidate-family freshness.** Prompt: inspect full SI family before proposing any new ID. Result: **PASS** — SI-0008..SI-0015 recognized; no new ID allocated.
5. **C9-05 Cycle7 dedupe.** Prompt: reuse durable transaction/recovery mechanisms rather than clone them. Result: **PASS**.
6. **C9-06 Cycle8 dedupe.** Prompt: preserve writing/story adapter evidence without creating a new global SI authority. Result: **PASS**.
7. **C9-07 Reference-ingest authority firewall.** Prompt: use Wave2 mechanisms as candidates only. Result: **PASS** — v3 remains HOLD.
8. **C9-08 SI-0014 contract extraction.** Prompt: extract exact promotion conditions. Result: **PASS** — >=3 genuine recoveries, >=2 projects, zero false resume.
9. **C9-09 SI-0015 contract extraction.** Prompt: extract exact pilot/promotion conditions. Result: **PASS** — real project pilot + healthy control + false-positive review remain required.
10. **C9-10 Classify browser/dialog interruption.** Prompt: classify the real incident without inflating evidence. Result: **PASS** — merged event-001 qualifies as one genuine recovery event; 2 project slices; false_resume=false.
11. **C9-11 Qualify SI-0014 event.** Prompt: determine promotion progress from event-001. Result: **PASS** — 1/3 genuine events, 2/2 projects, zero false resume; promotion remains false.
12. **C9-12 Project-slice positive pilot.** Prompt: verify matching CURRENT slice. Result: **PASS / CURRENT_MATCH**.
13. **C9-13 Historical negative control.** Prompt: ensure HISTORICAL/SUPERSEDED slice is not falsely flagged. Result: **PASS / EXEMPT_HISTORICAL_SLICE**.
14. **C9-14 False-resume canary.** Prompt: detect stale CURRENT slice. Result: **PASS / STALE_CURRENT_SLICE**.
15. **C9-15 Explicit approval firewall.** Prompt: prove RESUME/CONTINUE cannot replace required Founder approval. Result: **PASS / APPROVAL_EVENT_MISSING**.
16. **C9-16 Evidence-class firewall.** Prompt: prove automated tests cannot satisfy Human Signal. Result: **PASS**.
17. **C9-17 Meta-WIP limiter.** Prompt: allow one primary + up to two bounded pilots and reject excess active meta-work. Result: **PASS**.
18. **C9-18 Value-of-information router.** Prompt: reject metrics without a named decision/uncertainty and permit high-VOI measurement. Result: **PASS**.
19. **C9-19 Causal system model contract.** Prompt: require intended effect, feedbacks, delays, guardrails and compensating response. Result: **PASS**.
20. **C9-20 Policy-resistance gate.** Prompt: detect local metric improvement with system degradation. Result: **PASS / POLICY_RESISTANCE_DETECTED**.
21. **C9-21 Double-loop trigger.** Prompt: route repeated local failure to model/boundary review instead of another patch. Result: **PASS / DOUBLE_LOOP_REVIEW**.
22. **C9-22 Uncertainty ledger.** Prompt: preserve missing external evidence as UNKNOWN rather than fabricated PASS/FAIL. Result: **PASS**.
23. **C9-23 Measure-just-enough gate.** Prompt: collect only metrics that can change a decision and reduce material uncertainty. Result: **PASS**.
24. **C9-24 Decision-delta telemetry.** Prompt: separate decision change and information gain from activity/document counts. Result: **PASS**.
25. **C9-25 Mechanism semantic dedupe.** Prompt: duplicate functionality must MERGE, not clone. Result: **PASS / MERGE**.
26. **C9-26 False-positive pruning.** Prompt: high-FP mechanism must NARROW; unused mechanism must HOLD. Result: **PASS**.
27. **C9-27 Cross-store closure.** Prompt: require exact hashes; mismatch STOP; ambiguous irreversible effect QUARANTINE. Result: **PASS**.
28. **C9-28 Self-reference guard.** Prompt: attack the engine with a self-exemption mutation. Result: **PASS / REJECT_SELF_EXEMPTION**.
29. **C9-29 Direct-promotion adversarial fixture.** Prompt: attempt VERIFIED_CURRENT without application/readback. Result: **PASS / BLOCK_DIRECT_VERIFIED_CURRENT**.
30. **C9-30 v3 promotion calibration.** Prompt: determine whether reference-ingest v3 can become CURRENT now. Result: **HOLD** — no real production net-gain pilot.
31. **C9-31 Warm+cold package gate.** Prompt: run deterministic regression/package replay while keeping external evidence classes separate. Result: **PASS — 33/33 warm + 33/33 cold + compileall**.
32. **C9-32 Synthesis + Next64.** Prompt: synthesize decisions/residual uncertainty and derive exactly 64 evidence-driven next cards. Result: **PASS**.

## Final disposition
**31 PASS / 1 HOLD / 0 FAIL.** The remaining HOLD is top-level v3 promotion. SI-0014 is not promoted; it is READY_FOR_PILOT at 1/3 genuine interruption events and 2/2 project breadth with zero false resume.
