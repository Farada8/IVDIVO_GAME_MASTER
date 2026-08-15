# IVDIVO WRITING LIBRARY — STUDY LEDGER

**Code:** CRAFT-001  
**Version:** v0.1  
**Status:** DRAFT EXECUTION DOCUMENT / FOUNDER DIRECTIVE RECORDED  
**Date:** 2026-08-15  
**Owner / Founder:** Yaromyr Farada  
**Purpose:** превратить загруженную библиотеку книг по писательскому мастерству и художественных референсов в реально изученный и операционализированный корпус для производства книг, рассказов и сериалов IVDIVO.

---

## 0. FOUNDER DIRECTIVE

Прямое указание основателя от 2026-08-15:

> Изучить каждую загруженную книгу и внести извлечённые знания в проект, чтобы они применялись при написании.

Это означает:

1. загрузка файла сама по себе НЕ считается изучением;
2. просмотр оглавления НЕ считается изучением;
3. чтение нескольких отрывков НЕ даёт права маркировать книгу `STUDIED`;
4. дубликаты одной книги не увеличивают вес идеи;
5. по каждой книге фиксируется её функция, извлечённые механизмы, ограничения и место применения;
6. художественные произведения используются как школа механизмов, а не как материал для копирования;
7. знания должны перейти из «конспекта» в конкретные production-tests для сюжета, сцены, персонажа, языка и редактуры.

---

## 1. BASELINE CORPUS

Последний формальный аудит `IVDIVO_STORY_ENGINE_v4_1_Professional_Framework.xlsx` зафиксировал:

- **171** файла в библиотеке;
- **100** файлов с эвристическим статусом `LIKELY_FULL`;
- **40** явных фрагментов / demo;
- **12** collections;
- **2** scanned/text-unavailable;
- отдельные duplicate groups.

После этого аудита в библиотеку были дополнительно загружены новые craft-книги и художественные референсы; поэтому эти числа являются **baseline, а не финальным текущим количеством**.

---

## 2. STUDY STATUS — ЕДИНАЯ ШКАЛА

Каждый уникальный источник проходит только вперёд по этой шкале:

`REGISTERED → INTEGRITY VERIFIED → READ PASS 1 → STRUCTURE/PASSPORT → MECHANISM EXTRACTION → CROSS-SOURCE SYNTHESIS → OPERATIONALIZED`

### REGISTERED
Файл найден, определены название/автор/формат/дубликаты.

### INTEGRITY VERIFIED
Проверено, что это FULL / FRAGMENT / COLLECTION / SCAN / DUPLICATE. Нельзя делать выводы о середине/кульминации книги по демо-фрагменту.

### READ PASS 1
Пройден сам текст, а не только metadata/contents. Для длинных академических сборников допускается разделение по главам/эссе с явным логом прогресса.

### STRUCTURE / PASSPORT
Зафиксированы: предмет книги, школа/модель, ключевые термины, область применимости, ограничения, спорные положения, связь с другими школами.

### MECHANISM EXTRACTION
Извлечены конкретные переносимые механизмы в формате:

`MECHANISM → INPUTS → PROCESS → OUTPUT → FAILURE MODES → DO-NOT-COPY → IVDIVO TEST`

### CROSS-SOURCE SYNTHESIS
Механизм сравнен минимум с одним независимым источником, когда такой источник существует. Совпадение нескольких авторов не превращается в несколько одинаковых правил — создаётся один core mechanism с несколькими supporting sources.

### OPERATIONALIZED
Знание встроено в production gate / checklist / story architecture / scene audit / character audit / prose audit и реально применяется при создании/редактировании текста.

**Только после OPERATIONALIZED допускается разговорное сокращение «книга изучена и встроена».**

---

## 3. SOURCE CLASSES

### A. CRAFT CORE
Прямые учебники по истории, роману, сцене, персонажу, POV, диалогу, стилю, редактуре.

### B. CRAFT SPECIALIST
YA, romance, suspense, mystery, SF, series/TV, game narrative, lyric/prose sound, cognitive story psychology.

### C. THEORY / NARRATOLOGY / CRITICISM
Aristotle, narratology, literary criticism, genre studies, philosophy of fiction, semiotics.

### D. FICTION MECHANISM LAB
Романы/рассказы/сценарии разбираются на реальные работающие механизмы: story promise, objective, scene causality, reveal cadence, relationships, voice, retention, ending.

### E. WORLD / PHILOSOPHY SOURCE
Материалы для философии и worldbuilding. Они не определяют автоматически драматургию и не заменяют IVDIVO canon.

---

## 4. HIGH-PRIORITY CRAFT CORPUS — CURRENT REGISTER

