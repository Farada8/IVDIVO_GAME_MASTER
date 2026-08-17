# IVDIVO REFERENCE STUDY PASS 13 — DIALOGUE / SUBTEXT / VOICE

Date: 2026-08-17
Status: REFERENCE ONLY / WORKING TOOL
Canon effect: NONE

## PURPOSE
Turn the existing IVDIVO law `DIALOGUE = ACTION` into an executable dialogue engine and gate based on multiple independent craft sources.

## SOURCES

### 1. Robert McKee — *Dialogue: The Art of Verbal Action for Page, Stage, and Screen*
Primary Drive ID: `1u8KCZkyUxJ7vd6rKM6sB7SKTMv7CA898`
Shelf: `01_WRITING_CRAFT/04_DIALOGUE_VOICE_SUBTEXT`
Text status: FULL TEXT EXTRACTABLE
Role: PRIMARY CRAFT SOURCE

Key mechanism:
A spoken line is not information delivery; it is an action chosen to pursue a desire. Under the surface text sits intent/subtext. A sequence of verbal actions and reactions changes the scene beat by beat.

Important operational consequences:
- beneath a meaningful line there should be desire/intention/action;
- speech is a tactic, not a transcript of thought;
- silence can itself be an action when speech is expected;
- conflict loads words with implication;
- dialogue should move the character closer to or farther from what they want;
- scene dialogue can be analyzed as action/reaction beats around a turning point.

### 2. Tom Chiarella — *Writing Dialogue*
Drive ID: `1IbW87QTdMJjsbMRda02GFpkJqmgsgziD`
Shelf: `01_WRITING_CRAFT/04_DIALOGUE_VOICE_SUBTEXT`
Text status: FULL TEXT EXTRACTABLE
Role: PRIMARY CRAFT SOURCE

Key mechanism:
Good fictional dialogue is shaped, not recorded. Even apparently neutral replies contain resistance, distance, direction and rhythm. Turns, pauses, reversals and silence generate dramatic energy.

Important operational consequences:
- every reply does not need to answer the literal question;
- resistance can be tiny: refusal to elaborate, change of subject, a short answer, a joke, a pause;
- dialogue may appear misdirected while still accumulating tension;
- compression matters: real conversation contains repetition and filler that fiction does not need;
- rhythm and interruption are structural tools, not decorative realism.

### 3. Charles Baxter — *The Art of Subtext*
Drive ID: `1AhgBpBaL5pFS4GkMdq5Q7Xs6vINCdxLh`
Shelf: `01_WRITING_CRAFT/04_DIALOGUE_VOICE_SUBTEXT`
Text status: FULL EPUB TEXT EXTRACTED
Role: PRIMARY SUBTEXT / LITERARY CRAFT SOURCE

Key mechanism:
A strong scene may be driven less by what characters admit they want than by desires they cannot acknowledge. That creates a subterranean pressure system under the literal conversation.

Important operational consequences:
- subtext becomes strongest when direct admission is socially, emotionally or morally difficult;
- silence can destabilize the other speaker and force a tactic change;
- physical behavior around speech can contradict or intensify the words;
- talking does not automatically solve conflict; conversation can worsen the problem;
- a scene can carry several incompatible meanings at once rather than resolving into one clean thematic statement.

### 4. Linda Seger — *Hidden Meaning / Creating Subtext in Film* (Russian edition)
Drive ID: `1ansnpIvHRvaw5TAQCJXO--UNCe-HgSxV`
Shelf: `01_WRITING_CRAFT/04_DIALOGUE_VOICE_SUBTEXT`
Text status: FULL TEXT EXTRACTABLE
Role: PRIMARY SUBTEXT CRAFT SOURCE

Key mechanism:
Spoken content, behavior, situation and known context can point in different directions. A character may consciously hide the truth or reveal an unrecognized inner conflict through the discrepancy between words and action.

