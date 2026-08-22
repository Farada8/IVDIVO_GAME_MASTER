# PL-05 Agent Executor

This layer is a bounded execution runtime, not an autonomous self-modifying agent system.

## Registered strict contract

The canonical PL-05 acceptance path is `BoundedAgentExecutor.execute()` with an `AgentDefinition` containing exactly:

- `ROLE`
- `GOAL`
- `INPUT`
- `TOOLS`
- `MEMORY`
- `MAX_STEPS`
- `OUTPUT_SCHEMA`

Strict execution is iterative and finite:

`LOAD TASK -> LOAD CONTEXT -> PROPOSE ACTION -> CALL TOOL -> OBSERVE -> UPDATE STATE -> STOP`.

Controls:
- hard `MAX_STEPS` bound (1..20);
- monotonic timeout;
- explicit named tool registry plus per-agent allowlist;
- unknown/non-allowlisted tools fail closed before execution;
- tool results must be JSON-serializable observations;
- output schema validation before OUTPUT persistence;
- project/task state updates and project-local JSONL action log;
- failure state and EVENT memory are persisted;
- network-backed providers still require explicit authorization.

The core allowlisted tool registry contains only bounded local helpers (`memory_search`, `echo`). It does not expose shell/code execution, recursive agent creation or destructive filesystem operations.

## Compatibility mode

`BoundedAgentExecutor.run(AgentRunRequest(...))` is retained for the baseline CLI and provider-only workflows. It uses the bounded `CONTINUE:` protocol, now also with a timeout guard. It is **not** the complete tool/observation contract used to prove strict PL-05 acceptance.

CLI compatibility path:

```bash
python personal-ai/run.py --home /tmp/pai project create demo
python personal-ai/run.py --home /tmp/pai agent run demo "hello" --provider mock --max-steps 2
```

## Evidence boundary

Acceptance requires deterministic offline tests proving bounded completion, state persistence after reopen, memory persistence, action logs, tool allowlisting, tool observation, output schema validation, timeout and max-step stop behavior. Live provider calls are not required for PL-05 acceptance and are not performed by CI.
