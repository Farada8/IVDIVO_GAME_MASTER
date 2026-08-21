# IVDIVO — 32 PROMPTS EXECUTED SEQUENTIALLY

Status: COMPLETED INTERNAL RESEARCH/RED-TEAM SPRINT
Date: 2026-08-21
Basis: current 18B protocol, current executable transcript-recovery tool/schema/tests, current Self-Improvement v2 and current cross-dialog/persistence law.

Important evidence boundary: these are design/review findings. They do not fabricate human/provider/market evidence. Existing deterministic extractor has 5/5 exact-source tests; proposed upgrades below require their own implementation/tests.

---

## P01 — Authority reconstruction — EXECUTED
**Finding:** The protocol correctly says transcript != authority, but recovery needs a formal two-axis model: `SOURCE AUTHORITY` and `PERSISTENCE/VERIFICATION STATE`. A direct Founder statement can have high authority while still being recovered from a pasted corpus; an assistant `LOCKED/PASS` claim has low authority regardless of wording.
**Decision:** Add an `authority_class` plus `verification_state`; never collapse them into one confidence score.
**Target algorithm:** Founder chronology first -> locked project authority -> current domain/project source -> verified state pointer -> chat-only candidate -> assistant/external finding. Any unresolved contradiction affecting canon = `AUTHORITY_UNRESOLVED`.

## P02 — Completeness and tail detection — EXECUTED
**Finding:** `final_tail_processed=true` currently proves only that the parser reached the end of the supplied file, not that the supplied file is the complete old conversation.
**Decision:** Split `INPUT_TAIL_PROCESSED` from `SOURCE_COMPLETENESS_PROVEN`. `FULL_TRANSCRIPT` must be user/provider-declared or supported by structural evidence; otherwise remain `UNKNOWN_COMPLETENESS`.
**Upgrade:** add `first_turn_signature`, `last_turn_signature`, `truncation_indicators`, `completeness_basis`.

## P03 — Role and chronology parsing — EXECUTED
**Finding:** Current role regex is useful but nested quotes, copied assistant text inside user turns, generated system summaries and external-model blocks can create false speaker attribution.
**Decision:** Maintain `outer_turn_role` and optional `embedded_source_role`; only outer Founder/user turns may create direct Founder directives unless an embedded original turn is explicitly recovered with provenance.
**Upgrade:** chronology key = transcript order + source timestamp when available, never timestamp alone.

## P04 — Artifact-claim verification — EXECUTED
**Finding:** Current `verification_queue` has only kind/reference/action. It cannot record store attempted, expected identity, result, evidence locator, supersession or mismatch.
**Decision:** Introduce `verification_task_id`, `store`, `expected_identity`, `result`, `evidence_ref`, `checked_at`, `superseded_by`, `notes`.
**Route:** GitHub path/commit/PR -> GitHub; Drive ID/doc title -> Drive; File Library pointer -> Library; provider/render claim -> provider artifact/evidence; human/market claim -> explicit external evidence only.

## P05 — Chat-only artifact recovery — EXECUTED
**Finding:** Main risk is either dropping substantial work or over-promoting it.
**Decision:** Use `CHAT_ONLY_CANDIDATE` with a content fingerprint and smallest recoverable artifact boundary. Preserve exact material when complete; preserve fragments with `UNKNOWN_GAPS` when incomplete.
**Rule:** Candidate may be persisted automatically, but canon/lock promotion requires normal project gates.

## P06 — Semantic deduplication — EXECUTED
**Finding:** File-name dedupe is insufficient. Same work may be renamed; different work may share a title.
**Decision:** Dedupe on `project + artifact_type + semantic purpose + source lineage + content fingerprint + protected invariants`.
**Disposition order:** SAME_CURRENT -> DUPLICATE -> EXTENSION -> NEWER_STRONGER_COMPATIBLE -> OLDER_STALE -> COMPETING_ALTERNATIVE -> CONFLICT.

## P07 — Freshness and supersession — EXECUTED
**Finding:** Modified dates are low-trust. Project-specific passed gates can legitimately outrank older aggregate state without rewriting stable system law.
**Decision:** Freshness weight order: explicit Founder override > project authority/gate lineage > source/version/hash lineage > content state > timestamps/filename labels.
**Rule:** Rebase volatile frontier; do not overwrite stable higher-level law merely because a project artifact is newer.

