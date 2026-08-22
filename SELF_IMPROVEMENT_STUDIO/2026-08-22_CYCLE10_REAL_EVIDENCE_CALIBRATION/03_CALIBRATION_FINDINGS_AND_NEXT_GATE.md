# CYCLE10 — CALIBRATION FINDINGS + NEXT GATE

## Real evidence consumed
Cycle10 used persisted recovery records, not a synthetic fixture.

Observed:
- genuine interruption events = 1;
- recovered project slices = 2;
- false resumes = 0;
- explicitly avoided duplicate work units = 1;
- rejected wrong-resume paths in Business slice = 4;
- stale Business frontier was replaced by a newer merged authority before qualification continued.

Not observed/measured:
- operator minutes;
- tool calls attributable only to recovery;
- minutes saved;
- money saved;
- productivity percentage;
- probability/cost of the counterfactual wrong route.

These remain null.

## Important distinction discovered
`rejected wrong path` is not the same quantity as `genuine interruption event` and is not automatically an independent `failure avoided`.

One raw interruption produced multiple route checks across two project slices. The event count stays one. Project diversity becomes two. The four Business route rejections are decision evidence inside the same recovery, not four new incidents.

## Self-Improvement value now demonstrable
We can make two bounded observed claims:
1. the persisted-authority recovery path prevented one explicitly recorded duplicate Cycle8 rerun;
2. the Business slice prevented continuation from a stale frontier by detecting and adopting newer merged authority.

We cannot yet make a time-saving, money-saving, ROI, productivity or universal reliability claim.

## SI-0014 gate
Project diversity requirement is already met: 2/2.
Genuine event count remains 1/3.
False resume remains 0.
Therefore status remains `READY_FOR_PILOT / HOLD_RECOVERY_EVIDENCE_GATE`.

Two additional **naturally occurring** genuine interruption recoveries are still required. They must not be manufactured for the test.

## Instrumentation improvement for the next natural event
Capture, only if available without changing behavior:
- observable recovery start/end timestamps or elapsed duration;
- number of stale/duplicate routes actually considered and rejected;
- exact current authority readbacks;
- project count;
- false resume outcome;
- any manual correction/override;
- if a counterfactual duplicate was actually queued or attempted, its concrete work unit ID.

Do not require time instrumentation if it would distort or delay recovery.

## Next high-information work
1. Keep Cycle10 event/receipt schema as bounded observability candidate.
2. On genuine event #2, run the same validator and compare schema fit without changing the event.
3. Track false positives: recovery/freshness guard fired but would not have changed a decision.
4. Track false negatives: stale/duplicate work escaped the guard.
5. After event #3, compile a promotion-review packet for SI-0014; machine may only return `ELIGIBLE_FOR_REVIEW`.
6. Independently evaluate whether the observability overhead is lower than the failure/rework it helps prevent; do not infer until measurements exist.

## No-promotion decision
Cycle10 is an evidence-calibration adapter, not a new Self-Improvement engine and not a new SI candidate ID by itself.
