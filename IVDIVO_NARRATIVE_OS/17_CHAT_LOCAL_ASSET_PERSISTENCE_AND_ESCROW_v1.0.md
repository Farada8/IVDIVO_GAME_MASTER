# IVDIVO — CHAT-LOCAL ASSET PERSISTENCE & ESCROW LAW v1.0

**Status:** CANONICAL OPERATIONAL PERSISTENCE STANDARD  
**Established:** 2026-08-21  
**Scope:** all IVDIVO chats/models/tools that create, receive, render, upload, transform or depend on binary/large production assets.

## 1. Defect this standard closes

A production result is not safely handed off merely because one conversation can see it.

`CHAT-LOCAL ONLY` is a volatile transport state, not durable project memory.

A critical WAV, stem, MP3, ZIP, image, video, PDF, DOCX, JSON bundle, render log, alignment file, model output package or other dependency must not remain accessible only inside one model conversation if later work depends on its bytes.

The ROOM917 case `ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav` exposed this failure class: filename/hash/metrics were persisted, but the actual WAV bytes remained in another ChatGPT conversation and were not available from shared Drive/File Library during continuation. That is an operational persistence defect, not evidence that the asset never existed.

## 2. Primary law

For every future-critical asset:

`CREATE/RECEIVE -> HASH/IDENTIFY -> PERSIST BYTES TO SHARED DURABLE STORAGE -> REGISTER POINTER + PROVENANCE -> READBACK/ACCESS VERIFY -> ONLY THEN ADVANCE FRONTIER`.

A chat-visible attachment is not equivalent to persistence.

Do not close a production work block with a critical asset in `CHAT_LOCAL_ONLY` state when a supported durable write path is available.

## 3. Required asset state

Every material binary/large artifact should resolve these fields where applicable:

- `asset_id`
- `project_id`
- `filename`
- `asset_class`
- `status`
- `source_conversation_or_provider`
- `created_or_received_at`
- `sha256` where tooling permits
- `size_bytes`
- `format/container/codec`
- `sample_rate/bit_depth/channels/duration` for audio when relevant
- `parent_artifact_ids[]`
- `derived_children[]`
- `source_text_or_prompt_version`
- `build_id`
- `durable_storage_type`
- `durable_storage_id_or_url`
- `access_verified_at`
- `ingest_register_id`
- `current_consumer_stage`
- `blocked_if_bytes_missing`

## 4. Status vocabulary

Allowed operational states:

- `CHAT_LOCAL_ONLY` — bytes exist only in one conversation/session; NOT durable.
- `PERSISTENCE_PENDING` — durable write is required and currently executable/in progress.
- `QUARANTINE_BAD_METADATA` — bytes persisted but provenance/identity incomplete.
- `DURABLE_WORKING` — bytes persisted and access verified; not approved/locked.
- `APPROVED_REFERENCE` — passed applicable gates; immutable reference.
- `SUPERSEDED` / `REJECTED` — retained for audit/regression.
- `UNRECOVERABLE_CHAT_ONLY` — actual bytes cannot currently be retrieved from source conversation/tool; record exact known provenance and stop any downstream action requiring those bytes.

`CHAT_LOCAL_ONLY` and `PERSISTENCE_PENDING` may never be treated as completed handoff states.

## 5. Automatic escrow behavior

When a critical asset appears in an executing session and a durable connector/write path is available:

1. preserve the original bytes without destructive transformation;
2. compute/recover identity metadata and checksum where possible;
3. write the original to the active project's shared ingest/asset store;
4. write derivatives separately, never over the raw source;
5. register the asset in the project ingest/version-control register;
6. update project execution state with the durable pointer;
7. read back metadata/accessibility;
8. only then mark persistence PASS and continue.

For ROOM917 audio, preferred durable intake is the existing controlled Drive ingest tree (`06_INCOMING_AUDIO_INGEST` and its appropriate raw/working/reference subfolders) unless current project authority names a newer location.

## 6. Tool-boundary law

If the current model can see an attachment but no available connector/tool can transfer its bytes to shared durable storage:

- do not pretend persistence occurred;
- preserve exact filename/hash/size/provenance metadata;
- mark `PERSISTENCE_BLOCKER` / `CHAT_LOCAL_ONLY`;
- complete all work that does not require asset bytes;
- stop only when the next dependent stage actually requires those bytes;
- next session must first attempt source-conversation retrieval or supported durable transfer before asking Founder to repeat/re-upload.

If source-conversation retrieval is impossible with available tools, state that exact tool boundary. Do not reconstruct binary assets from summaries, metrics or memory.

## 7. Cross-conversation boot requirement

Before declaring `MISSING ASSET`, perform:

`PROJECT STATE -> INGEST REGISTER -> SHARED DRIVE/FOLDER -> FILE LIBRARY WHERE AVAILABLE -> CURRENT CROSS-AI HANDOFF -> SOURCE CONVERSATION/PROJECT CONTEXT DISCOVERY -> EXACT FILENAME/HASH SEARCH`.

Distinguish:

- `ASSET NEVER CREATED`
- `ASSET CREATED BUT NOT PERSISTED`
- `ASSET PERSISTED BUT POINTER STALE`
- `ASSET BYTES CURRENTLY INACCESSIBLE`
- `ASSET IDENTITY CONFLICT`

These are different failure classes and require different repair.

## 8. Handoff completeness gate

A material stage that creates/receives a critical asset is not handoff-complete until:

`BYTES DURABLE + POINTER REGISTERED + PROVENANCE RECORDED + READBACK ACCESS VERIFIED`.

If any is false, set an open gate such as:

`ASSET_PERSISTENCE_REQUIRED:<asset_id>`

and do not advertise the downstream consumer stage as fully unblocked.

## 9. Multi-AI law

Another AI/model receives asset pointers, hashes and exact current status, not claims such as “the other chat has the file.”

If the model cannot access the durable pointer, its state is `ACCESS_BLOCKED`, not `MISSING` and not permission to regenerate the asset.

No AI may silently regenerate or replace a missing critical source asset merely to make the pipeline continue.

## 10. Security / secret law

Persist production assets only to Founder-authorized project storage. Never place API keys, passwords, auth tokens or other secrets inside asset manifests, filenames, GitHub commits or shared prompts.

Provider credentials remain local/secret even when provider outputs are persisted.

## 11. Audio-specific acceptance

For production audio, persistence should preserve when available:

- original render/master bytes;
- dry dialogue / edited dialogue;
- SFX/Foley/ambience/music stems;
- alignment/timestamp sidecars;
- render/provider logs without secrets;
- mix/master QC;
- exact build/source/voice/asset provenance.

A final/full-mix WAV alone is enough to perform perceptual master review, but not enough to enable selective repair if the required source stems/takes cannot be recovered. Persist the repairable production graph where economically practical.

## 12. Founder experience law

The Founder should not be used as manual cloud storage or cross-chat courier.

If the studio can persist a future-critical asset itself, it must do so during the producing work block.

If it cannot, the state must expose that limitation immediately rather than discovering it many turns later.

**A PRODUCTION RESULT THAT ONLY ONE CHAT CAN SEE IS NOT A FINISHED HANDOFF.**