## P08 — Secret/privacy firewall — EXECUTED
**Finding:** Current regex redaction catches common token shapes but cannot guarantee all secrets or personal/private data classes.
**Decision:** Keep deterministic regex as first layer, then semantic `SECRET_OR_CREDENTIAL` pass before persistence. Store only `credential_required=true`, service/domain if needed, never secret value.
**Hard fail:** any candidate/write artifact containing detected raw secret must be blocked.

## P09 — Concurrent-dialog write safety — EXECUTED
**Finding:** Real project history already demonstrated stale-SHA conflicts. Concurrency is normal, not exceptional.
**Decision:** Every material write follows `READ CURRENT -> capture revision/SHA -> WRITE CONDITIONAL -> on conflict REFETCH -> DIFF -> REBASE -> retry or branch/PR`. Never force-update shared current state.
**Drive rule:** use revision-aware writes where supported; GitHub fallback branch+PR when main advances repeatedly.

## P10 — Cross-dialog delta scan — EXECUTED
**Finding:** Searching all Drive/GitHub on every action would become expensive ritual.
**Decision:** Bounded freshness sweep at boot/material gates using current project name, active authority pointers, recent commits/docs and known sibling surfaces. Expand only on evidence of mismatch/missing work.
**Stopping rule:** stop scan when current frontier is supported by current project authority and no newer compatible material delta is found in bounded sources.

## P11 — Multi-project transcript bundle — EXECUTED
**Finding:** One long chat can contain several projects; a single frontier field is unsafe.
**Decision:** Recovery ledger needs `project_partitions[]`, each with project ID, branch/line, directives, artifact claims, candidate outputs, conflicts, frontier and next action.
**Hard rule:** no artifact crosses partitions without explicit universalization/reuse classification.

## P12 — External-AI provenance — EXECUTED
**Finding:** Model agreement is frequently mistaken for independent evidence.
**Decision:** Each external finding records model, source version/hash, task, whether prior verdict was visible, evidence family, diagnosis and proposed fix separately.
**Rule:** same source + same assumption + repeated agreement = one evidence family, not triangulation.

## P13 — Claim taxonomy and confidence — EXECUTED
**Finding:** Current classes are broadly adequate but need state metadata. Numeric confidence would falsely imply authority precision.
**Decision:** Use categorical `extraction_confidence: HIGH/MEDIUM/LOW` only for parser quality, separate from `authority_class` and `verification_state`.
**New useful classes:** `PERSISTENCE_CLAIM`, `PROVIDER_EXECUTION_CLAIM`, `HUMAN_SIGNAL_CLAIM`, `FRONTIER_CLAIM` as subtypes.

## P14 — Artifact identity contract — EXECUTED
**Finding:** Recovery cannot safely reconcile artifacts without identity lineage.
**Decision:** Minimum common tuple: `store, locator, project, artifact_type, status, version/revision/hash if available, source_parent, branch/line, created/modified metadata, gate/result if relevant`.
**Mandatory:** locator/project/type/status. Hash mandatory for protected source/render/package where available; not mandatory for native Docs lacking stable content hash.

## P15 — Founder-directive extractor — EXECUTED
**Finding:** Keyword extraction alone can misclassify discussion or quoted commands.
**Decision:** Direct Founder directives require outer user/Founder role + imperative/approval/rejection/lock semantics + chronological context. Assistant summaries become `PARAPHRASED_DIRECTIVE_CLAIM`, never direct Founder authority.
**Escalate:** contradictory Founder directives with unresolved chronology -> decision gate.

## P16 — LOCK/PASS/status verifier — EXECUTED
**Finding:** Words `FINAL`, `GREEN`, `LOCKED`, `PASS`, `READY` are semantically overloaded.
**Decision:** Introduce `claim_type` and evidence contract. `STORY_GATE_PASS` needs gate artifact/result; `FOUNDER_LOCK` needs direct Founder approval; `TEST_PASS` needs test evidence; `PROVIDER_RENDERED` needs provider/output artifact; `HUMAN_PASS` needs actual human signal.
**Rule:** filename labels never satisfy evidence contract by themselves.

