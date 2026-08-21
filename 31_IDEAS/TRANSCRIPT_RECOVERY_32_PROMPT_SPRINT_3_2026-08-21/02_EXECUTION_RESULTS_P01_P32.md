# SPRINT 3 — SEQUENTIAL EXECUTION RESULTS P01–P32

**Execution rule:** each prompt was executed in order after a freshness/rebase read of the durable GitHub/Drive frontier. A BLOCKED result is a completed, honest execution when required evidence is unavailable.

## P01 — Fresh Recovery Frontier Rebase
**Result:** PASS.

Current durable frontier separates four layers correctly:
1. **VERIFIED CURRENT first pass:** 18B protocol + `tools/ivdivo_transcript_recovery.py` / v1 ledger behavior.
2. **WORKING semantic candidate:** SI-0009 in draft PR #67; 11/11 exact-source unit smoke is engineering evidence only.
3. **CURRENT registry-family architecture:** base + extension shards; SI-0008..0011 are addressable through the family pointer, but status remains candidate-specific.
4. **Production evidence gate:** first real large transcript pilot remains unavailable/unrun.

Merged PR #77 supplies broader self-improvement mechanisms. Open PR #78 overlaps several generic evidence/routing/story contracts and explicitly reports real-transcript N11/N12 blocked. **Do-not-repeat:** another first-pass extractor, another top-level recovery engine, synthetic Human/provider/market evidence.

## P02 — Cross-Sprint Semantic Dedupe
**Result:** PASS_DEDUPE.

Semantic dedupe found:
- 18B/v1 extractor: KEEP CURRENT.
- SI-0009 reconciliation/completion gate: KEEP AS PRIMARY SEMANTIC CANDIDATE; do not rebuild in Sprint 3.
- SI-0010 registry compaction transaction: KEEP AS CANDIDATE; Sprint 3 tightens prerequisites but does not claim implementation.
- SI-0011 real-corpus pilot: KEEP AS OPEN PILOT.
- PR #77 state adapter/evidence/transactional mechanisms: REUSE where generic.
- PR #78 boot/evidence/story schemas: REFERENCE/REUSE, not duplicate.

New unique Sprint-3 work is therefore limited to recovery-operational contracts, adversarial recovery fixtures and **cycle-level dedupe/information-gain governance**.

## P03 — Recovery Authority Surface Map
**Result:** PASS.

Authority capability map:
- Founder newest direct instruction: can choose/lock/reject; cannot be inferred from silence/model paraphrase.
- Project source-of-truth/locked canon: controls project facts and branch.
- 18B/v1: may extract and label claims; may not certify canon/persistence.
- SI-0009 candidate: may model reconciliation/completion in candidate tests; not CURRENT authority.
- GitHub/Drive connectors: may verify actual persisted artifact claims within accessible scope; cannot certify Founder intent or human/market facts unless those facts are stored as actual evidence.
- Registry family: routes candidate lifecycle records; does not promote them.
- Next-action resolver: executes only after recovery handoff and still obeys real gates.

## P04 — Missing-Gate Analysis
**Result:** PASS_MAJOR_FINDING.

Ranked missing gates:
1. **FIRST_REAL_LARGE_CORPUS PILOT** — decisive production evidence, currently blocked.
2. **SI-0009 integration/adversarial regression** — candidate exists but is not current.
3. **Connector verification adapters** — contracts need concrete GitHub/Drive implementation/regression.
4. **Transactional persistence/compaction integration** — safe state mutation and readback under concurrency.
5. **Package/main coherence** — only after selected current extensions are proven.

Conclusion: **another parser expansion is not the bottleneck.**

## P05 — Source Completeness Classifier
**Result:** PASS_CONTRACT.

Required separate fields:
- `supplied_input_tail_processed`;
- `supplied_corpus_coverage = COMPLETE_AS_SUPPLIED | PARTIAL_AS_SUPPLIED | UNKNOWN`;
- `original_conversation_completeness = PROVEN_FULL | KNOWN_PARTIAL | UNKNOWN`;
- `completeness_basis`;
- `truncation_indicators`.

Rule: processing every byte supplied by the user proves only the supplied corpus was processed; it does not prove the historical conversation export was complete.

## P06 — Multi-Transcript Bundle Splitter Contract
**Result:** PASS_CONTRACT.

