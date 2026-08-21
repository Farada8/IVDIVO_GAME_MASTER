# IVDIVO — TRANSCRIPT RECOVERY — NEXT 64 PROMPTS v2

**Derived from:** Sprint 2 N01–N32 executed results.  
**Status:** WORKING ROUTED DEVELOPMENT BANK — do not run mechanically.  
**Primary rule:** the first real large pasted-corpus pilot outranks further prompt inflation.

**Return contract for every prompt:** evidence used; decision/status; artifacts changed; blockers; exact next gate; reusable learning. Never simulate Founder/provider/Human/market evidence.

# A — REAL CORPUS / PARSER FIDELITY

## R2-01 — First Real Large Corpus Pilot
Run the verified v1 extractor on the first genuinely copied/exported long prior conversation. Persist source hash, completeness basis, extracted ledger and false-positive/false-negative observations.

## R2-02 — Structured Export vs Plain Paste Comparator
Compare role/turn reconstruction on structured export and plain copied text of the same conversation; quantify ambiguous-role differences without treating accuracy as authority.

## R2-03 — JSON/YAML/Escaped Role Fuzz
Generate adversarial `User:`/`Assistant:` strings inside JSON, YAML, escaped strings, HTML, Markdown tables and code; test outer-turn isolation.

## R2-04 — Truncated Tail Detector
Develop conservative indicators for supplied-transcript truncation and prove they only downgrade completeness; they may never assert original-chat completeness.

## R2-05 — Role-Confidence Quarantine
Add extraction-confidence and embedded-source metadata so ambiguous segments enter quarantine instead of inheriting outer authority.

## R2-06 — Artifact Reference Precision/Recall Canary
Build fixture corpus of true/false filenames, Drive IDs, GitHub paths and URLs; measure lookup noise vs missed references and tune only when misses are material.

## R2-07 — Secret Redaction Adversarial Suite
Stress secret firewall with credentials/tokens in prose, code, quoted logs and URLs; prove persisted excerpts cannot leak raw secrets.

## R2-08 — Large-Corpus Chunk Boundary Stress
Force directives/artifact claims to straddle chunk boundaries; validate overlap/finding hashes and no duplicate/lost material findings.

# B — SEMANTIC RECONCILIATION / AUTHORITY

## R2-09 — v1 Ledger→v2 State Compiler Spec
Define deterministic copied fields vs semantic fields; compiler may copy source identity but cannot assign canon/current status without reconciliation evidence.

## R2-10 — Direct Founder vs Paraphrase Disambiguator
Build fixtures where assistant paraphrases Founder decisions; require original direct statement or classify paraphrase as lower-authority claim.

## R2-11 — Chronology Resolution Engine
Resolve same-authority directives using trustworthy timestamps/turn order only; quarantine ambiguous chronology that changes branch/lock.

## R2-12 — Multi-Project Partition Pilot
Use a real mixed-project transcript to test project-key assignment, quarantine and zero cross-project write-through.

## R2-13 — Supersession Graph Builder
Construct supersedes/duplicates/extends/conflicts graph from transcript claims plus persisted artifacts and derive one current path without deleting audit history.

## R2-14 — Frontier Reconstruction Pilot
On a known project reconstruct last verified completed artifact, passed gates, blockers, do-not-repeat and next legal action; compare to current authority.

## R2-15 — Materiality Classifier
Define when unknown/conflict is material enough to block recovery versus safe to retain; test canon, filenames, prose polish and provider metadata.

## R2-16 — Founder Question Minimizer
Generate a Founder decision packet only for irreducible choices; prove recoverable file/state questions were resolved through tools first.

# C — CLAIM / EVIDENCE / PROOF ADAPTERS

## R2-17 — GitHub Artifact Verification Adapter
Implement/specify path/branch/SHA/currentness verification with explicit MISSING/SUPERSEDED outcomes.

## R2-18 — Drive Artifact Verification Adapter
Implement/specify file ID/title/revision/parent/currentness readback with revision evidence and conflict-safe semantics.

## R2-19 — Founder Lock Proof Fixtures
Create positive/negative fixtures for direct lock, recommendation, model claim, filename FINAL and stale lock superseded by later Founder instruction.

## R2-20 — Test PASS Proof Fixtures
Create exact-source positives and prose-claim negatives; test log/count/exit/evidence requirements.

## R2-21 — Provider Execution Proof Fixtures
Separate compiled request, dry manifest, submitted job, returned asset and accepted asset; only real output may satisfy provider-executed claim.

## R2-22 — Human Signal Import Schema
Define participant/stimulus/build/question/response/blinding fields; prohibit model-generated pseudo-participants.

## R2-23 — Market Signal Import Schema
Define platform/source/date/cohort/denominator/metric/variant fields and strict hypothesis-vs-observation separation.

## R2-24 — Cross-Evidence Contradiction Router
Handle machine PASS + human FAIL or provider output contradicting dry assumptions; route to earliest responsible layer instead of majority vote.

# D — TRANSACTIONAL PERSISTENCE / CONCURRENCY

## R2-25 — Recovery Write Journal Implementation
Implement machine journal for planned/written/failed/repaired/rolled-back/skipped-duplicate writes with preconditions and readback.

## R2-26 — GitHub Stale-SHA Automated Fixture
Simulate stale SHA after sibling update; require abort→fresh read→rebase or branch+PR with no force overwrite.

## R2-27 — Drive Revision-Conflict Fixture
Simulate revision change between read/write; require failed precondition→re-read→semantic merge/no-op.

## R2-28 — Cross-Store Partial-Write Chaos Test
Make GitHub succeed while Drive fails and vice versa; prove `PARTIAL_WRITE_REPAIR_REQUIRED` and no false completion.

