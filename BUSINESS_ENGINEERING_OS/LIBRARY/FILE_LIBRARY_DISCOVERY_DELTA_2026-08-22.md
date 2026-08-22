# BUSINESS LIBRARY — FILE LIBRARY DISCOVERY DELTA — 2026-08-22

Status: `DISCOVERY_DELTA / NO_SILENT_RAW_PROMOTION`

Current physical RAW authority remains:
- private Google Drive RAW folder: `1X6mo94Qo103HheyDry4P3dcQkv5qZg6N`
- physical files: 78
- valid files: 68
- unique valid byte hashes: 58

## Newly reconciled File Library discovery

### FLD-2026-08-22-001
- title: `international-human-resource-management-5nbsped-1398603554-9781398603554_compress.pdf`
- File Library ref: `file_0000000043d881f4b8cc4b7670fa7464`
- domain: `ORGANIZATION / PEOPLE / INTERNATIONAL HRM`
- status: `FILE_LIBRARY_REFERENCE_ONLY`
- raw Drive file id: `null`
- raw byte hash: `null`
- canonical work/edition identity: `PENDING_PASSPORT`
- evidence use: `REFERENCE_ONLY`
- public GitHub raw binary allowed: `false`

The current connector can discover/read this File Library source but does not expose a truthful binary-transfer path from File Library into the private RAW Drive folder. Therefore this record does **not** increment the 78-file physical RAW count. If a future connector/import step produces a Drive file id plus byte hash, promote through the normal Source Passport + duplicate/edition reconciliation protocol.

## Boundary law

`FILE_LIBRARY_REFERENCE != RAW_DURABLE`

A source becomes `RAW_DURABLE` only when a private Drive file id and byte hash are both present and read back. Raw copyrighted books are never copied into public GitHub; GitHub stores metadata, hashes, source passports, mechanisms, contracts, tests and pointers only.

## Domain filter

Recent File Library also contains IVDIVO story-engine files and heritage/design images. Those are not silently added to the Business RAW library because they belong to other production domains. Cross-domain use requires an explicit Source Passport and a concrete business mechanism/use case.
