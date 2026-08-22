# SI-0015 — SMITH post-D01-repair routing telemetry

Status: `REAL_ROUTING_TELEMETRY / NO_PROMOTION / NO_CANON_MUTATION`

This bounded pilot reuses the existing `tools/ivdivo_preexecution_resume_guard.py` and current project-specific SMITH state. It does not create a second freshness classifier.

## Observed current mismatch

At capture time the aggregate router correctly moved away from locked D01 and selected SMITH, but its selected next obligation was still the pre-prose authority/continuity gate. Project-specific SMITH authority has advanced to `ACTIVE_WORKING_PROSE_CH24_PASS_CH25_AUTHORIZED` and requires `DRAFT_CH25_CASCADE_FROM_ACTUAL_CH24_PASS_AND_FRESH_P65_P72_REBASE`.

Expected pre-execution guard outcome before aggregate repair: `STOP_REBASE_REQUIRED`.

## Evidence boundary

- source-grounded production routing evidence;
- not Human Signal;
- not SI-0015 promotion;
- project-specific state outranks aggregate state;
- no Smith story/canon mutation is authorized by this pilot.

## Next gate

1. prove `STOP_REBASE_REQUIRED` on the real current pair;
2. if main has not already rebased the aggregate router, perform a minimal aggregate-only repair;
3. repeat guard and require `EXECUTE` on the same project-specific next obligation;
4. retain historical D01 E96/E97 states as non-current/superseded only.
