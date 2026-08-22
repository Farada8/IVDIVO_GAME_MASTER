# MASTER RECOVERY INDEX — 2026-08-22

**Audit type:** cross-project recovery / deletion-safety audit  
**Repository:** `Farada8/IVDIVO_GAME_MASTER`  
**Fresh-main replay baseline:** `3fe685436dc6a230db9d70f7116dcd28f75fa7de`  
**Global deletion state:** `NOT_YET_SAFE_TO_DELETE_ALL_CHATS`  
**Browser-tab state:** `SAFE_TO_CLOSE_TABS` — closing browser tabs is not deletion of conversation history.

> This index is a **recovery control-plane**, not a frozen copy of every project frontier. On restart, always read each project's current state/handoff from fresh `main` and Drive. Fast-moving Business, B03 audio, Self-Improvement and Personal AI state may advance after this audit without invalidating their recovery pointers.

## 1. Recovery law

`CHAT != DURABLE_AUTHORITY`

`MEMORY != SOURCE_ARTIFACT`

`LIBRARY_FILE != GITHUB_AUTHORITY`

`DRIVE_EXISTENCE != CURRENT_AUTHORITY`

`CURRENT_POINTER + DURABLE_SOURCE + READBACK > CHAT_RECOLLECTION`

`KNOWN_CHAT_ONLY_ITEM -> DELETE_ALL_CHATS_BLOCKED`

A project may be marked `SAFE_FOR_WORK_AUTHORITY` only when its material current state has a durable recovery path. This does **not** mean every conversational sentence, discarded draft, generated image or audio binary has been archived.

## 2. Status vocabulary

- `DURABLE_VERIFIED` — material authority and restart path are durably recoverable.
- `DURABLE_PARTIAL` — substantial durable state exists, but known recovery gaps remain.
- `LIBRARY_DURABLE` — material artifacts exist in ChatGPT Library; GitHub/Drive project authority is absent or not verified.
- `RECOVERY_REQUIRED` — known chat-only / not-recorded / missing-artifact gap blocks deletion safety.
- `DISCOVERY_ONLY` — useful finding, not authority.
- `UNKNOWN` — not enough evidence to classify higher.

Deletion safety:
- `SAFE_FOR_WORK_AUTHORITY` — material project work can be resumed without the source chat.
- `SAFE_AFTER_RECOVERY` — keep relevant source chats until listed gaps are closed.
- `NOT_SAFE_TO_DELETE_SOURCE_CHAT` — known chat-only evidence exists.
- `ARCHIVE_CHECK_REQUIRED` — binary/image/audio completeness has not been proven.

## 3. Project recovery matrix

