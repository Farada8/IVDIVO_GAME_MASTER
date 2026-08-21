# IVDIVO — TRANSCRIPT RECOVERY SPRINT 2 — SYNTHESIS + UPGRADE DECISIONS

**Date:** 2026-08-21  
**Scope:** cross-dialog/full-chat recovery + Self-Improvement ingestion + persistence integrity.  
**Status:** EXECUTED SYNTHESIS / CANDIDATE DEVELOPMENT.

## Executive conclusion

The first recovery generation solved **safe extraction**. Sprint 2 shows that the hard problem is now **semantic reconciliation and proof**, not more regex.

The correct pipeline is:

`RAW/PASTED CHAT`
→ `RECOVERY LEDGER v1 (EXTRACTED_UNVERIFIED)`
→ `RECONCILED RECOVERY STATE v2`
→ `PROJECT PARTITIONS`
→ `CLAIM→EVIDENCE VERIFICATION`
→ `AUTHORITY/CHRONOLOGY/SUPERSESSION RECONCILIATION`
→ `CHAT_ONLY CANDIDATE ESCROW`
→ `TRANSACTIONAL WRITE + READBACK`
→ `RECOVERY COMPLETION GATE`
→ `NORMAL NEXT-ACTION RESOLVER`
→ `PRIMARY PRODUCTION CONTINUES`.

## 12 strongest conclusions

1. **Parser accuracy is not authority accuracy.** Extraction confidence, source authority, persistence verification and canon status remain separate fields.
2. **The last line of a chat is not the frontier.** Frontier = last verified completed artifact + current authority + passed gates + blockers + do-not-repeat + next legal action.
3. **One transcript may contain several projects.** Partition before write-through.
4. **Every consequential “saved / PASS / LOCK / rendered / approved / validated” claim needs an evidence contract.**
5. **Human/provider/market evidence are distinct classes.** AI cannot substitute for any of them.
6. **Unknown is a valid state.** Material unknown blocks completion instead of being filled from memory.
7. **Recovery must be idempotent.** Re-pasting the same chat must not duplicate candidates or writes.
8. **Persistence is transactional.** Write success without readback is incomplete.
9. **Concurrency is normal.** GitHub stale-SHA and Drive revision conflicts are rebase signals, not reasons to overwrite.
10. **Registry sharding is already the safer path.** Base+extensions+family pointer is preferable for concurrent writes; compaction becomes a controlled build artifact.
11. **Evidence-backed NO_OP is success.** Existing SI-0009/registry-family/hardening work should be extended, not recreated.
12. **The first real large pasted transcript remains the decisive operational pilot.** Unit tests cannot prove semantic recovery quality.

## Upgrade decisions

### KEEP CURRENT
- 18B Full Chat Recovery law.
- v1 deterministic extractor as fail-closed first pass.
- Self-Improvement v2 lifecycle/evidence separation.
- Registry-family shard/index architecture on main.

### EXTEND
- SI-0009 / PR67 with evidence-adapter + large-corpus + next-action integration tests.
- Transcript-parser hardening candidate with structured-export/fuzz fixtures.
- Recovery completion semantics with transaction/readback/partial-write tests.

### DO NOT PROMOTE YET
- PR67 Recovery State v2.
- parser-hardening candidate.
- any package version claiming these candidate extensions before full regression.

### DO NOT BUILD
- a second universal recovery router;
- an LLM confidence score that becomes authority;
- automatic Founder-lock inference;
- a monolithic transcript canon;
- a market/human/provider simulator.

## New machine-contract family

Sprint 2 defines five interoperable contracts:
1. `RECOVERY_AUTHORITY_CLASS`
2. `CLAIM_EVIDENCE_REQUIREMENT`
3. `RECOVERY_WRITE_TRANSACTION`
4. `RECOVERY_IDEMPOTENCY_KEY`
5. `REGISTRY_COMPACTION_MANIFEST`

Their compact candidate representation is in `05_MACHINE_CONTRACTS_OR_SCHEMAS.json`.

## Relationship to sibling work

- Draft PR #67 remains the primary SI-0009 implementation candidate. Sprint 2 **extends** it; it does not create a replacement v2 state architecture.
- Open PR #68 is a broader whole-system Self-Improvement 32→64 candidate. Its strongest compatible lesson is that state normalization, evidence-backed NO_OP, transactional persistence and execution integration matter more than another layer of prose rules. PR68 is not CURRENT merely because it is broader/newer.
- Current registry-family architecture already solves part of N31. Sprint 2 therefore avoids recreating a second registry system.

## Priority after this sprint

Primary evidence path:

`FIRST REAL LARGE CORPUS PILOT -> v1 extraction -> v2 semantic reconciliation -> persisted-source verification -> correct frontier -> transactional write/readback -> completion gate -> normal next action`.

Parallel bounded pilots:
- adversarial/fuzz parser hardening;
- registry compaction/transaction builder.

## Stop/hold law

No further prompt-count expansion may outrank the empirical pilot. The derived 64 prompts are a routed test/development bank. Run only the subset that closes the current evidence gap or production blocker.
