# DOCUMENT_REGISTRY

Версия: v2.0-cleanup  
Дата обновления: 2026-07-22  
Код документа: REG-002  
Тип: [TECHNICAL] [ACTIVE REGISTRY]

## Назначение

Единый реестр активных и устаревших документов GitHub-репозитория. После cleanup этот файл должен отражать реальное состояние проекта, а не старую миграционную структуру.

## Легенда статусов

- **ACTIVE** — действующий управляющий документ.
- **APPROVED** — утверждено основателем.
- **FOUNDER-DECISION** — прямое решение основателя, зафиксировано в DECISIONS.
- **FOUNDER-INPUT** — прямой ввод основателя, ещё требует механики / баланса.
- **DRAFT** — рабочий документ, не финальный rulebook.
- **TO-PLAYTEST / TO-BALANCE** — требуется бумажный тест / расчёт.
- **SUPERSEDED / OLD MODEL** — заменено новой моделью, не использовать как активный дизайн.
- **ARCHIVE** — исторический материал / архив разговора.

## Активные корневые документы

| Код | Документ | Путь | Статус | Версия | Что фиксирует |
|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | `/PROJECT_CORE_CONTEXT.md` | ACTIVE | v2.0-cleanup | Текущий активный контекст: Dark Cosmic Adventure, 5 ярусов + орбитали, тройка ресурсов, Экополис |
| DEC-REG | DECISIONS | `/DECISIONS.md` | ACTIVE | 2026-07-22 | Решения DEC-001..022; старые DEC-002/003 помечены SUPERSEDED |
| REG-002 | DOCUMENT_REGISTRY | `/DOCUMENT_REGISTRY.md` | ACTIVE | v2.0-cleanup | Реестр документов |
| CHG-001 | CHANGELOG | `/CHANGELOG.md` | ACTIVE | 2026-07-22 | Журнал изменений |
| ROAD-001 | ROADMAP | `/ROADMAP.md` | ACTIVE | 2026-07-22 | Дорожная карта новой модели |
| OQ-001 | OPEN_QUESTIONS | `/OPEN_QUESTIONS.md` | ACTIVE | 2026-07-22 | Открытые вопросы после cleanup |
| CLEAN-001 | REPOSITORY_CLEANUP_2026-07-22 | `docs/00_PROJECT_CORE/REPOSITORY_CLEANUP_2026-07-22.md` | ACTIVE CLEANUP NOTE | v0.1 | Почему старый слой убран из активной модели |

## Активный механический слой — docs/06_MECHANICS

Эта папка является текущим основным рабочим слоем механики после миграционного конфликта со старыми `docs/03_MECHANICS`.

