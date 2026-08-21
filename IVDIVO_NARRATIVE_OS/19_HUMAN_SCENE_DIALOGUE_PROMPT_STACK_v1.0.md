# IVDIVO — HUMAN SCENE / DIALOGUE NATURALISM — 24-PASS PROMPT STACK v1.0

**Status:** CURRENT EXECUTION PROMPT PACK  
**Established:** 2026-08-21  
**Parent:** `19_HUMAN_SCENE_AND_DIALOGUE_NATURALISM_ENGINE_v1.0.md`  
**Use:** apply selectively. Do not run all 24 passes on every trivial exchange. Major/new/high-risk scenes should use the full stack or an explicitly justified subset.

The stack is intentionally denser than the previous dialogue workflow. It separates diagnosis from repair and text from performance so that the system does not rewrite good prose to compensate for weak TTS or acting.

---

# RUN CARD INPUT

Before any pass provide:

```text
PROJECT / BOOK:
SCENE / CHAPTER:
CURRENT AUTHORITY:
TEXT STATUS: WORKING / LOCKED / EXACT-TEXT-PROTECTED
STORY FACTS THAT MUST NOT CHANGE:
CHARACTERS PRESENT:
RELATIONSHIP STATE ENTERING SCENE:
KNOWN / UNKNOWN / SUSPECTED PER CHARACTER:
SCENE OBJECTIVE:
SCENE TURN:
WHY THIS PASS IS RUNNING:
AVAILABLE AUDIO / READER EVIDENCE:
```

No authority = no rewrite.

---

# PHASE A — HUMAN REALITY BEFORE WORDS

## PROMPT 01 — BODY / NERVOUS SYSTEM STATE
For each character, infer only from canon/current scene what the body is doing: fatigue, pain, hunger, adrenaline, sensory load, posture, breath, movement pressure. Explain how that state constrains speech length, speed, precision and willingness to engage. Do not invent trauma or diagnosis. Output a compact BODY STATE CARD and flag any dialogue whose polish conflicts with the body state.

## PROMPT 02 — IMMEDIATE WANT VS BACKGROUND WANT
Separate what each character wants in the next two minutes from the larger desire driving the relationship/story. Identify contradictions. For every important line, state whether it pursues the immediate want, protects the background want, or accidentally exposes the deeper want. Flag lines with no behavioral motive.

## PROMPT 03 — FEAR / SHAME / STATUS RISK
Map what each person risks by speaking honestly now: rejection, humiliation, authority loss, intimacy, blame, punishment, appearing weak, losing control. Identify what words would therefore be difficult or unavailable. Flag dialogue that unrealistically jumps over the risk.

## PROMPT 04 — KNOWLEDGE BOUNDARY
Create a per-character `KNOWN / BELIEVED / SUSPECTED / UNKNOWN / WRONG` table. Check every line for impossible knowledge, overly perceptive inference, information the listener already knows, and exposition that exists only for the audience. No prose rewrite yet.

## PROMPT 05 — RELATIONSHIP DEBT
Map affection, resentment, attraction, obligation, rivalry, guilt, dependency, old wounds and trust. Identify the 2–4 relationship facts most likely to distort how each line is heard. Show how the same sentence would mean something different if spoken by another person.

## PROMPT 06 — POWER / STATUS / PERMISSION
Separate formal authority from emotional authority. Who can interrupt whom? Who can leave? Who needs politeness? Who is allowed to joke? Who can ask invasive questions? Flag dialogue that ignores the actual status geometry.

## PROMPT 07 — DEFAULT DEFENSE MECHANISM
For each character identify the established conversational defense: precision, joke, attack, withdrawal, caretaking, problem-solving, silence, intellectualization, compliance, status play, distraction. Test whether the scene uses character-specific defenses or gives everyone the same rhetorical toolkit.

## PROMPT 08 — COMMON GROUND / MISALIGNMENT
What do both people assume is shared? What is actually not shared? Where could misunderstanding, false agreement, repair or clarification naturally arise? Do not add misunderstandings for texture. Identify only state-supported opportunities.

---

# PHASE B — SPEAKER VOICE / RESPONSE MECHANICS

