# 133_B03 — SPEAKER CONTEXT BATCH CH25–27 GATE v0.4

**Status:** **PASS — batch only. FULL SPEAKER GATE NOT PASSED.**  
**Story authority:** FOUNDER-LOCKED CH01–29.  
**Text mutation:** **0 bytes**.  
**Voice IDs assigned:** **0**.

## Batch result
- CH25: **120/120**, UNKNOWN 0.
- CH26: **169/169**, UNKNOWN 0.
- CH27: **153/153**, UNKNOWN 0.
- Batch: **442/442**, UNKNOWN 0.
- Reconciled cumulative CH01–27: **3340/3340**, UNKNOWN 0.
- Remaining exact scope: CH28 **166** + CH29 **208** = **374** turns.

## Strong-baseline Red Team
CH25: 28 strong overlaps, substantive conflicts 0 after role-alias normalization.

CH26: 45 strong overlaps. One substantive baseline defect:
- `B03_CH26_S0024`: baseline = SMITH; corrected acoustic speaker = `NETWORK_TECHNICIAN_CH26`.
- Text anchor: the technician connects his maintenance terminal, waits for the local controller, then says `Local view is cleaner than remote`.
- Root cause: pronoun resolver attached `he said` to Smith instead of the active grammatical/local subject.

CH27: 53 strong overlaps. One substantive audio-ownership defect:
- `B03_CH27_S0136`: baseline/source-author = TAREN; corrected acoustic speaker = SMITH.
- Text states that Smith reads Taren's reply aloud. `Taren's message continued` describes message authorship/content, not a live Taren voice.
- Production rule: source-author and acoustic speaker are separate fields when a character reads a message/document aloud.

## Drive authority
- CH25: `1CIl_lXpd-GIMsNEeuxo1oPdJThHwun-2`
- CH26: `1QCc-GOuqGcA7kxrO67i2wQwa_VwQKAx3`
- CH27: `1PdzmD7tgPhBy8SR62jncNaUT0q0Op7d8`
- manifest: `1dJBSnLhIqsg5V0MWS8lMEk0tpZF8SrsW`
- voice-map template: `1yvUlY7ZFSc8KjbHuE0VtgmWnvijLG7Kj`
- gate: `1NpofxohfThXFLq5lIJMDOMgu5_jWSvuk`
- ZIP: `1LKFhoFP8xQu6EuPnII7amqOYBF-wA_Fr`

## Safeguards
- No alternating-turn inference.
- No invented personal identity for operational roles.
- No precursor ontology invention.
- Local Slovenian operational authority remains local.
- `voice_id = null`.
- No provider call, paid synthesis, human audition, WAV, alignment, mix, master, or audio QC claimed.

## Decision
**GO to CH28–29 contextual speaker review.**
