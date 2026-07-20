# DOCUMENT_REGISTRY

Версия: v1.2
Дата создания: 2026-07-09
Дата обновления: 2026-07-20 (добавлены MASTER_INDEX.md, OPEN_QUESTIONS.md, архив разговора по архетипической эмоциональности и ARCHETYPICAL_EMOTIONALITY_v0.1_DRAFT)
Код документа: REG-002
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/` и ключевых корневых файлов. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем (единственный, кто может присвоить)
- **ACTIVE** — действующий управляющий / навигационный документ
- **ARCHIVE** — исторический архив разговора или версии
- **DEPRECATED** — заменено более новой версией, хранится для истории

## Легенда категорий

канон · механика · мир · персонажи · архетипы · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · образование/психология · архив · техническое

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE (не Draft/Review/Approved — корневой документ, статус вне обычной шкалы) | v1.1 | бизнес, мир, канон (родитель для всех) | — | все документы ниже |
| MASTER-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE | v0.1 | техническое, навигация | CORE-001 | DOCUMENT_REGISTRY, CHANGELOG, DECISIONS |
| OPENQ-001 | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | v0.1 | техническое, открытые вопросы | CORE-001 | DEC-015, ARCHETYPE-EMO-001 |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12, PROPOSED — см. DEC-012) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT / partially superseded by later DEC-015 context | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — BLOCKED) | v0.1 | персонажи, архетипы | GCORE-001, WORLD-001 | NARR-002, MATH-001, ARCHETYPE-EMO-001 |
| ARCHETYPE-EMO-001 | ARCHETYPICAL_EMOTIONALITY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | DRAFT | v0.1 | архетипы, образование/психология, механика | PSY-001, ENT-001, GCORE-001 | ARCH-2026-07-20-ARCHETYPE-EMO, OPENQ-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 (P57), ARCHETYPE-EMO-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный, не первичный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT (входные данные основателя + структурирование) | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12 — качественный слой) | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT (базовая практика, DEC-011 этап 3; не завершено основателем) | v0.1 | канон (сравнительный) | CORE-001 | MECH-001 (P49.3), COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT (методология + частичный реальный прогон) | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| ARCH-2026-07-20-ARCHETYPE-EMO | Архив разговора: архетипическая эмоциональность | 98_CONVERSATION_ARCHIVE/2026-07-20_архетипическая-эмоциональность.md | ARCHIVE | v1.0 | архив, архетипы, образование/психология | CORE-001 | ARCHETYPE-EMO-001, PSY-001, ENT-001 |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.2 | техническое | — | все документы выше |

---

## Пробелы / актуальные предупреждения

| Категория | Состояние | Комментарий |
|---|---|---|
| канон | частично | первичный канонический индекс по источникам ИВДИВО по-прежнему требует отдельного прохода |
| механика | рабочее покрытие | GAME CORE и GAME MECHANICS существуют, но требуют бумажных тестов |
| мир | конфликт версий | WORLD-001 основан на ранней восьмимировой вертикали; актуальный Drive-контекст v1.6 фиксирует DEC-015: пять вертикальных миров + орбитали |
| персонажи / архетипы | частично | ENT-001 + ARCHETYPE-EMO-001; нужна матрица MVP-архетипов |
| образование/психология | частично | PSY-001 + ARCHETYPE-EMO-001; не превращать в терапевтический продукт |
| дополнения | рано | проектировать после подтверждения базового ядра |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии (пирамида, DEC-012). Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку "Связанные" / "Родитель".
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме — если есть, предложить обновление существующего файла или связанную новую версию, а не хаотичный дубликат.
5. Присвоить код.
6. После публикации — обновить этот реестр и `CHANGELOG.md`.

Статус APPROVED никогда не присваивается ассистентом — максимум DRAFT/REVIEW, если документ предлагается основателю к утверждению явно.
