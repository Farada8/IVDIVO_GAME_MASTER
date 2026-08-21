# IVDIVO AUDIO NOVEL ENGINE — 64 NEXT PROMPTS

These prompts are **derived from the 32-run evidence**. They are not permission to repeat architecture audits. Execute in dependency order; each prompt must persist artifacts, gates, evidence and exact next action.

---

# WAVE A — LIVE PORTABILITY + CASTING (01–08)

## 01 — THREE-VOICE CANDIDATE RECOVERY
**PROMPT:** Restore the current LESSON ZERO RU Chapter 1 voice-map and current provider voice inventory. Select only provisional candidates for Narrator, Ethan and Aoife. Do not lock any voice from one sample. Produce `LZ_CH01_CANARY_VOICE_CANDIDATES_v1.json` with evidence status and hard-fail risks.

## 02 — PRONUNCIATION MICRO-CANARY
**PROMPT:** Build the smallest pronunciation test that exercises `Ифа/Aoife`, `Контакт/Contact` and any other Chapter 1 high-risk proper nouns. Compare candidate pronunciations without music/reverb. Produce pronunciation decisions, aliases/phoneme strategy if needed and `PRONUNCIATION_LOCK_v1` only for proven items.

## 03 — NARRATOR DIRECTION-CHANGE TEST
**PROMPT:** Test Narrator candidate(s) in at least three states from the same source: neutral observation, restrained tension and intimate reflective delivery. Change direction, not text. Reject voices that cannot respond without sounding synthetic or over-performed.

## 04 — ETHAN MULTI-STATE TEST
**PROMPT:** Test Ethan in ordinary speech, pressure, restrained disagreement and curiosity. Evaluate age credibility, status behavior, phrase endings, listening and fatigue risk. Persist accepted/rejected hypotheses.

## 05 — AOIFE MULTI-STATE TEST
**PROMPT:** Test Aoife in ordinary youth-life speech, technical/audio curiosity, humor/embarrassment and pressure. Preserve believable young-person rhythm; reject adult-policy tone and generic TTS brightness.

## 06 — ETHAN/AOIFE RELATIONSHIP PAIR GATE
**PROMPT:** Assemble Ethan and Aoife in the same contextual beat at loudness-matched playback. Judge distinction, relational energy, interruption/reply timing and whether the voices sound like inhabitants of the same dramatic world. No music or heavy processing may hide the decision.

## 07 — EXACT THREE-REQUEST LIVE CANARY
**PROMPT:** Using the accepted provisional Narrator/Ethan/Aoife bindings, dispatch exactly the three preselected LESSON ZERO canary requests and no other Chapter 1 requests. Persist request JSON, request hashes, provider response metadata, WAVs and raw alignment. Fail closed on any mismatch.

## 08 — LIVE PORTABILITY GATE
**PROMPT:** Evaluate the three-request canary for exact text, speaker binding, pronunciation, performance, artifacts and raw alignment. Output PASS/FAIL per request plus whether the universal engine has passed second-project LIVE provider portability. No full Chapter 1 render is authorized unless this gate passes.

---

# WAVE B — ALIGNMENT + ORCHESTRATION + RESUME (09–16)

## 09 — NORMALIZE SECOND-PROJECT ALIGNMENT
**PROMPT:** Convert raw provider alignment from the LESSON ZERO canary into the universal normalized alignment schema. Verify every spoken unit against exact source text and preserve provider provenance.

## 10 — RESOLVE CANARY TIMELINE
**PROMPT:** Resolve semantic anchors into sample-accurate positions using only accepted live take timing. Attach protected silence, Foley, ambience and diegetic sound anchors. Synthetic fixture timing is forbidden.

## 11 — CLEAN-STATE ONE-COMMAND DRY BUILD
**PROMPT:** From a clean working directory/state, run the logical equivalent of `ivdivo-audio full <LZ_CH01> --dry-run` and prove that source ingest → direction → compilation → manifests/QC can complete without hand-edited JSON.

## 12 — BUILD REPRODUCIBILITY HASH TEST
**PROMPT:** Repeat the same dry build with identical inputs and configuration. Compare source hash, manifest hash, render-plan/request identities and deterministic artifacts. Classify legitimate nondeterminism explicitly.

## 13 — RESUME / NO-DUPLICATE-SPEND TEST
**PROMPT:** Resume the canary build after live requests already exist. Prove that `--resume` reuses accepted provider outputs and does not issue duplicate paid calls. Record reuse/provenance chain.

## 14 — CONTROLLED UPSTREAM-CHANGE INVALIDATION
**PROMPT:** Change one non-story upstream production input such as one voice binding or one pronunciation version. Recompute the dependency DAG and prove only dependent artifacts become stale; unrelated locked outputs remain valid.

