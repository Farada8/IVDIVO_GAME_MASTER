# CYCLE32C — 32 MODULES / CONTRACTS / PROOFS / PROTOCOLS

Local namespace avoids collisions with existing global SI/C/B identifiers.

|Module|Contract|Proof|Protocol|Invariant|
|---|---|---|---|---|
|M01 `AuthoritySnapshotGuard`|`C32C-01`|`PB32C-01`|`PT32C-01`|Freeze current authoritative surfaces before routing; stale snapshots cannot mutate state.|
|M02 `EmbeddedProjectSliceFreshness`|`C32C-02`|`PB32C-02`|`PT32C-02`|Compare embedded project slices with controlling project-specific state and mark stale slices superseded.|
|M03 `EmptyScaffoldProgressGuard`|`C32C-03`|`PB32C-03`|`PT32C-03`|Folder/file existence without substantive content cannot count as progress.|
|M04 `FileLibraryTransferBoundary`|`C32C-04`|`PB32C-04`|`PT32C-04`|Separate searchable File Library references from physically transferable bytes.|
|M05 `ParallelLaneDeduper`|`C32C-05`|`PB32C-05`|`PT32C-05`|Classify parallel work KEEP/MERGE/SALVAGE/STALE/REJECT before new implementation.|
|M06 `V3PromotionGuard`|`C32C-06`|`PB32C-06`|`PT32C-06`|Keep v2 current; v3 cannot promote without independent lifecycle evidence.|
|M07 `CandidateIDReservationGuard`|`C32C-07`|`PB32C-07`|`PT32C-07`|No new SI ID without fresh registry + open-reservation read immediately before allocation.|
|M08 `StalePointerRepairPlanner`|`C32C-08`|`PB32C-08`|`PT32C-08`|Repair stale pointers at the smallest controlling surface without rewriting valid history.|
|M09 `EffectLedgerEntryCompiler`|`C32C-09`|`PB32C-09`|`PT32C-09`|Record claimed improvement, downstream decision changed, evidence, counterfactual and uncertainty.|
|M10 `NoOpSuccessClassifier`|`C32C-10`|`PB32C-10`|`PT32C-10`|REUSE_CURRENT/NO_OP/PROTECT_NO_CHANGE/HOLD_REAL_EVIDENCE are valid successful dispositions.|
|M11 `MetaStarvationGuard`|`C32C-11`|`PB32C-11`|`PT32C-11`|Meta-work may continue only when Founder switched focus, P0 blocker exists, or it directly unblocks production.|
|M12 `ProductionEffectTrace`|`C32C-12`|`PB32C-12`|`PT32C-12`|Trace a mechanism to an actual production decision; document count is not effect.|
|M13 `CrossStoreWritePlan`|`C32C-13`|`PB32C-13`|`PT32C-13`|Declare GitHub/Drive writes, order, readbacks and rollback before mutation.|
|M14 `StaleBranchSalvagePlanner`|`C32C-14`|`PB32C-14`|`PT32C-14`|When branch is stale, salvage only unique semantic delta onto fresh main; never force overwrite.|
|M15 `BranchFreshnessClassifier`|`C32C-15`|`PB32C-15`|`PT32C-15`|Classify AHEAD/CLEAN/BEHIND/DIVERGED and block merge on stale evidence.|
|M16 `TransactionBundleState`|`C32C-16`|`PB32C-16`|`PT32C-16`|Represent multi-surface mutation as PLANNED/PARTIAL/COMMITTED/RECOVERY_REQUIRED/CLOSED.|
|M17 `PartialWriteRecoveryPlanner`|`C32C-17`|`PB32C-17`|`PT32C-17`|Recover from one-store success / one-store failure using fresh read and idempotent missing actions.|
|M18 `EvidenceClassFirewall`|`C32C-18`|`PB32C-18`|`PT32C-18`|Engineering/source/model evidence cannot silently become human/provider/market/canon evidence.|
|M19 `HumanProviderMarketFirewall`|`C32C-19`|`PB32C-19`|`PT32C-19`|External evidence remains HOLD until real interaction/artifact is observed.|
|M20 `ExperimentBudgetGuard`|`C32C-20`|`PB32C-20`|`PT32C-20`|Choose smallest reversible high-VOI experiment; backlog size never authorizes execution.|
|M21 `DoubleLoopTrigger`|`C32C-21`|`PB32C-21`|`PT32C-21`|Escalate from local fix to governing-model review only on recurrence/contradiction/guardrail failure.|
|M22 `SLOErrorBudgetGuard`|`C32C-22`|`PB32C-22`|`PT32C-22`|Track allowed reliability debt; stop feature accumulation when integrity error budget is exhausted.|
|M23 `DeprecationDecision`|`C32C-23`|`PB32C-23`|`PT32C-23`|Archive/supersede dead or duplicate mechanisms while preserving audit provenance.|
|M24 `BacklogGovernor`|`C32C-24`|`PB32C-24`|`PT32C-24`|Select highest-information admissible next work; 64 prompts are a backlog, not an order.|
|M25 `DecisionLatencyMetric`|`C32C-25`|`PB32C-25`|`PT32C-25`|Measure elapsed time to a justified decision only when timestamps are actually observed.|
|M26 `OperatorBurdenMetric`|`C32C-26`|`PB32C-26`|`PT32C-26`|Measure human actions/time/rework with null-safe fields; model speed is not human burden proof.|
|M27 `CausalAttributionGate`|`C32C-27`|`PB32C-27`|`PT32C-27`|Do not attribute improvement to a mechanism unless treatment, baseline and alternative causes are bounded.|
|M28 `TransferReplicationGate`|`C32C-28`|`PB32C-28`|`PT32C-28`|Cross-domain promotion requires repeated effect under same generic contract plus domain adapters.|
|M29 `FalsePositiveNoChangeGuard`|`C32C-29`|`PB32C-29`|`PT32C-29`|Every repair sensor needs protected healthy/no-change controls and false-positive tracking.|
|M30 `PromotionPacketState`|`C32C-30`|`PB32C-30`|`PT32C-30`|Separate EVIDENCE_PASS, READY_FOR_APPROVAL, APPROVED, APPLIED and VERIFIED_CURRENT.|
|M31 `SelfApplicationGate`|`C32C-31`|`PB32C-31`|`PT32C-31`|Self-improvement changes must pass the same authority, canary, regression, readback and rollback lifecycle.|
|M32 `NextCycleRouter`|`C32C-32`|`PB32C-32`|`PT32C-32`|Route to next real bottleneck and explicitly refuse automatic 64→128 if real evidence dominates.|

## Shared contract law
- Preconditions: fresh authority snapshot, explicit scope, provenance, protected authorities and evidence classes.
- Outputs: typed disposition + reasons + evidence class + next gate + rollback/readback requirements.
- Fail closed on authority conflict, missing provenance, stale branch, partial cross-store write, evidence substitution or unknown external evidence.
- Non-guarantees: engineering PASS never guarantees story quality, Human Signal, provider quality, legality, market demand or profitability.

## Shared proof law
Each proof obligation needs at least one negative/HOLD fixture. A passing unit test proves only implemented deterministic behavior. Real effect claims additionally require downstream decision evidence and, where relevant, real human/provider/market observations.

## Shared protocol
`FRESH READ -> DEDUPE -> DECLARE CONTRACT -> EXECUTE/NO_OP/HOLD -> NEGATIVE CONTROL -> READBACK -> EFFECT LEDGER -> DISPOSITION -> NEXT GATE`.
