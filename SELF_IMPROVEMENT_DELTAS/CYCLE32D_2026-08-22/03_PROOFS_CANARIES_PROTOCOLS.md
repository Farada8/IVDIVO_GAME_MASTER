# CYCLE32D — PROOFS / CANARIES / PROTOCOLS

## Proof families
P01 authority pointer resolves to v2 VERIFIED_CURRENT.
P02 v3 remains candidate.
P03 empty claimed artifact => persistence FAIL.
P04 missing claimed GitHub path => persistence UNVERIFIED.
P05 non-empty wrong content => FAIL.
P06 correct content but wrong destination => FAIL.
P07 correct destination+anchors => VERIFIED_PERSISTED.
P08 partial multi-store write => PARTIAL.
P09 retry after PARTIAL must be idempotent.
P10 prompt count increase with no decision delta => NON_PROGRESS.
P11 duplicate capability fingerprint => MERGE/NARROW.
P12 active WIP above limit => FAIL_CLOSED.
P13 new SI ID with unresolved branch reservation => FAIL_CLOSED.
P14 v3 promotion without real production pilot => FAIL_CLOSED.
P15 local candidate rollback leaves v2 authority unchanged => PASS.

## Protocols
PR-01 RESTORE_AUTHORITY
PR-02 MULTI_SURFACE_FRESHNESS_SWEEP
PR-03 CAPABILITY_DEDUPE
PR-04 DECISION_RELEVANCE
PR-05 VOI_TEST_SELECTION
PR-06 SMALL_REVERSIBLE_CANARY
PR-07 PERSISTENCE_TRANSACTION
PR-08 READBACK_AND_CONTENT_VERIFY
PR-09 PARTIAL_WRITE_RECOVERY
PR-10 CROSS_STORE_PARITY
PR-11 RED_TEAM_AND_REGRESSION
PR-12 PROMOTE_HOLD_ROLLBACK
PR-13 LEARNING_LEDGER_BRIDGE
PR-14 RETURN_TO_PRODUCTION
