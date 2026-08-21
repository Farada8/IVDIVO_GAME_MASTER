# NEXT 64 PROMPTS — EVIDENCE-DRIVEN NMM AUDIO PRODUCTION

These prompts are **not yet executed**. They are derived from the 32-prompt findings and are ordered to move from current preproduction frontier toward real evidence, locks, hard pilot, full E01 and release readiness. Each prompt must fail closed where live/human/specialist evidence is required.

## A — AUTHORITY / COMPILER

### 01
Reconcile every NMM E01 downstream document that still displays `1496` with the audio-compiler canonical count `1494` without touching locked spoken prose; output a metadata-override register.

### 02
Create `NMM_E01_SOURCE_FINGERPRINT_v1.json` containing authority document ID, revision, export SHA-256, E01 range identity, occurrence-ledger SHA-256 and canonical 1494 count; fail closed on mismatch.

### 03
Build a deterministic compiler test that asserts 269/269 spoken occurrences exactly once as RENDER or ALIAS and excludes SFX/MUSIC/headings/ledgers.

### 04
Create regression fixtures for all confession replay occurrences so every alias resolves to exact source text and exact master segment.

### 05
Audit speaker-label parsing for em dash, smart quotes, apostrophes and phone-role variants; output parser edge-case tests.

### 06
Create a `NO_BRANCH_FALLBACK` machine gate that rejects known superseded Mercer/Calder and pre-repair identifiers before compile.

### 07
Create a source-diff classifier that separates prose changes, metadata-only changes and non-recorded ledger changes, and route each class to the correct approval gate.

### 08
Create the episode build manifest schema that records DRY_RUN/LIVE/MIXED truthfully and binds authority, voices, assets, takes, provider profile and QC state.

## B — VOICE DISCOVERY / CASTING

### 09
Run fresh `/v2/voices` discovery locally and persist sanitized `ELEVENLABS_VOICES_AVAILABLE.json`; do not spend synthesis credits.

### 10
Rank real account voices for Isla using metadata only as a shortlist heuristic, explicitly marking metadata ranking as non-casting evidence.

### 11
Rank real account voices for Leo using metadata only; exclude any voice whose provenance is a different project's locked identity unless explicitly re-authorized.

### 12
Rank real account voices for Vivian with a spoiler-neutrality risk flag; avoid `villain`, `dark`, `sinister` descriptors as positive signals.

### 13
Run zero-cost `/v1/voices/{voice_id}` preflight on all shortlisted bindings and record availability/category/labels without secrets.

### 14
Design S1 fair-anchor job matrix for max 3 candidates per principal role using identical exact text and matched provider settings.

### 15
Design S2 discriminating-state jobs for only S1 survivors: Isla warmth/status, Leo public/private/uncertainty, Vivian care/control.

### 16
Design S4 pair/ensemble matrix for Isla↔Leo plus Isla↔Vivian; define hard differentiation and chemistry criteria before rendering.

## C — PERFORMANCE / TAKE LOCK

### 17
Write a performance packet for Isla opening narration with objective, tactic, subtext, status, energy, tempo, breath, proximity, listening behavior and forbidden modes.

### 18
Write a performance packet for Leo confession master that preserves uncertainty without murder-guilt coding and separates performance from telephone post.

### 19
Write a performance packet for Vivian's service-entrance exchange that makes her argument credible without secret-guilt acting.

