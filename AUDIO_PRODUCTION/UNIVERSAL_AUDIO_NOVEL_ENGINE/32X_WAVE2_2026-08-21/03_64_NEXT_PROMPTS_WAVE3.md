# IVDIVO AUDIO NOVEL ENGINE — WAVE 3 — 64 NEXT PROMPTS
Derived from Wave 2. These prompts replace generic redesign with evidence/integration work.
Execution law: persist evidence; fail closed; no fabricated live/human/cost claims; do not rewrite locked story.

## A — LIVE CAST + CANARY CLOSURE

### 01 — AUTHENTICATED VOICE INVENTORY SNAPSHOT
**Execution prompt:** Retrieve current provider voice inventory through a no-generation authenticated read. Record voice IDs/names/languages/access, but no secret. Diff against any saved inventory and mark unavailable/drifted entries.
**Required output:** Versioned inventory + drift report.
**PASS gate:** Inventory is durable, contains no credential, and no voice is silently substituted.

### 02 — THREE-ROLE CANDIDATE SHORTLIST
**Execution prompt:** Using current Narrator/Ethan/Aoife passports, shortlist only candidates supported by current inventory. Do not reuse ROOM917 roles by assumption.
**Required output:** Candidate ledger with evidence and hard fails.
**PASS gate:** Each candidate is traceable to inventory and every hard fail is explicit.

### 03 — PRONUNCIATION AUDITION PACK
**Execution prompt:** Prepare unchanged canonical lines that exercise Ифа/Контакт and exact provider settings. No synthetic story text.
**Required output:** Audition manifest + comparison rubric.
**PASS gate:** Only canonical text is dispatched; pronunciation decision remains unlocked until heard.

### 04 — NARRATOR THREE-STATE AUDITION
**Execution prompt:** Render/compare neutral observation, restrained tension and intimate reflection for narrator candidates at matched loudness.
**Required output:** Audition takes + blind score sheet.
**PASS gate:** Candidate demonstrates direction change without trailer/sentimental drift.

### 05 — ETHAN FOUR-STATE AUDITION
**Execution prompt:** Render/compare ordinary banter, pressure, defensive over-speed and uncertainty for Ethan candidates.
**Required output:** Audition takes + score sheet.
**PASS gate:** Voice reads as 17 and preserves state differences.

### 06 — AOIFE FOUR-STATE AUDITION
**Execution prompt:** Render/compare peer banter, technical curiosity, quiet humor and serious waiting pressure.
**Required output:** Audition takes + score sheet.
**PASS gate:** No therapist/flirt/counselor/adult-policy hard fail.

### 07 — ETHAN_AOIFE PAIR GATE
**Execution prompt:** Assemble survivor Ethan/Aoife candidates inside RB001/RB002 context, loudness matched, no music/reverb masking.
**Required output:** Pair comparison + provisional binding decision.
**PASS gate:** Instant distinction + same-age credibility + relational timing pass.

### 08 — EXACT THREE-REQUEST LIVE CANARY
**Execution prompt:** After provisional bindings and pronunciation preflight, dispatch exactly RB001/RB002/RB003. Persist requests, hashes, response IDs, raw WAV and raw alignment.
**Required output:** Live canary package.
**PASS gate:** Exactly 3 paid dialogue requests; exact hashes match; durable provenance complete.

## B — REAL ALIGNMENT + TIMELINE + CLI

### 09 — RAW LIVE PROVENANCE INGEST
**Execution prompt:** Ingest all canary responses into take registry with provider request/trace IDs, audio hashes, raw alignment and binding versions.
**Required output:** Take registry.
**PASS gate:** Every live byte is attributable to one request/build and cannot be confused with dry fixtures.

### 10 — LIVE ALIGNMENT NORMALIZATION
**Execution prompt:** Normalize actual TTD voice_segments and narrator TTS character alignment into one schema.
**Required output:** Normalized alignment records.
**PASS gate:** 36/36 units have proven timing lineage; unsupported correspondence fails closed.

