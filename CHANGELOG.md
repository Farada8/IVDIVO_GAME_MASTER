# CHANGELOG

Журнал изменений базы знаний GitHub.

## 2026-07-12

### Added

- `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.2_APPROVED.md` (WORLD-002) — утверждённая архитектура пяти вертикальных миров и орбиталей параллельных миров.
- `DEC-015` — Физический, Тонкий, Метагалактический, Огненный и Синтезный миры образуют вертикаль; Ад, Рай, Аидия, Демонский и Омарный миры относятся к орбиталям.
- `docs/03_MECHANICS/ASCENSION_UNLOCK_SYSTEM_v0.1_APPROVED.md` (MECH-004) — утверждённая система прогрессии через физическое раскрытие новых колод, полей, Инструментов, условий и функций старых карт.
- `docs/04_CARDS_AND_COMPONENTS/ASCENSION_UNLOCK_MODULES_v0.1_APPROVED.md` (CARD-002) — типы и гипотетический состав пакетов открытий.
- `docs/14_TESTING_AND_BALANCE/ASCENSION_REWARD_PLAYTEST_v0.1_DRAFT.md` (TEST-003) — тест различия между числовым усилением и ощущением восхождения.
- `docs/13_AI_RESULTS/PROMPT_EXECUTION_MASTER_100_v0.2_DRAFT.md` (AI-100) — мастер-реестр 100 производственных промтов, обновлённый после решения канона.
- `docs/13_AI_RESULTS/blocks/BLOCK_01_PROJECT_AND_GITHUB_v0.1_DRAFT.md` — архитектура проекта, источники истины, гейты и дорожная карта.
- `docs/13_AI_RESULTS/blocks/BLOCK_02_BASE_GAME_v0.1_DRAFT.md` — scope, core loop, роли, экономика, кампания и состав базовой коробки.
- `docs/13_AI_RESULTS/blocks/BLOCK_03_WORLD_EXPANSIONS_v0.2_DRAFT.md` — пять вертикальных миров и орбитали как основа продуктовых дополнений.
- `docs/13_AI_RESULTS/blocks/BLOCK_04_STORY_AND_CAMPAIGNS_v0.1_DRAFT.md` — сюжетная грамматика, сценарии, ветвления, диалоги и финалы.
- `docs/13_AI_RESULTS/blocks/BLOCK_05_CHARACTERS_AND_FACTIONS_v0.1_DRAFT.md` — герои, антигерой, союзник, фракции и отношения.
- `docs/13_AI_RESULTS/blocks/BLOCK_06_CARDS_TOOLS_ECONOMY_v0.1_DRAFT.md` — карты, Инструменты, законы, условия, угрозы и награды.
- `docs/13_AI_RESULTS/blocks/BLOCK_07_BOARDS_COMPONENTS_UI_v0.1_DRAFT.md` — поля, кольца, портал, планшеты, Убежище и PnP.
- `docs/13_AI_RESULTS/blocks/BLOCK_08_RULES_BALANCE_TESTING_v0.1_DRAFT.md` — правила, обучение, доступность, соло и тестовая инфраструктура.
- `docs/13_AI_RESULTS/blocks/BLOCK_09_EMOTION_RISK_SOCIAL_v0.1_DRAFT.md` — эмоции, азарт, победы, поражения и разговоры за столом.
- `docs/13_AI_RESULTS/blocks/BLOCK_10_VISUAL_PRODUCTION_MARKET_v0.1_DRAFT.md` — визуал, производство, Kickstarter, линейка и цифровой продукт.
- `docs/16_EXPANSIONS/BASE_GAME_AND_WORLD_EXPANSION_STRATEGY_v0.1_REVIEW.md` (EXP-001) — базовая коробка как законченная игра и миры как модульные дополнения.
- Пакет из десяти форм в `docs/00_PROJECT_CORE/templates/`: механика, мир, дополнение, персонаж, фракция, карта, сценарий, плейтест, art brief и production spec.

### Changed

