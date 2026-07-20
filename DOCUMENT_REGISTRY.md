# DOCUMENT_REGISTRY

Версия: v1.2  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/`, ключевых корневых файлов и архивных разговоров. Обязателен к обновлению при создании, изменении или устаревании любого документа.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, не утверждена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем
- **ACTIVE** — действующий управляющий документ
- **SUPERSEDED / OLD MODEL** — заменено более новой версией, хранится для истории
- **ARCHIVE** — архив разговора или исторический материал

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE | v1.6 | ядро проекта | — | DECISIONS, WORLD-002, все документы |
| DEC-REG | DECISIONS | /DECISIONS.md | ACTIVE | n/a | решения | CORE-001 | DEC-001–017 |
| CHG-001 | CHANGELOG | /CHANGELOG.md | ACTIVE | n/a | журнал изменений | CORE-001 | REG-002 |
| ROAD-001 | ROADMAP | /ROADMAP.md | ACTIVE | n/a | дорожная карта | CORE-001 | WORLD-002, LVL-001 |
| REG-002 | DOCUMENT_REGISTRY | /DOCUMENT_REGISTRY.md | ACTIVE | v1.2 | техническое | — | все документы |
| MASTER-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE | v0.1 | навигация | CORE-001 | README, REG-002 |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-002, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика | GCORE-001 | MATH-001, WORLD-002, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика | MECH-001 | GCORE-001, WORLD-002, ENT-001 |
| LVL-001 | LEVEL_AND_SCENARIO_PROGRESSION_SYSTEM_v0.1_DRAFT | docs/03_MECHANICS/LEVEL_AND_SCENARIO_PROGRESSION_SYSTEM_v0.1_DRAFT.md | DRAFT | v0.1 | механика, сценарии | WORLD-002 | ARCH-20260720-02, GAME_CORE, STORY_SYSTEM |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | SUPERSEDED / OLD MODEL / REVIEW REQUIRED | v0.1 | мир | CORE-001 | заменено WORLD-002 |
| WORLD-002 | WORLD_ARCHITECTURE_v0.2_APPROVED | docs/05_WORLDS/WORLD_ARCHITECTURE_v0.2_APPROVED.md | APPROVED / FOUNDER-DECISION | v0.2 | мир, канон, архитектура | CORE-001 | DEC-015, LVL-001 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT | v0.1 | персонажи | GCORE-001, WORLD-002 | NARR-002, MATH-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | сюжеты | CORE-001 | NARR-002, LVL-001 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | сюжеты | STORY-001, WORLD-002, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бренд | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | сообщество, бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | продукт, бизнес | CORE-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование, психология | CORE-001 | PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | рынок | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | концепция | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT | v0.1 | карты, компоненты | GCORE-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | тестирование | MATH-001 | CARD-001, KS-001, LVL-001 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровой продукт | PROD-001 | WORLD-002 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительные источники | CORE-001 | ENT-001, WORLD-002 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительные источники | COMP-001 | WORLD-002, MECH-001 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительные источники | CORE-001 | MECH-001, DEC-012 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT | v0.1 | рынок, аналоги | CORE-001 | RES-001, TEST-001 |
| ARCH-20260720-02 | 2026-07-20_СИСТЕМА-МИРОВ-И-УРОВНЕЙ | 98_CONVERSATION_ARCHIVE/2026-07-20_СИСТЕМА-МИРОВ-И-УРОВНЕЙ.md | ARCHIVE | 1.0 | архив разговора | LVL-001 | WORLD-002, DEC-015 |

## Пробелы / открытые зоны

| Категория | Статус | Комментарий |
|---|---|---|
| Орбитали | OPEN | Нужен `ORBITAL_WORLD_MAP_v0.1_DRAFT` и паспорта орбиталей |
| Уровни первой коробки | OPEN | Требуется бумажный тест 5–7 уровней |
| Полная синхронизация Drive → GitHub | PARTIAL | WORLD-002 перенесён; другие Drive-оригиналы остаются частично неперенесёнными |
| MASTER_INDEX | CREATED | GitHub-файл создан 2026-07-20, потому что отсутствовал |

## Архив: до-DEC-015 модели миров

Документы и ответы, основанные на восьми вертикальных мирах или на схеме `4 сферы → 16 миров → 64 уровня → 1024 уровня`, не считаются текущим каноном. Их можно использовать только как банк идей и как источник отдельных игровых механик после перераспределения через WORLD-002.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Проверять `PROJECT_CORE_CONTEXT.md`, `DECISIONS.md`, `CHANGELOG.md`.
3. Если тема касается миров, сверяться с WORLD-002 / DEC-015.
4. Если тема касается уровней, сверяться с LVL-001 и GAME_CORE.
5. Не присваивать APPROVED без прямого решения основателя.
6. После публикации обновлять этот реестр и CHANGELOG.
