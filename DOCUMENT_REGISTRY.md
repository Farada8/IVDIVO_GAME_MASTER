# DOCUMENT_REGISTRY

Версия: v1.3
Дата создания: 2026-07-09
Дата обновления: 2026-07-22 (добавлен ART-001: ART_DIRECTION_BRIEF_v0.1_DRAFT)
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

канон · механика · мир · персонажи · дополнения · Kickstarter · цифровая версия · франшиза · бизнес · карты · компоненты · визуальный бренд · арт-дирекшн

---

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE (корневой документ) | v1.1 | бизнес, мир, канон | — | все документы ниже |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (P49.3, P49.4 добавлены 2026-07-12) | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MECH-002 / CARD-SYSTEM-001 | REALITY_FRACTURES_SYSTEM_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика, карты, компоненты, сценарии | GCORE-001, MECH-001 | DEC-005, DEC-006, DEC-015, DEC-016, DEC-017, TEST-001, ART-001 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT (числа = HYPOTHESIS) | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | DRAFT | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002, ART-001 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT (P25 частично зависит от канона — BLOCKED) | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002, MATH-001, COMP-001, ART-001 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | персонажи, мир | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT (P53 — BLOCKED, зависит от канона) | v0.1 | персонажи, мир | STORY-001, WORLD-001, ENT-001 | ART-001 |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | франшиза, визуальный бренд | CORE-001 | PROD-001, ART-001 |
| ART-001 | ART_DIRECTION_BRIEF_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | DRAFT | v0.1 | визуальный бренд, арт-дирекшн, concept art | CORE-001, VBC-001 | WORLD-001, MECH-002, ENT-001, CARD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес | CORE-001 | PROD-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT (P64 = аудит, не проект) | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-001 | FRAN-001, COMM-001 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT / MIGRATION-COMPLETE (2026-07-22) | v0.1 | франшиза, бизнес | CORE-001 | PROD-001, VBC-001, COMM-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001 |
| COMP-001 | COMPARATIVE_TRADITIONS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | ENT-001, WORLD-001, PROD-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | бизнес | CORE-001 | PROD-001, KS-001, CARD-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | мир, механика, бизнес | CORE-001 | GCORE-001, RES-001, ART-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT | v0.1 | механика | GCORE-001, MECH-001, MATH-001 | ENT-001, TEST-001, ART-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT (§7 добавлен 2026-07-12) | v0.1 | механика | MATH-001 | CARD-001, KS-001, COMP-003, MECH-002 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001, ART-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-001, ART-001 |
| COMP-002 | SHMAKOV_ASCENT_PATH_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | COMP-001 | WORLD-001, MECH-001, PSY-001, NARR-002 |
| COMP-003 | SVET_DUH_KUMARY_MAGNIT_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный) | CORE-001 | MECH-001, COMP-001, COMP-002 |
| COMP-004 | MARKET_COMPARATIVE_ANALYSIS_v0.1_DRAFT | references/ | DRAFT | v0.1 | канон (сравнительный), бизнес | CORE-001 | RES-001, TEST-001 |
| NARR-003 | NARRATIVE_DESIGN_FRAMEWORKS_v0.1_DRAFT | references/ | DRAFT | v0.1 | нарратив (методология) | GCORE-001 | ENT-001 |
| REG-002 | DOCUMENT_REGISTRY (этот файл) | / | ACTIVE | v1.3 | техническое | — | все документы выше |

---

## Обновление 2026-07-22 — ART-001

`docs/08_VISUAL_BRAND/ART_DIRECTION_BRIEF_v0.1_DRAFT.md` добавляет рабочий арт-дирекшн IVDIVO: cosmic adventure / mythic cosmology, не horror как главный визуальный язык, стили персонажей, миров, порталов, Разломов, Искажений, Корней, Форм, карт и цветовую систему по мирам.

## Обновление 2026-07-22 — FRAN-001

`docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT.md` полностью синхронизирован с загруженным исходником `Коммерческая модель франшизы.txt`. Удалён статус частичной миграции. Документ остаётся DRAFT; финансовые параметры и юридическая конструкция требуют отдельной проверки.

## Обновление 2026-07-22 — MECH-002

`docs/03_MECHANICS/REALITY_FRACTURES_SYSTEM_v0.1_DRAFT.md` добавляет полный рабочий набор: 36 Разломов, 60 Проявлений, 50 Искажений, 36 Корней. Статус DRAFT. Числовые параметры, ресурсы и эффекты требуют тестирования.

## Архив: до-пирамидная гипотеза (2026-07-12)

`31_IDEAS/archive_pre_pyramid_2026-07-12/` — шесть документов, созданных до выяснения актуальной топологии. Структурные принципы валидны, привязка к конкретным названиям миров/уровней — нет. Не считать текущим каноном.

## Протокол для новых документов

Перед созданием любого документа:
1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку "Связанные" / "Родитель".
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме.
5. Присвоить код.
6. После публикации — обновить этот реестр.

Статус APPROVED никогда не присваивается ассистентом.
