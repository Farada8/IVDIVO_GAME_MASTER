# MIGRATION INDEX — перенос из Google Drive

Статус: ACTIVE  
Дата начала: 2026-07-08

## Цель

Перенести текстовую базу проекта из Google Drive в GitHub без потери структуры, статусов и ссылок на источники.

## Правило

- GitHub становится главным текстовым хранилищем.
- Google Drive сохраняет оригиналы, Word/PDF, изображения, презентации, макеты и тяжёлые файлы.
- Каждый перенесённый документ должен иметь ссылку на исходник.
- APPROVED-документы не изменяются молча.

## ⚠️ Известная проблема: коллизия нумерации DEC

В Google Drive существует отдельный, более ранний журнал решений (`00_AI_PROJECT_CORE/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_ACTIVE.xlsx`, автор ChatGPT/Текс, дата 2026-07-07), который использует номера DEC-001–DEC-008 для решений, полностью отличных от `DECISIONS.md` в этом репозитории (например, Drive-DEC-001 объявляет Google Drive источником истины — что впоследствии заменено GitHub-DEC-007).

До явного разрешения этой коллизии (перенумерация одного из журналов) ссылки на "DEC-00X" должны всегда указывать источник: GitHub-DEC или Drive-DEC. Drive-DEC-008 (обязательный протокол работы с проектом) уже перенесён в `DECISIONS.md` под тем же номером — это единственная запись, где коллизия сейчас разрешена явно.

## Найденные документы Google Drive

| Статус переноса | Исходный документ | Раздел GitHub | Drive URL |
|---|---|---|---|
| MIGRATION-PARTIAL | PROJECT_CORE_CONTEXT_2026 | PROJECT_CORE_CONTEXT.md | https://docs.google.com/document/d/1pTm-ZSYXCCXqeEGrQsMqBguytDluuSq1EPGlUs5ZdeE |
| MIGRATION-PARTIAL | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md | https://docs.google.com/document/d/1DfcQLuGpDVZ24mRLmnNnmDs0lw1Mp_6totiXI8J7Hh0 |
| MIGRATION-PARTIAL | СИСТЕМА_СЮЖЕТОВ_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/STORY_SYSTEM_v0.1_DRAFT.md | https://docs.google.com/document/d/1s4m5bxxNHtPyRDJtl95xiqGEoyVA6sUmrBnLkhpN3Fk |
| MIGRATION-PARTIAL | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/VISUAL_BRAND_CODE_v0.1_DRAFT.md | https://docs.google.com/document/d/1UucvFIYKuRjUUd0beI8_Xs38miW2p0CmqJPebTwyuTk |
| MIGRATION-PARTIAL | СИСТЕМА_СООБЩЕСТВА_v0.1_DRAFT | docs/09_BUSINESS_MODEL/COMMUNITY_SYSTEM_v0.1_DRAFT.md | https://docs.google.com/document/d/1xy_fgLfkP5UvU-tmBB5DuPSEqewfZ7kkhWgcct5QRcA |
| MIGRATION-PARTIAL | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT.md | https://docs.google.com/document/d/1qjGdK5w0MkwxBuvC9R2IItPA6TByieTXxnN0IPp-vJM |
| QUEUED — найден в ZIP-архиве (2026-07-08) | GAME_DEVELOPMENT_ROADMAP_v0.1 | ROADMAP.md / docs/00_PROJECT_CORE/ | https://docs.google.com/document/d/1QO9tEZXOLJWrUz40_MXR8NwgEGtvOuEv8zWFr0CP0SU |
| QUEUED — найден в ZIP-архиве | IVDIVO_AI_GAME_FACTORY_MASTER_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/1YGCGOUZJfEJ3iIVdoKCXPGmZWshik-s8y8Bx_yH5nmg |
| QUEUED — найден в ZIP-архиве | IVDIVO_PROMPT_LIBRARY_64_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/1TND6gCOEK-YDfdi92CQLh-E1HlonljOPMfvQ8knE2wE |
| QUEUED — найден в ZIP-архиве | IVDIVO_AI_SKILLS_LIBRARY_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/15nAFoYv1qJH53S4Bc7RJDaV4Gq9GAGfdrj6BjM1PNSg |
| QUEUED — найден в ZIP-архиве | WEB_SOURCE_LIBRARY_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1r42Prk2XjmlIt0DVMMmyfhqRfZ-XHMxGTP5XwBuLb3A |
| QUEUED — найден в ZIP-архиве | ALICE_BAILEY_SOURCE_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1IMe76wizfMKN0C1-pRXrPfgrbAw57UhQ-foaMvcXUkU |
| QUEUED — найден в ZIP-архиве | ROSE_OF_WORLD_SOURCE_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1Xz8VQNrzCKHj4X3_oQwELrv10FjJFI3PHdae6TjC3iA |
| QUEUED | Коммерческая модель франшизы | docs/12_FRANCHISE/ | uploaded file in ChatGPT context |

