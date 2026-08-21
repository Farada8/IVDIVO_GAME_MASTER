# FRESH TECH RADAR — CYCLE 2 — 2026-08-21

**Status:** REFERENCE / PILOT CANDIDATES ONLY. No external product is promoted by documentation alone.

## OpenAI
- April 15, 2026 OpenAI described an updated Agents SDK with controlled sandbox execution, file/command/code work, long-horizon tasks and separation of agent harness from compute. Mechanism implication: code-first orchestration, bounded workspaces and replaceable execution backends.
- OpenAI AgentKit material updated June 3, 2026 says Agent Builder/Evals products are being wound down, with code workflows directed to Agents SDK. Decision implication: do not make IVDIVO dependent on a disappearing visual workflow product; keep Prompt IR/orchestration code-first and provider-neutral.
- Agent evaluation guidance reinforces that model, harness, tools, budget and validity all belong to the evaluated system. Decision implication: telemetry records the complete execution context rather than a naked score.

## Anthropic / Claude Code
- Current instruction surfaces include CLAUDE.md/rules/skills/subagents/hooks/output styles/system-prompt append with different loading, persistence and authority behavior.
- Lifecycle hooks such as PreToolUse/PostToolUse and subagent lifecycle events support a portable mechanism: important authority/freshness/mutation guards should live outside ordinary prompt prose when possible.

## ElevenLabs
- Current Text-to-Dialogue supports multiple voices but recommends bounded input sizes for reliable generation; several generations may be required. Decision implication: render-block compiler must be provider-capability-aware rather than assuming arbitrary context.
- Voice Design is useful exploration, not automatic recurring-role authority; consistent recurring-role binding still needs staged evidence and long-form proof.

## Durable workflow reference — Temporal
- Durable workflow replay plus retryable external Activities supports a portable architecture: deterministic workflow state + idempotent non-deterministic provider calls + replay/rollback.

## Pilot candidates
1. Code-first Prompt IR → backend task-packet compiler.
2. Lifecycle hooks for pre-tool freshness/authority checks and post-tool readback.
3. Capability-aware audio chunk/render planner.
4. Durable-execution canary: kill/restart orchestrator and prove completed external calls are not repeated.

## HOLD
No framework/provider migration until a bounded IVDIVO pilot demonstrates lower failure/rework or stronger evidence quality.