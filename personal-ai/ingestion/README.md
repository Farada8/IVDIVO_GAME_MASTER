# PL-13 File Ingestion

PL-13 provides bounded, deterministic ingestion for local files. It does not claim OCR, PDF understanding, arbitrary binary parsing, embedding generation, or semantic search.

## Supported inputs

- `.txt` -> normalized UTF-8 text
- `.md` -> normalized UTF-8 Markdown
- `.json` -> parsed and deterministic canonical JSON representation
- `.csv` -> validated UTF-8 CSV with row/column metadata

Inputs must be regular non-symlink files, non-empty, valid UTF-8, and at most 10 MiB. Unsupported extensions fail closed.

## Ingestion contract

For each accepted input PL-13:

1. reads the raw bytes once and records byte size;
2. computes raw SHA-256 over those exact bytes;
3. creates a deterministic text representation and representation SHA-256;
4. stores the exact raw bytes in a content-addressed object path under `runtime/ingestion/objects/` and verifies the stored checksum;
5. persists a PL-02 `SOURCE` record for provenance;
6. persists a PL-02 `DOCUMENT` record linked to that source;
7. persists a JSON manifest under `runtime/ingestion/manifests/<project>/`;
8. returns the existing document/source identities instead of creating duplicates when the same project ingests the same raw content through the same handler again.

The raw object store is global by raw SHA-256, so identical bytes can be physically shared across projects. PL-02 SOURCE/DOCUMENT identities remain project-specific so provenance is not merged across projects.

The ingestion fingerprint includes raw SHA-256, extension and representation handler. Therefore identical bytes presented under semantically different supported handlers can share the raw object but do not collapse into one document representation.

## CLI

```bash
python personal-ai/run.py --home /tmp/pai ingest file PROJECT ./reference.md
```

## Evidence boundary

PL-13 proves hashing, deterministic representation, content-addressed raw persistence, project-scoped provenance and deduplication for the explicitly supported local text formats only. It does not prove that document content is true, complete, safe, useful, semantically understood, or ready for retrieval. PL-14 owns personal knowledge search.
