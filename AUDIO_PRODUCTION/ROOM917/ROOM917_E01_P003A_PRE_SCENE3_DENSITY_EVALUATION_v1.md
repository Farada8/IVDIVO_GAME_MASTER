# ROOM917 E01 — P003A PRE-SCENE3 DENSITY / ROOM-BED EVALUATION v1

**Date:** 2026-08-21  
**Status:** P003A COMPLETE AT SEGMENT/CONTRACT LEVEL / EXACT PATCH TIMECODES STILL REQUIRE BYTE-ACCESS OR LOW-LEVEL INTERVAL MAP  
**Story:** LOCKED — `THE INSURABLE FIRE`  
**Target segment:** `00:00.000–07:24.980` (first 444.980 s of current full E01 master)  
**Preserved downstream:** Scene 3 `07:24.980–10:58.190` v1.3E technical lineage PASS.

## 1. Sources

Current project evidence:
- `ROOM917_E01_SCENE3_LIVE_LINEAGE_RECOVERY_v1`, Drive `1fLsYEFBvP_TPBjotET2zGnqjWGBxgnw9smGiClmNuGE`;
- `ROOM 917 — AUDIO PRODUCTION OVERLAY v2.0`, Drive `1_kvPrAs0lQnDl7SvC3FzDLOtmqUSNQmgfAQgCzUv810` — CANON project audio overlay;
- `ROOM 917 — E01 ELEVENLABS ACTOR + SOUND DIRECTOR MASTER v1.0`, Drive `1Rz_Tv83fNhQIuPnMA4jRkESmgiu8xA-GZnctbQYDP_I` — current-branch E01 actor/sound contract;
- `ROOM 917 — E01 P001 + P002 ARTIFACT EVIDENCE PASS v1`, Drive `1n0DNOgQIU4LMl7GTSdKju8KdoOxYdEWpfvStagCbiZE`;
- `15_ROOM917_E01_DIRECTOR_SCORE_REFERENCE_FIXTURE_v0.1`, Drive `1P-W8UuLBlAcb24RpblEuP82O_-iiIdfhabf3spEj6-g` — WORKING fixture used only where compatible with current branch and higher authority.

No human/perceptual master listen is claimed in this pass.

## 2. Objective pre-Scene3 evidence

For `00:00.000–07:24.980`:
- channel correlation ~0.996636;
- Mid/Side gap ~24.95 dB;
- sample peak ~-2.15 dBFS;
- ~109.8 s of 100 ms windows below -45 dBFS;
- ~103.2 s below -50 dBFS;
- ~36.1 s below -85 dBFS.

Corrected Scene 3 tail comparison:
- 213.210 s duration;
- 0.0 s below -45 dBFS in 100 ms windows;
- 0.0 s below -50 dBFS;
- minimum 100 ms RMS ~-43.18 dBFS.

The difference is materially large and is the reason for this targeted evaluation.

## 3. Authored-silence reconciliation

Persisted QC defines six protected-silence masks in E01. Only ONE belongs to pre-Scene3:

`E01_S02_SIL001 = 21,600 samples = 0.450 s`.

The remaining five protected masks belong to Scene 3.

The pre-Scene3 protected pause is narratively intentional and must remain protected from generic tightening/fill. It is associated with a procedural/status collision, not a broad instruction to make Scenes 1–2 silent.

Therefore the formal pre-Scene3 protected-silence budget is only 0.450 s. It cannot by itself account for ~36.1 s below -85 dBFS or >100 s below -45/-50 dBFS.

Important firewall: this does NOT mean every remaining low-level window is defective. There may be short authored beats, transitions, fades or valid quiet physical actions. Exact locations are not yet available in this pass.

## 4. Scene 1 acoustic contract — Greyhaven lobby

Higher project overlay requires locations to remain materially distinguishable and characters to audibly move through them.

E01 Sound Director contract defines:

`A01_GREYHAVEN_LOBBY_30S_LOOP`
- old seaside hotel lobby;
- Atlantic rain at tall windows;
- distant wind;
- radiator ticking;
- sparse distant staff/cutlery activity;
- large stone-room resonance;
- no voices in the bed;
- no music.

