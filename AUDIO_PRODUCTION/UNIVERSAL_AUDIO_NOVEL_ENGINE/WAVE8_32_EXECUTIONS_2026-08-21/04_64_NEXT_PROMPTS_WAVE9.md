# WAVE9 — EXACTLY 64 TRUST-ANCHORED PROMPTS

Derived after Wave8 32/32 execution + CI/recovery + independent Red Team. Execute by dependency, not ritual order. For every prompt: `P=` prerequisite; `E=` evidence required; `G=` exact PASS/HOLD condition; `X=` forbidden fake evidence.

## A — Authority / stale-state / recovery / trust anchors
01 **FRESH MAIN READBACK** — P: none. E: main SHA, open/merged relevant PRs, Drive revision. G: PASS if one consistent current frontier is frozen for this work block; HOLD on concurrent unresolved state movement. X: stale chat snapshot.
02 **FRESH-MAIN FUNCTION DIFF** — P:01. E: changed paths/functions touching provider/evidence/recovery/PMV/SI. G: PASS when each is REUSE/COMPATIBLE/CONFLICT/SUPERSEDES; HOLD on unreviewed overlap. X: filename-only equivalence.
03 **WAVE8 DOC/SCHEMA VERSION SYNC** — P:01–02. E: runtime/schema/protocol versions. G: PASS when prose matches executable evidence classes including REAL_ALIGNMENT/DURABLE_RECOVERY; HOLD on drift. X: docs claiming code not present.
04 **PROOF SOURCE-VALIDATOR CONTRACT** — P:02–03. E: evidence_class→validator→source ref/hash/readback mapping. G: PASS only when caller assertions cannot satisfy external classes alone. X: `verified=true` as external truth.
05 **HUMAN ATTESTATION CONTRACT** — P:04. E: reviewer submission/attestation binding, artifact hash, timestamp, durable readback. G: PASS when synthetic fixtures are excluded from HUMAN production gates. X: machine-created “human” event.
06 **DURABLE CONTENT READBACK CONTRACT** — P:04. E: pointer/readability/hash/transaction-recovery states. G: PASS only at CONTENT_HASH_VERIFIED + TRANSACTION_RECOVERABLE where required. X: pointer presence as durability.
07 **PROVIDER PREFLIGHT SOURCE BINDING** — P:04. E: authenticated preflight source ref/hash/readback bound to snapshot. G: PASS when snapshot cannot self-prove AUTH_PROVIDER. X: snapshot hash alone.
08 **FRESH MERGE-RESULT CI GATE** — P:01–07 integrated. E: run/job IDs, exact SHA, dedicated+full suite result. G: PASS on fresh green CI; HOLD/FAIL otherwise. X: old green run relabeled fresh.

## B — Provider / authentication / capability
09 **PROVIDER ACCESS SURFACE INVENTORY** — P:08. E: available authenticated surfaces, read-only/spend authority, secret boundary. G: PASS if at least one admissible path is identified or exact BLOCKED_EXTERNAL is recorded. X: assumed connector/account access.
10 **RUNTIME-ONLY SECRET INGEST** — P:09. E: negative fixtures for key/token/cookie persistence. G: PASS if secrets exist only ephemerally and persisted artifacts are secret-free. X: credentials in chat/GitHub/Drive.
11 **FIRST AUTHENTICATED PREFLIGHT CAPTURE** — P:09–10. E: real read-only provider calls + source artifact/hash/auth outcome. G: PASS only on authenticated readback; HOLD_EXTERNAL when credential unavailable. X: fabricated account/quota/model/voice values.
12 **PROVIDER SNAPSHOT COMPILE + SOURCE BIND** — P:11 PASS. E: validated secret-free snapshot, source binding, stable/volatile hashes. G: PASS on schema/hash/provenance/freshness validation. X: hand-authored snapshot claimed real.
13 **TARGETED VS ACCOUNT-WIDE PROOF** — P:12. E: source-side enumeration coverage. G: PASS when scope cannot be inflated by caller flags. X: ACCOUNT_WIDE from TARGETED data.
14 **SNAPSHOT REPEATABILITY DIFF** — P:12. E: second authenticated snapshot. G: PASS if stable drift classified and no silent substitution; HOLD on unexplained drift. X: copied first snapshot.
15 **REQUIRED MODEL/VOICE CAPABILITY PROBE** — P:12–14. E: current provider evidence for exact required models/voices/output/alignment. G: PASS for proven capabilities only; HOLD for unknown IDs/features. X: model-name assumptions.
16 **PROVIDER BRIDGE RELEASE GATE** — P:11–15. E: class-validated AUTH_PROVIDER proof + freshness. G: PASS to casting only if complete; HOLD at earliest missing provider prerequisite. X: CI/code as provider proof.

