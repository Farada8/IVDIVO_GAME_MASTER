# PROMPT_DEVELOPMENTS_2026-07-22_SYNC_REPORT_v0.1_DRAFT

Дата: 2026-07-22  
Статус: DRAFT / SYNC REPORT  
Тип: [AI-RESULTS] [PROMPT-DEVELOPMENTS] [GITHUB-DRIVE-SYNC]  
Основание: запрос основателя внести все сегодняшние разработки по промтам из разных разговоров в GitHub и Google Drive.

## 1. Назначение

Этот документ фиксирует единый синхронизационный срез всех разработок, видимых на 2026-07-22 в GitHub / Google Drive / текущем проектном контексте. Он не заменяет сами рабочие документы и таблицы, а связывает их в один навигационный слой, чтобы Claude, GPT и команда разработки могли продолжать работу из GitHub без чтения разрозненных чатов.

Главное правило: если полный документ или таблица уже существуют в GitHub или Google Drive, этот отчёт не дублирует весь массив, а фиксирует путь, статус, состав и ограничения. Если полный массив не удалось перенести, это отмечено явно.

## 2. Критические правила основателя, подтверждённые сегодня

- GitHub должен содержать сами данные и инструкции, а не только ссылки на Google Drive.
- Google Drive остаётся человекочитаемым зеркалом и местом для native Docs / Sheets.
- Нельзя говорить «всё сохранено», пока файл или PR не подтверждает наличие данных.
- Все новые материалы, созданные по промтам, должны быть связаны с актуальным контекстом проекта, а не висеть в чатах.
- Рабочие карточные модули имеют статус DRAFT / TO-PLAYTEST и не становятся каноном без отдельного решения основателя.

## 3. Текущий источник архитектуры

- Актуальная архитектура: PROJECT_CORE_CONTEXT_2026 v1.6 + WORLD_ARCHITECTURE_v0.2_APPROVED / WORLD-002 / DEC-015.
- Основная схема: пять вертикальных миров + орбитали / параллельные миры.
- Старые восьмимировые и шестнадцатимировые модели не используются как текущий канон; они могут сохраняться только как архив / рабочие идеи.

## 4. GitHub-разработки 2026-07-22, обнаруженные и связанные

### 4.1. Миры, орбитали и движение

| Статус | Артефакт | Суть | Где находится |
|---|---|---|---|
| Draft PR #25 | worlds: record founder orbital parallel worlds | Фиксация орбитальных / параллельных миров: физические, тонкие, метагалактические, религиозно-архетипические и синтезные орбитали; отделение клеток/секторов мира от орбитальных миров. | `worlds/2026-07-22-orbitals-revision` |
| main commit | MOVEMENT_MODEL v0.1 | Круги, сектора, кости, движение по зонам и кольцам. | GitHub main |
| main commit | MOVEMENT_MODEL sector LEVELS | Уровни сектора: поле развивается по заслуге игрока; колоды 2–10 накладываются на поле; масштаб не решён. | GitHub main |
| main commit | ZONES_48 v0.1 | 48 секторов-клеток: функция × грань мира × специальные вставки. | GitHub main |
| main commit | EVENTS_SCALES v0.1 | События по масштабу от планеты до вселенной; Council trigger; фракционные/клановые колоды; milestone-восхождения. | GitHub main |

### 4.2. Ресурсы, формы, инструменты, законы

| Статус | Артефакт | Суть | Где находится |
|---|---|---|---|
| main commit | RESOURCE_MODEL_v0.2_DRAFT | Аккумулятор для Fire / Light / Spirit substance model; DRAFT, не утверждено. | GitHub main |
| main commit | RESOURCE_MODEL v0.2 forks | Развилки: энергия как сырьё? выращивание в физическом мире; пять субстанций = пять ярусов; связь со Свет-веществом / Дух-веществом. | GitHub main |
| main commit | FORMS_50 v0.1 DRAFT | 50 карт Форм для материи зоны A; canon-format + playable slice. | GitHub main |
| Draft PR #26 | card data index | Индекс generated card data tables: 144 starter, 90 development, 100 instruments, 50 forms, 32 Ecopolis buildings, 36 world laws. | `cards/2026-07-22-card-tables` |
| main commit | CARDSET_PORTALS_VORTEX_v0.1 | 36 карт порталов + 12 режимов Вихря. | GitHub main |

