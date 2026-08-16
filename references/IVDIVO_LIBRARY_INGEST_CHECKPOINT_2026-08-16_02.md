# IVDIVO Library Ingest Checkpoint — 2026-08-16 / 02

Status: WORKING / INGEST CHECKPOINT

## Drive state

- `19_INBOX_TO_PROCESS` is empty at this checkpoint.
- All files visible in the ingest queue have been routed into genre, author, series, project-material, fragment, or duplicate corpora.
- No file was deleted as part of the ingest cleanup; confirmed duplicates were moved to `20_ARCHIVE_DUPLICATES`.

## Quality controls applied

- Numeric ZIP archives were classified from internal FB2 metadata (title, author, genres, sequence/number) rather than guessed from filenames.
- Suspected duplicates were not archived from filename similarity alone.
- `READING_LIKE_A_WRITER (1).pdf` was SHA-256 matched against the retained `READING_LIKE_A_WRITER.pdf` and confirmed byte-identical before archiving.
- `64854856.fb2 (1).zip` was previously confirmed byte-identical to its retained counterpart before duplicate archiving.
- Small/incomplete Ishiguro TXT archives (`Не отпускай меня`, `Погребённый великан`) were separated into `23_FRAGMENTS_PARTIAL` rather than treated as full reference texts.

## Major corpora consolidated during this pass

Metaphysical/reference:
- ALICE_BAILEY
- AGNI_YOGA_ROERICH, including `Грани Агни Йоги` 1–14
- RUDOLF_STEINER_ANTHROPOSOPHY
- KABBALAH_ESOTERIC
- ASTRAL_PLANE_BODIES
- JOHN_KEHO_CONSCIOUSNESS
- DAN_BAKADZHI_CONSCIOUSNESS
- OSHO_RAJNEESH
- ANGEL / Christian hierarchy references separated from Bailey/theosophy

Fiction/craft:
- DOZORY and DOZORY_SHARED_UNIVERSE separated
- SERGEY_LUKYANENKO_SF and other urban-fantasy lines separated from DOZORY
- MAX_GLEBOV_SF expanded from previously opaque numeric ZIPs
- VICTOR_PELEVIN corpus established
- JAMES_ROLLINS split into SIGMA_FORCE / FANTASY / OTHER
- MARTHA_WELLS split into MURDERBOT / RAKSURA / other fantasy
- KAZUO_ISHIGURO split into SPECULATIVE / LITERARY, with fragments quarantined
- THRONE_OF_GLASS full available cycle collected
- EMPYREAN_FOURTH_WING, CHARLIE_BONE, GIDEON, HUNGER_GAMES, SCHOOL_FOR_GOOD_AND_EVIL and other YA/fantasy corpora normalized
- JOHN_LE_CARRE_SMILEY, MILLENNIUM, ROBERT_LANGDON, STEPHEN_KING_FICTION and other mystery/horror corpora normalized
- `anatomiya_istorii.zip` routed to Truby/story-structure craft instead of fiction

## New genre/utility layers created where needed

- `08_FANTASY_REFERENCE`
- `09_ADVENTURE_HISTORICAL_FICTION`
- `10_CONTEMPORARY_LITERARY_FICTION`
- `23_FRAGMENTS_PARTIAL`
- SF anthologies separated from main author/series canon

## Final files removed from inbox in the closing batch

- Anastasia Shelest — `Великая Библиотека` → urban fantasy
- Anna Shtak — `Тени Штарнбергского озера` → horror
- Lee Redford — `Жёлтый глаз` → SF/speculative romance
- Jean Paiva — `Фактор Лилит` → thriller/detective
- Andrea Portes — `Ускользающая красавица` → YA fantasy
- Denis Lukyanov — `Человек человеку` → contemporary horror
- Elena Prudnikova — `Песня скорпионов` / `Хартия мирного неба #1` → SF
- Amy Liou — `Алый трон` / `Ложная богиня #1` → fantasy
- Yulia Arver — `Диспноэ` → fantasy
- Katrin Tordashi — `Огненное перо` / `Птицы Парижа #1` → children/YA reference

## Production consequence

The library is now materially better suited to the IVDIVO Writers’ Room because source retrieval can distinguish:
- story craft vs fiction,
- main-series canon vs shared-universe anthology,
- full text vs fragment,
- metaphysical systems that should not be collapsed into one ontology,
- YA/children mechanics vs adult genre fiction,
- SF/social-SF vs urban fantasy vs horror vs thriller.

Next useful stage is not more inbox cleanup; it is corpus indexing and mechanism extraction for Writers’ Room use (story engine, character, youth psychology, relationships, mystery, institutional conflict, AI/synthetic life, metaphysical ontology, and dialogue).