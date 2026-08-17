# IVDIVO SCREEN / MEDIA REFERENCE ROUTING LAW v0.1

Date: 2026-08-17
Status: WORKING LIBRARY CONTROL
Canon effect: NONE

## PURPOSE
Prevent screenplay, tie-in novel, franchise analysis, oral-history and unrelated same-title fiction from being mixed together.

## PRIMARY ROUTING

### `06_SCREENPLAYS_TV_AUDIO`
Use for PRIMARY SCREEN/AUDIO TEXT SOURCES:
- screenplay PDFs;
- teleplay / shooting-script PDFs;
- pilot scripts;
- episode scripts;
- audio-drama scripts;
- production transcripts when they are the closest available primary dialogue/scene source;
- script drafts/revisions.

These sources are studied for:
- scene entry/exit;
- act turns;
- dialogue action;
- ensemble cutting;
- visual causality;
- setup/payoff;
- production scene economy.

### `27_SCREEN_TV_MEDIA_REFERENCE`
Use for SECONDARY / ADAPTED / TRANS-MEDIA SOURCES:
- tie-in novelizations;
- franchise novels;
- oral histories;
- production histories;
- media criticism;
- interviews/case studies;
- franchise guides;
- retrospective analysis.

These are not screenplay authority unless the source itself contains an actual script.

## TITLE COLLISION RULE
Never classify by title alone.

Before routing a title that matches a known franchise, verify at least one of:
- internal EPUB/PDF metadata;
- publisher / copyright holder;
- series/franchise statement;
- cast / episode / script header;
- author relationship to franchise.

Example from Pass 10:
`Charmed` by Erica Ridley is *A Nether-Netherland Romance*, not a Charmed TV tie-in. It belongs in romance/fantasy reference, not Charmed media reference.

## SOURCE AUTHORITY LABELS
Use one of:
- PRIMARY_SCREENPLAY
- PRODUCTION_DRAFT
- TRANSCRIPT_PRIMARY_APPROXIMATION
- LICENSED_TIE_IN
- ADAPTED_NOVELIZATION
- MEDIA_ANALYSIS
- ORAL_HISTORY
- FRANCHISE_GUIDE
- UNRELATED_TITLE_COLLISION
- SCANNED_TEXT_UNAVAILABLE

## DUPLICATE LAW
A similar title/size is not enough for destructive cleanup.
When practical, hash raw files.

Recommended statuses:
- BYTE_IDENTICAL_DUPLICATE — hash match confirmed;
- LIKELY_UPLOAD_DUPLICATE — same work / same size but hash not checked;
- ALTERNATE_DRAFT — meaningful production revision;
- ALTERNATE_SCAN — same source, different scan/extraction quality.

Never collapse different screenplay drafts merely because the episode title matches.

## STUDY LAW
For novels/tie-ins:
REFERENCE -> ABSTRACT MECHANISM -> IVDIVO TRANSFORM.

For screenplays:
SCENE OBJECTIVE -> RESISTANCE -> TURN -> CUT / ACT OUT -> CONSEQUENCE.

Do not copy dialogue, scene sequence, franchise characters or signature inventions.

## CURRENT STRUCTURE
`06_SCREENPLAYS_TV_AUDIO` currently contains dedicated series folders including CHARMED / CHARMED_2018 / SMALLVILLE and other screenplay material.

`27_SCREEN_TV_MEDIA_REFERENCE` is reserved for secondary media reference and tie-in material.

## RESULT
Future screen/media ingestion should route by SOURCE FUNCTION, not title familiarity.
