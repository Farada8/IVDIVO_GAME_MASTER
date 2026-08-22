# MONEY MECHANISMS P49–P50 — MINIMUM DELIVERY SOP + QA / ACCEPTANCE

**Status:** INTERNAL DELIVERY ENGINEERING ONLY / NO REAL DELIVERY EXECUTED / NO EXTERNAL ACTION AUTHORIZED

## Authority and dependency boundary

Canonical `05_NEXT64.md` defines:

- P49 — design minimum delivery SOP;
- P50 — define QA and acceptance evidence;
- P51 — measure actual delivery hours/cost after first real delivery.

Therefore this block closes only P49–P50. It does **not** invent P51–P56 evidence.

Current WIP3 remains:

1. `OW-01` — corrected cross-protocol/custom-stack Agent Commerce diagnostic;
2. `CF-01` — Article 50 technical transparency diagnostic, non-legal and non-certifying;
3. `CF-03` — DPP supplier-data / Registry readiness diagnostic, non-certifying and no live Registry action.

`DELIVERY_SOP_READY != DELIVERY_OCCURRED`

`QA_SPEC_READY != CUSTOMER_ACCEPTANCE`

`CUSTOMER_ACCEPTANCE != LEGAL_COMPLIANCE`

`SYNTHETIC_RUNTIME != ACTUAL_DELIVERY_HOURS`

## P49 — Minimum delivery SOP

### Common delivery state machine

All three lanes use the same bounded envelope:

`SCOPE_FREEZE -> INPUT_MANIFEST -> EVIDENCE_CLASSIFY -> RUN_DIAGNOSTIC -> HUMAN_REVIEW -> UNRESOLVED_REGISTER -> PACKAGE -> QA_GATE -> DELIVERY_READY`

No case may skip from intake directly to a polished conclusion.

### Step D0 — Scope freeze

Before analysis, record:

- lane id and diagnostic version;
- buyer/user role if known;
- exact system/product/use-case boundary;
- included surfaces/assets;
- excluded surfaces/assets;
- permitted evidence sources;
- prohibited claims;
- freshness cut-off;
- confidentiality/data-handling boundary;
- requested output form.

If the scope requires legal opinion, certification, live Registry action, production credential use, or unsupported platform approval, route to `HOLD_OUT_OF_SCOPE`.

### Step D1 — Input manifest

Create a machine-readable or structured manifest of every input used. Each item binds:

- source id;
- source type;
- provenance class;
- collection/assessment date where relevant;
- version/release where relevant;
- hash or stable reference where practical;
- owner or source authority;
- sensitivity flag;
- admissibility for the diagnostic.

Missing evidence remains missing; it is never silently reconstructed from generic assumptions.

### Step D2 — Evidence classification

Normalize evidence into the lane’s allowed states. At minimum distinguish:

- observed/tested evidence;
- customer-declared evidence;
- design-only evidence;
- unknown/missing evidence;
- not-applicable evidence.

`UNKNOWN` must never be promoted to `PASS` or `FAIL` merely to complete the report.

### Step D3 — Deterministic diagnostic run

Use the current pinned implementation/ruleset for the lane. Capture:

- tool/ruleset version;
- input manifest reference;
- execution timestamp/reference when a real run exists;
- raw machine result;
- errors/warnings;
- rerun/reproducibility information.

A narrative-only answer with no traceable diagnostic result is not an accepted delivery.

### Step D4 — Human review

A reviewer checks only for:

- correct scope and role;
- evidence-to-finding traceability;
- rule applicability;
- unsupported inference;
- false certainty around UNKNOWN;
- stale-rule or source drift;
- contradiction between machine output and source evidence;
- forbidden legal/certification/platform-approval language.

Human review may downgrade a claim to HOLD/UNKNOWN or correct a deterministic implementation error. It may not upgrade missing evidence into proof.

### Step D5 — Unresolved-item register

Every unresolved item receives:

- item id;
- affected finding/control/data point;
- missing or contradictory evidence;
- owner/source needed;
- decision impact;
- disposition: `HOLD`, `NEEDS_EVIDENCE`, `OUT_OF_SCOPE`, or `NON_BLOCKING_LIMITATION`.

The unresolved register is a first-class output, not an appendix to hide uncertainty.

### Step D6 — Delivery package

Every package contains:

1. scope/exclusions;
2. input/evidence manifest;
3. diagnostic version;
4. finding/control/data-gap table;
5. evidence references for each material result;
6. unresolved-item register;
7. limitations and prohibited interpretations;
8. correction/revalidation instructions;
9. QA receipt;
10. explicit statement of what the packet does **not** prove.

### Step D7 — QA gate

Only `QA_PASS_DELIVERY_READY` may advance to delivery-ready status. Other routes:

- `QA_RETURN_FOR_CORRECTION`;
- `QA_HOLD_SCOPE_OR_EVIDENCE`;
- `QA_ABORT_UNSAFE_OR_OUT_OF_SCOPE`.

### Step D8 — Post-delivery evidence placeholder

For a future real delivery only, capture:

- delivery start/end timestamps;
- actual operator hours by stage;
- direct external costs;
- number of correction loops;
- customer acceptance/rejection evidence;
- what decision, if any, the artifact changed;
- requested follow-up;
- payment state.

All these fields are currently NULL/0 because no real delivery is executed by P49–P50.

## Lane-specific delivery contracts

### OW-01 — Agent Commerce diagnostic

**Required inputs:** normalized provenance-labelled merchant/system snapshot; tested protocol/product-data surfaces; current ruleset/version; admissible evidence for public/private claims.

**Minimum output:**

