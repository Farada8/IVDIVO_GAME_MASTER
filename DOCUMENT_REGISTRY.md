# DOCUMENT_REGISTRY

Версия: v1.12
Дата создания: 2026-07-09
Дата обновления: 2026-08-15 (добавлены CRAFT-001 и CRAFT-002 — Writing Library Study Ledger + Professional Fiction Craft Body of Knowledge)
Код документа: REG-002
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/`. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория (зафиксирован в CHANGELOG.md, запись 2026-07-09).

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем (единственный, кто может присвоить)
- **DEPRECATED** — заменено более новой версией, хранится для истории

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · карты · компоненты · нарратив · production · craft · research

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE (корневой документ) | v1.1 | бизнес, мир, канон | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3, P49.4 добавлены 2026-07-12) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MECH-002 / CARD-SYSTEM-001 | REALITY_FRACTURES_SYSTEM_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика, карты, компоненты, сценарии | GCORE-001, MECH-001 | DEC-005, DEC-006, DEC-015, DEC-016, DEC-017, TEST-001 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT / MIGRATION-COMPLETE (2026-07-22) | v0.1 | франшиза, бизнес | CORE-001 | PROD-001, VBC-001, COMM-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12) | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003, MECH-002 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| NARR-003 | NARRATIVE_DESIGN_FRAMEWORKS_v0.1_DRAFT | references/ | DRAFT | v0.1 | нарратив (методология) | GCORE-001 | ENT-001 |
| NARR-004 | IVDIVO_PROFESSIONAL_WRITING_STUDIO_v2.0_DRAFT | docs/00_PROJECT_CORE/ | DRAFT | v2.0 | нарратив, production | CORE-001, IVDIVO_WRITING_PRODUCTION_CANON | NARR-003, STORY-001, NARR-002 |
| NARR-005 | IVDIVO_PROFESSIONAL_WRITING_STUDIO_v3.0_DRAFT | docs/00_PROJECT_CORE/ | DRAFT | v3.0 | нарратив, production, социология, психология, worldbuilding, market | CORE-001, IVDIVO_WRITING_PRODUCTION_CANON | NARR-004, NARR-003, STORY-001, NARR-002, PSY-001, FRAN-001 |
| NARR-006 | IVDIVO_SERIES_EMBODIMENT_DIMENSIONAL_WORLDS_ANGEL_GAIA_CYCLE_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | нарратив, мир, персонажи, production | CORE-001, IVDIVO_WRITING_PRODUCTION_CANON | NARR-005, STORY-001, NARR-002, WORLD-001, ENT-001 |
| NARR-007 | IVDIVO_THREE_LINE_SERIES_ARCHITECTURE_ORBITAL_YOUTH_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | нарратив, мир, персонажи, production | NARR-006, CORE-001, IVDIVO_WRITING_PRODUCTION_CANON | NARR-005, STORY-001, NARR-002, WORLD-001, ENT-001 |
| NARR-008 | IVDIVO_EARTH_MATRIX_SMITH_DAUGHTER_YOUTH_SAGA_BOOK2_MASTER_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | нарратив, мир, персонажи, production | NARR-006, NARR-007, IVDIVO_WRITING_PRODUCTION_CANON | NARR-009, NARR-010, NARR-011, NARR-012, NARR-013, NARR-005, STORY-001, WORLD-001, ENT-001 |
| NARR-009 | IVDIVO_70_BOOK_YOUTH_STORY_ENGINE_MULTILINE_SAGA_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | нарратив, production, франшиза, персонажи | NARR-008, NARR-007, NARR-006, IVDIVO_WRITING_PRODUCTION_CANON | NARR-010, NARR-011, NARR-012, NARR-013, NARR-005, STORY-001, PSY-001, FRAN-001 |
| NARR-010 | IVDIVO_BOOK2_DEVELOPMENT_PACK_CHARACTER_MYSTERY_BACKGROUND_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT / ACTIVE PRODUCTION | v0.1 | нарратив, персонажи, production, mystery | NARR-008, NARR-009, IVDIVO_WRITING_PRODUCTION_CANON | NARR-011, NARR-012, NARR-013, NARR-007, NARR-005, STORY-001, PSY-001, WORLD-001 |
| NARR-011 | IVDIVO_BOOK2_VOICE_TEST_01_BREAKFAST_WITH_SMITH_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT PROTOTYPE | v0.1 | нарратив, персонажи, prose calibration | NARR-008, NARR-010, IVDIVO_WRITING_PRODUCTION_CANON | NARR-009, NARR-012, NARR-013, NARR-007, NARR-005 |
| NARR-012 | IVDIVO_YOUTH_EVERYDAY_LIFE_RECOGNITION_ENGINE_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT / ACTIVE PRODUCTION RULE | v0.1 | нарратив, youth, production, empathy | NARR-008, NARR-009, NARR-010, IVDIVO_WRITING_PRODUCTION_CANON | NARR-011, NARR-013, NARR-007, PSY-001, STORY-001 |
| NARR-013 | IVDIVO_2035_SYNCHRONIZED_THREE_ZONE_TECH_ASYMMETRY_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT / ACTIVE WORLD RULE | v0.1 | нарратив, мир, технологии, экономика, youth | NARR-007, NARR-008, NARR-009, NARR-010, IVDIVO_WRITING_PRODUCTION_CANON | NARR-012, NARR-011, WORLD-001, PSY-001, FRAN-001 |
| CRAFT-001 | IVDIVO_WRITING_LIBRARY_STUDY_LEDGER_v0.1_DRAFT | docs/01_RESEARCH/WRITING_CRAFT/ | DRAFT EXECUTION / FOUNDER DIRECTIVE RECORDED | v0.1 | craft, research, production | IVDIVO_WRITING_PRODUCTION_CANON, NARR-005 | CRAFT-002, NARR-003, NARR-009 |
| CRAFT-002 | IVDIVO_PROFESSIONAL_FICTION_CRAFT_BODY_OF_KNOWLEDGE_v0.1_DRAFT | docs/01_RESEARCH/WRITING_CRAFT/ | DRAFT / EVIDENCE-BACKED INITIAL SYNTHESIS | v0.1 | craft, research, нарратив, production | CRAFT-001, IVDIVO_WRITING_PRODUCTION_CANON | NARR-005, NARR-003, NARR-009, NARR-010, NARR-012 |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.12 | техническое | — | все документы выше |

---

## Обновление 2026-08-15 — CRAFT-001 / CRAFT-002

`docs/01_RESEARCH/WRITING_CRAFT/IVDIVO_WRITING_LIBRARY_STUDY_LEDGER_v0.1_DRAFT.md` фиксирует прямое указание основателя: каждая загруженная книга должна быть реально изучена и её знания должны быть внесены в проект. Введена строгая шкала `REGISTERED → INTEGRITY VERIFIED → READ PASS 1 → STRUCTURE/PASSPORT → MECHANISM EXTRACTION → CROSS-SOURCE SYNTHESIS → OPERATIONALIZED`; запрещено приравнивать наличие файла/оглавления/фрагмента к изучению. Baseline library audit: 171 файл, 100 `LIKELY_FULL`, 40 explicit fragments, 12 collections, 2 scanned/text-unavailable; новые загрузки после baseline требуют дальнейшего ingestion. Статус DRAFT execution document; сама Founder Directive является прямым указанием владельца.

`docs/01_RESEARCH/WRITING_CRAFT/IVDIVO_PROFESSIONAL_FICTION_CRAFT_BODY_OF_KNOWLEDGE_v0.1_DRAFT.md` создаёт первый единый evidence-backed слой профессионального писательского знания: main story, plot causality, scene engine, character, relationships, dialogue/subtext, POV, reader psychology, YA, genre, SF/worldbuilding, prose/voice/sound, show/tell, mystery, suspense, endings и developmental editing. Каждый принцип должен быть связан с source support, механизмом и operational test. Документ не заявляет, что весь ~100-book corpus уже прочитан; completion truth хранится в CRAFT-001.

## Обновление 2026-08-15 — NARR-013

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_2035_SYNCHRONIZED_THREE_ZONE_TECH_ASYMMETRY_v0.1_DRAFT.md` фиксирует рабочую синхронизацию основных молодёжных линий в 2035: Earth Youth, Orbital Youth и Confederation Human Training Youth существуют одновременно, а не в разных исторических эпохах. Разница технологий объясняется не временем, а неравномерной диффузией Contact-технологий, миграцией капитала и талантов, новой инфраструктурой Orbit, ограниченным доступом к Confederation training systems и политико-экономическим интересом части orbital elites сохранять технологическую асимметрию с Землёй. Земля продолжает развиваться, но новые технологии появляются там выборочно — сначала в premium/institutional секторах. Зафиксирован производственный принцип: каждая технологическая разница должна создавать узнаваемую человеческую/подростковую проблему, а не служить декорацией. Статус DRAFT / ACTIVE WORLD RULE; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-012

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_YOUTH_EVERYDAY_LIFE_RECOGNITION_ENGINE_v0.1_DRAFT.md` фиксирует обязательный Recognition-First принцип молодёжной саги: подросток должен узнавать себя в героях до раскрытия космологии. Введены everyday arenas (школа, подработка, спортзал, площадка/двор, дорога домой, дом/кухня, кафе/магазин, вечеринка), micro-pain empathy rule, Fantastic Amplification Rule, Scene Acceptance Test, recognition rhythm, no-fake-youth rules и обязательная daily-life braid для Core Six Book 2. Перед 40-главным outline необходимо определить их школу/район, работу, спорт, транспорт, деньги, место встреч, orbital opportunity и обычное событие недели, которое существовало до supernatural incident. Статус DRAFT / ACTIVE PRODUCTION RULE; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-011

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_BOOK2_VOICE_TEST_01_BREAKFAST_WITH_SMITH_v0.1_DRAFT.md` — первый prose/voice prototype активной разработки Book 2. Сцена тестирует 16–17-летнюю дочь Смита (временное имя Mara Keene), текущую публичную личность Смита Daniel Keene, живую мать Elise Ward и подругу Sloane Mercer как provisional names only. Сцена сознательно остаётся бытовой: завтрак, вечеринка, контроль отца, предложение матери переехать в ранний orbital habitat, Contact-news как фон. Вводится первая минимальная, отрицаемая аномалия — задержка/искажение отражения Смита — и его слишком быстрая профессиональная реакция на возможное visual disturbance. Никакого объяснения Matrix/Hierarchy/Lucifer. Статус DRAFT PROTOTYPE; не manuscript и не канон.

