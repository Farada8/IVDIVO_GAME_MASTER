# DOCUMENT_REGISTRY

Версия: v1.2
Дата создания: 2026-07-09
Дата обновления: 2026-07-20 (добавлены TERM-001, FRAN-002, ARCH-2026-07-20, MASTER_INDEX.md и OPEN_QUESTIONS.md; зафиксирован конфликт Drive v1.6 vs GitHub v1.1)
Код документа: REG-002
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/` и ключевых корневых навигационных файлов. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория (зафиксирован в CHANGELOG.md, запись 2026-07-09).

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем (единственный, кто может присвоить)
- **DEPRECATED** — заменено более новой версией, хранится для истории
- **ACTIVE** — действующий реестр, индекс или управляющий файл
- **MIGRATION-PARTIAL** — перенесено частично, требуется сверка с Drive/ZIP
- **OUTDATED VS DRIVE** — GitHub-версия устарела относительно актуального Drive-источника

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · терминология · управление · архив · образование/психология

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE / MIGRATION-PARTIAL / OUTDATED VS DRIVE v1.6 | v1.1 | бизнес, мир, канон | — | все документы ниже; OQ-001 |
| MASTER-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE / GITHUB NAVIGATION BRIDGE | v0.1 | управление | CORE-001 | README, DOCUMENT_REGISTRY, MIGRATION_INDEX |
| OQ-001 | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | v0.1 | управление | CORE-001 | OQ-001..OQ-006 |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12, PROPOSED — см. DEC-012) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT / NEEDS DRIVE v1.6 SYNC | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002, OQ-001 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT / SUPERSEDED BY FRAN-002 FOR UPLOADED SOURCE MIGRATION | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001, FRAN-002 |
| FRAN-002 | COMMERCIAL_FRANCHISE_MODEL_v0.2_DRAFT | docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.2_DRAFT.md | DRAFT | v0.2 | франшиза, бизнес | FRAN-001, CORE-001 | COMM-001, DIG-001, PSY-001, ARCH-2026-07-20 |
| TERM-001 | UNIFIED_TERMINOLOGY_STANDARD_v0.1_DRAFT | docs/00_PROJECT_CORE/UNIFIED_TERMINOLOGY_STANDARD_v0.1_DRAFT.md | DRAFT | v0.1 | терминология, управление | CORE-001 | DEC-001, DEC-006, OQ-001, OQ-003, OQ-004 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный, не первичный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001, FRAN-002 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| ARCH-2026-07-20 | Единая терминология и франшизная модель | 98_CONVERSATION_ARCHIVE/2026-07-20_ЕДИНАЯ-ТЕРМИНОЛОГИЯ-И-ФРАНШИЗА.md | ARCHIVE / MIXED SOURCE | 2026-07-20 | архив | CORE-001 | TERM-001, FRAN-002, OQ-001 |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.2 | техническое | — | все документы выше |

---

## Пробелы и конфликты

| Категория | Покрытие | Комментарий |
|---|---|---|
| канон | частично | Первичный канонический индекс не завершён; требуется аккуратная работа с источниками ИВДИВО. |
| механика | есть | Требует синхронизации с актуальной архитектурой Drive v1.6. |
| мир | есть, но конфликт | GitHub-версия world/core context устарела относительно Drive v1.6. См. OQ-001. |
| персонажи | частично | Некоторые разделы заблокированы до канонической сверки. |
| терминология | добавлено | TERM-001 создан 2026-07-20; требуется MASTER_GLOSSARY_v0.1_DRAFT. |
| франшиза | обновлено | FRAN-002 переносит полный загруженный source-text как v0.2 DRAFT. |
| цифровая версия | есть | DIG-001 существует, нужно связать с франшизной платформой. |
| Kickstarter | есть | KS-001 существует, но запуск зависит от тестовых гейтов. |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии. Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном. Кандидаты на перенос после утверждения и синхронизации актуальной архитектуры.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку `Связанные` / `Родитель`.
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме.
5. Присвоить код.
6. После публикации обновить этот реестр и `MIGRATION_INDEX.md` при необходимости.

Статус APPROVED никогда не присваивается ассистентом — максимум REVIEW, если документ предлагается основателю к утверждению явно.