Director fixture identifies:
- scene `E01_S01_LOBBY`;
- acoustic passport `ROOM917_GREYHAVEN_LOBBY_v1`;
- roomtone `GREYHAVEN_LOBBY_LOOP`;
- `AMB_LOBBY_START` anchored at SCENE_START;
- ambience is background and ducks under dialogue, but is not specified to disappear.

Required physical events in Scene 1 include, depending on block:
- revolving-door tail / arrival;
- rain and distant lobby work;
- Julian measured stone steps;
- keyring placed with control;
- later carpet transition into switchboard area;
- cabinet/wood/metal/toggle tactile actions.

### P003A classification — Scene 1

`ROOM_BED_EXPECTATION = CONTINUOUS_MATERIAL_PRESENCE`.

Short sparse moments may be valid, but extended near-digital silence is inconsistent with the authored lobby identity unless a specific transition/fade contract proves otherwise.

Any < -85 dBFS interval materially longer than a transition/intentional beat inside active Scene 1 is therefore a `MISSING_ROOM_OR_AMBIENCE_SUPPORT_CANDIDATE` until exact position mapping closes it.

## 5. Scene 2 acoustic contract — switchboard alcove, evening

E01 Sound Director contract defines:

`A02_SWITCHBOARD_ALCOVE_30S_LOOP`
- smaller carpeted alcove attached to the lobby;
- rain materially present but spatially changed/muted by distance;
- old wood cabinet;
- faint building resonance;
- no horror tone.

Block-specific requirements add:

### E01-07 — chain of custody
- rain stronger in the active moment;
- clean test tone;
- clips / camera actions.

### E01-08 — limiter / bridge
- dry competence rhythm;
- NO romance music;
- NO breathy romantic proximity.

“No romance music” does not mean “remove room acoustic identity.”

### E01-09 — board wakes / weather noise
Required causal sound chain:
1. transformer;
2. short recognition space;
3. relay ripple;
4. conduit/weather signature.

The recognition space is a semantic beat inside an active room, not authorization for long digital silence.

### E01-10 — normal 916 test
- selector clack;
- faint glass ping;
- comedy remains alive while clue grammar remains audible.

### E01-11 — first status fight
Dialogue pressure is the foreground, but no contract removes the alcove bed.

### E01-12 — concession / care without romance
- one beat of rain;
- Julian exhales;
- NO music;
- NO romantic pause.

This explicitly requires audible environment/body behavior rather than empty digital space.

### E01-13 — after Julian leaves
- Julian steps recede;
- door;
- perceptible smaller-room state;
- probe contacts left-to-right.

Again, the smaller room must remain materially legible.

### P003A classification — Scene 2

`ROOM_BED_EXPECTATION = CONTINUOUS_BUT_CHANGED_MATERIAL_PRESENCE`.

There is exactly one formal protected silence mask in Scene 2: `E01_S02_SIL001 = 0.450 s`.

Outside that mask and valid short semantic beats, long or repeated near-digital-silence windows are incompatible with the room-presence and causal-action contract.

## 6. Music conclusion — do NOT solve this defect with score

The older E01 actor/sound master explicitly specified Scene 1 = NO SCORE and Scene 2 = NO SCORE. The newer CANON project overlay v2.0 is less absolute: music remains restrained/consequence-based and may use buttons, transitions, aftermath and selective thematic return, while forbidden from supplying evidence.

Therefore P003A does NOT authorize blanket background music as a repair for low density.

The current production defect must first be repaired at its earliest demonstrated layer:

`ROOM / WEATHER / MATERIAL BED -> BODY/FOLEY/CAUSAL ACTION -> only then optional selective music if a later commercial/perceptual gate justifies it`.

This protects the commercial-quality experiment from confusing “more score” with “a scene that physically exists.”

## 7. Defect register

### D003 — PRE_SCENE3_ROOM_BED_CONTINUITY_UNDERCOVERAGE