Ниже — уже идентифицированное ядро. Статусы намеренно консервативны: наличие файла не равно полному изучению.

| Source | Primary role | Current status |
|---|---|---|
| Aristotle — *Poetics* | unity of action, probability/necessity, reversal/recognition, plot evaluation | READ/EXTRACTION IN PROGRESS |
| John Truby — *The Anatomy of Story* | organic story architecture, desire, opposition, revelations, moral choice, scene weave | READ/EXTRACTION IN PROGRESS |
| John Truby — *The Anatomy of Genres* | genre promises, genre-specific beats, genre mixing | REGISTERED / READ PASS STARTED |
| Robert McKee — *Story* | value change, inciting incident, scene/act design, crisis/climax/resolution | READ/EXTRACTION IN PROGRESS |
| Robert McKee — specialist volumes when present | character/action/dialogue specialization | REGISTERED / PARTIAL EXTRACTION |
| John Yorke — *Into the Woods* | structural recursion, change, act logic, series/serial | REGISTERED / READ PASS STARTED |
| Will Storr — *The Science of Storytelling* | reader psychology, curiosity, control, salience, flawed self, status, empathy | READ/EXTRACTION IN PROGRESS |
| Lajos Egri — *The Art of Creative Writing* | character contradiction, motivation, emotional identification | READ/EXTRACTION IN PROGRESS |
| Alice LaPlante — *The Making of a Story* | literary craft, detail, scene, character, POV, revision, reading-as-writer | READ PASS STARTED |
| Janet Burroway et al. — *Writing Fiction* | narrative craft, scene, characterization, POV, prose technique | REGISTERED / READ PASS STARTED |
| Jack Hodgins — *A Passion for Narrative* | fiction process, narrative life, character/scene/voice | REGISTERED |
| Dwight V. Swain — *Techniques of the Selling Writer* | scene/sequel, motivation-reaction, causal flow | READ/EXTRACTION IN PROGRESS |
| Shawn Coyne — *The Story Grid* | developmental editing, genre obligations, scene evaluation | REGISTERED / READ PASS STARTED |
| K. M. Weiland — *Structuring Your Novel* | long-form structural diagnostics | REGISTERED / READ PASS STARTED |
| K. M. Weiland — character arc books/workbooks | Lie/Truth, Want/Need, arc families, plot-arc coupling | REGISTERED / PARTIAL EXTRACTION |
| Jessica Brody — *Save the Cat! Writes a Young Adult Novel* | YA hero, beat logic, YA story categories, series planning | READ/EXTRACTION IN PROGRESS |
| Christopher Vogler — *The Writer's Journey* | mythic/archetypal transformation as optional lens | REGISTERED / PARTIAL EXTRACTION |
| Joseph Campbell — *The Hero with a Thousand Faces* | comparative myth / archetypal source | REGISTERED |
| Ignasi Ribó — *Prose Fiction* | story/discourse, plot, narration, language, theme | READ PASS STARTED |
| Jordan Rosenfeld — *The Sound of Story* | voice, tone, syntax, lexicon, rhythm, prose sound | READ PASS STARTED |
| Michael Noll — *The Writer's Field Guide to the Craft of Fiction* | practical craft drills and scene/prose problem solving | REGISTERED |
| Anne Bernays & Pamela Painter — *What If?* | exercises for beginnings, character, POV, dialogue, plot, style, pacing | READ PASS STARTED |
| Anne Lamott — *Bird by Bird* | drafting process, perfectionism, character/plot/dialogue, revision mindset | READ PASS STARTED |
| Erin M. Pushman — *How to Read Like a Writer* | reverse engineering genre, structure, character, POV, scene, language | READ PASS STARTED |
| Michael Breault — *Narrative Design* | objective/progression/systemic narrative/agency | READ PASS STARTED |
| Edward James — *Science Fiction in the Twentieth Century* | SF history and genre literacy | READ PASS STARTED |
| James & Mendlesohn (eds.) — *The Cambridge Companion to Science Fiction* | SF critical frameworks, history, themes/subgenres | REGISTERED |
| Ursula K. Le Guin — essays / craft corpus present in library | voice, rhythm, world-making, SF/fantasy craft, reading aloud | REGISTERED / NEW |
| Edith Wharton — *The Writing of Fiction* | novel/short-story craft, character/situation | REGISTERED |
| Clayton Meeker Hamilton — *A Manual of the Art of Fiction* | classical fiction technique | REGISTERED |
| Clayton Meeker Hamilton — *Materials and Methods of Fiction* | classical fiction method | REGISTERED |
| William Archer — *Play-Making* | dramatic craftsmanship, preparation, tension, climax | REGISTERED |
| George Pierce Baker — *Dramatic Technique* | dramatic action, character, dialogue, audience | REGISTERED |
| Gustav Freytag — *Die Technik des Dramas* | historical dramatic structure model | REGISTERED |
| Georges Polti — *36 Dramatic Situations* | situation taxonomy / ideation aid | REGISTERED |
| Robert Louis Stevenson — *Essays in the Art of Writing* | sentence craft, rhythm, literary style | REGISTERED |
| Herbert Spencer — *The Philosophy of Style* | cognitive economy, sentence ordering, stylistic effect | REGISTERED |
| William Strunk — *The Elements of Style* | clarity/usage as limited auxiliary source | REGISTERED |
| Bob Mayer — *The Novel Writer's Toolkit* | practical novel production | REGISTERED |
| George Green & Lizzy Kremer — *Writing a Novel and Getting Published* | novel structure + publishing interface | REGISTERED |
| Dara Marks — *Inside Story* | transformational arc / thematic character change | REGISTERED |

