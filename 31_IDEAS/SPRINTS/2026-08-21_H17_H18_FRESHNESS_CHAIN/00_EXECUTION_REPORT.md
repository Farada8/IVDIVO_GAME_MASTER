# H17–H18 — PROJECT STATE FRESHNESS + AUTHORITY VERSION CHAIN

**Date:** 2026-08-21  
**Status:** WORKING ENGINEERING / READY FOR CI + REAL DRIFT PILOT  
**Self-Improvement candidate:** SI-0014 — READY_FOR_PILOT

## Freshness / rebase result before work
The selected H01/H02/H03/H05/H09/H13/H14/H15 tranche was already completed and merged by newer project work through PR #98. That implementation includes:
- transactional improvement-registry shard writer + rollback/compaction tests;
- SI-0008 real registry-family write-through;
- Self-Improvement Integrity CI;
- project-state portfolio coverage gate;
- durable D06/D07/D08 project states recovered from exact Drive authority;
- coverage index v1.2 with D01 explicitly `BLOCKED_RECOVERY`.

Therefore no duplicate H01-H15 engine was created. The next unresolved prompts H17/H18 were executed.

## H17 — state-staleness detector
Implemented `tools/ivdivo_project_state_freshness.py`.

Outputs:
- `PASS_FRESH`
- `REVIEW_REQUIRED`
- `STALE_REBASE_REQUIRED`
- `FAIL_CONTRACT`

Detected drift classes:
- source locator changed;
- revision changed;
- provider modified time advanced;
- title changed;
- CURRENT authority source changed;
- authority-rank regression;
- required source not observable.

Critical firewall:
**revision drift triggers re-read/rebase; it does not itself change canon.**

## H18 — authority version-chain validator
Implemented `tools/validate_authority_version_chain.py`.

Hard checks:
- unique source keys;
- exactly one CURRENT source;
- CURRENT has highest authority rank;
- supersession targets resolve;
- no supersession cycles;
- no orphan `SUPERSEDED` source.

## Real provider baseline
Created `PROJECT_STATES/AUTHORITY_FRESHNESS_BASELINE_2026-08-21.json` using direct Google Docs revision IDs for:
- D06 SHE STOLE MY NAME current authority + Final Story Gate;
- D07 THE PERFECT WIFE KNOWS current authority + Final Story Gate;
- D08 SHE FIRED THE BILLIONAIRE current authority + Final Story Gate.

Evidence class: provider revision identity / routing freshness only.

## Deterministic evidence
Local smoke before persistence:
- unchanged authority set -> `PASS_FRESH`;
- changed revision -> `STALE_REBASE_REQUIRED`;
- valid chain -> PASS.

Repository regression suite adds 9 tests including real D06-D08 baseline-chain validation.

## CI integration
Existing `.github/workflows/self-improvement-integrity.yml` extended to run the freshness/version-chain regression with registry transaction, registry-reference, and portfolio coverage suites.

## Self-Improvement integration
Registered candidate shard:
`31_IDEAS/REGISTRY_EXTENSIONS/SI-0014_PROJECT_STATE_FRESHNESS_AUTHORITY_CHAIN.json`

Status remains `READY_FOR_PILOT`. No universal promotion from internal tests.

## Promotion evidence still required
1. Repository CI green.
2. Real unchanged provider observation -> PASS_FRESH.
3. Real changed revision -> STALE_REBASE_REQUIRED.
4. Re-read/reconciliation proves correct routing without silent canon change.
5. Replication on a second project family outside D06-D08.

## Next bounded frontier after this gate
If CI passes, next high-value H work is H19/H20: integrate explicit evidence classes into writing/reference QA without creating a second evidence system. Reuse the already merged Evidence-Aware Gate mechanisms and promote only missing enforcement.
