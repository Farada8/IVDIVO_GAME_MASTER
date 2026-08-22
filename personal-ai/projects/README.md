# Project State System — PL-01

Each local project is stored under the configured Personal AI home:

```text
projects/<project-id>/
├── project.yaml
├── state.json
├── tasks.json
├── decisions.md
├── artifacts/
├── references/
└── logs/
```

`ProjectStateManager` implements create/load/state update/task add/task complete/task block/decision record/next-task operations. JSON writes use a temporary file and replace step to avoid partial state files.

CLI:

```bash
python personal-ai/run.py project create demo
python personal-ai/run.py project status demo
python personal-ai/run.py project next demo
```

Project IDs reject traversal/path separators. PL-01 does not claim PL-02 long-term memory semantics or PL-05 agent execution.
