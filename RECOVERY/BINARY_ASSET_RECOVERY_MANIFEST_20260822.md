# BINARY ASSET RECOVERY MANIFEST — 2026-08-22

**Purpose:** distinguish real missing binary risk from projects that have not generated live media yet.  
**Rule:** `TEXT/RECEIPT != BINARY BYTES`; `NO_LIVE_BINARY_CREATED != MISSING_BINARY`; `EXISTED_BUT_NOT_DURABLY_LOCATED = RECOVERY BLOCKER`.

## A. AUDIO

### ROOM 917 — full E01 real master

- Asset: `ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav`
- Evidence status: **REAL ASSET EXISTED**.
- Expected SHA-256: `231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8`
- Expected size: `189,558,764 bytes`
- Format: WAV / 48,000 Hz / 24-bit PCM / stereo
- Duration: `658.190 s` (`10:58.190`)
- Recorded ChatGPT File Library pointer: `file_000000002c8081f58d0e656cdc0e7267`
- Recorded Library path: `/IVDIVO — SAGA WRITERS' STUDIO/ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav`
- Drive ingest register: `ROOM 917 — FIRST RENDER INGEST + VERSION CONTROL REGISTER — v1.0`, Drive ID `1v_A25N-fxI097TqxQh4hgp7db5gdJFaInczUSNWYktY`
- Post-render engineering evidence records **two raw reacquisition attempts returning HTTP 403** for this full master. This proves the problem was already encountered as a byte-persistence/readback failure, not merely a missing catalog entry.
- The same post-render evidence says an accepted Scene3 WAV materialized successfully, so transport was not globally unavailable; the full-master failure is asset-specific/persistence-specific.
- Current recovery status: **BINARY_DURABILITY_NOT_VERIFIED / CONTROLLED_DRIVE_DUPLICATE_NOT_CONFIRMED / PRIOR_REACQUISITION_HTTP403_CONFIRMED**.
- Action allowed: locate identical bytes, verify size + SHA-256, copy to controlled Drive ingest, read back, register stable Drive ID.
- Action forbidden: rerender and silently substitute a different master.

### ROOM 917 — Scene 3 pilot package

- Provenance evidence: independent forensic review records inspection of `ROOM917_E01_SCENE3_FINAL_PILOT_v1_FULL.zip` with master/premaster/mono/mobile WAVs, 6 stems, 10 dialogue takes + alignment/bound requests, 18 sound assets, asset report, timeline and QC.
- Named master: `ROOM917_E01_SCENE3_MASTER_24BIT_48K.wav`
- Objective evidence: 48 kHz / 24-bit PCM / stereo / `213.210 s`; technical engine proof PASS, artistic mix NOT READY.
- Prior File Library transcript evidence explicitly lists both the Scene3 WAV and the full Scene3 ZIP as uploaded Library items.
- Post-render engineering evidence says the accepted Scene3 control WAV **materialized successfully** during the earlier repair investigation.
- Current Drive search: named WAV not located in controlled Drive during this audit.
- Current recovery status: **EXISTED / PREVIOUS_MATERIALIZATION_SUCCEEDED / CONTROLLED_DURABLE_BYTE_LOCATION_UNVERIFIED**.

### D01 / THE WIFE AT HIS WEDDING audio

- Current Drive render authority explicitly says: `NO LIVE AUDIO GENERATED`.
- Principal voice IDs are not yet locked.
- Recovery status: **NOT_A_MISSING_BINARY**.
- Do not create a deletion blocker merely because planned filenames exist in a dry-render manifest.

### B03 / SMITH — THE EMPTY RESCUE audio

- Current GitHub state: story/release locked; audio is still at speaker-attribution frontier (`580 / 3715` current assignments), voice map not authorized.
- No current authority claims a finished live WAV master.
- Recovery status: **PRE_LIVE / NOT_A_MISSING_MASTER_BINARY**.

### Audio deletion gate