## P17 — Recovery Ledger schema audit — EXECUTED
**Finding:** Current schema is intentionally first-pass and is missing semantic-reconciliation state required by 18B. Missing: recovery_id, chunk/checkpoint state, project partitions, conflicts/unknowns, verified artifacts, chat-only dispositions, writes performed, readback, current frontier, exact next obligation, superseded items, system candidate promotion relation.
**Decision:** Keep schema v1 as extractor schema; create a separate reconciled ledger schema v2 rather than bloating the deterministic first-pass contract.
**Architecture:** `EXTRACT_LEDGER_v1 -> RECONCILED_RECOVERY_STATE_v2`.

## P18 — Parser adversarial robustness — EXECUTED
**Finding:** Existing 5 tests cover secret redaction, simple role/directive, unverified save claim, tail/hash and system-improvement discovery. They do not cover nested quotes, malformed labels, Markdown/code, mixed languages beyond simple RU/EN, prompt-like fake paths, multi-project bundles or huge inputs.
**Decision:** Build adversarial fixture corpus. Parser must prefer false negatives over false authority promotion.
**New tests:** quoted assistant claim inside user turn; code block containing `Assistant:`; duplicate filenames; Unicode role labels; secret variants; generated big-paste headers; embedded JSON; 100k+ line chunk simulation.

## P19 — Very-large transcript chunking — EXECUTED
**Finding:** A monolithic parser can process a file locally, but semantic AI reconciliation may exceed context. Recovery needs resumable chunk state.
**Decision:** `source_sha256 + chunk_id + byte/line range + overlap_hash + processed_at + findings_hash + tail_flag`.
**Rule:** chunks are immutable slices of one source identity; if source hash changes, old checkpoints cannot silently continue.

## P20 — Context compaction — EXECUTED
**Finding:** Keeping every raw conversation forever as authority would create noise and privacy risk.
**Decision:** Retain source fingerprint/provenance, material Founder directives, artifact/verdict map, unresolved gaps, recovered candidates, system learnings and frontier. Raw corpus may remain user-provided/archive but is not copied into canon/normal operational docs.
**Compaction gate:** every material item must have disposition before raw context can be dropped from active working memory.

## P21 — Project frontier reconstruction — EXECUTED
**Finding:** “Where we stopped” is a derived state, not the last assistant sentence.
**Decision:** Frontier tuple: `last_verified_completed_artifact + current authority + passed gates + unresolved blockers + do_not_repeat + next legal unblocked action`.
**Algorithm:** reconstruct from persisted artifacts first; transcript may fill missing candidate work but cannot override a newer verified frontier.

## P22 — Coupling to next-action resolver — EXECUTED
**Finding:** Automatic continuation after recovery is unsafe until reconciliation finishes.
**Decision:** next-action resolver may receive recovery state only after `recovery_status=INGESTION_COMPLETE`, `authority_unambiguous=true`, `frontier_fresh=true`, required write/readbacks green and no unresolved material conflicts.
**Fail closed:** `EXTRACTED_UNVERIFIED` or `RECONCILING` must STOP continuation of state-changing production actions.

## P23 — Self-improvement harvest — EXECUTED
**Finding:** Recovery itself is a rich sensor for repeated context loss, duplicate work and false persistence claims.
**Decision:** Harvest only abstract reusable mechanisms. Each candidate needs source provenance, dedupe relation, scope, evidence family, application target and rollback.
**Do not universalize:** plot, characters, culprit, clue chains, voice IDs, exact project chronology.

## P24 — Improvement Registry integration — EXECUTED
**Finding:** Current central registry is a large minified file; previous work avoided risky whole-file reconstruction by writing SI-0008 as a shard. That is safe but creates index/registry divergence.
**Decision:** Move toward `registry index + candidate shards + compaction build` or an atomic utility that loads current registry, inserts candidate, audits, writes temp, validates, then replaces. Never manual whole-file recreation.
**Priority:** MAJOR tooling hygiene because it affects anti-loss guarantees.

## P25 — Learning Ledger integration — EXECUTED
**Finding:** Registry answers “what improvement candidate exists / what next”; Learning Ledger should answer “what actually happened / what was learned”.
**Decision:** Record events such as stale-write collision, claim-not-found, successful chat-only recovery, secret caught, duplicate prevented, frontier corrected. Link events to candidate IDs rather than duplicating candidate bodies.
**Rule:** observation != promotion.

