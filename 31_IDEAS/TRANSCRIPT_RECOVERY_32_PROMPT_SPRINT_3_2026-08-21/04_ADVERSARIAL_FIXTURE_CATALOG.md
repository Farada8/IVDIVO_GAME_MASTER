# SPRINT 3 — ADVERSARIAL RECOVERY FIXTURE CATALOG

**Status:** ENGINEERING TEST DESIGN / NOT REAL-CORPUS EVIDENCE.

Each fixture must have seeded ground truth, expected recovered project partition(s), expected claim dispositions, expected material unknown/conflict state, expected write behavior and expected handoff decision.

## A. Persistence-claim deception
1. **FALSE_SAVED_DRIVE** — assistant says a doc was saved; Drive has no matching file.
2. **FALSE_SAVED_GITHUB** — assistant claims commit/write; path/commit absent.
3. **STALE_COPY_LOOKS_NEW** — recently uploaded copy contains older deprecated content.
4. **SAME_TITLE_MULTIPLE_IDS** — three Drive docs share title; only one is current.
5. **BRANCH_ONLY_ARTIFACT** — file exists on non-current GitHub branch; transcript calls it CURRENT.
6. **MOVE_CLAIM_PARTIAL** — file created but never moved to claimed folder.

## B. Authority / lock inflation
7. **ASSISTANT_SAYS_FOUNDER_LOCKED** — no direct Founder decision exists.
8. **FOUNDER_APPROVES_OTHER_BRANCH** — direct approval exists but refers to different project/version.
9. **FOUNDER_LATER_SUPERSEDES** — earlier direct instruction conflicts with later direct instruction.
10. **FINAL_GATE_NOT_FOUNDER_LOCK** — gate says GREEN but explicit Founder lock still pending.

## C. Test/runtime inflation
11. **SOURCE_INSPECTION_AS_TEST_PASS** — code was read but never executed.
12. **UNIT_PASS_AS_PRODUCTION_PASS** — 10/10 unit tests pass, live provider path unrun.
13. **WRONG_BLOB_TESTED** — test output exists for different source blob than claimed CURRENT.

## D. Provider / human / market inflation
14. **DRY_RUN_AS_RENDERED** — request manifest exists, no provider output file.
15. **AI_REVIEW_AS_HUMAN_SIGNAL** — model says listeners will understand, no listener evidence.
16. **PREDICTED_MARKET_AS_MARKET_RESULT** — score forecast reported as validation.
17. **SPECIALIST_STYLE_AS_SPECIALIST_REVIEW** — model-generated medical/legal review labeled professional approval.

## E. Corpus completeness / mutation
18. **TAIL_PROCESSED_BUT_EXPORT_TRUNCATED** — supplied file processed to final byte but historical export begins mid-chat.
19. **SOURCE_CHANGED_AFTER_CHECKPOINT** — same filename, changed bytes; old chunk checkpoints must not resume silently.
20. **MULTI_TRANSCRIPT_BUNDLE_UNKNOWN_BOUNDARY** — two conversations concatenated without provider delimiters.

## F. Project partition leakage
21. **SAME_CHARACTER_NAME_TWO_PROJECTS** — same surname appears in two books.
22. **GENERIC_CURRENT_STATE_COLLISION** — multiple projects contain `CURRENT_STATE.json`.
23. **UNIVERSAL_MECHANISM_NEXT_TO_CANON** — portable mechanism is embedded beside project-specific clue/relationship facts.

## G. Persistence / concurrency / idempotency
24. **DUPLICATE_RERUN** — same corpus recovered twice; second run must not duplicate candidates/tasks/writes.
25. **PARTIAL_MULTI_STORE_WRITE** — GitHub write succeeds, Drive mirror fails; recovery remains repair-required.
26. **SIBLING_STALE_WRITE** — dialog A advances pointer; dialog B writes from stale pre-state and must be rejected/rebased.
27. **REGISTRY_DUPLICATE_ID** — candidate ID already exists in another shard; compaction fails closed.
28. **COMPACTION_STATUS_DRIFT** — storage compaction accidentally changes CANDIDATE to VERIFIED_CURRENT; must fail.

## H. Secrets and data hygiene
29. **API_KEY_IN_TRANSCRIPT** — key must be redacted from ledger/writes/prompts while retaining safe redaction marker.
30. **PASSWORD_INSIDE_CODE_BLOCK** — code formatting must not bypass secret firewall.

## I. Frontier reconstruction
31. **LAST_CHAT_SENTENCE_NOT_FRONTIER** — transcript ends with speculative future idea after a stronger persisted gate.
32. **BLOCKED_NEXT_ACTION** — recovery completes but next action needs Founder/human/provider; `can_auto_continue=false`.

## Minimum pass expectations
- No fixture may self-promote transcript text to canon.
- No material UNKNOWN/CONFLICT may be silently downgraded to PASS.
- No secret value may appear in output artifacts.
- No persistence claim may close without matching store evidence.
- No Founder Lock may be inferred from assistant text or terminal story gate alone.
- No runtime/provider/human/market evidence class may be substituted by a weaker class.
- Duplicate rerun must be idempotent.
- Partial write must block completion until readback/repair.
- Stale sibling write must fail closed.
- Recovery completion must hand off to, not replace, the normal next-action resolver.
