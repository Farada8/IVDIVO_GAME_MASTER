# PL-14 Personal Knowledge Search

`ask` is a project-local retrieval command. It does not ask an LLM to invent an answer.

## Search mode

`LITERAL_CASE_INSENSITIVE_SUBSTRING`

No embeddings or semantic search are claimed.

## Source-separated groups

- `project_state` — `state.json` and matching tasks from `tasks.json`;
- `documents` — active PL-02 `DOCUMENT` and `SOURCE` records for the selected project;
- `decisions` — matching sections from `decisions.md`, active `DECISION` memory, and `USER_DECISION` claims;
- `memory` — other active project-scoped memory records.

Each hit retains its origin, id/path, kind/status and provenance fields where available.

## Safety/integrity rules

- `project_id` is mandatory; cross-project search is not performed;
- invalidated memory is excluded;
- missing evidence returns `NO_HIT` + `UNKNOWN`;
- retrieval does not promote source authority or convert evidence into VERIFIED_FACT;
- reports are persisted under `artifacts/knowledge-search/` for audit;
- no web search, OCR, embeddings, model inference or truth verification occurs in PL-14.

## CLI

```bash
python personal-ai/ask.py --home /path/to/home PROJECT_ID "query text"
```

The standalone executable is intentional: it avoids overwriting the fast-moving shared `run.py` router while parallel production work is active. A future bounded integration may expose the same service through `run.py` without changing the PL-14 search semantics.

The output is structured evidence, not a generated factual answer.
