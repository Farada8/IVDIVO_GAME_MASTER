# DOCUMENT_REGISTRY

Версия: v1.2
Дата создания: 2026-07-09
Дата обновления: 2026-07-20 (добавлены ARCH-2026-07-20-001, WORLD-002, IDEA-2026-07-20-001, MASTER_INDEX.md, OPEN_QUESTIONS.md)
Код документа: REG-002
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/` и ключевых корневых/архивных документов. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория (зафиксирован в CHANGELOG.md, запись 2026-07-09).

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем (единственный, кто может присвоить)
- **DEPRECATED / SUPERSEDED** — заменено более новой версией, хранится для истории
- **ACTIVE** — постоянно обновляемый реестр или корневой документ
- **ARCHIVE** — историческая фиксация разговора или миграции

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · архив · идеи · управление · образование/психология

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE | v1.1 | бизнес, мир, канон | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12, PROPOSED — см. DEC-012) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| WORLD-002 | WORLD_ARCHITECTURE_INTAKE_2026-07-20_DRAFT | docs/05_WORLDS/ | DRAFT / INTAKE | v0.1 | мир, архив | WORLD-001 | ARCH-2026-07-20-001, IDEA-2026-07-20-001, DEC-003, DEC-012 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — не Draft, а BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный, не первичный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT (входные данные основателя + структурирование) | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12 — качественный слой) | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT (базовая практика, DEC-011 этап 3; не завершено основателем) | v0.1 | канон (сравнительный) | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT (методология + частичный реальный прогон) | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| REG-002 | DOCUMENT_REGISTRY | / | ACTIVE | v1.2 | управление | — | все документы выше |
| INDEX-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE | v0.1 | управление | REG-002 | README, PROJECT_CORE_CONTEXT, DECISIONS, CHANGELOG |
| OQ-001 | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | v0.1 | управление | DECISIONS, CHANGELOG | WORLD-002, DEC-012 |
| ARCH-2026-07-20-001 | 2026-07-20_архитектура-вселенной | 98_CONVERSATION_ARCHIVE/ | ARCHIVE / INTAKE | v0.1 | архив, мир | WORLD-001 | WORLD-002, IDEA-2026-07-20-001 |
| IDEA-2026-07-20-001 | 2026-07-20_архитектура-вселенной_ранний-черновик_SUPERSEDED | 31_IDEAS/ | SUPERSEDED / IDEAS | v0.1 | идеи, мир | ARCH-2026-07-20-001 | WORLD-002, DEC-003, DEC-012 |

---

## Пробелы по категориям

| Категория | Покрытие | Комментарий |
|---|---|---|
| канон | сравнительные документы есть; первичный канонический индекс ИВДИВО всё ещё требует отдельного прохода | Не использовать сравнительные материалы как прямой канон |
| механика | хорошее покрытие | Нужны плейтесты и числовые проверки |
| мир | WORLD-001 + WORLD-002 | WORLD-002 — intake, не замена WORLD-001 |
| персонажи | ENT-001, STORY-001/NARR-002 частично | Требует сверки с каноном и IP-языком |
| дополнения | отдельного зрелого документа пока нет | Рано до проверки ядра |
| Kickstarter | KS-001 | Требует обновления после новых исследований рынка |
| цифровая версия | DIG-001 | Должна оставаться необязательной для офлайн-партии |
| франшиза | FRAN-001, PROD-001 частично | Коммерческая модель перенесена частично |
| архив разговоров | ARCH-2026-07-20-001 | Требуется продолжать архивацию прошлых сессий |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии (пирамида, DEC-012), явно помечены как архив, не текущий канон. Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном.

## Архив: ранний 7-уровневый черновик (2026-07-20)

`31_IDEAS/2026-07-20_архитектура-вселенной_ранний-черновик_SUPERSEDED.md` — ранний черновик, созданный до повторной сверки с контекстом. Полезные идеи сохранены, но 7-уровневая структура, прямой язык ИВДИВО и старт от Истока не являются текущей архитектурой проекта.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку «Связанные» / «Родитель».
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме — если есть, предложить обновление существующего файла или новую версию, а не дубликат.
5. Присвоить код.
6. После публикации — обновить этот реестр и `CHANGELOG.md`.

Статус APPROVED никогда не присваивается ассистентом — максимум REVIEW, если документ предлагается основателю к утверждению явно.