## 15 — CONTROLLED SINGLE-BLOCK FAILURE
**PROMPT:** Mark one canary dialogue block as failed for a clearly defined performance reason. Route to selective rerender and prove no unrelated request is regenerated.

## 16 — ONE-COMMAND ORCHESTRATION ACCEPTANCE
**PROMPT:** Produce `AUDIO_ENGINE_ONE_COMMAND_ACCEPTANCE_v1.json` covering clean build, resume, selective invalidation, selective rerender, artifact hashes and fail-closed behavior. Decide whether orchestration is v1.0-ready.

---

# WAVE C — PROVIDER ADAPTER RELIABILITY (17–24)

## 17 — PROVIDER-NEUTRAL CONTRACT TEST
**PROMPT:** Verify that internal `PerformanceCompilation`, SFX and Music artifacts contain no ElevenLabs-only fields outside the adapter layer. List any vendor leakage and patch only interface violations.

## 18 — ERROR TAXONOMY / FAIL-CLOSED TEST
**PROMPT:** Map provider failures into stable engine errors: authentication, voice missing, invalid model, malformed request, unsupported output format, quota/rate limit, timeout and alignment absence. Never silently downgrade quality or switch voices.

## 19 — IDEMPOTENCY + RETRY POLICY
**PROMPT:** Define and test safe retry rules using request hashes/build IDs so network retries cannot create accidental duplicate accepted takes or hidden extra spend.

## 20 — PROVIDER AUDIO FORMAT NORMALIZATION
**PROMPT:** Validate the adapter path for PCM/WAV wrapping, sample-rate/bit-depth metadata and channel expectations. Include the ROOM 917 live evidence where SFX/Music rejected the original `wav_48000` assumption and required `pcm_48000` + local wrapping.

## 21 — ALIGNMENT SCHEMA DRIFT TEST
**PROMPT:** Feed representative raw alignment variants into the normalizer. Fail closed if required character/word timing or text correspondence cannot be proven. Persist compatibility fixtures.

## 22 — MODEL / VOICE DRIFT DETECTION
**PROMPT:** Detect when a previously accepted provider voice/model/version is unavailable or changed. Do not auto-substitute. Produce a supersession workflow through `VOICE_BINDING_LEDGER`.

## 23 — SFX + MUSIC ADAPTER REGRESSION
**PROMPT:** Run zero-cost/dry adapter tests for dialogue, TTS, SFX and music request compilation under the current provider contract. Verify separate media types cannot contaminate clean dialogue masters.

## 24 — SECOND-PROVIDER INTERFACE MOCK
**PROMPT:** Without requiring live spend, implement or specify a minimal second-provider mock adapter that consumes the same internal contracts. The objective is interface proof, not feature parity or vendor shopping.

---

# WAVE D — PERFORMANCE ENGINE (25–32)

## 25 — LESSON ZERO DIRECTOR SCORE REGRESSION
**PROMPT:** Recompile LESSON ZERO Chapter 1 performance direction from source and compare with the existing accepted director-score fixture. Differences must be explained as bug fix, nondeterminism or changed authority; never silently rewrite text.

## 26 — SILENT REACTION COVERAGE
**PROMPT:** Identify beats where a character's silence changes the scene. Generate `SILENT_REACTION_ANCHOR`s and prove they do not distort spoken-unit coverage.

## 27 — PAUSE/BREATH FUNCTION PASS
**PROMPT:** For canary beats, label each material pause/breath by function: thought, hesitation, recognition, status, listening, object action, aftermath, interruption window or no reply. Remove arbitrary TTS pauses only when the function is unsupported.

## 28 — REPLY LATENCY + OVERLAP PASS
**PROMPT:** Plan reply latency and justified overlap from heard-event → response-impulse rather than uniform spacing. Produce alternative hypotheses only where the scene supports them.

## 29 — MICROPHONE CHOREOGRAPHY PASS
**PROMPT:** Compile performance and mic perspective jointly for close, normal, across-room and media/recorded speech. Test whether projection/breath/articulation match distance before any mix correction.

## 30 — LONG-FORM FATIGUE TEST
**PROMPT:** For any voice approaching lock, render/listen to an 8–10 minute equivalent workload or a carefully assembled multi-state proxy. Evaluate fatigue, repetitive cadence, over-clean diction and AI tells.

## 31 — PERFORMANCE HARD-FAIL LIBRARY
**PROMPT:** Build project-neutral hard-fail examples: generic trailer voice, melodramatic emphasis, identical sentence endings, no listening, status flattening, robotic breath, adult voice on youth material, false intimacy. Connect each to rejection rules.

