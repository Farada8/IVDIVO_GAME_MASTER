# DETERMINISTIC TEST REPORT — G01–G32

**Execution environment:** local Python runtime during the Founder-authorized sprint.  
**Evidence class:** MACHINE_TEST / INTERNAL_EVIDENCE.  
**Cannot prove:** literary quality, human listener response, external model parity, provider performance, Founder approval or market demand.

## Evidence-aware writing gate
Command equivalent:
`python evidence_gate_validator.py writing_fixtures`

Result: **6 / 6 fixture expectations PASS**.
- machine test presented as literary proof -> rejected;
- model review presented as Human Signal -> rejected;
- dry run presented as live render -> rejected;
- persisted story gate presented as Founder lock -> rejected;
- source integrity presented as full read -> rejected;
- persisted readback used only for persisted-state claim -> accepted.

## Audio evidence boundary
Result: **3 / 3 PASS**.
- DRY_RUN -> LIVE_RENDER rejected;
- AI critique -> HUMAN_SIGNAL rejected;
- LIVE_PROVIDER bytes may support LIVE_RENDER, but explicitly cannot prove artistic quality.

## Reference lifecycle evidence boundary
Result: **3 / 3 PASS**.
- checksum/integrity -> FULL_READ rejected;
- model summary -> HUMAN_SIGNAL rejected;
- persisted synthesis -> persisted-state claim accepted, not market truth.

## Story Core causal validator
Result: **7 / 7 PASS**.
- valid causal core accepted;
- label-only/permutable core rejected;
- passive/unproven hero agency rejected;
- missing price rejected;
- weak midpoint rejected;
- climax choice that does not change outcome rejected;
- external rescue solving main conflict rejected.

## Registry/state invariant
Two-state regression:
- **BEFORE repair:** expected FAIL -> `SI-0008:COUNT=0`.
- **AFTER fixture adds SI-0008:** expected PASS.

This proves the invariant and the current defect shape. It does **not** claim the central registry has been repaired; G01 remains blocked on safe atomic mutation.

## Concurrency fixture
Result: **2 / 2 PASS**.
- second overlapping write from stale base revision -> `STALE_WRITE_BLOCKED`;
- dependency-independent branch keys serialize/read back successfully.

This is deterministic fixture evidence, not a real two-agent network/concurrency run.

## Cross-model benchmark runner smoke
Result: **1 / 1 PASS** on provider-neutral record validation.
Required fields: model, locked source_set, answer, evidence, defect_class, confidence.

Real GPT/Claude/Grok parity remains blocked because independent external backends were not available in the current session.

## Promotion consequence
No validator is promoted to universal CURRENT solely from this report. Promotion requires its application target, domain regression, evidence-class preservation, rollback path and—where requested—independent or real-product pilot evidence.