| Код | Документ | Путь | Статус | Категория | Примечание |
|---|---|---|---|---|---|
| STUDIO-001 | STUDIO_BRAIN v0.1 | `docs/06_MECHANICS/` | DRAFT / AUDIT / ACTIVE REFERENCE | студия, жанр, аудит | Зафиксировал Dark Cosmic Adventure и 4 конфликтные зоны |
| CORELOOP-001 | GAME_CORE_LOOP_v0.1 | `docs/06_MECHANICS/GAME_CORE_LOOP_v0.1.md` | DRAFT / TO-PLAYTEST | core loop | Активная механическая опора прототипа |
| PROTO-001 | PROTOTYPE_v0.1_PLAYABLE | `docs/06_MECHANICS/PROTOTYPE_v0.1_PLAYABLE.md` | DRAFT / TO-PLAYTEST | прототип | Старый/новый статус требует проверки под DEC-018..021 |
| MOVE-001 | MOVEMENT_MODEL_v0.1_DRAFT | `docs/06_MECHANICS/MOVEMENT_MODEL_v0.1_DRAFT.md` | DRAFT / FOUNDER-DECISION PARTS / TO-PLAYTEST | движение | Кольца, кубик, секторы, аттестации |
| RES-002 | RESOURCE_MODEL_v0.2_DRAFT | `docs/06_MECHANICS/RESOURCE_MODEL_v0.2_DRAFT.md` | DRAFT / FOUNDER-DECISION PARTS / TO-BALANCE | ресурсы | Дух / Свет / Огонь; три исхода Суда Огня; виды Огня; пути добычи |
| HERO-001 | HEROES_16_v0.1 | `docs/06_MECHANICS/HEROES_16_v0.1.md` | DRAFT / ACTIVE STRUCTURE | роли | 16 ролей заменяют старую 4-role рамку |
| ROLE-001 | ROLES_ARCHITECTURE_v0.1 | `docs/06_MECHANICS/ROLES_ARCHITECTURE_v0.1.md` | DRAFT / ACTIVE STRUCTURE | роли | Архитектура ролей и ограничений |
| FACTION-001 | FACTIONS_OF_WORLDS_v0.1 | `docs/06_MECHANICS/FACTIONS_OF_WORLDS_v0.1.md` | DRAFT | фракции | Требует сверки с 5 ярусами + орбитали |
| INH-001 | INHABITANTS_TEMPLATE_v0.1 | `docs/06_MECHANICS/INHABITANTS_TEMPLATE_v0.1.md` | DRAFT | жители | Шаблон жителей |
| INH-002 | INHABITANTS_PHYSICAL_v0.1 | `docs/06_MECHANICS/INHABITANTS_PHYSICAL_v0.1.md` | DRAFT | жители | Физический ярус |
| INH-003 | INHABITANTS_SUBTLE_v0.1 | `docs/06_MECHANICS/INHABITANTS_SUBTLE_v0.1.md` | DRAFT | жители | Тонкий ярус |
| INH-004 | INHABITANTS_FIRE_v0.1 | `docs/06_MECHANICS/INHABITANTS_FIRE_v0.1.md` | DRAFT | жители | Огненный ярус / переход |
| INH-005 | INHABITANT_TYPES_BY_WORLD_v0.1 | `docs/06_MECHANICS/INHABITANT_TYPES_BY_WORLD_v0.1.md` | DRAFT | жители | Типы жителей по мирам |
| WORLDMECH-001 | MULTIWORLD_ARCHITECTURE_v0.1 | `docs/06_MECHANICS/MULTIWORLD_ARCHITECTURE_v0.1.md` | DRAFT / REVIEW REQUIRED | миры | Проверить против DEC-019; не использовать старую 8-world модель |
| TOOLS-001 | WORLD_TOOLS_MATRIX_v0.1 | `docs/06_MECHANICS/WORLD_TOOLS_MATRIX_v0.1.md` | DRAFT | инструменты | Матрица инструментов по ярусам |
| TOOLS-002 | WORLD_INHABITANTS_AND_TOOLS_v0.2 | `docs/06_MECHANICS/WORLD_INHABITANTS_AND_TOOLS_v0.2.md` | DRAFT | жители, инструменты | Требует сверки с DEC-019 |
| CARDTYPE-001 | CARD_TYPE_SYSTEM_v0.1 | `docs/06_MECHANICS/CARD_TYPE_SYSTEM_v0.1.md` | DRAFT | карты | Типы карт |
| ANALOG-001 | ANALOG_ANALYSIS_v0.1 | `docs/06_MECHANICS/ANALOG_ANALYSIS_v0.1.md` | DRAFT | аналоги | Использовать как дизайн-референсы, не канон |
| SLICE-001 | FIRST_VERTICAL_SLICE_SCENARIO_v0.1 | `docs/06_MECHANICS/FIRST_VERTICAL_SLICE_SCENARIO_v0.1.md` | DRAFT / REVIEW REQUIRED | сценарий | Требует обновления под Dark Cosmic Adventure и Экополис |
| FRACTURE-001 | REALITY_FRACTURES_SYSTEM_v0.1_DRAFT | `docs/03_MECHANICS/REALITY_FRACTURES_SYSTEM_v0.1_DRAFT.md` | DRAFT / TO-PLAYTEST | разломы, карты | Находится в старой папке, но содержательно актуален; позже перенести/зеркалировать в `docs/06_MECHANICS` |

## Активный карточный слой — docs/04_CARDS