## 32 — PERFORMANCE QC HUMAN/MACHINE CROSSCHECK
**PROMPT:** Compare machine-detectable performance symptoms with human judgment on the same canary. Identify which issues are safely automatable and which must remain human-gated.

---

# WAVE E — SOUND / MUSIC / SPACE / MIX (33–40)

## 33 — LESSON ZERO ACOUSTIC PASSPORTS
**PROMPT:** Create scene-level acoustic passports for the canary: room/world identity, point of audition, source positions, movement, occlusion, stereo intent and mono constraints.

## 34 — AMBIENCE VARIATION / DEAD-AIR TEST
**PROMPT:** Build ambience variants long enough to avoid obvious looping. Measure low-level windows but classify them against dramatic intent/protected silence before repair.

## 35 — FOLEY CAUSALITY BUILD
**PROMPT:** Convert every canary Foley proposal into `cause → physical action → audible consequence → listener function → space`. Remove Foley that exists only because sound can be generated.

## 36 — DIEGETIC RECORDING / MEDIA AUTHENTICITY
**PROMPT:** For Aoife's recording/audio-within-audio material, define medium identity, bandwidth/noise/perspective and transitions in/out of playback. Preserve intelligibility while making the medium inferable without narration explaining it.

## 37 — MUSIC ENTRY/EXIT CAUSALITY
**PROMPT:** Test whether each proposed canary music cue has a real dramatic entry cause and exit cause. Reject constant emotional wallpaper and music that answers a story question prematurely.

## 38 — SHARED MUSICAL/ACOUSTIC FACT CONTRACT
**PROMPT:** Create the generic mechanism for cases where voice hum, diegetic melody, SFX and score must share pitch/rhythm identity. Use ROOM 917 fourth-note failure as regression evidence; do not copy ROOM 917's specific motif into other projects.

## 39 — SPATIAL AUTOMATION + MONO SAFETY
**PROMPT:** Produce a spatial plan for canary dialogue, ambience, Foley and diegetic audio. Verify that declared perspective survives mono/mobile without clue/action loss.

## 40 — A/B/C MINI-MIX
**PROMPT:** Build or specify three loudness-matched canary mixes: A Forensic Control, B Commercial, C Premium. Score acting, body presence, space, music, Foley, naturalness, comprehension and desire to continue. Promote only evidence-backed differences.

---

# WAVE F — QC / REPAIR / REGRESSION (41–48)

## 41 — GOLDEN MACHINE-QC FIXTURES
**PROMPT:** Create minimal PASS and FAIL fixtures for every mandatory machine QC gate: authority, exact text, units, binding, pronunciation, assets, anchors, protected silence, music policy, stems, loudness and alignment.

## 42 — SYNTHETIC-TIMING FIREWALL REGRESSION
**PROMPT:** Attempt to feed synthetic fixture timestamps into a live-build path and prove the engine fails closed before timeline/master generation.

## 43 — PROTECTED-SILENCE COLLISION TESTS
**PROMPT:** Inject music/reverb/ambience/trim collisions into protected-silence fixtures and prove QC identifies each collision while allowing explicitly permitted physical baselines.

## 44 — CLUE / INFORMATION AUDIBILITY TEST
**PROMPT:** Create generic tests where a comprehension-critical line or sound is masked, reordered or over-scored. Verify listener-contract/clue QC catches the failure.

## 45 — SOURCE→STEM STEREO INTEGRITY REGRESSION
**PROMPT:** Reproduce the class of ROOM 917 bug where stereo source becomes mono downstream. Make source-vs-stem integrity a regression fixture rather than a whole-master correlation heuristic.

## 46 — EDIT-BEFORE-REGENERATE DECISION TEST
**PROMPT:** Feed a set of defects into the repair controller and verify pause/trim/crossfade/reaction-placement issues route to edit-only while identity/intention/text failures route to selective rerender.

## 47 — EARLIEST-CAUSE DEFECT ROUTER
**PROMPT:** For compound defects, identify the earliest failed layer and invalidate only descendants. Demonstrate at least one case where a mix symptom is caused upstream by performance or staging.

## 48 — HUMAN REVIEW PRIORITY QUEUE
**PROMPT:** Convert machine QC and unresolved artistic risks into a prioritized human-review queue so listeners review high-risk beats first rather than manually auditing every second equally.

---

# WAVE G — ECONOMICS / SCALE / STORAGE (49–56)

## 49 — COST INSTRUMENTATION
**PROMPT:** Record per build: provider characters, request count, SFX/music calls, generated seconds, rejected takes, accepted seconds and provider cost. Produce cost per accepted minute.

