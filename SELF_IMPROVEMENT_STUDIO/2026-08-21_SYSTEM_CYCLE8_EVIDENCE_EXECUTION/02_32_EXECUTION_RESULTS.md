# Cycle 8 — 32 sequential execution results

Fresh integration base: `132149b052e9d29faf6695d9659aaaf59ec082d2`

Rule: execute each card once; external evidence requirements return explicit HOLD rather than synthetic evidence.

## C8-01 — Live registry reservation service
**PASS_ENGINEERING** — Fresh registry family 1.5 exposes SI-0008..SI-0015. Deterministic reservation view computes SI-0016 only as next-unreserved; no ID allocated.

## C8-02 — Unified transaction adapter
**PASS_REUSE_CURRENT** — Current main contains Cycle7 durable convergence plus integrated Run35 SI-0012/SI-0014 interface. Cycle8 does not create a second adapter/runtime; it adds compatibility canaries only.

## C8-03 — Checkpoint recovery telemetry
**PASS_ENGINEERING_CANARY** — Recovery event contract now requires fresh authority, checkpoint, post-restart authority readback, recovery readback, project identity and source-hash match. Stale main returns REBASE_FIRST.

## C8-04 — D04 Human Signal
**HOLD_REAL_HUMAN** — D04 machine G4 packet is ready, but current project state explicitly requires a real blind human response. No synthetic/model proxy counted.

## C8-05 — D01 Human Signal
**HOLD_REAL_HUMAN** — No raw target-reader/listener dataset is present. Main persistence closure keeps D01 at E01-E120 text-complete / Founder-lock decision gate; no Human Signal fabricated.

## C8-06 — Provider snapshot
**HOLD_AUTHENTICATED_PROVIDER** — No authenticated provider inventory was available through the current execution surface. Secret-free runbooks exist; capability proof remains external.

## C8-07 — Measured audio economics
**HOLD_MEASURED_DATA** — No verified provider spend/human-minutes/generated-minutes/accepted-minutes row was available. Unknown numeric values remain null; unmeasured zero is forbidden.

## C8-08 — Real interruption observation
**HOLD_REAL_INCIDENT** — No genuine unplanned interruption was manufactured. SI-0014 real-recovery promotion evidence remains absent for this cycle.

## C8-09 — Proof ledger integration
**PASS_ENGINEERING** — Bounded proof-ledger contract counts evidence families by root source, requires evidence class + root source, and rejects Human Signal laundering.

## C8-10 — Cross-project recovery
**PASS_CONTROLLED_ONLY** — Cross-project identity/source-hash gates are executable and fail closed. This is a controlled engineering canary and does not count toward SI-0014 genuine-interruption evidence.

## C8-11 — Package rebuild gate
**HOLD_DEPENDENCY_CLOSURE** — #133/#140/#141/#143 were reconciled as already integrated and closed provenance-only during this cycle, but other independent draft/evidence deltas remain open; a new immutable consolidated package is still premature. Historical package identity remains immutable.

## C8-12 — Prompt IR parity
**HOLD_SECOND_MODEL** — Structural omission/parity guard is executable, but no independent second model/execution surface was available; semantic second-model evidence is not claimed.

## C8-13 — Book sensor third-project
**PASS_MACHINE_INTERNAL** — MF-C03 third-project ORBITAL YOUTH replication is now integrated on current main: known-positive 1/1, repaired negative 0, bounded false positives 0/4, PROTECT_NO_CHANGE. Human/editor adjudication remains HOLD.

## C8-14 — NMM Human test
**HOLD_REAL_HUMAN** — NMM Cycle4 is integrated with trusted internal machine/Drive evidence, but no new uncoached human clue-discrimination/device-listening responses exist in this cycle.

## C8-15 — NMM provider canary
**HOLD_AUTHENTICATED_PROVIDER** — NMM Cycle4 keeps provider truth external; no authenticated provider canary executed and no voice/take/provider lock inferred.

## C8-16 — Portfolio governor
**PASS_REAL_FRONTIER_ROUTING** — D04 Human Signal remains highest-information overall but externally unavailable here. SI-0015/MF-C03/Run35/Cycle7 stale review surfaces were reconciled into current main/provenance during this cycle; after Cycle8 persistence closure the correct internal outcome is HOLD_REAL_EVIDENCE rather than invent another meta-architecture task. Parallel writing-Cycle8 mechanisms are reused, not duplicated.

## C8-17 — Reservation collision attack
**PASS_FAIL_CLOSED** — Injected committed/reserved SI-0015 collision returns HOLD_COLLISION.

## C8-18 — Partial-write attack
**PASS_FAIL_CLOSED** — GitHub committed/readback + Drive missing yields DRIVE-only safe completion plan; already-complete store is not replayed.

## C8-19 — Checkpoint stale-main attack
**PASS_FAIL_CLOSED** — Checkpoint SHA != current main SHA returns REBASE_FIRST.

## C8-20 — Human-signal laundering attack
**PASS_FAIL_CLOSED** — MACHINE or MACHINE_PROXY evidence presented as HUMAN_SIGNAL is rejected.

## C8-21 — D01 stale-episode attack
**PASS_FAIL_CLOSED** — E96 and E113 are rejected as stale relative to persisted E120 text frontier. This does not itself issue Founder lock.

## C8-22 — Provider credential leakage attack
**PASS_FAIL_CLOSED** — Secret-bearing keys such as api_key/token/secret/authorization/password are rejected before persistence.

## C8-23 — Economics false-zero attack
**PASS_FAIL_CLOSED** — 0 with measured=false is rejected; null remains a valid unknown.

## C8-24 — False-resume attack
**PASS_FAIL_CLOSED** — Any false resume count >0 blocks recovery promotion review even if interruption-count thresholds are otherwise met.

## C8-25 — Evidence-family inflation attack
**PASS_FAIL_CLOSED** — Multiple derived reports sharing one root source count as one evidence family.

## C8-26 — Cross-project recovery identity attack
**PASS_FAIL_CLOSED** — Wrong project identity or source hash fails the recovery-event acceptance contract.

## C8-27 — Package relabel attack
**PASS_FAIL_CLOSED** — Post-package commits cannot mutate or relabel a historical package SHA.

## C8-28 — Prompt IR omission attack
**PASS_FAIL_CLOSED** — Dropping or changing a protected fact/prohibition returns PARITY_FAIL.

## C8-29 — Book sensor false-positive attack
**PASS_FAIL_CLOSED** — Any healthy-control false positive blocks MF-C03 scope widening.

## C8-30 — NMM perceptual proxy attack
**PASS_FAIL_CLOSED** — Machine perceptual proxy cannot become Human Signal/perceptual PASS.

## C8-31 — Provider acceptance laundering attack
**PASS_FAIL_CLOSED** — Provider acceptance proves only provider acceptance; it does not imply production acceptance, take lock, voice lock or release lock.

## C8-32 — Governor starvation attack
**PASS_FAIL_CLOSED** — When P1 real evidence becomes admissible, governor selects it ahead of meta work; meta expansion cannot starve higher-information evidence.