Important operational consequences:
- subtext can be conscious or unconscious;
- physical action can make a spoken claim read differently;
- audience knowledge changes the meaning of an otherwise ordinary line;
- contradiction between text and behavior creates interpretive pressure;
- the writer should know what the character is protecting even when the character does not formulate it cleanly.

---

# SOURCE CONTROL — MCKEE COPIES

English primary candidate:
`1u8KCZkyUxJ7vd6rKM6sB7SKTMv7CA898` — 1,766,841 bytes.

English alternate scan:
`1-4bLQ6j3rdjl-U2vXxkP6lSUTeJgjS9-` — 1,694,371 bytes.

Both extract to approximately 498k characters and clearly contain the same work/edition family, but raw sizes differ and normalized extracted-text hashes are not identical. Therefore:
- DO NOT classify as BYTE_IDENTICAL_DUPLICATE;
- retain primary + ALTERNATE_SCAN.

Russian translation:
`1Tvhhn78YZfa96jlyR43PShpAbGA_iwDs` — keep as ALTERNATE_TRANSLATION, not duplicate.

---

# PASS 13 — EXECUTABLE DIALOGUE ENGINE

## CORE LOOP

CHARACTER WANT
-> CHOSEN VERBAL TACTIC
-> OTHER PERSON RESISTS / MISREADS / COUNTERS
-> STATUS OR INFORMATION SHIFTS
-> TACTIC CHANGES
-> UNSAID PRESSURE INCREASES OR BREAKS
-> SCENE TURN

If the same tactic repeats without changed pressure, the dialogue is probably stalled.

## CARD 1 — EVERY IMPORTANT LINE DOES SOMETHING
For every meaningful line, identify a verb:
PERSUADE / TEST / DEFLECT / SEDUCE / SHAME / REASSURE / PROVOKE / DELAY / CONCEAL / RECRUIT / THREATEN / BARGAIN / DISMISS / SIGNAL BELONGING / REPAIR STATUS / ESCAPE.

If the line has no actionable verb and only informs the reader, rewrite or move the information into causal action.

## CARD 2 — RESPONSE ≠ ANSWER
A character does not owe the previous speaker a literal response.

Possible counteractions:
- answer another question;
- attack the premise;
- joke;
- stay silent;
- change subject;
- demand proof;
- leave;
- answer too narrowly;
- expose something the first speaker wanted hidden.

This prevents scripted round-robin dialogue.

## CARD 3 — SUBTEXT GAP
For each important speaker track:
WHAT THEY SAY
vs.
WHAT THEY WANT
vs.
WHAT THEY FEAR THE OTHER PERSON WILL NOTICE.

The larger the socially plausible gap, the more pressure can exist without explicit explanation.

## CARD 4 — SILENCE IS A MOVE
Do not write silence as empty atmosphere.

Ask:
WHO EXPECTED AN ANSWER?
WHAT DOES THE REFUSAL TO ANSWER DO TO THEM?
WHAT TACTIC DO THEY TRY NEXT?

## CARD 5 — TACTIC SHIFT RULE
A dialogue beat changes when a character changes method.

Example abstract sequence:
ASK -> JOKE -> ACCUSE -> WITHDRAW -> OFFER -> THREATEN -> ADMIT.

The exact tactics depend on character. The important thing is that resistance forces adaptation.

## CARD 6 — PHYSICAL COUNTERTEXT
OBJECT/ACTION can contradict WORDS.

Examples at mechanism level:
- says calm words while destroying an object;
- claims indifference while blocking an exit;
- says yes while delaying the action;
- jokes while checking who is listening.

Use sparingly. Do not turn every line into theatrical contradiction.

## CARD 7 — VOICE = PRESSURE PATTERN, NOT VOCABULARY LIST
Distinct voice is not merely slang or sentence length.

Track for each character:
- preferred tactic under threat;
- what they joke about;
- what they refuse to name;
- how quickly they answer;
- whether they ask questions or make assertions;
- how they handle status loss;
- what they notice first;
- how they lie;
- how they apologize;
- how they flirt;
- how they go silent.

