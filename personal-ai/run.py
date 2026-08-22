from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.bootstrap import bootstrap
from memory.store import LocalMemory, MEMORY_TABLES
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

    memory = sub.add_parser("memory", help="Versioned local memory operations")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)

    memory_store = memory_sub.add_parser("store", help="Store a new memory record")
    memory_store.add_argument("entity", choices=MEMORY_TABLES)
    memory_store.add_argument("record_id")
    memory_store.add_argument("content")
    memory_store.add_argument("--project-id")
    memory_store.add_argument("--source", default="user")
    memory_store.add_argument("--source-id")
    memory_store.add_argument("--confidence", type=float)
    memory_store.add_argument("--status", default="ACTIVE")

    memory_search = memory_sub.add_parser("search", help="Search current memory records")
    memory_search.add_argument("query")
    memory_search.add_argument("--entity", choices=MEMORY_TABLES)
    memory_search.add_argument("--project-id")
    memory_search.add_argument("--include-invalid", action="store_true")
    memory_search.add_argument("--limit", type=int, default=50)

    memory_update = memory_sub.add_parser("update", help="Create a new record version")
    memory_update.add_argument("entity", choices=MEMORY_TABLES)
    memory_update.add_argument("record_id")
    memory_update.add_argument("--content")
    memory_update.add_argument("--project-id")
    memory_update.add_argument("--source")
    memory_update.add_argument("--source-id")
    memory_update.add_argument("--confidence", type=float)
    memory_update.add_argument("--status")

    memory_invalidate = memory_sub.add_parser(
        "invalidate", help="Invalidate a record by creating an audit version"
    )
    memory_invalidate.add_argument("entity", choices=MEMORY_TABLES)
    memory_invalidate.add_argument("record_id")
    memory_invalidate.add_argument("--reason", default="invalidated")

    memory_trace = memory_sub.add_parser("trace", help="Trace a record to source records")
    memory_trace.add_argument("entity", choices=MEMORY_TABLES)
    memory_trace.add_argument("record_id")

    memory_versions = memory_sub.add_parser("versions", help="Read all preserved versions")
    memory_versions.add_argument("entity", choices=MEMORY_TABLES)
    memory_versions.add_argument("record_id")

    return parser


def _resolve_home(raw: str | None) -> Path:
    default_home = Path(__file__).resolve().parent
    return Path(raw).expanduser().resolve() if raw else default_home


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
        memory_store = LocalMemory(home / "runtime" / "state.db")
        memory_store.initialize()
        if args.memory_command == "store":
            result = memory_store.store(
                args.entity,
                args.record_id,
                args.content,
                project_id=args.project_id,
                source=args.source,
                source_id=args.source_id,
                confidence=args.confidence,
                status=args.status,
            )
        elif args.memory_command == "search":
            result = {
                "query": args.query,
                "results": memory_store.search(
                    args.query,
                    entity=args.entity,
                    project_id=args.project_id,
                    include_invalid=args.include_invalid,
                    limit=args.limit,
                ),
            }
        elif args.memory_command == "update":
            result = memory_store.update(
                args.entity,
                args.record_id,
                content=args.content,
                project_id=args.project_id,
                source=args.source,
                source_id=args.source_id,
                confidence=args.confidence,
                status=args.status,
            )
        elif args.memory_command == "invalidate":
            result = memory_store.invalidate(
                args.entity, args.record_id, reason=args.reason
            )
        elif args.memory_command == "trace":
            result = memory_store.trace_source(args.entity, args.record_id)
        elif args.memory_command == "versions":
            result = {
                "entity": args.entity,
                "record_id": args.record_id,
                "versions": memory_store.get_versions(args.entity, args.record_id),
            }
        else:  # pragma: no cover - argparse enforces choices
            raise RuntimeError("unsupported memory command")
    else:  # pragma: no cover - argparse enforces choices
        raise RuntimeError("unsupported command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