| ID | Project | Recovery status | Durable recovery coordinates | Missing / residual gap | Chat deletion safety |
|---|---|---|---|---|---|
| BUS-01 | General Business Engineering OS | `DURABLE_VERIFIED` | GitHub `BUSINESS_ENGINEERING_OS/CURRENT_GENERAL_BUSINESS_ENGINE.md` + engine/state/PR evidence; Drive canonical folder `16fvKMboBdMi5_wfv8KkR8njx-raNoZ-X` | recovery index deliberately does not freeze fast-moving Business frontier; read CURRENT fresh | `SAFE_FOR_WORK_AUTHORITY` |
| BUS-02 | eTenders `8872468` | `DURABLE_VERIFIED_WITH_EXTERNAL_BLOCKER` | GitHub procurement states/validator/receipts under `BUSINESS_ENGINEERING_OS`; official documents coordinate durably recorded | current official attachment inventory/bytes not acquired; explicit bidder designation absent; these are external evidence gaps, not chat loss | `SAFE_FOR_WORK_AUTHORITY` |
| BOOK-B03 | SMITH / **THE EMPTY RESCUE** | `DURABLE_VERIFIED` | GitHub `PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json` plus B03 audio/speaker states; Drive locked master `141BOyku8VX8WXehH05rZnQGZirMOP-3iCs-5_yMJbGU` and locked manuscript `1gs64S1WxaSPUiN-BXusmceM2E-EoquDntCasFaf8zas` | manuscript/story authority is durable; any wanted unexported media binaries need separate inventory | `SAFE_FOR_WORK_AUTHORITY` |
| DORAMA-BB | **BLOODBOUND** | `DURABLE_VERIFIED_DRIVE` | Drive current authority `17dt299YyIeflzUkbfaDn3FbI9qUAoMEiHi3Otb4KSV8`; Founder Lock `1Fp0vPbvt8JaGxGIvfxwyN4LuA4BXo8Ia1Rcp2Qk8hDA`; final gate `1zaaP_q1WGJGoPJRZhsZ7nwqO3R-Q83Vqjw6uFacIr7s`; E24 `1zb0aMErYQcEPhcPC3xMit2vpQwWOmVP9qyERB92W9BI` | dedicated GitHub-native CURRENT pointer was not verified; master recovery index now supplies cross-project pointer | `SAFE_FOR_WORK_AUTHORITY` |
| DORAMA-WIFE | **THE WIFE AT HIS WEDDING** | `DURABLE_VERIFIED_DRIVE` | Drive folder `1FjjH_8AAw6ZAHZR-8wuAfc4NEIJTdxMg`; Founder Lock `1eueZnnYaUGktaSXCcMIiOAUUcINmCTV6xATBdZ9B9UA`; E1–E120 regression `1-kXiIx3utxWTmIlPUuudiWVsXLfCHbBTOAADrrLrGF8`; final gate `1C-VzyTORtauuDFZToJ4bx5Nic9dOwsrPfRudL3dAOcM` | verify wanted audio binaries separately | `SAFE_FOR_WORK_AUTHORITY` |
| AUDIO-R917 | **ROOM 917** | `DURABLE_VERIFIED_DRIVE` | Production master `1dsun3R7mdKBEnVIhPcj3Fx9l07zLKJkyDKsaUuHLLHA`; current-state doc `1u4yKOIiJwDicsh27nar52bzZ2rM48U0dnlAL5ucWDwo`; post-render folder `1P2mavegKiziTOcdNoRQvHvgEHzySY3OA`; byte-recovery tests `14f7OKXMgnRjVpgOT852fOaifqmFNBr12vQF2DPXx4qU` | text/engineering authority does not prove every wanted WAV/render binary exists outside chat | `ARCHIVE_CHECK_REQUIRED` |
| AUDIO-D01 | D01 cast/readiness | `DURABLE_VERIFIED_GITHUB` | merged project cast-readiness and universal audio runtime in GitHub | real provider inventory/auditions/voice locks/media are separate evidence and binary planes | `SAFE_AFTER_RECOVERY` |
| SI-01 | IVDIVO Self-Improvement Engine | `DURABLE_VERIFIED` | GitHub `SELF_IMPROVEMENT_ENGINE/` including recovery evidence, library current, incidents and guards; Drive CURRENT authority `1xare6Mz0FG6fDsY5QWx-hirI9D4A4BPtSG6vXY4sPa0`, library index `1-2Qpt0TFq2dQiH7LzXJHD89SdCsVVbz3z9HbhwAWH_M` | read current promotion/frontier state fresh; recovery coordinates are durable | `SAFE_FOR_WORK_AUTHORITY` |
| PAI-01 | Personal AI / Production Launch | `DURABLE_VERIFIED` | GitHub `SELF_IMPROVEMENT_ENGINE/PRODUCTION_LAUNCH_2026-08-22/CURRENT_PRODUCTION_LAUNCH_STATE.json` + `CURRENT_HANDOFF.md`; Drive launch master `1WsinAXMIo9uGLLGSg8NnKRlEDnYLd1MPk6D-46QyXuA` | local/provider credentials and local-only data are intentionally not archived here | `SAFE_FOR_WORK_AUTHORITY` |
| GAME-PORTALS | **Portals: Ireland** | `DURABLE_PARTIAL + RECOVERY_REQUIRED` | Library `PORTALS_IRELAND_IDEA_REGISTER_v0_1.csv`; this recovery ledger now preserves known missing decisions as non-canon context | explicit `CHAT_ONLY`, `CONFIRMED_NOT_RECORDED`, `TO_RECOVER` items; no verified current `PORTALY_IR` GitHub/Drive authority | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| ART-IRELAND | Ireland vintage cards / murals / Shillelagh-Wicklow | `LIBRARY_DURABLE + DURABLE_PARTIAL` | Library contains actual PNGs including `Винтажные туристические постеры Дублина.png`, `Концепты фресок Шиллега и Уиклоу.png` and individual images | complete wanted final-image inventory, dimensions/version/current status not proven | `ARCHIVE_CHECK_REQUIRED` |
| BUILD-FARADA | FARADA modular buildings / windows-doors | `LIBRARY_DURABLE` | Library spreadsheets `FARADA_G30_L45_Fabrication_RFQ_Package_v1.xlsx`, `FARADA_G30_L45_Preliminary_Engineering_BOM.xlsx` | no dedicated current GitHub/Drive project pointer verified in this pass | `SAFE_AFTER_RECOVERY` |
| WEB-PAINTERS | painters-dublin.ie | `RECOVERY_REQUIRED` | no current repo/site export or Drive handoff verified in this audit | create site/config handoff/export if chat history is needed for recovery; never persist credentials | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| MATH-ORDERS | numerical orders / bases / synthesis-growth research | `LIBRARY_DURABLE + RECOVERY_REQUIRED` | Library contains Paradigma sources, working reports and prior chat writing blocks; recovery ledger stores newest methodological constraints as hypotheses | no single current mathematical/research authority; some newest derivations were conversational | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| RESEARCH-IVDIVO | thin-body / matter / synthetic-life / consciousness-transfer research | `LIBRARY_DURABLE` | Library research corpus; Drive `IVDIVO Atlas — MASTER UNIFIED PRODUCTION PROTOCOL v7` id `1jYDgXJ4U_UP8Ei49ksZCSyTqstL6fNvG66PLBEUoS0I` | keep source doctrine, authored hypothesis, engineering possibility and fiction/worldbuilding as separate evidence classes | `SAFE_AFTER_RECOVERY` |
| WRITE-ENGINE | Book Intelligence / Writers’ Room / Dorama engines | `DURABLE_VERIFIED` | GitHub writing/Book Intelligence/Production Launch/audio engines, tests and state; Drive production packs; Library source corpus | individual media/project binaries can have their own archive gaps; raw copyrighted books remain private | `SAFE_FOR_WORK_AUTHORITY` |