This table is not the complete library. It is the current high-priority writing-craft register; the 171-file baseline and later uploads require continued ingestion.

---

## 5. FICTION REVERSE-ENGINEERING RULE

Для каждой художественной книги уровня `CORE / ENGINE / SPECIALIST` создаётся Source Passport и, для A-tier источников, scene/sequence map.

Минимум извлекается:

1. opening disturbance;
2. story promise;
3. central dramatic question;
4. protagonist external objective;
5. human/emotional problem;
6. opposition system;
7. stakes;
8. clock/pressure;
9. major relationship engine;
10. mystery/reveal architecture;
11. scene causality;
12. midpoint state change;
13. crisis choice;
14. climax action;
15. ending payoff;
16. sequel/series door;
17. POV/voice function;
18. pacing/retention mechanism;
19. transferable mechanism;
20. explicit `DO NOT COPY` surface elements.

---

## 6. STUDY OUTPUT IS NOT A SUMMARY

Для проекта мало написать «книга говорит о персонаже/сюжете».

Каждый useful finding должен иметь форму:

`SOURCE CLAIM / OBSERVED MECHANISM → WHY IT WORKS → WHEN TO USE → FAILURE MODE → IVDIVO OPERATIONAL TEST`

Пример уровня абстракции:

> Если осложнение рождается из разумного решения героя при неполной информации, оно обычно сильнее случайной катастрофы, потому что одновременно двигает plot и характеризует человека. Test: может ли следующий крупный поворот быть причинно выведен из решения героя, а не из авторского «вдруг»?

---

## 7. ANTI-IMITATION FIREWALL

Нельзя переносить из внешнего произведения:

- имена/образы персонажей;
- уникальную последовательность событий;
- узнаваемую систему мира;
- характерный голос автора;
- конкретные puzzles/twists;
- отличительные сцены;
- сеттинг с косметической заменой существительных.

Можно переносить абстрактный механизм после снятия surface layer.

---

## 8. APPLICATION TO PRODUCTION

До написания нового крупного текста соответствующий production room должен обратиться к уже `OPERATIONALIZED` знаниям.

Например:

- Story Architect → Aristotle / Truby / McKee / Yorke / Coyne;
- Scene Room → Swain / McKee / Rosenfeld / Burroway / LaPlante;
- Character Room → Egri / Storr / Corbett / Card / Stanislavski / Weiland;
- YA Room → Brody + youth psychology sources;
- Voice/Prose Room → Burroway / LaPlante / Rosenfeld / Le Guin / Stevenson;
- Genre Room → Truby Genres + genre-specialist sources + fiction reverse engineering;
- Red Team → cross-source contradictions + source-distance audit.

No room may claim that a source was used if its relevant mechanism has not been extracted or directly re-read for the task.

---

## 9. CURRENT EXECUTION PRIORITY

1. Finish integrity + duplicate audit for all new Aug-15 uploads.
2. Separate CRAFT / FICTION / THEORY / WORLD sources.
3. Finish full-pass of Tier A craft corpus.
4. Build `IVDIVO PROFESSIONAL FICTION CRAFT BODY OF KNOWLEDGE`.
5. Convert findings into production gates.
6. Re-audit Book 1 against the completed knowledge base before further cosmetic line editing.
7. Develop Book 2 only under the new story-first and evidence-backed craft system.

---

## 10. NO FALSE COMPLETION

This ledger deliberately refuses the label `100 BOOKS STUDIED` until the evidence exists.

The project may say:

- `100 likely full files identified` — if supported by audit;
- `N unique books registered` — after dedupe;
- `N books read-pass complete` — after actual read pass;
- `N books operationalized` — after mechanism integration.

It must never convert file count into knowledge count.
