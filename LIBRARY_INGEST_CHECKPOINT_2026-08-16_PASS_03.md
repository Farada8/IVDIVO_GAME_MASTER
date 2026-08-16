# IVDIVO Library Ingest Checkpoint — 2026-08-16 — Pass 03

Status: ACTIVE / INCOMPLETE

Purpose: recovery point for the ongoing Google Drive library cleanup and Writers’ Room source architecture. This checkpoint records what has been classified and what remains unresolved. It is not a claim that `19_INBOX_TO_PROCESS` is empty.

## Operating rules

- Preserve different languages, editions and file containers unless an exact duplicate is proven.
- Archive exact duplicates in `20_ARCHIVE_DUPLICATES`; do not delete them automatically.
- Keep craft, fiction, science, metaphysics, scripts, comics, project files and images in separate functional layers.
- Identify opaque numeric/Gutenberg archives from internal metadata/content before routing.
- Do not count broken/error-page files as ingested books.
- Source texts are mined for abstract narrative mechanisms; they are not templates for copying.

## Major corpora established / expanded in this pass

### SF / futures
- MAX_GLEBOV_SF: `Гражданский специалист`, `Рубеж атаки`, `Звезд не хватит на всех. Игры Старших`, `Объект контроля`, `Сумрак Чужой войны`, `Сеть орбитальной блокады`, `Внешняя агрессия` (Барьер Ориона #5), `Лорд утерянных земель` (#4), `Столица мятежной окраины`, `Армада Вторжения`, `Шёпот вакуума` #1–2, `Фактор дисбаланса` (Барьер Ориона #3).
- SERGEY_LUKYANENKO_SF: `Лето волонтёра` (Изменённые #4), `Рыцари Сорока Островов`.
- SF_ANTHOLOGIES: `Спасти человека. Лучшая фантастика 2016`.
- Existing corpora further cleaned/expanded: Victor Pelevin, Blake Crouch, Project Hail Mary, Murderbot, J. G. Ballard, Ishiguro speculative, Red Rising, Children of Time, Ender, Pournelle, Dungeon Crawler Carl, Skyward.

### Horror / thriller
- STEPHEN_KING_FICTION: `После заката`, `Последнее дело Гвенди` (Gwendy #3).
- FIVE_NIGHTS_AT_FREDDYS: numeric archive identified as `Пять ночей у Фредди. Серебряные глаза`.
- Existing thriller/espionage corpora include John le Carré / Smiley, Millennium, Robert Langdon, The Terror, Rollins Sigma Force.

### Romance / relationships
- GABRIEL_COSTA_FICTION: numeric archive identified as `За стенкой. История Отиса Ревиаля` (genre `love_contemporary`).

### Fantasy / YA
- New top shelf `08_FANTASY_REFERENCE` created.
- New top shelf `09_ADVENTURE_HISTORICAL_FICTION` created.
- Multiple series already organized separately: Nevermoor, Skyward, Magisterium, Keeper of the Lost Cities, Mysterious Benedict Society, School for Good and Evil, His Dark Materials, Hunger Games, Throne of Glass, Fourth Wing/Empyrean, Gideon, Charlie Bone, Pennyroyal, Tapestry, etc.

### Metaphysics / ontology
- ALICE_BAILEY separated as its own author corpus.
- AGNI_YOGA_ROERICH created and populated with `Agni Yoga` packages, `Психическая энергия` 1–2, `Размышляя над Беспредельностью`, `Через страницы Агни`, `Надземное` 2–3, Roerich compilation, `Приносите радость`, and complete `Грани Агни Йоги` 1–14.
- ASTRAL_PLANE_BODIES: `astral_plane`, `astral_body`, `astralnyye_bitvy`, plus Marcel Louis Forhan / Yram `Иные миры`, vol. 3 (astral projection / evolution of consciousness).
- KABBALAH_ESOTERIC: `kabbalistic_method_complete`.
- RUDOLF_STEINER_ANTHROPOSOPHY: Steiner, `Действие ангелов в астральном теле человека`, GA 182, Zurich, 9 Oct 1918.
- DAN_BAKADZHI_CONSCIOUSNESS: `Книга перемен. Пробуждение` (Perm, 2013).
- Other already separated corpora: Christian angelology, Osho/Rajneesh, Tao/Energy/Chakras, Sacred Geometry, Humi/Synthesis.

## Opaque archive identifications made in this phase

- `92931234.zip` → Gabriel Costa — `За стенкой. История Отиса Ревиаля`.
- `103304218.zip` → Max Glebov — `Объект контроля`.
- `121548868.zip` → Max Glebov — `Сумрак Чужой войны`.
- `118360894.zip` → Max Glebov — `Сеть орбитальной блокады`.
- `114932446.zip` → Max Glebov — `Внешняя агрессия` (Барьер Ориона #5).
- `110868253.zip` → Max Glebov — `Лорд утерянных земель` (Барьер Ориона #4).
- `98631853.zip` → Max Glebov — `Столица мятежной окраины`.
- `99983695.zip` → Max Glebov — `Армада Вторжения`.
- `129977773.zip` → Max Glebov — `Шёпот вакуума` #1.
- `135980327.zip` → Max Glebov — `Шёпот вакуума – 2. Без ложных иллюзий`.
- `106065340.zip` → Max Glebov — `Фактор дисбаланса` (Барьер Ориона #3).
- `118993555.zip` → Stephen King — `После заката`.
- `94475606.zip` → Stephen King — `Последнее дело Гвенди` (#3).
- `92733054.zip` → Sergey Lukyanenko — `Лето волонтёра` (Изменённые #4).
- `19934176.zip` → `Спасти человека. Лучшая фантастика 2016` anthology.
- `71003718.zip` → Sergey Lukyanenko — `Рыцари Сорока Островов`.
- `31006932.zip` → `Пять ночей у Фредди. Серебряные глаза`.
- `91558359.zip` → Gregory Kravinsky — `Код 51. Новая эра`.
- `93958164.zip` → Andrey Lazarenkov — `Мы были в Советском Союзе` (adventure).
- `64854856.fb2.zip` → Kazuo Ishiguro — `Клара и Солнце`; duplicate copy proven byte-identical by SHA-256 and archived.

## Non-library material rehomed

- Large batches of generated PNG/JPG images moved from `19_INBOX_TO_PROCESS` to project/non-library materials; none were deleted.
- Own IVDIVO archives `god_multiverse.zip`, `avatarizatciya.zip`, `ob_atlantide.zip` moved out of external reference-library inbox to project materials.
- Executable/download debris (e.g. PixelSee `.exe`) and incomplete `.crdownload` files separated from reference books.

## Known unresolved items

- `READING_LIKE_A_WRITER (1).pdf` — Drive connector repeatedly blocked the move as uncertain; file remains intact in inbox.
- `The_School_for_Good_and_Evil_The_Ever_Never_Handbook...epub` — Drive connector previously blocked the move; file remains intact in inbox.

## Next actions

1. Continue `19_INBOX_TO_PROCESS` from the currently visible fiction/numeric ZIP layer.
2. Identify remaining numeric ZIPs from internal FB2 metadata in batches.
3. Route named fantasy/YA/SF titles into existing broad shelves or create author/series corpora only when justified.
4. Continue separating metaphysical systems rather than merging them into one undifferentiated esoteric shelf.
5. Run another Drive top-layer audit after each major block to reveal files hidden by list limits.
6. Do not declare ingest complete until the inbox has been exhaustively re-listed and only documented unresolved exceptions remain.
