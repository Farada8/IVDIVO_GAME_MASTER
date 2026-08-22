# CYCLE32D — EXECUTABLE MODULES + ENGINEERING CONTRACTS + PROOFS + PROTOCOLS

Cycle32D implements a bounded subset of Cycle32C M01–M32. It is a local v2 extension pilot, not a new authority.

## Contracts

### SIC32D-C01 CROSS_SURFACE_SI_ID_RESERVATION_READ
Before proposing a global SI ID, read main registry-family and active registry-changing PR/branch reservations. Any collision -> STOP. Merge-time recheck remains required.

### SIC32D-C02 NO_ID_IS_VALID_OUTPUT
A cycle that does not require a new candidate returns `NO_ALLOCATION`; it must not allocate IDs to prove progress.

### SIC32D-C03 AUTHORITY_STACK_FAILS_ON_PEER_CURRENT_CONFLICT
Two controlling CURRENT surfaces with unresolved equal priority -> HOLD.

### SIC32D-C04 FRESHNESS_IS_VECTOR_NOT_SCALAR
Execution/main, project, strategy, registry, Drive, PR/branch and approval-event freshness may differ. Required dimensions are scope-specific.

### SIC32D-C05 STALE_MAIN_INVALIDATES_WRITE_BASE
A previously observed main head cannot authorize a new global write after current main changes.

### SIC32D-C06 META_WIP_LIMIT
Default: <=1 primary meta candidate + <=2 independent pilots. Overflow queues unless system blocker/prerequisite/explicit Founder switch applies.

### SIC32D-C07 FOUNDER_SWITCH_IS_SCOPED
Explicit system-development instruction may temporarily supersede production-return priority, but does not permanently rewrite global priority order.

### SIC32D-C08 PRODUCTION_RETURN_TARGET_REQUIRED
Every meta cycle declares an exact return target or bounded Founder-switch reason.

### SIC32D-C09 PROMPT_FUNCTIONAL_FINGERPRINT
Prompt identity is functional: consumer + evidence class + gate + action semantics + state mutation; title/wording differences do not establish novelty.

### SIC32D-C10 DUPLICATE_PROMPTS_MERGE
Same functional fingerprint -> MERGE/NARROW, not another NEW slot.

### SIC32D-C11 EVIDENCE_YIELD_REQUIRED
Execution must change a decision, add evidence, remove a blocker, or create an explicit evidence-bounded HOLD.

### SIC32D-C12 NO_EFFECT_STEP_REJECT
A step that only increases text/files/prompt count without evidence/decision/blocker delta is rejected as meta-noise.

### SIC32D-C13 VOI_ORDINAL_NOT_FAKE_PRECISION
Route by decision-changing potential and evidence independence against burden/risk. Monetary/time precision is forbidden unless measured.

### SIC32D-C14 RESEARCH_NEEDS_DECISION_CONSUMER
No identified decision consumer -> research/meta step HOLD.

### SIC32D-C15 COST_OF_DELAY_QUALITATIVE_BY_DEFAULT
High/medium/low consequence bands are allowed without fabricated euro/hour estimates.

### SIC32D-C16 PROOF_CLASS_CEILING
Evidence below the required class cannot support the claim, regardless of test count or document volume.

### SIC32D-C17 EXTERNAL_EVIDENCE_NON_SUBSTITUTION
Model review, automated tests, source inspection and self-produced artifacts cannot satisfy Human Signal/provider live/payment/market behavior claims.

### SIC32D-C18 FAIL_CLOSED_LOCALITY
Stop or hold only the affected action where possible; do not freeze unrelated production by default.

### SIC32D-C19 OBSERVABILITY_NO_VANITY_SCORE
Track decisions changed, gaps closed, duplicates avoided, stale surfaces, blockers, write/readback, rollback, production return and no-effect separately.

### SIC32D-C20 SELECTIVE_ROLLBACK_ONLY
Revalidate true descendants of a changed contract; locked/unrelated surfaces remain protected.

### SIC32D-C21 UPLOAD_PROVENANCE_NOT_AUTHORITY
Conversation upload -> hash/classify/pointer. It does not automatically become canon, CURRENT, market evidence or knowledge authority.

### SIC32D-C22 RAW_BINARY_DEDUPE
When a canonical Drive source is already known, GitHub stores metadata/hash/pointer rather than duplicating production binaries.

### SIC32D-C23 PROMOTION_REQUIRES_NORMAL_V2_LIFECYCLE
Executable tests can move a local pilot forward but cannot self-promote v3/CURRENT or assign scope beyond evidence.

### SIC32D-C24 NEXT64_IS_DEPENDENCY_QUEUE
64 follow-up cards may be designed because Founder requested doubling; design does not activate them as WIP. Every card has a dependency and stopping rule.

## Proof protocol
`FRESH AUTHORITY -> PARALLEL SURFACES -> DECISION -> EXISTING OWNER -> SMALLEST TEST -> FAIL-CLOSED GATE -> YIELD RECORD -> SELECTIVE WRITE -> READBACK -> PROMOTION/HOLD -> RETURN`.

## Deterministic proof
32 unit tests exercise collision/no-allocation, authority conflict, freshness, WIP, return target, prompt dedupe, evidence yield/no-effect, VOI, Cost-of-Delay, evidence ceilings, external evidence firewall, fail-closed routing, observability, rollback, promotion HOLD and asset-registry validation.

## Evidence ceiling
This proves implemented mechanical behavior only. It does not prove literary improvement, time/cost reduction, Human Signal, provider reliability, market behavior or universal superiority.
