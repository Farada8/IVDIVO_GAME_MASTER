# SPRINT 4 CANDIDATE QUEUE — EXACTLY 64 NEXT PROMPTS

**Status:** WORKING CANDIDATE / DEPENDENCY-AWARE. These prompts are derived from Sprint-3 evidence. They are not automatically authorized for mechanical execution as a block. Before each prompt: freshness read, semantic dedupe, dependency check, evidence-class check, sibling-owner check.

## BLOCK A — FIRST REAL CORPUS / OPERATIONAL PILOT

### S4-01 — Real Corpus Intake Gate
When a genuine exported/pasted large prior AI transcript becomes available, verify source identity, declared completeness and safe handling before parsing. Output GO/HOLD and immutable source manifest.

### S4-02 — v1 Extraction on Real Corpus
Run the verified v1 transcript extractor on the exact source; record source/blob identity, output ledger identity and parser warnings. Never promote extracted claims.

### S4-03 — Real Corpus Source-Unit Split
Partition multi-transcript bundles using provider/user boundaries first, structural inference second, UNKNOWN when unresolved. Measure boundary errors against human-inspectable source structure.

### S4-04 — Real Corpus Project Partition
Partition recovered material into projects/domains; detect cross-project leakage and produce unresolved-partition queue.

### S4-05 — Real Founder Directive Recovery
Separate direct Founder directives from assistant paraphrases in the real corpus; preserve chronology and scope; produce no lock decision from paraphrase.

### S4-06 — Real Persistence Claim Queue
Extract every material SAVED/CREATED/UPDATED/LOCK/PASS/RENDERED/HUMAN/MARKET claim into typed verification tasks.

### S4-07 — Real Chat-Only Candidate Recovery
Identify substantial work that exists in transcript but not in durable stores; persist only as candidate with provenance/fingerprint after verification.

### S4-08 — Real Corpus Completion + Handoff Gate
Run the full completion gate, readback, idempotent rerun and next-action handoff. Produce PASS/HOLD/FAIL with defect ledger.

## BLOCK B — CONNECTOR EVIDENCE ADAPTERS

### S4-09 — GitHub Exact-File Verification Adapter
Implement/test adapter mapping recovery claims to repo/path/ref/blob/commit readback outcomes.

### S4-10 — GitHub Branch-vs-Main Authority Adapter
Detect branch-only artifacts and prevent branch existence from being misreported as main/current persistence.

### S4-11 — GitHub Commit/Test Evidence Adapter
Bind claimed runtime PASS to exact source/test commit/blob identities and stored verification evidence.

### S4-12 — Drive Exact-ID Verification Adapter
Implement/test Drive claim verification using file ID, title, MIME, parents, revision/content readback.

### S4-13 — Drive Same-Title Ambiguity Adapter
Return FOUND_MULTIPLE rather than guessing when multiple files share title; resolve only with stronger identity evidence.

### S4-14 — Drive Move/Folder Claim Adapter
Verify that a claimed file move actually changed parent folder; distinguish created-but-not-moved from success.

### S4-15 — Cross-Store Claim Resolver
For claims mirrored to GitHub + Drive, reconcile partial success, version skew and one-store failure without declaring global PASS.

### S4-16 — Adapter Negative Regression Pack
Run false saved, access-unavailable, stale copy, wrong branch, same-title and readback mismatch fixtures across both adapters.

## BLOCK C — SEMANTIC / AUTHORITY ADVERSARIAL TESTS

### S4-17 — False Founder Lock Fixture Runtime
Test that assistant “Founder locked it” language cannot create direct approval state.

### S4-18 — Scope-Ambiguous Founder Approval Runtime
Test approval referring to one branch/version against a similarly named competing branch.

### S4-19 — Superseded Founder Directive Runtime
Test chronology inside equal highest authority and confirm later direct instruction supersedes earlier only within matching scope.

