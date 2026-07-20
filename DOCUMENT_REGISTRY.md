# DOCUMENT_REGISTRY

Версия: v1.2  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20 (добавлен AI-001, архив разговора 2026-07-20, OPEN_QUESTIONS)  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/`. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория (зафиксирован в CHANGELOG.md, запись 2026-07-09).

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем (единственный, кто может присвоить)
- **DEPRECATED** — заменено более новой версией, хранится для истории

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · AI workflow · образование/психология

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE (не Draft/Review/Approved — корневой документ, статус вне обычной шкалы) | v1.1 | бизнес, мир, канон (родитель для всех) | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12, PROPOSED — см. DEC-012) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — не Draft, а BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 (коллизия имени "Кут Хуми") |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| AI-001 | AI_WORKFLOW_EXECUTION_PLAN_v0.1_DRAFT | docs/13_AI_RESULTS/ | DRAFT | v0.1 | AI workflow | CORE-001, DEC-008 | PROMPT_LIBRARY_64_v0.2_DRAFT, IVDIVO_AI_GAME_FACTORY_MASTER_v0.1, IVDIVO_AI_SKILLS_LIBRARY_v0.1, 98_CONVERSATION_ARCHIVE/2026-07-20_AI_WORKFLOW_AND_ARCHIVE_PLAN.md |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 (P57) |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный, не первичный) | CORE-001 | ENT-001 (P25, коллизия "Кут Хуми"), WORLD-001 (P18, параллель с шаманской космологией), PROD-001 (P57, референс Ошо) |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT (входные данные основателя + структурирование) | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12 — качественный слой) | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001 (P18), MECH-001 (P45), PSY-001, NARR-002 (P50) |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT (базовая практика, DEC-011 этап 3; не завершено основателем) | v0.1 | канон (сравнительный) | CORE-001 | MECH-001 (P49.3), COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT (методология + частичный реальный прогон) | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.2 | техническое | — | все документы выше |

---

## Архивы и системные файлы вне `docs/`

| Документ | Путь | Статус | Связанные |
|---|---|---|---|
| 2026-07-20_AI_WORKFLOW_AND_ARCHIVE_PLAN | 98_CONVERSATION_ARCHIVE/ | ARCHIVE / DRAFT | AI-001, CORE-001, DECISIONS.md, CHANGELOG.md |
| OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | AI-001, DEC-012 |

---

## Пробелы по категориям

| Категория | Покрытие | Комментарий |
|---|---|---|
| канон | 1+ сравнительных документов | COMP-001/002/003 — сравнительные источники; первичный канонический индекс ИВДИВО по-прежнему требует отдельного прохода |
| механика | хорошее покрытие | MECH-001, MATH-001, CARD-001, TEST-001 |
| мир | 1 документ | WORLD-001 требует расширения по мере роста дополнений |
| персонажи | частичное покрытие | ENT-001, STORY-001/NARR-002 |
| AI workflow | новое покрытие | AI-001 создан 2026-07-20, требует аудита существующих AI-библиотек |
| дополнения | недостаточно | Нет системного документа дополнений после базовой коробки |
| Kickstarter | есть отдельный документ | KS-001 |
| цифровая версия | есть отдельный документ | DIG-001 |
| франшиза | 2 документа | FRAN-001, VBC-001 частично |
| бизнес | несколько документов | COMM-001, PROD-001, FRAN-001 |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов (кампания на 14 сценариев, листы персонажей, антигерой, реестр пробелов, предложение структуры GitHub, 100 продакшн-промптов), созданных в сессии 2026-07-12 до выяснения, что актуальная топология — пирамида ярусов (DEC-012), а не линейная восьмимировая иерархия. Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном. Кандидаты на перенос после утверждения DEC-012.

## Протокол для новых документов (обязателен для Claude/ассистента)

Перед созданием любого документа:
1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку "Связанные" / "Родитель".
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме — если есть, предложить обновление существующего файла (новая версия + запись в его собственный changelog), а не создание дубликата.
5. Присвоить код (следующий свободный номер в своей категории, например MECH-002, WORLD-002, AI-002).
6. После публикации — обновить этот реестр и `MIGRATION_INDEX.md` при необходимости.

Статус APPROVED никогда не присваивается ассистентом — максимум REVIEW, если документ предлагается основателю к утверждение явно.
