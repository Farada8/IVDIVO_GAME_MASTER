# EVIDENCE GAP MATRIX — PROCUREMENT AUTHORITY SIDE vs SUPPLIER SIDE

A field is not `FATAL` merely because it is commonly important in procurement. Until the complete current tender pack proves the requirement, classify it as `CURRENT_REQUIREMENT_UNKNOWN` or `LIKELY_EVIDENCE_CATEGORY`, never as a tender-specific threshold.

## Tender-authority side
- Complete official document inventory: MISSING — blocks authoritative requirement extraction.
- Current document bytes + hashes: MISSING — blocks pack identity / same-packet PA4.
- Addenda / revision set: MISSING — blocks authoritative delta ledger.
- ESPD / exclusion grounds: CURRENT SPECIFIC CONTENT UNKNOWN.
- Selection criteria: CURRENT SPECIFIC CONTENT UNKNOWN.
- Turnover threshold: UNKNOWN.
- Insurance thresholds: UNKNOWN.
- Similar-project requirements: UNKNOWN.
- H&S / PSCS / competence requirements: UNKNOWN.
- MEAT criteria / weights: PARTIAL, mechanism known, details unknown.
- Pricing / Billsoft structure: UNKNOWN.
- Bonds / retention / payment terms: UNKNOWN.
- Site access / occupation / phasing: UNKNOWN.

## Supplier side
- Legal name: VERIFIED from private primary formation documents — identity only.
- Legal form: VERIFIED from private primary formation documents — identity only.
- Formation-declared activity code: recovered as formation declaration — not construction capability proof.
- Current company number / CRO status: UNKNOWN.
- Tax clearance: UNKNOWN.
- Turnover history: UNKNOWN.
- Working capital / credit facilities: UNKNOWN.
- Liability insurance: UNKNOWN.
- Personnel / subcontractors: UNKNOWN.
- Similar roofing/energy-upgrade references: UNKNOWN.
- Safety statement / competence / PSCS evidence: UNKNOWN.
- Roofing and insulation capability: UNKNOWN.
- Live-school / occupied-site capability: UNKNOWN.

## Join state
`AUTHORITY_SIDE = INCOMPLETE`
`SUPPLIER_SIDE = PARTIAL_IDENTITY_ONLY`
`REQUIREMENT_BY_REQUIREMENT_JOIN = BLOCKED`
`BID/HOLD/NO-BID = NOT_AUTHORIZED`
`INDEPENDENT_PA4 = NOT_AUTHORIZED`

## Acquisition sequence
1. Recover complete current tender pack from authoritative current source.
2. Inventory and hash every document/addendum/revision.
3. Extract exact tender requirements and classify mandatory/evaluated/informational fields.
4. Separately acquire current supplier evidence for those requirements plus universal legal identity fields.
5. Bind every supplier field to a source artifact and verification timestamp.
6. Execute requirement-by-requirement join.
7. Route each item `MET / UNKNOWN / CURABLE_BEFORE_DEADLINE / NONCURABLE / NOT_APPLICABLE`.
8. Only then compile BID/HOLD/NO-BID and same-packet blinded PA4 review.
