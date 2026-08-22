# Engineering Integration Contract v0.1

Date: 2026-08-22
Scope: Personal AI / Business / Books / Projects production launch
Authority effect: NONE on current Self-Improvement promotion state

## 1. Core truth conditions

1. `PROMPT_EXECUTED != IMPLEMENTATION_DONE`.
2. `FILE_CREATED != FEATURE_WORKS`.
3. `TEST_COUNT != QUALITY_PROOF`.
4. `AI_OUTPUT != VERIFIED_FACT`.
5. `WRITE_CLAIM != PERSISTED_ARTIFACT`.
6. `DISCOVERED_RELEVANCE != FRONTIER_SWITCH_AUTHORITY`.
7. `DONE_VERIFIED` requires implementation, test/readback and persisted evidence.

## 2. Current authority

- Preserve Self-Improvement v2 as `VERIFIED_CURRENT`.
- This pack is an additive production backlog and does not promote v3 or assign a new SI identifier.
- Existing project/story/audio/business authority is not rewritten by this pack.

## 3. Execution contract per run card

Every card must declare and persist:
- `card_id`
- objective
- input(s)
- files changed/created
- executable command when applicable
- expected output
- tests/fixtures
- actual test result
- blocker(s)
- artifact/readback evidence
- state transition
- next admissible card(s)

If executable code cannot be created or run, state must be `DESIGN_ONLY` or `BLOCKED`, never `DONE_VERIFIED`.

## 4. Wave discipline

### Wave 1 — Foundation
PL-00, PL-01, PL-02, PL-04, PL-05, PL-11.

Exit gate: a real `python run.py` path exists and performs at least one persisted action; project state, memory, provider mock, bounded agent and benchmark runner have passing required tests.

### Wave 2 — Real production
PL-06, PL-07, PL-08, PL-09, PL-13, PL-14.

Exit gate: one business artifact path and one book artifact/check path run against persisted state; ingestion/search are source-aware.

### Wave 3 — Reliability
PL-03, PL-10, PL-12, PL-16, PL-17, PL-18.

Exit gate: provenance, independent review, change control, backup/restore, security and cost attribution have deterministic fixtures.

### Wave 4 — Optimization
PL-15, PL-19, PL-20.

Exit gate: current-state control panel and model router operate from real state; Production Gate reports FATAL/MAJOR accurately.

### Wave 5 — Real pilots + release
PL-21, PL-22, PL-23, PL-24.

Exit gate: real business and book pilots exist; failures are analyzed; release v0.1 is permitted only after critical regression gates pass.

## 5. Acceptance and regression

Before any change is accepted:

`BASELINE -> CANDIDATE -> TEST -> BENCHMARK -> REGRESSION -> DECISION -> PERSIST -> READBACK`

Minimum fail-closed rules:
- any FATAL => reject/no release;
- any unresolved security secret leak/path traversal/destructive action => reject;
- critical regression > 0 => reject;
- missing required readback => not verified;
- unknown measurements remain UNKNOWN/null, never fabricated as zero/pass.

## 6. Human/market/provider evidence boundary

No simulated customer response, provider behavior, market outcome, tender decision, payment, literary reception or other external evidence may satisfy a production gate. Synthetic fixtures may validate software mechanics only.

## 7. Frontier law

Execution begins at `PL-00` unless persisted evidence proves that its requirements already exist in current authority and tests. If so, reconcile and mark with evidence rather than redoing work.

A newly discovered sibling project or file may inform the current card but may not silently switch the active project/frontier.

## 8. Anti-bloat rule

Do not generate another architecture document as a substitute for the current run card. The smallest executable implementation that proves the next gate is preferred.

## 9. Release naming

Until PL-24 passes, use `v0.x candidate` / `DESIGN_ONLY` / `PRODUCTION_BACKLOG_READY` as appropriate. Do not claim `production-ready`, `finished`, or equivalent while FATAL/MAJOR gates remain.