`AUDIO_DELETE_GATE = BLOCKED_BY_ROOM917_REAL_BINARY_DURABILITY_ONLY`

Any additional audio project becomes a blocker only if evidence proves a wanted live binary existed and that binary cannot be recovered from durable storage.

## B. VISUALS

### Wicklow / Shillelagh durable image outputs

Controlled Drive folder: `WICKLOW_SHILLELAGH_MASTER_PROJECT/07_IMAGE_OUTPUTS`, folder ID `1lh6725Bax555GG3l3KdIVLrJt_S3afNR`.

Known durable PNGs:

| File | Drive ID | Size | Recovery class |
|---|---|---:|---|
| `women_carry_memory_board.png` | `1NBATcf8uItQn8BsNGR34hUCwfcoWH7D_` | 3,428,073 | `PRELIMINARY_APPLICATION_STUDY` |
| `ten_concepts_contact_board.png` | `1rtQTce_HDOj86EOqzIYe0TsMNjgaL8aI` | 3,469,516 | `PRELIMINARY_APPLICATION_STUDY` |
| `house_many_windows_variant.png` | `10hdfcU42tVTeH9wzQQHWtY75TGdLmwMW` | 3,160,183 | `PRELIMINARY_APPLICATION_STUDY` |
| `house_many_windows_board.png` | `1ZoTIVFu0kzl8nmloskoLsYRiB_wsDOd-` | 3,483,590 | `PRELIMINARY_APPLICATION_STUDY` |
| `great_cartouche_primary.png` | `1nu0fKByoPoKzg0x8SGwLuSAip1Nma-Nk` | 3,155,568 | `PRELIMINARY_APPLICATION_STUDY` |
| `giulio_hyperreal_railway.png` | `16gQTzydwX8sICiKqBSjUdx8ASmDAn4HO` | 3,216,590 | `PRELIMINARY_APPLICATION_STUDY` |
| `alternate_vertical_mural.png` | `1lBJNKKhkBlZKEbtbugIvhjWuZjIze4R_` | 3,082,611 | `PRELIMINARY_APPLICATION_STUDY` |

Current Shillelagh application authority explicitly says the concept visualisations are preliminary and **not final mural designs**. This resolves their selection class without inventing a final mural.

### File Library visual evidence

Multiple generated images survive in File Library, including Shillelagh concept boards, Dublin tourism cards and Portals-related images. Library existence preserves bytes, but an old image can represent superseded architecture; therefore Library presence alone is not current canon.

Detailed routing authority:
`RECOVERY/VISUAL_SELECTION_RECOVERY_MANIFEST_20260822.md`.

### Visual deletion gate

`VISUAL_DELETE_GATE = BLOCKED_FINAL_SELECTION_ROUTING_NOT_COMPLETE`

Required closure is a selection manifest, not merely a file-count manifest:

`WANTED_FINAL_IMAGE -> STABLE FILE/DRIVE ID -> PROJECT/PLACE -> DIMENSIONS -> CURRENT/REJECTED/ARCHIVE -> OPTIONAL HASH`

Old Portals prototype imagery that depicts superseded architecture remains `ARCHIVE/REFERENCE`, not current game authority.

## C. RECOVERY DECISION

Remaining confirmed binary-risk classes:

1. ROOM917 full E01 master bytes — real asset; prior reacquisition HTTP 403; controlled Drive duplicate unverified.
2. ROOM917 Scene3 full pilot package — real package; prior Scene3 WAV materialization succeeded; current controlled byte location unverified.
3. Cross-project visual final-selection routing — many bytes survive, but exact wanted-final classification is incomplete.

False blockers removed:

- D01 planned WAV names where no live audio has been generated.
- B03 live master where production has not reached live master generation.
- Shillelagh image outputs already present in controlled Drive.

`BINARY-RECOVERY-20260822-EVIDENCE-GATED-NO-FAKE-MISSING-BINARY-CLAIMS`