## Обновление 2026-08-15 — NARR-010

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_BOOK2_DEVELOPMENT_PACK_CHARACTER_MYSTERY_BACKGROUND_v0.1_DRAFT.md` запускает активную разработку Book 2 после Master Architecture. В пакете созданы Character Lab для шести молодёжных функций, взрослый контур, relationship web, 24-ступенчатый Mystery Evidence Ledger, ограничения и возможности Смита именно для Book 2, Earth-2033 Contact/Orbit background braid, разные эмоциональные значения Орбиты для персонажей, chapter-braid gate, 12 prototype voice-test scenes и Red Team risks. Следующие проходы: voice tests/names, выбор конкретной школьной/городской арены, механизм mass-state incident, точная механика normalization, 40 chapter cards, расширение Human Problem Bank и Earth seed bank. Статус DRAFT / ACTIVE PRODUCTION; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-009

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_70_BOOK_YOUTH_STORY_ENGINE_MULTILINE_SAGA_v0.1_DRAFT.md` фиксирует производственный принцип долгой саги: ориентир около 70 самостоятельных человеческих романов на каждую большую линию Earth / Orbit / Frontier, но без padding и без превращения lore в сюжет. Введены Human-Problem-First gate, обязательная Story Card, 7 development waves, no-repetition matrix, relationship graph как межлинейная инфраструктура, source-learning protocol для загруженных книг и стартовые 12 book seeds для каждой из трёх линий. Статус DRAFT; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-008

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_EARTH_MATRIX_SMITH_DAUGHTER_YOUTH_SAGA_BOOK2_MASTER_v0.1_DRAFT.md` фиксирует Founder-driven планетарную линию Earth/Matrix/Smith и запускает Book 2 вокруг 16–17-летней дочери Смита. Зафиксированы: YA social ensemble, оригинальная Constantine-function без копирования персонажа, case-of-book с подростковой «нормализацией», исторический mystery Смита, body-transfer, false-light / искусственная психическая субстанция любви, ontological camouflage, иерархический ликвидатор, пробуждения 15–18, типология необычных субъектов, сильные Посвящённые/Иерархи, футуристический Кутхуми, поздняя гипотеза Lucifer, тёмные внешние воплощения, Смит как двойной агент в школе Синтеза, пробуждение Смита, кармическая разгрузка/просветление Матрицы, ранний orbital exodus из-за кризиса психической безопасности, Contact/Confederation background braid, временная лестница до ~2200 и дальние Frontier/galactic limits. Статус DRAFT; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-007

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_THREE_LINE_SERIES_ARCHITECTURE_ORBITAL_YOUTH_v0.1_DRAFT.md` фиксирует трёхконтурную архитектуру будущих книг: (A) Embodiment/Youth Cohort frontier, (B) Earth/Ouroboros/Custodian detective-horror line, (C) Orbital Youth — coming-of-age/romance/social ensemble в Contact-accelerated орбитальном городе. В документе закреплены continuity lock для 2032, технологический быт на основе future-tech palette (Personal AI, Second Brain, Digital Twin, Spatial Computing, Neurorights, Synthetic Persons, AI-run enterprises, post-scarcity, longevity, programmable materials), точки пересечения трёх линий, character rotation и development ledgers. Статус DRAFT; не канон до Founder approval.

