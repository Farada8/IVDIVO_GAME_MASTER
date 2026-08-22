# EVIDENCE GAP MATRIX — PROCUREMENT AUTHORITY SIDE vs SUPPLIER SIDE

## Rule
A field is not `FATAL` merely because it is commonly important in procurement. Until the complete current tender pack proves the requirement, classify it as `CURRENT_REQUIREMENT_UNKNOWN` or `LIKELY_EVIDENCE_CATEGORY`, never as a tender-specific threshold.

## A. Tender-authority side
| Evidence category | Current state | Effect |
|---|---|---|
| Complete official document inventory | MISSING | Blocks authoritative requirement extraction |
| Current document bytes + hashes | MISSING | Blocks pack identity / same-packet PA4 |
| Addenda / revision set | MISSING | Blocks authoritative delta ledger |
| ESPD / exclusion grounds | CURRENT SPECIFIC CONTENT UNKNOWN | Blocks current exclusion mapping |
| Selection criteria | CURRENT SPECIFIC CONTENT UNKNOWN | Blocks supplier qualification join |
| Turnover threshold | UNKNOWN | Cannot evaluate financial capacity |
| Insurance thresholds | UNKNOWN | Cannot evaluate coverage |
| Similar-project requirements | UNKNOWN | Cannot classify references |
| H&S / PSCS / competence requirements | UNKNOWN | Cannot classify compliance evidence |
| MEAT criteria / weights | PARTIAL: mechanism known, details unknown | Blocks evaluation model |
| Pricing / Billsoft structure | UNKNOWN | Blocks pricing-workload/cash analysis |
| Bonds / retention / payment terms | UNKNOWN | Blocks cash-risk model |
| Site access / occupation / phasing | UNKNOWN | Blocks delivery-capacity join |

## B. Supplier side
| Evidence category | Current state | Effect |
|---|---|---|
| Legal name | VERIFIED from private primary formation documents | Identity only |
| Legal form | VERIFIED from private primary formation documents | Identity only |
| Formation-declared activity code | VERIFIED as historical formation declaration | Not construction capability proof |
| Current company number / CRO status | UNKNOWN | Current legal-identity verification incomplete |
| Tax clearance | UNKNOWN | Supplier evidence slot incomplete |
| Turnover history | UNKNOWN | Financial capacity unproven |
| Working capital / credit facilities | UNKNOWN | Delivery cash capacity unproven |
| Public/employers/other liability insurance | UNKNOWN | Insurance evidence unproven |
| Direct personnel / subcontractors | UNKNOWN | Delivery capacity unproven |
| Similar roofing/energy-upgrade references | UNKNOWN | Experience unproven |
| Safety statement / competence / PSCS evidence | UNKNOWN | Safety/competence unproven |
| Roofing system capability | UNKNOWN | Specialist scope unproven |
| Insulation capability | UNKNOWN | Specialist scope unproven |
| Live-school / occupied-site capability | UNKNOWN | Site-delivery evidence unproven |

## C. Join state
`AUTHORITY_SIDE = INCOMPLETE`
`SUPPLIER_SIDE = PARTIAL_IDENTITY_ONLY`
`REQUIREMENT_BY_REQUIREMENT_JOIN = BLOCKED`
`BID/HOLD/NO-BID = NOT_AUTHORIZED`
`INDEPENDENT_PA4 = NOT_AUTHORIZED`

## D. Acquisition sequence
1. Recover complete current tender pack from authoritative current source.
2. Inventory and hash every document/addendum/revision.
3. Extract exact tender-side requirements and classify mandatory/evaluated/informational fields.
4. Separately acquire current supplier evidence for only those requirements plus universal legal identity fields.
5. Bind every supplier field to a source artifact and verification timestamp.
6. Execute requirement-by-requirement join.
7. Route each item `MET / UNKNOWN / CURABLE_BEFORE_DEADLINE / NONCURABLE / NOT_APPLICABLE`.
8. Only then compile BID/HOLD/NO-BID and same-packet blinded PA4 review.
