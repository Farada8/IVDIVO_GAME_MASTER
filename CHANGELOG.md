# CHANGELOG

Журнал изменений базы знаний GitHub.

## 2026-07-12

### Added

- `docs/03_MECHANICS/ASCENSION_UNLOCK_SYSTEM_v0.1_APPROVED.md` (MECH-004) — утверждённая система прогрессии через физическое раскрытие новых колод, полей, Инструментов, условий и функций старых карт.
- `docs/04_CARDS_AND_COMPONENTS/ASCENSION_UNLOCK_MODULES_v0.1_APPROVED.md` (CARD-002) — типы и гипотетический состав пакетов открытий.
- `docs/14_TESTING_AND_BALANCE/ASCENSION_REWARD_PLAYTEST_v0.1_DRAFT.md` (TEST-003) — тест различия между числовым усилением и ощущением восхождения.
- `docs/13_AI_RESULTS/PROMPT_EXECUTION_MASTER_100_v0.1_DRAFT.md` (AI-100) — мастер-реестр выполнения 100 производственных промтов.
- `docs/13_AI_RESULTS/blocks/BLOCK_01_PROJECT_AND_GITHUB_v0.1_DRAFT.md` — архитектура проекта, источники истины, гейты и дорожная карта.
- `docs/13_AI_RESULTS/blocks/BLOCK_02_BASE_GAME_v0.1_DRAFT.md` — scope, core loop, роли, экономика, кампания и состав базовой коробки.
- `docs/13_AI_RESULTS/blocks/BLOCK_03_WORLD_EXPANSIONS_v0.1_DRAFT.md` — вертикальные уровни и параллельные миры как дополнения.
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

- `PROJECT_CORE_CONTEXT.md` обновлён до v1.4: добавлена прогрессия через открытия и восхождение.
- `DECISIONS.md` дополнен DEC-014.
- Создана ветка `agent/execute-100-game-workstreams` для системного выполнения библиотеки из 100 промтов.

### Notes

- Блоки 1–100 являются INITIAL DRAFT, а не доказанным финальным дизайном.
- Числа, стоимость, UX, эмоциональный эффект и баланс требуют бумажных и слепых тестов.
- Стратегия «миры как дополнения» сохраняет статус REVIEW / FOUNDER DIRECTION до явного утверждения.

## 2026-07-11

### Added

- `docs/13_AI_RESULTS/PROMPT_LIBRARY_64_v0.2_DRAFT.md` — библиотека 64 промптов: реконструкция и развитие v0.1 (8 блоков P01–P64, владельцы блоков, экспертные гейты, правила исполнения 0.1–0.7, статусы исполнения блоков, маршрутизация ROADMAP → промпты). Оригинал v0.1 (.docx) ожидает переноса и diff.
- `docs/00_PROJECT_CORE/MANDATORY_WORK_PROTOCOL_v1.0_ACTIVE.md` — частичный перенос Обязательного протокола работы с проектом (ядро по DEC-008; полный текст оригинала ожидает выгрузки из ZIP/Drive).
- `docs/01_RESEARCH/MARKET_RESEARCH_2026_v0.1_DRAFT.md` (RES-001) — рыночное исследование: входной материал основателя (BGG-топ, направления 2026–2030, параметры первой коробки, антирекомендации, оценка), дельта-анализ с ядром, предложение DEC-009.
- `docs/02_GAME_CONCEPT/GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT.md` (CONC-001) — одностраничник концепта и публичный словарь IP.
- `docs/04_CARDS_AND_COMPONENTS/PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT.md` (CARD-001) — полный карточный состав прототипа «2 Диска + 1 Вихрь» (~100 карт, PnP-план).
- `docs/14_TESTING_AND_BALANCE/PLAYTEST_PROTOCOL_v0.1_DRAFT.md` (TEST-001) — протокол трёх волн тестирования, метрики и коридоры, гейт ≥40 слепых партий.
- `docs/10_KICKSTARTER/KICKSTARTER_PLAN_v0.1_DRAFT.md` (KS-001) — гейты запуска, скелет pledge-структуры, вопрос платформы.
- `docs/11_DIGITAL_PRODUCT/DIGITAL_COMPANION_v0.1_DRAFT.md` (DIG-001) — MVP-компаньон (3 функции), этапность, принцип необязательности.
- `references/SHMAKOV_ASCENT_PATH_v0.1_DRAFT.md` (COMP-002) — источник «путь восхождения духа» (внутренний контур): резонанс с механикой Разрыв/Преобразование, 4 варианта игровой абстракции, файрвол терминов, предложение DEC-010. По запросу основателя.
- `docs/03_MECHANICS/WORLD_ECONOMY_SYSTEM_v0.1_APPROVED.md` (MECH-002) — утверждённая системная экономика миров: материальные, Тонкие, Духовные, Огненные и Синтезные ценности; стяжание; экономика антигероев; капиталы персонажей и фракций; обязательный экономический паспорт каждого мира.
- `docs/03_MECHANICS/PORTAL_CONJUNCTION_SYSTEM_v0.1_APPROVED.md` (MECH-003) — утверждённая замена бинарного зала ожидания: переход из центра доступен сразу, а конъюнкция задаёт цену, риск, бонус и последствия; уточнены Накал, роли и Великая Конъюнкция.
- `docs/14_TESTING_AND_BALANCE/PORTAL_GATE_PLAYTEST_v0.1_DRAFT.md` (TEST-002) — обязательный сравнительный бумажный тест трёх вариантов шлюза портала с метриками простоя, расхода Накала и альфа-давления.

### Changed

- `MIGRATION_INDEX.md` — обновлены статусы библиотеки промптов и обязательного протокола.
- `DOCUMENT_REGISTRY.md` — v1.3: добавлены MECH-003 и TEST-002; P49.1 MECH-001 отмечен как SUPERSEDED.
- `DECISIONS.md` — добавлен DEC-012: экономика является обязательным системным слоем вселенной.
- `DECISIONS.md` — добавлен DEC-013: конъюнкция определяет цену и риск, но не блокирует обязательное восхождение.
- `PROJECT_CORE_CONTEXT.md` — v1.3: добавлены утверждённая экономическая формула и принцип неблокирующей конъюнкции; ранняя восьмимировая схема отмечена как коллизия, требующая отдельного решения основателя.

### Superseded

- `GAME_MECHANICS_v0.1_DRAFT`, P49.1 «центр = зал ожидания» — заменён DEC-013 и MECH-003. Вращающиеся кольца и спицы остаются на тесте; бинарный запрет перехода отменён.

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
