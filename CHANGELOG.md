# CHANGELOG

Журнал изменений базы знаний GitHub.

## 2026-07-20

### Added

- `98_CONVERSATION_ARCHIVE/2026-07-20_main-goal-protocol-franchise.md` — архив текущего разговора: главная цель проекта, обязательный протокол, архивный протокол, коммерческая модель франшизы.
- `docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT.md` — рабочая модель франшизы: продукт, ведущие, клубы, образовательная/психологическая лицензия, цифровая платформа, мастер-франшиза.
- `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.2_APPROVED.md` — GitHub-копия утверждённого Drive-документа WORLD-002: пять вертикальных миров + орбитали параллельных миров.
- `MASTER_INDEX.md` — краткий корневой индекс актуальных GitHub-документов.
- `OPEN_QUESTIONS.md` — список открытых вопросов, выявленных при синхронизации.

### Changed

- `PROJECT_CORE_CONTEXT.md` синхронизирован с Google Drive v1.6: добавлены DEC-015, DEC-016, DEC-017, DEC-018; старая восьмимировая вертикаль заменена на пять вертикальных миров + орбитали.
- `DECISIONS.md` обновлён: DEC-003 помечен как SUPERSEDED BY DEC-015; добавлены DEC-015–DEC-018.
- `DOCUMENT_REGISTRY.md` обновлён: добавлены WORLD-002, FRAN-001, ARCH-20260720-05, MASTER-002, OPENQ-001; WORLD-001 помечен как OLD MODEL / REVIEW REQUIRED.
- `MIGRATION_INDEX.md` обновлён: отмечен перенос WORLD-002, FRAN-001 и архива разговора; зафиксирована необходимость полной синхронизации Drive v1.6 → GitHub.
- `docs/README.md` обновлён ссылками на WORLD-002, FRAN-001 и архив разговора.

### Conflicts / Open

- Google Drive `PROJECT_CORE_CONTEXT_2026` уже v1.6, а GitHub-main до этой ветки содержал v1.1 с устаревшей восьмимировой вертикалью.
- В Google Drive и GitHub сохраняется историческая коллизия нумерации DEC; текущая ветка явно фиксирует источник решений, но полная перенумерация остаётся отдельной задачей.
- `MASTER_INDEX.md` и `OPEN_QUESTIONS.md` отсутствовали в main, хотя упомянуты в архивном протоколе; созданы в этой ветке.

## 2026-07-12 (продолжение)

### Added
- `references/MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT.md` (COMP-004) — методология сравнительного аудита (30 критериев) + реальные находки по Etherfields, Oath, Kingdom Death: Monster, Gloomhaven, Pandemic Legacy, Too Many Bones.
- `docs/14_TESTING_AND_BALANCE/PLAYTEST_PROTOCOL_v0.1_DRAFT.md` (TEST-001) — §7: качественный слой философского/эмоционального восприятия, дополняет количественные коридоры §2.
- `templates/practical_templates_v0.1_draft.md` — 10 практических форм.
- `31_IDEAS/archive_pre_pyramid_2026-07-12/` — 6 документов, созданных до выяснения актуальной топологии.

### Changed
- `DOCUMENT_REGISTRY.md` — добавлен COMP-004, обновлена запись TEST-001, зафиксирован архивный раздел.

## 2026-07-12

### Added

- `references/SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT.md` (COMP-003) — базовая практика, различение Свет-вещества и Дух-вещества, Магнит Отца-Матери, пять ярусов пирамиды.
- В `docs/03_MECHANICS/GAME_MECHANICS_v0.1_DRAFT.md` (MECH-001) — раздел P49.3: вертикальный переход как сужающаяся пирамида колец (PROPOSED), отвечает на открытый вопрос P49.1.
- В `DECISIONS.md` — DEC-012 (PROPOSED): пирамида с орбиталями как амендмент к DEC-003.

### Changed

- `DOCUMENT_REGISTRY.md` — v1.1: добавлена строка COMP-003, обновлена запись MECH-001.

### Open

- Согласование пятиярусной пирамиды с восемью мирами DEC-003.
- Коллективная vs индивидуальная вершина пирамиды.
- Завершение описания практики Магнита Отца-Матери.
- Кумара — одна фигура или несколько.

## 2026-07-11

### Added

- `docs/13_AI_RESULTS/PROMPT_LIBRARY_64_v0.2_DRAFT.md` — библиотека 64 промптов.
- `docs/00_PROJECT_CORE/MANDATORY_WORK_PROTOCOL_v1.0_ACTIVE.md` — частичный перенос обязательного протокола работы с проектом.
- `docs/01_RESEARCH/MARKET_RESEARCH_2026_v0.1_DRAFT.md` (RES-001).
- `docs/02_GAME_CONCEPT/GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT.md` (CONC-001).
- `docs/04_CARDS_AND_COMPONENTS/PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT.md` (CARD-001).
- `docs/14_TESTING_AND_BALANCE/PLAYTEST_PROTOCOL_v0.1_DRAFT.md` (TEST-001).
- `docs/10_KICKSTARTER/KICKSTARTER_PLAN_v0.1_DRAFT.md` (KS-001).
- `docs/11_DIGITAL_PRODUCT/DIGITAL_COMPANION_v0.1_DRAFT.md` (DIG-001).
- `references/SHMAKOV_ASCENT_PATH_v0.1_DRAFT.md` (COMP-002).

### Changed

- `MIGRATION_INDEX.md` — обновлены статусы библиотеки промптов и обязательного протокола.
- `DOCUMENT_REGISTRY.md` — v1.2: шесть новых записей, пробелы Kickstarter/цифровая версия закрыты.

## 2026-07-08

### Added

- Инициализирован репозиторий `IVDIVO_GAME_MASTER`.
- Создан `README.md`.
- Создан `PROJECT_CORE_CONTEXT.md` как сжатая GitHub-копия главного контекста проекта.
- Создан `DECISIONS.md`.
- Начата миграция документов из Google Drive.

### Migration notes

- Google Drive остаётся источником полных оригиналов до завершения переноса.
- Все перенесённые документы должны сохранять ссылку на исходный Drive-документ.
- Документы со статусом APPROVED не переписываются молча; при изменении создаётся новая версия.
