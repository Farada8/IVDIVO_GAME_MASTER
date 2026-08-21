# PMV217–PMV248 — ANALYTICS / PATH TO RU PILOT v1.0

## Conclusion
PMV217–248 closes the provider/voice/pilot architecture gap. Once RU text is locked and authenticated provider capabilities are known, the system can move from exactly two baseline previews to a bounded RU E01 pilot without inventing evidence or spending at season scale.

## Executable layer now ready
Provider snapshot normalization; baseline preview manifest; reproducibility analysis; PCM48 acoustic QC; deterministic blind randomization; weighted score + hard-fail override; direction response; pair exchange; fatigue protocol; semantic regression; bounded TTD/TTS gate; slice/full-render authorization; device/clue protocol; listener failure clustering; earliest-failure pickup routing; RU pilot lock.

## Proofs
Synthetic-only tests PASS: clean PCM48 passes; clipped fixture fails; pair compiler extracts 7 target lines; randomizer produces hidden key; hard fail rejects a 95-scoring synthetic candidate; bounded TTD/TTS decision executes; pilot gate fails closed when incomplete and locks only on a fully populated synthetic fixture with authority effect NONE.

## Self-improvement finding
`PREPARE DOWNSTREAM AUTOMATION WHILE BLOCKED, BUT DO NOT ADVANCE AUTHORITY WITHOUT THE BLOCKING EVIDENCE.`

## Current bottleneck
`COLLECT_PMV177_PMV180_EXTERNAL_REVIEW_RESPONSES`.

## Shortest path
External reviews → PMV209–216 RU text lock → authenticated provider snapshot → Naomi N1 + Eli E1 baseline → acoustic QC → conditional challengers → blind/direction/pair/fatigue → provisional voice lock → one TTD/TTS A/B → 3–4 minute slice → editability/device/clue → full E01 → blind listeners → pickups → RU E01 pilot lock.

## Scaling law
Scale only after the immediately smaller unit passes: line → preview → candidate → pair → fatigue → 4-minute slice → E01 → language pilot → next locale.