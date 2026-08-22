# Local Memory — PL-02

PL-02 uses the same local SQLite database as the PL-00 bootstrap. It adds auditable `memory_records` and `memory_events` tables without requiring a paid service or vector database.

Operations:

- `store` — persist content with kind/source/metadata;
- `search` — bounded text/source/metadata search, ACTIVE records only by default;
- `update` — mutate an ACTIVE record and append an audit event;
- `invalidate` — preserve the record but remove it from normal retrieval with a reason;
- `trace` — return STORE/UPDATE/INVALIDATE history in order.

CLI examples:

```bash
python personal-ai/run.py memory put "fact" --kind evidence --source source-a --id mem-1
python personal-ai/run.py memory search "fact"
python personal-ai/run.py memory update mem-1 "corrected fact"
python personal-ai/run.py memory invalidate mem-1 --reason superseded
python personal-ai/run.py memory trace mem-1
```

Invalidated memory cannot be edited and is excluded from default search. PL-02 is persistence/retrieval infrastructure; PL-03 owns evidence-class semantics and must separately prevent unsupported inference from becoming a verified fact.