### 20
Create context-specific variants of Leo's `I don't know` and define what must audibly differ without changing exact text.

### 21
Create a micro-humor direction test for Isla/Leo that avoids rom-com timing and audience winks.

### 22
Create a direction-change responsiveness test: same voice must execute one controlled variable change without identity drift.

### 23
Create take acceptance schema `GENERATED -> REVIEW_PENDING -> ACCEPTED -> LOCKED`, including reject reason taxonomy and selective-regeneration eligibility.

### 24
Define lead season-lock fatigue test length, playback conditions and failure criteria after hard pilot; keep provisional and season locks separate.

## D — SOUND / ACOUSTIC CLUE

### 25
Generate or source 3–5 candidate `W_EXTRA_SHORT` assets with no horror/police/cartoon coding and record provenance.

### 26
Generate or source 3–5 candidate `W_OFFICIAL_LONG` referee-whistle assets with credible stadium identity and record provenance.

### 27
Build blind A/B discrimination test for short vs long whistle on headphones, earbuds, mono phone and low-volume phone.

### 28
Create an acoustic-identity ledger for whistle masters including duration, envelope, spectral summary, context, hash and accepted use.

### 29
Create candidate METAL_DOOR_DISTANT and MECHANICAL_HUM confession environment assets and test replay stability/no masking.

### 30
Create PHONE_REMOTE_CHAIN and VOICE_NOTE_RECORDING_CHAIN candidates from clean speech, with intelligibility and identity checks.

### 31
Create a Foley minimalism cue sheet: retain only body/object events that change action, space, attention or causality.

### 32
Create a sound-density regression checklist for all timestamp/provenance/clue-comparison beats and mark maximum allowed simultaneous focus owners.

## E — PROVIDER / ALIGNMENT / TIMELINE

### 33
Run provider model preflight and verify selected model IDs/capabilities before any paid call; record non-secret evidence.

### 34
Run S0 with 3–5 minimal technical renders to validate Unicode, smart punctuation, output codec/sample rate, alignment and file sidecars.

### 35
Test `apply_text_normalization=off` versus `auto` on one harmless exact-text sample; compare source, alignment characters and audible output for drift.

### 36
Test pronunciation handling for Isla, Vivian, Aaron, Northbridge and time phrases using the smallest local method; prefer dictionary/local repair.

### 37
Implement TTD compiler hard ceiling <=1800 characters and split at semantic/selective-regeneration boundaries rather than arbitrary character positions.

### 38
Normalize TTS and TTD raw alignment into one provider-neutral schema and reject unsupported/malformed shapes.

### 39
After accepted pilot renders, resolve logical anchors to integer samples at project master rate; prohibit invented absolute production timestamps.

### 40
Create a provider-drift preflight checklist to rerun when endpoint/model/output/voice availability changes.

## F — MIX / QC / HUMAN LISTEN

### 41
Build the two-sample hard pilot from exact source: temporal-confession sample + relationship/whistle sample; do not pretend it is a full episode.

### 42
Create mix-action score for hard pilot only after real alignment, including focus owner, ducking, protected silence and clue audibility.

### 43
Run mono/phone/earbuds/headphones QC and persist a matrix for critical lines, confession identity and both whistle assets.

### 44
Run AI-artifact review for prosody repetition, breath artifacts, sibilance, identity drift and unnatural pause patterns; map each defect to smallest repair.

### 45
Run blind speaker-differentiation test for Isla/Leo/Vivian without names visible; set failure threshold before listening.

### 46
Run Vivian spoiler-neutrality blind test on neutral exchanges; reject/redirect if performance itself leaks culprit identity.

### 47
Run five-listener one-listen pilot comprehension test with no transcript; record exact misunderstandings, not just ratings.

### 48
Create selective repair plan from listener/QC failures using earliest-layer diagnosis: performance -> order/edit -> sound/mix -> provider -> text escalation only if proven.

## G — SPECIALIST / RELEASE / ECONOMICS

### 49
Prepare elite-team sports-medicine specialist review packet limited to unresolved publication claims; do not invite story redesign.

### 50
Prepare jurisdiction/legal specialist review packet for E22 and any evidence/admissibility terminology; classify changes by necessity and story impact.

### 51
Design E10 one-listen three-object comprehension test: Callum message vs Bell notes vs signed declaration.

### 52
Design E11 knowledge-sequence comprehension test: Daniel heard warning -> withheld it -> Bell assessed on denials/current findings.

### 53
Create provider-credit budget by stage using job counts and actual account pricing only after current pricing is retrieved; do not estimate unsupported money figures.

### 54
Create cost ledger fields for render purpose, candidate, chars, provider request, accepted/rejected, regeneration cause and avoidable waste.

### 55
Calculate selective-regeneration savings after first pilot from actual failed vs locked blocks; feed only observed data to the learning ledger.

### 56
Create final release GO/NO-GO checklist requiring FATAL=0, MAJOR=0, required live evidence, human review, specialist holds closed and master provenance.

## H — SCALE / SEASON / SELF-IMPROVEMENT

### 57
After E01 hard-pilot PASS, propagate the casting and provider mechanisms—not project-specific performance content—to E02/E03 planning.

### 58
Create season voice bible extension protocol before each recurring character's first render; prevent silent voice locks from one episode.

### 59
Create recurring acoustic identity ledger for whistle, phone, door/access and evidence-device families across episodes.

### 60
Create season-level narration fatigue checkpoints and detect gradual Isla cadence flattening or speed drift.

### 61
Create season-level Leo recorded/live identity checks wherever source recordings recur.

### 62
Create music motif registry that invokes MUSICAL_FACT_CONTRACT only when listener inference depends on shared pitch/melody identity.

### 63
At E01 master lock, write learning-ledger observations for voice rejection causes, pair failures, pronunciation, provider defects, clue audibility and cost waste—strip project-specific identities before universalization.

### 64
Run an independent end-to-end Red Team after real E01 evidence exists; reopen only failed gates and promote reusable mechanisms to universal IVDIVO audio authority after cross-project validation.
