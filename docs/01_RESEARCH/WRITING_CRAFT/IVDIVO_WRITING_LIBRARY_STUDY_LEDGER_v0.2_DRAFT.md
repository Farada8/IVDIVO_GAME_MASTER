# IVDIVO WRITING LIBRARY — STUDY LEDGER

**Code:** CRAFT-001  
**Version:** v0.2  
**Status:** DRAFT EXECUTION DOCUMENT / FOUNDER DIRECTIVE RECORDED  
**Date:** 2026-08-15  
**Owner / Founder:** Yaromyr Farada  
**Supersedes:** `IVDIVO_WRITING_LIBRARY_STUDY_LEDGER_v0.1_DRAFT.md`  
**Purpose:** превратить загруженную библиотеку книг по писательскому мастерству, нарратологии, психологии чтения и художественных референсов в реально изученный, сопоставленный, проверенный и операционализированный корпус для производства книг, рассказов и сериалов IVDIVO.

---

# 0. FOUNDER DIRECTIVE

Прямое указание основателя:

> Изучить каждую загруженную книгу и внести извлечённые знания в проект, чтобы они применялись при написании.

Из этого следует:

1. `UPLOADED` ≠ `STUDIED`;
2. оглавление ≠ прочитанная книга;
3. поиск нескольких цитат ≠ прочитанная книга;
4. тематический read-pass ≠ полный read-pass;
5. дубликаты не увеличивают epistemic weight;
6. каждая идея должна иметь source provenance;
7. метод автора не принимается автоматически как истина;
8. конфликтующие школы должны сравниваться;
9. механизм должен быть переведён в production-test;
10. внешняя художественная форма не копируется;
11. знания должны проверяться на реальной рукописи;
12. только после полного цикла источник получает статус `STUDIED + INTEGRATED`.

---

# 1. BASELINE CORPUS

Последний формальный baseline-аудит библиотеки зафиксировал:

- **171** файл;
- **100** файлов с эвристическим статусом `LIKELY_FULL`;
- **40** явных fragment/demo;
- **12** collections;
- **2** scanned/text-unavailable;
- duplicate groups.

После baseline были загружены дополнительные книги. Поэтому 171/100 — историческая нижняя граница, а не текущий окончательный объём библиотеки.

**Обязательная единица учёта:** уникальное произведение/издание, а не файл. PDF + EPUB одной книги = один source record, если содержание эквивалентно.

---

# 2. SOURCE CLASSES

## A. CRAFT CORE
Story, novel, scene, character, POV, dialogue, prose, revision.

## B. CRAFT SPECIALIST
YA, romance, mystery, suspense/thriller, SF, series/TV, game narrative, action, humor, emotional writing, line editing.

## C. THEORY / NARRATOLOGY / CRITICISM
Aristotle, narratology, semiotics, rhetoric of fiction, genre theory, literary criticism.

## D. READER PSYCHOLOGY / COGNITION
Curiosity, prediction, attention, transportation, empathy, status, memory, surprise, narrative comprehension.

## E. FICTION MECHANISM LAB
Novels, stories, scripts, manga/serial texts: reverse engineer actual mechanisms without copying surface.

## F. WORLD / PHILOSOPHY SOURCE
Worldbuilding, philosophy, science, history, religion, institutions. These sources do not automatically define fiction craft.

---

# 3. REQUIRED 12-STAGE STUDY LIFECYCLE

A source moves only forward through the following stages. No stage may be silently skipped.

## STAGE 1 — REGISTERED
Record:
- author;
- title;
- edition/year if known;
- format(s);
- duplicate group;
- source class;
- primary expected role.

**Pass condition:** source identity is unambiguous.

## STAGE 2 — INTEGRITY VERIFIED
Determine:
- FULL;
- PARTIAL;
- DEMO/FRAGMENT;
- COLLECTION;
- SCAN;
- DAMAGED;
- DUPLICATE;
- OCR risk.

**Pass condition:** we know what portion of the work is actually available.

## STAGE 3 — FULL READ PASS
Read the available full relevant text, not metadata or TOC only.

For long anthologies/academic collections, component essays/chapters may be tracked independently, but incomplete coverage must remain explicit.

**Pass condition:** chapter/section coverage log exists.

## STAGE 4 — STRUCTURE MAP
Map the internal architecture:
- chapters/parts;
- progression of argument;
- recurring concepts;
- examples/case studies;
- exercises;
- conclusion;
- internal dependencies.

**Pass condition:** we can explain how the book builds its method, not only list isolated tips.

