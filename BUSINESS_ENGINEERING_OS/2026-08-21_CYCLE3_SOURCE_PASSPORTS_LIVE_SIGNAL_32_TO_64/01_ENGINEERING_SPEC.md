# LIBRARY AUTHORITY + DELTA — CYCLE 3

## Authority policy
The 69 raw source files remain in private Google Drive folder `1X6mo94Qo103HheyDry4P3dcQkv5qZg6N`.
GitHub stores only derived metadata, canonical aliases, source passports, mechanisms, tests and provenance pointers. Raw copyrighted book binaries are not duplicated into the public repository.

## Reconciled Cycle2 inventory
- raw Drive files: 69
- chat uploads represented in Cycle2: 64
- Drive-only delta: 5
- chat-valid files: 59
- chat-broken placeholders: 5
- unique valid chat byte hashes: 50
- exact duplicate groups: 8
- canonical unique works: unresolved/null until edition/translation/format reconciliation completes

## Cycle3 canonicalization law
`physical_file_id -> byte_hash -> edition_alias -> canonical_work_id -> source_passport_id -> mechanism_claims[]`.
Exact byte duplicates get one evidence weight. Distinct format/edition/translation files may point to the same canonical work but retain separate physical-source provenance.

## High-priority works for Cycle3
1. The New Business Road Test — John Mullins
2. Testing Business Ideas — David J. Bland / Alexander Osterwalder
3. The Lean Startup — Eric Ries
4. Getting to Plan B — John Mullins / Randy Komisar
5. Seeing What's Next — Clayton Christensen / Scott Anthony / Erik Roth
6. Value Proposition Design — Osterwalder et al.
7. The Invincible Company — Strategyzer
8. The Mom Test — Rob Fitzpatrick
9. The Right It — Alberto Savoia
10. Competing Against Luck — Christensen et al.
11. Buy Then Build — Walker Deibel
12. HBR Guide to Buying a Small Business — Ruback / Yudkoff
13. Financial Intelligence — Berman / Knight
14. finance/valuation corpus
15. Theory of Constraints / The Goal / Goldratt corpus
16. Thinking in Systems — Donella Meadows
17. 7 Powers — Hamilton Helmer
18. Disciplined Entrepreneurship — Bill Aulet
19. Lead and Disrupt — O'Reilly / Tushman
20. Self-Improvement Wave2 references — candidate only where applicable.

A failed download/HTML placeholder/short invalid PDF is `QUARANTINED` and carries `evidence_weight=0` until replaced.

# PRIORITY SOURCE PASSPORTS v3

## SP-01 — The New Business Road Test
Jurisdiction: opportunity assessment before major resource commitment. Mechanisms: Seven Domains; target-segment benefit gate; market/industry split; sustainable advantage; mission/risk fit; execution-on-CSFs; connectedness; fatal-flaw search. Application: early opportunity kill/reshape before build. Conflict routing with Lean/TBI: fatal-flaw desk checks first, then cheapest decisive test. Proof ceiling: K4 when cross-mapped; does not prove current demand.

## SP-02 — Testing Business Ideas
Jurisdiction: experiment design/evidence strength. Mechanisms: assumption mapping; Test Card/Learning Card; cheap/fast early tests; multiple experiments for stronger evidence; strongest evidence within constraints; desirability/feasibility/viability. Application: ExperimentStrengthRouter and PublicEvidenceExperimentCatalog.

## SP-03 — The Lean Startup
Jurisdiction: innovation under extreme uncertainty. Mechanisms: validated learning; Build-Measure-Learn; innovation accounting; MVP as hypothesis test; pivot/persevere; small batches; value vs waste. Conflict: field testing does not cancel pre-test fatal-flaw analysis when cost/risk is high.

## SP-04 — Getting to Plan B
Jurisdiction: business-model discovery and cash timing. Mechanisms: analogs/antilogs; leaps of faith; dashboards; revenue/gross-margin/operating/working-capital/investment model coupling. Critical law: favorable accounting profit cannot compensate for an unfinanceable cash gap.

## SP-05 — Seeing What's Next
Jurisdiction: theory-based industry-change signals. Mechanisms: nonconsumption; overshot/undershot; motivation/ability; asymmetric motivation/skills; nonmarket levers; competitive battle analysis. Freshness rule: theory can classify a fresh signal; the book cannot establish that a 2026 signal exists.

