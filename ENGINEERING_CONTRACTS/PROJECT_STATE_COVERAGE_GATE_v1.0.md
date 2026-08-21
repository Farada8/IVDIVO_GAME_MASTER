# IVDIVO — PROJECT-STATE COVERAGE / PORTFOLIO RESUMABILITY CONTRACT v1.0

**Status:** ENGINEERING CANDIDATE / H09-H16  
**Date:** 2026-08-21  
**Purpose:** prove that a future conversation/model can route every required portfolio project without inventing its current frontier.

## 1. Core law
A project counts as resumable only when one of these is persisted:
1. a durable current state pointer with recovery status `PASS*`; or
2. an explicit `BLOCKED_RECOVERY` record with a concrete reason.

Missing routing must never be converted into a guessed next action.

## 2. Required index fields
`PROJECT_STATES/00_PROJECT_STATE_COVERAGE_INDEX.json` must include:
- `required_project_ids[]`;
- `coverage[]`;
- `blocked_recovery[]`;
- `portfolio_resumability_claim`.

## 3. Valid portfolio claims
- `PASS_FULL`: all required projects have durable PASS-like routing; no blocked recovery remains.
- `PASS_WITH_BLOCKED_RECOVERY`: every required project is represented, but at least one is explicitly blocked on exact authority recovery.

There is no valid “full” claim while a required project is blocked.

## 4. Fail-closed conditions
The validator must fail on:
- missing `required_project_ids`;
- required project absent from both coverage and blocked recovery;
- project represented in both coverage and blocked recovery;
- coverage row without a state path;
- non-PASS recovery value stored as normal coverage;
- blocked row without `BLOCKED_RECOVERY` status/reason;
- duplicate project rows;
- portfolio claim inconsistent with blocked state.

## 5. Evidence boundary
Coverage PASS proves routing completeness, not:
- manuscript quality;
- story completion;
- Founder lock;
- commercial release readiness;
- audio readiness;
- legal/medical/technical clearance.

Those statuses must be read from the project-specific state/authority.

## 6. State-file minimum contract
A durable project state should contain only what continuation needs:
- project ID/title;
- authority note/order;
- current story/text status;
- controlling artifact IDs/paths;
- downstream stage;
- blockers/holds;
- next safe action;
- do-not-repeat rules;
- provenance.

It must not manufacture detailed canon from aggregate labels.

## 7. Staleness protection
A project state is a routing pointer, not immortal authority. On boot:
`STATE POINTER -> SOURCE AUTHORITY EXISTS? -> NEWER CONTROLLING ARTIFACT? -> TERMINAL GATE? -> REBASE OR ACCEPT`.

A newer timestamp/title alone does not automatically supersede an authority file. Status, version lineage and governing text decide.

## 8. Current pilot
The H09 pilot expands durable recovery to D06/D07/D08 using their exact Drive authority documents and final-season gate IDs. D01 remains explicit `BLOCKED_RECOVERY` until its current authority is reconciled into a durable state.

## 9. Promotion gate
The coverage mechanism remains a candidate until:
- repository validator + fixtures pass CI;
- D06/D07/D08 cold-start from their new states succeeds;
- D01 is either recovered or remains correctly blocked without stopping independent portfolio work;
- a later freshness sweep does not reveal stale/contradictory pointers.

**Unknown must remain unknown. A blocked route is safer than an invented continuation.**