### S4-20 — Final-Gate-vs-Founder-Lock Runtime
Test a GREEN Final Story Gate that explicitly awaits Founder lock; resolver must stop at decision gate.

### S4-21 — Mixed Project Name Collision Runtime
Test identical surnames/file names across unrelated projects and require project locator before transfer.

### S4-22 — Universal Mechanism Extraction Runtime
Test abstraction of a reusable mechanism while project-specific canon remains excluded from universal registry candidate.

### S4-23 — Material UNKNOWN Classification Runtime
Test that an unknown affecting branch/lock/next action blocks completion while a proven non-material formatting unknown does not.

### S4-24 — Authority Confidence vs Parser Confidence Test
Prove a 0.99 extraction-confidence assistant claim remains lower authority than a lower-confidence but directly sourced Founder directive requiring review.

## BLOCK D — TRANSACTIONS / CONCURRENCY / REGISTRY

### S4-25 — Recovery Transaction Helper Implementation
Implement expected-pre-state, delta hash, idempotency, apply, readback and rollback state machine for bounded writes.

### S4-26 — Partial GitHub+Drive Transaction Test
Force one store success and one failure; verify recovery becomes repair-required, not complete.

### S4-27 — Idempotent Rerun Runtime
Run identical recovery twice and verify zero duplicate candidates/tasks/writes on second execution.

### S4-28 — Corrected Export Lineage Runtime
Change source bytes intentionally; verify new recovery lineage and no silent reuse of incompatible checkpoints.

### S4-29 — Concurrent Sibling Stale-Write Test
Simulate/execute two branch writers where one advances target first; second must rebase or fail closed.

### S4-30 — Registry Shard Uniqueness Validator
Validate unique candidate IDs across base registry and all extension shards; fail on duplicate IDs.

### S4-31 — Deterministic Registry Compaction Builder
Build compacted registry from validated shards with input hashes, deterministic ordering and output hash, without changing lifecycle states.

### S4-32 — Registry Pointer Switch + Rollback Pilot
Transactionally switch family pointer to compacted registry in a test/candidate context; read back and roll back on mismatch.

## BLOCK E — SI-0009 INTEGRATION / PACKAGE PROMOTION

### S4-33 — SI-0009 Fresh Rebase Review
Rebase PR #67 candidate concepts against current main; identify superseded pieces and unique remaining delta before merge consideration.

### S4-34 — SI-0009 Schema Validation Audit
Validate schema invariants, enum terminality and illegal completion combinations using adversarial fixtures.

### S4-35 — SI-0009 Next-Action Integration Regression
Connect candidate completion output to current next-action resolver and test STOP/CONTINUE/Founder/Human/Provider gates.

### S4-36 — SI-0009 Secret Firewall Regression
Inject secrets in plain text/code blocks and verify no secret value persists in outputs.

### S4-37 — SI-0009 Multi-Project Corpus Regression
Run candidate reconciliation on a seeded multi-project bundle and verify partition containment.

### S4-38 — SI-0009 Readback Failure Regression
Test completion gate against successful API call followed by mismatching readback.

### S4-39 — SI-0009 Promotion Decision
After adversarial + integration + real-corpus evidence, decide PROMOTE / REVISE / HOLD with exact evidence; no vote-based promotion.

### S4-40 — Next Engine Package Candidate Build
Only after selected extensions become CURRENT, build a fresh package candidate with immutable version/checksum and full cold-unpack regression; never relabel v11.2 retroactively.

## BLOCK F — OBSERVABILITY / MULTI-AI / EVIDENCE QUALITY

### S4-41 — Recovery Telemetry Schema
Instrument corpus size, claims, verification tasks, unresolved items, writes, readbacks, duplicate suppression, time/cost and failures.

### S4-42 — False-Positive Authority Metric
Measure any case where low-authority transcript prose is elevated above durable/direct authority; target zero.

