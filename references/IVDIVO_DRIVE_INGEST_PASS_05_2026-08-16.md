# IVDIVO Drive Ingest — PASS 05 — 2026-08-16

Status: WORKING CONTROL LOG

## Scope
Continued physical routing from `IVDIVO_LIBRARY/19_INBOX_TO_PROCESS` after PASS_04.

## Important ingest rule
Drive `list_folder` may temporarily show stale membership after mass moves. Therefore:
- same Drive file ID = same source; never archive it as a duplicate merely because an old folder listing still shows it in INBOX;
- duplicate handling requires a genuinely new Drive ID plus matching bibliographic identity / file size / edition evidence;
- ambiguous genre is checked from EPUB metadata/content before routing.

## New routing completed in this pass

### Contemporary / literary fiction
- The Making of Her — Bernadette Jiwa — Drive ID `1H-oyqscjO24LavOYv6HLNr4ggOBmtihg` → `10_CONTEMPORARY_LITERARY_FICTION`
- The Sorcerer of Pyongyang — Marcel Theroux — `1wVP6KQcVW-SCWbeVOBD1cC4kN1c6U_gq` → `10_CONTEMPORARY_LITERARY_FICTION`
- Hotel Moscow — Talia Carner — `1XEnmIfBAOxVp2saTWRdL0_eh947FedHu` → `10_CONTEMPORARY_LITERARY_FICTION`
- The Force of Such Beauty — Barbara Bourland — `1J9mfgjcO1F2yaLxlvh8gNRJIn3KO1Dlg` → `10_CONTEMPORARY_LITERARY_FICTION`

### Wartime historical fiction
- Steel Girls on the Home Front — Michelle Rawlins — `1ym9P0vHbUvuzgH_U95zifbgwcYwqwrln`
- To Kill the Leopard — Theodore Taylor — `1YveFWAb9eeUkyEpgf-aKA2QNwoowXvwq`
- The Runaway Orphans — Pam Weaver — `1vfV3J3MzdkkM6hx93SYG95lGx5Ii6n8P`
- The Other Girl — Pam Jenoff — `186plYPgs2sfJgtrw1dufH2unYHIJxgBg`
- The Ways We Hide — Kristina McMorris — `1DwiWdr1HGKpYg8CrKswOExrLY2m41AiI`
→ `09_ADVENTURE_HISTORICAL_FICTION/01_WARTIME_20C_HISTORICAL_FICTION`

### General historical fiction
- A Dress of Violet Taffeta — Tessa Arlen — `1Q3DxZBjwuKAZxYXuwl5p-YBb4vX3N9ot`
- Forty Elephants — Erin Bledsoe — `1fR_55erRt7fXjT5LG_suM5OyK3isPVEm`
- On Gin Lane — Brooke Lea Foster — `1BXvXqkTYKAH7wgKDX5iMYHqPI61G71Re`
- The Manhattan Girls — Gill Paul — `1JYJmqdhgnCxWcQMp-2waJL3g76CTF1zG`
- On the Rooftop — Margaret Wilkerson Sexton — `1uFhCsgMfGQrp49lH3Bx7uX_J2ThWj9Gj`
- The Brightest Star — Emma Harcourt — `1zVCJWdLnbGguDdXDgwJC7FO0BUOeBM6a`
- The Two Lives of Sara — Catherine Adel West — `1kfS9w3ekFDaKsj8aehaw6VuTnU3haKy-`
- The Last Dress from Paris — Jade Beer — `13On240OWmgN1u6YmKRWaMkmZnyRSIa2-`
- A Mother's Betrayal — Emma Hornby — `16SXZbk_bMU4cfubqxIIiFZHiLOuFS7ff`
- The Nurse's Secret — Amanda Skenandore — `14bzbhStXhf4cYRfvvtxamCITxKpXKgN0`
- Groupies — Sarah Priscus — `13KahNxxOs7pEcXMFSS4hQFaMR6hqUvCs`
- An Orphan's Song — Lizzie Page — `1jBtRXOZXjO1SSVbas1a1MfQy-05kWY7u`
- The Horse Master's Daughter — Elles Lohuis — `1XceCdr133hEOigJZ5VocI6xttwAm2eOm`
- Mother of Strangers — Suad Amiry — `1fUMooB_cegF_h0sM4q-kiysvrCCCaUag`
- The Secret Wife — Mark Lamprell — `17NRIEa9SNOf17ja7xT6tGR80C4RABEDa`
- A Remarkable Woman — Jules Van Mil — `1OYDjBEJlRpdJcsxfZTVp1k4GPVIK4Z8m`
→ `09_ADVENTURE_HISTORICAL_FICTION/03_GENERAL_HISTORICAL_FICTION`

