# DOCUMENT_REGISTRY

Версия: v1.3  
Дата создания: 2026-07-09  
Дата обновления: 2026-07-22 (добавлен CARD-002: 24 карты Разрыва + 24 карты Преобразования)  
Код документа: REG-002  
Тип: [TECHNICAL]

## Назначение

Единый реестр всех документов `docs/`. Обязателен к обновлению при создании, изменении или устаревании любого документа.

## Легенда статусов

- **DRAFT** — рабочая гипотеза, автор — Claude/ассистент, не проверена
- **REVIEW** — предложена основателю на утверждение
- **APPROVED** — утверждено основателем
- **SUPERSEDED** — заменено более новой версией, хранится для истории
- **ACTIVE** — постоянно обновляемый реестр

## Реестр

| Код | Документ | Путь | Статус | Версия | Категория | Родитель | Связанные |
|---|---|---|---|---|---|---|---|
| CORE-001 | PROJECT_CORE_CONTEXT | /PROJECT_CORE_CONTEXT.md | ACTIVE / synced from Drive v1.6 | v1.6-sync | бизнес, мир, канон | — | все документы ниже |
| DEC | DECISIONS | /DECISIONS.md | ACTIVE | — | управление | CORE-001 | все документы |
| REG-002 | DOCUMENT_REGISTRY | /DOCUMENT_REGISTRY.md | ACTIVE | v1.3 | техническое | — | все документы |
| WORLD-001 | WORLD_ARCHITECTURE_v0.1_DRAFT | docs/05_WORLDS/ | SUPERSEDED IN PART BY WORLD-002 / historical draft | v0.1 | мир | CORE-001 | GCORE-001, MECH-001, ENT-001, NARR-002 |
| WORLD-002 | WORLD_ARCHITECTURE_v0.2_APPROVED | docs/05_WORLDS/ | APPROVED / synced from Drive DEC-015 | v0.2 | мир | CORE-001 | DEC-015, CONC-002, OPEN_QUESTIONS |
| CONC-001 | GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT / needs DEC-015 review | v0.1 | концепция | CORE-001 | GCORE-001, RES-001, WORLD-002 |
| CONC-002 | STRATEGIC_GAME_DEFINITION_v0.1_DRAFT | docs/02_GAME_CONCEPT/ | DRAFT / FOUNDER-FORMULATION | v0.1 | концепция, франшиза | CORE-001 | CONC-001, FRAN-001, DIG-001, PSY-001 |
| CARD-001 | PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT / HYPOTHESIS | v0.1 | карты, прототип | GCORE-001 | MECH-001, MATH-001, TEST-001 |
| CARD-002 | ROOT_RESOLUTION_CARDS_v0.1_DRAFT | docs/04_CARDS_AND_COMPONENTS/ | DRAFT / HYPOTHESIS | v0.1 | карты, Корни, Разрыв, Преобразование | GCORE-001 | MECH-001, MATH-001, CARD-001, TEST-001, WORLD-002 |
| FRAN-001 | COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT | docs/12_FRANCHISE/ | DRAFT | v0.1 | франшиза | CORE-001 | PROD-001, VBC-001, CONC-002 |
| PROD-001 | PRODUCT_AND_FRANCHISE_v0.1_DRAFT | docs/09_BUSINESS_MODEL/ | DRAFT | v0.1 | Kickstarter, франшиза, цифровая версия, бизнес | COMM-001, WORLD-002 | FRAN-001, COMM-001 |
| DIG-001 | DIGITAL_COMPANION_v0.1_DRAFT | docs/11_DIGITAL_PRODUCT/ | DRAFT | v0.1 | цифровая версия | PROD-001 | WORLD-002, CONC-002 |
| PSY-001 | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/ | MIGRATION-PARTIAL / DRAFT | v0.1 | образование/психология | CORE-001 | PROD-001, CONC-002 |
| ARCH-2026-07-20 | 2026-07-20_STRATEGIC-GAME-FRANCHISE | 98_CONVERSATION_ARCHIVE/ | ARCHIVE / REVIEW | — | архив разговора | CORE-001 | CONC-002, FRAN-001, WORLD-002 |
| OPENQ | OPEN_QUESTIONS | /OPEN_QUESTIONS.md | ACTIVE | — | управление | CORE-001 | DEC-015, CONC-002, CARD-002 |

## Примечания 2026-07-22

- `CARD-002` создаёт первый набор карт решения Корня: 24 Разрыва и 24 Преобразования.
- Все числа и эффекты в `CARD-002` имеют статус HYPOTHESIS до плейтестов.
- Набор должен проверяться по TEST-001: выбор Разрыв vs Преобразование в коридоре 35–65%.

## Примечания 2026-07-20

- GitHub был синхронизирован с Google Drive v1.6 по DEC-015.
- Старые документы, построенные на восьмимировой вертикали, не удалены: они требуют отдельного migration pass.
- Новая стратегическая формулировка основателя оформлена как CONC-002, а не как замена CONC-001.

## Протокол для новых документов

Перед созданием любого документа:

1. Сканировать этот реестр и релевантные разделы `docs/`.
2. Найти связанные документы через колонку «Связанные» / «Родитель».
3. Определить целевой раздел по категории.
4. Проверить, нет ли уже существующего документа по теме — если есть, обновить существующий файл или создать новую версию, а не дубликат.
5. Присвоить код.
6. После публикации обновить этот реестр и CHANGELOG.

Статус APPROVED никогда не присваивается ассистентом. Исключение в синхронизации 2026-07-20: WORLD-002 переносит уже утверждённый в Google Drive DEC-015, а не создаёт новое утверждение ассистентом.
