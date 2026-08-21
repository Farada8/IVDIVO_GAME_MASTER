# Wave11 — Engineering Modules, Contracts, Proofs and Protocols

## A. Concrete engineering modules

| ID | Module | Status | Responsibility |
|---|---|---|---|
| M01 | `wave11_frontier_evaluator.py` | NEW / CODED | 01–32 dependency DAG, READY/BLOCKED routing, ordering violations. Routing only. |
| M02 | `provider_snapshot_contract.py` | REUSE CURRENT | Authenticated secret-free snapshot shape, freshness, provider/account provenance. |
| M03 | `elevenlabs-provider-snapshot.yml` | REUSE CURRENT | Manual read-only acquisition, secret in Actions only, durable artifact readback, no synthesis. |
| M04 | `provider_snapshot_diff.py` | REUSE CURRENT | Two-snapshot account/capability repeatability and drift. |
| M05 | `provider_inventory_compiler.py` | REUSE CURRENT | Validated snapshot → source-bound model/voice inventory; unknown stays unknown. |
| M06 | `cast_readiness.py` | REUSE CURRENT | Provisional NARRATOR/ETHAN/AOIFE bindings and real-audition requirements. |
| M07 | `external_evidence_trust.py` | REUSE CURRENT | Class-specific external receipt validation; booleans/pointers are not truth. |
| M08 | `human_review_ledger.py` | REUSE CURRENT | Append-only validated human review history; conflict preserved. |
| M09 | controlled provider dispatch | REUSE CURRENT | Fail-closed provider dispatch/idempotency/quarantine; acceptance != take lock. |
| M10 | `live_lineage_escrow.py` | REUSE CURRENT | Exact-N paid lineage, no paid replay, transaction recovery coverage. |
| M11 | alignment/timeline/QC runtime | REUSE CURRENT | Real audio ingest/alignment/timeline/repair after live assets exist. |
| M12 | Self-Improvement evidence bridge | REUSE + NEW DISCOVERY RECORD | Converts evidenced defect/repair/retest into candidate learning; no auto-promotion. |

## B. Engineering contracts

### C01 — UPSTREAM_EVIDENCE_BEFORE_DOWNSTREAM_EXECUTION
A prompt may be READY only when every declared dependency is completed through its own authoritative evidence path. Dependency completion cannot be inferred from code existence.

### C02 — ROUTING_IS_NOT_TRUTH
`wave11_frontier_evaluator.py` may route work but may not authenticate provider/human/live/economics evidence. `external_truth_validated=false` is invariant.

### C03 — AUTH_PROVIDER_SOURCE_OF_TRUTH
Account-specific voice/model capability must come from current validated authenticated ProviderSnapshot evidence. Public documentation, remembered IDs, old project IDs, or caller booleans cannot substitute.

### C04 — NO_CROSS_ACCOUNT_INVENTORY
If two ProviderSnapshots have different account fingerprints, comparison stops. Inventories cannot be unioned.

### C05 — UNKNOWN_IS_UNKNOWN
Missing model/voice capability metadata is not silently guessed. TTS model eligibility requires explicit observed capability.

### C06 — PROVISIONAL_CAST_IS_NOT_LOCK
Provider metadata may create provisional candidates only. Pronunciation/performance/fatigue/pair quality require heard real audio + trusted human receipts.

### C07 — HUMAN_LOCK_IS_EXPLICIT
Voice lock or pre-spend GO requires explicit authorized human/Founder evidence with hashes. Continuation commands, machine scoring or CI cannot stand in for the lock.

### C08 — SPEND_BOUNDARY_IS_SEQUENTIAL
RB001 must be dispatched and resolved first. RB002/RB003 remain blocked until RB001 human sanity passes. Ambiguous provider outcome quarantines downstream paid work.