### Mystery / thriller reference
- The Man in the Shadows — Alys Clare — `1e6whgf48yv1mx-sDiOUngLlxRI8UT-Yr`
- Gods of Deception — David Adams Cleveland — `1_EoL5b7jFqhmJzM1XoV-9e4JfSzWErkL`
- Deception — Lesley Pearse — `1br1zMQoQSw7Fe7n-NMsqZqWa7MxiOqg1`
- Golden Cargoes — Fiona Buckley — `1YEs9mGVfJWSciVJhmTJuJCzVXEI-27Gv`
- Death at the Manor — Katharine Schellman — `1wJ-DTUEdBB_pum0bs0EfyTBQ5Up-BUkt`
- Murder at the Victoria and Albert Museum — Jim Eldridge — `1fMlNaj9uQPN-chNVSPDbX4RbZeNPse8S`
→ mystery/thriller reference shelf

### Romance / relationship reference
- A Tenuous Betrothal — Jen Geigle Johnson — `1kTTgTQSmm4eyTRvDHDmPAdoUBQHrtbXZ`
- A Secret From the Duchess' Past — Leah Conolly — `1U7jwc3n9X5dNkIP2GHwrBboUgi4COgfs`
- Cutslut — Kim Jones — `1OuVJ7LkFWaN18nazdNFRXZb-6vZ95IJH`
- Family Ties — Stephie Walls — `1A47ZQrEtRiWayQu8BZeUYORCGFrA1t_i`
- Cry Baby — Ginger Scott — `1ZhQy_8twW-Kk5VkmkyHbNdkscmVtnt6Z`
→ romance/relationship reference shelf

### Fantasy / horror reference
- The Monsters We Defy — Leslye Penelope — `1L8Ct_ZaFjeCUnLMZkvIuehshsc6PYEDP` → fantasy reference
- Bloody Fool for Love — William Ritter — `1Bp7B75T7dUNOlUtOUPpab_IlySbJYkHo` → horror/dread reference
  - EPUB metadata verified this is a Buffy prequel featuring Spike/Drusilla and supernatural London; title alone would have misclassified it as romance.

### Nonfiction / world-source
- Holland House — Linda Kelly — `1olj9J8wP0bnqlX-lUirHnNvCcVqo0vZ6` → Britain/Ireland history
- The Price of Time — Edward Chancellor — `19g7iW5UIRXT2dV2L6CbfiNWZKaDoAsOJ` → general civilization/institutions
- Blood and Roses — Helen Castor — `1iCRxnW1jzuJFLeB1rBN6aw7M0PG5ebZv` → Britain/Ireland history
- The Social Life of Books — Abigail Williams — `1oCO9vHXzOVvRNbFDr_Qjl0Q4s0J4iMAG` → Britain/Ireland history
- Disability and the Tudors — Phillipa Vincent-Connolly — `1Uxaf8AIum66D2YC9yyH792l9aAPtw4_0` → Britain/Ireland history
- House of Treason — Hutchinson — `1z9dOrcouBPNiGqHAUypczu5S0gPe5f6p` → Britain/Ireland history
- Watching Darkness Fall — David McKean — `1KdDQf-H99KTQOCrygIl1mq6LciQsdiKg` → European war/monarchy/dynasties
- Diana, William and Harry — James Patterson — `1bLHqu8GgEXteRaiEvTbpMSQSE9zy9i7E` → biography/lived experience
- Enjoy Me Among My Ruins — Juniper Fitzgerald — `1yvTBsM5vPrK0EIykP-gbUNW7PT6TKEv_` → biography/lived experience

## Editorial relevance for IVDIVO
This pass materially strengthens:
- ordinary family and social life for future Ireland and Orbital Youth;
- women-centered historical pressure and status systems;
- mystery engines built around institutions and physical places;
- wartime logistics, civilian pressure and clandestine action;
- real-world institutional history kept separate from dramatized historical fiction;
- supernatural reference mechanisms without importing franchise canon.

REFERENCE LAW remains: extract mechanisms only; never import protected plots, distinctive characters, dialogue or signature inventions into IVDIVO.
