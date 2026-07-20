# MIGRATION INDEX — перенос из Google Drive

Статус: ACTIVE  
Дата начала: 2026-07-08  
Дата обновления: 2026-07-20

## Цель

Перенести текстовую базу проекта из Google Drive в GitHub без потери структуры, статусов и ссылок на источники.

## Правило

- GitHub становится главным текстовым хранилищем.
- Google Drive сохраняет оригиналы, Word/PDF, изображения, презентации, макеты и тяжёлые файлы.
- Каждый перенесённый документ должен иметь ссылку на исходник.
- APPROVED-документы не изменяются молча.

## ⚠️ Известная проблема: коллизия нумерации DEC

В Google Drive существует отдельный, более ранний журнал решений (`00_AI_PROJECT_CORE/03_ЖУРНАЛ_РЕШЕНИЙ_v0.2_ACTIVE.xlsx`), который использует номера DEC-001–DEC-008 для решений, отличных от `DECISIONS.md` в этом репозитории.

До явного разрешения этой коллизии ссылки на `DEC-00X` должны всегда указывать источник: GitHub-DEC или Drive-DEC.

## ⚠️ Второй случай коллизии DEC (внутри GitHub, 2026-07-11)

При работе над принципом `архитектура → философия → базовые практики → отбор → активация` запись была сначала закоммичена как DEC-009 без проверки кросс-ссылок. Исправлено перенумерованием в DEC-011. Урок: перед присвоением следующего номера DEC грепать весь репозиторий на `DEC-0\d\d`.

## ⚠️ Новый конфликт синхронизации: Drive v1.6 vs GitHub v1.1 (найдено 2026-07-20)

Google Drive `PROJECT_CORE_CONTEXT_2026` экспортируется как v1.6 и содержит актуальное решение: пять вертикальных миров + орбитали параллельных миров; ранняя восьмимировая вертикаль указана как SUPERSEDED BY DEC-015.

GitHub `PROJECT_CORE_CONTEXT.md` пока остаётся v1.1 и содержит старую восьмимировую вертикаль. GitHub `DECISIONS.md` содержит DEC-003 про восемь миров и DEC-012 как PROPOSED-пирамиду, но не содержит Drive-DEC-015. Это требует отдельного синхронизационного прохода, а не молчаливой правки.

Следующий синхронизационный пакет: `SYNC_PROJECT_CORE_v1.6_AND_DEC015`.

## Найденные документы Google Drive

| Статус переноса | Исходный документ | Раздел GitHub | Drive URL / источник |
|---|---|---|---|
| MIGRATION-PARTIAL / OUTDATED VS DRIVE v1.6 | PROJECT_CORE_CONTEXT_2026 | PROJECT_CORE_CONTEXT.md | https://docs.google.com/document/d/1pTm-ZSYXCCXqeEGrQsMqBguytDluuSq1EPGlUs5ZdeE |
| MIGRATION-PARTIAL | GAME_CORE_v0.1_DRAFT | docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md | https://docs.google.com/document/d/1DfcQLuGpDVZ24mRLmnNnmDs0lw1Mp_6totiXI8J7Hh0 |
| MIGRATION-PARTIAL | СИСТЕМА_СЮЖЕТОВ_v0.1_DRAFT | docs/07_CAMPAIGNS_AND_STORIES/STORY_SYSTEM_v0.1_DRAFT.md | https://docs.google.com/document/d/1s4m5bxxNHtPyRDJtl95xiqGEoyVA6sUmrBnLkhpN3Fk |
| MIGRATION-PARTIAL | VISUAL_BRAND_CODE_v0.1_DRAFT | docs/08_VISUAL_BRAND/VISUAL_BRAND_CODE_v0.1_DRAFT.md | https://docs.google.com/document/d/1UucvFIYKuRjUUd0beI8_Xs38miW2p0CmqJPebTwyuTk |
| MIGRATION-PARTIAL | СИСТЕМА_СООБЩЕСТВА_v0.1_DRAFT | docs/09_BUSINESS_MODEL/COMMUNITY_SYSTEM_v0.1_DRAFT.md | https://docs.google.com/document/d/1xy_fgLfkP5UvU-tmBB5DuPSEqewfZ7kkhWgcct5QRcA |
| MIGRATION-PARTIAL | PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT | docs/15_EDUCATION_AND_PSYCHOLOGY/PSYCHOLOGICAL_METHODOLOGY_v0.1_DRAFT.md | https://docs.google.com/document/d/1qjGdK5w0MkwxBuvC9R2IItPA6TByieTXxnN0IPp-vJM |
| QUEUED | GAME_DEVELOPMENT_ROADMAP_v0.1 | ROADMAP.md / docs/00_PROJECT_CORE/ | https://docs.google.com/document/d/1QO9tEZXOLJWrUz40_MXR8NwgEGtvOuEv8zWFr0CP0SU |
| QUEUED | IVDIVO_AI_GAME_FACTORY_MASTER_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/1YGCGOUZJfEJ3iIVdoKCXPGmZWshik-s8y8Bx_yH5nmg |
| MIGRATION-PARTIAL | IVDIVO_PROMPT_LIBRARY_64_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/1TND6gCOEK-YDfdi92CQLh-E1HlonljOPMfvQ8knE2wE |
| QUEUED | IVDIVO_AI_SKILLS_LIBRARY_v0.1 | docs/13_AI_RESULTS/ | https://docs.google.com/document/d/15nAFoYv1qJH53S4Bc7RJDaV4Gq9GAGfdrj6BjM1PNSg |
| QUEUED | WEB_SOURCE_LIBRARY_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1r42Prk2XjmlIt0DVMMmyfhqRfZ-XHMxGTP5XwBuLb3A |
| QUEUED | ALICE_BAILEY_SOURCE_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1IMe76wizfMKN0C1-pRXrPfgrbAw57UhQ-foaMvcXUkU |
| QUEUED | ROSE_OF_WORLD_SOURCE_INDEX_v0.1 | references/ | https://docs.google.com/document/d/1Xz8VQNrzCKHj4X3_oQwELrv10FjJFI3PHdae6TjC3iA |
| MIGRATION-COMPLETE-FOR-UPLOADED-SOURCE | Коммерческая модель франшизы | docs/12_FRANCHISE/COMMERCIAL_FRANCHISE_MODEL_v0.2_DRAFT.md | uploaded file `Коммерческая модель франшизы.txt`; archived 2026-07-20 |
| CREATED-FROM-CONVERSATION | Единая терминология | docs/00_PROJECT_CORE/UNIFIED_TERMINOLOGY_STANDARD_v0.1_DRAFT.md | conversation 2026-07-20 |
| CREATED-FROM-CONVERSATION | Архив разговора: единая терминология и франшиза | 98_CONVERSATION_ARCHIVE/2026-07-20_ЕДИНАЯ-ТЕРМИНОЛОГИЯ-И-ФРАНШИЗА.md | conversation 2026-07-20 |

