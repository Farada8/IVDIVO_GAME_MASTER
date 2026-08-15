# IVDIVO LIBRARY INGEST PROTOCOL

## Goal
Convert raw books into retrievable, copyright-safe production intelligence for Writers’ Room without losing the original source.

## Intake
All new files first enter Google Drive `19_INBOX_TO_PROCESS`.

## Stage 1 — Identity
Assign `source_id`; verify title, author, series, edition where possible, language, file name and original format.

## Stage 2 — Integrity
Classify one of:
- LIKELY_FULL
- FRAGMENT_EXPLICIT
- COLLECTION_UNVERIFIED
- UNKNOWN_MEDIUM
- SCANNED_TEXT_UNAVAILABLE
- PROJECT_TEXT
- TO_VERIFY

Record duplicate groups. Duplicates never increase evidentiary or creative weight.

## Stage 3 — Searchability
If the source is a heavy/image PDF or otherwise poorly searchable, retain the original and create a searchable OCR/TXT/MD mirror under `18_OCR_TEXT_MIRRORS`. Never discard the original scan after OCR.

## Stage 4 — Functional routing
Assign a primary Writers’ Room role and optional secondary roles: story architecture, character, dialogue, YA, youth psychology, relationships, mystery, thriller, institutions, sociology, worldbuilding, science/technology, philosophy, horror, prose, screenwriting, etc.

## Stage 5 — Rank
- S — core, repeatedly reopened.
- A — strong specialist.
- B — useful for specific problems.
- REFERENCE — occasional research.
- HOLD — low priority until a matching problem appears.

## Stage 6 — Extraction
Create/update a Book Card. Extract abstract mechanisms, never chunks of copyrighted prose. Mechanism schema:

`ID → mechanism → function → trigger → sequence → effect → failure risk → IVDIVO use → DO NOT COPY`.

## Stage 7 — Registry
Update `SOURCE_REGISTRY_SCHEMA.csv` or its future live registry implementation with Drive URL, OCR mirror, rank, functions, completeness, Book Card path, active-shelf state and processing status.

## Stage 8 — Move from inbox
After classification, move the original from `19_INBOX_TO_PROCESS` to the best category folder. Multi-role books have one canonical home; secondary roles exist in metadata rather than duplicated copies.

## Stage 9 — Active Shelf decision
Only S-tier craft and sources required for current production belong in ChatGPT Library / `21_ACTIVE_SHELF`. Do not keep every processed original in the active cache.

## Stage 10 — Writers’ Room retrieval
For a concrete task, query the registry/mechanism bank first. Select 3–10 high-value sources, then reopen originals from Drive only when the Book Card’s return-to-original trigger fires.

## Stage 11 — QA
Red Team checks: source integrity, duplicate weighting, overgeneralization from fragments, accidental imitation, unsupported claims, and whether the extracted mechanism actually improves a specific IVDIVO production problem.
