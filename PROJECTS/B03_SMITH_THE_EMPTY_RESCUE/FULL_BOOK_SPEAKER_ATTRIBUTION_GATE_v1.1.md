# 138_B03 — FULL-BOOK SPEAKER ATTRIBUTION GATE v1.1 — RECONCILED

**STATUS: PASS — FULL BOOK SPEAKER OWNERSHIP CLOSED.**  
**Book:** B03 — THE EMPTY RESCUE  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Locked prose mutation:** **0 bytes**  
**CH30 authorized:** **NO**  
**Voice IDs assigned:** **0**  
**Provider dispatch authorized by this gate:** **NO**

## 1. Why v1.1 exists

v1.0 correctly closed acoustic-speaker ownership at **3714/3714**, but it was created before the CH24 source-identity quarantine repair. Its CH22–24 provenance therefore pointed to v0.4, where two separate precursor packet recordings shared one speaker/source id despite no textual proof that they were the same source.

v1.1 preserves all chapter-local ownership decisions and arithmetic, while replacing only that unsafe identity merge with the repaired CH22–24 v0.5 authority.

## 2. Immutable source

- Exact-text segmentation package: Drive `1FuDJDUGNjgsNITpNmfQV_d8N4oIrs5HB`
- Package SHA-256: `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`
- Total segments: **7465**
- Original curly-quoted spans: **3718**
- Proven narrator-inline quoted spans: **4**
- Actual cast speech denominator: **3714**

Narrator-inline semantic exceptions remain unchanged:
1. `B03_CH02_S0200`
2. `B03_CH16_S0082`
3. `B03_CH17_S0002`
4. `B03_CH19_S0206`

## 3. Chapter-local authority chain

- CH01–03: **376/376**, UNKNOWN 0 — reconciliation v4.
- CH04–06: **491/491**, UNKNOWN 0 — re-audited; CH06 S0038 corrected to Smith.
- CH07–09: **257/257**, UNKNOWN 0.
- CH10–12: **490/490**, UNKNOWN 0.
- CH13–15: **202/202**, UNKNOWN 0.
- CH16–18: **219/219**, UNKNOWN 0.
- CH19–21: **355/355**, UNKNOWN 0.
- CH22–24: **508/508**, UNKNOWN 0 — **v0.5 source-boundary repaired authority**.
- CH25–27: **442/442**, UNKNOWN 0 — Red Team corrections retained.
- CH28–29: **374/374**, UNKNOWN 0 — final contextual batch.

Arithmetic:
`376 + 491 + 257 + 490 + 202 + 219 + 355 + 508 + 442 + 374 = 3714`.

**Result: 3714/3714 actual speech turns have chapter-local contextual acoustic-speaker ownership. Residual UNKNOWN speaker ownership = 0.**

## 4. CH24 source-identity quarantine

The following five CH24 dialogue segments are still assigned to packet-local acoustic sources, but the two recordings are no longer asserted to share identity:

- `B03_CH24_S0152`, `B03_CH24_S0154` → `PRECURSOR_SOURCE_CH24_PACKET_1`
- `B03_CH24_S0376`, `B03_CH24_S0378`, `B03_CH24_S0380` → `PRECURSOR_SOURCE_CH24_PACKET_2`

Inter-packet identity relation: **UNKNOWN**.

Corrected CH24 map: Drive `1hzNIm7VyLiiuip2gDiZS4InvEPpzGKqx`  
SHA-256: `8c10023044771e420ae0fd59e9f2188a3696b449428a296a18ec66aa37c7c04e`  
Repair gate: Drive `1tl4xYMLOQmnJPT-PIAzDOMNFwrrzpu9L`  
Repaired CH22–24 manifest: Drive `1eGz0wHrkl7owFgXlSlmHec88-5_Fnsth`

Hard rule: `SAME_TOPIC_OR_PACKET_CLASS != SAME_SPEAKER_IDENTITY`.

Casting may later choose one performer for multiple unknown sources as an artistic decision, but metadata must not convert that casting choice into claimed source identity.

## 5. Proven regression defects retained

- `B03_CH06_S0038`: action/attention boundary proved Smith, not Jana.
- `B03_CH22_S0216`: manual strong evidence proved road control, not Maja.
- `B03_CH24_S0152/S0154/S0376/S0378/S0380`: separate packet boundaries prohibit unsupported identity merge.
- `B03_CH26_S0024`: local grammatical/action subject is network technician, not Smith.
- `B03_CH27_S0136`: Taren is source author; Smith is acoustic speaker reading aloud.
- `B03_CH29_S0312`: active local male subject is `OES_SUPERVISOR_CH29`, not Smith.

## 6. Acoustic speaker vs source identity

Downstream metadata must distinguish where applicable:
- `source_author`
- `source_identity`
- `acoustic_speaker`
- `delivery_mode`
- `source_boundary`

A known acoustic speaker does not prove the identity of a quoted, recorded, relayed, or document source.

## 7. Authority boundaries

PASS means speaker ownership is complete enough to enter casting/voice-binding production.

This gate does **not** claim:
- provider account access;
- paid synthesis authorization;
- human audition approval;
- Slovenian pronunciation approval;
- voice lock;
- generated WAVs;
- alignment/timestamps;
- sound-asset acceptance;
- Hard Pilot assembly;
- mix/master/audio QC;
- market or Human Signal evidence.

`voice_id` remains `null` until casting evidence is accepted.

## 8. Canon / jurisdiction safeguards

- Locked CH01–29 prose unchanged.
- CH30 remains forbidden without Founder unlock.
- Slovenian rescue authority remains local.
- Taren/Confederation remains analysis/advisory only.
- OES labels do not create local command authority.
- Precursor origin/mechanism remains UNKNOWN.
- Anonymous operators/callers/technicians remain role-labelled unless the story names them.

## 9. Decision

**FULL SPEAKER ATTRIBUTION GATE v1.1: PASS.**

**Supersedes:** `137_B03_FULL_BOOK_SPEAKER_ATTRIBUTION_GATE_v1.0` for downstream speaker/casting provenance only. v1.0 remains valid historical evidence for the 3714/3714 closure before the source-boundary repair.

### Next production frontier

**CASTING + PRONUNCIATION + LIVE S0 EVIDENCE.**

Required sequence:
1. enumerate real provider workspace voices/models;
2. build casting roster from canonical speaker/source roles;
3. bind temporary audition candidates only;
4. create Slovenian/proper-name pronunciation test set;
5. preserve exact-text hashes;
6. run bounded S0 audition jobs only after provider capability is verified;
7. collect provider/model/voice provenance and alignment;
8. human cast + pronunciation adjudication;
9. after accepted voice lock, run CH01 Hard Pilot/canary;
10. no bulk CH01–29 synthesis before Hard Pilot PASS.
