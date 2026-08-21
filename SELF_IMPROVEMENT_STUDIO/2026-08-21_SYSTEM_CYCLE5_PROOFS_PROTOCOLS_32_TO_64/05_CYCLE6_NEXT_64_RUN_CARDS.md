# CYCLE 6 — NEXT 64 RUN CARDS

**Status:** READY / TARGETED FUTURE BANK / NOT BLINDLY AUTO-AUTHORIZED.  
**Derivation:** four successors for each of the 16 proof/enforcement mechanisms exercised in Cycle 5: real integration, adversarial attack, replication/measurement, promotion/deprecation decision.

## Registry Identity — C6-01…04
**C6-01 — Full-Family ID Allocator Integration.** Read current base + all registry shards, allocate the next proven-unused SI ID, and persist the allocation proof. **Gate:** partial visibility fails closed.

**C6-02 — Registry Split-Brain Attack.** Hide one shard containing a colliding ID and prove allocator refuses to issue an ID when family completeness cannot be established. **Gate:** no silent allocation.

**C6-03 — Historical Collision Replay.** Reproduce SI-0010/SI-0014 collision history in a sandbox and prove current allocator catches it before write. **Gate:** deterministic rejection + provenance.

**C6-04 — Registry Identity Promotion Review.** Decide whether allocator belongs in CURRENT registry transaction tooling or remains candidate. **Gate:** application + regression + readback + rollback.

## Durable Reconciliation — C6-05…08
**C6-05 — SI-0014/SI-0012 Transaction Interface Reconcile.** Merge only non-duplicated durable-write semantics into one candidate interface. **Gate:** no second transaction runtime.

**C6-06 — Partial GitHub/Drive Crash Injection.** Simulate GitHub committed / Drive failed and Drive committed / GitHub failed. **Gate:** both become `REPAIR_REQUIRED`, never PASS.

**C6-07 — Real Multi-Store Write Pilot.** Use one reversible non-canon artifact write across GitHub+Drive with transaction ID and readback. **Gate:** exact before/after evidence.

**C6-08 — Durable Transaction Promotion Review.** Compare recovered failure rate/rework against current behavior. **Gate:** promote only if actual reliability improves without material overhead.

## Checkpoint Lineage — C6-09…12
**C6-09 — Material-Boundary Checkpoint Hook.** Add checkpoints only at stage/result/write boundaries, not every thought/tool call. **Gate:** bounded overhead.

**C6-10 — Tamper/Reorder/Replay Attack.** Reorder checkpoints, alter payload, replay an old head. **Gate:** lineage validation rejects all three.

**C6-11 — Real Abrupt-Session Recovery Pilot.** On the next genuine interrupted work block, measure frontier recovery and duplicate work avoided. **Gate:** incident evidence, not simulation claim.

**C6-12 — Checkpoint Retention Policy.** Determine minimum retained lineage needed for safe recovery without state bloat. **Gate:** recovery remains possible after compaction.

## Interruption Learning — C6-13…16
**C6-13 — Interruption Event Auto-Ingest.** Convert real recovery incidents into typed Learning Ledger observations. **Gate:** raw incident fields preserved.

**C6-14 — False-Success Attack.** Feed an incident with silent state loss or duplicated work and prove learner cannot label it success. **Gate:** defect remains visible.

**C6-15 — Recovery Cost Baseline.** Measure recovery minutes, duplicated steps, manual Founder intervention across multiple incidents. **Gate:** at least two real incidents before trend claim.

**C6-16 — Session Resilience Value Review.** Decide whether checkpoint/reconciler complexity is justified by measured avoided rework. **Gate:** retain, simplify or reject based on evidence.

## Book→SI Bridge — C6-17…20
**C6-17 — MF-C02 Schema Compatibility Pilot.** Map BookObservation→EvidenceClass→EarliestFailure→Candidate into CURRENT SI schema without new authority. **Gate:** no parallel registry model.

**C6-18 — Duplicate Mechanism Attack.** Submit a Book Engine mechanism already covered by current SI kernels. **Gate:** MERGE_WITH_EXISTING, not duplicate engine.

**C6-19 — Second-Book Positive Transfer.** Apply one MF-C03 sensor to a second independent completed book with source hash bound. **Gate:** detection + source provenance.

