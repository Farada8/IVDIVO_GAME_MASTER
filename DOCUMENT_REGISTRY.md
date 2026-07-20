# DOCUMENT_REGISTRY

Версия: v1.2  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр основных Markdown-документов репозитория. Обязателен к обновлению при создании, изменении или устаревании любого документа.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, не утверждена.
- **REVIEW** — предложена основателю на утверждение.
- **APPROVED** — утверждено основателем.
- **ACTIVE** — действующий управляющий документ или реестр.
- **OLD MODEL / REVIEW REQUIRED** — документ содержит устаревшую модель и требует сверки перед использованием.
- **SUPERSEDED** — заменено более новой версией, хранится для истории.

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель / связанные |
|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | `PROJECT_CORE_CONTEXT.md` | ACTIVE | v1.6 | корневой контекст | все документы |
| MASTER-002 | MASTER_INDEX | `MASTER_INDEX.md` | ACTIVE | v0.1 | индекс | CORE-001, REG-002 |
| DEC-REG | DECISIONS | `DECISIONS.md` | ACTIVE | rolling | решения | CORE-001 |
| CHG-001 | CHANGELOG | `CHANGELOG.md` | ACTIVE | rolling | история изменений | REG-002 |
| OPENQ-001 | OPEN_QUESTIONS | `OPEN_QUESTIONS.md` | ACTIVE | v0.1 | открытые вопросы | CORE-001, DEC-018 |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | `docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md` | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | MECH-001, WORLD-002 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | `docs/03_MECHANICS/GAME_MECHANICS_v0.1_DRAFT.md` | DRAFT | v0.1 | механика | GCORE-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | `docs/03_MECHANICS/GAME_MATH_v0.1_DRAFT.md` | DRAFT | v0.1 | механика | MECH-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.1_DRAFT.md` | OLD MODEL / REVIEW REQUIRED / SUPERSEDED BY WORLD-002 | v0.1 | миры | DEC-003, DEC-015 |
| WORLD-002 | WORLD_ARCHITECTURE_v0.2_APPROVED | `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.2_APPROVED.md` | APPROVED / FOUNDER-DECISION | v0.2 | миры | DEC-015, CORE-001 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | `docs/06_CHARACTERS_AND_ARCHETYPES/` | DRAFT / частично BLOCKED | v0.1 | персонажи | WORLD-002 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | `docs/07_CAMPAIGNS_AND_STORIES/` | MIGRATION-PARTIAL / DRAFT | v0.1 | сюжеты | WORLD-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | `docs/07_CAMPAIGNS_AND_STORIES/` | DRAFT / BLOCKED | v0.1 | нарратив | STORY-001 |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | `docs/08_VISUAL_BRAND/` | MIGRATION-PARTIAL / DRAFT | v0.1 | визуальный бренд | CORE-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | `docs/09_BUSINESS_MODEL/` | MIGRATION-PARTIAL / DRAFT | v0.1 | сообщество | FRAN-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | `docs/09_BUSINESS_MODEL/` | DRAFT | v0.1 | бизнес, франшиза | FRAN-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | `docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT.md` | DRAFT | v0.1 | франшиза | CORE-001, COMM-001, DIG-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | `docs/15_EDUCATION_AND_PSYCHOLOGY/` | MIGRATION-PARTIAL / DRAFT | v0.1 | психология | CORE-001, FRAN-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | `docs/01_RESEARCH/` | DRAFT | v0.1 | исследование | KS-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | `docs/02_GAME_CONCEPT/` | DRAFT | v0.1 | концепция | CORE-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | `docs/04_CARDS_AND_COMPONENTS/` | DRAFT | v0.1 | компоненты | GCORE-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | `docs/14_TESTING_AND_BALANCE/` | DRAFT | v0.1 | тестирование | CARD-001 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | `docs/10_KICKSTARTER/` | DRAFT | v0.1 | Kickstarter | RES-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | `docs/11_DIGITAL_PRODUCT/` | DRAFT | v0.1 | цифровая версия | FRAN-001 |
| ARCH-20260720-05 | Главная цель, протокол, франшиза | `98_CONVERSATION_ARCHIVE/2026-07-20_main-goal-protocol-franchise.md` | ARCHIVE | v1.0 | архив разговора | DEC-018, FRAN-001 |

## Специальное предупреждение: WORLD-001

`WORLD_ARCHITECTURE_v0.1_DRAFT` содержит старую восьмимировую вертикаль. После DEC-015 / WORLD-002 она не является текущим каноном. Использовать только как исторический источник и банк механических идей после сверки.

## Протокол для новых документов

Перед созданием любого документа:

1. Проверить этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через родительские связи.
3. Проверить, нет ли существующего документа по теме.
4. Если документ существует, обновлять его новой версией или отдельной записью, а не создавать дубликат.
5. После публикации обновить `DOCUMENT_REGISTRY.md`, `MIGRATION_INDEX.md`, `CHANGELOG.md` и, при необходимости, `DECISIONS.md`.

Статус APPROVED не присваивается ассистентом — только на основании прямого решения основателя.
