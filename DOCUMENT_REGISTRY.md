# DOCUMENT_REGISTRY

Версия: v1.3  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-20  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех управляемых Markdown-документов репозитория. Обязателен к обновлению при создании, изменении или устаревании любого документа.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, не утверждена.
- **REVIEW** — предложена основателю на утверждение.
- **APPROVED** — утверждено основателем.
- **SUPERSEDED / DEPRECATED** — заменено более новой версией.
- **ACTIVE** — постоянно обновляемый управляющий документ.
- **ARCHIVE** — архив разговора или исторический материал.

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE / GitHub-sync v1.6 | v1.6 | канон, продукт, миры, механика, бизнес | — | все документы |
| INDEX-001 | MASTER_INDEX | /MASTER_INDEX.md | ACTIVE | v0.1 | техническое | CORE-001 | REG-002, README, CHANGELOG |
| REG-002 | DOCUMENT_REGISTRY | /DOCUMENT_REGISTRY.md | ACTIVE | v1.3 | техническое | — | все документы |
| DEC-REG | DECISIONS | /DECISIONS.md | ACTIVE | — | решения | CORE-001 | CHANGELOG, REG-002 |
| CHG-001 | CHANGELOG | /CHANGELOG.md | ACTIVE | — | техническое | REG-002 | все изменения |
| OPENQ-001 | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | v0.1 | открытые вопросы | CORE-001 | EXP-001, FRAN-001 |
| ROAD-001 | ROADMAP | /ROADMAP.md | ACTIVE | — | roadmap | CORE-001 | CHANGELOG |
| GCORE-001 | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/ | MIGRATION-PARTIAL / DRAFT | v0.1 | механика | CORE-001 | MECH-001, MATH-001, WORLD-001, ENT-001 |
| MECH-001 | GAME_MECHANICS_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика | GCORE-001 | MATH-001, WORLD-001, COMP-003 |
| MATH-001 | GAME_MATH_v0.1_DRAFT | docs/03_MECHANICS/ | DRAFT | v0.1 | механика | MECH-001 | GCORE-001, WORLD-001, ENT-001 |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | SUPERSEDED / see DEC-015 | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001 |
| AI-BLOCK-003 | BLOCK_03_WORLD_EXPANSIONS_v0.2_DRAFT | docs/13_AI_RESULTS/blocks/ | DRAFT / CANON-GROUNDED BY DEC-015 | v0.2 | дополнения, миры, AI-results | CORE-001 | EXP-001, WORLD-001 |
| EXP-001 | BASE_GAME_AND_WORLD_EXPANSION_STRATEGY_v0.1_REVIEW | docs/16_EXPANSIONS/ | REVIEW | v0.1 | дополнения, продукт | CORE-001 | AI-BLOCK-003, FRAN-001, ARCH-20260720-03 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза, бизнес | CORE-001 | COMM-001, EXP-001 |
| ENT-001 | ENTITIES_AND_CHARACTERS_v0.1_DRAFT | docs/06_CHARACTERS_AND_ARCHETYPES/ | DRAFT | v0.1 | персонажи | GCORE-001, WORLD-001 | NARR-002 |
| STORY-001 | STORY_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | MIGRATION-PARTIAL / DRAFT | v0.1 | сюжет | CORE-001 | NARR-002 |
| NARR-002 | NARRATIVE_SYSTEM_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/ | DRAFT | v0.1 | сюжет, мир | STORY-001, WORLD-001 | — |
| VBC-001 | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бренд | CORE-001 | PROD-001 |
| COMM-001 | COMMUNITY_SYSTEM_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | MIGRATION-PARTIAL / DRAFT | v0.1 | бизнес, сообщество | CORE-001 | FRAN-001 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | продукт, бизнес | CORE-001 | FRAN-001, COMM-001 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование, психология | CORE-001 | FRAN-001 |
| RES-001 | MARKET_RESEARCH_2026_v0.1_DRAFT | docs/01_RESEARCH/ | DRAFT | v0.1 | исследования | CORE-001 | PROD-001, KS-001 |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT | v0.1 | концепция | CORE-001 | GCORE-001, RES-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT | v0.1 | компоненты | GCORE-001 | TEST-001 |
| TEST-001 | PLAYTEST_PROTOCOL_v0.1_DRAFT | docs/14_TESTING_AND_BALANCE/ | DRAFT | v0.1 | тестирование | MATH-001 | CARD-001, KS-001 |
| KS-001 | KICKSTARTER_PLAN_v0.1_DRAFT | docs/10_KICKSTARTER/ | DRAFT | v0.1 | Kickstarter | PROD-001 | RES-001, TEST-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровой продукт | PROD-001 | WORLD-001, EXP-001 |
| ARCH-20260720-03 | 2026-07-20_СТРУКТУРА-ДОПОЛНЕНИЙ-И-ФРАНШИЗА | 98_CONVERSATION_ARCHIVE/ | ARCHIVE | 1.0 | архив разговора | EXP-001, FRAN-001 | DEC-015, DEC-018 |

## Примечания по состоянию на 2026-07-20

- GitHub `PROJECT_CORE_CONTEXT.md` синхронизирован с Drive v1.6 в ветке архива: DEC-003 помечен как заменённый DEC-015.
- Категория «дополнения» теперь покрыта EXP-001 и AI-BLOCK-003.
- Категория «франшиза» покрыта FRAN-001.
- Открытые вопросы вынесены в `OPEN_QUESTIONS.md`.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонки «Родитель» и «Связанные».
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме.
5. Присвоить код.
6. После публикации обновить этот реестр и `CHANGELOG.md`.

Статус APPROVED никогда не присваивается ассистентом.
