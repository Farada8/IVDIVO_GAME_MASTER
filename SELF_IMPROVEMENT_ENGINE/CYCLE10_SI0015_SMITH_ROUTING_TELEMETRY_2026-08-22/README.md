# SI-0015 — SMITH post-D01-repair routing telemetry

Status: `REAL_ROUTING_TELEMETRY / NO_PROMOTION / NO_CANON_MUTATION`

This bounded pilot reuses `tools/ivdivo_preexecution_resume_guard.py` and current project-specific SMITH state. It does not create a second freshness classifier.

## Real production findings
The aggregate router selects SMITH but lags the project-specific state in two ways:
- aggregate project id `IVDIVO_BOOK_3_SMITH_FULL_NOVEL` vs project state id `IVDIVO_BOOK_3_SMITH`;
- aggregate next obligation still describes the pre-prose authority/continuity gate while project-specific SMITH state is `ACTIVE_WORKING_PROSE_CH24_PASS_CH25_AUTHORIZED` with next obligation `DRAFT_CH25_CASCADE_FROM_ACTUAL_CH24_PASS_AND_FRESH_P65_P72_REBASE`.

The real guard therefore first fails closed as `PROJECT_NOT_ACTIVE`. After only the id is aligned, it must surface the second defect as `STOP_REBASE_REQUIRED`.

A separate generic compatibility defect was also found: the guard did not read project-level `next_obligation`, a field used by the real SMITH state. The bounded fix adds that field without changing authority ordering.

Evidence boundary: source-grounded production routing evidence only; not Human Signal; not SI-0015 promotion; no Smith story/canon mutation.