Two characters can use the same vocabulary and still sound different because their pressure behavior differs.

## CARD 8 — GROUP DIALOGUE IS NOT A PANEL
For each participant:
OBJECTIVE / STATUS / PRIVATE KNOWLEDGE / FEAR / TACTIC / EXIT CONDITION.

Then permit unequal participation.
A person may dominate, fail to speak, interrupt, leave, get ignored or change alliance.

## CARD 9 — EXPLANATION MUST BE CONTESTED
If information must be verbalized, attach it to a conflict:
- somebody doubts it;
- somebody wants it withheld;
- somebody uses it to gain authority;
- somebody understands it differently;
- somebody realizes what it implies before the speaker does.

## CARD 10 — CONVERSATION CAN MAKE THINGS WORSE
Do not assume honesty produces immediate healthy resolution.
A confession may:
- transfer guilt;
- destroy trust;
- expose leverage;
- force a choice;
- create a new misunderstanding;
- reveal incompatible wants.

---

# IVDIVO DIALOGUE GATE v0.1

Before a major conversation is GREEN:

1. WHO wants WHAT from WHOM in this scene?
2. Why must they talk NOW rather than later?
3. What does the other person want instead?
4. What is each person's starting status?
5. What information is asymmetric?
6. What is each speaker unwilling to say directly?
7. What tactic does each start with?
8. Where does resistance force a tactic change?
9. What silence / interruption / refusal matters?
10. What physical action changes the meaning of words?
11. What new fact, status, decision or relationship state exists at the end?
12. Could three consecutive lines be reassigned to another character without damage? If yes, voice is insufficiently specific.
13. Does the conversation end with everyone correctly articulating the theme? If yes, RED TEAM it.
14. If all exposition were removed, would there still be a conflict? If no, the scene is probably an information briefing.

---

# ORBITAL YOUTH APPLICATION

Teen dialogue should especially preserve:
- embarrassment avoidance;
- flirtation disguised as mockery/help;
- status repair;
- exclusion signals;
- private jokes;
- refusal to look uncool;
- money/work shame;
- parent/guardian code-switching;
- different speech with employer vs friend vs romantic interest;
- silence after social injury.

Do not make teenagers verbalize their developmental psychology.

## Orbital-specific example mechanism
A teenager knows a transit rule is being violated but does not say so directly because admitting how they know would expose a forbidden job favor, crush, debt or access privilege.

The world rule enters dialogue as leverage, not lecture.

---

# SMITH APPLICATION

Smith conversations should often involve:
- jurisdictional testing;
- controlled disclosure;
- old professional shorthand;
- interrogation by hypothesis rather than accusation;
- strategic silence;
- questions whose real target is not the literal answer;
- Confederation personnel who interpret the same fact through a different institutional model.

Enia dialogue must not become oracle exposition. Enia should change Smith's question, assumption or action threshold, not simply state the plot solution.

---

# RED TEAM ADDITIONS

MAJOR:
- five smart answers in sequence;
- exposition with no owner/resistance;
- speaker repeats same tactic for a full scene;
- confession instantly solves the relationship;
- every character says exactly what they feel;
- all voices distinguished only by slang;
- group scene gives equal airtime regardless of status/objective.

MEDIUM:
- dialogue has conflict but no turn;
- subtext is identical to text;
- pauses/silences are decorative;
- physical business does not alter meaning;
- witty lines repeatedly reduce pressure instead of changing it.

POLISH:
- repeated sentence lengths;
- repeated reaction tags;
- excessive names in direct address;
- unnecessary greetings/farewells;
- overexplained emotional interpretation after the line.

# RESULT

The IVDIVO dialogue engine is now:

WANT -> TACTIC -> RESISTANCE -> COUNTERTACTIC -> SUBTEXT PRESSURE -> STATUS/INFO SHIFT -> TACTIC CHANGE -> TURN -> CONSEQUENCE.

Dialogue is successful when something is *done* to another person and the relationship/action state changes — not when every necessary fact has been spoken aloud.
