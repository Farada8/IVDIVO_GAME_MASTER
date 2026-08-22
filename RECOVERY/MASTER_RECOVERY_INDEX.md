# MASTER RECOVERY INDEX — 2026-08-22

**Audit type:** cross-project recovery / deletion-safety audit  
**Repository:** `Farada8/IVDIVO_GAME_MASTER`  
**Fresh-main baseline at audit branch cut:** `a13b835aea9779840ad40c8266df9cf5ba1e9763`  
**Global deletion state:** `NOT_YET_SAFE_TO_DELETE_ALL_CHATS`  
**Browser-tab state:** `SAFE_TO_CLOSE_TABS` — closing browser tabs is not deletion of conversation history.

## 1. Recovery law

`CHAT != DURABLE_AUTHORITY`

`MEMORY != SOURCE_ARTIFACT`

`LIBRARY_FILE != GITHUB_AUTHORITY`

`DRIVE_EXISTENCE != CURRENT_AUTHORITY`

`CURRENT_POINTER + DURABLE_SOURCE + READBACK > CHAT_RECOLLECTION`

`KNOWN_CHAT_ONLY_ITEM -> DELETE_ALL_CHATS_BLOCKED`

A project may be marked `SAFE_FOR_WORK_AUTHORITY` only when its current material state has a durable recovery path. This does **not** mean every conversational sentence, discarded draft, or generated image has been archived.

## 2. Status vocabulary

- `DURABLE_VERIFIED` — current material authority and restart path are durably recoverable.
- `DURABLE_PARTIAL` — substantial durable state exists, but known recovery gaps remain.
- `LIBRARY_DURABLE` — material artifacts exist in ChatGPT Library; GitHub/Drive project authority is absent or not verified.
- `RECOVERY_REQUIRED` — known chat-only / not-recorded / missing-artifact gap blocks deletion safety.
- `DISCOVERY_ONLY` — useful finding, not authority.
- `UNKNOWN` — not enough evidence to classify higher.

Deletion safety:
- `SAFE_FOR_WORK_AUTHORITY` — material current work can be restored without the chat.
- `SAFE_AFTER_RECOVERY` — keep source chats until listed recovery gaps are closed.
- `NOT_SAFE_TO_DELETE_SOURCE_CHAT` — known chat-only evidence exists.
- `ARCHIVE_CHECK_REQUIRED` — binary/image completeness has not been proven.

## 3. Project recovery matrix

