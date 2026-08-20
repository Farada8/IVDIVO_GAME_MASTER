# IVDIVO AUDIO NOVEL STUDIO — RUNTIME EXTENSION v0.1

**Status:** WORKING / IMPLEMENTATION EXTENSION — NOT YET UNIVERSAL CANON  
**Purpose:** turn the existing Audio Studio v3.0 canon/SOP into executable performance-learning machinery without creating a parallel production system.

## 1. Boundary

This extension sits **behind the existing Studio OS v3.0 gate chain**. It does not replace story authority, v2.3, the Studio OS, SOP, Machine Contract, provider contracts or release gates.

It exists to close the observed implementation gap between a rich Director Score and a provider request that otherwise degenerates into `text + voice_id`.

## 2. Central runtime object — SCENE_STATE_GRAPH

The production unit is a **listener-experienced dramatic moment**, not a line and not a sound file.

Every scene is represented as one shared state graph. At each beat/turn the graph may carry simultaneous layers:

1. STORY / FACT — what objectively happens.
2. KNOWLEDGE — what each character knows/does not know now.
3. ATTENTION — what owns the character's and listener's attention.
4. WANT / ACTION / TACTIC — what the character is doing to another person now.
5. EMOTION — FELT vs SHOWN, intensity, suppression, leakage, trigger, transition and carry-over.
6. RELATIONSHIP — trust, connection, intimacy boundary and current relationship state.
7. STATUS / POWER — who controls the exchange and how that changes.
8. LISTENING / RESPONSE — heard event, response impulse, entry trigger, reply mode.
9. BODY / PHYSIOLOGY — posture, effort, breath, mouth/food/drink state and physical occupation.
10. PERFORMANCE — tempo, projection, phrase ending, emphasis, hesitation, restraint and playable behavior.
11. RHYTHM — functional pause, interruption, overlap, wait, false start, no-reply and breath timing.
12. BLOCKING / SPACE — position, movement, orientation, distance, occlusion and microphone relationship.
13. SOUND WORLD — causal Foley/SFX/ambience permissions and suppressions.
14. MUSIC / MIX — value-change permission, no-music windows, focus ownership and later mix action.
15. LISTENER STATE — must understand / may feel / must wait for / focus owner / suppress.

All departments read the same graph. They do not independently invent conflicting versions of the scene.

## 3. Scene world model / auditory camera

The graph contains an `imagined_scene` / world state. It is the audible equivalent of mise-en-scène.

Sound is derived from a coherent imagined world:

`WORLD / ACTION / ATTENTION CHANGE -> AUDIBLE CONSEQUENCE`

not:

`available SFX -> decorate scene`.

The Listener Point of Audition is the auditory camera. A scene can contract from a public environment into a private conversational bubble, hold on an authored silence, or reopen into the wider world. Distance must change depth/direct-reverb/spectral perspective, not pan alone.

## 4. Emotion architecture

Emotion is not a provider tag and not one label per scene.

Minimum internal model:

`TRIGGER -> FELT STATE -> SUPPRESSION/EXPRESSION -> LEAKAGE -> PLAYABLE BEHAVIOR -> STATE_OUT -> CARRYOVER`.

The runtime distinguishes what a character **feels** from what the character **shows**. It compiles emotional state into behavior such as response latency, breath, projection, tempo, phrase endings, interruption pressure, hesitation and physical orientation.

Provider-facing packets receive the playable behavior, not an unfiltered psychology dump.

## 5. Runtime modules v0.1

`runtime/scene_state_graph.py`
- validates the multi-layer Scene State Graph;
- fail-closes reactive lines without causal response state;
- checks body/mouth consistency, spatial mono fallback, state/emotion continuity and world transitions.

`runtime/performance_compiler.py`
- compiles Scene State Graph into Actor Director Score;
- compiles functional rhythm/pause/breath plan;
- compiles provider-independent local context packets and request hashes;
- keeps felt emotion/subtext internal while exposing playable behavior.

`runtime/performance_qc.py`
- performs mechanical timing/activity QC on WAV;
- measures pause distribution and level dynamics;
- checks authored long/protected pause requirements and explicit regression rules;
- never claims waveform metrics alone prove believable acting.

`runtime/learning_registry.py`
- records defect -> root cause -> repair -> result evidence;
- aggregates repeated successful repair patterns;
- creates `CANDIDATE_FOR_REVIEW` only after repeated success across units + human passes;
- never silently rewrites universal canon;
- promotion requires explicit human/Founder approval.

## 6. Production learning loop

`PLAN -> RENDER -> MEASURE -> HUMAN LISTEN -> DEFECT -> ROOT CAUSE -> SMALLEST REPAIR -> RETEST -> RECORD`.

A single success does not become a universal rule.

Candidate promotion default:
- at least 3 successful uses;
- at least 2 distinct production units;
- at least 2 human-listen passes;
- successful evidence outweighs contradictions;
- explicit review/approval required.

The registry may improve prompts, block strategy, provider adapter defaults, edit policies, QC thresholds and production heuristics. It may **not** silently alter locked story canon, character canon, release authority or provider contracts.

## 7. Regression discipline

Known bad pilots are retained as regression fixtures.

For LESSON ZERO CH01 Scene 2, v1 is a known artistic failure. The failure is useful evidence: the live renderer passed only text/voice IDs, collapsed authored block structure and did not enforce protected silences. The replacement pipeline must beat the fixture before it is allowed to become the new baseline.

## 8. Promotion gate

This extension remains WORKING until one hard scene proves:
- Scene State Graph validation PASS;
- full protected-text coverage;
- provider-safe performance compilation;
- authored rhythm survives render/edit;
- human listen reports believable actor-to-actor reaction;
- no FATAL/MAJOR performance defect;
- selective repair works without rerendering unrelated locked material.

After that evidence, merge the runtime into the canonical orchestrator and version the Machine Contract/templates rather than maintaining a second system.