- finding table using `PASS / FAIL / UNKNOWN / NOT_APPLICABLE`;
- applicable OpenAI-feed/UCP rule ids and ruleset version;
- source/evidence reference per material finding;
- separate product-feed vs UCP readiness;
- binding/transport applicability preserved;
- unresolved private-state items kept UNKNOWN;
- correction/retest instructions.

**Hard failures:**

- generic “AI-ready” advice replaces deterministic findings;
- platform approval is implied;
- public page observation is presented as private merchant declaration;
- unknown transport/private state becomes FAIL or PASS without evidence;
- old ruleset is used after a material protocol/ruleset drift without explicit version pinning.

### CF-01 — Article 50 technical transparency diagnostic

**Required inputs:** actor role; system/content use; relevant deployment surface; evidence objects; exception/special/transition facts where invoked.

**Minimum output:**

- routed Article 50 branch(es);
- provider/deployer distinction;
- control object(s);
- evidence object(s);
- unresolved legal/implementation items;
- versioned source/rule baseline;
- explicit non-legal/non-certifying limitation.

**Hard failures:**

- provider and deployer obligations are merged;
- transition becomes exemption or blanket grace period;
- DESIGN_ONLY/UNKNOWN/NOT_TESTED becomes implemented;
- Code adherence becomes automatic compliance proof;
- technical packet states or implies legal certification/compliance clearance.

### CF-03 — DPP supplier-data / Registry readiness diagnostic

**Required inputs:** declared applicability state; economic-operator role/id; product identity; product-specific mapping source; carrier/payload location; supplier evidence; imported-product fields where applicable.

**Minimum output:**

- preflight disposition;
- deterministic data/evidence gap list;
- supplier-evidence provenance;
- product-specific required-point source;
- Registry metadata vs decentralised payload separation;
- correction/revalidation instructions;
- explicit no-live-Registry/no-certification limitation.

**Hard failures:**

- generic product-group priority is treated as legal applicability;
- guessed universal DPP field list is presented as authoritative;
- missing supplier evidence is labelled product noncompliance;
- Registry-generated identifier is claimed before registration;
- preflight readiness is labelled Registry acceptance.

## P50 — QA and acceptance evidence

### QA dimensions

Every future real delivery must pass all seven dimensions:

1. **Scope fidelity** — output stays inside frozen scope/exclusions.
2. **Evidence traceability** — every material finding maps to admissible evidence or explicit UNKNOWN.
3. **Deterministic reproducibility** — same frozen inputs + same pinned ruleset reproduce the material machine result, except explicitly non-deterministic external probes.
4. **Boundary fidelity** — no legal certification, platform approval, Registry acceptance, market demand or profitability claim is manufactured.
5. **Freshness/version fidelity** — ruleset/source versions are recorded and known drift is surfaced.
6. **Uncertainty fidelity** — HOLD/UNKNOWN/NOT_APPLICABLE are preserved rather than cosmetically resolved.
7. **Package completeness** — scope, manifest, findings, unresolved register, limitations, correction path and QA receipt are present.

### QA receipt schema

A future QA receipt must contain:

- case id;
- lane id;
- diagnostic/ruleset version;
- input-manifest reference;
- reviewer;
- review timestamp;
- seven QA dimension states;
- defect list;
- correction count;
- final QA disposition;
- delivery-package reference;
- evidence hash/reference where practical.

Allowed QA states per dimension:

`PASS`, `FAIL`, `HOLD`, `NOT_APPLICABLE`.

Final QA disposition:

- `QA_PASS_DELIVERY_READY` only if every applicable dimension is PASS;
- `QA_RETURN_FOR_CORRECTION` if a correctable defect exists;
- `QA_HOLD_SCOPE_OR_EVIDENCE` if required scope/evidence is missing;
- `QA_ABORT_UNSAFE_OR_OUT_OF_SCOPE` for prohibited or unsafe delivery requests.

### Customer acceptance evidence — future real delivery only

Customer acceptance is recorded independently from internal QA. Allowed states:

- `NOT_DELIVERED`;
- `DELIVERED_AWAITING_REVIEW`;
- `ACCEPTED_AS_SCOPED_TECHNICAL_DELIVERABLE`;
- `RETURNED_FOR_CORRECTION`;
- `REJECTED_SCOPE_OR_VALUE`.

Acceptable evidence may include an explicit written acceptance, an approved delivery milestone, or other auditable customer action tied to the scoped technical artifact.

`SILENCE != ACCEPTANCE`

`ACCEPTED_TECHNICAL_DELIVERABLE != COMPLIANCE_CERTIFICATION`

`ACCEPTANCE != PAYMENT`

`PAYMENT != REPEATABILITY`

### Current P49–P50 execution state

`REAL_DELIVERIES = 0`

`ACTUAL_DELIVERY_HOURS = NULL`

`ACTUAL_DELIVERY_COST = NULL`

`CUSTOMER_ACCEPTANCE_EVENTS = 0`

`PAYMENTS = 0`

`REPEAT_DELIVERIES = 0`

`P49 = PASS_ENGINEERING`

`P50 = PASS_ENGINEERING`

## Dependency stop

P51–P56 remain blocked until real evidence exists.

Specifically:

- P51 cannot be closed without actual delivery hours/cost;
- P52 cannot be closed from synthetic throughput alone;
- P53–P55 cannot infer repeat/renewal/referral from zero deliveries;
- P56 cannot open a scale gate without economics + delivery + demand evidence.

Therefore the correct next Money Mechanisms state after this block is **50/64 internal prompts executed, 14 remaining, with P51–P56 evidence-blocked**.

READBACK_MARKER: `MONEY-MECHANISMS-P49-P50-DELIVERY-QA-2OF2-NO-REAL-DELIVERY-20260822`