A bundle must split into `source_units[]` before project reconciliation. Boundaries may be `PROVIDER_EXPLICIT`, `USER_EXPLICIT`, `STRUCTURALLY_INFERRED`, or `UNKNOWN`. Structural inference may create a working partition but may not invent missing turns or claim a full transcript boundary. Ambiguous neighboring fragments remain linked by provenance rather than silently concatenated.

## P07 — Multi-Project Partition Contract
**Result:** PASS_CONTRACT.

Each recovered material item must carry:
`source_unit -> project_partition -> domain -> claim/artifact/candidate -> evidence/disposition`.
Cross-project reuse is allowed only after explicit classification `PROJECT_SPECIFIC | PORTABLE_MECHANISM | UNIVERSAL_CANDIDATE`. Plot, clue, relationship, voice and canon facts default PROJECT_SPECIFIC.

## P08 — Cross-Project Leakage Red Team
**Result:** PASS_REDTEAM.

Hard cases identified:
- same character surname in different books;
- same generic filename `CURRENT_STATE.json` in different directories;
- same prompt name copied across projects;
- shared engine mechanism mentioned beside project-specific canon;
- one transcript jumping between ROOM917, D09, D10 and engine work without headings.

Fail-closed rule: ambiguous evidence cannot cross partitions merely because names match. Require project locator/context or mark `PARTITION_UNRESOLVED`.

## P09 — Chronology + Supersession Resolver
**Result:** PASS_CONTRACT.

Resolution requires both **authority rank** and **chronology within that rank**. Newer lower-authority assistant prose cannot supersede older direct Founder instruction. Later direct Founder instruction may supersede earlier direct Founder instruction. Persisted project terminal gate can supersede an older aggregate pointer, but cannot create Founder Lock if the gate itself says approval is pending.

## P10 — Artifact Identity / Same-Name Ambiguity
**Result:** PASS_CONTRACT.

Strong identity keys ranked:
1. provider-native file/document/repo path + immutable ID/hash;
2. durable URL + version/blob/revision identity;
3. content hash + contextual project locator;
4. visible title only = weak/ambiguous.

A newly uploaded copy of an old file is not automatically the newest authority.

## P11 — SAVED / CREATED / UPDATED Claim Evidence Contract
**Result:** PASS_CONTRACT.

Terminal states:
`VERIFIED_PERSISTED`, `NOT_FOUND`, `AMBIGUOUS_MULTIPLE_MATCHES`, `STALE_OR_SUPERSEDED_COPY`, `ACCESS_UNVERIFIABLE`, `CONFLICT`, `UNKNOWN`.
A model statement “saved to Drive/GitHub” creates a verification task; it never closes it.

## P12 — Founder LOCK / Approval Claim Contract
**Result:** PASS_CONTRACT.

Valid evidence requires a direct Founder decision attributable to the relevant project/version/branch. States:
`DIRECT_APPROVAL`, `DIRECT_REJECTION`, `DIRECT_REVISION_REQUEST`, `NO_DECISION_EVIDENCE`, `AMBIGUOUS_SCOPE`, `SUPERSEDED_DECISION`.
Assistant statements, implied satisfaction and model consensus cannot produce Founder Lock.

## P13 — Test PASS / Runtime Claim Contract
**Result:** PASS_CONTRACT.

Minimum runtime evidence for a reproducible automated PASS:
- exact source/version/blob identity;
- exact harness/test identity;
- executed command or equivalent runner identity;
- output summary;
- exit status;
- environment/version notes sufficient to distinguish inspection from execution.
Unit PASS does not prove production correctness, literary quality or provider behavior.

## P14 — Provider / Human / Market Evidence Firewall
**Result:** PASS_CONTRACT.

Non-substitution matrix locked:
- API/schema discovery != live provider output;
- dry run != paid/live render;
- model auditory prediction != listening result;
- AI review != Human Signal;
- one human taste comment != repeated population evidence;
- specialist-like model prose != specialist review;
- market forecast != observed market behavior.

## P15 — UNKNOWN + CONFLICT as First-Class States
**Result:** PASS_CONTRACT.

Materiality must be attached to the decision/gate affected, not chosen for convenience. A non-material unknown may remain open only if it cannot change current authority, canon, persistence truth or next legal action. Material UNKNOWN/CONFLICT blocks `INGESTION_COMPLETE`.