### 11 — CANARY SAMPLE TIMELINE
**Execution prompt:** Resolve CUE008–CUE012 from semantic anchors using accepted take timing at 48 kHz.
**Required output:** Resolved sample timeline.
**PASS gate:** No synthetic timestamps; unresolved selected anchors=0.

### 12 — PROTECTED SILENCE REALIZATION
**Execution prompt:** Resolve CUE011 after U024 using actual alignment and auditioned duration; preserve allowed physical baseline only.
**Required output:** Silence manifest + QC.
**PASS gate:** No music/Foley/reverb tail violates protected window.

### 13 — PRODUCTION CLI CLEAN BUILD
**Execution prompt:** Run actual ivdivo-audio full/equivalent from clean mounted source in dry mode, no hand-edited JSON.
**Required output:** CLI log + artifact hashes.
**PASS gate:** One command reaches full dry package with deterministic gates.

### 14 — PRODUCTION CLI RESUME
**Execution prompt:** Resume the same build with live canary outputs already present.
**Required output:** Resume log/spend ledger.
**PASS gate:** No accepted request is resent; reused artifacts retain identity.

### 15 — PRODUCTION CLI SCOPED INVALIDATION
**Execution prompt:** Change pronunciation version, then binding version, and inspect actual DAG invalidation.
**Required output:** Invalidation reports.
**PASS gate:** Pronunciation touches only dependent blocks; binding touches correct role-dependent descendants.

### 16 — CLI ORCHESTRATION RELEASE GATE
**Execution prompt:** Aggregate clean-build, resume, invalidation, selective rerender and fail-closed tests into one acceptance artifact.
**Required output:** Orchestration acceptance JSON/MD.
**PASS gate:** All mandatory production-code tests pass; harness-only status removed.

## C — PRODUCTION CODE INTEGRATION

### 17 — PORT CANARY IDENTITY CONTRACT
**Execution prompt:** Move 3-block/36-unit/hash invariants from research harness into production validation fixtures.
**Required output:** Code + tests.
**PASS gate:** CI fails on block/unit/hash drift.

### 18 — PERSISTENT SPEND LEDGER
**Execution prompt:** Implement immutable request-attempt ledger keyed by build/request hash with PLANNED/SENT/AMBIGUOUS/ACCEPTED/REJECTED.
**Required output:** Code + tests.
**PASS gate:** Retry cannot silently duplicate accepted paid work.

### 19 — AMBIGUOUS RESPONSE QUARANTINE
**Execution prompt:** Implement response-started/network-drop quarantine requiring provider reconciliation before retry.
**Required output:** Code + tests.
**PASS gate:** Ambiguous attempt never auto-retries as if nothing happened.

### 20 — STABLE PROVIDER ERROR TAXONOMY
**Execution prompt:** Implement normalized AUTH/RATE_LIMIT/QUOTA/INVALID_REQUEST/FORMAT/TIMEOUT/ALIGNMENT/MODEL/VOICE errors.
**Required output:** Code + fixtures.
**PASS gate:** Provider-specific payload changes do not leak into domain state.

### 21 — AUDIO FORMAT NORMALIZER
**Execution prompt:** Productionize PCM/WAV normalization with sample-rate/bit-depth/channel assertions and audio hash.
**Required output:** Code + fixtures.
**PASS gate:** 48k PCM fixture produces valid WAV and malformed data fails closed.

### 22 — DUAL ALIGNMENT NORMALIZER
**Execution prompt:** Productionize TTD and TTS raw-shape normalizers with source_schema provenance.
**Required output:** Code + fixtures.
**PASS gate:** Every supported endpoint shape yields canonical timing; unknown shape is fatal to timeline.

### 23 — VOICE_MODEL CAPABILITY REGISTRY
**Execution prompt:** Add versioned provider capability/voice availability snapshot without auto-substitution.
**Required output:** Code + fixture.
**PASS gate:** Unavailable model/voice causes explicit drift gate.