## SP-06 — Value Proposition Design / Strategyzer corpus
Jurisdiction: customer jobs/pains/gains and value mapping. Mechanisms: Customer Profile; jobs, pains, gains; products/services; pain relievers; gain creators; fit. Application: BuyerWorkloadObject and problem/value hypothesis decomposition.

## SP-07 — The Invincible Company
Jurisdiction: explore/exploit portfolio, testing/de-risking and model patterns. Mechanisms: discovery/validation/acceleration/execution; innovation metrics; recurring value; portfolio actions.

## SP-08 — The Mom Test
Jurisdiction: human evidence hygiene. Compliments/fluff/hypotheticals weak; concrete past behavior, constraints and commitments stronger. Protocol compiled but not executed under NO_OUTREACH.

## SP-09 — Buy Then Build / HBR Small Business Acquisition
Jurisdiction: acquisition search/screening. Mechanisms: growth wedge; SDE/adjusted EBITDA; cash-flow-centered target; acquisition as platform for innovation.

## SP-10 — Finance/valuation corpus
Jurisdiction: capital budgeting and financial reality checks. Positive-NPV narratives require an identifiable competitive/economic-rent source; unknown financial inputs stay null.

## SP-11 — TOC / Goldratt corpus
Jurisdiction: system constraint and throughput. Identify constraint -> exploit -> subordinate -> elevate -> repeat; local efficiency can harm system throughput.

## SP-12 — Thinking in Systems / Sterman candidate crosswalk
Jurisdiction: feedback, stocks/flows, delays, policy resistance. Sterman Wave2 integration remains candidate where it changes authority.

## SP-13 — 7 Powers
Jurisdiction: durable strategic power. Benefit + Barrier gate retained; full power-type fixture extraction remains a future dependency.

## SP-14 — Disciplined Entrepreneurship
Drive-only source exists; full K3/K4 extraction remains a Cycle4 dependency. No invented detailed claims in Cycle3.

A passport is a typed provenance wrapper. Mechanism claims without source support stay `INFERENCE_CANDIDATE`; current market facts require fresh external evidence.

# MECHANISM COVERAGE + CONFLICT ROUTING

| Mechanism | Primary source | Supporting source | Current status |
|---|---|---|---|
| Fatal-flaw precheck | Road Test | TBI risk framing | K4 |
| Seven Domains | Road Test | — | K3 |
| Cheap decisive tests | TBI | Lean / SI-v3 candidate VOI | K4 |
| Validated learning | Lean | TBI | K4 |
| MVP as hypothesis test | Lean | TBI | K4 |
| Evidence-strength escalation | TBI | Invincible Company | K4 |
| Analog/antilog/leaps | Plan B | Road Test | K4 |
| Five business-model elements | Plan B | finance corpus | K4 |
| Cash timing / working capital | Plan B | finance corpus | K4 |
| Change signals | Seeing What's Next | SI-v3 candidate system dynamics | K4 theory / live facts separate |
| Motivation/ability | Seeing What's Next | live sources at runtime | K3 theory |
| Asymmetric motivation/skills | Seeing What's Next | disruption corpus | K4 |
| Jobs/pains/gains | VPD/Strategyzer | TBI | K4 |
| Human evidence hygiene | Mom Test | TBI evidence ladder | K4 |
| SDE/acquisition growth wedge | Buy Then Build/HBR | finance corpus | K4 |
| Constraint/throughput | Goldratt corpus | SI-v3 WIP candidate | K4 |
| Benefit+Barrier strategic power | 7 Powers | strategy sanity checks | K3 pending full fixture |
| Feedback/delays/policy resistance | systems corpus | SI-v3 Sterman candidate | K3/K4 candidate bridge |

## Conflict routing
**CR-01 Road Test vs Lean:** if a fatal flaw can be established cheaply from authoritative/public data, test it before building. If uncertainty is behavioral, run the smallest decisive field experiment. High-cost/irreversible tests justify more pre-analysis.

**CR-02 Planning vs testing:** maintain a compact learning plan, not a ceremonial long business plan.

**CR-03 Revenue/profit vs cash:** cash timing has an independent hard gate.

**CR-04 Large market vs micro-segment benefit:** macro attractiveness cannot rescue weak segment benefit/access/economics.

**CR-05 Innovation enthusiasm vs evidence:** internal/model excitement is not independent evidence.

**CR-06 Local optimization vs system throughput:** reject local improvement if it worsens the constraint, cash conversion or learning throughput.

**CR-07 Metric availability vs decision value:** every measurement must name the decision and uncertainty it can change.