## C — Casting / pronunciation / performance
17 **LESSON ZERO VOICE PASSPORT READBACK** — P:16. E: current project authority for Narrator/Ethan/Aoife only. G: PASS on exact role requirements with zero sibling leakage. X: ROOM917/BODYGUARD voice facts.
18 **NARRATOR REAL-ID BASELINE** — P:17 + current snapshot. E: real candidate ID from bound inventory. G: PASS_BASELINE_ID only; quality remains UNKNOWN until heard. X: invented ID/quality.
19 **ETHAN REAL-ID BASELINE** — P:17 + current snapshot. E: real ID + rationale. G: PASS_BASELINE_ID only. X: adult-leading-man suitability asserted without audio.
20 **AOIFE REAL-ID BASELINE** — P:17 + current snapshot. E: real ID + rationale. G: PASS_BASELINE_ID only. X: therapist/flirt verdict without heard evidence.
21 **ИФА HUMAN MICRO-REVIEW** — P:18–20 + minimal real render. E: audio/source/candidate hashes + trusted human attestation. G: PASS pronunciation only on actual heard consistency; HOLD otherwise. X: phonetic text rule as heard result.
22 **КОНТАКТ HUMAN MICRO-REVIEW** — P:18–20. E: both protected contexts + attested heard review. G: PASS only with exact source unchanged and heard consistency. X: source rewrite to force PASS.
23 **NARRATOR MULTI-STATE HUMAN EVIDENCE** — P:18,21/22 as relevant. E: natural/private/pressure/technical audio + bound reviews. G: PASS when direction response and fatigue risk acceptable. X: machine score as human quality.
24 **ETHAN + AOIFE MULTI-STATE EVIDENCE** — P:19–22. E: real state renders + attested age/status/listening reviews. G: PASS when both survive hard fails. X: chemistry/age guessed from metadata.

## D — Pair / fatigue / lock / pre-spend
25 **ETHAN–AOIFE BLIND PAIR PACK** — P:24. E: opaque randomized labels, frozen questions/playback. G: PASS_PACKAGE when contamination-free pack exists; quality result pending humans. X: visible candidate identities.
26 **TRUSTED PAIR REVIEW INGEST** — P:25. E: externally attested submissions bound to pack/audio. G: PASS if provenance valid and conflicts stay HOLD. X: synthetic reviews satisfying HUMAN_REVIEW.
27 **NARRATOR 3–5 MIN FATIGUE PREFLIGHT** — P:23. E: longer real render + attested listen. G: PASS if acceptable listenability across states; HOLD/FAIL on fatigue evidence. X: short clip extrapolated to fatigue.
28 **HUMAN EVIDENCE FAMILY COVERAGE** — P:21–27. E: pronunciation/state/pair/fatigue/blind families bound to same candidate identities. G: PASS when required families complete and non-conflicting. X: mixed candidate/model/settings evidence.
29 **LOCK ELIGIBILITY COMPILER** — P:28. E: complete valid evidence ledger. G: output only ELIGIBLE_FOR_HUMAN_LOCK_DECISION/HOLD/FAIL_HARD. X: machine `voice_lock=true`.
30 **AUTHORIZED HUMAN/FOUNDER LOCK DECISION** — P:29 eligible. E: explicit authorized decision ref/hash. G: PASS_LOCK only after authority decision. X: inference from reviewer majority.
31 **LOCK INVALIDATION DRILL** — P:30. E: controlled change to snapshot/model/voice/settings identity + dependency graph. G: PASS if only declared descendants invalidate. X: silent retained stale lock.
32 **EXACT PRE-SPEND GO/NO-GO** — P:16,30–31. E: exact 3 requests/36 units/2163 chars, immutable hashes, three locks, pronunciation locks, measured spend ceiling. G: GO only if all complete; otherwise HOLD naming earliest prerequisite. X: estimated provider evidence or missing lock treated as GO.

