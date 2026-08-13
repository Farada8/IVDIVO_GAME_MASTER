# IVDIVO ↔ Sudowrite Integration v1

## Role
Sudowrite is the **fiction-drafting and prose-development layer** of the IVDIVO production system. It is not the authority for canon, market research, source-book analysis, or final approval.

Current official Sudowrite features relevant to this workflow: Story Bible; Genre; Style; Synopsis; Characters; Worldbuilding; Outline; Scenes; Draft; Write/Guided; Rewrite; Expand; Chapter Continuity; Plugins; selectable prose modes/models.

## Source of truth hierarchy
1. `project_state.json` — current production state.
2. IVDIVO canon cards / canon corpus — authoritative world facts.
3. Approved season bible / episode passport / scene map — approved plot.
4. Sudowrite Story Bible — **working mirror** of the approved material for prose generation.
5. Sudowrite Draft/Write output — draft only, never canon automatically.

## What Sudowrite MAY do
- turn an approved scene into fiction prose;
- generate alternate prose versions of the same approved beat;
- improve sensory grounding, flow, dialogue texture, pacing inside a scene;
- draft chapter prose from approved Scenes;
- use Story Bible and Chapter Continuity to maintain local continuity;
- run custom plugins for dialogue, anti-cliche, sensory grounding, audio clarity, or POV checks.

## What Sudowrite MUST NOT do
- invent new IVDIVO canon;
- change the episode outcome;
- add a new power, rank, office, world law, or historical fact without approval;
- replace an approved character motivation;
- import plot surface from reference novels;
- resolve canon tensions on its own;
- generate the whole novel from a vague braindump and treat it as approved architecture.

## Mapping our system → Sudowrite Story Bible

### Braindump
Paste only the approved **episode/novel production brief**, not the whole research library.
Required content:
- franchise promise;
- season premise;
- current episode goal;
- local human problem;
- IVDIVO rule under test;
- forbidden inventions;
- tone constraints;
- current unresolved question.

### Genre
Use a compact production label, e.g.:
`metaphysical thriller / institutional mystery / speculative investigation / long-form audio fiction`

### Style
Style is **project style**, never “write like [living/dead author]”.
Include:
- direct, concrete prose;
- strong physical grounding;
- professional procedural detail when relevant;
- restrained metaphysical language;
- no fake profundity;
- no repetitive AI cadence;
- no unexplained omniscience;
- dialogue driven by goals/status/subtext;
- audio clarity at normal playback speed.

### Synopsis
Use the approved **episode passport** or approved novel/season synopsis.
Do not let Sudowrite generate a new central plot unless the Showrunner explicitly requests brainstorming.

### Characters
Each recurring character card must contain:
- role in story;
- role in institution;
- conscious want;
- deeper need;
- fear/shame;
- competence;
- status / office / initiation coordinates when relevant;
- knowledge boundary;
- relationship to other recurring characters;
- speech logic;
- what the character will not do;
- current episode state.

### Worldbuilding
Only approved `[IVDIVO CANON]` material needed for the current book/season/episode.
Do not dump the entire cosmology into Story Bible.
For each world card include:
- term;
- operational meaning;
- observable consequence;
- who can perceive/use it;
- limitation/prohibition;
- what is still unknown;
- source/canon status.

### Outline
Use the approved season/novel outline.
For an audio episode, outline should preserve:
- opening human problem;
- anomaly;
- investigation/action chain;
- midpoint redefinition;
- irreversible choice;
- price;
- climax mechanism;
- local resolution;
- caused larger question.

### Scenes
Sudowrite Scene = our approved `scene_card`.
Paste into Scene Extra Instructions:
- POV;
- immediate goal;
- obstacle;
- action;
- new actionable information;
- turn;
- relationship delta;
- institution delta;
- price;
- exit state;
- exact canon needed;
- forbidden additions;
- mechanism IDs.

## Drafting mode
Preferred order:
1. Build/verify Story Bible manually from approved project artifacts.
2. Create approved Scenes.
3. Use **Draft** for a first chapter/scene batch when structure is already locked.
4. Use **Guided Write** for local continuation and corrections.
5. Use **Rewrite** only after structural accuracy is confirmed.
6. Use **Expand/Describe** sparingly and only when the scene is underdeveloped physically/sensorily.
7. Export draft back to IVDIVO pipeline for Red Team / Canon Audit / Source-Distance Audit / Audio Pass.

## Handoff: Scene Card → Sudowrite
Template:

```text
SCENE ID: {{scene_id}}
POV: {{pov}}
LOCATION: {{location}}
IMMEDIATE GOAL: {{goal}}
OBSTACLE: {{obstacle}}
ACTION: {{action}}
NEW ACTIONABLE INFORMATION: {{new_info}}
TURN: {{turn}}
RELATIONSHIP DELTA: {{relationship_delta}}
INSTITUTION DELTA: {{institution_delta}}
PRICE: {{price}}
EXIT STATE / EXIT QUESTION: {{exit_state}}
CANON NEEDED: {{canon_needed}}
FORBIDDEN NEW CANON: yes
MECHANISMS: {{mechanism_ids}}

PROSE RULES:
- Write only this approved scene.
- Do not change the scene outcome.
- Do not add new world rules, powers, ranks, backstory facts, or hidden organizations.
- Keep the physical task/location active.
- Dialogue must pursue concrete goals and reflect status/knowledge asymmetry.
- Explain IVDIVO terminology only when the POV character needs it for the current action.
- Avoid generic mystical language and AI-style aphoristic fragments.
- End after the specified state change.
```

## Handoff: Sudowrite → IVDIVO
Every generated scene returns with:
- scene draft;
- actual state delta;
- any new factual claims introduced by prose;
- any deviations from scene card;
- unresolved ambiguity;
- estimated audio duration.

Then mandatory passes:
1. Structural delta check.
2. IVDIVO Canon Audit.
3. Institutional Realism Pass.
4. Anti-GPT / Cliche Red Team.
5. Source-Distance / Copyright Check.
6. Audio-First Pass.
7. Showrunner approval.

## Plugins to build in Sudowrite
1. `IVDIVO Scene Guard` — checks whether generated prose changed approved scene outcome or invented canon.
2. `IVDIVO Dialogue Pressure` — improves goal/subtext/status asymmetry without changing plot.
3. `IVDIVO Concrete Metaphysics` — replaces vague mystical adjectives with observable canon-grounded effects.
4. `IVDIVO Anti-GPT` — flags generic profundity, repetitive syntax, empty ominous phrasing, and exposition disguised as dialogue.
5. `IVDIVO Audio Clarity` — improves speaker/location clarity and listening comprehension without simplifying content.

## Practical limitation
Until an official automation/API path is confirmed, Sudowrite is treated as a **human-in-the-loop drafting workstation**. GitHub/Drive remain the persistent machine-readable sources of truth. We transfer approved Story Bible/Scene material into Sudowrite and bring drafts back for audit.
