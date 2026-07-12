# DOCUMENT_REGISTRY

Версия: v1.6
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
- **SUPERSEDED** — положение или документ заменены более поздним решением.
- **BLOCKED** — дальнейшая работа зависит от канона, теста или другого решения.

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE | v1.5 | бизнес, мир, канон | — | все документы |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT / OLD WORLD REFERENCES REVIEW REQUIRED | v0.1 | механика | CORE-001 | MECH-001–004, MATH-001, WORLD-002 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT; P49.1 SUPERSEDED; OLD WORLD REFERENCES REVIEW REQUIRED | v0.1 | механика | GCORE-001 | MECH-002–004, TEST-002, WORLD-002 |
| MECH-002 | WORLD_ECONOMY_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION; taxonomy review against WORLD-002 | v0.1 | механика, мир, бизнес | CORE-001 | MECH-003–004, WORLD-002 |
| MECH-003 | PORTAL_CONJUNCTION_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, мир | CORE-001 | TEST-002, MECH-004, WORLD-002 |
| MECH-004 | ASCENSION_UNLOCK_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, кампания | CORE-001 | CARD-002, TEST-003, EXP-001, WORLD-002 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT / NUMBERS HYPOTHESIS | v0.1 | механика | MECH-001 | TEST-001–003 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | SUPERSEDED / HISTORICAL DRAFT | v0.1 | мир | old DEC-003 | WORLD-002 |
| WORLD-002 | WORLD_ARCHITECTURE_v0.2_APPROVED | docs/05_WORLDS/ | APPROVED / FOUNDER-DECISION | v0.2 | канон, мир | CORE-001, DEC-015 | MECH-002–004, ENT-001, NARR-002, EXP-001, AI-100 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT / PARTLY BLOCKED / UPDATE TO WORLD-002 REQUIRED | v0.1 | персонажи | WORLD-002 | NARR-002, MECH-004 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | сюжет | CORE-001 | NARR-002, WORLD-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT / OLD WORLD REFERENCES REVIEW REQUIRED | v0.1 | сюжет, мир | STORY-001, WORLD-002 | MECH-004 |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT / UPDATE TO FIVE-WORLD CODES REQUIRED | v0.1 | визуал | CORE-001 | PROD-001, WORLD-002 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | Kickstarter, франшиза, цифровой продукт | CORE-001 | FRAN-001, KS-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование, психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT / NOT CANON SOURCE | v0.1 | сравнительный канон | CORE-001 | WORLD-002, ENT-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT / TO-VERIFY / NOT CANON SOURCE | v0.1 | сравнительный канон | COMP-001 | WORLD-002, MECH-004 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | исследование, бизнес | CORE-001 | PROD-001, KS-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT / UPDATE TO WORLD-002 REQUIRED | v0.1 | концепт | CORE-001 | GCORE-001, WORLD-002 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT / OLD MODEL PARTLY ACTIVE / REVIEW REQUIRED | v0.1 | компоненты | GCORE-001 | TEST-001–002, WORLD-002 |
| CARD-002 | ASCENSION_UNLOCK_MODULES_v0.1_APPROVED | docs/04_CARDS_AND_COMPONENTS/ | APPROVED SYSTEM / COUNTS HYPOTHESIS | v0.1 | компоненты, прогрессия | MECH-004 | TEST-003, EXP-001, WORLD-002 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | тестирование | MATH-001 | CARD-001 |
| TEST-002 | PORTAL_GATE_PLAYTEST_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT / REQUIRED TEST | v0.1 | тестирование | MECH-003 | CARD-001, WORLD-002 |
| TEST-003 | ASCENSION_REWARD_PLAYTEST_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT / REQUIRED TEST | v0.1 | тестирование | MECH-004, CARD-002 | EXP-001, WORLD-002 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT / DEFERRED BY GATES | v0.1 | Kickstarter | PROD-001 | TEST-001–003 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровой продукт | PROD-001 | WORLD-002 |
| EXP-001 | BASE_GAME_AND_WORLD_EXPANSION_STRATEGY_v0.1_REVIEW | docs/16_EXPANSIONS/ | REVIEW / PRODUCT STRATEGY; CANON GROUNDED | v0.1 | дополнения, продукт | CORE-001, MECH-004, WORLD-002 | AI-100 |
| AI-100 | PROMPT_EXECUTION_MASTER_100_v0.2_DRAFT | docs/13_AI_RESULTS/ | DRAFT / CANON ARCHITECTURE RESOLVED | v0.2 | все категории | CORE-001, WORLD-002 | BLOCK-01–10, TEMPLATE-001 |
| BLOCK-01 | PROJECT_AND_GITHUB | docs/13_AI_RESULTS/blocks/ | DRAFT / HISTORICAL INITIAL AUDIT | v0.1 | управление | AI-100 | CORE-001, WORLD-002 |
| BLOCK-02 | BASE_GAME | docs/13_AI_RESULTS/blocks/ | DRAFT / REQUIRES PLAYTEST | v0.1 | концепт, механика | AI-100 | GCORE-001, WORLD-002 |
| BLOCK-03 | WORLD_EXPANSIONS | docs/13_AI_RESULTS/blocks/BLOCK_03_WORLD_EXPANSIONS_v0.2_DRAFT.md | DRAFT / CANON GROUNDED BY DEC-015 | v0.2 | дополнения, мир | AI-100, WORLD-002 | EXP-001 |
| BLOCK-04 | STORY_AND_CAMPAIGNS | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | сюжет | AI-100 | NARR-002, WORLD-002 |
| BLOCK-05 | CHARACTERS_AND_FACTIONS | docs/13_AI_RESULTS/blocks/ | DRAFT / LORE TO-VERIFY | v0.1 | персонажи | AI-100, WORLD-002 | ENT-001 |
| BLOCK-06 | CARDS_TOOLS_ECONOMY | docs/13_AI_RESULTS/blocks/ | DRAFT / NUMBERS HYPOTHESIS | v0.1 | карты, экономика | AI-100 | MECH-002, CARD-002, WORLD-002 |
| BLOCK-07 | BOARDS_COMPONENTS_UI | docs/13_AI_RESULTS/blocks/ | DRAFT / ORBIT MAP TO-VERIFY | v0.1 | компоненты, производство | AI-100 | CARD-001, WORLD-002 |
| BLOCK-08 | RULES_BALANCE_TESTING | docs/13_AI_RESULTS/blocks/ | DRAFT | v0.1 | правила, тесты | AI-100 | TEST-001–003 |
| BLOCK-09 | EMOTION_RISK_SOCIAL | docs/13_AI_RESULTS/blocks/ | DRAFT / REQUIRES BLIND TEST | v0.1 | эмоции, UX | AI-100 | TEST-003 |
| BLOCK-10 | VISUAL_PRODUCTION_MARKET | docs/13_AI_RESULTS/blocks/ | DRAFT / FIVE-WORLD VISUAL SYSTEM REQUIRED | v0.1 | визуал, производство, рынок | AI-100, WORLD-002 | PROD-001 |
| TEMPLATE-001 | CORE DOCUMENT TEMPLATES | docs/00_PROJECT_CORE/templates/ | ACTIVE WORKING FORMS | v0.1 | управление | AI-100 | все новые документы |
| REG-002 | DOCUMENT_REGISTRY | / | ACTIVE | v1.6 | техническое | — | все документы |

## Ключевые пробелы

1. Не составлена карта привязки орбитальных миров к пяти вертикальным мирам.
2. Не определено точное число орбиталей и их пространственная модель.
3. Core loop не подтверждён бумажным тестом.
4. Карты ролей и реальная экономика базы не сбалансированы.
5. Нет финальных персонажных имён и канонических связей.
6. Производство и Kickstarter заблокированы гейтами тестирования.

## Разрешённые коллизии

- Ранняя восьмимировая вертикаль DEC-003 заменена DEC-015.
- Активный источник архитектуры: WORLD-002.
- Старые документы с восьмимировой моделью не удаляются, но не могут использоваться без маркировки `SUPERSEDED / REVIEW REQUIRED`.

## Протокол новых документов

1. Проверить реестр и существующие файлы.
2. Определить источник истины и статус.
3. Для архитектуры миров использовать DEC-015 и WORLD-002.
4. Не создавать дубликат без причины.
5. Использовать шаблон из `docs/00_PROJECT_CORE/templates/`.
6. Все числа маркировать HYPOTHESIS до теста.
7. После изменения обновить этот реестр и CHANGELOG.
8. APPROVED присваивает только основатель либо прямая запись его решения.