| Код | Документ | Путь | Статус | Кол-во | Примечание |
|---|---|---|---|---:|---|
| CARDIDX-001 | CARD_TABLES_IMPORT_INDEX_v0.1 | `docs/04_CARDS/CARD_TABLES_IMPORT_INDEX_v0.1.md` | DRAFT / CARD-DATA-INDEX | — | Индекс карточных таблиц |
| CARD-START-001 | Starter cards | `docs/04_CARDS/data/IVDIVO_144_starter_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 144 | Если CSV ещё не зеркалирован, добавить отдельным PR |
| CARD-DEV-001 | Deckbuilding development | `docs/04_CARDS/data/IVDIVO_90_deckbuilding_development_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 90 | Если CSV ещё не зеркалирован, добавить отдельным PR |
| CARD-INST-001 | Instruments | `docs/04_CARDS/data/IVDIVO_100_instrument_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 100 | Если CSV ещё не зеркалирован, добавить отдельным PR |
| CARD-FORM-001 | Form cards | `docs/04_CARDS/data/IVDIVO_50_form_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 50 | Формы меняют состояние зоны/портала/Корня/закона |
| CARD-ECO-001 | Ecopolis buildings | `docs/04_CARDS/data/IVDIVO_32_ecopolis_organization_buildings_v0_1_DRAFT.csv` | DRAFT / GAME-ADAPTATION | 32 | Активная замена Убежища |
| CARD-LAW-001 | World Laws | `docs/04_CARDS/data/IVDIVO_36_world_law_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 36 | Закон меняет правило, не просто бонус |
| CARD-PORT-001 | Portals + Vortex Modes | `docs/04_CARDS/PORTALS_AND_VORTEX_MODES_v0.1_DRAFT.md` | DRAFT / TO-PLAYTEST | 48 | 36 порталов + 12 режимов Вихря |
| CARD-EVR-001 | Round Events | `docs/04_CARDS/data/IVDIVO_60_round_event_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 60 | События раунда двигают мир |
| CARD-TRL-001 | Trials | `docs/04_CARDS/data/IVDIVO_40_trial_cards_v0_1_DRAFT.csv` | DRAFT / TO-PLAYTEST | 40 | Испытания дают развилку |
| CARD-EVRTRL-INDEX | Round Events and Trials index | `docs/04_CARDS/ROUND_EVENTS_AND_TRIALS_v0.1_DRAFT.md` | DRAFT / TO-PLAYTEST | 100 | Индекс двух колод |

## Старый слой / не использовать как активную модель

| Код | Документ / слой | Путь | Новый статус | Причина |
|---|---|---|---|---|
| OLD-MECH-03 | Старые механики `docs/03_MECHANICS` | `docs/03_MECHANICS/` | SUPERSEDED / PARTIAL MIGRATION | Registry старой версии ссылался сюда как на активную структуру; активная работа сейчас в `docs/06_MECHANICS` |
| OLD-WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | `docs/05_WORLDS/` | SUPERSEDED BY DEC-019 | Восьмимировая/переходная модель заменена 5 ярусами + орбитали |
| OLD-CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | `docs/02_GAME_CONCEPT/` | REVIEW REQUIRED / OLD FRAMING | Может содержать horror / old-world framing |
| OLD-VISUAL-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | `docs/08_VISUAL_BRAND/` | SUPERSEDED / REWRITE REQUIRED | Старый horror-визуал заменить на Dark Cosmic Adventure |
| OLD-ROLE-004 | 4-role framing | разные ранние документы | SUPERSEDED BY HERO-001 | Активно 16 ролей |
| OLD-RESOURCE-RAY | Луч как центральная валюта | разные ранние документы | SUPERSEDED BY DEC-020 | Активно Дух / Свет / Огонь |
| OLD-SHELTER | Убежище как primary base term | разные ранние документы | SUPERSEDED BY DEC-022 | Активно Экополис IVDIVO |

## Правило для будущей работы

1. Если задача касается архитектуры миров — сверяться с DEC-019 и `docs/06_MECHANICS/MULTIWORLD_ARCHITECTURE_v0.1.md` только после проверки на старые 8-world элементы.
2. Если задача касается ресурсов — использовать DEC-020 и `RESOURCE_MODEL_v0.2_DRAFT`.
3. Если задача касается движения — использовать DEC-021 и `MOVEMENT_MODEL_v0.1_DRAFT`.
4. Если задача касается базы игроков — использовать DEC-022 и карточки Экополиса.
5. Если документ содержит horror-primary, 8 worlds, Луч-as-currency, Убежище-primary или 4 roles, он требует пометки `SUPERSEDED / OLD MODEL` перед использованием.