## Обнаружено в ZIP-архиве, но не отслеживалось в этом индексе (найдено 2026-07-09)

| Приоритет | Документ | Путь в ZIP | Почему важно |
|---|---|---|---|
| КРИТИЧЕСКИЙ | ОБЯЗАТЕЛЬНЫЙ_ПРОТОКОЛ_РАБОТЫ_С_ПРОЕКТОМ_v1.0_ACTIVE.docx | 00_AI_PROJECT_CORE/01_СТРАТЕГИЯ_И_РАМКИ/ | Цитируется как APPROVED входной материал; частичный перенос выполнен в `docs/00_PROJECT_CORE/MANDATORY_WORK_PROTOCOL_v1.0_ACTIVE.md`. |
| ВЫСОКИЙ | 00_MASTER_INDEX_v0.2_ACTIVE.xlsx | 00_AI_PROJECT_CORE/ | Главный навигационный индекс всех управляемых документов проекта. |
| ВЫСОКИЙ | RESEARCH_ANALOGS_REGISTER_v0.1.xlsx | 11_ИССЛЕДОВАНИЯ_И_АНАЛОГИ/00_ИНДЕКС_ИССЛЕДОВАНИЙ/ | Нужен для исследования и аналогов. |
| СРЕДНИЙ | CONTEXT_KNOWLEDGE_REGISTER_v0.1.xlsx | 12_КОНТЕКСТНАЯ_БАЗА_ЗНАНИЙ/00_КАТАЛОГ/ | Каталог контекстной базы знаний. |
| СРЕДНИЙ | 04_РЕЕСТР_ДОКУМЕНТОВ_v0.1.xlsx | 00_AI_PROJECT_CORE/ | История версий управляемых документов. |
| СРЕДНИЙ | 02_ПАСПОРТ_ПРОЕКТА_v0.1_DRAFT.docx | 00_AI_PROJECT_CORE/ | Паспорт проекта. |
| НИЗКИЙ | 06_ТЕКУЩАЯ_ЗАДАЧА_v0.1_DRAFT.docx | 00_AI_PROJECT_CORE/ | Снимок активной задачи на 2026-07-07. |
| НИЗКИЙ | 00_КАРТА_ПРОЕКТА_IVDIVO_GAME.docx | 00_START_HERE/ | Карта проекта. |
| НИЗКИЙ | CANON_MASTER_REGISTER_v0.1.xlsx | 01_КАНОН_IVDIVO/00_КАНОНИЧЕСКИЙ_ИНДЕКС/ | Канонический индекс источников. |
| НИЗКИЙ | OFFICIAL_SITE_SOURCE_REGISTER_v0.1.xlsx | 01_КАНОН_IVDIVO/.../01_OFFICIAL_SITE_ARCHIVE/ | Реестр источников официального сайта. |

## Следующий проход

1. Выполнить `SYNC_PROJECT_CORE_v1.6_AND_DEC015`.
2. Перенести документы QUEUED.
3. Разрешить коллизию нумерации DEC.
4. После каждого переноса обновлять этот индекс.
