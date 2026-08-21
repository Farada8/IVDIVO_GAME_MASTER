# SAGA100 SELF-IMPROVEMENT EVIDENCE BRIDGE v1.0

**Status:** WORKING ADAPTER TO EXISTING SELF-IMPROVEMENT v2  
**Rule:** this is not a new improvement authority or registry.

## 1. Purpose

Connect failures and verified improvements discovered during century-scale saga production to the existing IVDIVO Self-Improvement Meta Engine v2.0 without allowing story-specific observations to mutate universal rules automatically.

## 2. Candidate event contract

Each emitted event must contain:
- `event_id` unique within Saga100;
- `source_project_id` and optional `saga_slot_id`;
- `source_artifact` and version/hash/ref when available;
- `observation_type`;
- `symptom`;
- `root_cause_hypothesis`;
- `earliest_failed_layer`;
- `proposed_mechanism_change`;
- `scope_candidate = PROJECT_ONLY | LINE_LEVEL | SAGA_LEVEL | UNIVERSAL_ENGINE`;
- `evidence_refs`;
- `counterevidence_refs`;
- `required_proof`;
- `required_regression`;
- `status = OBSERVED | CANDIDATE | TESTING | ACCEPT | ACCEPT_WITH_MODIFICATION | HOLD | REJECT | PROMOTED`.

## 3. Eligible Saga100 observations

- repeated continuity substitutions caused by missing ledger fields;
- stale strategic roadmap omitted during resume;
- Smith/OES professional matrix repeatedly becomes exposition rather than action;
- Orbital future system does not affect character choice;
- Confederation capability repeatedly loses limit/cost/internal disagreement;
- crossover can be solved by advanced deus ex or arbitrary authority grant;
- philosophical question repeats earlier cycle under cosmetic terminology;
- technology/access progression jumps without bridge evidence;
- relationship consequences reset between books;
- generational age/status is frozen incorrectly;
- no-repeat gate produces false positives/negatives;
- proof gates fail to distinguish UNKNOWN from FAIL;
- long-horizon planning creates bureaucracy without changing story decisions.

## 4. Evidence classes

`E1 DETERMINISTIC`: schema/contract/test failure or machine reproducible inconsistency.  
`E2 PROJECT PROOF`: source-backed defect demonstrated in a real project.  
`E3 CROSS-PROJECT`: same abstract defect demonstrated independently in >=2 eligible projects.  
`E4 INDEPENDENT REVIEW`: Red Team/editor/reviewer working from the same authoritative source and producing a traceable diagnosis.  
`E5 HUMAN/EXTERNAL`: real reader/editor/market/perceptual evidence where the claim requires human signal.

Repeated model paraphrases of one observation remain one evidence family.

## 5. Promotion rules

### Project-only
Promote locally when a defect and repair are proven for one project but generality is unproven.

### Line-level
Requires recurrence across at least two books in the same line or a deterministic line-specific contract failure.

### Saga-level
Requires recurrence across multiple lines/cycles or a structural defect in shared Saga100 contracts.

### Universal engine
Requires evidence that the mechanism improves non-Saga100 production too; must pass current Self-Improvement v2 promotion/regression law. Saga100 cannot grant this status itself.

## 6. Regression protocol

Use:
`SYMPTOM -> ROOT CAUSE -> EARLIEST FAILED LAYER -> SMALLEST EFFECTIVE REPAIR -> SELECTIVE DESCENDANT REGRESSION`.

Never globally rewrite locked manuscripts because a prompt/contract wording improved.

## 7. First candidate family created by this cycle

### S100-SI-CANDIDATE-001 — STRATEGIC_AUTHORITY_DISCOVERABILITY
**Observation:** long-horizon NARR-009 existed in Drive but was missed when a narrow CURRENT execution slice was loaded.  
**Hypothesis:** current project freshness routing and long-horizon strategic discovery are conflated.  
**Proposed repair:** strategic authority pointer + separate `EXECUTION_FRONTIER` and `LONG_HORIZON_STRATEGY` retrieval classes in CrossConversationFreshnessGuard.  
**Evidence:** direct conversation failure + persisted NARR-009 + current router law requiring persisted state recovery.  
**Status:** CANDIDATE / proof required.  
**Required next proof:** R32 Persistence/Freshness Tests reproduces the omission and demonstrates recovery.

### S100-SI-CANDIDATE-002 — NON_DESTRUCTIVE_SEQUENCE_IDENTITY
**Observation:** existing Bxx project IDs predate a new 25x4 scheduling law.  
**Risk:** global renumbering would damage references and authority.  
**Repair:** preserve PROJECT_ID, add SAGA_SLOT_ID mapping.  
**Status:** ACCEPTED_AS_SAGA100_WORKING_MECHANISM; universal promotion not requested.

### S100-SI-CANDIDATE-003 — CIVILIZATION_DELTA_PROOF
**Observation:** long saga development can become lore accumulation unless each book records an earned durable change.  
**Repair:** require P-S100-CD and ConsequenceLedger.  
**Status:** CANDIDATE / validate on B02/B03/B07/B08 before promotion.

## 8. Fail-closed rules

Do not promote when:
- source authority is ambiguous;
- evidence is only model preference;
- repair was not tested against the defect;
- regression scope is unknown;
- project-specific lore would leak into universal rules;
- an accepted change would reopen locked story without unlock evidence.