### 4.3. Карточные модули и банки карт

| Статус | Артефакт | Состав | Где находится |
|---|---|---:|---|
| Draft PR #27 | ROOT_RESOLUTION_CARDS_v0.1_DRAFT | 48 карт: 24 Разрыв + 24 Преобразование. | `cards/2026-07-22-root-resolution-cards` |
| Draft PR #28 | PORTAL_RISK_DECK_v0.1_DRAFT | 36 карт Риска перехода: 12 мягких, 16 средних, 8 тяжёлых. | `cards/2026-07-22-transition-risk-cards` |
| Draft PR #29 | ENTITY_INTERACTION_CARDS_v0.1_DRAFT note | 50 карт Жителей миров, 36 карт Союзников, 24 карты Посредников; raw XLSX/CSV не внесены полностью из-за ограничения загрузки. | `cards/2026-07-22-entity-interaction-cards` |
| Draft PR #30 | OBJECTIVE_CARDS_v0.1_DRAFT | 24 Общие цели + 30 Личные цели. Личные цели усиливают кооперацию, не скрытое предательство. | `cards/2026-07-22-objective-cards` |
| Draft PR #32 | CARD_BANK_MASTER_v0.1_DRAFT | 550 исходных строк; 484 после дедупликации; 66 дублей объединено; 0 строк без функции/эффекта. | `cards/card-bank-master-v0.1` |
| Draft PR #33 | CAMPAIGN_MEMORY_CARDS_v0.1_DRAFT | 100 карт памяти кампании: 40 Consequences, 30 Scars, 30 Transformed Zones. | `archive/2026-07-22-campaign-memory-cards` |
| main commit | PROTOTYPE_V02_300_CARDS_v0.1_DRAFT | Отбор 300 карт для следующего прототипа: 48 keep, 36 rework, 216 new, 24 cut. | `docs/04_CARDS_AND_COMPONENTS/PROTOTYPE_V02_300_CARDS_v0.1_DRAFT.md` |

### 4.4. Кампания, плейтест, Kickstarter и производство

| Статус | Артефакт | Суть | Где находится |
|---|---|---|---|
| Draft PR #31 | CORE_BOX_CAMPAIGN_v0.1_DRAFT | 16 сценариев в банке, 12 сценариев core path, 40 карт кампании, non-legacy replayable campaign. | `campaign/2026-07-22-core-box-campaign` |
| Draft PR #34 | PLAYTEST_PROTOCOL_v0.2_DRAFT | Расширенная форма плейтеста: порталы, Разлом, Искажение, Корень, Разрыв/Преобразование, downtime, повторная игра, пороги переделки. | `agent/playtest-protocol-v0.2` |
| Draft PR #35 | Core Box component list / BOM | 540-card target, boards, 30 double-sided zone tiles, tokens, books, campaign log, organizer; DRAFT/TO-VERIFY. | `feature/2026-07-22-component-list-kickstarter` |
| Draft PR #36 | KICKSTARTER_CORE_BOX_PAGE_v0.1_DRAFT | Полная рабочая Kickstarter page на английском с русскими комментариями под блоками. | `kickstarter/2026-07-22-core-box-page-draft` |
| Google Drive only / to mirror | KICKSTARTER_CORE_BOX_PARAMETERS_v0.1 | Core Box: 1–5 игроков, 90–120 мин, 10–12 сценариев, 8 персонажей, 5 ролей, 450–550 физических карт, dev-bank 800–1000 слотов; no required app / no expensive minis. | Drive `18_KICKSTARTER_И_КРАУДФАНДИНГ` |

## 5. Google Drive-разработки 2026-07-22, обнаруженные и связанные

