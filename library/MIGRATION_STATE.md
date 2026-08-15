# IVDIVO LIBRARY MIGRATION STATE

**Status:** ACTIVE MIGRATION  
**Started:** 2026-08-16  
**Master store:** Google Drive `IVDIVO_LIBRARY`  
**Intelligence store:** `Farada8/IVDIVO_GAME_MASTER/library/`

## Baseline inherited from Story Engine v4.1

- Files audited: 171
- Likely full texts: 100
- Explicit fragments/demos: 40
- Collections: 12
- Scanned/text unavailable: 2
- Duplicate groups: 3

These figures are inherited from the existing audit and must not be interpreted as the final Drive migration count.

## Migration phases

### Phase A — Infrastructure
- [x] Create Drive root.
- [x] Create category folders.
- [x] Create index/control, templates, migration logs, OCR mirrors, inbox, archive and active-shelf folders.
- [x] Create GitHub library architecture.
- [x] Create source registry schema.
- [x] Create Book Card template.
- [x] Create ingest protocol.
- [x] Create Active Shelf policy.

### Phase B — Original-file transfer
- [ ] Bulk upload existing ChatGPT/File Library originals to Drive.
- [ ] Confirm each Drive original against inherited audit metadata.
- [ ] Preserve duplicates until verified; then move redundant copies to `20_ARCHIVE_DUPLICATES`.

### Phase C — Searchability
- [ ] Detect scan/image PDFs.
- [ ] Create OCR/text mirrors where needed.
- [ ] Link mirror URLs in source registry.

### Phase D — Intelligence migration
- [ ] Import/reconcile the 171-file Story Engine audit into the live registry.
- [ ] Reconcile post-v4.1 books added after the audit.
- [ ] Generate/update Book Cards.
- [ ] Route mechanism cards into canonical banks.

### Phase E — Active shelf
- [ ] Select persistent S-tier sources.
- [ ] Select current Book 1 / YA active set.
- [ ] Remove unnecessary originals from ChatGPT Library only after Drive copy + registry + Book Card are verified.

## Current blocker
ChatGPT/File Library search references do not expose raw file bytes/file_uri to the Google Drive upload action in the current connector path. Therefore I can prepare, index and operate the Drive archive, but I cannot directly bulk-copy historical ChatGPT Library binaries into Drive from those search references. The manual step is: upload the original files into `19_INBOX_TO_PROCESS` (or appropriate category folders). After they are in Drive, the rest of the routing, metadata reconciliation and analysis can be automated through the connected Drive tools.
