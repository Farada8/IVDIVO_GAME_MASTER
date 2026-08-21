# WAVE11 — 64 EVIDENCE-DRIVEN NEXT PROMPTS

Derived from Wave10. READY / NOT AUTO-AUTHORIZED. Execute in dependency order and stop at the first higher-information real gate. Every prompt must preserve the evidence ceiling and may return HOLD.

## A — AUTHENTICATED PROVIDER SNAPSHOT + REPEATABILITY 01–08
01. Run the merged read-only provider workflow with an externally configured runtime secret; persist only the secret-free AUTH_PROVIDER evidence bundle. PASS only on canonical receipt validation.
02. Read back the first evidence artifact and independently verify ProviderSnapshotContract, durable receipt binding, age <= 6h and zero secret-bearing fields.
03. Acquire a second read-only snapshot without synthesis; compare with `provider_snapshot_diff.py`; separate capability drift from volatile usage drift.
04. If account fingerprint differs across snapshots, stop and classify account-identity drift; do not combine inventories.
05. Compare model added/removed/changed sets; record exact model metadata hashes; never infer missing capability flags.
06. Compare voice added/removed/changed sets; record exact voice metadata hashes; never auto-substitute a changed/missing voice.
07. Classify observed provider errors using current production-control taxonomy; persist only real observed errors, not hypothetical incidents.
08. Issue Provider Bridge GO/HOLD: GO only if current authenticated snapshot is durable, fresh and inventory-consumable; otherwise return exact blocker.

## B — INVENTORY + PROVISIONAL CAST 09–16
09. Compile the real snapshot through `provider_inventory_compiler.py`; persist normalized real model/voice inventory bound to source snapshot hash.
10. Verify at least one explicitly TTS-capable current model; if none, HOLD_MODEL_CAPABILITY rather than guessing compatibility.
11. Generate NARRATOR candidate pool from real inventory metadata and explicit casting criteria; preserve all real IDs and mark UNLOCKED.
12. Generate ETHAN candidate pool under the same no-auto-lock/no-auto-substitution law.
13. Generate AOIFE candidate pool under the same law; do not infer pronunciation quality from name/metadata.
14. Bind provisional candidate lists through `cast_readiness.py`; reject every ID absent from the same current snapshot.
15. Red Team candidate-pool contamination: ensure no ROOM917/D04/project-specific voice ID is inherited merely because it worked elsewhere.
16. Freeze one versioned audition candidate manifest for the next human-heard tests; changing snapshot/candidate IDs must produce a new manifest hash.

## C — PRONUNCIATION + PERFORMANCE EVIDENCE 17–24
17. Render the minimum real pronunciation audition needed to hear canonical `Ифа`; bind audio hash to candidate/role/manifest.
18. Render the minimum real pronunciation audition needed to hear canonical `Контакт`; preserve exact source term and evidence lineage.
19. Obtain trusted human PRONUNCIATION review for NARRATOR candidates; synthetic/model review cannot satisfy it.
20. Obtain trusted human PRONUNCIATION review for ETHAN/AOIFE candidates as required by the actual canary lines.
21. Run NATURAL_RESTRAINED vs DIRECTED_CHANGE multi-state audition for surviving candidates; require audible response to direction.
22. Run ETHAN/AOIFE pair gate on matched loudness with music/reverb/heavy processing OFF.
23. Run 8–10 minute fatigue/listenability test for surviving candidates; include headphones/mono/phone translation checks where applicable.
24. Compile trusted multi-state/pronunciation/pair/fatigue/performance receipts through current Studio Evidence; machine may only report ELIGIBLE_FOR_HUMAN_LOCK_DECISION, never lock.

## D — LOCK + PRE-SPEND + EXACT LIVE CANARY 25–32
25. Present surviving candidate evidence to the authorized human/Founder cast decision; persist explicit lock or HOLD with candidate hashes.
26. Bind locked NARRATOR/ETHAN/AOIFE voice IDs and chosen current model to immutable LESSON ZERO RB001/RB002/RB003 request hashes.
27. Re-run current capability drift gate immediately before paid dispatch; fail on missing/changed locked voice/model and forbid substitution.
28. Build exact pre-spend manifest: 3 requests / 36 spoken units / 2163 characters, expected charge basis if provider exposes it, idempotency keys and rollback/quarantine semantics.
29. Require explicit pre-spend GO; no paid request may auto-dispatch from a planning/test result.
30. Dispatch RB001 only; persist request/response IDs, raw bytes hash, spend ledger transition and durable receipt before any next paid request.
31. Human sanity-check RB001 for catastrophic identity/pronunciation/performance failure; if FAIL, stop and repair earliest failing layer before RB002.
32. If RB001 passes the bounded sanity gate, dispatch RB002 then RB003 sequentially under the same idempotent escrow; never batch past an unresolved ambiguity.

