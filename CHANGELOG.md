# CHANGELOG

Журнал изменений базы знаний GitHub.

## 2026-07-22 — cleanup репозитория под текущие founder-решения

### Added

- `docs/00_PROJECT_CORE/REPOSITORY_CLEANUP_2026-07-22.md` — управляющая заметка cleanup: какие старые слои больше не являются активной моделью и почему.
- `docs/99_ARCHIVE/superseded_2026-07-22/` — архивная корзина старых вариантов, вынесенных из рабочих папок.
- DEC-018 — главный жанр: `Dark Cosmic Adventure`; заменяет horror-primary framing DEC-002.
- DEC-019 — активная архитектура: `5 ярусов + орбитали`; заменяет DEC-003 / 8 миров и закрывает конфликт DEC-012.
- DEC-020 — активная ресурсная модель: Дух / Свет / Огонь; заменяет старый слой `Луч` как central currency.
- DEC-021 — активная рамка движения: кольца / кубик / секторы / аттестации.
- DEC-022 — активная база игроков: Экополис IVDIVO; заменяет Убежище как primary base term.

### Changed

- `PROJECT_CORE_CONTEXT.md` переписан в `v2.0-cleanup`: убраны старые активные утверждения horror-primary / 8 worlds / Убежище; зафиксирована новая текущая рамка.
- `DECISIONS.md` обновлён: DEC-002 и DEC-003 получили статус `SUPERSEDED`; добавлены DEC-018..022.
- `DOCUMENT_REGISTRY.md` обновлён до `v2.1-cleanup-archive`: активные слои оставлены в `docs/06_MECHANICS` и `docs/04_CARDS`, старые варианты теперь указывают на физический архив.
- `ROADMAP.md` переписан под новую модель: cleanup → Dark Cosmic Adventure → 5 ярусов + орбитали → тройка ресурсов → аттестации → Экополис → первый playable vertical slice.
- `OPEN_QUESTIONS.md` обновлён: закрыты старые противоречия; оставлены только реальные вопросы founder / playtest / technical debt.

### Moved to archive bin

Старые варианты физически вынесены из рабочих папок в `docs/99_ARCHIVE/superseded_2026-07-22/`:

- `docs/02_GAME_CONCEPT/GAME_CONCEPT_ONE_PAGER_v0.1_DRAFT.md`
- `docs/03_MECHANICS/GAME_CORE_v0.1_DRAFT.md`
- `docs/03_MECHANICS/GAME_MECHANICS_v0.1_DRAFT.md`
- `docs/03_MECHANICS/GAME_MATH_v0.1_DRAFT.md`
- `docs/04_CARDS_AND_COMPONENTS/PROTOTYPE_V01_COMPONENTS_v0.1_DRAFT.md`
- `docs/05_WORLDS/WORLD_ARCHITECTURE_v0.1_DRAFT.md`
- `docs/06_CHARACTERS_AND_ARCHETYPES/ENTITIES_AND_CHARACTERS_v0.1_DRAFT.md`
- `docs/08_VISUAL_BRAND/VISUAL_BRAND_CODE_v0.1_DRAFT.md`

### Superseded / cleaned from active model

- Horror как главный жанр.
- Восемь миров как позвоночник архитектуры.
- Схема 16 миров / 1024 уровня как архитектура.
- Луч как единственный центральный ресурс.
- Убежище как primary base term.
- Старые 4 роли как активная ролевая рамка.
- Старый registry v1.2 как достоверная карта репозитория.

### Not moved yet

`docs/03_MECHANICS/REALITY_FRACTURES_SYSTEM_v0.1_DRAFT.md` оставлен в рабочем дереве временно, потому что содержательно ещё используется как система Разломов. Его нужно позже перенести или зеркалировать в `docs/06_MECHANICS` отдельным PR.

### Next

- Проверить cleanup PR и слить в `main` после ревью.
- Затем провести первый бумажный тест новой модели: 1 диск / 1 орбиталь / 4 роли / Дух-Свет-Огонь / Экополис / 10 событий / 10 испытаний / 1 аттестация.

## 2026-07-22 — система Разломов Реальности

### Added

- `docs/03_MECHANICS/REALITY_FRACTURES_SYSTEM_v0.1_DRAFT.md` — рабочая система Разломов Реальности для IVDIVO: 36 Разломов, 60 Проявлений, 50 Искажений, 36 Корней; каждый Корень имеет два решения — Разрыв и Преобразование.

### Changed

- `DOCUMENT_REGISTRY.md` — добавлена запись `MECH-002 / CARD-SYSTEM-001` для системы Разломов Реальности.

### Notes

- Документ имеет статус DRAFT. Это не утверждённый канон и не финальный баланс.
- Horror не используется как главный жанр; система оформлена как космологические кризисы повреждения миров, законов, связей, памяти, порталов и Форм.

## 2026-07-12 (архивация разговора, полный протокол)

### Added
- `98_CONVERSATION_ARCHIVE/2026-07-12_topologiya-piramida-sintez-razrabotok.md` — полный архив разговора по стандартному шаблону.
- `OPEN_QUESTIONS.md` — единая точка входа для нерешённых вопросов.
- `references/NARRATIVE_DESIGN_FRAMEWORKS_v0.1_DRAFT.md`.
- В `docs/03_MECHANICS/GAME_MECHANICS_v0.1_DRAFT.md` — P49.4: асимметричная видимость колец как источник push-your-luck.
- `docs/13_AI_RESULTS/CROSS_MODEL_AUDIT_PROTOCOL_v0.1_DRAFT.md`.

### Notes

- Этот блок оставлен как исторический журнал до cleanup.