### 24 — SECOND PROVIDER CI MOCK
**Execution prompt:** Keep a second-provider mock in CI to prove domain schemas remain provider-neutral.
**Required output:** Mock adapter + tests.
**PASS gate:** Provider swap changes adapter behavior, not stored domain schemas.

## D — PERFORMANCE EVIDENCE ENGINE

### 25 — SILENT REACTION SCHEMA PROMOTION
**Execution prompt:** Promote SILENT_REACTION_ANCHOR fields and LESSON ZERO fixtures into production schema.
**Required output:** Schema + tests.
**PASS gate:** Silent reactions own cues/silence but add zero spoken units.

### 26 — FUNCTIONAL PAUSE COMPILER
**Execution prompt:** Compile only supported pause functions and reject vague DRAMATIC pause.
**Required output:** Code + fixture.
**PASS gate:** Every material pause has story/action function.

### 27 — REPLY LATENCY COMPILER
**Execution prompt:** Translate heard-event/response-impulse states into auditionable latency hypotheses, not absolute pre-render timestamps.
**Required output:** Code + fixture.
**PASS gate:** Uniform spacing is not default; hypotheses remain semantic until alignment.

### 28 — MICROPHONE CHOREOGRAPHY COMPILER INTEGRATION
**Execution prompt:** Bind performance state to CLOSE/NORMAL/ACROSS_ROOM/MEDIA perspective and movement path.
**Required output:** Code + LESSON ZERO fixture.
**PASS gate:** Projection/proximity intent exists before mix and survives scene-specific topology.

### 29 — LONG-FORM FATIGUE PROTOCOL EXECUTION
**Execution prompt:** Run survivor voices through 8–10 minute workload or equivalent multi-state sequence.
**Required output:** Audio + fatigue report.
**PASS gate:** Repetitive cadence/AI tells do not exceed human gate tolerance.

### 30 — AI-TELL MACHINE FLAGGER
**Execution prompt:** Implement only non-authoritative flags for repeated endings, abnormal pause regularity, breath regularity and cadence repetition.
**Required output:** Code + calibration set.
**PASS gate:** Flags never self-reject artistic performance without human review.

### 31 — PERFORMANCE MACHINE_HUMAN CROSSCHECK
**Execution prompt:** Compare machine flags with blind human judgments on same takes.
**Required output:** Calibration report.
**PASS gate:** False positive/negative rates are measured; human-only dimensions remain human.

### 32 — PERFORMANCE LOCK GATE
**Execution prompt:** Create final provisional→approved→locked voice/performance gate for chapter scaling.
**Required output:** Gate artifact.
**PASS gate:** No voice locks without multi-state, pair where relevant, pronunciation and fatigue evidence.

## E — SOUND MUSIC SPACE MIX

### 33 — LESSON ZERO ACOUSTIC PASSPORTS
**Execution prompt:** Compile scene-level room/world identity, POA, positions, movement, occlusion, stereo intent and mono constraints.
**Required output:** Acoustic passports.
**PASS gate:** Both CH01 scenes have explicit non-ROOM917 spatial identities.

### 34 — AMBIENCE VARIATION DEAD-AIR TEST
**Execution prompt:** Build/select long enough ambience variants for festival/pool world; classify low-level windows against protected silence.
**Required output:** Assets + density report.
**PASS gate:** No obvious looping; active silence not filled decoratively.

### 35 — FOLEY CAUSALITY BUILD
**Execution prompt:** Map recorder/coffee/body/footstep actions as cause→action→sound→listener function.
**Required output:** Foley graph.
**PASS gate:** Decorative Foley without cause/function removed.

### 36 — DIEGETIC RECORDER AUTHENTICITY
**Execution prompt:** Design Aoife recorder capture medium identity and transitions.
**Required output:** Media processing spec.
**PASS gate:** Listener can infer audio-within-audio without exposition.