## P26 — Test strategy — EXECUTED
**Finding:** Five unit tests are a good seed, not sufficient production evidence.
**Decision:** seven layers: unit parser -> schema validation -> adversarial/property fixtures -> simulated connector reconciliation -> concurrency/stale-write -> end-to-end synthetic corpus -> real pasted corpus monitoring.
**Evidence separation:** automated tests prove contracts, not literary/canon correctness.

## P27 — Observability and metrics — EXECUTED
**Finding:** Useful metrics must diagnose loss/error, not reward volume.
**Decision:** track `material_items_found`, `% dispositioned`, verified/missing/superseded claims, chat-only candidates persisted, duplicates prevented, unresolved conflicts, secrets blocked, stale writes/rebases, frontier corrections, repeat-work avoided, recovery elapsed/tool calls.
**Anti-metric:** number of prompts/files created is not success.

## P28 — Failure, rollback and repair — EXECUTED
**Finding:** Recovery can partially write several surfaces before discovering conflict.
**Decision:** assign `recovery_id` to all writes; preserve previous current pointers; use candidate status until final reconciliation; log write set; on failure mark `PARTIAL_WRITE_REPAIR_REQUIRED`, re-read every touched artifact, reverse/repair only affected writes.
**Idempotence:** rerunning same source SHA should not create duplicate candidates/artifacts.

## P29 — Human/Founder decision gates — EXECUTED
**Finding:** Most recovery work should not bother Founder. Questions are justified only when higher-authority directives conflict, missing exact content changes canon, irreversible external action is required, or multiple competing creative branches remain equally authorized.
**Decision:** missing assistant details, duplicate files, stale pointers, artifact existence and ordinary routing are system responsibilities.
**Goal:** `ASK ONLY FOR REAL CHOICE, NOT FOR RECOVERABLE STATE`.

## P30 — Packaging/versioning — EXECUTED
**Finding:** Transcript recovery is post-v11.2 verified extension; retroactive package relabeling would corrupt provenance.
**Decision:** next package should bump release (candidate v11.3 or later), include protocol/tool/schema/tests, migration note and full-package regression. Keep v11.2 immutable.
**Gate:** no package promotion until clean unzip/full regression + exact manifest/hash evidence.

## P31 — First real large-corpus pilot — EXECUTED
**Finding:** The most important missing evidence is operational performance on a real abrupt-chat paste.
**Decision:** Pilot records source completeness, extractor result, material-item manual/AI reconciliation, persisted-claim accuracy, missed/false items, secret behavior, dedupe quality, frontier reconstruction, writes/readbacks and Founder questions required.
**Acceptance:** zero false canon/LOCK/PASS promotion; zero secret persistence; all material items dispositioned; no duplicate current artifacts; correct frontier; substantially reduced Founder reconstruction burden.

## P32 — End-to-end Red Team and roadmap — EXECUTED
**FATAL:** none in the current conceptual separation, provided extractor cannot self-promote authority.
**MAJOR:** (1) no reconciled ledger v2; (2) central Improvement Registry atomic/shard/index weakness; (3) first real large-corpus pilot not yet performed; (4) adversarial parser/connector/concurrency suite too small; (5) automatic coupling to next-action resolver not formally gated by recovery completion.
**MEDIUM:** completeness basis ambiguity; multi-project partitioning; observability; claim-type evidence contracts; context compaction policy.
**POLISH:** naming/CLI ergonomics and reporting layout.

### Priority roadmap from all 32 executions
1. Build `RECONCILED_RECOVERY_STATE_SCHEMA_v2` + semantic reconciliation contract.
2. Harden extractor tests with adversarial/mixed/large-corpus fixtures.
3. Add resumable chunk/checkpoint model for huge transcripts.
4. Add formal claim-evidence contracts and verification-task results.
5. Integrate recovery-completion gate into next-action resolver.
6. Repair Improvement Registry atomicity/sharding/indexing.
7. Run first real pasted-corpus production pilot and log Learning Ledger evidence.
8. Only then package into next engine ZIP after full regression.

### Studio guard
Do not turn recovery research into endless meta-work. Once these enabling controls are sufficient, return to the highest unblocked story/audio production obligation. The recovery system exists to preserve and accelerate production, not to replace it.