## E — REAL ALIGNMENT + TIMELINE 33–40
33. Canonically ingest each real canary audio asset at 48 kHz without overwriting raw provider bytes/provenance.
34. Normalize provider alignment for RB001 and bind exact source units to raw audio hash.
35. Normalize RB002 alignment under the same schema.
36. Normalize RB003 alignment under the same schema.
37. Prove exactly 36/36 spoken units appear once across the combined real alignment; zero duplication/omission.
38. Resolve actual timeline boundaries only from real alignment/audio; do not invent absolute timestamps from pre-render plans.
39. Bind protected silence and acoustic-domain transitions to the resolved real timeline; fail closed on overlap violations.
40. Persist durable REAL_ALIGNMENT receipt and current-lineage cross-bind to the same live audio transaction.

## F — SOUND / SPACE / MIX + SELECTIVE REPAIR 41–48
41. Map CUE_008 ambience to the real canary timeline and current acoustic passport; no generic bed substitution.
42. Map CUE_009 recorder Foley causally to the source action and real timing.
43. Map CUE_010 diegetic performance sound while preserving intelligibility and clue function.
44. Enforce CUE_011 protected silence as an active no-fill mask across ambience/music/processing.
45. Evaluate whether deferred CUE_012 music is functionally earned after real performance; default remains no music if it masks a performance defect.
46. Build one sparse mini-mix with explicit stems and null/missing-asset handling; preserve raw and clean voice masters.
47. Run mono/mobile/headphone QC plus clue intelligibility and spatial-legibility checks; machine metrics remain diagnostic.
48. Route failures through earliest-cause selective repair; invalidate only dependent artifacts and prove no unrelated rerender/spend.

## G — HUMAN BENCHMARK + ECONOMICS 49–56
49. Build loudness-matched same-source NARRATED / MULTI_VOICE / DRAMATIZED variants using the real canary source and locked evidence lineage.
50. Blind variant identity for human evaluation; keep scoring key separate from listener-facing pack.
51. Collect real human believability ratings with exact artifact hashes.
52. Collect clarity/comprehension and clue-retention responses.
53. Collect want-more/engagement responses without leading the listener toward a preferred mode.
54. Collect fatigue/AI-distraction responses; separate voice, performance, edit, mix and test-design failure categories.
55. Measure provider spend, generated seconds, accepted seconds, manual minutes, cache reuse and rerender waste; unknown values remain null.
56. Compute cost per accepted minute only from measured evidence and attach charge/time provenance; no estimated value may masquerade as measured economics.

## H — PORTABILITY / SELF-IMPROVEMENT / RELEASE 57–64
57. Feed only evidenced defects/repairs into `learning_registry`: DEFECT -> ROOT CAUSE -> REPAIR -> RETEST -> RESULT -> REUSE CONDITIONS.
58. Compare ProviderSnapshot repeatability behavior across a second acquisition window; determine whether any provider-drift rule deserves candidate status.
59. Replicate provider→cast readiness on a second locked audio project without transferring LESSON ZERO voice IDs, story facts or acoustic values.
60. Replicate on a third project or protected no-change control; verify that the mechanism can also recommend NO CHANGE/HOLD.
61. Audit Cycle7 SI-0012/SI-0014 transaction interface during one genuine interruption if one naturally occurs; never manufacture an interruption and label it real.
62. Compile cross-project proof families; duplicate evidence families count once and one-project success cannot promote universal authority.
63. Independent Red Team Audio Novel Engine v1: causality of evidence chain, provider/cast trust, live lineage, human evidence, economics, recovery, portability; classify FATAL/MAJOR/MEDIUM/POLISH.
64. Produce Founder-facing V1 decision packet. PRODUCTION READY may be proposed only if every required external evidence family is real, current, cross-bound and sufficient; otherwise output precise HOLD + next highest-information experiment.