### 37 — MUSIC ENTRY_EXIT CAUSALITY
**Execution prompt:** Audit CUE012 and other Chapter 1 music for earned entry/exit cause.
**Required output:** Music dramaturgy.
**PASS gate:** Wallpaper/premature-answer music rejected.

### 38 — SHARED ACOUSTIC FACT GENERIC CONTRACT
**Execution prompt:** Implement generic shared pitch/rhythm identity between diegetic sound/SFX/score without copying ROOM917 motif.
**Required output:** Schema + regression fixture.
**PASS gate:** Identity can persist across media while content stays project-specific.

### 39 — SPATIAL AUTOMATION MONO SAFETY
**Execution prompt:** Create staging automation for canary dialogue/ambience/Foley/diegetic capture and mono/mobile proxies.
**Required output:** Spatial manifest + QC.
**PASS gate:** Perspective survives mono/mobile and does not rely on extreme pan.

### 40 — A_B_C MINI MIX
**Execution prompt:** Create loudness-matched Forensic/Commercial/Premium canary mixes after real alignment.
**Required output:** 3 mixes + scorecard.
**PASS gate:** Winner improves acting/body/space/comprehension/desire-to-continue without masking defects.

## F — QC REPAIR REGRESSION

### 41 — GOLDEN QC FIXTURE PACK
**Execution prompt:** Create minimal PASS/FAIL fixtures for authority, text, units, binding, pronunciation, assets, anchors, silence, music, stems, loudness and alignment.
**Required output:** Fixture pack + tests.
**PASS gate:** Each mandatory gate has at least one failing test.

### 42 — SYNTHETIC TIMING FIREWALL
**Execution prompt:** Attempt to route synthetic alignment into live timeline/master path.
**Required output:** Negative test.
**PASS gate:** Build fails before timeline/master.

### 43 — POST_FX PROTECTED SILENCE TEST
**Execution prompt:** Inject reverb/ducking tails crossing protected windows.
**Required output:** Negative tests.
**PASS gate:** Post-FX mask catches forbidden tails while whitelist baseline survives.

### 44 — INFORMATION AUDIBILITY TEST
**Execution prompt:** Mask/reorder comprehension-critical line/sound in generic fixtures.
**Required output:** QC tests.
**PASS gate:** Listener-contract/information QC catches the failure.

### 45 — STEREO SOURCE_STEM INTEGRITY
**Execution prompt:** Reproduce stereo-source→mono-stem class from ROOM917 as permanent fixture.
**Required output:** Regression test.
**PASS gate:** Unexpected channel collapse fails before master.

### 46 — EDIT_BEFORE_REGEN CONTROLLER
**Execution prompt:** Feed pause/trim/crossfade/reaction vs identity/intention/text failures.
**Required output:** Decision tests.
**PASS gate:** Edit-only and selective-rerender routes separate correctly.

### 47 — EARLIEST CAUSE DEFECT ROUTER
**Execution prompt:** Build compound cases where mix symptom originates in performance/staging.
**Required output:** Router tests.
**PASS gate:** Earliest causal layer selected; only descendants invalidated.

### 48 — HUMAN REVIEW PRIORITY QUEUE
**Execution prompt:** Convert machine failures + unresolved artistic risks into bounded review segments.
**Required output:** Priority queue.
**PASS gate:** Review effort focuses on highest risk rather than entire runtime.

## G — ECONOMICS STORAGE SCALE

### 49 — COST INSTRUMENTATION LIVE
**Execution prompt:** Record provider characters/requests/generated seconds/rejected takes/accepted seconds/cost for canary.
**Required output:** Cost ledger.
**PASS gate:** Cost per accepted minute uses measured data only.

### 50 — MANUAL MINUTES INSTRUMENTATION
**Execution prompt:** Time casting/pronunciation/listening/repair/approval separately.
**Required output:** Manual-time ledger.
**PASS gate:** Automation percentage cannot be reported without human minutes.