## 4. High-risk chat-only recovery queue

A blanket “delete every conversation” decision is blocked by these known classes:

1. **Portals: Ireland:** explicit `CHAT_ONLY`, `CONFIRMED_NOT_RECORDED`, and `TO_RECOVER` rows exist.
2. **Visual generation:** representative PNGs survive, but complete wanted final-version inventory is not proven.
3. **Audio/provider media:** text receipts and runbooks do not substitute for wanted WAV/render bytes.
4. **Numerical-order research:** newest methodological rules/hypotheses need a single current research note.
5. **painters-dublin.ie:** current site/config export/handoff was not verified.

## 5. Predecessor recovery sources

This control-plane links, rather than silently supersedes, earlier recovery work:
- Drive `1ZVOJLoHK_kkUi5hor66dCxtm_Y4DR3WVnBeCZO4_s2Y` — `00_MASTER — IVDIVO FULL CHAT RECOVERY 32-PROMPT SPRINT + 64 NEXT PROMPTS v1.0`;
- Drive `1MsB3B0Byh4AlCMLtmPde9rXguzaejwUswBD5qPM8W50` — `18B — IVDIVO FULL CHAT TRANSCRIPT RECOVERY + INGESTION PROTOCOL v1.0`;
- Drive `1wrm_Qt2i3Csx49oeFixgCTr-pRPIYWewfsrnX_0S-sQ` — `00 IVDIVO Narrative OS — Canon & Index v1.2`.

Precedence:
`CURRENT_PROJECT_AUTHORITY > MASTER_RECOVERY_POINTER > PREDECESSOR_RECOVERY_SPRINT > CHAT_RECOLLECTION`.

## 6. Required closure before “delete all chats”

Global chat deletion can move from `BLOCKED` only when:
- [ ] every known Portals `CHAT_ONLY` / `CONFIRMED_NOT_RECORDED` item is persisted or explicitly abandoned;
- [ ] the Portals `Place Verbs` raw dictionary is recovered or formally declared irrecoverable;
- [ ] visual projects have a manifest proving every wanted final PNG exists outside chat;
- [ ] wanted ROOM917/D01/B03 and other audio renders have a binary manifest outside chat;
- [ ] numerical-order research has one current research note with hypotheses and evidence ceiling;
- [ ] painters-dublin.ie has a current export/handoff if the project remains active;
- [ ] any other wanted user-uploaded/generated artifact that exists only in a chat is exported or explicitly abandoned;
- [ ] this audit is rerun and the deletion gate changes from evidence, never assumption.

## 7. Restart protocol

1. Read `RECOVERY/MASTER_RECOVERY_STATE.json`.
2. Read the relevant project CURRENT/state/handoff from fresh `main`/Drive.
3. Prefer current durable authority over chat recollection.
4. Treat Library-only artifacts as source/evidence, not automatic current authority.
5. Read `RECOVERY/CHAT_ONLY_RECOVERY_LEDGER.md` before canonising recovered context or deleting source chats.
6. Never promote a recovery description to canon merely because the original chat is unavailable.

## 8. Current global decision

**Browser tabs may be closed.**  
**Do not yet delete all conversations.**

`MASTER_RECOVERY_MARKER: IVDIVO-MASTER-RECOVERY-20260822-V1-GLOBAL-DELETE-BLOCKED-KNOWN-GAPS-RECORDED`
