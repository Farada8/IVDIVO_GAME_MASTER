# IVDIVO Library Architecture

## Purpose

Google Drive is the master store for original books and searchable mirrors. ChatGPT Library is an active working shelf only. GitHub stores the machine-readable intelligence layer: source registry, book cards, extracted abstract mechanisms, routing rules, migration state, and Writers’ Room production standards.

## Storage layers

1. **Google Drive** — originals, scans, EPUB/PDF/DOC/FB2, OCR/TXT/MD mirrors.
2. **GitHub** — metadata, provenance, source passports, book cards, mechanism banks, routing rules.
3. **ChatGPT Library** — S-tier craft plus the current 20–100 active sources required by the present book/arc.

## Drive root

`IVDIVO_LIBRARY`

Folders:

- `00_INDEX_AND_CONTROL`
- `01_WRITING_CRAFT`
- `02_YA_AND_COMING_OF_AGE`
- `03_SF_AND_FUTURES`
- `04_URBAN_FANTASY_SUPERNATURAL`
- `05_MYSTERY_THRILLER_ESPIONAGE`
- `06_SCREENPLAYS_TV_AUDIO`
- `07_CHARACTER_PSYCHOLOGY`
- `08_YOUTH_PSYCHOLOGY`
- `09_RELATIONSHIPS_ROMANCE`
- `10_SOCIOLOGY_ANTHROPOLOGY`
- `11_PHILOSOPHY_CONSCIOUSNESS`
- `12_AI_ROBOTICS_NEURO_BIO`
- `13_WORLD_HISTORY_INSTITUTIONS`
- `14_HORROR_DREAD`
- `15_COMICS_MANGA`
- `16_REFERENCE_NOVELS`
- `17_WORLD_SOURCE_METAPHYSICS`
- `18_OCR_TEXT_MIRRORS`
- `19_INBOX_TO_PROCESS`
- `20_ARCHIVE_DUPLICATES`
- `21_ACTIVE_SHELF`

## Existing baseline

The pre-migration IVDIVO Story Engine audit tracked 171 files: 100 likely full texts, 40 explicit fragments, 12 collections, 2 scanned/text-unavailable items and 3 duplicate groups. Migration must preserve those integrity statuses and must not reset source provenance.

## Core rule

A book is not useful merely because it is stored. A processed source must have a source ID, integrity status, Drive location, functional role, rank, extraction targets, copyright-safe mechanism notes and return-to-original triggers.