## Обновление 2026-08-15 — NARR-006

`docs/07_CAMPAIGNS_AND_STORIES/IVDIVO_SERIES_EMBODIMENT_DIMENSIONAL_WORLDS_ANGEL_GAIA_CYCLE_v0.1_DRAFT.md` фиксирует Founder-driven развитие серии после `LESSON ZERO`: embodiment и специализированные тела, влияние материи носителя на личность, кислотные/океанические/звёздные/сверхплотные/квантово-мерностные тела, distributed subjectivity, plasmoid/stellar life, dimensional inversion through sleep, ontological spectrum, fractal universes, zero-distance/co-local layer, ancient Traveler/Angel/Gaia historical cycle, Earth-born descendants, character rotation, Books 2–6 macro-architecture и параллельную Earth/Ouroboros thriller line с оригинальным Custodian mechanism. Статус DRAFT; не канон до Founder approval. Book 1 continuity explicitly locked.

## Обновление 2026-08-14 — NARR-005

`docs/00_PROJECT_CORE/IVDIVO_PROFESSIONAL_WRITING_STUDIO_v3.0_DRAFT.md` расширяет v2.0 до 64-ролевой operating system. Добавлены самостоятельные вертикали социологии, социальной антропологии, этнографии, политики, экономики, права, безопасности, криминологии, переговоров, когнитивистики, нейронауки, AI/robotics/synthetic life, переноса сознания, системной инженерии, технологической диффузии, биологии/xenophysiology, лингвистики, семиотики, педагогики, этики, онтологии ИВДИВО, media sociology, book/series production, screen/streaming production, line production и consumer/market/franchise/transmedia analysis. Зафиксированы три уровня подключения специалистов, Scene Routing Card, BLOCKER/MAJOR/WATCH/NOTE, Conflict Board, 12 specialist ledgers и полный production pipeline. Статус DRAFT; `IVDIVO_WRITING_PRODUCTION_CANON.md` остаётся вышестоящим стандартом.

