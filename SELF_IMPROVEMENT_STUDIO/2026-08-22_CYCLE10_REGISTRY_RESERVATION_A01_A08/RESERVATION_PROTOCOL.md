# ACTIVE SI REGISTRY RESERVATION PROTOCOL v1

## Goal
Prevent two concurrent conversations/branches from assigning the same global `SI-xxxx` identifier.

## Source planes
1. committed registry base + committed extension shards on current `main`;
2. complete metadata list of open PRs;
3. candidate-changing PR diff/path evidence;
4. explicit candidate shard content;
5. merge-time fresh-main revalidation.

## Fail-closed law
`MAIN_REGISTRY_COMPLETE != GLOBAL_RESERVATION_VIEW_COMPLETE`.

`next_unreserved` may be emitted only when open-PR metadata coverage is complete, candidate-changing diff coverage is complete, no committed/reserved collision exists, and snapshot main SHA is still current at allocation/merge.

Otherwise: `HOLD_PARTIAL_VISIBILITY` or `HOLD_STALE_SNAPSHOT`.

## Current real result
- committed main: through SI-0015;
- PR #147 contains dedicated `SI-0016` shard + registry-family change: `RESERVED_OPEN_PR`;
- PR #104 SI-0012 is historical because SI-0012 is already committed;
- PR #80 candidate-only SI-0012/SI-0013 explicitly forbids central registry write-through and both IDs are already committed;
- inspected Cycle32D/Cycle9/SI-0014/SI-0015 calibration PRs do not allocate a new SI ID;
- PR #251 correctly uses `UNASSIGNED_*` and explicitly refuses a global ID while SI-0016 is reserved;
- GitHub reported 106 open PRs while bulk diff enumeration exceeded provider limit (>20,000 lines), so global visibility remains incomplete.

Therefore SI-0017 is **not** declared available and no new ID is allocated.

## Merge-time collision repair
If a candidate ID is consumed after branch creation: stop merge; re-read committed family + reservations; assign a different ID only after complete visibility; preserve old ID as historical alias; update pointers; rerun schema/lifecycle tests; persist and read back.

## PR lifecycle
- open + candidate shard present → RESERVED_OPEN_PR
- closed unmerged → RELEASED_CLOSED_UNMERGED
- merged → REVALIDATE_AS_COMMITTED
- candidate removed → RELEASED_CANDIDATE_REMOVED
- superseded → RELEASED_SUPERSEDED

No PR body, prompt count, or model statement alone creates a reservation.
