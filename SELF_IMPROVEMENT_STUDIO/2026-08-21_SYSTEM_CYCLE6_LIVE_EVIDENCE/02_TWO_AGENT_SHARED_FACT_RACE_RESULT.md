# CYCLE 6 — TWO-AGENT SHARED-FACT CAS RACE

**Status:** `PASS_LIVE_STALE_WRITER_REJECTED`  
**Evidence class:** `PERSISTED_READBACK / LIVE_REPOSITORY_MUTATION`  
**Scope:** non-canon Self-Improvement sandbox.

## Setup
Both logical writers started from the same fact state and the same GitHub blob SHA:
`94189e2d0048c594bd9770e66d0a63971fd13285`.

Shared fact: `C6_SHARED_FACT_001`.
Initial version: `1`.
Initial value: `ALPHA`.

## Writer A
Agent A committed version `2`, value `BETA_FROM_AGENT_A`, value hash:
`c13e43ec3c280c264703758167d187c58dcba64ac0f9d39849f5dd63b1ae9dc5`.

Commit: `f7079d5a8de7526223aae0c50d50f55728573945`.
New blob SHA: `ace034e0c3347c3504a33436ce4af2c6e77dafa7`.

## Writer B stale race
Agent B then attempted to commit a conflicting version from the original stale SHA `94189e...` with value `GAMMA_FROM_AGENT_B`.

Provider result: **HTTP 409 SHA mismatch**.

The conflicting write did not land.

## Readback
Fresh readback after the rejected Writer-B mutation still contained:
- value `BETA_FROM_AGENT_A`;
- version `2`;
- lock_owner `agent_A`;
- blob SHA `ace034e0c3347c3504a33436ce4af2c6e77dafa7`.

## Engineering conclusion
The repository CAS boundary successfully prevents the second stale writer from silently overwriting the first writer. Any higher-level multi-model fact-lock service should reuse this primitive and add semantic/version ownership around it rather than inventing a second write engine.

This result does not mean model agreement is evidence and does not promote any project fact or canon.