## E — Live render / provenance / alignment
33 **RB001 CONTROLLED LIVE DISPATCH** — P:32 GO. E: one paid request, request hash/ID, response, terminal spend, raw bytes, alignment if returned. G: PASS_PROVIDER_ACCEPTED only on one traceable lineage; take still unlocked. X: second request/retry without reconciliation.
34 **RB001 CLASS-SPECIFIC RECEIPT VALIDATION** — P:33. E: content identities for request/response/audio/alignment/spend/charge. G: PASS when every required class validator passes. X: pointer membership as content proof.
35 **RB001 HUMAN SANITY GATE** — P:34. E: actual listen for identity/age/pronunciation/artifact. G: PASS only on attested human sanity result. X: waveform metrics as listening.
36 **RB001 RESTART RECOVERY** — P:34. E: fresh process/session reconstruction + hashes. G: PASS when no provider replay and recovered content matches. X: chat memory or pointer-only recovery.
37 **RB002 CONTROLLED DISPATCH + RECEIPTS** — P:35–36 PASS. E: independent lineage/charge/content. G: PASS on one accepted traceable request. X: duplicate spend or inherited RB001 IDs.
38 **RB002 PAIR SANITY GATE** — P:37. E: real human distinction/status/listening review. G: PASS/HOLD from attested review. X: metadata-only pair judgment.
39 **RB003 CONTROLLED DISPATCH + RECEIPTS** — P:38 PASS. E: narrator-only independent lineage + pronunciation check. G: PASS_PROVIDER_ACCEPTED with complete receipts. X: reused request identity.
40 **EXACT THREE-LINEAGE DURABLE ESCROW** — P:33–39. E: exactly RB001/RB002/RB003 request/response/audio/alignment/spend/charge content readback using SI-0014-compatible recovery. G: PASS only with no duplicate/unknown fourth lineage and fresh recovery. X: three pointers without verified contents.

## F — Timeline / Foley / spatial / music / mix
41 **CANONICAL 48K INGEST** — P:40. E: provider/source hash, explicit format metadata, conversion/resample proof. G: PASS on valid canonical assets. X: assumed sample rate/channels.
42 **36/36 SPOKEN-UNIT COVERAGE** — P:41. E: accepted real alignment mapping U001–U036. G: PASS only every unit exactly once. X: synthetic/guessed alignment.
43 **REAL ALIGNMENT PROOF MANIFEST** — P:42. E: validated alignment hash/ref bound to source/audio/request lineage. G: PASS_REAL_ALIGNMENT only with validated artifact. X: LIVE_AUDIO as alignment proof.
44 **ALIGNMENT OUTLIER HUMAN REVIEW** — P:43. E: machine flags + human review of suspicious durations. G: PASS/repair decision from evidence; HOLD unresolved. X: automatic source rewrite.
45 **CUE008–012 SAMPLE-ACCURATE RESOLUTION** — P:43–44. E: accepted real alignment/audio. G: PASS when anchors derive only from accepted evidence. X: guessed/directorial timestamps.
46 **PROTECTED SILENCE REAL-TAIL A/B** — P:45. E: real tails + authored silence contract + human A/B. G: PASS when semantic silence preserved and dropout separated. X: blanket fill/trim.
47 **FIRST SPARSE MIX BUILD** — P:45–46. E: causal ambience/Foley/diegetic assets with rights/version + accepted timeline. G: PASS_BUILD if every byte-touch authorized. X: decorative asset insertion without contract.
48 **MIX TECHNICAL PROOF** — P:47. E: PCM/seam/headroom/protected-range/mono/phone/low-volume tests. G: PASS_TECH if all technical gates green; artistic result still separate. X: technical PASS as listener preference.