**Severity:** MAJOR  
**Status:** `PROVEN_AT_SEGMENT_AGGREGATE_LEVEL / EXACT_PATCH_INTERVALS_NOT_YET_RESOLVED`

Evidence:
- Scene 1 and Scene 2 contracts require persistent material/acoustic identities;
- only 0.450 s of formal protected silence exists pre-Scene3;
- measured pre-Scene3 contains ~36.1 s below -85 dBFS and >100 s below -45/-50 dBFS;
- corrected Scene 3 lineage demonstrates 0.0 s below -45/-50 dBFS while preserving authored protected silence.

This is enough to establish an aggregate bed-continuity undercoverage problem. It is NOT enough to identify every exact interval or authorize blanket fill.

**Patch status:** HOLD FOR INTERVAL MAP.

### D004 — PRE_SCENE3_CAUSAL_FOLEY / ACTION UNDERDENSITY

**Severity:** MAJOR candidate  
**Status:** `CANDIDATE_NOT_PROVEN`

Reason:
Scenes 1–2 contain many explicitly required physical actions. Without exact low-level interval positions or perceptual listen, we cannot prove which specified actions are absent/under-mixed versus already present.

**Patch status:** NOT AUTHORIZED YET.

### D005 — PRE_SCENE3_MUSIC UNDERUSE

**Severity:** WORKING COMMERCIAL HYPOTHESIS, not production defect in current baseline.  
**Status:** `HOLD_FOR_P003B / COMMERCIAL_A_B_C_TEST`

Founder reports music feels insufficient versus professional commercial references, but current E01 baseline deliberately minimized score. Do not relabel this as a canonical defect until perceptual/commercial testing separates music need from missing physical scene-bed need.

## 8. Classification law for the missing interval map

When exact low-level intervals become available, classify each interval as exactly one of:

1. `PROTECTED_AUTHORED_PAUSE` — preserve; no fill beyond allowed baseline.
2. `VALID_LOW_DENSITY` — intentional brief semantic/transition space with sufficient room identity.
3. `MISSING_ROOM_OR_AMBIENCE_SUPPORT` — room/world disappears contrary to acoustic passport.
4. `MISSING_CAUSAL_OVERLAP_CANDIDATE` — a specified physical/causal event should occupy/support the moment.
5. `UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE` — no safe automatic decision.

No generic silence removal is permitted.

## 9. P003A verdict

**P003A = PASS WITH ONE PROVEN AGGREGATE MAJOR + ONE MAJOR CANDIDATE.**

- D003 room-bed continuity undercoverage = PROVEN at aggregate pre-Scene3 level.
- D004 causal Foley/action underdensity = CANDIDATE.
- D005 music underuse = commercial hypothesis pending perceptual/A-B evidence.
- Scene 3 v1.3E technical lineage remains protected PASS.

## 10. Exact next obligations

### P003A-2 — INTERVAL LOCALIZATION
Recover or generate from the exact master a list of pre-Scene3 low-level intervals, especially contiguous regions below -85, -50 and -45 dBFS. Map them to current Scene 1/2 block/cue lineage. This can be machine analysis and does not require aesthetic judgment.

### P004A — SELECTIVE BED PATCH CONTRACT
Only after interval localization, patch demonstrated `MISSING_ROOM_OR_AMBIENCE_SUPPORT` intervals with the correct scene bed and crossfades; preserve transitions/protected silence. Do not blanket-fill the whole segment.

### P003B — HUMAN/PERCEPTUAL LISTEN
Still required for:
- acting/prosody;
- commercial music need;
- body/Foley realism;
- intimacy/relationship tension;
- mystery comprehension;
- pacing/emotional pull;
- sellability.

### COMMERCIAL A/B/C
Only after technical physical-world defects are repaired:
- A = restrained forensic/current baseline;
- B = commercially enhanced body/ambience/selective scoring;
- C = premium hand-polished dramaturgical mix.

Compare at matched playback loudness. Do not infer commercial GO from machine QC.