## 50 — MANUAL-MINUTES INSTRUMENTATION
**PROMPT:** Measure human time for casting, pronunciation, listening, repair and final approval separately. Automation percentage without manual-minute accounting is invalid.

## 51 — REUSE / CACHE ECONOMICS
**PROMPT:** Quantify accepted take/asset reuse and provider calls avoided by cache/selective remix. Persist provenance so reuse does not become hidden contamination.

## 52 — PAID-CALL CASCADE OPTIMIZATION
**PROMPT:** Compare canary-first, full-cast-first and full-chapter-first spend models using actual measured costs. Keep only the cascade that minimizes cost per accepted minute without reducing evidence quality.

## 53 — THROUGHPUT MODEL
**PROMPT:** Measure wall-clock production stages separately from provider latency and human gates. Estimate accepted minutes/day only from observed runs, not theoretical provider speed.

## 54 — DURABLE AUDIO PROVENANCE STORAGE
**PROMPT:** Define the storage package for raw WAV, normalized copies, stems, request/response records, alignment, hashes, manifests and accepted masters so cross-dialog recovery never depends on chat-local files.

## 55 — SECRET / CREDENTIAL HYGIENE
**PROMPT:** Audit production artifacts for API keys, bearer tokens, credentials and provider secrets. Credentials may exist only in approved runtime environment; never in GitHub/Drive canon, JSON manifests or prompts.

## 56 — SCALE SIMULATION WITHOUT PAID RENDER
**PROMPT:** Using real canary measurements and full Chapter 1 dry manifests, simulate expected requests/assets/storage/manual-review load for Chapter 1 and a full book. Clearly separate measured values from projections.

---

# WAVE H — HUMAN VALIDATION / PRODUCTIZATION / RELEASE (57–64)

## 57 — BLIND LISTENER PROTOCOL
**PROMPT:** Design a blind test that does not tell listeners which version is AI, baseline or premium. Capture comprehension, emotion, naturalness, distraction, character distinction and desire to continue.

## 58 — LOUDNESS-MATCHED REFERENCE COMPARISON
**PROMPT:** Compare our accepted canary/master against legally available premium audio references only after loudness matching. Abstract mechanisms such as density, body presence, transition craft and music use; do not imitate distinctive content.

## 59 — DELIVERY-MODE COMPARISON ON SAME EXCERPT
**PROMPT:** Produce dry or low-cost versions of one short excerpt as Narrated, Multi-Voice and Dramatized. Compare production cost, comprehension and emotional value to test whether delivery-mode selection is economically rational.

## 60 — THIRD PORTABILITY FIXTURE
**PROMPT:** Choose a third materially different locked source — e.g. youth/orbital, romance or Smith/OES — and run source→dry-package only. The goal is schema stress, not another live spend before LESSON ZERO closes.

## 61 — LANGUAGE PORTABILITY REGRESSION
**PROMPT:** Run the same ingest/compilation/QC schema on a short locked excerpt in another manuscript language. Identify only language-specific pronunciation/tokenization/provider assumptions.

## 62 — SECOND REAL CHAPTER/EPISODE AFTER CANARY
**PROMPT:** Once LESSON ZERO canary passes, select the smallest next Chapter 1 slice that meaningfully expands role count/sound complexity. Scale gradually and verify cost/quality do not degrade.

## 63 — V1.0 RELEASE DOCUMENTATION
**PROMPT:** Assemble START HERE, command reference, folder/schema definitions, failure codes, release gates, migration notes, known limitations and evidence ledger for `IVDIVO AUDIO NOVEL ENGINE v1.0`.

## 64 — FINAL INDEPENDENT RED TEAM + RELEASE DECISION
**PROMPT:** After all v1.0 blockers have evidence, run an independent Red Team against the actual code/artifacts and real ROOM 917 + LESSON ZERO builds. Classify FATAL/MAJOR/MEDIUM/POLISH. Release `PRODUCTION READY v1.0` only if FATAL=0, MAJOR=0 and all mandatory live/human/economic gates have evidence. Otherwise issue a bounded repair list, not a new architecture project.

---

# EXECUTION LAW FOR ALL 64

Every prompt must end with:
- sources/authority used;
- artifact(s) changed or created;
- machine gates run;
- human evidence if actually obtained;
- measured costs if actually incurred;
- ACCEPT / ACCEPT_WITH_MODIFICATION / HOLD_FOR_TEST / REJECT;
- exact next unblocked action;
- persistence/readback confirmation.

Do not claim provider execution, perceptual listening or market evidence unless it actually occurred.