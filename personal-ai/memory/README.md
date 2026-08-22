# Local Memory — PL-02

PL-02 uses the same local SQLite database as the PL-00 bootstrap.

Two interfaces coexist intentionally:

1. `MemoryStore` — compatibility layer for the already-merged PL-02 CLI (`put/search/update/invalidate/trace`).
2. `VersionedMemory` — strict implementation of the original PL-02 contract with physical `documents`, `facts`, `decisions`, `sources`, `outputs`, and `events` tables, immutable versions, content hashes, confidence, source IDs, and traceable provenance.

The required PL-02 physical table set is therefore:

- `projects`
- `tasks`
- `documents`
- `facts`
- `decisions`
- `sources`
- `outputs`
- `events`

Every VersionedMemory record stores: logical ID, version, project ID when applicable, UTC timestamp, source, optional source record ID, confidence where supplied, status, content, SHA-256 content hash, current-version flag, and invalidation metadata.

Strict operations:

- `store` — create version 1 and reject accidental overwrite;
- `search` — search only current records; INVALIDATED is excluded unless explicitly requested;
- `update` — create a new version while preserving the old content/hash;
- `invalidate` — create an INVALIDATED audit version rather than deleting history;
- `trace_source` — follow record -> source record -> parent source chain with missing/cycle/truncation reporting;
- `versions` — return complete immutable history for one logical record.

Compatibility CLI remains available:

```bash
python personal-ai/run.py memory put "fact" --kind evidence --source source-a --id mem-1
python personal-ai/run.py memory search "fact"
python personal-ai/run.py memory update mem-1 "corrected fact"
python personal-ai/run.py memory invalidate mem-1 --reason superseded
python personal-ai/run.py memory trace mem-1
```

The strict VersionedMemory API is exercised directly in regression tests. The original PL-02 prompt requires a CLI search path, not a second incompatible CLI grammar, so the compatibility search path remains canonical for command-line use.

PL-02 is persistence/retrieval infrastructure only. Storing a record does **not** turn an inference into a verified fact. Evidence-class semantics and the `AI_INFERENCE -> VERIFIED_FACT` firewall belong to PL-03.
