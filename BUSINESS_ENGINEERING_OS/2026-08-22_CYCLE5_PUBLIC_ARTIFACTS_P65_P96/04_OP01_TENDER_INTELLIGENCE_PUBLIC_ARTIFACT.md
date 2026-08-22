# OP01 PUBLIC ARTIFACT — Tender / Procurement Decision Brief
**Observed:** 2026-08-22
**Evidence ceiling:** E2+ public-only. This is a sample decision artifact, **not** buyer proof, bid eligibility, legal/procurement advice, or a recommendation to submit.

## What this artifact is testing
Whether current public procurement data can be transformed from an alert list into a decision-ready brief that exposes deadline, workload, fit signal, and fatal unknowns before a contractor spends time on tender documents.

## Current sample — five live/public opportunities

### 8899923 — Refurbishment and Repair of Sash windows at Moyderwell building Tralee Co. Kerry
- Contracting authority: Kerry Education and Training Board
- Published: 2026-08-21 17:29 IST
- Submission deadline: **2026-09-21 12:00 IST**
- Public estimated value: €200,000
- Procurement/work type: Works
- Fit signal: windows / refurbishment / glazing / painting
- Fatal unknown before bid/no-bid: exact tender documents + supplier capability requirements.
- Decision state: `REVIEW_CAPABILITY`, not BID/NO-BID yet.
- Official source: https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8899923

### 8894062 — Summer Works 2026 — Refurbishment of 2 Home Economics Rooms, Tullow Community School
- Contracting authority: Tullow Community School
- Published: 2026-08-21 11:10 IST
- Submission deadline: **2026-09-18 17:00 IST**
- Public estimated value: €230,000
- Procurement/work type: Works
- Fit signal: building + M&E refurbishment
- Fatal unknown: drawings/specifications and supplier capability requirements.
- Decision state: `REVIEW_CAPABILITY`.
- Official source: https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8894062

### 8826393 — 58 Mayorstone Drive Limerick — municipal building to 2 apartment units + extension
- Contracting authority: Limerick City and County Council
- Published: 2026-08-12 12:35 IST
- Submission deadline: **2026-09-09 12:00 IST**
- Public estimated value: €300,000
- Procurement/work type: Works
- Fit signal: residential refurbishment / first-floor extension / A2 target / ancillary works
- Fatal unknown: full works capability and procurement qualification requirements.
- Decision state: `REVIEW_CAPABILITY`.
- Official source: https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8826393

### 8893404 — Heat Pump Supply, Installation and Commissioning — IWA Clontarf
- Contracting authority: Irish Wheelchair Association
- Published: 2026-08-21 15:29 IST
- Submission deadline: **2026-09-25 15:00 IST**
- Public estimated value: €75,000
- Procurement/work type: specialist M&E works
- Fit signal: heat-pump plant, controls, pipework, commissioning
- Fatal unknown: specialist M&E / heat-pump competence and exact tender qualification criteria.
- Decision state: `SPECIALIST_REVIEW_REQUIRED`.
- Official source: https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8893404

### 8788179 — Deep Energy Retrofit 2 — Stage 0 Energy Audit
- Contracting authority: Health Service Executive
- Published: 2026-08-06 12:03 IST
- Submission deadline: **2026-09-11 17:00 IST**
- Public estimated value: `null / not stated in the public result used`
- Procurement/work type: specialist energy consulting services across 30 healthcare sites
- Fit signal: strong signal of downstream retrofit/decarbonisation workload; not automatically a construction bid.
- Fatal unknown: specialist consulting qualification and exact tender criteria.
- Decision state: `SIGNAL_OR_SPECIALIST_REVIEW`, not BID/NO-BID.
- Official source: https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8788179

## Decision rubric — veto first
1. Is the notice still open according to deadline + current portal state?
2. Does the supplier have the exact work category/capability?
3. Are registration, insurance, tax clearance, turnover, certification, prior-experience, bonds or framework conditions satisfied? **Unknown until tender documents/capability file are read.**
4. Is there enough lead time to price and assemble evidence?
5. Is estimated contract value relevant to the supplier's scale? This is not revenue until an award exists.
6. If any fatal requirement is unknown, state `REVIEW_REQUIRED`, not a score.

## Artifact result
The artifact improves *decision structure* versus a raw alert because it exposes qualification unknowns and deadline risk. It still does not prove that an SME will pay for the service. `NEXT_EVIDENCE = E3_EXTERNAL_BEHAVIOUR_WHEN_AUTHORISED`.