| ID | Project | Recovery status | GitHub authority | Drive authority | Library / other durable evidence | Latest state / handoff | Missing chat-only / recovery gaps | Chat deletion safety |
|---|---|---|---|---|---|---|---|---|
| BUS-01 | General Business Engineering OS | `DURABLE_VERIFIED` | `BUSINESS_ENGINEERING_OS/CURRENT_GENERAL_BUSINESS_ENGINE.md` + engine/state/PR evidence on `main` | Canonical General Business folder `16fvKMboBdMi5_wfv8KkR8njx-raNoZ-X`; recent Article 50 closure doc `1JtUjyAEoVRGiBtkkmgeYd75C7lImjpVieBTS52MqLJM` | extensive Library/Drive evidence | Early-Wave WIP lanes remain evidence-bounded; current control-plane lives in CURRENT file | no known material engineering result relies solely on chat in audited current layer | `SAFE_FOR_WORK_AUTHORITY` |
| BUS-02 | eTenders procurement `8872468` | `DURABLE_VERIFIED_WITH_EXTERNAL_BLOCKER` | Business procurement states, validator, receipts, P225/P235 gates under `BUSINESS_ENGINEERING_OS` | multiple P225/P288/unlock receipts; official document URL recorded | public first-party coordinates and internal receipts | exact documents endpoint known; target attachment pack still not acquired; bidder designation missing | authenticated attachment bytes/inventory are external missing evidence, not chat loss | `SAFE_FOR_WORK_AUTHORITY` |
| BOOK-B03 | SMITH / **THE EMPTY RESCUE** | `DURABLE_VERIFIED` | `PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json` plus B03 audio/speaker state and publishing paths | locked master exists; `76_B03 — THE EMPTY RESCUE — LOCKED MASTER — CH01-29 — 2026-08-22`, doc `141BOyku8VX8WXehH05rZnQGZirMOP-3iCs-5_yMJbGU`; additional locked master `1gs64S1WxaSPUiN-BXusmceM2E-EoquDntCasFaf8zas` | supporting speaker/audio artifacts exist | Founder-locked manuscript; active frontier is downstream audio/speaker attribution, not story redevelopment | keep any unexported generated audio/image binaries if they exist only in a chat; no known story-authority gap | `SAFE_FOR_WORK_AUTHORITY` |
| DORAMA-BB | **BLOODBOUND** | `DURABLE_VERIFIED_DRIVE` | no dedicated current GitHub path was located by code-search in this audit; this master index now supplies a GitHub recovery pointer | current authority doc `17dt299YyIeflzUkbfaDn3FbI9qUAoMEiHi3Otb4KSV8`; Founder Story Lock `1Fp0vPbvt8JaGxGIvfxwyN4LuA4BXo8Ia1Rcp2Qk8hDA`; final gate `1zaaP_q1WGJGoPJRZhsZ7nwqO3R-Q83Vqjw6uFacIr7s`; E24 `1zb0aMErYQcEPhcPC3xMit2vpQwWOmVP9qyERB92W9BI` | Library source inventory + execution logs | E01–E24 text complete; Founder story lock/recording authority exists in Drive | GitHub-native project CURRENT pointer should still be added later if desired; no known text-only loss | `SAFE_FOR_WORK_AUTHORITY` |
| DORAMA-WIFE | **THE WIFE AT HIS WEDDING** | `DURABLE_VERIFIED_DRIVE` | no dedicated current GitHub path was located by code-search in this audit; this master index supplies the GitHub recovery pointer | folder `1FjjH_8AAw6ZAHZR-8wuAfc4NEIJTdxMg`; Founder Story Lock `1eueZnnYaUGktaSXCcMIiOAUUcINmCTV6xATBdZ9B9UA`; final E1–E120 regression `1-kXiIx3utxWTmIlPUuudiWVsXLfCHbBTOAADrrLrGF8`; final story gate `1C-VzyTORtauuDFZToJ4bx5Nic9dOwsrPfRudL3dAOcM` | master prompts and production artifacts in Library | E1–E120 story gate + recording authority are durable | GitHub-native CURRENT pointer optional; verify any unexported audio binaries separately | `SAFE_FOR_WORK_AUTHORITY` |
| AUDIO-R917 | **ROOM 917** audio/post-render | `DURABLE_VERIFIED_DRIVE` | no dedicated path located by code-search in this audit; related Self-Improvement integration exists | current research pointer `1vK_dPQQSa_F-J-dPpZKDSLSzdysKTJQUQle8tRSNSDg`; post-render folder `1P2mavegKiziTOcdNoRQvHvgEHzySY3OA`; source/runbook `1P4Q4xHZfb5NSJgmnNx3NQZPv6c34FbRJHua2-N9ngxg` | Library contains semantic-divergence and post-render pipeline artifacts | E01 post-render engineering has durable runbook/toolkit; real rendered/provider evidence remains a separate execution plane | actual provider WAV/render binaries must be checked before deleting any chat that contains the only copy | `ARCHIVE_CHECK_REQUIRED` |
| AUDIO-D01 | D01 / project cast readiness | `DURABLE_VERIFIED_GITHUB` | merged D01 cast-readiness v1.1 work; universal audio runtime preserved in GitHub | Drive status not exhaustively re-audited here | repo/PR history durable | project-specific cast spec exists; real provider inventory / auditions / voice locks remain external evidence | no known chat-only code authority; possible media binaries still require export check | `SAFE_AFTER_RECOVERY` |
| SI-01 | IVDIVO Self-Improvement Engine | `DURABLE_VERIFIED` | `SELF_IMPROVEMENT_ENGINE/` with `RECOVERY_EVIDENCE`, `LIBRARY_CURRENT`, incidents, Cycle10/11 and live interception guards | CURRENT authority `1xare6Mz0FG6fDsY5QWx-hirI9D4A4BPtSG6vXY4sPa0`; current library index `1-2Qpt0TFq2dQiH7LzXJHD89SdCsVVbz3z9HbhwAWH_M`; production-launch folder `1KYheQh4SqDffsgAFuN47s_mwMB5rgY5f` | extensive Library/Drive receipts | evidence-first/fail-closed engine is restartable; newer improvements remain bounded by explicit proof gates | none known that changes current authority | `SAFE_FOR_WORK_AUTHORITY` |
| PAI-01 | Personal AI / Production Launch | `DURABLE_VERIFIED` | `SELF_IMPROVEMENT_ENGINE/PRODUCTION_LAUNCH_2026-08-22/CURRENT_PRODUCTION_LAUNCH_STATE.json` + `CURRENT_HANDOFF.md` | master launch doc `1WsinAXMIo9uGLLGSg8NnKRlEDnYLd1MPk6D-46QyXuA` plus stage receipts | code/tests/state in repo | PL-09 is verified; queue/handoff identifies the current runnable frontier; state must be read fresh on restart | local/provider credentials and local-only runtime data are not stored in GitHub/Drive by design | `SAFE_FOR_WORK_AUTHORITY` |
| GAME-PORTALS | **Portals: Ireland** | `DURABLE_PARTIAL` + `RECOVERY_REQUIRED` | no `PORTALY_IR` path located by GitHub code-search in this audit | exact current Portals: Ireland authority folder/doc not located; old `PORTALS_OF_STARS` docs exist but are not auto-promoted | Library idea register `PORTALS_IRELAND_IDEA_REGISTER_v0_1.csv` | base identity partly recoverable from Library, but several Founder decisions are explicitly chat-only/not-recorded | see `CHAT_ONLY_RECOVERY_LEDGER.md`: card-only base, 3-location Dublin route, SF cards, Place Verbs dictionary, Seals, Leprechaun role, 24 Portals + 40 Memory Places; 64-location architecture conflicted | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| ART-IRELAND | Ireland vintage cards / murals / Shillelagh-Wicklow visual system | `LIBRARY_DURABLE` + `DURABLE_PARTIAL` | no unified current GitHub visual authority verified | Drive contains design/business documents, but complete generated-image set was not exhaustively proven | Library contains actual PNGs: `Винтажные туристические постеры Дублина.png`, `Концепты фресок Шиллега и Уиклоу.png`, individual mural/card PNGs | style and representative outputs survive; complete card-by-card binary inventory not established | exact latest card dimensions, one-card-per-sheet production rule, Carna/Barna/Ballyvaghan sequence and every generated image need binary inventory/export verification | `ARCHIVE_CHECK_REQUIRED` |
| BUILD-FARADA | FARADA modular buildings / windows-doors procurement | `LIBRARY_DURABLE` | no dedicated current GitHub authority verified in this pass | Drive authority not exhaustively verified in this pass | Library spreadsheets `FARADA_G30_L45_Fabrication_RFQ_Package_v1.xlsx` and `FARADA_G30_L45_Preliminary_Engineering_BOM.xlsx` retain detailed RFQ/BOM/procurement data | preliminary engineering/RFQ package is durable; not final structural design | create dedicated CURRENT pointer before destructive chat cleanup if this becomes active production | `SAFE_AFTER_RECOVERY` |
| WEB-PAINTERS | painters-dublin.ie / service-business website | `RECOVERY_REQUIRED` | no current repo/site authority verified in this audit | no current Drive handoff verified in this audit | recoverable from prior project context, but not proven here as durable project state | WordPress/Elementor service-site project exists as an active business stream, but current implementation snapshot is not part of this audit evidence | export site/config/credentials separately; credentials must never be copied into GitHub/Recovery index | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| MATH-ORDERS | numerical orders / bases / synthesis-growth research | `LIBRARY_DURABLE` + `RECOVERY_REQUIRED` | no current GitHub authority located by key-term search | Drive has related IVDIVO Atlas/research material but not a verified current numerical-order authority | Library has Paradigma source texts, working reports and prior chat-writing blocks | research remains hypothesis-driven, not established mathematics | preserve methodological constraints and unfinished synthesis hypotheses in recovery ledger; exact lost derivations must not be reconstructed as fact | `NOT_SAFE_TO_DELETE_SOURCE_CHAT` |
| RESEARCH-IVDIVO | thin-body / 64-matter / synthetic-life / consciousness-transfer research | `LIBRARY_DURABLE` | no single current GitHub authority verified in this pass | Drive contains IVDIVO Atlas production protocol and related research assets | Library contains `Механика_тонких_тел_и_64_видов_материи_IVDIVO_v0_1` and source texts | substantial research corpus survives; many numerical/cosmological claims remain source-specific or experimental | distinguish sourced doctrine, authored hypothesis and fiction/worldbuilding on recovery | `SAFE_AFTER_RECOVERY` |
| WRITE-ENGINE | Book Intelligence / Writers’ Room / Dorama production engines | `DURABLE_VERIFIED` | repo contains Book Intelligence, Production Launch, writing/audio engines, CI/state and project-specific integrations | multiple production packs in Drive | Library holds reference corpus and prompts | engine-level authority is durable; individual project binaries can still have separate gaps | raw copyrighted books remain private; do not mirror them to public GitHub | `SAFE_FOR_WORK_AUTHORITY` |

