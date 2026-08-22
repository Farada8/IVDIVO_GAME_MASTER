# Next Frontier after PL-07 — PL-14 Personal Knowledge Search

PL-14 is dependency-admissible because PL-02 Local Memory and PL-13 File Ingestion are DONE_VERIFIED.

Base acceptance: `ask command retrieves project/docs/decisions/state with source separation`.

Required pre-implementation laws:
- retrieval is not truth verification;
- project state, ingested documents, explicit user decisions and generic memory remain distinguishable source classes;
- cross-project leakage fails closed;
- invalidated/superseded memory does not surface as current without an explicit historical label;
- no-hit/missing evidence returns UNKNOWN/no result rather than invented synthesis;
- source IDs and project IDs persist through ranking/output;
- semantic embeddings/vector search are not claimed unless actually implemented and tested;
- exact deterministic lexical/index retrieval is acceptable as the first bounded implementation;
- answer synthesis may summarize retrieved records but may not upgrade their evidence status.

This file is a handoff, not a PL-14 implementation or DONE claim.
