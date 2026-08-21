# IVDIVO SELF-IMPROVEMENT — CYCLE 6 — REAL INTEGRATION — 32 EXECUTION RESULTS

**Status:** 32/32 EXECUTED / DISPOSITIONED  
**Authority:** WORKING / PILOT / NOT CURRENT AUTHORITY  
**Evidence boundary:** real persisted GitHub/Drive inputs where available; no fabricated Human/provider/economics/market proof.

## C6R-01 — Registry reservation scan

**Type:** `REAL_INTEGRATION`  
**Module:** `REGISTRY_RESERVATION_SCAN`  
**Status:** `PASS_REAL_PERSISTED_INPUT`

Main+open reservation scan finds SI-0015 next-unreserved but does not allocate.

```json
{"status":"PASS","collisions":[],"next_unreserved":"SI-0015","main_ids":["SI-0008","SI-0009","SI-0010","SI-0011","SI-0012","SI-0013"],"reserved_ids":["SI-0014"]}
```

**Claim limits:** NO_NEW_ID_ALLOCATED

## C6R-02 — Registry partial visibility attack
`PASS_FAIL_CLOSED` — allocation blocked without complete family proof: `HOLD_PARTIAL_VISIBILITY`.

## C6R-03 — Durable transaction convergence
`PASS_ENGINEERING_CONVERGENCE` — mixed GitHub/Drive states become `REPAIR_REQUIRED`; no implicit success.

## C6R-04 — Paid replay attack
`PASS_FAIL_CLOSED` — ambiguous paid/irreversible replay becomes `QUARANTINED`, `replay_allowed=false`.

## C6R-05 — Checkpoint restart proof
`PASS_ENGINEERING` — exact fresh checkpoint returns `RESUME_EXACT` only when main/state still match.

## C6R-06 — Stale-main restart attack
`PASS_FAIL_CLOSED` — main drift returns `REBASE_FIRST / AUTHORITY_OR_STATE_DRIFT`.

## C6R-07 — Interruption observer
`PASS_CONTRACT_REAL_INCIDENT_REQUIRED` — protocol records bounded incident observations; no forced interruption was fabricated in this cycle.

## C6R-08 — Incomplete interruption attack
`PASS_FAIL_CLOSED` — incomplete recovery observation is `HOLD_INCOMPLETE_OBSERVATION`.

## C6R-09 — MF-C03 second-book replication
`PASS_REAL_PROJECT_EVIDENCE` — D10 BLOODBOUND known-positive 1/1, repaired current 0/0, false-positive control 0, locked story unchanged. Disposition: `SECOND_BOOK_REPLICATION_PASS / BOOK_DOMAIN_REVIEW_ONLY`, not universal promotion.

## C6R-10 — Book sensor false-positive attack
`PASS_FAIL_CLOSED` — a healthy-control hit returns `FAIL_FALSE_POSITIVE`.

## C6R-11 — Book mechanism dedupe
`PASS_ENGINEERING` — semantically equivalent mechanism disposition is `MERGE_WITH_EXISTING`; no parallel engine/candidate is spawned.

## C6R-12 — Book overpromotion attack
`PASS_FAIL_CLOSED` — insufficient transfer remains `HOLD_FOR_MORE_EVIDENCE`.

## C6R-13 — D01 rapid frontier replay
`PASS_REAL_PERSISTED_INPUT` — persisted E120 / Founder-lock frontier supersedes E95→E96 and E112→E113 working frontiers.

## C6R-14 — D01 stale E96 attack
`PASS_FAIL_CLOSED` — proposed return from E120 to E96 is `FAIL_STALE_WORK`.

## C6R-15 — D01/D04 Human Signal gate
`HOLD_REAL_HUMAN_REQUIRED` — packets are ready but raw participant responses are absent. `HOLD_HUMAN_SIGNAL_NOT_RUN`. No synthetic-persona substitution.

## C6R-16 — Model-as-human attack
`PASS_FAIL_CLOSED` — model output classifies as `MODEL_REVIEW`, never Human Signal.

## C6R-17 — Evidence family graph
`PASS_ENGINEERING` — three reports sharing two root sources collapse to two independent evidence families; claim ceiling remains persistence-supported.

## C6R-18 — Model-vote inflation attack
`PASS_FAIL_CLOSED` — two derived model reports from one root count as one family.

## C6R-19 — Package promotion witness
`PASS_ENGINEERING` — post-package main extensions yield `NEW_PACKAGE_REQUIRED`; old package cannot be relabelled.

## C6R-20 — Missing package hash attack
`PASS_FAIL_CLOSED` — no exact package hash = `HOLD_PACKAGE_PROOF`.

## C6R-21 — Promotion proof bundle
`HOLD_EXTERNAL_EVIDENCE` — engineering closure cannot satisfy an explicitly external evidence gate.

## C6R-22 — Incomplete promotion attack
`PASS_FAIL_CLOSED` — missing regression/readback/rollback/source/evidence-boundary proof blocks promotion.

## C6R-23 — Real telemetry ingest
`PASS_REAL_PERSISTED_INPUT` — D04 Human gate is captured while unknown spend and human time remain null.

## C6R-24 — False-zero telemetry attack
`PASS_FAIL_CLOSED` — unmeasured `provider_spend=0` is rejected as false zero.

## C6R-25 — Audio economics gate
`HOLD_MEASURED_DATA_REQUIRED` — current persisted D04 evidence lacks provider spend, human minutes, generated minutes, accepted minutes and hourly cost. No estimate is substituted.

## C6R-26 — Economics formula canary
`PASS_ENGINEERING` — deterministic measured fixture yields total cost 20.0, cost/accepted-minute 2.0, waste 2 minutes. **Fixture only; not production economics.**

## C6R-27 — Second-audio replication attempt
`HOLD_NOT_SAME_MECHANISM` — NMM is genuinely a second project, but identical project-neutral post-render contract identity is not yet proven.

## C6R-28 — Second-audio human gate attack
`PASS_FAIL_CLOSED` — even if generic mechanism identity matched, NMM remains HOLD because Human result is `NOT_TESTED`.

## C6R-29 — Proof-ledger compaction
`PASS_ENGINEERING` — duplicate proof lineage compacts to newest revision without evidence-class inflation.

## C6R-30 — Proof laundering attack
`PASS_FAIL_CLOSED` — engineering evidence cannot become `HUMAN_SIGNAL` through compaction.

## C6R-31 — Live governor
`PASS_REAL_FRONTIER_ROUTING` — among current admissible alternatives, real D04 Human Signal outranks another meta prompt cycle.

## C6R-32 — Legitimate-meta attack
`PASS_ENGINEERING` — critical integrity work may still outrank lower-information product work when it actually has higher priority/information value.
