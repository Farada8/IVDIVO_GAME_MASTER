# DOCUMENT_REGISTRY

Версия: v1.2
Дата создания: 2026-07-09
Дата обновления: 2026-07-11 (добавлен MECH-002; CORE-001 обновлён до v1.2)
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

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес

Категории не покрытые ни одним документом на дату реестра: **дополнения** — см. раздел "Пробелы" внизу.

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE (не Draft/Review/Approved — корневой документ, статус вне обычной шкалы) | v1.2 | бизнес, мир, канон (родитель для всех) | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MECH-002, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика | GCORE-001 | MECH-002, MATH-001, WORLD-001 |
| MECH-002 | WORLD_ECONOMY_SYSTEM_v0.1_APPROVED | docs/03_MECHANICS/ | APPROVED / FOUNDER-DECISION | v0.1 | механика, мир, бизнес | CORE-001, GCORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001, NARR-002 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, MECH-002, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, MECH-002, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — не Draft, а BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, MECH-002, COMP-001 (коллизия имени "Кут Хуми") |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | MECH-002 |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001, MECH-002 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | не покрыто текущими категориями (требуется добавить "образование/психология") | CORE-001 | PROD-001 (P57) |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный, не первичный) | CORE-001 | ENT-001 (P25, коллизия "Кут Хуми"), WORLD-001 (P18, параллель с шаманской космологией), PROD-001 (P57, референс Ошо) |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT (входные данные основателя + структурирование) | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | механика | MATH-001 | CARD-001, KS-001 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001 (P18), MECH-001 (P45), PSY-001, NARR-002 (P50) |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.2 | техническое | — | все документы выше |

---

## Пробелы по категориям (на 2026-07-11)

| Категория | Покрытие | Комментарий |
|---|---|---|
| канон | 1 документ (сравнительный) | COMP-001 — только сравнительные традиции и веб-источники; первичный канонический индекс (P01, прямое чтение "Синтезов" ИВДИВО) по-прежнему не выполнен |
| механика | 4 документа | GCORE-001, MECH-001, MECH-002, MATH-001; MECH-002 утверждает системную экономику |
| мир | 2 документа | WORLD-001 и междисциплинарный MECH-002; архитектура миров требует разрешения коллизии ранней и поздней моделей |
| персонажи | 2 документа | ENT-001, STORY-001/NARR-002 частично |
| дополнения | 0 документов | Нет ни одного дополнения после базовой коробки — рано, ядро не подтверждено |
| Kickstarter | 1 отдельный документ | KS-001 |
| цифровая версия | 1 отдельный документ | DIG-001 |
| франшиза | 2 документа | FRAN-001, VBC-001 частично |
| бизнес | 3 документа | COMM-001, PROD-001, MECH-002 частично |

Обновление 2026-07-11: пробелы «Kickstarter» и «цифровая версия» закрыты отдельными документами (KS-001, DIG-001); добавлено покрытие разделов 01, 02, 04, 14 (RES-001, CONC-001, CARD-001, TEST-001); экономика миров зафиксирована в MECH-002.

## Протокол для новых документов (обязателен для Claude/ассистента)

Перед созданием любого документа:
1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку "Связанные" / "Родитель".
3. Определить целевой раздел по категории (см. таблицу выше).
4. Проверить, нет ли уже существующего документа по теме — если есть, предложить обновление существующего файла (новая версия + запись в его собственном changelog), а не создание дубликата.
5. Присвоить код (следующий свободный номер в своей категории, например MECH-002, WORLD-002).
6. После публикации — обновить этот реестр (новая строка) и `MIGRATION_INDEX.md` при необходимости.

Статус APPROVED никогда не присваивается ассистентом — максимум REVIEW, если документ предлагается основателю к утверждению явно. Исключение: прямое подтверждение основателя в текущем диалоге, зафиксированное как FOUNDER-DECISION с указанием источника.
