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

## Evidence labels for future mechanism cards

- `[SOURCE BOOK]` — directly extracted from an uploaded literary source.
- `[IVDIVO CANON]` — explicitly present in IVDIVO canon.
- `[OUR SYNTHESIS]` — new synthesis/deduction; never silently present as source content.

## Weighting rules

1. Duplicates add zero additional source weight.
2. A fragment cannot support claims about midpoint, climax, ending, or full character arc.
3. One author must not dominate simply because many files were uploaded.
4. Store abstract mechanisms and metadata, not copyrighted book text.
5. Each mechanism card should contain: function → emotion → mechanism → abstract formula → IVDIVO use → cliché risk → copying prohibition.

## Next production stage

1. Build 40-parameter passports for A-tier sources.
2. Extract 500–1000 reusable story-mechanism cards.
3. Cross them with IVDIVO canon/world rules.
4. Generate 30–50 distinct plot architectures.
5. Red-team for repetition, exposition, cliché, continuity, and unauthorized copying.

The Google Drive workbook is the primary human-readable audit; this repository keeps the machine-friendly audit and workflow rules.