## G — Human benchmark / fatigue / quality / economics
49 **NARRATED MODE BUILD** — P:48. E: same protected source/text/loudness contract. G: PASS_BUILD if source identity preserved. X: adaptation drift.
50 **MULTI_VOICE MODE BUILD** — P:48. E: same source/text/loudness. G: PASS_BUILD if only treatment differs. X: rewritten dialogue advantage.
51 **DRAMATIZED MODE BUILD** — P:48. E: same source/text + controlled SFX/music. G: PASS_BUILD if comprehension is not hidden by adaptation. X: new exposition/story edits.
52 **RANDOMIZED BLIND HUMAN PACK** — P:49–51. E: hidden labels, frozen instructions/questions/order seed. G: PASS_PACKAGE when blinding/loudness/fairness verified. X: visible treatment labels.
53 **BLIND COMPREHENSION + EMOTION EVIDENCE** — P:52. E: real listener submissions. G: PASS/HOLD/FAIL from predefined thresholds for understanding, identity, naturalness, emotional pull, fatigue, continue intent. X: assistant/model preference.
54 **AI-TELL CALIBRATION** — P:53. E: advisory machine flags vs trusted human labels. G: PASS_CALIBRATION when false positives/negatives measured. X: machine-only artistic rejection.
55 **MEASURED PROVIDER ECONOMICS** — P:33–53. E: actual charges/requests/generated/accepted/rejected seconds/retries/cache. G: PASS_METRICS when complete measured ledger exists; HOLD on unknowns. X: estimates substituted for charges.
56 **MEASURED HUMAN-TIME ECONOMICS** — P:53. E: casting/listening/edit/QC/repair/admin time logs. G: PASS_METRICS when human minutes/accepted minute computable from real logs. X: guessed labor time.

## H — Selective repair / scale / cross-project / Red Team / V1
57 **ONE-BLOCK SELECTIVE REGEN PROOF** — P: real rejected performance block + 55. E: dependency closure, new request/charge, unaffected hashes. G: PASS if only target descendants change and no duplicate spend. X: broad rerender called selective.
58 **EDIT-BEFORE-REGENERATE PROOF** — P: eligible edit defect. E: timing/crossfade/level edit + quality/time/cost comparison. G: PASS if provider call avoided and quality gate preserved. X: performance/content defect hidden by edit.
59 **FULL CONTENT-VERIFIED RECOVERY DRILL** — P:40–58. E: fresh reconstruction of source/bindings/requests/responses/spend/audio/alignment/timeline/reviews/economics. G: PASS only content-verified restart. X: pointer-only or conversation-memory recovery.
60 **SELF-IMPROVEMENT EVENT COMPILATION** — P: at least one real defect/repair. E: project, mechanism, problem class, earliest layer, evidence class, delta, regression, metrics, leakage scan. G: PASS_EVENT if bounded and non-promoting. X: project facts universalized.
61 **SECOND REAL PROJECT MICRO-CANARY** — P: first-project empirical closure. E: materially different BODYGUARD or D04 provider/live/alignment/human/economics/recovery evidence. G: PASS_REPLICATION if same mechanism survives with zero LZ leakage. X: synthetic second project.
62 **CROSS-PROJECT CONTAMINATION + RECOVERY ATTACK** — P:61. E: injected wrong voices/facts/assets/timing/evidence refs/stale pointers. G: PASS if fail-closed/recovery route triggers. X: hidden contamination not tested.
63 **TWO-PROJECT RELEASE RED TEAM** — P:61–62. E: attack caller assertions, fake human, snapshot-without-preflight, pointer-only durability, duplicate spend, source drift, replay, laundering, contamination, authority escalation. G: PASS_RED_TEAM only FATAL/MAJOR closed; promotion remains Founder/domain-reviewed. X: self-promotion from tests.
64 **AUDIO NOVEL ENGINE V1 DECISION + INFORMATION ROUTER** — P:63. E: source authority, fresh CI, authenticated provider, live audio, real alignment, trusted human quality, measured economics, content-verified recovery, second real project, contamination scan, authorized release. G: output only `GO / LIMITED_GO / HOLD / NO_GO`. If HOLD, name exactly one next experiment with maximum information gain. X: architecture count, prompt count, synthetic evidence or partial engineering PASS used as Production Ready.

## Current execution note
The post-Wave8 provider hardening already merged to current main is compatible with the Wave9 provider/trust path, but does not fabricate completion of the v1.1 prompt IDs above. The current real external frontier remains Prompt 11/12 class: first authenticated provider capture and source-bound snapshot in a trusted runtime.