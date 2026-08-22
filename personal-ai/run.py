from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.bootstrap import bootstrap
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
    else:  # pragma: no cover - argparse enforces choices
        raise RuntimeError("unsupported command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