## Обновление 2026-08-14 — NARR-004

`docs/00_PROJECT_CORE/IVDIVO_PROFESSIONAL_WRITING_STUDIO_v2.0_DRAFT.md` расширяет писательскую студию до исполняемой системы из 37 специализированных ролей. Для каждой роли определены линза, защищаемые активы, границы полномочий, критерий эскалации и acceptance test. Документ также фиксирует voice engines, Anti-GPT prose lock и Full-Studio gate. Статус DRAFT; канонический `IVDIVO_WRITING_PRODUCTION_CANON.md` остаётся вышестоящим производственным стандартом.

## Обновление 2026-07-22 — FRAN-001

`docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT.md` полностью синхронизирован с загруженным исходником `Коммерческая модель франшизы.txt`. Удалён статус частичной миграции. Документ остаётся DRAFT; финансовые параметры и юридическая конструкция требуют отдельной проверки.

## Обновление 2026-07-22 — MECH-002

`docs/03_MECHANICS/REALITY_FRACTURES_SYSTEM_v0.1_DRAFT.md` добавляет полный рабочий набор: 36 Разломов, 60 Проявлений, 50 Искажений, 36 Корней. Статус DRAFT. Числовые параметры, ресурсы и эффекты требуют тестирования.

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии. Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном.

## Протокол для новых документов

Перед созданием любого документа:
1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку "Связанные" / "Родитель".
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме.
5. Присвоить код.
6. После публикации — обновить этот реестр.

Статус APPROVED никогда не присваивается ассистентом.