## P16 — Secret / Sensitive Persistence Firewall
**Result:** PASS_CONTRACT.

Recovery ledger stores `REDACTED_SECRET_PRESENT` + source range/fingerprint category, never the secret value. API keys, passwords, tokens, private credentials and equivalent secrets are excluded from writes, logs, prompt packs and learning artifacts. Redaction does not convert the surrounding transcript into trusted evidence.

## P17 — Transactional Recovery Write Manifest
**Result:** PASS_CONTRACT.

Candidate transaction fields:
`recovery_id`, `operation_id`, `target_store`, `target_locator`, `expected_pre_identity`, `intended_delta_hash`, `idempotency_key`, `reversibility`, `apply_status`, `post_readback_identity`, `verification_status`, `rollback_status`.
No current-pointer mutation is terminal until readback matches intent.

## P18 — Readback / Rollback Gate
**Result:** PASS_CONTRACT.

States:
`NOT_ATTEMPTED -> APPLIED_UNVERIFIED -> READBACK_PASS | READBACK_MISMATCH -> ROLLBACK_REQUIRED | MANUAL_REPAIR_REQUIRED`.
API success alone is insufficient. Partial multi-store persistence keeps recovery in repair state.

## P19 — Recovery Idempotency Contract
**Result:** PASS_CONTRACT.

Primary idempotency tuple:
`source_sha256 + source_unit_id + project_partition_id + material_item_fingerprint + target_locator + operation_kind`.
A corrected source hash creates a new lineage linked by `supersedes_recovery_id`; it must not silently reuse checkpoints from the old bytes.

## P20 — Source Mutation + Resume Gate
**Result:** PASS_CONTRACT.

Resume is allowed only when source identity matches and chunk lineage is intact. Changed bytes -> `SOURCE_CHANGED_RECONCILIATION_REQUIRED`. Unchanged verified prefix may be reused only if prefix identity is independently proven; otherwise restart semantic reconciliation. Tail completion and historical-export completeness remain separate.

## P21 — Concurrent Sibling Write Collision
**Result:** PASS_CONTRACT.

Concurrency law:
1. fresh-read target identity;
2. prefer unique branch/shard for additive work;
3. expected pre-state token for mutation;
4. reject stale write;
5. rebase/reconcile newer main;
6. never force-overwrite newer state merely to preserve an older sprint.

This is validated by current repository behavior: multiple sibling branches are active simultaneously, so stale-base risk is operational, not hypothetical.

## P22 — Registry Shard / Compaction Transaction
**Result:** PASS_CANDIDATE.

Current base+extension family is the safer concurrent-write model. Compaction may occur only after:
- unique candidate IDs across base/shards;
- schema compatibility;
- deterministic sorted build;
- input shard hashes recorded;
- output hash recorded;
- roundtrip lifecycle validation;
- pointer switch transaction + readback;
- rollback to previous family pointer.

Compaction changes storage form, not candidate lifecycle status.

## P23 — Adversarial Recovery Fixture Catalog
**Result:** PASS_FIXTURE_DESIGN.

A fixed catalog of 24 fixture families was produced in `04_ADVERSARIAL_FIXTURE_CATALOG.md`, including false SAVED/LOCK/PASS claims, missing tail, mixed projects, same-name files, stale mirrors, secret leakage, source mutation, duplicate chat-only persistence, fake provider/human/market evidence and concurrent races.

## P24 — Synthetic Large-Corpus Fixture Strategy
**Result:** PASS_FIXTURE_DESIGN.

Synthetic corpus may test scale, chunking, reconciliation and known-ground-truth failure detection. It must include seeded truth labels and expected dispositions. It **cannot** close the real-corpus pilot because real historical messiness, provider formatting and recovery-value distribution are not represented by construction.

## P25 — First Real Large Transcript Pilot Protocol
**Result:** BLOCKED_REAL_CORPUS.

Protocol is ready, but no genuinely large exported/pasted prior AI transcript is available here as an ingestable artifact. Current conversation summaries/project context are not substituted for that artifact because doing so would invalidate the evidence claim.

Required first pilot output:
`source identity -> v1 extraction -> semantic partitions -> claim verification -> chat-only candidates -> transactional persistence -> readback -> reconstructed frontier -> next-action handoff -> defect/learning log`.

## P26 — Connector Verification Adapter Contract
**Result:** PASS_CONTRACT_IMPLEMENTATION_PENDING.