### C09 — PAID_LINEAGE_IS_RECOVERABLE
Every paid request/result/spend/audio/alignment lineage must be durably receipt-bound. Recovery must prove transaction-recoverable content coverage with zero duplicate calls/charges.

### C10 — ENGINEERING_CI_HAS_AN_EVIDENCE_CEILING
CI proves deterministic code behavior only. It cannot prove real provider availability, human preference, voice suitability, accepted audio, measured economics or production readiness.

## C. Proof obligations

| Proof | Required evidence | Current Wave11 state |
|---|---|---|
| P01 DAG exactness | 32 prompt IDs + causal deps + regression | CODED / CI REQUIRED |
| P02 Illegal-order rejection | downstream completion without deps => HOLD | CODED / CI REQUIRED |
| P03 Authority non-escalation | evaluator always false for voice_lock/release_go/dispatch | CODED / CI REQUIRED |
| P04 Provider authenticity | class-valid AUTH_PROVIDER durable receipt | HOLD EXTERNAL |
| P05 Provider repeatability | two independently valid snapshots, same account | HOLD P04 |
| P06 Inventory source binding | inventory hash bound to valid snapshot | HOLD P04 |
| P07 Cast provenance | candidates all from same inventory/model | HOLD P06 |
| P08 Pronunciation/performance | real audio + trusted human receipts | HOLD P07 |
| P09 Explicit voice lock | authorized human lock with hashes | HOLD P08 |
| P10 Pre-spend immutability | 3 request hashes / 36 units / 2163 chars + capability revalidation | HOLD P09 |
| P11 RB001 lineage | request/result/spend/raw/durable receipts | HOLD P10 |
| P12 Sequential canary | RB002/3 impossible before RB001 human pass | CODED routing / REAL EXECUTION HOLD |

## D. Protocols

### PR01 — FRESH_AUTHORITY_PROTOCOL
Before each major Wave11 write/merge: re-read `main`, current Wave10 state, open overlapping PRs and Drive workstate. Never force an older branch over newer authority.

### PR02 — EXTERNAL_EVIDENCE_ACQUISITION_PROTOCOL
Run provider workflow only with repository secret configured outside chat/Git/Drive. Persist only secret-free snapshot + receipt. Validate source/readback/freshness before any inventory use.

### PR03 — DEPENDENCY_FRONTIER_PROTOCOL
Execute prompt in numerical dependency order. If upstream evidence is missing, record a precise HOLD/BLOCKED reason and stop destructive/paid descendants. HOLD is stored as result.

### PR04 — HUMAN_EVIDENCE_PROTOCOL
Blind or scoped listening uses actual rendered assets, artifact/candidate hashes, device/session provenance and real reviewer attestation. Model simulation cannot enter human ledger.

### PR05 — PAID_CANARY_PROTOCOL
Preflight → explicit human GO → RB001 only → durable lineage → human sanity → RB002 → resolve → RB003. No batch past ambiguity and no automatic paid replay.

### PR06 — SELF_IMPROVEMENT_PROTOCOL
Only record `DEFECT → ROOT CAUSE → REPAIR → RETEST → RESULT → REUSE CONDITIONS`. Engineering replication may create a review candidate; universal/current promotion requires independent real-project evidence and appropriate human/Founder authority.

## E. Engine-level interaction graph

`Fresh Authority Resolver`
→ `Provider Snapshot Bridge`
→ `Snapshot Validator + Diff`
→ `Provider Inventory Compiler`
→ `Cast Readiness`
→ `Real Audition + Human Review Ledger`
→ `Explicit Lock`
→ `Capability Drift Recheck`
→ `Pre-Spend Manifest`
→ `Controlled Dispatch`
→ `Live Lineage Escrow`
→ `Human Sanity`
→ `Real Alignment / Timeline / Mix / QC`
→ `Measured Human + Economics Evidence`
→ `Self-Improvement Candidate`
→ `Founder Release Decision`.

Wave11 adds the dependency frontier around this graph; it does not replace any node.