### 51 — CACHE REUSE ECONOMICS
**Execution prompt:** Measure provider calls and cost avoided by accepted take/asset reuse.
**Required output:** Reuse report.
**PASS gate:** Savings tied to actual provenance, not estimates.

### 52 — PAID CASCADE COMPARISON
**Execution prompt:** Compare canary-first vs full-cast-first vs full-chapter-first using measured values.
**Required output:** Strategy model.
**PASS gate:** Chosen cascade minimizes cost per accepted minute without weakening gates.

### 53 — THROUGHPUT MEASUREMENT
**Execution prompt:** Separate compute/provider latency/human gate durations.
**Required output:** Throughput report.
**PASS gate:** Accepted minutes/day is measured, not guessed.

### 54 — DURABLE AUDIO PROVENANCE PACKAGE
**Execution prompt:** Persist raw WAV, normalized audio, stems, requests/responses, alignments, hashes, manifests and masters outside chat-local storage.
**Required output:** Storage spec + actual canary package.
**PASS gate:** New dialog can recover build without chat-local bytes.

### 55 — SECRET CREDENTIAL HYGIENE
**Execution prompt:** Scan GitHub/Drive artifacts for API keys/tokens and enforce runtime-only secret policy.
**Required output:** Audit + guard.
**PASS gate:** No secret in canon/prompts/manifests/repo.

### 56 — CHAPTER_BOOK SCALE SIMULATION
**Execution prompt:** Use canary measurements + full CH01 dry manifest to project requests/storage/review/cost for chapter and book.
**Required output:** Projection with confidence labels.
**PASS gate:** Measured and projected quantities are explicitly separated.

## H — PORTABILITY PRODUCTIZATION RELEASE

### 57 — BLIND LISTENER PROTOCOL EXECUTION
**Execution prompt:** Run blind comparison without revealing version provenance.
**Required output:** Listener dataset.
**PASS gate:** Comprehension/emotion/naturalness/distinction/AI distraction/desire-to-continue captured.

### 58 — LOUDNESS_MATCHED PREMIUM REFERENCE
**Execution prompt:** Compare mechanisms against lawful premium reference audio after loudness matching.
**Required output:** Comparison report.
**PASS gate:** No distinctive content imitation; mechanism gaps only.

### 59 — DELIVERY MODE SAME_EXCERPT
**Execution prompt:** Produce/compare Narrated, Multi-Voice and Dramatized variants of one locked excerpt.
**Required output:** Mode comparison.
**PASS gate:** Cost/comprehension/emotional delta measured.

### 60 — THIRD PORTABILITY FIXTURE
**Execution prompt:** Run a materially different locked source through source→dry package, no live spend unless justified.
**Required output:** Dry portability report.
**PASS gate:** No LESSON ZERO/ROOM917 hardcodes surface.

### 61 — LANGUAGE PORTABILITY REGRESSION
**Execution prompt:** Run short locked excerpt in another manuscript language through schemas/QC.
**Required output:** Regression report.
**PASS gate:** Language-specific assumptions isolated without changing universal contracts.

### 62 — SECOND REAL SLICE AFTER CANARY
**Execution prompt:** After canary PASS, render smallest slice expanding roles/sound complexity.
**Required output:** Live build + QC.
**PASS gate:** Quality/cost remain within gate while complexity increases.

### 63 — V1 RELEASE DOCUMENTATION
**Execution prompt:** Assemble START HERE, commands, schemas, failure codes, migration, limitations and evidence ledger.
**Required output:** Release docs.
**PASS gate:** A new operator can run dry workflow and understand all live/human gates.

### 64 — FINAL INDEPENDENT RED TEAM RELEASE DECISION
**Execution prompt:** Red Team actual code + ROOM917 live evidence + LESSON ZERO live build + human/economic evidence.
**Required output:** Release decision.
**PASS gate:** PRODUCTION_READY only if FATAL=0, MAJOR=0 and mandatory live/human/economic/CLI gates PASS.