## STAGE 5 — SOURCE PASSPORT
Record:
- main problem addressed;
- school/tradition;
- key terms;
- scope;
- assumptions;
- intended medium/genre;
- strongest contribution;
- weak/dated areas;
- source genealogy/influences if identifiable.

**Pass condition:** the book has a clear professional role in the library.

## STAGE 6 — CLAIM EXTRACTION
Separate what the source actually claims from our synthesis.

For each major claim:
`CLAIM ID | SOURCE LOCATION | CLAIM | AUTHOR'S EXAMPLE/EVIDENCE | DOMAIN`

**Pass condition:** no major operational rule is attributed vaguely to the book.

## STAGE 7 — MECHANISM EXTRACTION
Convert advice/observation into transferable mechanisms:

`MECHANISM → INPUTS → PROCESS → OUTPUT → READER EFFECT → CONDITIONS`

For fiction references:
`OBSERVED EFFECT → TEXTUAL DECISION → STORY/SCENE/POV/PROSE MECHANISM`

**Pass condition:** source yields concrete mechanisms, not only summary.

## STAGE 8 — LIMITS / FAILURE MODES
For every important mechanism ask:
- When does it fail?
- Which genres/forms does it not fit?
- What happens if overused?
- Is it prescription, description, interpretation, or empirical claim?
- Is the evidence anecdotal/secondary/primary?
- What does the author underweight?

**Pass condition:** mechanism is bounded, not dogma.

## STAGE 9 — CROSS-SOURCE COMPARISON
Compare with independent schools/sources.

Record:
`AGREES WITH | CONTRADICTS | DIFFERENT SCALE | DIFFERENT TERMINOLOGY | SOURCE DEPENDENCE`

Repeated wording across derivative books does not count as independent confirmation.

**Pass condition:** key mechanism has a place in the conflict/convergence map.

## STAGE 10 — IVDIVO OPERATIONALIZATION
Translate the mechanism into:
- Story Contract field;
- Character passport;
- Scene card;
- clue ledger;
- POV/knowledge budget;
- prose audit;
- genre gate;
- revision pass;
- specialist-room duty;
- red-team question.

**Pass condition:** a writer/editor can actually use it.

## STAGE 11 — MANUSCRIPT VALIDATION
Test against real IVDIVO material or a controlled prototype.

Validation questions:
- Does the test detect a real defect?
- Does following it improve causality/clarity/emotion/retention?
- Does it create new artifacts or formulaic writing?
- Does it conflict with canon/specification?

**Pass condition:** result logged as `SUPPORTED / MODIFIED / REJECTED / NEEDS MORE TESTING`.

## STAGE 12 — SYNTHESIZED
Merge with the Body of Knowledge.

Requirements:
- duplicate mechanisms consolidated;
- source provenance retained;
- contradiction noted;
- final operational rule stated at correct confidence;
- no author-specific surface copied.

**Pass condition:** knowledge is part of the active IVDIVO writing system.

---

# 4. SYSTEM-LEVEL PASS — REGRESSION

After new books are synthesized, older IVDIVO rules must be rechecked.

A later source may show that an earlier rule was:
- too narrow;
- too absolute;
- genre-specific;
- derivative;
- contradicted by stronger evidence;
- missing a failure mode.

Therefore periodically run:

`NEW KNOWLEDGE → CONFLICT SCAN → AFFECTED GATES → CHANGE PROPOSAL → VERSION UPDATE → MANUSCRIPT REGRESSION`

This is not Stage 13 of a single source; it is a recurring system-maintenance process.

---

# 5. TERMINAL STATUS RULES

Only these labels are allowed:

- `REGISTERED`
- `VERIFIED`
- `READ PARTIAL`
- `READ FULL`
- `MAPPED`
- `PASSPORTED`
- `CLAIMS EXTRACTED`
- `MECHANISMS EXTRACTED`
- `LIMITS ANALYSED`
- `CROSS-COMPARED`
- `OPERATIONALIZED`
- `MANUSCRIPT-TESTED`
- `STUDIED + INTEGRATED`
- `FRAGMENT — CANNOT COMPLETE`
- `DUPLICATE — NO INDEPENDENT WEIGHT`
- `REJECTED AS CRAFT SOURCE`

**Forbidden completion language:** “studied” when actual status is thematic/partial extraction.

---

# 6. SOURCE FINDING RECORD

Every important finding uses:

`SOURCE / LOCATION`
`→ CLAIM OR OBSERVED MECHANISM`
`→ WHY IT WORKS`
`→ CONDITIONS`
`→ FAILURE MODES`
`→ CROSS-SOURCE SUPPORT/CONFLICT`
`→ IVDIVO TEST`
`→ VALIDATION RESULT`
`→ CONFIDENCE`

