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
- `[SOURCE BOOK — OPENING ONLY]` — extracted from an explicit fragment; cannot support full-arc claims.
- `[IVDIVO CANON]` — explicitly present in IVDIVO canon.
- `[OUR SYNTHESIS]` — new synthesis/deduction; never silently present as source content.

## Weighting rules

1. Duplicates add zero additional source weight.
2. A fragment cannot support claims about midpoint, climax, ending, or full character arc.
3. One author must not dominate simply because many files were uploaded.
4. Store abstract mechanisms and metadata, not copyrighted book text.
5. Each full mechanism card contains function → emotion → mechanism → abstract formula → IVDIVO use → cliché risk → copying prohibition.
6. Semantic duplicates across authors are clustered before weighting so repetition does not masquerade as stronger evidence.

## Batch 1 completed — 2026-08-13

Deep extraction completed for seven sources: Project Hail Mary, Dark Matter, Recursion, Tinker Tailor Soldier Spy / «Шпион, выйди вон!», Storm Front, The Da Vinci Code, and Red Rising.

- **280** passport parameter rows.
- **105** source-derived mechanism cards.
- **35** IVDIVO / Miss Gallagher crosswalk cards.

## Batch 2 completed — 2026-08-13

Extraction completed for seven further sources: Murderbot / «Отказ всех систем», Dungeon Crawler Carl, «Звёздная кровь 8. Истинный», Ninth House, «Песчаный дьявол», plus fragment-limited opening analysis of «Остаток дня» and «Дозоры 1–3».

- **280** additional passport parameter rows.
- **105** additional source-derived mechanism cards.
- **35** additional IVDIVO crosswalk cards.
- **24** semantic dedupe clusters across Batches 1–2.
- Fragment-limited sources have later-arc fields explicitly blocked as `NOT SUPPORTED — FRAGMENT`.

## Cumulative STORY ENGINE state

- **14** analyzed literary source units.
- **560** passport parameter rows.
- **210** raw source-derived mechanism cards before semantic normalization.
- **70** IVDIVO application/crosswalk cards.
- Human-readable master workbook in Google Drive: `IVDIVO_STORY_ENGINE_v3_Batch2`.
- GitHub machine indexes:
  - `story_engine/passports/source_passport_index_batch1.csv`
  - `story_engine/passports/source_passport_index_batch2.csv`
  - `story_engine/mechanisms/mechanism_index_batch1.csv`
  - `story_engine/mechanisms/mechanism_index_batch2.csv`
  - `story_engine/crosswalk/crosswalk_index_batch1.csv`
  - `story_engine/crosswalk/crosswalk_index_batch2.csv`
  - `story_engine/dedupe/semantic_dedupe_v1.csv`

## Next production stage

1. Batch 3: add the most complementary sources, not more repetitions of the same mechanisms.
2. Normalize Batches 1–2 into a smaller canonical mechanism taxonomy with variants and source support counts.
3. Continue toward **500–1000** high-value raw cards, but weight normalized mechanisms rather than raw count.
4. Cross the normalized engine with IVDIVO canon/world rules.
5. Generate and score the first **30–50** distinct IVDIVO plot architectures.
6. Red-team for repetition, exposition, cliché, continuity and unauthorized copying.

The Google Drive workbook is the primary human-readable analysis; this repository keeps compact machine-friendly indexes and workflow rules.