**C6-20 — Book Bridge Scope Decision.** Choose PROJECT / BOOK_DOMAIN / UNIVERSAL / HOLD for MF-C01/C02/C03 individually. **Gate:** one-book test count cannot decide universal scope.

## Book Sensor Transfer — C6-21…24
**C6-21 — Healthy No-Change Portfolio Control.** Run sensors on a book/section already judged healthy. **Gate:** false-positive rate explicit.

**C6-22 — Causal Delete Audit Attack.** Delete a known causal bridge in a sandbox and prove sensor notices the change. **Gate:** positive sensitivity without blanket flagging.

**C6-23 — Promise Ledger Cross-Book Pilot.** Test promise setup/payoff tracking on two structurally different books. **Gate:** mechanism adapts without copying story-specific facts.

**C6-24 — Sensor Promotion/Prune Review.** Promote only sensors with useful signal; prune noisy diagnostics. **Gate:** healthy-control performance included.

## Frontier Drift — C6-25…28
**C6-25 — Portfolio Frontier Auto-Scanner.** Resolve project frontiers from current project state, main, Drive and working PRs. **Gate:** D01 must resolve to E120/Founder lock, not E95/E112.

**C6-26 — Rapid Drift Race Attack.** Advance a fixture three times during one run and prove stale planned work is cancelled before execution. **Gate:** no stale episode/action write.

**C6-27 — Authority-vs-Frontier Conflict Pilot.** Test newer lower-authority progress against older higher-authority source. **Gate:** compatible extension allowed; contradiction stops.

**C6-28 — Stale Aggregate Deprecation Map.** Identify aggregate workstate lines that are unsafe routing sources and point them to project-specific state. **Gate:** no destructive history rewrite required.

## Human Signal — C6-29…32
**C6-29 — Real D01 or D04 Human Signal Session.** Run one uncoached target-reader/listener test from an already prepared packet; save raw answers first. **Gate:** real participant provenance.

**C6-30 — Coaching/Persona Contamination Attack.** Compare coached, synthetic-persona and raw-human inputs. **Gate:** only raw real-human path can become Human Signal.

**C6-31 — Human Signal Synthesis Compiler.** Convert raw responses into findings while retaining dissent/outliers and original response IDs. **Gate:** synthesis cannot erase contradictory human evidence.

**C6-32 — Human-to-Repair Routing Pilot.** Route one proven human failure to PERFORMANCE / WRITING / ADAPTATION / LOCALIZATION / CONTEXT / NO_DEFECT. **Gate:** text reopens only for proven WRITING defect.

## Evidence Independence — C6-33…36
**C6-33 — Cross-Model Lineage Tagging.** Require every GPT/Claude/Grok report to include root source/evidence lineage. **Gate:** missing lineage lowers independence confidence.

**C6-34 — Duplicate Report Cluster Attack.** Feed paraphrased copies through multiple models. **Gate:** one evidence family, not multiple votes.

**C6-35 — Independent Two-Model Review Trial.** Give two models same source/version independently, then reconcile only after both submit. **Gate:** reports remain model evidence, not Human Signal.

**C6-36 — Evidence Weight Policy Review.** Define when independent evidence families materially change a decision. **Gate:** no prestige/majority shortcut.

## Package Witness — C6-37…40
**C6-37 — vNext Package Candidate Manifest.** Inventory accepted post-v11.2 modules with exact blobs/dependencies/tests. **Gate:** closed dependency set.

**C6-38 — Package/Main Divergence Attack.** Add a main-only feature after package build and prove package report does not claim it. **Gate:** immutable package identity.

**C6-39 — Fresh-Unzip Script Repro Pilot.** Execute package from clean extraction without caller-specific path hacks. **Gate:** cold regression PASS.

**C6-40 — Package Promotion Decision.** Build a new package only if accepted modules are merged/current and regressions pass. **Gate:** old v11.2 never relabeled.

## Promotion Proof — C6-41…44
**C6-41 — Promotion Packet Compiler.** Generate TARGET/REGRESSION/READBACK/ROLLBACK/EVIDENCE-BOUNDARY packet for one candidate. **Gate:** all fields sourced.

