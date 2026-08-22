# NEXT64 A01–A08 EXECUTION — REGISTRY RESERVATION / CONCURRENCY

1. **A01 Complete active reservation snapshot** — `HOLD_PARTIAL_VISIBILITY` after complete 106-PR metadata enumeration because provider refused bulk diff >20,000 lines. Honest HOLD, not false PASS.
2. **A02 Machine-readable reservation record** — PASS. SI-0016 record includes PR, branch, path, blob SHA, lifecycle state and mechanism.
3. **A03 Reservation expiry/revalidation** — PASS_ENGINEERING. Runtime handles merge/close/remove/supersede states.
4. **A04 Two-branch same-ID attack** — PASS_FAIL_CLOSED. Deterministic collision test.
5. **A05 Main consumes ID after snapshot** — PASS_FAIL_CLOSED through stale-main and committed-vs-reserved tests.
6. **A06 Merge-time renumber protocol** — PASS_SPEC. Provenance/history preserved.
7. **A07 Registry-family completeness before candidate merge** — READY_FOR_CI. Scanner contract gates allocation; current snapshot itself remains partial.
8. **A08 False-HOLD/overhead review** — PARTIAL. Real provider limit proves whole-repo diff expansion is too expensive; recommended implementation is metadata-complete + targeted candidate-path discovery + explicit ambiguity HOLD. No measured maintenance-time savings yet.

## Decision
No new SI ID allocation. The value of this cycle is preventing a false `SI-0017 free` assertion.
