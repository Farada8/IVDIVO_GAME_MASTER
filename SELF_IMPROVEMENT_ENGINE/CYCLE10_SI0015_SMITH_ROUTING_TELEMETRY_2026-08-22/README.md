# SI-0015 — SMITH post-D01-repair routing telemetry

Status: `REAL_ROUTING_TELEMETRY / NO_PROMOTION / NO_CANON_MUTATION`

This bounded pilot reuses `tools/ivdivo_preexecution_resume_guard.py` and current project-specific SMITH state. It does not create a second freshness classifier.

## Observed mismatch at fresh-main capture
The aggregate router correctly moved away from locked D01 and selected SMITH, but its `next_unblocked_obligation` still describes pre-prose authority/continuity reconciliation. Project-specific SMITH state is already `ACTIVE_WORKING_PROSE_CH24_PASS_CH25_AUTHORIZED` and requires `DRAFT_CH25_CASCADE_FROM_ACTUAL_CH24_PASS_AND_FRESH_P65_P72_REBASE`.

Expected real pre-execution decision before aggregate rebase: `STOP_REBASE_REQUIRED`.

## Evidence boundary
- source-grounded production routing evidence;
- not Human Signal;
- not SI-0015 promotion;
- project-specific state outranks aggregate state;
- no Smith story/canon mutation authorized.

## Next gate
1. prove real guard returns STOP_REBASE_REQUIRED;
2. if aggregate router is still stale, perform aggregate-only bounded repair;
3. rerun guard and require EXECUTE on the project-specific CH25 next obligation;
4. retain old D01 E96/E97 as historical/superseded only.