# ENGINEERING CONTRACTS C65–C96
C65 RAW_BOOK_AUTHORITY_PRIVATE_DRIVE_ONLY  
C66 HASH_DUPLICATES_ONE_EVIDENCE_WEIGHT  
C67 CANONICAL_WORK_ID_NEQ_FILE_ID  
C68 SOURCE_PASSPORT_REQUIRES_PROVENANCE  
C69 BOOK_MECHANISM_NEQ_LIVE_MARKET_FACT  
C70 K_NEQ_E  
C71 SIGNAL_NEQ_BUYER  
C72 CURRENT_FACT_REQUIRES_FRESH_SOURCE  
C73 FATAL_FLAW_BEFORE_IRREVERSIBLE_BUILD  
C74 CHEAPEST_DECISIVE_TEST  
C75 MULTI_EXPERIMENT_EVIDENCE_STRENGTH  
C76 VALUE_HYPOTHESIS_NEQ_GROWTH_HYPOTHESIS  
C77 ANALOG_ANTILOG_LEAP_BINDING  
C78 CASH_TIMING_FIRST_CLASS  
C79 ZERO_FOUNDER_CASH_NEQ_ZERO_TOTAL_CAPITAL  
C80 UNKNOWN_ECONOMICS_NULL  
C81 NO_MAGIC_TOTAL_SCORE  
C82 CONTRADICTION_PRESERVE_DISSENT  
C83 CURRENT_CONSTRAINT_BEFORE_OPTIMIZATION  
C84 CREATE_BROKER_ACQUIRE_MANDATORY  
C85 POWER_REQUIRES_BENEFIT_AND_BARRIER  
C86 SYSTEM_EFFECT_NEQ_LOCAL_EFFECT  
C87 ACTIVE_EXPERIMENT_WIP_BOUNDED  
C88 MEASUREMENT_NAMES_DECISION  
C89 VALUE_OF_INFORMATION_BEFORE_MEASURE  
C90 REPEATED_FAILURE_TRIGGERS_HYPOTHESIS_OR_BOUNDARY_REVISION  
C91 COMPLIMENT_NEQ_EVIDENCE  
C92 PAST_BEHAVIOR_GT_HYPOTHETICAL  
C93 V3_CANDIDATE_NO_AUTHORITY_PROMOTION  
C94 CONCURRENT_MAIN_REQUIRES_BRANCH_PR_NO_FORCE  
C95 READBACK_REQUIRED  
C96 PROMPT_COUNT_NEQ_PROGRESS

## Proof objects
KnowledgeProof = `source_id, integrity, canonical_work_id, mechanism_id, provenance, conflict_state, fixture_state, K_grade`.
SignalProof = `signal_id, source_authority, observed_at, valid_from, valid_until, freshness_status, corroboration, causal_context, public_buyer_mapping, S_grade`.
MarketProof = `E_grade, buyer_identity_or_class, interaction_artifact, commitment_artifact, payment_or_PO_artifact, repeat_artifact, economics_artifact`.
No missing proof field may be synthesized.

## Protocols
P-BIZ-01 Library/Canonicalization: enumerate -> integrity -> hash -> alias -> canonical work -> quarantine invalid -> readback.  
P-BIZ-02 Source Passport/Mechanism: source -> claim -> exact provenance -> mechanism -> jurisdiction -> conflict -> fixture -> K-grade.  
P-BIZ-03 Contradiction/Confidence: preserve dissent -> identify conditions -> route by uncertainty/cost/reversibility.  
P-BIZ-04 Live Signal/Freshness: fresh source -> authority -> timestamp -> expiry -> corroboration -> forced action/budget context -> S-grade.  
P-BIZ-05 Opportunity Compilation: signal -> WhyNow -> BuyerWorkload -> micro-market -> benefit -> alternatives -> asymmetry -> assumptions -> route -> E ceiling.  
P-BIZ-06 Experiment/VOI: decision -> uncertainty -> kill power -> information value -> cost -> reversibility -> strongest permitted evidence -> test -> causal update.  
P-BIZ-07 Zero-Cash/Capital Topology: cash timeline -> founder cash gap -> customer funding -> supplier terms -> grant/loan/investor bridge -> route vectors. `€0 founder cash` is a founder constraint, not a claim that the business requires no capital.  
P-BIZ-08 Self-Improvement/Concurrency/Persistence: fresh main -> current authority -> candidate mechanisms -> bounded pilot only -> branch/PR -> CI -> Drive mirror -> readback -> promote/hold/rollback.