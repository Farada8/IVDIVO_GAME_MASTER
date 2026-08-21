# BODYGUARD FOR THE FALLEN IDOL
## E01 — ELEVENLABS ROUGH RENDER RUN SHEET v1.0

**STATUS:** READY FOR VOICE BINDING  
**AUTHORITY:** Recording Master v1.6 — RECORDING LANGUAGE CLEAN  
**SOURCE DOC:** `1blOK7CwpExgKZ4QJriMFY6tMDyJgtiy4GAsGLonrqcE`  
**EPISODE:** E01 — “11:43”  
**EXACT TEXT:** LOCKED  
**VOICE IDs:** NULL until casting lock  
**ABSOLUTE TIMESTAMPS:** prohibited until render alignment

# 1. COVERAGE
- Source spoken lines: **190**
- Render requests: **190**
- Source spoken words: **1,344**
- Render-request spoken words: **1,344**
- Expected master count: **1,344**
- Ordered exact-text match: **PASS**
- Every source speech line exactly once: **PASS**
- SHA-256 spoken-sequence match: **PASS**
- Unique block IDs: **PASS**

**COVERAGE VERDICT: PASS — READY FOR ROUGH RENDER**

# 2. BLOCK DISTRIBUTION
- S1 — soundcheck: **64** spoken blocks
- S2 — final preset: **52** spoken blocks
- S3 — live show / collapse / evidence: **74** spoken blocks
- Isolated TTS blocks: **37**
- Standard TTS blocks: **153**

# 3. PROCESSING DOMAINS
- `CLEAN_DIALOGUE`: **174** blocks
- `CREW_COMMS`: **2** blocks
- `IEM_THREAT`: **2** blocks
- `NARRATION_VO`: **3** blocks
- `PHONE_MEDIA`: **1** block
- `SHOW_COMMS`: **8** blocks

Mandatory isolation:
- `VOICE IN IEM` → `IEM_THREAT`; stereo-left is a mix property, not a text change.
- `PHONE REPORTER` → `PHONE_MEDIA`.
- Naomi V.O. → `NARRATION_VO`.
- crew utility → `CREW_COMMS`.
- live-show Talia → `SHOW_COMMS`.
- every HIGH/CRITICAL performance line → isolated TTS.

# 4. TAKE LOAD
- CRITICAL: **13**
- HIGH: **12**
- STANDARD: **165**

CRITICAL/HIGH → 3 takes: `NEUTRAL_TRUTH / DIRECTOR_ADJUSTED / UNDERPLAYED`  
STANDARD → 2 takes: `NEUTRAL_TRUTH / DIRECTOR_ADJUSTED`

Do not select the most emotional take automatically. Select the take that most clearly performs the story function.

# 5. P51 / P52 / P53 CONTROL
**Naomi:** precision first. Danger makes her clearer, not louder. Personal cost appears only after safety and never removes environmental awareness.

**Eli:** public polish → private economy. Threat creates one private fracture, not helplessness. He remains an active witness and chooser.

**Cal:** operationally plausible. Defensive is allowed; villain coding is not.

**Talia:** show-control authority. Cue language must sound habitual. Alarm comes from broken procedure.

**Threat voice:** human, neutral, deliberate. No monster processing, sinister whisper or theatrical menace.

**Relationship target:** **privately important, professionally constrained.**

No chemistry beat may delay safe action. Functional contact ends when function ends. After-action recognition is where emotional voltage belongs.

# 6. PRIORITY ISOLATIONS
Key isolated blocks include:
- `BG_E01_S1_028` — emergency movement contract.
- `BG_E01_S2_087` / `088` — autonomy vs emergency authority.
- `BG_E01_S2_106` / `111` — Daniel information-control wound / Naomi protection ethic.
- `BG_E01_S3_120` — threat voice.
- `BG_E01_S3_121` — Eli private fracture.
- `BG_E01_S3_122` — `Cross right. Now.`
- `BG_E01_S3_135` — missing acknowledgement.
- `BG_E01_S3_152` — wrong-side talkback clue.
- `BG_E01_S3_160` / `161` — bodypack consent.
- `BG_E01_S3_165` — public media frame.
- `BG_E01_S3_173` — insider logic.
- `BG_E01_S3_180` — Eli reclaims memory.
- `BG_E01_S3_181` — threat replay.
- `BG_E01_S3_186` / `188` / `190` — four-click / left-channel / changed theory.

# 7. RENDER ORDER
1. Bind temporary casting voices; do not change text.
2. Render Naomi calibration lines.
3. Render Eli public/private/emergency calibration lines.
4. Render all CRITICAL/HIGH blocks in three takes.
5. Render STANDARD blocks in two takes.
6. Assemble raw dialogue with no music.
7. Add story-critical SFX only.
8. Apply acoustic-domain processing.
9. Build stereo rough.
10. Build mono rough.
11. Build phone/small-speaker reference.
12. Cut the 64-second cold open from aligned render.
13. Run the blind-listener protocol.
14. Create pickup entries only from evidence.

# 8. FAIL-CLOSED CONDITIONS
Do not advance if:
- any exact text differs from source;
- total spoken words ≠ 1,344;
- a source speech line is missing or duplicated;
- threat/media/comms domains are not isolated;
- a required clue works only in stereo;
- Naomi reads reckless before the intended public frame;
- Eli reads helpless;
- music is needed to create chemistry;
- Cal is villain-coded by performance;
- blind testing reveals a repeated blocker.

# 9. MACHINE-READABLE SOURCE
`BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json`

The JSON contains all **190** ordered spoken requests, exact text, source order, voice-role placeholders, P51/P52/P53 performance direction, acoustic/post-chain domains, take plans, null alignment fields and fail-closed coverage validation.
