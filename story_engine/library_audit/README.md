# IVDIVO STORY ENGINE — Library Audit v1

Initial source audit for the IVDIVO fiction/audio story engine.

## Current corpus

- Files audited: **171**
- Explicit fragments / demos: **40**
- Likely full texts: **100**
- Collections / omnibus files requiring split: **12**
- Scanned PDFs with unusable local text layer: **2**
- Exact duplicate groups detected: **3**

## Completeness labels

- `LIKELY_FULL` — substantial text, no explicit demo marker. This is a heuristic, not a guarantee about the edition.
- `FRAGMENT_EXPLICIT` — the text itself contains an ознакомительный/demo marker. Use only for opening mechanics.
- `COLLECTION_UNVERIFIED` — anthology/omnibus; split into component works before full structural analysis.
- `SCANNED_TEXT_UNAVAILABLE` — pages exist visually, but local text extraction is insufficient; use multimodal/file_search.
- `UNKNOWN_MEDIUM` / `SHORT_OR_FRAGMENT_UNKNOWN` — insufficient evidence to infer completeness.
- `PROJECT_TEXT` — original IVDIVO story/project material.

## Evidence labels

- `[SOURCE BOOK]` — directly extracted from an uploaded literary source.
- `[IVDIVO CANON]` — explicitly present in IVDIVO canon.
- `[OUR SYNTHESIS]` — new synthesis/deduction; never silently present as source content.

## Weighting rules

1. Duplicates add zero additional source weight.
2. A fragment cannot support claims about midpoint, climax, ending, or full character arc.
3. One author must not dominate simply because many files were uploaded.
4. Store abstract mechanisms and metadata, not copyrighted book text.
5. Each full mechanism card contains function → emotion → mechanism → abstract formula → IVDIVO use → cliché risk → copying prohibition.

## Batch 1 completed — 2026-08-13

Deep extraction completed for seven sources: Project Hail Mary, Dark Matter, Recursion, Tinker Tailor Soldier Spy / «Шпион, выйди вон!», Storm Front, The Da Vinci Code, and Red Rising.

- **280** passport parameter rows: 7 sources × 40 parameters.
- **105** reusable source-derived mechanism cards: 15 per source.
- **35** initial crosswalk cards mapping mechanisms into IVDIVO / Miss Gallagher.
- Full human-readable workbook is stored in the project Google Drive as `IVDIVO_STORY_ENGINE_v2_Batch1`.
- GitHub keeps compact machine-readable indexes:
  - `story_engine/passports/source_passport_index_batch1.csv`
  - `story_engine/mechanisms/mechanism_index_batch1.csv`
  - `story_engine/crosswalk/crosswalk_index_batch1.csv`

## Next production stage

1. Batch 2: Murderbot, Dungeon Crawler Carl, Ishiguro fragments, Lukyanenko fragments, Prokofiev, Ninth House and Rollins.
2. Deduplicate semantically equivalent mechanisms across authors.
3. Expand the bank toward **500–1000** high-value mechanism cards.
4. Cross with IVDIVO canon/world rules.
5. Generate and score the first **30–50** distinct IVDIVO plot architectures.
6. Red-team for repetition, exposition, cliché, continuity and unauthorized copying.

The Google Drive workbook is the primary human-readable analysis; this repository keeps compact machine-friendly indexes and workflow rules.