## 4. High-risk chat-only recovery queue

The following classes block a blanket “delete every conversation” decision:

1. **Portals: Ireland:** explicit `CHAT_ONLY`, `CONFIRMED_NOT_RECORDED`, and `TO_RECOVER` records exist.
2. **Visual generation:** representative PNGs survive in Library, but the complete latest output inventory is not proven. A deleted chat may contain the only copy of a generated image/version.
3. **Numerical-order research:** core methodological rules and some newest hypotheses live partly in conversation context; the recovery ledger preserves them as hypotheses, not established results.
4. **Website / ad-hoc physical-business streams:** no unified current authority was verified for every stream.
5. **Provider media:** real WAV/render files must be checked independently; text receipts do not substitute for binary audio.

## 5. Projects already safe as operational authority

The audited current operational state is strongly recoverable for:
- General Business Engineering OS;
- eTenders 8872468 engineering state;
- B03 / THE EMPTY RESCUE manuscript authority;
- BLOODBOUND text/Founder-lock state via Drive;
- THE WIFE AT HIS WEDDING text/Founder-lock state via Drive;
- Self-Improvement Engine;
- Personal AI / Production Launch;
- core writing/Book-Intelligence engineering.

`SAFE_FOR_WORK_AUTHORITY` means the project can be resumed from durable sources. It does not certify archival completeness of every image, audio file, discarded draft, or conversational explanation.

