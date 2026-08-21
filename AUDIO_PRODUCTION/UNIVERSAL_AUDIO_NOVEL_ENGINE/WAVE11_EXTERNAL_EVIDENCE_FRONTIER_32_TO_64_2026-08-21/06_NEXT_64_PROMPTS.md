# Wave12 — 64 Next Evidence-Driven Prompts

Derived from Wave11 prompts 01–32 actual dispositions.
Status: READY BACKLOG / NOT AUTO-AUTHORIZED.
Law: execute in dependency order; every prompt may truthfully return HOLD. Do not bypass a higher-information external gate merely to increase completion count.

## A — MATERIALIZE AUTHENTICATED PROVIDER EVIDENCE
01. Run the merged read-only ElevenLabs provider snapshot workflow with `ELEVENLABS_API_KEY` configured only as a GitHub Actions repository secret; perform no synthesis and persist only secret-free output.
02. Read back the workflow artifact from durable storage and verify source bytes == readback bytes, logical ProviderSnapshot hash, file hash, provider identity and credential-persisted=false.
03. Validate the resulting bundle through canonical `AUTH_PROVIDER` class validation; record exact validator status and snapshot hash, never a caller boolean.
04. Verify snapshot capture age against the current <=6h production freshness gate at the moment of intended use; stale evidence becomes HOLD, never silently refreshed in memory.
05. Run a secret-field leakage scan over the emitted snapshot/receipt/artifact metadata; any credential-like field is FATAL and invalidates the bundle.
06. Record actual workflow/provider errors through the existing provider error taxonomy, including source/run identity; do not manufacture clean-error fixtures as real observations.
07. Persist a Wave12 provider-evidence pointer record containing run ID, artifact identity, snapshot hash, readback strength and expiry/freshness boundary, but no secret.
08. Issue `PROVIDER_BRIDGE_GO` only if 01–07 pass real evidence validation; otherwise persist one precise HOLD and stop provider-dependent descendants.

## B — REPEATABILITY, DRIFT AND REAL INVENTORY
09. Acquire a second read-only snapshot in a separate acquisition event without synthesis and validate it independently before comparison.
10. Compare account fingerprints first; if different, fail closed and prohibit inventory union, scoring or candidate carryover.
11. Run `provider_snapshot_diff.py` and persist exact model added/removed/changed sets plus metadata hashes; classify volatile usage separately from capability drift.
12. Run the same diff for voices; any removed/changed locked candidate requires downstream revalidation and never automatic substitution.
13. Compile the fresher valid snapshot through `provider_inventory_compiler.py`; persist inventory source snapshot hash and account fingerprint.
14. Prove at least one model has explicit observed `can_do_text_to_speech=true`; absent/unknown capability returns `HOLD_MODEL_CAPABILITY`.
15. Produce an inventory provenance report showing every candidate model/voice ID exists in the same current snapshot and every unknown metadata field remains null/unknown.
16. Red Team provider repeatability for stale snapshot reuse, cross-account mixing, removed voice reuse, public-doc/account-data confusion and hidden fallback IDs.

## C — REAL CANDIDATE SET + AUDITION MANIFEST
17. Generate a bounded NARRATOR candidate set from the current verified inventory using explicit role criteria; preserve every real voice ID as UNLOCKED and source-hash-bound.
18. Generate the ETHAN candidate set under the same inventory/account/model boundary; reject remembered ROOM917/D04 or other-project IDs unless they independently appear in the current inventory.
19. Generate the AOIFE candidate set; metadata may filter logistics/accent/category but may not claim correct `Ифа` pronunciation or performance quality.
20. Run candidate-contamination audit across NARRATOR/ETHAN/AOIFE: same voice ID reused across conflicting role hypotheses must be explicit, not accidental.
21. Bind candidates through `cast_readiness.py`; reject any voice or model missing from the exact current inventory.
22. Freeze one audition candidate manifest with provider snapshot hash, model ID, candidate IDs, candidate hashes, pronunciation terms, multi-state/pair/fatigue requirements and no voice lock.
23. Generate exact minimum audition request plans from the frozen manifest; no provider dispatch yet and no text drift from the authoritative audition source.
24. Recompute manifest/request hashes after a fresh provider drift check; any inventory/model/voice change creates a new manifest version rather than mutating the old one.

## D — PRONUNCIATION, PERFORMANCE AND TRUSTED HUMAN EVIDENCE
25. Render the minimum real `Ифа` pronunciation audition only for current manifest candidates, preserving request/provider/raw/spend lineage and clean dry masters.
26. Render the minimum real `Контакт` audition under identical lineage discipline; do not reuse a result from another role/candidate as equivalent evidence.
27. Run `NATURAL_RESTRAINED` vs `DIRECTED_CHANGE` real multi-state audition and capture whether direction produces an audible, repeatable performance change.
28. Render the ETHAN/AOIFE pair test loudness-matched with music/reverb/heavy processing off; preserve individual stems and pair assembly hash.
29. Run 8–10 minute real fatigue/listenability audition for surviving candidates and prepare headphone/mono/phone translations without destructive overwrite.
30. Collect trusted human PRONUNCIATION attestations bound to artifact/candidate/task hashes; synthetic/model review remains inadmissible.
31. Collect trusted MULTI_STATE/PAIR/FATIGUE/PERFORMANCE attestations and append them to the immutable human-review ledger, preserving FAIL/HOLD history.
32. Compile role-by-role human lock eligibility; the machine may report eligibility and contradictions but may not select or lock a winner.

