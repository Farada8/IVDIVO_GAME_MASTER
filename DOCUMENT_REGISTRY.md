# DOCUMENT_REGISTRY

Версия: v1.2  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20 (полная синхронизация GAME_CORE v0.1 и архив разговора по ядру игровой механики)  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/` и ключевых архивов. Обязателен к обновлению при создании, изменении или устаревании любого документа.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, не утверждена.
- **REVIEW** — предложена основателю на утверждение.
- **APPROVED** — утверждено основателем.
- **ACTIVE** — постоянно действующий управляющий файл.
- **ARCHIVE** — историческая фиксация разговора или устаревшего материала.
- **DEPRECATED** — заменено более новой версией, хранится для истории.

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · тестирование · архив

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE | v1.1 | бизнес, мир, канон | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md | DRAFT (полная синхронизация 2026-07-20) | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001, ARCH-20260720-GCORE |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12, PROPOSED — см. DEC-012) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT / BLOCKED частично каноном | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование, психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительный канон | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | механика, тестирование | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительный канон | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT (базовая практика, DEC-011 этап 3) | v0.1 | сравнительный канон | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT | v0.1 | сравнительный анализ, бизнес | CORE-001 | RES-001, TEST-001 |
| ARCH-20260720-GCORE | 2026-07-20_ядро-игровой-механики | 98_CONVERSATION_ARCHIVE/2026-07-20_ядро-игровой-механики.md | ARCHIVE | v0.1 | архив, механика | GCORE-001 | GAME_CORE_v0.1_DRAFT; Google Drive archive |
| REG-002 | DOCUMENT_REGISTRY | /DOCUMENT_REGISTRY.md | ACTIVE | v1.2 | техническое | — | все документы выше |

---

## Пробелы и статус покрытия

| Категория | Покрытие | Комментарий |
|---|---|---|
| канон | частичное | первичный канонический индекс ИВДИВО по-прежнему требует отдельной работы |
| механика | хорошее покрытие | GAME_CORE синхронизирован; следующий шаг — прототипный сценарий |
| мир | частичное | WORLD-001 требует согласования с DEC-012, если она будет утверждена |
| персонажи | частичное | ENT-001 и NARR-002 частично зависят от канона |
| дополнения | рано | не проектировать до проверки ядра |
| Kickstarter | есть KS-001 | зависит от тестов |
| цифровая версия | есть DIG-001 | companion должен оставаться необязательным |
| франшиза | есть FRAN-001 | не определяет правила базовой партии |
| архивы | начато | добавлен архив разговора 2026-07-20 по GAME CORE |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии (пирамида, DEC-012). Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном.

## Протокол для новых документов

Перед созданием любого документа:

1. Проверить `PROJECT_CORE_CONTEXT.md`, `DECISIONS.md`, этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку «Связанные» / «Родитель».
3. Проверить, нет ли уже существующего документа по теме.
4. Присвоить код документа.
5. После публикации обновить `DOCUMENT_REGISTRY.md`, `CHANGELOG.md`, а при необходимости `MASTER_INDEX.md` и `OPEN_QUESTIONS.md`.
6. Не присваивать APPROVED без прямого решения основателя.