Confidence:
- `A` — strong cross-source + manuscript validation;
- `B` — strong craft support, validation incomplete;
- `C` — provisional/single-source useful hypothesis;
- `D` — idea lab only.

---

# 7. FICTION REVERSE-ENGINEERING PROTOCOL

For each A-tier fiction/script reference extract at least:

1. opening disturbance;
2. story promise;
3. main story / central question;
4. protagonist external objective;
5. human/emotional problem;
6. opposition system;
7. stakes;
8. clock/pressure;
9. relationship engine;
10. clue/reveal architecture;
11. scene causality;
12. chapter/sequence retention;
13. midpoint change;
14. crisis choice;
15. climax action;
16. local ending/payoff;
17. sequel/series door;
18. POV/knowledge function;
19. prose/voice function where relevant;
20. explicit `DO NOT COPY` surface list.

For especially important works add scene/sequence maps.

---

# 8. ANTI-IMITATION FIREWALL

Never transfer:
- names;
- recognizable characters;
- unique world systems;
- distinctive prose voice;
- signature metaphors/images;
- exact clue/puzzle;
- unique twist;
- recognizable sequence of events;
- setting with cosmetic noun replacement.

Transfer only abstracted mechanism after source-distance review.

---

# 9. CURRENT STUDY BATCHES

## CRAFT-003 — Batch 01
Focus: scene mechanics, YA, dialogue/subtext, reader psychology.

## CRAFT-004 — Batch 02
Focus: one-main-action story architecture, character causality, action, revelation→decision, character arcs.

## CRAFT-005 — Batch 03
Focus: plot/scene causality, value shifts, crisis/climax/resolution, scene→sequel, setting-as-action, prose/voice/revision.

## CRAFT-006 — Batch 04
Focus: series/serial, renewable engine, curiosity/model pressure, genre hierarchy, Coming-of-Age, SF, Detective/Thriller, Love Story.

## CRAFT-007 — Batch 05
Focus: drafting/discovery discipline, chapter treatments, reverse engineering, POV scope/knowledge budget, psychic distance, exercises, revision.

**Important:** batch membership means “material processed,” not automatically “source fully studied.”

---

# 10. CURRENT HIGH-PRIORITY CORPUS / CONSERVATIVE STATUS

| Source | Role | Conservative current status |
|---|---|---|
| Aristotle — *Poetics* | unity/action/probability/reversal/recognition | READ/EXTRACTION IN PROGRESS |
| John Truby — *The Anatomy of Story* | story architecture, revelations, scene weave | READ/EXTRACTION IN PROGRESS |
| John Truby — *The Anatomy of Genres* | genre obligations/mixing | THEMATIC READ + EXTRACTION IN PROGRESS |
| Robert McKee — *Story* | value change, scene/act, crisis/climax | READ/EXTRACTION IN PROGRESS |
| John Yorke — *Into the Woods* | nested change, acts/scenes, series/serial | THEMATIC READ + EXTRACTION IN PROGRESS |
| Will Storr — *The Science of Storytelling* | curiosity, model defense, status, reader psychology | THEMATIC READ + EXTRACTION IN PROGRESS |
| Lajos Egri — *The Art of Creative Writing* | character contradiction/motivation | READ/EXTRACTION IN PROGRESS |
| Dwight Swain — *Techniques of the Selling Writer* | scene/sequel, MRU | READ/EXTRACTION IN PROGRESS |
| Shawn Coyne — *The Story Grid* | developmental scene/genre diagnostics | THEMATIC READ + EXTRACTION IN PROGRESS |
| K.M. Weiland — *Structuring Your Novel* | long-form structure, scene/sequel | THEMATIC READ + EXTRACTION IN PROGRESS |
| K.M. Weiland — character arc corpus | Lie/Truth, Want/Need, arc families | PARTIAL/THEMATIC EXTRACTION |
| Jessica Brody — YA novel craft | YA genre/hero/beat logic | READ/EXTRACTION IN PROGRESS |
| Alice LaPlante — *The Making of a Story* | prose fiction craft/revision | READ PASS STARTED |
| Janet Burroway et al. — *Writing Fiction* | narrative craft/prose/POV | THEMATIC READ + EXTRACTION IN PROGRESS |
| Jack Hodgins — *A Passion for Narrative* | character-generated narrative/plot flexibility | THEMATIC READ + EXTRACTION IN PROGRESS |
| Jordan Rosenfeld — *The Sound of Story* | voice/syntax/lexicon/rhythm | THEMATIC READ + EXTRACTION IN PROGRESS |
| Anne Lamott — *Bird by Bird* | drafting/discovery/character/plot/voice/revision | THEMATIC READ + EXTRACTION IN PROGRESS |
| Bernays & Painter — *What If?* | controlled craft exercises/revision | THEMATIC READ + EXTRACTION IN PROGRESS |
| Erin M. Pushman — *How to Read Like a Writer* | formal reverse engineering | THEMATIC READ + EXTRACTION IN PROGRESS |
| Alicia Rasley — *The Power of Point of View* | POV architecture/reader knowledge | THEMATIC READ + EXTRACTION IN PROGRESS |
| Michael Noll — *Writer's Field Guide* | practical craft problem solving | THEMATIC READ + EXTRACTION IN PROGRESS |
| Orson Scott Card — *Characters & Viewpoint* | character/POV | PARTIAL EXTRACTION |
| David Corbett — *The Art of Character* | contradiction/secret/behavior | PARTIAL EXTRACTION |
| Stanislavski — *An Actor's Work* | objective/action/given circumstances | PARTIAL TRANSFER TO FICTION |
| Brandilyn Collins — *Getting Into Character* | acting→fiction character/action tools | PARTIAL EXTRACTION |
| Christopher Vogler — *Writer's Journey* | optional mythic lens | REGISTERED / PARTIAL |
| Joseph Campbell — *Hero with a Thousand Faces* | comparative myth | REGISTERED |
| Ignasi Ribó — *Prose Fiction* | narratology/story-discourse | READ PASS STARTED |
| Michael Breault — *Narrative Design* | objective/progression/agency | READ PASS STARTED |
| Edward James — SF criticism/history | genre literacy | READ PASS STARTED |

