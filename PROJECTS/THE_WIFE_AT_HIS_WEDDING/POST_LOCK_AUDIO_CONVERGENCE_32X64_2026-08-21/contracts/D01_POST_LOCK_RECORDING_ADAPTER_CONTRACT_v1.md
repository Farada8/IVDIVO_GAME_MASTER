# D01 POST-LOCK RECORDING ADAPTER CONTRACT v1.0

**Scope:** D01 `THE WIFE AT HIS WEDDING` locked source -> shared IVDIVO Audio Runtime.  
**Status:** project contract / shared-runtime extension candidate.

## Invariants

1. Story authority is the Founder-locked E01–E120 source. Audio engineering cannot silently modify words.
2. D01 does not own or fork provider logic. It consumes the shared `provider_snapshot -> provider_inventory -> cast_readiness` chain.
3. Project-specific casting data must be supplied as data, not hard-coded into a second module.
4. Required D01 principal roles are NARRATOR, MARA, ADRIAN, LILY, CELESTE.
5. Mara/Adrian is a relationship-pair audition gate; chemistry must come from incompatible evidence/status, not generic flirtation.
6. Voice metadata never equals artistic approval.
7. `provider_dispatch_allowed` remains false until real provider/cast/preflight gates explicitly unlock it.
8. `machine_may_auto_lock=false` permanently for artistic voice lock.
9. Supporting roles may remain provisional until principal separation/chemistry passes.
10. Existing R01–R08 and S01–S07 topology is inherited unless real evidence demonstrates a segmentation defect.

## Interfaces

Input A — `ProviderSnapshot` (authenticated, secret-free, fresh).  
Input B — normalized `provider_inventory`.  
Input C — `D01_CAST_READINESS_SPEC_v1.json`.  
Input D — candidate real provider voice IDs.  
Output — cast-readiness manifest in `READY_FOR_REAL_AUDITION` or a fail-closed HOLD/FAIL state.

## Fail closed

- stale/unverified inventory;
- missing principal role candidates;
- unknown provider voice IDs;
- selected model absent from verified inventory;
- invalid pair outside the project role set;
- invalid fatigue window;
- pronunciation evidence missing when a lock is requested;
- any auto-substitution of a locked principal;
- any attempt to treat machine metadata as Human Signal.

## Reopen boundary

A failed voice/performance/adaptation gate first routes to selective audio repair. Locked story text reopens only under the Founder Lock reopen law.