## PROMPT 09 — SPEECH FINGERPRINT
For each recurring speaker derive a fingerprint from existing canon/text: vocabulary source, abstract/concrete ratio, average sentence length, directness, hedges, certainty, humor, metaphor domain, question style, correction style, apology style, profanity boundary, silence tolerance, stress compression. Include 5 `WOULD SAY` tendencies and 5 `WOULD NOT NATURALLY SAY` tendencies. Do not invent catchphrases.

## PROMPT 10 — AGE / CULTURE / PROFESSION FILTER
Audit the scene for speech that is too old, too young, too professional, too therapeutic, too literary, too internet-coded or too generic. Distinguish unusual-but-earned articulation from authorial leakage. Output only suspect lines and reasons.

## PROMPT 11 — LISTENING TRACE
For every important reply, identify exactly what previous word, gesture, silence or implication it responds to. If no plausible trigger exists, mark `RESPONSE_FLOATS`. If it responds to theme/reader information rather than the partner, mark `AUTHOR_RESPONSE`.

## PROMPT 12 — RESPONSE LATENCY / FRICTION
Ask whether the character would answer immediately. Consider pause, task interference, mishearing, emotional lag, refusal, self-correction, overlap or abandoning the answer. Recommend friction only where caused by state. Never add filler mechanically.

## PROMPT 13 — TACTIC VERBS
Translate each major line from sentence into playable action: reassure, corner, test, shame, deflect, provoke, seduce, minimize, warn, recruit, expose, conceal, delay, repair, punish, gain permission. If a line has no action verb, it probably does not belong or is exposition.

## PROMPT 14 — TACTICAL CHANGE
Map when a tactic fails and what the speaker tries next. A scene with the same tactic for 20 lines is flat. A scene where every response instantly works is false. Mark the exact beat where strategy changes.

## PROMPT 15 — SILENCE / UNSAID PASS
Identify what is emotionally or strategically unsayable. Locate one or more places where silence, physical action or incomplete speech may carry more truth than an explanatory line. Do not cut dialogue unless the silent alternative preserves story clarity.

## PROMPT 16 — CHARACTER SEPARABILITY BLIND TEST
Remove speaker names mentally. Estimate which lines can still be assigned to one speaker from vocabulary/tactic alone. Mark interchangeable lines. If multiple principals share the same correction syntax, joke cadence or abstract phrasing, flag `VOICE_CONVERGENCE`.

---

# PHASE C — AUTHORIAL LEAK / NATURALISM / SCENE DESIGN

## PROMPT 17 — CLEVERNESS DENSITY AUDIT
Mark polished, aphoristic, witty, symmetrical or rhetorical lines. Do not call them bad automatically. For each, ask: who owns this cleverness, what does it cost/reveal, and could another character have said it? Flag three or more consecutive writerly lines without behavioral friction as `CLEVERNESS_CLUSTER`.

## PROMPT 18 — HOUSE-STYLE REPETITION AUDIT
Search current chapter/book evidence for repeated frames such as `I know`, `That is not...`, `apparently`, `technically`, `exactly`, perfect corrections, similar joke structures and narrator irony. Classify each recurring pattern: CHARACTER SIGNATURE / RELATIONSHIP SIGNATURE / NECESSARY REGISTER / AUTHOR HOUSE STYLE / GENERATED REPETITION. Recommend reduction only for the last two.

## PROMPT 19 — EXPOSITION AS ACTION
For every factual line, answer: why this speaker says it now, what effect they seek, why the listener needs it, and what resistance exists. Convert unsupported exposition into action-motivated delivery or move it to narration/behavior. Preserve facts and clue order.

## PROMPT 20 — SCENE TURN / VALUE SHIFT
State the scene's opening relationship/value charge, the turn, and the exit state. Prove the turn occurs through behavior/action, not a thematic declaration. If lines can be rearranged without damaging cause/effect, flag `DIALOGUE_ACTIVITY_NOT_ACTION`.

---

# PHASE D — TEXT VS PERFORMANCE DIAGNOSIS

## PROMPT 21 — READ-ALOUD NATURALISM
Read the scene mentally as performance, not prose. Mark breathless sentence loads, tongue-twister syntax, unnatural emphasis requirements, lines that need acting tricks to sound credible, and spots where pause/overlap could reveal existing subtext. Preserve exact text in diagnosis phase.

## PROMPT 22 — PERFORMANCE / WRITING SPLIT
Given audio or a performance plan, classify every reported break as one of: PERFORMANCE_DEFECT / WRITING_DEFECT / ADAPTATION_DEFECT / TRANSLATION_DEFECT / CONTEXT_REQUIRED / NO_DEFECT. Give evidence. Do not rewrite text for a performance defect.