## Обнаружено в ZIP-архиве, но не отслеживалось в этом индексе (найдено 2026-07-09)

Эти документы существуют в `IVDIVO_CARD_GAME_MASTER-20260708T222947Z-3-001.zip`, но ранее не были внесены ни в GitHub, ни в этот индекс:

| Приоритет | Документ | Путь в ZIP | Почему важно |
|---|---|---|---|
| КРИТИЧЕСКИЙ | ОБЯЗАТЕЛЬНЫЙ_ПРОТОКОЛ_РАБОТЫ_С_ПРОЕКТОМ_v1.0_ACTIVE.docx | 00_AI_PROJECT_CORE/01_СТРАТЕГИЯ_И_РАМКИ/ | Цитируется как APPROVED входной материал в GAME_CORE_v0.1_DRAFT.md; сам текст решения (DEC-008) уже в DECISIONS.md, но протокольный документ ещё не перенесён |
| ВЫСОКИЙ | 00_MASTER_INDEX_v0.2_ACTIVE.xlsx | 00_AI_PROJECT_CORE/ | Главный навигационный индекс всех управляемых документов проекта с кодами (CORE-001, PASS-001, PROT-001 и т.д.) — основа для будущего docs/00_PROJECT_CORE/ |
| ВЫСОКИЙ | RESEARCH_ANALOGS_REGISTER_v0.1.xlsx | 11_ИССЛЕДОВАНИЯ_И_АНАЛОГИ/00_ИНДЕКС_ИССЛЕДОВАНИЙ/ | Напрямую нужен для Этапа 1 ROADMAP.md ("Исследования и аналоги") |
| СРЕДНИЙ | CONTEXT_KNOWLEDGE_REGISTER_v0.1.xlsx | 12_КОНТЕКСТНАЯ_БАЗА_ЗНАНИЙ/00_КАТАЛОГ/ | Каталог контекстной базы знаний |
| СРЕДНИЙ | 04_РЕЕСТР_ДОКУМЕНТОВ_v0.1.xlsx | 00_AI_PROJECT_CORE/ | История версий управляемых документов |
| СРЕДНИЙ | 02_ПАСПОРТ_ПРОЕКТА_v0.1_DRAFT.docx | 00_AI_PROJECT_CORE/ | Паспорт проекта (DRAFT, требует утверждения) |
| НИЗКИЙ | 06_ТЕКУЩАЯ_ЗАДАЧА_v0.1_DRAFT.docx | 00_AI_PROJECT_CORE/ | Снимок активной задачи на 2026-07-07 — вероятно устарел |
| НИЗКИЙ | 00_КАРТА_ПРОЕКТА_IVDIVO_GAME.docx | 00_START_HERE/ | Карта проекта |
| НИЗКИЙ | CANON_MASTER_REGISTER_v0.1.xlsx | 01_КАНОН_IVDIVO/00_КАНОНИЧЕСКИЙ_ИНДЕКС/ | Канонический индекс источников |
| НИЗКИЙ | OFFICIAL_SITE_SOURCE_REGISTER_v0.1.xlsx | 01_КАНОН_IVDIVO/.../01_OFFICIAL_SITE_ARCHIVE/ | Реестр источников официального сайта |

## Следующий проход

1. Перенести документы со статусом QUEUED — все уже физически найдены в ZIP-архиве, ждать нечего.
2. Перенести таблицу выше ("Обнаружено в ZIP-архиве") — в первую очередь Обязательный протокол и Master Index.
3. Разрешить коллизию нумерации DEC (см. предупреждение выше).
4. После каждого переноса обновлять этот индекс.