### S4-43 — False-Negative Recovery Metric
Measure substantial chat-only work missed by recovery on known-ground-truth fixtures and real pilot review.

### S4-44 — Partition Leakage Metric
Track project-specific material incorrectly assigned across partitions; target zero material leakage.

### S4-45 — Persistence Verification Yield
Measure fraction of material persistence claims resolved automatically vs manual/Founder/unknown, without downgrading uncertainty to improve metric.

### S4-46 — Multi-AI Source-Parity Recovery Review
Give GPT/Claude/Grok identical source manifest, authority packet and questions; compare independent defects only after parity verification.

### S4-47 — Multi-AI Evidence-Family Dedupe
Collapse several models repeating the same unsupported assumption into one evidence family; do not count consensus as independent proof.

### S4-48 — Recovery Cost/Benefit Baseline
Measure time, token/tool calls, human verification burden, recovered valuable items and avoided duplicate work on real pilots.

## BLOCK G — FAILURE RECOVERY / SECURITY / RESILIENCE

### S4-49 — Truncated Export Detection Stress
Seed beginning/middle/end truncation patterns and verify correct completeness states and no false FULL declaration.

### S4-50 — Corrupted Formatting Stress
Test broken markdown, nested quotes, code fences, escaped JSON and malformed role labels without granting inferred content authority.

### S4-51 — Duplicate Transcript Bundle Stress
Include the same conversation twice with minor formatting changes and test semantic/source dedupe.

### S4-52 — Secret Scanner Adversarial Stress
Test keys/tokens/password-like values split across lines, code blocks and quoted assistant output; verify safe redaction.

### S4-53 — Access-Loss Recovery State
Test claims whose Drive/GitHub targets are temporarily inaccessible; distinguish ACCESS_UNVERIFIABLE from NOT_FOUND.

### S4-54 — Provider/Market Claim Poisoning Test
Seed confident false render/listener/market claims and verify evidence firewall holds.

### S4-55 — Recovery Crash/Resume Transaction Test
Interrupt after some writes, restart, inspect transaction ledger and ensure no duplicate/half-promoted state.

### S4-56 — Rollback Evidence Preservation
After rollback, preserve audit trail of attempted mutation without leaving the invalid current pointer active.

## BLOCK H — PRUNING / PRODUCTION INTEGRATION / NEXT CYCLE GOVERNANCE

### S4-57 — Recovery Mechanism Inventory Dedupe
Build one map of 18B, SI-0009..0013, PR #77 generic mechanisms and PR #78 overlaps; merge aliases and mark true unique components.

### S4-58 — Dead Candidate Prune Gate
Identify recovery candidates with no unique mechanism, no evidence path or superseded implementation; archive/reject with provenance.

### S4-59 — Prompt Queue Semantic Dedupe
Compare this 64 queue with other live 64-card packs; remove/route duplicates before execution rather than after creating new artifacts.

### S4-60 — WIP Limit for Meta-Integration
Enforce at most one primary recovery integration frontier plus bounded independent tests; blocked real-corpus pilot should not spawn unlimited architecture branches.

### S4-61 — Evidence-Triggered Auto-Routing
When a real transcript appears, route directly to S4-01..08 rather than asking for another research cycle or repeating design prompts.

### S4-62 — Story/Audio Priority Protection Test
Verify recovery/self-improvement work yields to higher P1/P2 production when no system FATAL/MAJOR requires meta intervention, unless Founder explicitly switches focus.

### S4-63 — Marginal Information Gain Audit
Before any future 32→64/64→128 cycle, score new evidence, implementation delta, unresolved gate closure, overlap and integration debt; recommend RUN/HOLD/PRUNE.

### S4-64 — Sprint-4 Decision Gate
Integrate all executed S4 evidence. Promote only mechanisms with matching proof, archive duplicates, update Learning Ledger/registry, and derive further prompts only if a real new frontier justifies them. If decisive dependency remains external, STOP with exact trigger instead of doubling mechanically.
