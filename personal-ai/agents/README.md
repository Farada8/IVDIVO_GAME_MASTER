# PL-05 Agent Executor

This layer is a bounded execution runtime, not an autonomous self-modifying agent system.

## Contract

Input: `AgentRunRequest(project_id, prompt, provider, model, max_steps, allow_network, task_id)`.

Execution:
1. project must already exist;
2. selected provider must exist;
3. network-backed providers require explicit `allow_network=True` / CLI `--allow-network`;
4. executor creates a READY task and moves it to RUNNING;
5. each provider response is logged as one step;
6. only a response beginning with `CONTINUE:` requests another bounded step;
7. any other response is final;
8. final text is persisted as PL-02 `OUTPUT` memory, then the task becomes DONE;
9. provider/runtime failures or exhausted `max_steps` mark the task FAILED;
10. every run has a project-local JSONL audit log.

`max_steps` is constrained to 1..20. There is no unbounded loop, hidden recursion, tool execution, background work or automatic network permission.

## Offline acceptance path

```bash
python personal-ai/run.py --home /tmp/pai project create demo
python personal-ai/run.py --home /tmp/pai agent run demo "hello" --provider mock --max-steps 2
```

Acceptance requires persisted project task state, persisted OUTPUT memory, a JSONL run log and deterministic mock execution. Live provider calls are not required for PL-05 acceptance and are not performed by CI.
