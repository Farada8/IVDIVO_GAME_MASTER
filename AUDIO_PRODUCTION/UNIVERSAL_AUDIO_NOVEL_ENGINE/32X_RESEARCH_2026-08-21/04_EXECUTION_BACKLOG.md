# IVDIVO AUDIO NOVEL ENGINE — EXECUTION BACKLOG AFTER 32X WAVE

## Current state

`RELEASE_CANDIDATE / LIVE_PORTABILITY_GATE_OPEN`

The next work is evidence acquisition, not architecture discovery.

## Dependency DAG

### GATE A — LESSON ZERO LIVE CANARY
**Inputs already ready:**
- locked Chapter 1 source;
- 146/146 spoken-unit coverage;
- 11 render blocks / dry requests;
- 14/14 sound cues;
- voice/pronunciation structure;
- canary selection: 3 requests / 36 units / 2163 chars / Narrator + Ethan + Aoife;
- fail-closed dispatch manifest.

**Remaining:**
1. provisional voice IDs;
2. pronunciation micro-test;
3. exactly 3 live dispatches;
4. raw WAV + raw alignment + provider metadata persistence.

**PASS TO GATE B only if:** exact text, speaker binding, pronunciation, no hard provider/performance failure.

### GATE B — REAL TIMELINE + MINI MIX
1. normalize alignment;
2. resolve semantic anchors;
3. produce required ambience/Foley/diegetic assets;
4. assemble mini timeline;
5. A/B/C loudness-matched mix if useful;
6. machine QC + mono/mobile.

**PASS TO GATE C only if:** no FATAL/MAJOR technical or causality defects.

### GATE C — HUMAN LISTEN
Blind/listener review of:
- comprehension;
- naturalness;
- acting/listening;
- role distinction;
- body presence;
- space;
- music/SFX appropriateness;
- AI distraction;
- desire to continue.

**PASS TO GATE D only if:** no unresolved FATAL/MAJOR and explicit human approval.

### GATE D — ORCHESTRATOR PROOF
- clean one-command dry/full canary orchestration;
- reproducibility;
- `--resume` without duplicate provider spend;
- controlled one-block failure;
- selective rerender;
- edit-only repair;
- selective downstream invalidation.

### GATE E — ECONOMICS
Measure, do not estimate:
- provider requests/characters/assets;
- provider spend;
- rejected vs accepted take ratio;
- accepted audio minutes;
- manual minutes by function;
- reuse/cache savings;
- repair cost;
- cost per accepted minute.

### GATE F — V1.0 RELEASE
Independent Red Team against actual code/build artifacts and ROOM 917 + LESSON ZERO evidence.

Release `PRODUCTION READY v1.0` only if:
- FATAL=0;
- MAJOR=0;
- second-project live portability PASS;
- human-listen PASS;
- one-command/resume/selective-repair PASS;
- economics measured;
- raw/live provenance durable;
- known limitations documented.

## Parallel work allowed while waiting for provider/voice access

The following can proceed without live spend:
- provider-neutral interface tests;
- machine-QC golden fixtures;
- synthetic-timing firewall tests;
- protected-silence collision fixtures;
- stereo source→stem regression fixture;
- failure taxonomy implementation;
- cost/manual-time instrumentation;
- durable storage manifest/schema;
- v1.0 documentation skeleton;
- third-project dry portability fixture.

## Work explicitly prohibited now

- another generic engine redesign;
- full LESSON ZERO chapter paid render before canary PASS;
- ROOM 917 restart at S0/S1;
- full season scaling before project-specific release gates;
- fabricated listening/provider/market results;
- silent delivery-mode adaptation;
- synthetic fixture timestamps promoted into production.