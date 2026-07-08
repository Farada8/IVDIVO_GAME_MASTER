# ZIP_INVENTORY_2026-07-08

Статус: MIGRATION-RAW-INDEXED  
Источник: загруженный архив `IVDIVO_CARD_GAME_MASTER-20260708T223000Z-3-001.zip`  
Размер архива: 5,643,666 bytes  
Всего элементов в ZIP: 424  
Файлов: 50  
Папок: 374

## Типы файлов

- DOCX: 23
- XLSX: 14
- DOC: 13

## DOCX документы

1. `00_AI_PROJECT_CORE/02_ПАСПОРТ_ПРОЕКТА_v0.1_DRAFT.docx`
2. `00_AI_PROJECT_CORE/06_ТЕКУЩАЯ_ЗАДАЧА_v0.1_DRAFT.docx`
3. `00_AI_PROJECT_CORE/01_PROJECT_CORE_v0.1_DRAFT.docx`
4. `00_AI_PROJECT_CORE/05_CHANGELOG_v0.1.docx`
5. `00_AI_PROJECT_CORE/01_СТРАТЕГИЯ_И_РАМКИ/ОБЯЗАТЕЛЬНЫЙ_ПРОТОКОЛ_РАБОТЫ_С_ПРОЕКТОМ_v1.0_ACTIVE.docx`
6. `00_START_HERE/00_КАРТА_ПРОЕКТА_IVDIVO_GAME.docx`
7. `01_КАНОН_IVDIVO/00_ИНСТРУКЦИЯ_ПО_ЗАГРУЗКЕ_ИВДИВО.docx`
8. `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/06_ALICE_BAILEY/ALICE_BAILEY_SOURCE_INDEX_v0.1.docx`
9. `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/07_DANIIL_ANDREEV_ROSE_OF_WORLD/ROSE_OF_WORLD_SOURCE_INDEX_v0.1.docx`
10. `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/10_WEB_SOURCES_AND_LINKS/WEB_SOURCE_LIBRARY_INDEX_v0.1.docx`
11. `03_ИГРОВАЯ_МЕХАНИКА/00_GAME_CORE/GAME_DEVELOPMENT_ROADMAP_v0.1.docx`
12. `03_ИГРОВАЯ_МЕХАНИКА/01_БАЗОВЫЙ_ЦИКЛ/GAME_CORE_v0.1_DRAFT.docx`
13. `06_ИИ_РЕЗУЛЬТАТЫ/10_ЗАДАНИЯ_ДЛЯ_AI/IVDIVO_AI_GAME_FACTORY_MASTER_v0.1.docx`
14. `06_ИИ_РЕЗУЛЬТАТЫ/10_ЗАДАНИЯ_ДЛЯ_AI/IVDIVO_AI_SKILLS_LIBRARY_v0.1.docx`
15. `06_ИИ_РЕЗУЛЬТАТЫ/10_ЗАДАНИЯ_ДЛЯ_AI/IVDIVO_PROMPT_LIBRARY_64_v0.1.docx`
16. `07_СЮЖЕТЫ_И_КАМПАНИИ/СИСТЕМА_СЮЖЕТОВ_v0.1_DRAFT.docx`
17. `08_ВИЗУАЛЬНЫЙ_ДИЗАЙН_И_БРЕНД/01_СТРАТЕГИЯ_БРЕНДА/VISUAL_BRAND_CODE_v0.1_DRAFT.docx`
18. `13_ПСИХОЛОГИЧЕСКАЯ_МЕТОДОЛОГИЯ/01_МЕТОДОЛОГИЯ/PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT.docx`
19. `16_СООБЩЕСТВО/00_PLAN/СИСТЕМА_СООБЩЕСТВА_v0.1_DRAFT.docx`
20. `99_АРХИВ/PROJECT_WORK_PROTOCOL_v1.0_SUPERSEDED_DUPLICATE.docx`
21. `99_АРХИВ/AI_PROJECT_WORK_PROTOCOL_v1.0_ARCHIVE.docx`
22. `99_АРХИВ/05_CHANGELOG_v0.2_UNFINISHED_ARCHIVE.docx`
23. `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/06_ALICE_BAILEY/90_UNVERIFIED_WEB_COPIES/Бейли Алиса. Экстернализация Иерархии - royallib.com.doc.docx`

## XLSX документы

1. `00_AI_PROJECT_CORE/00_MASTER_INDEX_v0.2_ACTIVE.xlsx`
2. `00_AI_PROJECT_CORE/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_ACTIVE.xlsx`
3. `00_AI_PROJECT_CORE/04_РЕЕСТР_ДОКУМЕНТОВ_v0.1.xlsx`
4. `01_КАНОН_IVDIVO/00_КАНОНИЧЕСКИЙ_ИНДЕКС/CANON_MASTER_REGISTER_v0.1.xlsx`
5. `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/00_IVDIVO_PRIMARY_CANON/01_OFFICIAL_SITE_ARCHIVE/OFFICIAL_SITE_SOURCE_REGISTER_v0.1.xlsx`
6. `11_ИССЛЕДОВАНИЯ_И_АНАЛОГИ/00_ИНДЕКС_ИССЛЕДОВАНИЙ/RESEARCH_ANALOGS_REGISTER_v0.1.xlsx`
7. `12_КОНТЕКСТНАЯ_БАЗА_ЗНАНИЙ/00_КАТАЛОГ/CONTEXT_KNOWLEDGE_REGISTER_v0.1.xlsx`
8. `99_АРХИВ/00_MASTER_INDEX_v0.1_SUPERSEDED_A.xlsx`
9. `99_АРХИВ/00_MASTER_INDEX_v0.1_SUPERSEDED_B.xlsx`
10. `99_АРХИВ/03_ЖУРНАЛ_РЕШЕНИЙ_v0.1_SUPERSEDED.xlsx`
11. `99_АРХИВ/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_DUPLICATE_ARCHIVE.xlsx`
12. `99_АРХИВ/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_SUPERSEDED_INTERMEDIATE.xlsx`
13. `99_АРХИВ/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_ARCHIVE_DUPLICATE.xlsx`
14. `99_АРХИВ/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_ARCHIVE_DUPLICATE_2.xlsx`

## DOC источники

13 старых `.doc` файлов находятся в разделе `01_КАНОН_IVDIVO/01_ПЕРВОИСТОЧНИКИ/`. Это крупные первоисточники и web-copies. Они индексированы как сырьевой архив, но не перенесены в GitHub-текст как часть рабочей документации.

## Решение по миграции

- Рабочие документы проекта переносить в `docs/` как Markdown.
- Таблицы XLSX переносить как Markdown/CSV-представления или оставлять как raw metadata.
- Крупные первоисточники и web-copies не смешивать с рабочей документацией игры.
- Частичные файлы `MIGRATION-PARTIAL` заменить на полные Markdown-копии по мере переноса из ZIP.
