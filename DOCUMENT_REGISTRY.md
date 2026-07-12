# DOCUMENT_REGISTRY

Версия: v1.5
Дата создания: 2026-07-09
Дата обновления: 2026-07-12
Код документа: REG-002
Тип: [TECHNICAL]

## Назначение

Единый реестр основных документов `docs/`. Обязателен к обновлению при создании, изменении или устаревании документов.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, не проверена.
- **REVIEW** — предложена основателю на утверждение.
- **APPROVED** — утверждено основателем.
- **ACTIVE** — действующий технический/корневой документ.
- **DEPRECATED** — заменено более новой версией.
- **SUPERSEDED** — конкретное положение заменено более поздним решением.
- **BLOCKED** — дальнейшая работа зависит от канона, теста или другого решения.

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE | v1.4 | бизнес, мир, канон | — | все документы |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001–004, MATH-001, WORLD-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT; P49.1 SUPERSEDED | v0.1 | механика | GCORE-001 | MECH-002–004, TEST-002 |
| MECH-002 | WORLD_ECONOMY_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, мир, бизнес | CORE-001 | MECH-003–004, WORLD-001 |
| MECH-003 | PORTAL_CONJUNCTION_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, мир | CORE-001 | TEST-002, MECH-004 |
| MECH-004 | ASCENSION_UNLOCK_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, кампания | CORE-001 | CARD-002, TEST-003, EXP-001 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT / NUMBERS HYPOTHESIS | v0.1 | механика | MECH-001 | TEST-001–003 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT / CANON COLLISION | v0.1 | мир | CORE-001 | MECH-002–004, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT / PARTLY BLOCKED | v0.1 | персонажи | WORLD-001 | NARR-002, MECH-004 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | сюжет | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT / P53 BLOCKED | v0.1 | сюжет, мир | STORY-001 | MECH-004 |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | визуал | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | Kickstarter, франшиза, цифровой продукт | CORE-001 | FRAN-001, KS-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование, психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительный канон | CORE-001 | WORLD-001, ENT-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT / TO-VERIFY | v0.1 | сравнительный канон | COMP-001 | WORLD-001, MECH-004 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | исследование, бизнес | CORE-001 | PROD-001, KS-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | концепт | CORE-001 | GCORE-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT / OLD MODEL PARTLY ACTIVE | v0.1 | компоненты | GCORE-001 | TEST-001–002 |
| CARD-002 | ASCENSION_UNLOCK_MODULES_v0.1_APPROVED | docs/04_CARDS_AND_COMPONENTS/ | APPROVED SYSTEM / COUNTS HYPOTHESIS | v0.1 | компоненты, прогрессия | MECH-004 | TEST-003, EXP-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | тестирование | MATH-001 | CARD-001 |
| TEST-002 | PORTAL_GATE_PLAYTEST_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT / REQUIRED TEST | v0.1 | тестирование | MECH-003 | CARD-001 |
| TEST-003 | ASCENSION_REWARD_PLAYTEST_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT / REQUIRED TEST | v0.1 | тестирование | MECH-004, CARD-002 | EXP-001 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT / DEFERRED BY GATES | v0.1 | Kickstarter | PROD-001 | TEST-001–003 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровой продукт | PROD-001 | WORLD-001 |
| EXP-001 | BASE_GAME_AND_WORLD_EXPANSION_STRATEGY_v0.1_REVIEW | docs/16_EXPANSIONS/ | REVIEW / FOUNDER DIRECTION | v0.1 | дополнения, продукт | CORE-001, MECH-004 | AI-100 |
| AI-100 | PROMPT_EXECUTION_MASTER_100_v0.1_DRAFT | docs/13_AI_RESULTS/ | DRAFT / INITIAL EXECUTION | v0.1 | все категории | CORE-001 | BLOCK-01–10, TEMPLATE-001 |
| BLOCK-01 | PROJECT_AND_GITHUB | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | управление | AI-100 | CORE-001 |
| BLOCK-02 | BASE_GAME | docs/13_AI_RESULTS/blocks/ | DRAFT / REQUIRES PLAYTEST | v0.1 | концепт, механика | AI-100 | GCORE-001 |
| BLOCK-03 | WORLD_EXPANSIONS | docs/13_AI_RESULTS/blocks/ | DRAFT / CANON BLOCKED | v0.1 | дополнения, мир | AI-100 | EXP-001, WORLD-001 |
| BLOCK-04 | STORY_AND_CAMPAIGNS | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | сюжет | AI-100 | NARR-002 |
| BLOCK-05 | CHARACTERS_AND_FACTIONS | docs/13_AI_RESULTS/blocks/ | DRAFT / LORE TO-VERIFY | v0.1 | персонажи | AI-100 | ENT-001 |
| BLOCK-06 | CARDS_TOOLS_ECONOMY | docs/13_AI_RESULTS/blocks/ | DRAFT / NUMBERS HYPOTHESIS | v0.1 | карты, экономика | AI-100 | MECH-002, CARD-002 |
| BLOCK-07 | BOARDS_COMPONENTS_UI | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | компоненты, производство | AI-100 | CARD-001 |
| BLOCK-08 | RULES_BALANCE_TESTING | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | правила, тесты | AI-100 | TEST-001–003 |
| BLOCK-09 | EMOTION_RISK_SOCIAL | docs/13_AI_RESULTS/blocks/ | DRAFT / REQUIRES BLIND TEST | v0.1 | эмоции, UX | AI-100 | TEST-003 |
| BLOCK-10 | VISUAL_PRODUCTION_MARKET | docs/13_AI_RESULTS/blocks/ | DRAFT / DEFERRED BY GATES | v0.1 | визуал, производство, рынок | AI-100 | PROD-001 |
| TEMPLATE-001 | CORE DOCUMENT TEMPLATES | docs/00_PROJECT_CORE/templates/ | ACTIVE WORKING FORMS | v0.1 | управление | AI-100 | все новые документы |
| REG-002 | DOCUMENT_REGISTRY | / | ACTIVE | v1.5 | техническое | — | все документы |

## Ключевые пробелы

1. Не разрешена коллизия ранней восьмимировой модели и более поздней архитектуры уровней/параллельных миров.
2. Core loop не подтверждён бумажным тестом.
3. Карты ролей и реальная экономика базы не сбалансированы.
4. Нет финальных персонажных имён и канонических связей.
5. Производство и Kickstarter заблокированы гейтами тестирования.

## Протокол новых документов

1. Проверить реестр и существующие файлы.
2. Определить источник истины и статус.
3. Не создавать дубликат без причины.
4. Использовать шаблон из `docs/00_PROJECT_CORE/templates/`.
5. Все числа маркировать HYPOTHESIS до теста.
6. После изменения обновить этот реестр и CHANGELOG.
7. APPROVED присваивает только основатель либо прямая запись его решения.
