# PROJECT STATE FRESHNESS + AUTHORITY VERSION CHAIN — ENGINEERING CONTRACT v1.0

**Status:** WORKING / H17-H18 candidate engineering layer  
**Date:** 2026-08-21  
**Scope:** durable routing freshness only. Never story canon, literary quality, Founder lock, specialist clearance, or provider evidence.

## Problem
A durable `PROJECT_STATES` pointer can be internally valid and still become stale after its controlling Drive/GitHub authority changes. Existing coverage gates prove that a pointer exists; they do not prove that the pointer still reflects the newest source revision.

## Core contract

`PROJECT STATE -> AUTHORITY BASELINE -> CURRENT PROVIDER OBSERVATION -> VERSION-CHAIN CHECK -> FRESH / REVIEW / STALE_REBASE -> RE-READ -> SEMANTIC RECONCILIATION -> STATE WRITE -> READBACK`

Never:

`REVISION CHANGED -> SILENT CANON CHANGE`.

A changed revision is a **routing signal** requiring re-read/rebase. It is not evidence that story facts changed.

## H17 Freshness states

- `PASS_FRESH` — all required observed identities/revisions match baseline and the same source remains CURRENT.
- `REVIEW_REQUIRED` — a required source could not be observed; do not claim freshness.
- `STALE_REBASE_REQUIRED` — locator/revision/title/current-authority identity changed or a newer CURRENT authority replaced the baseline source.
- `FAIL_CONTRACT` — malformed/ambiguous observation set, multiple CURRENT authorities, or authority-rank regression.

## H18 Version-chain laws

1. Every source has unique `source_key`.
2. Exactly one source in a project chain is `CURRENT`.
3. CURRENT must have the highest authority rank.
4. `supersedes` edges must resolve to known source keys.
5. Supersession graph must be acyclic.
6. `SUPERSEDED` sources must be reachable from a newer source; orphan superseded labels fail.
7. `HISTORICAL` and `REFERENCE_ONLY` may remain for provenance but cannot outrank CURRENT.
8. A project-specific current authority always outranks generic portfolio/system routing.

## Evidence classes

Provider revision IDs / Git SHAs support identity/freshness claims only. They cannot prove:
- semantic equivalence;
- story quality;
- factual correctness;
- Founder approval;
- audio/provider success;
- commercial readiness.

Semantic reconciliation remains a separate human/model project-authority read after staleness is detected.

## Implementations

- `tools/ivdivo_project_state_freshness.py`
- `tools/validate_authority_version_chain.py`
- `tests/test_project_state_freshness.py`
- `PROJECT_STATES/AUTHORITY_FRESHNESS_BASELINE_2026-08-21.json`
- `.github/workflows/self-improvement-integrity.yml`

## First real baseline
D06 / D07 / D08 current Drive authority and Final Story Gate revision IDs were read directly from Google Docs during H17-H18 execution and persisted as routing-evidence baseline.

## Promotion gate
Do not promote this layer to universal CURRENT solely from unit tests. Required next evidence:
1. CI green on the repository branch/PR;
2. one real unchanged provider observation -> `PASS_FRESH`;
3. one deliberately newer provider revision -> `STALE_REBASE_REQUIRED`;
4. semantic re-read proves the workflow routes correctly without silently changing canon;
5. second-project-family replication outside D06-D08 before universal promotion.

## Rollback
These modules are advisory/fail-closed routing gates. Rollback means remove their CI invocation and candidate pointer; project authority/state files remain untouched.

**Invariant:** freshness tooling may force a re-read; it may never invent what the newer source says.