| Артефакт | Статус | Примечание |
|---|---|---|
| WORLDS_AND_PARALLEL_WORLDS_SCHEMA_v0.1_FOUNDER_CONFIRMED | FOUNDER-CONFIRMED / WORKING | Чистая текущая схема вертикальных миров и орбиталей: основной мир = вертикальный уровень, клетки/сектора = состояния/зоны на круге мира, орбитали = параллельные миры. |
| KICKSTARTER_CORE_BOX_PARAMETERS_v0.1 | DRAFT / TO-VERIFY | Параметры Core Box, созданные сегодня по требованию основателя. Требуется GitHub-зеркало, если его ещё нет в main/PR. |
| KICKSTARTER_CORE_BOX_PAGE_v0.1_DRAFT | DRAFT / TO-PRODUCTION-QUOTE | Drive document created and linked in PR #36. |
| OBJECTIVE_CARDS_v0.1_DRAFT companion sheet | DRAFT / TO-PLAYTEST | Полная таблица 54 карт записана в Drive и связана с PR #30. |
| CAMPAIGN_MEMORY_CARDS_v0.1_DRAFT sheet | DRAFT / TO-VERIFY | Drive sheet создан и связан с PR #33. |
| CARD_BANK_MASTER_v0.1 shell | PARTIAL | Drive shell создан, но полный workbook не был импортирован в connector pass. |
| ENTITY_INTERACTION_CARDS note | PARTIAL | Drive note создан, но raw XLSX/CSV не внесены полностью. |

## 6. Что сегодня уже внесено в GitHub

В GitHub уже зафиксированы данные в `main` и/или draft PRs. Самые важные незакрытые PR: #25–#36. Они не равны merge в `main`, но данные существуют в ветках и PR.

Критически важно: при дальнейшем продолжении Claude должен читать не только `main`, но и открытые draft PRs за 2026-07-22, иначе большая часть сегодняшних разработок будет казаться отсутствующей.

## 7. Что сегодня внесено в Google Drive этим синхронизационным проходом

Создан человекочитаемый Google Drive документ-зеркало этого отчёта: `PROMPT_DEVELOPMENTS_2026-07-22_SYNC_REPORT_v0.1_DRAFT`.

Он нужен как навигационная карта для людей; GitHub остаётся главным рабочим текстовым источником.

## 8. Что не удалось считать как полный текст разговора

Я не получил прямой полный transcript всех сегодняшних разговоров. Сводка основана на:

- доступном проектном контексте;
- personal context по сегодняшним разработкам;
- GitHub recent PRs;
- GitHub recent commits;
- Google Drive search results;
- текущей сессии.

Если в каком-то чате сегодня был сгенерирован текст, но он не попал ни в Drive, ни в GitHub, ни в доступный personal-context summary, этот документ не может гарантировать его полное восстановление.

## 9. Срочные follow-up задачи

1. Зеркалировать в Google Drive те GitHub-only модули, где ещё нет native Drive-документа: `PORTAL_RISK_DECK`, `ROOT_RESOLUTION_CARDS`, `PLAYTEST_PROTOCOL_v0.2`, `COMPONENT_LIST_KICKSTARTER`.
2. Решить, какие draft PRs #25–#36 мержить в `main`, а какие оставить review.
3. Импортировать raw XLSX/CSV для `ENTITY_INTERACTION_CARDS` и `CARD_BANK_MASTER`, если коннектор или ручная загрузка доступна.
4. Создать `TODAY_2026-07-22_MASTER_PROMPT_INDEX` или обновить существующий prompt-library индекс, чтобы будущие AI-агенты запускались не с чата, а с GitHub/Drive.
5. Устранить конфликт: часть сегодняшних PR базируется на открытых ветках, не только на `main`; нужен rebase/merge order.

## 10. Рекомендованный порядок merge/review

1. WORLD / context sync: PR #25 или тот PR, который окончательно закрепляет WORLD-002 / DEC-015 / orbitals.
2. Card data foundation: PR #26, #32, main `PROTOTYPE_V02_300_CARDS`.
3. Card modules: #27, #28, #29, #30, #33.
4. Campaign / playtest: #31, #34.
5. Production / Kickstarter: #35, #36.

До этого порядка нельзя считать main полноценным источником сегодняшнего результата.
