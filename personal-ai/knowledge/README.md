# PL-14 Personal Knowledge Search

`PersonalKnowledgeSearch` implements the Production Launch PL-14 acceptance surface:

```bash
python run.py ask "what have we already done about alpha" --project demo
```

The implementation is deliberately bounded and deterministic.

## Search planes

- `PROJECT_STATE` — current `state.json` + `tasks.json` for a project.
- `DECISION_FILE` — persisted `decisions.md` entries.
- PL-02 memory records, source-separated into DOCUMENT / SOURCE / CLAIM / FACT / OUTPUT / EVENT / generic MEMORY.
- PL-13 ingested documents are retrieved through their PL-02 DOCUMENT records and retain their source chain.

## Authority labels

Retrieval never upgrades evidence authority. In particular:

- a PL-03 `AI_INFERENCE` remains `AI_INFERENCE_UNVERIFIED` until an explicit verification event exists;
- a verified claim remains a claim;
- only a PL-03 derived FACT whose metadata explicitly says `record_role=VERIFIED_FACT` and `verified_state=VERIFIED` is labelled `VERIFIED_FACT`;
- DOCUMENT/SOURCE presence is labelled source material, not truth verification;
- project state and user decisions have their own source classes.

## Safety / integrity invariants

- search is lexical only; no embedding/semantic-search capability is claimed;
- project-scoped queries exclude records and files from other projects;
- invalidated PL-02 records are excluded;
- no-hit returns `UNKNOWN`, never fabricated content;
- results include source refs and memory provenance-chain IDs where available;
- search results are persisted under `runtime/knowledge_search/`, outside searchable memory, to avoid self-feedback loops;
- search does not independently verify source correctness, market truth, legal truth, or technical truth.
