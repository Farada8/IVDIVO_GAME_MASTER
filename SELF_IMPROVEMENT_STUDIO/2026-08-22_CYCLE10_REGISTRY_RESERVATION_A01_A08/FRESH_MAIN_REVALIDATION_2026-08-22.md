# Fresh-main revalidation — Registry Reservation A01–A08

Revalidation root: `main` = `81fa685dc0e85e85972ae00d9a1ee0d90b4cfed4`.

## Readback facts
- `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json` on current main still lists committed extensions through `SI-0015`; `SI-0016` is not committed.
- PR #147 remains OPEN / DRAFT / unmerged and its branch contains the dedicated `SI-0016_STRATEGIC_AUTHORITY_DISCOVERABILITY_SCOPE_BOOT.json` shard.
- GitHub open-PR search reports 106 open PRs with `incomplete_results=false`.
- Complete per-PR diff/path visibility is still not proven; therefore the allocation view remains fail-closed.

## Decision
`HOLD_PARTIAL_VISIBILITY` remains correct.

`SI-0017` is NOT declared free.
No new SI ID is allocated.
No Self-Improvement authority promotion is implied.

This receipt revalidates the historical A01–A08 snapshot against fresh main without rewriting the original captured evidence.