Defined common adapter outcomes:
`FOUND_EXACT`, `FOUND_MULTIPLE`, `NOT_FOUND`, `ACCESS_DENIED_OR_UNAVAILABLE`, `CONTENT_UNREADABLE`, `IDENTITY_MISMATCH`, `READBACK_MATCH`, `READBACK_MISMATCH`.
GitHub adapter needs repo/path/ref/blob semantics; Drive adapter needs file ID/revision/parent/content semantics. Contract exists; a unified executable adapter is **not claimed implemented** in this sprint.

## P27 — Recovery → Next-Action Handoff Contract
**Result:** PASS_CONTRACT.

`INGESTION_COMPLETE` means the recovery layer has safely reconstructed state. It does not mean the production action is executable. Handoff payload requires:
`active_project`, `authority`, `last_verified_completed`, `open_real_gate`, `next_legal_action`, `requires_founder`, `requires_human`, `requires_provider`, `requires_external_fact`, `do_not_repeat`.
The normal resolver owns the final execute/stop decision.

## P28 — Learning Harvest Without Canon Leakage
**Result:** PASS_ROUTING.

Reusable failure/mechanism candidates may enter Learning Ledger/Improvement Registry only with provenance, dedupe relation, evidence state, owner, next action and next gate. Project-specific story material remains project-specific unless separately abstracted as a mechanism. Recovery never universalizes canon automatically.

## P29 — Founder Question Minimizer
**Result:** PASS_POLICY.

Ask Founder only when a real decision cannot be recovered or verified:
- conflicting direct Founder directives;
- materially missing canon fact;
- equally authorized branch choice;
- explicit irreversible approval.
Do not ask Founder to re-find files, repeat known state, classify obvious duplicates, or verify persistence when connected tools can do it.

## P30 — Repeated 32→64 Cycle Dedupe Audit
**Result:** PASS_MAJOR_FINDING.

Repository evidence shows several simultaneous 32→64 research branches across whole-system, audio and project domains. This is productive when scopes differ, but creates four systemic risks:
1. duplicated mechanisms under different names;
2. stale-base PR debt;
3. prompt-count growth outrunning real evidence;
4. integration/pruning burden exceeding invention burden.

New cycle rule: before another meta sprint, compute `scope_overlap`, `new_evidence_available`, `unimplemented_unique_mechanisms`, `external_dependency`, `expected_information_gain`. A new cycle without new evidence must state that it is design hardening, not production validation.

## P31 — Marginal Information Gain Stop Gate
**Result:** PASS_POLICY.

Default STOP/HOLD when all are true:
- next decisive dependency is external/real evidence;
- no new source or runtime surface has appeared;
- proposed prompts mostly restate existing candidates;
- implementation/pruning queue is larger than invention queue.

Founder direct instruction may authorize another cycle regardless, but outputs remain WORKING and the system must not portray quantity as stronger evidence. The 64 prompts derived here are therefore a **candidate queue**, not an instruction to run all 64 mechanically.

## P32 — Promotion / Hold Decision + Roadmap
**Result:** PASS_HOLD_PROMOTION.

### Accepted now as Sprint-3 design results
- source completeness separation;
- project/bundle partition rules;
- claim/evidence contracts;
- transactional/readback/idempotency contracts;
- adversarial fixture catalog;
- recovery→next-action handoff contract;
- cycle dedupe + marginal-information stop gate.

### Hold / candidate
- SI-0009 semantic reconciliation promotion;
- SI-0010 compaction transaction;
- unified connector verification adapter;
- package integration.

### Real blocker
- first real large transcript operational pilot.

### New candidates
- **SI-0012 — Recovery Operational Pilot Harness**: binds real corpus, connector verification, transactional readback and next-action handoff without replacing 18B/SI-0009.
- **SI-0013 — Research Cycle Dedupe + Information-Gain Gate**: prevents repeated 32→64 prompt multiplication from outrunning evidence/integration.

### Final Sprint-3 verdict
- FATAL: 0.
- MAJOR: 4 operational gaps: real-corpus evidence absent; SI-0009 not current; connector adapter implementation pending; cycle/WIP duplication risk.
- 32/32 prompts executed/dispositioned.
- Exactly 64 next prompts derived in `06_NEXT_64_PROMPTS_S4.md`.
