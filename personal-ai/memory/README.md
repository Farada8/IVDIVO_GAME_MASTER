# Local Memory — PL-02

PL-02 adds durable, versioned SQLite knowledge storage to the `personal-ai` runtime.

Required tables are present in one SQLite database: `projects`, `tasks`, `documents`, `facts`, `decisions`, `sources`, `outputs`, `events`. PL-00/PL-01 remain authoritative for operational project/task state; PL-02 owns the six knowledge/evidence tables.

Each PL-02 knowledge record persists: logical ID, version, project ID when known, timestamp, source, optional source record ID, confidence, status, content, SHA-256 content hash, current-version flag, and invalidation metadata.

Operations:

```text
STORE -> new logical record/version 1
SEARCH -> current records, invalidated records excluded by default
UPDATE -> new immutable content version; prior content remains readable
INVALIDATE -> new INVALIDATED version; prior versions remain readable
TRACE_SOURCE -> record -> source record -> parent source ...
VERSIONS -> complete version history for one logical record
```

CLI examples:

```bash
python personal-ai/run.py memory store sources src-1 "Client interview" --source user
python personal-ai/run.py memory store facts f-1 "Client prefers written quotes" --source interview --source-id src-1 --confidence 0.9
python personal-ai/run.py memory search "written quotes" --entity facts
python personal-ai/run.py memory update facts f-1 --content "Client prefers itemized written quotes"
python personal-ai/run.py memory versions facts f-1
python personal-ai/run.py memory trace facts f-1
python personal-ai/run.py memory invalidate facts f-1 --reason "client changed preference"
```

This is persistent memory, not model-weight training. It must not convert an AI inference into a verified fact merely because it was stored; the stricter evidence-type firewall belongs to PL-03.