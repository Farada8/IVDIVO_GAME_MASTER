# D01 CENTRAL ROUTER REPAIR — GITHUB + DRIVE PERSISTENCE RECEIPT

**Date:** 2026-08-22  
**Status:** PERSISTED / PROVENANCE ONLY / NOT CURRENT STORY CANON

## GitHub lineage
- PR #275: `Repair D01 stale central router with minimal readable diff`.
- It was merged as commit `f409739c2448b5fa0905e0eac252d95cc13421ed`.
- Later main authority advanced beyond that intermediate routing state. PR #275 is therefore retained as **SUPERSEDED / DO NOT USE AS CURRENT AUTHORITY** while its engineering lesson remains valid provenance.
- Accidental duplicate persistence PRs #472 and #475 were closed immediately, unmerged, and have no authority.

## Drive lineage
- Parent folder: `03_D01_CENTRAL_ROUTER_REPAIR`
- Folder ID: `1SWPIsqT_Gx86jVUlRBwbh7McLLawuz0M`
- Previous diagnostic: `00_D01_CENTRAL_ROUTER_REPAIR_HOLD_AND_READBACK`
- Current cross-store receipt: `01_D01_ROUTER_REPAIR_PERSISTENCE_RECEIPT_GITHUB_DRIVE_2026-08-22`
- Google Doc ID: `1VovDwMUqZ87WNbQDjhjS1dUw02XvqUBuJY9ceSlGyIA`

## Proven defect at time of repair
Aggregate routing lagged behind `PROJECTS/THE_WIFE_AT_HIS_WEDDING/CURRENT_STATE.md`, which already recorded D01 Founder-locked E01–E120 with recording authority issued.

## Engineering lessons retained
1. `TEST_PASS != ACCEPTABLE_PATCH` — deterministic correctness is not enough if serialization creates an unreadable high-noise diff.
2. `FRESHNESS_CAN_SUPERSEDE_A_VALID_REPAIR_BEFORE_MERGE` — a correct intermediate repair must be abandoned if stronger current authority arrives first.
3. `WRITE_CLAIM != PERSISTED_ARTIFACT` — persistence requires provider readback, not a tool-call claim.
4. `TOOL_ROUTE_MISMATCH` — wrong connector/action routing is an operational defect and must not be counted as successful persistence.
5. `DUPLICATE_PR_CREATION` — accidental duplicate PRs must be closed immediately to avoid authority split.

## Evidence boundary
- no new story canon;
- no D01 prose reopen authorization;
- no SI-0015 promotion;
- no Human Signal/provider/market evidence inferred;
- current main/project authority always outranks this receipt.

## Safe continuation law
`FRESHNESS_SWEEP -> CURRENT PROJECT AUTHORITY -> CURRENT SYSTEM ROUTER -> EXECUTE HIGHEST UNBLOCKED OBLIGATION -> VERIFY -> PERSIST -> READBACK`.
