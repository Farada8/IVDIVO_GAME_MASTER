# PROJECT STATE FRESHNESS + AUTHORITY VERSION-CHAIN CONTRACT v1.0

**Status:** ENGINEERING CONTRACT / CANDIDATE ENFORCEMENT  
**Date:** 2026-08-21

## Purpose

Durable project state solves conversation-memory loss, but a durable pointer can itself become stale after parallel edits. This contract separates routing freshness from story/canon judgment.

## Core law

`STATE EXISTS` is not enough.

Before continuation:
`DURABLE STATE -> AUTHORITY SNAPSHOT -> LIVE PROVIDER OBSERVATION -> VERSION CHAIN -> FRESH / REVIEW / STALE -> SEMANTIC RE-READ -> REBASE -> STATE WRITE -> READBACK`.

## Freshness statuses

- `PASS_FRESH` — observed identity/revision/current-authority match the snapshot.
- `REVIEW_REQUIRED` — a required source was not observed; absence cannot be converted to freshness.
- `STALE_REBASE_REQUIRED` — revision, locator, title, modification order or current authority changed.
- `FAIL_CONTRACT` — malformed state/observation or authority-rank regression.

## Critical firewall

`REVISION_CHANGED != CANON_CHANGED`.

Freshness machinery may force re-read/rebase. It may not infer what the changed document means, whether story canon changed, or whether Founder authority changed. Those conclusions require semantic reconciliation against the actual source.

## Authority version-chain requirements

Each bounded authority manifest has:
- unique `source_key`;
- `locator`;
- `revision` when provider exposes one;
- integer `authority_rank`;
- disposition: `CURRENT | SUPERSEDED | HISTORICAL | REFERENCE_ONLY`;
- optional `supersedes[]` edges.

Hard invariants:
1. exactly one `CURRENT`;
2. CURRENT has highest authority rank in the bounded chain;
3. every supersedes target exists;
4. no supersession cycle;
5. a `SUPERSEDED` row must be reached by a newer row's supersedes edge;
6. reference/history cannot silently become current through file recency alone.

## Provider observations

Provider-neutral live observations may come from Google Drive, GitHub or another authority store. Metadata is evidence of change, not semantic meaning. If provider observation is unavailable, route `REVIEW_REQUIRED`.

## Rebase contract

On `STALE_REBASE_REQUIRED`:
1. stop unsafe continuation dependent on that authority;
2. fetch/read the changed source;
3. compare semantic delta;
4. classify `NO_SEMANTIC_AUTHORITY_CHANGE / ROUTING_CHANGE / CANON_OR_LOCK_CHANGE / UNKNOWN`;
5. update only true descendants;
6. persist new snapshot and project state;
7. read back;
8. rerun freshness gate.

## Acceptance

Required fixtures:
- unchanged snapshot PASS;
- changed revision STALE;
- new CURRENT authority STALE;
- missing observation REVIEW;
- two CURRENT FAIL;
- CURRENT not highest rank FAIL;
- cycle FAIL;
- real provider baseline captured from at least two project families;
- changed revision never sets `canon_changed=true` mechanically.
