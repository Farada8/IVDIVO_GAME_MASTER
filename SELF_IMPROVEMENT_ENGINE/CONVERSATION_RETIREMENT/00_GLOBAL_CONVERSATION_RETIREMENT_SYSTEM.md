# GLOBAL CONVERSATION RETIREMENT SYSTEM v0.1

Status: CANDIDATE OPERATIONAL CONTROL / NOT GLOBAL CHAT ENUMERATOR
Date: 2026-08-22
Parent: Self-Improvement Meta Engine v2 VERIFIED_CURRENT
Founder directive: all important work should be durably persisted in GitHub + Google Drive so old ChatGPT conversations can eventually become disposable archives rather than working memory.

## Purpose
Provide a fail-closed retirement gate for AI conversations. A conversation is safe to delete only after all material work available from that conversation has been reconciled with persistent project stores.

## Core law
`CHAT_EXISTS != WORK_PERSISTED`
`ASSISTANT_SAID_SAVED != VERIFIED_PERSISTED`
`TAB_CLOSED != CHAT_DELETED`
`PERSISTENCE_COMPLETE != GLOBAL_HISTORY_COMPLETE`
`SAFE_TO_DELETE requires verified retirement evidence for that conversation/recovery corpus.`

## Required workflow
`INGEST AVAILABLE CONVERSATION/TRANSCRIPT -> CLASSIFY PROJECTS -> EXTRACT FOUNDER DIRECTIVES + MATERIAL OUTPUTS + ARTIFACT CLAIMS + OPEN GATES -> VERIFY GITHUB/DRIVE -> RECOVER CHAT_ONLY_CANDIDATES -> DEDUPE/FRESHNESS -> PERSIST CORRECT ARTIFACTS -> UPDATE CURRENT/STATE/HANDOFF -> READBACK -> RETIREMENT DECISION`.

## Retirement states
- `UNASSESSED`: no recovery proof.
- `IN_PROGRESS`: recovery/persistence audit active.
- `PERSISTENCE_INCOMPLETE`: material unresolved/chat-only/expired source remains.
- `PERSISTENCE_COMPLETE`: all supplied/available material has disposition and persistent readback.
- `SAFE_TO_DELETE`: PERSISTENCE_COMPLETE plus no unresolved material dependency on the chat itself.
- `DO_NOT_DELETE`: unresolved material or inaccessible source exists.

## Mandatory per-conversation fields
- conversation_key or recovery_id (never invent an unavailable ChatGPT internal id)
- project(s)
- source completeness: FULL / PARTIAL / UNKNOWN
- founder directives disposition
- artifact claims verified
- chat-only material disposition
- expired/unavailable upload list
- GitHub writes/readback
- Drive writes/readback
- current frontier / next gate
- unresolved items
- persistence_complete boolean
- safe_to_delete boolean
- evidence timestamp

## Fail-closed rules
1. Never mark `SAFE_TO_DELETE=true` because a project has CURRENT files elsewhere.
2. Never infer that all user conversations are covered unless each relevant conversation/recovery corpus has been enumerated or supplied and audited.
3. If a previous upload has expired and no durable copy is verified, record `DO_NOT_DELETE`/`PERSISTENCE_INCOMPLETE` for that source.
4. A copied/exported transcript may close a conversation remotely: once that supplied corpus reaches the Full Chat Recovery completion gate and persistent readbacks pass, the original chat no longer needs to remain working memory.
5. GitHub stores canonical engineering/state/provenance; Google Drive stores human-readable mirrors, manuscripts/media/private source material as appropriate.
6. Do not copy secrets/credentials into persistent artifacts.

## Standard Founder command
`ЗАКРОЙ ЭТОТ РАЗГОВОР НА ХРАНЕНИЕ`

Semantics: process the entire available conversation/recovery corpus, persist all material work to the correct GitHub/Drive project surfaces, read back, then return exactly one retirement result: `PERSISTENCE_COMPLETE / SAFE_TO_DELETE` or `PERSISTENCE_INCOMPLETE / DO_NOT_DELETE` with blockers.

## Global limitation
The assistant does not have a guaranteed API that enumerates and reads every historical ChatGPT conversation from one current chat. Therefore this system tracks what has actually been supplied/audited. A single command cannot truthfully certify all historical chats unless those chats/transcripts become accessible to the recovery process.

## Integration
- Full transcript recovery: `IVDIVO_NARRATIVE_OS/18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md`
- Session interruption recovery: `CURRENT_IVDIVO_SELF_IMPROVEMENT_RECOVERY_STATE.json`
- Topic continuity guard: `SELF_IMPROVEMENT_ENGINE/TOPIC_CONTINUITY/01_MACHINE_STATE.json`

## Promotion boundary
This control is persisted as a candidate operational mechanism. It does not promote Self-Improvement v3 or invent global coverage. Promotion requires real retirement audits with zero lost material and at least one successful reopen/restore from GitHub+Drive without relying on the retired chat.

READBACK_MARKER: GLOBAL-CONVERSATION-RETIREMENT-SYSTEM-CANDIDATE-20260822