## 6. Required closure before “delete all chats”

Global chat deletion can move from `BLOCKED` only when:

- [ ] every `CHAT_ONLY` / `CONFIRMED_NOT_RECORDED` Portals item is either persisted or explicitly abandoned;
- [ ] `Place Verbs` raw dictionary is recovered or formally declared irrecoverable;
- [ ] visual projects have a binary manifest proving every wanted final PNG exists outside chat;
- [ ] ROOM917/D01/B03 audio projects have a binary manifest for wanted WAV/render assets;
- [ ] numerical-order research has a current research note containing the latest hypotheses and explicit evidence ceiling;
- [ ] painters-dublin.ie has an export/current handoff if its chat history is needed for recovery;
- [ ] any other conversation containing a user-uploaded/generated artifact not present in Library/Drive is exported or explicitly abandoned;
- [ ] this index is re-run after those recoveries and the global deletion gate is changed by evidence, not assumption.

## 7. Restart protocol

On any new chat/session:

1. Read `RECOVERY/MASTER_RECOVERY_STATE.json`.
2. Read the relevant project CURRENT/state/handoff listed here.
3. Prefer current GitHub/Drive authority over chat recollection.
4. Treat Library-only artifacts as evidence/source material, not automatic current authority.
5. Load `RECOVERY/CHAT_ONLY_RECOVERY_LEDGER.md` before deleting or canonising recovered ideas.
6. Reconcile against fresh `main` and fresh Drive metadata.
7. Never promote a recovery description to canon merely because the original chat is unavailable.

## 8. Current global decision

**You may close browser tabs.**  
**Do not yet delete all conversations.**

The work is now much safer because this index creates a cross-project recovery map, but the known Portals/visual/research gaps must be closed before a blanket deletion claim is evidence-valid.

`MASTER_RECOVERY_MARKER: IVDIVO-MASTER-RECOVERY-20260822-V1-GLOBAL-DELETE-BLOCKED-KNOWN-GAPS-RECORDED`