**C6-42 — External-Evidence Bypass Attack.** Try to promote human/provider/economics-dependent candidate using tests only. **Gate:** HOLD_EXTERNAL_EVIDENCE.

**C6-43 — Rollback Rehearsal.** Apply and revert one reversible candidate on sandbox/current-compatible surface. **Gate:** rollback restores previous verified state.

**C6-44 — Candidate Lifecycle Audit.** Find candidates stuck in PILOT/READY without a real next gate; disposition HOLD/REJECT/TEST rather than leave zombie state.

## Telemetry Proof — C6-45…48
**C6-45 — Real P1/P2 Event Instrumentation.** Capture routing, repair and evidence events from one book and one audio task. **Gate:** source-linked telemetry rows.

**C6-46 — False-Zero Injection.** Insert unmeasured spend/time/duration as zero and prove validator rejects it. **Gate:** null preserved.

**C6-47 — Telemetry Provenance Join.** Link event -> artifact/source hash -> gate -> result. **Gate:** dashboard numbers trace back to evidence.

**C6-48 — Telemetry Value Audit.** Remove metrics that never change a decision. **Gate:** observability without metric bloat.

## Economics Proof — C6-49…52
**C6-49 — Real Bounded Audio Economics Canary.** Capture provider spend, generated minutes, accepted minutes, human minutes and regeneration waste. **Gate:** measured row only.

**C6-50 — Estimate-vs-Actual Attack.** Feed predicted cost beside actual cost. **Gate:** prediction cannot populate measured fields.

**C6-51 — Cost/Quality Frontier Pilot.** Compare two bounded production modes using same locked source and human quality evidence. **Gate:** cost cannot compensate for failed quality gate.

**C6-52 — Economics Routing Integration.** Let real cost/rework data influence mode selection without overriding story/audio quality authority. **Gate:** optimization remains subordinate to quality gates.

## Second-Project Replication — C6-53…56
**C6-53 — SI-0009 Second Audio Project Replication.** Apply the generic post-render chain to a second locked audio project with unchanged mechanism hash. **Gate:** project-specific cues/timings remain adapters only.

**C6-54 — Mechanism Drift Attack.** Quietly alter the generic mechanism between projects. **Gate:** replication invalidated.

**C6-55 — Failure Replication Study.** If second project fails, localize whether mechanism or project adapter failed. **Gate:** no forced positive result.

**C6-56 — Audio-Domain Promotion Review.** Promote SI-0009-class mechanism only after independent replication and regression. **Gate:** one-project success remains HOLD otherwise.

## Proof Ledger — C6-57…60
**C6-57 — Proof Ledger Live Integration.** Attach evidence class/source ref to one real candidate lifecycle. **Gate:** claim traceable end-to-end.

**C6-58 — Evidence Substitution Attack.** Attempt ENGINEERING_TEST→HUMAN_SIGNAL and DRY_RUN→LIVE_PROVIDER substitutions. **Gate:** both fail closed.

**C6-59 — Proof Freshness Audit.** Mark evidence stale when source/version changes. **Gate:** old proof cannot silently validate new artifact.

**C6-60 — Proof Compaction.** Compact duplicate proofs by root evidence family while preserving provenance. **Gate:** no loss of material dissent/failure evidence.

## Governor v2 — C6-61…64
**C6-61 — Real Portfolio Routing Pilot.** Rank current P0/P1/P2/meta options by authorization + information value + effort. **Gate:** route to highest-value real gate.

**C6-62 — Meta-Starvation Attack.** Flood queue with attractive engine prompts while a decisive D04/D01 human gate is available. **Gate:** product evidence wins when higher value.

**C6-63 — Meta-Neglect Countertest.** Create a true P0 system integrity defect while product work is available. **Gate:** Governor correctly prioritizes integrity repair.

**C6-64 — Autonomous Cycle Gate.** Decide whether another 32/64 meta cycle is justified from new evidence. **Gate:** if no new recurring defect/evidence gap exists, STOP meta-cycle and return to books/audio/human/provider production.

## Execution law
Before any C6 run: `FRESHNESS/REBASE -> AUTHORITY -> SMALLEST DECISIVE TASK -> EXECUTE -> READBACK -> EVIDENCE CLASS -> PERSIST -> RECOMPUTE NEXT`.

The existence of 64 prompts is not authorization to execute all 64.