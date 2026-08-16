# IVDIVO DRIVE INGEST LOCATOR — 2026-08-16 — PASS 04

Status: WORKING CONTROL ARTIFACT
Sources: REFERENCE ONLY

## Critical connector safeguard discovered
After many Drive move operations, a subsequent `list_folder` call returned a stale/cached-looking snapshot containing some files under INBOX even though their exact Drive IDs had already been moved successfully. Therefore:

1. Never infer a duplicate solely because a recently moved file still appears in one immediate `list_folder` result.
2. Compare Drive IDs first.
3. Same Drive ID = same object; do NOT archive it as a duplicate. Trust the successful `update_file` parent result and/or verify metadata.
4. New Drive ID + same title + same byte size as an already-routed source = classify conservatively as `LIKELY_UPLOAD_DUPLICATE` and archive, not delete.
5. All mistakenly moved same-ID items in this pass were restored to their intended working folders immediately.

Restored same-ID items:
- Dark Earth — `1ebp_mGcjErbBenaLaCL1GD72nOHPHPr4` -> GENERAL_HISTORICAL_FICTION
- Sister Mother Warrior — `1KQC9WHqSBFEkoxDTZj70oKam1jxa6Dod` -> GENERAL_HISTORICAL_FICTION
- Fire Season — `1mf6_uD5xy_mV_vNEx-eilUQzlomiKcve` -> GENERAL_HISTORICAL_FICTION
- Proving Ground — `1Ku6FAfANJM0CHjLYcNxfWHDn67m-EMfR` -> COMPUTING_ROBOTICS_HISTORY
- Joan — `1ZvDRApabLwoybSpxOu71wyhMf4Bx3whL` -> MONARCHY_DYNASTY_HISTORICAL_FICTION
- The Crimson Thread — `1tYUnJo5A1OTu140LLpxiTMDVW54rk9Ht` -> GENERAL_HISTORICAL_FICTION
- The Falcon's Eyes — `1aeL_23E3cTWnYdbZYDKcrT27VbPfkVsZ` -> MONARCHY_DYNASTY_HISTORICAL_FICTION
- The Moonday Letters — `1P8fvKyf5K_LGYMnnvBllS4vhX4k-vMuR` -> SPECULATIVE_SF_MISC

## New-ID repeat uploads archived as LIKELY_UPLOAD_DUPLICATE
Archive folder: `1T0TAJzSiNDVPZv9kzrVSwXRSjEQ-5O6r`

Psychology/craft repeats:
- The Developing Mind 3e — `1AAN1K9dARiXzWF9kS2veuudspY29TYsc`
- Four Ways to Click — `11a_tu0-xOovHix9O07bAXRs8qOr1NRbW`
- The Power of Showing Up — `1NcuQLGiRhA_G3QZ_AdiA1JVZ6aAb8ap5`
- The Developing Mind 2e — `1lCdsBbzb4U76xF8ZFF_ZsGTuEcIWi-UK`
- Disarming the Narcissist — `1LX6MLJ54BCbWR6Knidx--Jjl8LjAnUDG`
- Aware — `1SS9fajDmt_v_hhMBzutDm0FkUFqLnrLw`
- The Whole-Brain Child — `1kw54Gi70XJbaC4h7lgxu33u5vaFk-zUC`
- No-Drama Discipline — `1X8z55LDVCXdMh8ScIs3-OWrr-QMLBu0g`
- Wired for Story — `1hpix6Bv5mpJ08Grwo2Er3UuEVJgeO9V3`

Ackroyd/history repeats:
- Innovation — `1ETc9v_25bJgF7m78O2sc7134VjzeMI0W`
- Dominion — `1kzrMLMeHukm4SZ9VLUT-o4Ve_n2ESziM`
- Civil War — `1DSspLBz0zQKz5h3qVh1lQjae_IH8qvP5`
- Rebellion — `1_6t80Fg3cb5d0Zts1ZVNiuYiGiFGPDNT`
- Foundation — `1TmA7pwAhZIcw7GCxCFVm8pqv-yZbsdk8`

Romanov repeats:
- Romanov: The Last Tsarist Dynasty — `11qQATUBDDf-3OaTWrGCDZkU6Xp-tE9gn`
- Diary of Olga Romanov — `1-53Zz4-_Je1cuf4DEHf2tl6ematLx2Oh`
- The Romanovs — `1YXWGIJrOhCzWO5KH_7pgMyD9efcwEMOE`
- Nicholas and Alexandra — `1ARG1Ho6aFlyr-iInf-ziOkGk_h1Y1TEe`
- Resurrection of the Romanovs — `1BoDabKNBG-WM0eesmp8d11Tlo6tNafSm`
- The Family Romanov — `1icsQ_HJYRMaUOyW7bYYOqyetmxbfr-iZ`
- Romanov Riches — `1zxX-cFW_EW1qBZ2tK8UpuGclOswxyiza`
- The Tsars' Travels — `1Fak8aPScP84eY2FO3G-4B3A1P1qX9trq`

## Newly inspected / routed sources
- Inventing the It Girl — Hilary A. Hallett — `1Je-qMl6Y74-2Z4g72yeWm9rPb2cC1lbm`
  - route: `28_MEMOIR_BIOGRAPHY_LIVED_EXPERIENCE` — `1KEcd4W9Jhnpxzn-frQtvkohsT3zQ2Vhr`
  - inspection: nonfiction biography/cultural history centered on Elinor Glyn.
- Percy St. John and the Chronicle of Secrets — E. A. Allen — `1ItU7BaOZAY0DYtiOn-XVDvrV4BuM69BE`
  - route: `09_GENERAL_YA_LITERARY` — `1WyQvMDD232mklZsx40gaUISFzcA2iWkc`
  - inspection: youth historical mystery/adventure; 1910–1911 setting, monastery, cipher/puzzle, murder/danger engine.
- Deadly Spirits — Mary Miley — `1A9G6Bm0xXt-DX036sBB3u16f0EpIr76f`
  - route: `14_MYSTERY_THRILLER_REFERENCE` — `1gURHsf7ZcIV6T-4v9k8zmn5Sm5wdHuMM`
- The Beekeeper's War — Deborah Carr — `1F2Tb_ZsdZLW7oPMbjQezN-v1DS3Z-8oD`
  - route: `01_WARTIME_20C_HISTORICAL_FICTION` — `1OgJZmqht0kEa12MyIO7eH7ydwvJ6BuMK`
- Death and the Conjuror — Tom Mead — `1wWZ9FSjJgpx0Che57Nw5PwIClJ6peZ5Y`
  - route: `14_MYSTERY_THRILLER_REFERENCE` — `1gURHsf7ZcIV6T-4v9k8zmn5Sm5wdHuMM`
- An Accidental Romance — Karen Tuft — `1Q4ESqjov19npGq8_GLNPH11vH-k4iUmM`
  - route: `15_ROMANCE_RELATIONSHIP_REFERENCE` — `1yLVrSHo35HXxmmm8qhEygcb99dPZwn9x`
- Mademoiselle Revolution — Zoe Sivak — `1heCoMmZa4IdwX59k6Q8ekmg81SIJJfm0`
  - route: `03_GENERAL_HISTORICAL_FICTION` — `1Zp0K_YjClxPK1mwDFg55AXe-fkeizqqo`

## Operational rule
Drive update results with explicit destination `parent_ids` are treated as the immediate write result. Folder listings immediately following mass moves are advisory until refreshed/verified. Never move a same-ID file to duplicate archive on the basis of one stale listing.