## R2-29 — Idempotent Repaste Test
Process identical transcript twice; second run must produce no duplicate candidate or duplicate mutation.

## R2-30 — Changed-Authority Repaste Test
Reprocess same transcript after authority advances; old extraction stays valid evidence but frontier/currentness must rebase.

## R2-31 — Write Rollback Boundary
Define what can safely roll back and what must repair forward because concurrent sibling changes have landed.

## R2-32 — Transaction Evidence Packet
Standardize precondition, mutation, result, readback, regression and rollback evidence into one portable packet.

# E — REGISTRY / LEARNING / COMPACTION

## R2-33 — Registry Shard Write API
Create candidate write path that adds one validated shard plus index/family update without rewriting the monolith.

## R2-34 — Registry Unique-ID Concurrency Test
Have two branches attempt same/new candidate IDs; duplicate ID fails closed while distinct IDs can merge.

## R2-35 — Registry Compaction Build
Compile base+extensions to deterministic pretty canonical registry; persist manifest with input SHAs and output SHA.

## R2-36 — Registry Compaction Roundtrip
Prove compacted registry semantically equals family view and loses no candidate/evidence/next gate.

## R2-37 — Learning-Ledger Recovery Return
Store actual recovery defects/successes separately from candidate proposals; prevent project-plot leakage into universal learning.

## R2-38 — Recovered-Mechanism Universalization Gate
Test a recovered process improvement in a second materially different domain before universal promotion.

## R2-39 — Stale Rule / Duplicate Router Sweep
Find recovery rules duplicated across 13/16/18B/Self-Improvement; MERGE/NARROW/SUPERSEDE rather than add layers.

## R2-40 — Recovery Context Compactor
Build minimal recovery boot pack from current pointers, 18B law, schemas and active project state; avoid copying giant historical chats into every run.

# F — MULTI-AI / INDEPENDENCE / HANDOFF

## R2-41 — Source-Parity Recovery Review Pack
Give GPT/Claude/Grok same transcript hash, current authority and bounded question; mark NON_PARITY when inputs differ.

## R2-42 — Blinded Authority Red Team
Ask independent model to find false promotions/conflicts without prior verdict, then reconcile its evidence.

## R2-43 — Diagnosis vs Fix Split
Run one pass for recovery-defect diagnosis and a separate pass for repair proposals; diagnosis acceptance does not auto-accept fix.

## R2-44 — Model-Echo Dedupe
Cluster findings derived from same source/assumption so multiple models do not become fake independent evidence.

## R2-45 — Cross-Model Chat-Only Recovery
Recover external-AI transcript containing unsaved work; preserve source/model provenance and candidate status.

## R2-46 — Handoff Packet Minimality Test
Compare full archive dump vs bounded recovery packet; measure missed material facts and context load before changing default.

## R2-47 — Model Backend Recovery Audition
Test candidate models on same mixed transcript for partition, verification planning and unknown preservation using one fixed rubric.

## R2-48 — Reconciler Role Contract
Define one integrator owning final dispositions/state mutations; specialists remain evidence producers, not parallel authorities.

# G — INTEGRATION / PACKAGE / NEXT-ACTION

## R2-49 — Recovery→Next-Action Resolver Integration
Connect v2 completion output to normal action resolver; prove RECOVERY_COMPLETE can still STOP on Founder/human/provider/tool gates.

## R2-50 — NO-OP Continuation Regression
If recovered work is already current and no new delta exists, route directly to real next obligation without rewriting artifacts.

## R2-51 — Do-Not-Repeat Propagation
Carry recovered do-not-repeat gates into normal production state and test that completed work is not selected again.

## R2-52 — Package vs Main Manifest
Track recovery extensions verified on main but absent from last engine ZIP; prohibit retroactive package claims.

## R2-53 — Next Engine ZIP Candidate Plan
Define exact files/tests/regressions needed to package transcript recovery v1 plus accepted v2 extensions in next release.

## R2-54 — Cold-Unpack Recovery Regression
From clean package run extraction→reconciliation fixtures→completion gate without hidden local state.

## R2-55 — Migration/Rollback Documentation
Document upgrade/downgrade if v2 proves worse on real corpora; preserve v1 first-pass compatibility.

## R2-56 — Current Pointer Promotion Packet
Prepare promotion packet only after gates pass: evidence, application targets, previous current, readback, rollback and unresolved external gates.

# H — REAL PILOT / CHAOS / PRODUCTIVITY

## R2-57 — First Large Corpus End-to-End
Execute complete recovery on first real long copied chat and compare recovered frontier against independently verified project state.

## R2-58 — False-Promotion Audit on Real Corpus
Enumerate every saved/PASS/LOCK/render/human/market statement and prove none advanced without matching evidence.

## R2-59 — Chat-Only Artifact Recovery Pilot
Recover one substantial unsaved artifact from real transcript, persist as candidate, run appropriate QA and read back.

## R2-60 — Recovery Time/Tool-Call Baseline
Measure manual recovery vs routed protocol effort; do not claim productivity gain without baseline.

## R2-61 — Recovery Failure Injection
Inject missing Drive access, stale GitHub state, partial corpus and conflicting Founder directives in bounded fixtures; verify correct stop/repair states.

## R2-62 — Second Material Domain Pilot
Repeat on a materially different project type (e.g. audio vs book/system) to test generality and project-partition firewall.

## R2-63 — Recovery Red Team + Rule Value Audit
After two real pilots identify controls that never change decisions and remove/narrow ritual complexity; preserve controls that prevented actual defects.

## R2-64 — Promotion or Hold Decision
Using only real pilot/regression evidence decide KEEP v1 ONLY / PROMOTE SELECTED v2 / HOLD / ROLLBACK; generate any later cycle from unresolved evidence gaps, not prompt-count habit.
