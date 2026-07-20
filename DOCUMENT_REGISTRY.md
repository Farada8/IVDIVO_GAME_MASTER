# DOCUMENT_REGISTRY

Версия: v1.2  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20 (синхронизация CORE v1.6 / DEC-015; архив разговора о формуле проекта, протоколе и франшизе; добавлены MASTER_INDEX и OPEN_QUESTIONS)  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех управляемых документов GitHub. Обязателен к обновлению при создании, изменении или устаревании любого документа. Реализует протокол архитектора репозитория и DEC-008.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена.
- **REVIEW** — предложена основателю на утверждение.
- **APPROVED** — утверждено основателем.
- **ACTIVE** — текущий управляющий документ/реестр.
- **SUPERSEDED / DEPRECATED** — заменено более новой версией, хранится для истории.
- **ARCHIVED** — архив разговора или исторический материал.

## Легенда категорий

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · образование/психология · архив · управление

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE / MIGRATION-PARTIAL (синхронизирован с Drive v1.6 по ключевым решениям 2026-07-20) | v1.6 | управление, канон, мир, бизнес | — | все документы ниже |
| INDEX-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE | v0.1 | управление | CORE-001 | REG-002, MIGRATION_INDEX |
| REG-002 | DOCUMENT_REGISTRY | /DOCUMENT_REGISTRY.md | ACTIVE | v1.2 | управление | CORE-001 | все документы |
| DEC-REG | DECISIONS | /DECISIONS.md | ACTIVE | n/a | управление, канон | CORE-001 | DEC-015, OPENQ-001 |
| ROAD-001 | ROADMAP | /ROADMAP.md | ACTIVE (обновлён под DEC-015) | n/a | управление | CORE-001 | WORLD-001, FRAN-001 |
| OPENQ-001 | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | v0.1 | управление | CORE-001 | DEC-015, FRAN-001 |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3 добавлен 2026-07-12; после DEC-015 требует ревизии) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | SUPERSEDED-PARTIAL / NEEDS v0.2 under DEC-015 | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес, сообщество | CORE-001 | PROD-001, FRAN-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT / linked to Drive 2026-07-20 | v0.1 | франшиза, бизнес | CORE-001 | PROD-001, VBC-001, ARCH-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT (внутренний контур; факты источника TO-VERIFY) | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT (базовая практика, DEC-011 этап 3; не завершено основателем) | v0.1 | канон (сравнительный) | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT (методология + частичный реальный прогон) | v0.1 | исследование, бизнес | CORE-001 | RES-001, TEST-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT (входные данные основателя + структурирование) | v0.1 | исследование, бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT (все числа HYPOTHESIS) | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12) | v0.1 | тестирование, механика | MATH-001 | CARD-001, KS-001, COMP-003 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001 |
| ARCH-001 | 2026-07-20_PROJECT-FORMULA-WORK-PROTOCOL-FRANCHISE | 98_CONVERSATION_ARCHIVE/2026-07-20_PROJECT-FORMULA-WORK-PROTOCOL-FRANCHISE.md | ARCHIVED / MIXED | n/a | архив | CORE-001 | FRAN-001, DEC-015, OPENQ-001 |

---

## Пробелы и статусы после 2026-07-20

| Категория | Статус | Комментарий |
|---|---|---|
| канон | частично синхронизирован | CORE обновлён под Drive v1.6; отдельные world/mechanics docs ещё требуют ревизии под DEC-015 |
| механика | требует ревизии | MECH-001 и GAME_CORE должны учитывать пять вертикальных миров + орбитали |
| мир | нужен новый документ | WORLD-001 v0.1 частично устарел; нужен WORLD_ARCHITECTURE_v0.2 |
| франшиза | DRAFT | FRAN-001 связан с Drive-документом и архивом разговора; числа требуют пилота |
| архивы разговоров | начато | создан `98_CONVERSATION_ARCHIVE/` и добавлен ARCH-001 |

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии. Структурные принципы могут быть валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном. После DEC-015 требуется переоценка.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку «Связанные» / «Родитель».
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме.
5. Присвоить код.
6. После публикации — обновить этот реестр, `CHANGELOG.md` и при необходимости `MIGRATION_INDEX.md`.

Статус APPROVED никогда не присваивается ассистентом — максимум REVIEW, если документ предлагается основателю к утверждению явно.
