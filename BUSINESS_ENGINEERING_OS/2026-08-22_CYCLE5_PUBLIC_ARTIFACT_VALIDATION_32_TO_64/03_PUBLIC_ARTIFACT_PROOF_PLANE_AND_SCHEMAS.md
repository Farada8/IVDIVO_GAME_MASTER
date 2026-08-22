# CYCLE5 — PUBLIC ARTIFACT PROOF PLANE + SCHEMAS

## PA proof plane
`PA` measures maturity of a decision artifact. It is deliberately independent from Knowledge K, Signal S and Market E proof.

- **PA0 IDEA** — artifact concept only.
- **PA1 CONTRACTED** — named user class, named decision, typed inputs, null policy, falsifier and next action exist.
- **PA2 SOURCE-POPULATED** — official/current public sample data populates the schema with provenance.
- **PA3 REGRESSION-PASS** — deterministic checks prove null safety, evidence ceiling, timing and lane-specific invariants.
- **PA4 INDEPENDENT-VALIDATED** — a genuinely independent reviewer or alternate implementation reproduces or improves decision utility without violating proof boundaries.
- **PA5 REAL-USE** — a real target user actually uses the artifact to make, change or reject a decision.

### Non-substitution law
`PA != K != S != E`.

A PA3 or PA4 sample artifact does not prove buyer willingness-to-pay, payment, repeatability, unit economics or retention. Public-only Cycle5 work cannot reach PA5 and cannot promote market evidence above E2+.

## Base ArtifactObject
Required fields:
- `artifact_id`
- `lane`
- `decision_owner_class`
- `decision`
- `inputs{}` with explicit known/unknown status
- `outputs{}`
- `unknowns[]`
- `falsifier`
- `next_action`
- `sources[] = {url, authority, observed_at, freshness_status}`
- `sample_data=true|false`
- `PA_grade`
- `market_claim_grade`

## Artifact acceptance gate
An artifact is rejected if any of the following is true:
1. it lacks a named decision;
2. it silently converts unknowns to numbers;
3. a secondary source is used where a current official source is available without explanation;
4. it claims procurement eligibility, grant approval, finance approval, legal clearance or WTP from public data;
5. it has no falsifier or next action;
6. sample/fictitious user data is not labelled;
7. market claim grade exceeds E2+ under public-only work;
8. PA5 is claimed without real target-user decision-use evidence.

## ProcurementDecisionArtifact extension
Required: `resource_id`, contracting authority, title, procedure/status, published time, submission deadline with timezone, public scope/CPV, estimated value if present, qualification unknowns, full-document-review gate.

**Important:** public scope match != eligibility != bid recommendation. Without full procurement documents and a verified supplier profile the highest permitted output is a bounded next action such as `PROCEED_TO_FULL_DOCUMENT_REVIEW`.

## RetrofitRouteArtifact extension
Required: route decision, property-data inputs, grant-before-work rule, registered-contractor dependency, OSS/individual distinction, technical assessment dependency where applicable, cash-timing note, missing inputs.

**Important:** no numerical lead score from public grant rules alone. Property BER, dwelling facts, technical assessment, quotes and contractor availability remain independent evidence.

## SMEAIWorkflowArtifact extension
Required: employee count, trading age, Digital for Business prerequisite, EI/IDA client status, solvency evidence state, current software inventory, workflow pain object, proposed software category, new-to-business test, co-funding/configuration constraints, public-support substitution analysis.

**Important:** Grow Digital eligibility != LEO approval != willingness-to-pay for an adviser. A generic digital audit is directly threatened by the fully-funded Digital for Business review; the commercial wedge must be differentiated implementation/configuration/workflow execution.