- `PROJECT_CORE_CONTEXT.md` обновлён до v1.5: старая восьмимировая схема заменена пятью вертикальными мирами и орбиталями.
- `DECISIONS.md`: DEC-003 переведён в `SUPERSEDED BY DEC-015`; добавлен DEC-015.
- `DOCUMENT_REGISTRY.md` обновлён до v1.6: WORLD-002 стал активным источником архитектуры; старые документы помечены для проверки.
- `PROMPT_EXECUTION_MASTER_100` обновлён до v0.2: канонические блокировки сняты, оставлены продуктовые и тестовые ограничения.
- `BLOCK_03_WORLD_EXPANSIONS` обновлён до v0.2 и привязан к DEC-015/WORLD-002.
- `EXP-001` теперь разделяет утверждённую космологию и всё ещё не утверждённую продуктовую последовательность дополнений.
- Создана ветка `agent/execute-100-game-workstreams` для системного выполнения библиотеки из 100 промтов.

### Superseded

- DEC-003 — восемь миров как центральная вертикальная архитектура.
- `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.1_DRAFT.md` — исторический DRAFT старой модели.
- `docs/13_AI_RESULTS/PROMPT_EXECUTION_MASTER_100_v0.1_DRAFT.md` — заменён v0.2.
- `docs/13_AI_RESULTS/blocks/BLOCK_03_WORLD_EXPANSIONS_v0.1_DRAFT.md` — заменён v0.2.

### Notes

- Каноническая коллизия миров разрешена.
- Точная карта привязки орбиталей, их количество, периоды и пространственная реализация остаются TO-VERIFY.
- Числа, стоимость, UX, эмоциональный эффект и баланс требуют бумажных и слепых тестов.
- Стратегия «миры как дополнения» сохраняет статус REVIEW; DEC-015 утверждает архитектуру, но не график выпуска.

## 2026-07-11

### Added

- `docs/13_AI_RESULTS/PROMPT_LIBRARY_64_v0.2_DRAFT.md` — библиотека 64 промптов: реконструкция и развитие v0.1.
- `docs/00_PROJECT_CORE/MANDATORY_WORK_PROTOCOL_v1.0_ACTIVE.md` — частичный перенос обязательного протокола работы.
- `docs/01_RESEARCH/MARKET_RESEARCH_2026_v0.1_DRAFT.md` (RES-001) — рыночное исследование.
- `docs/02_GAME_CONCEPT/GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT.md` (CONC-001) — одностраничник концепта и публичный словарь IP.
- `docs/04_CARDS_AND_COMPONENTS/PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT.md` (CARD-001) — карточный состав первого прототипа.
- `docs/14_TESTING_AND_BALANCE/PLAYTEST_PROTOCOL_v0.1_DRAFT.md` (TEST-001) — протокол трёх волн тестирования.
- `docs/10_KICKSTARTER/KICKSTARTER_PLAN_v0.1_DRAFT.md` (KS-001) — гейты запуска и скелет pledge-структуры.
- `docs/11_DIGITAL_PRODUCT/DIGITAL_COMPANION_v0.1_DRAFT.md` (DIG-001) — MVP-компаньон.
- `references/SHMAKOV_ASCENT_PATH_v0.1_DRAFT.md` (COMP-002) — внутренний сравнительный источник.
- `docs/03_MECHANICS/WORLD_ECONOMY_SYSTEM_v0.1_APPROVED.md` (MECH-002) — системная экономика миров.
- `docs/03_MECHANICS/PORTAL_CONJUNCTION_SYSTEM_v0.1_APPROVED.md` (MECH-003) — неблокирующая конъюнкция.
- `docs/14_TESTING_AND_BALANCE/PORTAL_GATE_PLAYTEST_v0.1_DRAFT.md` (TEST-002) — тест шлюза портала.

### Changed

- `MIGRATION_INDEX.md` — обновлены статусы миграции.
- `DOCUMENT_REGISTRY.md` — добавлены MECH-003 и TEST-002.
- `DECISIONS.md` — добавлены DEC-012 и DEC-013.
- `PROJECT_CORE_CONTEXT.md` — добавлены экономическая формула и принцип неблокирующей конъюнкции.

### Superseded

- `GAME_MECHANICS_v0.1_DRAFT`, P49.1 «центр = зал ожидания» — заменён DEC-013 и MECH-003.

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
