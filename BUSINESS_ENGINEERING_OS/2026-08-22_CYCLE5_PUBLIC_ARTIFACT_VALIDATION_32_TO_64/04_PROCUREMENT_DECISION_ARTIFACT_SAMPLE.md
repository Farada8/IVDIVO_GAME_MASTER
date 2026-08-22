# PA-PROC-001 — TENDER DECISION CARD

**Lane:** tender/procurement decision intelligence  
**PA grade:** PA3 after Cycle5 regression  
**Market grade:** E2+ ceiling / no buyer proof  
**Sample data:** yes — public official tender data, not a claim about any specific supplier's eligibility.

## Decision
Should an SME contractor/bid manager spend time and bid-preparation resources on a full document review for this opportunity?

## Official public sample
Source: Ireland eTenders / Government of Ireland.  
Resource ID: `8872468`  
Contracting authority: **St Joseph's Secondary School (Ballybunion)**  
Title: **Climate Summer Works: Roof replacements and energy efficiency upgrades at St. Joseph’s Secondary School and the adjacent former Convent Building in Ballybunion, Co. Kerry**  
Published: **19 Aug 2026 10:33 IST**  
Submission deadline: **2 Sep 2026 17:00 IST**  
Procedure: **Open**  
Procurement type: **Works**  
Estimated value: **€1,600,000**  
Public CPV/scope signals: roof works, roof-covering, demolition, thermal insulation. Public summary names replacement of roof weathering membranes, upgraded thermal insulation, replacement of rooflights and ceilings, wall-insulation upgrades and renewal of rainwater goods.

Official source pointer: `https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468`

## Public scope-match vector
- roofing / weathering membrane work: HIGH public scope presence
- thermal insulation: HIGH public scope presence
- wall-insulation upgrade: PRESENT
- rainwater goods: PRESENT
- rooflight/ceiling replacement: PRESENT
- heritage/specialist-conservation requirement: UNKNOWN from public listing
- electrical/M&E package: UNKNOWN / not inferred

This is **not** a supplier-fit score. It describes the tender scope only.

## Qualification fields that remain UNKNOWN until full tender-document extraction
- minimum turnover / financial standing
- tax-clearance requirements
- insurance limits
- required similar-project references and value thresholds
- PSDP/PSCS / H&S requirements and competence evidence
- bonds / parent guarantees
- programme and school-occupation constraints
- site-visit requirements
- subcontracting rules
- award criteria / quality-price weighting
- mandatory certifications / standards
- document list / ESPD or declarations

## Artifact output
`PUBLIC_SCOPE_MATCH = POTENTIAL`

`BID_DECISION = UNKNOWN`

`PROCUREMENT_ELIGIBILITY = NOT_PROVEN`

`NEXT_DECISION = PROCEED_TO_FULL_DOCUMENT_REVIEW`

## Why this output is decision-useful
The public listing is enough to reject obviously irrelevant opportunities and enough to justify opening the full documents where scope is materially relevant. It is **not** enough to recommend a bid because qualification and delivery constraints can still be fatal.

## Fatal-assumption / falsifier
Reject or HOLD after full-document review if mandatory turnover, insurance, prior-project evidence, programme, bonding, access, safety or specialist requirements are incompatible with the verified supplier profile.

## Next cheapest test
Download the complete tender pack and compile a `TenderQualificationObject` with:
`mandatory criterion -> evidence required -> supplier evidence state -> gap -> cure possible? -> deadline risk -> BID/HOLD/NO-BID`.

## Proof boundary
This artifact proves that a current public opportunity exists and that its public scope can be structured into a decision card. It does **not** prove that any named company qualifies, will win, can deliver profitably or will be paid on acceptable terms.