This table is intentionally conservative. No source above is marked `STUDIED + INTEGRATED` unless its complete 12-stage record exists.

---

# 11. PRODUCTION ROUTING

Only operationalized mechanisms may be claimed as active source use.

- **Story Architect:** Aristotle / Truby / McKee / Yorke / Coyne + cross-source synthesis.
- **Scene Room:** Swain / McKee / Coyne / Weiland / Rosenfeld / Burroway / Noll.
- **Character Room:** Egri / Storr / Corbett / Card / Stanislavski / Weiland / Collins.
- **YA Room:** Brody + Coming-of-Age + youth psychology.
- **POV Room:** Rasley / Card / Burroway / Pushman / LaPlante / narratology.
- **Voice/Prose Room:** Burroway / LaPlante / Rosenfeld / Pushman / later line-style corpus.
- **Genre Room:** Truby Genres + specialist sources + fiction reverse engineering.
- **Mystery Room:** backward event design + clue/suspect ledger + specialist corpus.
- **Red Team:** contradictions, source-distance, structural regression, formula detection.

---

# 12. NEXT EXECUTION PRIORITY

1. Continue ingestion and duplicate/integrity audit for new uploads.
2. Complete full read-pass for high-priority Tier A sources rather than accumulating endless partial statuses.
3. Maintain per-source passports/claim/mechanism records.
4. Expand CRAFT-002 Body of Knowledge only from extracted material.
5. Build cross-source conflict matrix.
6. Validate gates against Book 1 and controlled Book 2 prototypes.
7. Promote individual books to `STUDIED + INTEGRATED` only after Stage 12.
8. Run regression on older IVDIVO writing standards as stronger synthesis emerges.

---

# 13. NO FALSE COMPLETION

The library is a professional research corpus, not a decorative list of titles.

The project must always be able to answer:
- Which books are merely uploaded?
- Which are verified full texts?
- Which have full read coverage?
- Which claims came from which chapters/pages?
- Which mechanisms are cross-supported?
- Which were rejected or limited?
- Which are operationalized?
- Which were tested on manuscript?
- Which are truly `STUDIED + INTEGRATED`?

If these answers are unavailable, the project must say **not completed**, not infer completion from file presence.

---

# CHANGELOG

## v0.2 — 2026-08-15

- Replaced the earlier short status ladder with the founder-corrected 12-stage lifecycle.
- Added explicit full-read, structure-map, claim-extraction, limits/failure-mode, manuscript-validation, synthesis, and system-regression requirements.
- Added confidence levels and terminal status vocabulary.
- Added CRAFT-003 through CRAFT-007 study-batch tracking.
- Added conservative source-progress table.
- Explicitly forbids calling thematic/partial read passes “studied.”

## v0.1 — 2026-08-15

Initial study ledger. Superseded by v0.2.