## E — EXPLICIT LOCK, PRE-SPEND AND EXACT PAID CANARY
33. Present the complete evidence packet to the authorized human/Founder and persist explicit NARRATOR/ETHAN/AOIFE/model lock or explicit HOLD with hashes.
34. If locked, bind model+voice IDs to immutable RB001/RB002/RB003 source/request identities; any later text/model/voice change invalidates the affected request hash.
35. Re-run authenticated capability/freshness drift immediately before spend; removed/changed locked capability = FAIL_NO_SUBSTITUTION.
36. Build and verify the exact pre-spend manifest: 3 requests, 36 spoken units, 2163 characters, expected output handling, idempotency identities, spend ceiling and ambiguity quarantine.
37. Independently verify that no request hash or paid transaction identity already exists in accepted/ambiguous lineage before dispatch.
38. Obtain explicit pre-spend GO bound to the exact manifest hash; engineering tests, continuation commands and machine confidence cannot authorize spend.
39. Dispatch RB001 only and atomically persist request receipt, provider result receipt, spend receipt, raw asset receipt and live-lineage escrow before any other paid request.
40. Run real human RB001 sanity check for catastrophic identity/pronunciation/performance error; PASS unlocks RB002, FAIL routes earliest-cause repair, ambiguity blocks all further paid dispatch.

## F — SEQUENTIAL CANARY, ALIGNMENT, TIMELINE AND MIX
41. If RB001 passes, dispatch RB002 only; persist the same durable lineage family and require resolution before RB003.
42. If RB002 passes, dispatch RB003; compile exact-three lineage escrow and prove no unknown fourth request, duplicate request hash, duplicate provider call or duplicate charge.
43. Canonically ingest RB001/RB002/RB003 real assets to accepted 48k production representation without overwriting provider-original bytes/provenance.
44. Normalize real alignment for each asset, bound to source/audio hashes; malformed/nonmonotonic/incomplete alignment quarantines the affected asset.
45. Prove exactly 36/36 spoken units appear once across the combined real alignment; no missing, duplicate or invented unit/timestamp.
46. Resolve actual timeline, protected silence and acoustic transitions only from real alignment/audio; no pre-render absolute timestamp authority survives.
47. Build one sparse evidence-preserving mini-mix with separate dialogue/SFX/roomtone/music stems, explicit null stems and clean-master preservation.
48. Run mono/mobile/headphone QC, clue intelligibility, spatial legibility, clipping/headroom/seam checks; route every failure to earliest causal layer and prohibit unrelated rerender/spend.

## G — REAL HUMAN BENCHMARK AND MEASURED ECONOMICS
49. Build same-source loudness-matched NARRATED/MULTI_VOICE/DRAMATIZED real variants with blinded identity keys separated from listener packs.
50. Pre-register listener questions/thresholds for believability, clarity/comprehension, clue retention, want-more and fatigue/AI distraction before collecting responses.
51. Collect real one-listen believability responses with listener/device/session/artifact hashes and freeze raw answers before scoring.
52. Collect clarity/comprehension + clue-retention responses without correcting listeners during the scored block.
53. Collect want-more/engagement responses without disclosing the preferred mode or producer hypothesis.
54. Collect fatigue/AI-distraction responses and code cause separately as voice/performance/edit/mix/test-design rather than one generic quality score.
55. Persist measured provider charges, generated/accepted seconds, manual minutes, cache reuse, regeneration seconds and rerender waste with source refs; unknown stays null.
56. Compute cost per accepted minute only from real charge/time provenance and report quality/economics separately; no machine auto-selection of artistic mode.

## H — RECOVERY, SELF-IMPROVEMENT, PORTABILITY AND RELEASE
57. Execute one restart/recovery readback over a completed real paid lineage without re-calling the provider; prove transaction-recoverable content coverage and zero duplicate charges.
58. Feed only real defects into learning records as `DEFECT → ROOT CAUSE → REPAIR → RETEST → RESULT → REUSE CONDITIONS`; exclude opinions without evidence.
59. Evaluate `DEPENDENCY_AWARE_EXTERNAL_EVIDENCE_FRONTIER` on this real provider+human run: count false completions prevented, false blocks introduced, skipped gates and duplicate-spend incidents.
60. Replicate the same frontier on a second real locked audio project while preventing transfer of project-specific voice/story/acoustic facts.
61. Run a third project or protected no-change control and require the mechanism to permit progression when evidence is actually complete; measure false blocking.
62. Compare the candidate mechanism against SI-0014 recovery and SI-0015 freshness/approval-event responsibilities; promote only unique non-duplicative scope and count duplicate evidence once.
63. Run independent Red Team across provider trust, human evidence, live lineage, spend, recovery, alignment, portability and Self-Improvement authority escalation; FATAL/MAJOR findings block universal promotion/release.
64. Produce the Founder V1 decision packet with current hashes, real evidence classes, unresolved HOLDs, economics, listener evidence and exact next experiment. `PRODUCTION_READY` is allowed only when the real cross-bound evidence and authorized decision exist.

## Derivation summary
Wave11 showed that prompts 02–32 are not independent work items; they are descendants of a real provider-authentication edge. Wave12 therefore concentrates the first 16 prompts on materializing, repeating and verifying provider evidence before any candidate/audio work, then keeps human lock and paid dispatch as explicit typed boundaries.
