from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.bootstrap import bootstrap
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IVDIVO Personal AI Production System")
    parser.add_argument(
        "--home",
        default=os.environ.get("PERSONAL_AI_HOME"),
        help="Persistent home directory; defaults to the personal-ai directory.",
    )
    sub = parser.add_subparsers(dest="command")

    project = sub.add_parser("project", help="Project state operations")
    project_sub = project.add_subparsers(dest="project_command", required=True)

    create = project_sub.add_parser("create", help="Create a persisted project")
    create.add_argument("project_id")
    create.add_argument("--name")

    status = project_sub.add_parser("status", help="Read project state")
    status.add_argument("project_id")

    next_task = project_sub.add_parser("next", help="Return the next actionable task")
    next_task.add_argument("project_id")

    memory = sub.add_parser("memory", help="Auditable local memory operations")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    put = memory_sub.add_parser("put", help="Persist a memory record")
    put.add_argument("content")
    put.add_argument("--kind", default="NOTE")
    put.add_argument("--source")
    put.add_argument("--id", dest="record_id")
    put.add_argument("--metadata", default="{}", help="JSON object")
    put.add_argument("--project-id")
    put.add_argument("--source-id")
    put.add_argument("--confidence", type=float)

    search = memory_sub.add_parser("search", help="Search local memory")
    search.add_argument("query")
    search.add_argument("--kind")
    search.add_argument("--project-id")
    search.add_argument("--include-invalid", action="store_true")
    search.add_argument("--limit", type=int, default=20)

    update = memory_sub.add_parser("update", help="Create a new memory version")
    update.add_argument("record_id")
    update.add_argument("content")
    update.add_argument("--source")
    update.add_argument("--metadata", help="replacement JSON object")
    update.add_argument("--project-id")
    update.add_argument("--source-id")
    update.add_argument("--confidence", type=float)

    invalidate = memory_sub.add_parser("invalidate", help="Invalidate a memory record")
    invalidate.add_argument("record_id")
    invalidate.add_argument("--reason", required=True)

    trace = memory_sub.add_parser("trace", help="Show a memory record audit-event trail")
    trace.add_argument("record_id")

    versions = memory_sub.add_parser("versions", help="Show immutable memory versions")
    versions.add_argument("record_id")

    source_trace = memory_sub.add_parser(
        "source-trace", help="Trace a memory record through source_id provenance"
    )
    source_trace.add_argument("record_id")
    source_trace.add_argument("--max-depth", type=int, default=20)

    return parser


def _resolve_home(raw: str | None) -> Path:
    default_home = Path(__file__).resolve().parent
    return Path(raw).expanduser().resolve() if raw else default_home


def _json_object(raw: str) -> dict:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("metadata must decode to a JSON object")
    return value


def main() -> int:
    args = build_parser().parse_args()
    home = _resolve_home(args.home)

    if args.command is None:
        result = bootstrap(home)
    elif args.command == "project":
        manager = ProjectStateManager(home)
        if args.project_command == "create":
            result = manager.create_project(args.project_id, args.name)
        elif args.project_command == "status":
            result = manager.load_project(args.project_id)
        elif args.project_command == "next":
            result = {"project_id": args.project_id, "next_task": manager.get_next_task(args.project_id)}
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported project command")
    elif args.command == "memory":
        store = MemoryStore(home / "runtime" / "state.db")
        if args.memory_command == "put":
            result = store.store(
                args.content,
                kind=args.kind,
                source=args.source,
                metadata=_json_object(args.metadata),
                record_id=args.record_id,
                project_id=args.project_id,
                source_id=args.source_id,
                confidence=args.confidence,
            )
        elif args.memory_command == "search":
            result = {
                "query": args.query,
                "results": store.search(
                    args.query,
                    kind=args.kind,
                    project_id=args.project_id,
                    include_invalid=args.include_invalid,
                    limit=args.limit,
                ),
            }
        elif args.memory_command == "update":
            metadata = None if args.metadata is None else _json_object(args.metadata)
            result = store.update(
                args.record_id,
                content=args.content,
                source=args.source,
                metadata=metadata,
                project_id=args.project_id,
                source_id=args.source_id,
                confidence=args.confidence,
            )
        elif args.memory_command == "invalidate":
            result = store.invalidate(args.record_id, args.reason)
        elif args.memory_command == "trace":
            result = {"memory_id": args.record_id, "events": store.trace(args.record_id)}
        elif args.memory_command == "versions":
            result = {"memory_id": args.record_id, "versions": store.versions(args.record_id)}
        elif args.memory_command == "source-trace":
            result = store.trace_source(args.record_id, max_depth=args.max_depth)
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported memory command")
    else:  # pragma: no cover - argparse enforces choices
        raise RuntimeError("unsupported command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
