# IVDIVO BUSINESS ENGINE v1 — CROSS-DOMAIN INTEGRATION REBASE

**Status:** CANDIDATE / FRESH-MAIN REBASE / NO_OUTREACH / €0 NEW FOUNDER CASH / PUBLIC PROOF CEILING E2+  
**Base main:** `416bf029e0b842b697a3eeeb107faae40e9a12cf`  
**Purpose:** integrate already-merged Business Engineering OS verticals into one dependency-aware business runtime without duplicating their domain engines.

## Existing authority reused
Current `main` already contains Library78, live signals, 32 OpportunityObjects, procurement/capital routing, public-signal runtime, WIP/VOI, CREATE/BROKER/ACQUIRE, proof ceilings and Self-Improvement bridges. This package adds only missing cross-domain orchestration/invalidation/lock/dependency mechanisms.

## Engine spine
`LIBRARY/AUTHORITY -> SIGNAL -> BUYER/WORKLOAD -> OPPORTUNITY -> FATAL ASSUMPTION -> EXPERIMENT -> OFFER -> CONTRACT/PAYMENT -> DELIVERY -> OBSERVED ECONOMICS -> CAPITAL/FINANCE -> SCALE -> LEARNING`

## New integration modules BI145–BI160
- **BI145 SharedInfrastructurePassport** — binds reused engine capability to immutable version/hash/size/Drive ID and forbidden semantics.
- **BI146 BusinessDependencyGraph** — typed edges among signals, opportunities, experiments, offers, contracts, deliveries, economics, finance and scale artifacts.
- **BI147 SelectiveInvalidationEngine** — changed nodes dirty only dependent descendants; unrelated artifacts remain valid.
- **BI148 LockedDependencyBlocker** — locked descendant becomes `BLOCKED_LOCKED`, never silently rewritten.
- **BI149 FounderBusinessLockGuard** — Founder-approved offer/contract/strategy accepts evidence updates but rejects silent semantic mutation.
- **BI150 BusinessProofTransitionGuard** — K/S/public work cannot auto-promote E3/E4; only real buyer/payment events can.
- **BI151 BusinessTransitionCompleteness** — detects impossible lifecycle holes after a missing stage.
- **BI152 ObservedEconomicsGate** — price/cost/time/contribution are null until observed; no invented point estimates.
- **BI153 FinanceAfterProofGate** — debt/grant/invoice-finance/investor assessment cannot substitute for E4 demand/payment proof.
- **BI154 DecisionLineageGraph** — evidence -> interpretation -> competing hypothesis -> decision -> expected/actual consequence.
- **BI155 MechanismDispositionGovernor** — `REUSE_CURRENT | MERGE_DELTA | NO_OP | KEEP_NEW_BOUNDED`.
- **BI156 BoundedSelfImprovementPromotion** — observed defect + regression + provenance + readback required; otherwise HOLD/PROTECT_NO_CHANGE.
- **BI157 BusinessProfileComposer** — attaches bounded domain constraints without spawning another top-level OS.
- **BI158 CrossStoreIdentityBinder** — Drive raw dependency and GitHub manifest identity via SHA/size/ID lineage.
- **BI159 DecisionDeltaTelemetry** — progress metric is decision/evidence delta, not prompt count.
- **BI160 IntegrationReleaseGate** — fresh-main + CI + Drive readback + no authority collision before integration closure.

