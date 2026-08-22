# IVDIVO — BOOK INTELLIGENCE ENGINE v1.0 — COMPATIBILITY ROUTER

**Status:** SUPERSEDED FOR CURRENT ROUTING BY v1.1  
**Updated:** 2026-08-22  
**Historical v1.0 blob:** `424105eecb7dc9b6d7b44f7ff3a3034dbd7b3a0a`

This legacy path is intentionally retained because older Narrative/System routers may still reference it.

## Current authority
Use, in order:
1. `CURRENT_BOOK_INTELLIGENCE_ENGINE_STATE.json`;
2. `BOOK_INTELLIGENCE_ENGINE/00_BOOK_INTELLIGENCE_ENGINE_CANON_v1.1.md`;
3. `BOOK_INTELLIGENCE_ENGINE/01_SOURCE_LIBRARY_MANIFEST_v1.1.json`;
4. `BOOK_INTELLIGENCE_ENGINE/02_BOOK_INTELLIGENCE_SCHEMAS_v1.1.json`;
5. `BOOK_INTELLIGENCE_ENGINE/05_ALL_ENGINE_ADAPTER_AND_INTEGRATION_CONTRACT_v1.1.md`;
6. `tools/ivdivo_book_intelligence.py`.

## Migration boundary
Do not continue using the v1.0 linear source lifecycle as current authority.

Current source state is orthogonal:
`integrity_status + read_coverage + extraction_stage`.

`EXTRACTION_STAGE DOES NOT IMPLY FULL_READ`.

Engineering verification and real validation are separate evidence classes. Bidirectional traceability is required for promotion.

Historical v1.0 content remains recoverable from Git history/blob provenance; replacing this current path with a compatibility router does not erase history.

**ROUTE TO v1.1; DO NOT REINTRODUCE THE LINEAR LIFECYCLE.**