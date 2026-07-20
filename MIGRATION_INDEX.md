# MIGRATION INDEX — перенос из Google Drive

Статус: ACTIVE  
Дата начала: 2026-07-08  
Дата обновления: 2026-07-20

## Цель

Перенести текстовую базу проекта из Google Drive в GitHub без потери структуры, статусов и ссылок на источники.

## Правило

- GitHub используется как главное текстовое хранилище.
- Google Drive сохраняет оригиналы, Word/PDF, изображения, презентации, макеты и тяжёлые файлы.
- Каждый перенесённый документ должен иметь ссылку на исходник.
- APPROVED-документы не изменяются молча.
- После DEC-018 каждый значимый разговор также получает архивный Markdown-документ.

## ⚠️ Известная проблема: коллизия нумерации DEC

В Google Drive и GitHub исторически существуют разные диапазоны и коллизии номеров DEC. До полной перенумерации ссылки на решения должны указывать источник: GitHub-DEC или Drive-DEC.

Текущая ветка синхронизирует ключевые решения DEC-015–DEC-018, но не выполняет полную перенумерацию старых журналов.

## Найденные и перенесённые документы Google Drive

| Статус переноса | Исходный документ | Раздел GitHub | Drive URL |
|---|---|---|---|
| MIGRATION-PARTIAL | PROJECT_CORE_CONTEXT_2026 v1.6 | `PROJECT_CORE_CONTEXT.md` | https://docs.google.com/document/d/1pTm-ZSYXCCXqeEGrQsMqBguytDluuSq1EPGlUs5ZdeE |
| MIGRATED | WORLD_ARCHITECTURE_v0.2_APPROVED | `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.2_APPROVED.md` | https://docs.google.com/document/d/10kZlrTYS9B8IpSyhBO0VJP8UIMDIAu_yZ_3F2Ha5aqc |
| MIGRATION-PARTIAL | GAME_CORE_v0.1_DRAFT | `docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md` | https://docs.google.com/document/d/1DfcQLuGpDVZ24mRLmnNnmDs0lw1Mp_6totiXI8J7Hh0 |
| MIGRATION-PARTIAL | СИСТЕМА_СЮЖЕТОВ_v0.1_DRAFT | `docs/07_CAMPAIGNS_AND_STORIES/STORY_SYSTEM_v0.1_DRAFT.md` | https://docs.google.com/document/d/1s4m5bxxNHtPyRDJtl95xiqGEoyVA6sUmrBnLkhpN3Fk |
| MIGRATION-PARTIAL | VISUAL_BRAND_CODE_v0.1_DRAFT | `docs/08_VISUAL_BRAND/VISUAL_BRAND_CODE_v0.1_DRAFT.md` | https://docs.google.com/document/d/1UucvFIYKuRjUUd0beI8_Xs38miW2p0CmqJPebTwyuTk |
| MIGRATION-PARTIAL | СИСТЕМА_СООБЩЕСТВА_v0.1_DRAFT | `docs/09_BUSINESS_MODEL/COMMUNITY_SYSTEM_v0.1_DRAFT.md` | https://docs.google.com/document/d/1xy_fgLfkP5UvU-tmBB5DuPSEqewfZ7kkhWgcct5QRcA |
| MIGRATION-PARTIAL | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | `docs/15_EDUCATION_AND_PSYCHOLOGY/PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT.md` | https://docs.google.com/document/d/1qjGdK5w0MkwxBuvC9R2IItPA6TByieTXxnN0IPp-vJM |
| MIGRATED | Коммерческая модель франшизы | `docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.1_DRAFT.md` | https://docs.google.com/document/d/1gJ4TWbe68FNsPrDnsCj2qAJXC2f_ffnDEZeViky68y4 |
| MIGRATED | Архив разговора: главная цель / протокол / франшиза | `98_CONVERSATION_ARCHIVE/2026-07-20_main-goal-protocol-franchise.md` | https://docs.google.com/document/d/1X3YwGfFiimwiNim5iLy6fuTrK3QDKApMlVDhzpXklzE |

## Обнаружено в ZIP-архиве, но не полностью перенесено

| Приоритет | Документ | Почему важно |
|---|---|---|
| КРИТИЧЕСКИЙ | ОБЯЗАТЕЛЬНЫЙ_ПРОТОКОЛ_РАБОТЫ_С_ПРОЕКТОМ_v1.0_ACTIVE.docx | Полный оригинал протокола; частично перенесён ранее, требует diff с текущим Drive-документом. |
| ВЫСОКИЙ | 00_MASTER_INDEX_v0.2_ACTIVE.xlsx | Навигационный индекс; GitHub-копия создана как `MASTER_INDEX.md`, но полная таблица остаётся в Drive. |
| ВЫСОКИЙ | RESEARCH_ANALOGS_REGISTER_v0.1.xlsx | Нужен для этапа исследований. |
| СРЕДНИЙ | CONTEXT_KNOWLEDGE_REGISTER_v0.1.xlsx | Каталог контекстной базы знаний. |
| СРЕДНИЙ | 04_РЕЕСТР_ДОКУМЕНТОВ_v0.1.xlsx | История версий управляемых документов. |
| СРЕДНИЙ | 02_ПАСПОРТ_ПРОЕКТА_v0.1_DRAFT.docx | Паспорт проекта, требует утверждения. |

## Следующий проход

1. Полностью синхронизировать `PROJECT_CORE_CONTEXT_2026 v1.6` с GitHub-main после review этой ветки.
2. Разрешить коллизию нумерации DEC между Drive и GitHub.
3. Перенести оставшиеся QUEUED-документы, начиная с реестров и индексов.
4. После каждого переноса обновлять `DOCUMENT_REGISTRY.md`, `MIGRATION_INDEX.md`, `CHANGELOG.md`.