## Engineering contracts C153–C184
- **C153 REUSE_BEFORE_NEW_ENGINE** — merged capability is reused unless a tested semantic gap exists.
- **C154 DOMAIN_ADAPTER_NEQ_TOP_LEVEL_OS** — creative/public-art/hospitality/construction/compliance remain profiles/adapters.
- **C155 DEPENDENCY_EDGE_TYPED** — every dependency edge has explicit semantic type.
- **C156 SELECTIVE_INVALIDATION_ONLY** — change cannot dirty unrelated artifacts.
- **C157 LOCKED_DESCENDANT_NEVER_AUTO_REWRITE** — lock yields block/escalation, not silent rewrite.
- **C158 FOUNDER_LOCK_OUTRANKS_MODEL_RECOMMENDATION** — model/score/research cannot overwrite Founder lock.
- **C159 EVIDENCE_ONLY_UPDATE_ALLOWED_ON_LOCK** — factual evidence may append without mutating locked decision semantics.
- **C160 K_SE_NEQ_E** — knowledge/signal/engineering proof planes cannot substitute for market proof.
- **C161 PUBLIC_WORK_MAX_E2_PLUS** — public/no-outreach work is capped E2+.
- **C162 E3_REQUIRES_REAL_BUYER_EVENT** — model simulation/public source is insufficient.
- **C163 E4_REQUIRES_REAL_PAYMENT_EVENT** — payment/PO/deposit/commission evidence is external and verifiable.
- **C164 UNKNOWN_ECONOMICS_NULL** — missing price/time/cost/conversion/margin remains null.
- **C165 OBSERVED_ECONOMICS_TRACEABLE** — measured economics bind source/event/time.
- **C166 FINANCE_AFTER_PROOF** — financing is an accelerator, never proof substitute.
- **C167 GRANT_AWARD_NEQ_ELIGIBILITY** — eligibility/programme presence cannot become awarded capital.
- **C168 BUSINESS_LIFECYCLE_NO_HOLES** — downstream artifacts cannot pretend missing upstream authority exists.
- **C169 DECISION_LINEAGE_REQUIRED** — material decisions bind evidence and competing hypothesis.
- **C170 ACTUAL_CONSEQUENCE_WRITEBACK** — later outcomes close the prediction loop.
- **C171 MECHANISM_SEMANTIC_DEDUPE** — semantic identity outranks local numbering/naming.
- **C172 NO_OP_IS_VALID_PROGRESS** — protecting a correct current mechanism is a valid result.
- **C173 PROMPT_COUNT_NEQ_PROGRESS** — prompts are work units, not evidence.
- **C174 DECISION_DELTA_REQUIRED** — research with no changed decision/evidence state is non-progress.
- **C175 SHARED_DEPENDENCY_IMMUTABLE_IDENTITY** — dependency version/hash/size/Drive ID are bound.
- **C176 SHARED_DEPENDENCY_CAPABILITY_ALLOWLIST** — reuse only explicitly approved domain-neutral capabilities.
- **C177 FORBIDDEN_SEMANTICS_NOT_IMPORTED** — Book Engine story semantics cannot leak into Business Engine decisions.
- **C178 RAW_COPYRIGHTED_LIBRARY_DRIVE_ONLY** — raw business-book binaries remain private Drive.
- **C179 GITHUB_STORES_DERIVED_LIBRARY_STATE** — catalog/passports/hashes/mechanisms/tests/provenance only.
- **C180 CONCURRENCY_STALE_WRITER_FAIL_CLOSED** — stale path collision triggers read/rebase, never force overwrite.
- **C181 FRESH_MAIN_BEFORE_PR** — diverged branch cannot be integration authority.
- **C182 DRIVE_READBACK_BEFORE_CLOSURE** — upload alone is not persistence proof.
- **C183 CI_LATEST_HEAD_BEFORE_CLOSURE** — prior local PASS cannot substitute for current-head CI.
- **C184 SELF_IMPROVEMENT_BOUNDED** — local mechanism evidence cannot auto-promote universal SI authority.

## Proof obligations P153–P184
P153 duplicated capability returns `REUSE_CURRENT`; P154 profiles compose without new OS; P155 invalid edge type fails; P156 one changed signal dirties only descendants; P157 locked descendant is blocked; P158 Founder-lock mutation fails; P159 evidence-only lock update passes; P160 K/S cannot promote E; P161 public E7 request caps E2+; P162 buyer event yields E3; P163 payment event yields E4; P164 incomplete economics serializes null; P165 observed contribution computed from measured fields; P166 pre-E4 finance HOLD; P167 grant presence cannot become award; P168 lifecycle hole detected; P169 lineage without evidence fails; P170 actual consequence field retained; P171 semantic duplicate routes reuse/merge; P172 no-defect SI returns PROTECT_NO_CHANGE; P173 prompt count does not alter proof state; P174 zero decision delta returns NO_OP; P175 invalid dependency SHA/passport fails; P176 dependency capability allowlist required; P177 forbidden semantic import documented; P178 raw binary path absent from public Git; P179 derived dependency manifest present; P180 concurrent same-path create collision is read/rebase event; P181 branch created from current main; P182 Drive artifact readback required; P183 current-head workflow required; P184 SI promotion requires regression+provenance+readback.

## Protocols
- **P-BIZ-I01 Fresh Authority/Rebase:** main + Drive + parallel branches -> semantic dedupe -> one writer path.
- **P-BIZ-I02 Shared Dependency:** local/upload -> SHA/size -> Drive immutable copy -> GitHub passport -> capability allowlist.
- **P-BIZ-I03 Dependency/Invalidation:** changed field -> node -> typed descendants -> lock check -> minimal dirty set -> validator/rebuild.
- **P-BIZ-I04 Founder Lock:** lock read -> mutation classify -> evidence-only append OR BLOCK/Founder decision.
- **P-BIZ-I05 Proof Transition:** K/S/E source -> requested promotion -> external event check -> cap/pass/fail.
- **P-BIZ-I06 Economics/Finance:** observed delivery -> actual economics -> E4/E5 -> financing assessment -> scale only after proof.
- **P-BIZ-I07 Decision Learning:** evidence -> decision -> prediction -> actual consequence -> calibration -> bounded SI candidate.
- **P-BIZ-I08 Closure:** regression -> fresh main -> semantic diff -> PR CI -> Drive write/readback -> closure state.

## Evidence boundary
This package proves engineering behavior only. It does not prove willingness-to-pay, profitability, funding approval, legal compliance, insurance acceptability, customer demand, or scaled business viability.