## PROMPT 23 — MINIMAL A/B REPAIR
Only for proven WRITING_DEFECTS, produce A = current line and B = smallest plausible repair that preserves objective, clue, relationship state and voice. No global polish. Each B must state what failure it fixes. If no meaningful improvement, return KEEP A.

## PROMPT 24 — REGRESSION / HUMAN BELIEF GATE
After repair, run: character identity, knowledge boundaries, clue causality, relationship consent/authority, scene turn, voice separability, read-aloud credibility and chapter continuity. Output FATAL / MAJOR / MEDIUM / POLISH. PASS requires FATAL=0 and MAJOR=0. Record uncertain aesthetic issues as HUMAN_SIGNAL_REQUIRED rather than faking certainty.

---

# FULL-SCENE INTEGRATED PROMPT

Use when one model must run the full stack:

```text
You are the IVDIVO Human Scene + Dialogue Naturalism Integrator.

Authority first. Preserve all locked story facts and text-protection boundaries.

Run the scene through 24 lenses in four phases:
A HUMAN REALITY: body state; immediate/background wants; fear/status risk; knowledge boundary; relationship debt; power/permission; defenses; common-ground misalignment.
B VOICE/RESPONSE: speech fingerprints; age/culture/profession; listening trace; latency/friction; tactic verbs; tactical changes; silence/unsaid; blind speaker separability.
C NATURALISM: cleverness density; house-style repetition; exposition-as-action; scene turn/value shift.
D DIAGNOSIS/REPAIR: read-aloud; performance-vs-writing classification; minimal A/B patches; regression/human-belief gate.

Do not reward raw everyday chatter. Target fictional authenticity: compressed meaning that feels spontaneously generated by this specific character in this specific moment.

Do not rewrite until the earliest failing layer is identified.
Do not solve performance problems with prose changes.
Do not add random stutters, filler, slang, interruptions or gestures.
Do not reduce intelligent characters to generic speech.
Do not let multiple characters share the same clever correction syntax unless canon supports it.

Return:
1. HUMAN_SCENE_STATE_CARD
2. SPEECH_FINGERPRINTS
3. DIALOGUE_BEAT_MAP
4. SUSPECT_LINES with failure codes
5. TEXT_VS_PERFORMANCE classification
6. minimal A/B patches only where justified
7. NATURALISM_QC_REPORT
8. FATAL/MAJOR/MEDIUM/POLISH counts
9. HUMAN_SIGNAL_REQUIRED items
10. exact next action.
```

---

# LESSON ZERO DIAGNOSTIC PROMPT

```text
Do NOT rewrite LESSON ZERO globally.

Use the current reading edition and current locked/development authority. Analyze a representative 45–60 minute sample including:
- early five-person interaction;
- Ethan/Aoife private conversation;
- Lesson Zero institutional interaction;
- one friendship conflict;
- one later high-stakes scene.

Run the 24-pass Naturalism stack.
Track cross-book recurrence of `I know`, `That is...`, `apparently`, correction frames and joke structures, but treat frequency as a signal, not a verdict.

Key question:
Does the manuscript create genuinely distinct spontaneous speech, or does a shared authorial rhetorical engine leak across characters?

Separate TEXT failure from PERFORMANCE failure.
The `failing investment bank` line is a test case, not an assumed defect.

Output a ranked repair map. No bulk rewriting until properly directed audio and/or reader evidence confirms WRITING_DEFECT.
```

---

# SMITH PRE-DRAFT PROMPT

```text
Before drafting each major SMITH scene, build HUMAN_SCENE_STATE_CARD + SPEECH_FINGERPRINTS for all principals.

For every planned dialogue beat prove:
- who heard what;
- what they want;
- what they cannot say;
- what tactic they choose;
- how the other person resists or misreads it;
- how the tactic changes;
- what behavior turns the scene;
- why the exact words belong to this speaker rather than the author.

Reject dialogue whose primary function is explaining the world, theme or plot to the reader.
Reject major-character lines that would remain equally plausible after swapping speaker names.
Pass through Prompt 17, 18, 21 and 24 before chapter lock.
```

**24 PASSES, BUT ONE PURPOSE: MAKE THE CHARACTER CAUSE THE LINE.**
