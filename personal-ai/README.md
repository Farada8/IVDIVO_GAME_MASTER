# IVDIVO Personal AI Production System — PL-00

Minimal laptop-first executable bootstrap for the production-launch backlog.

## Run

```bash
python personal-ai/run.py
```

For an isolated persistent home:

```bash
python personal-ai/run.py --home /path/to/home
```

The command initializes SQLite, creates one deterministic demo project and task, reads both back, writes `logs/bootstrap.log`, and prints the persisted snapshot as JSON.

## Test

```bash
python -m unittest discover -s personal-ai/tests -v
```

PL-00 deliberately uses only the Python standard library. Provider APIs, project CLI, long-term memory semantics, agents, business and book workflows are later production-launch cards and are not claimed complete here.
