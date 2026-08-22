from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from knowledge import PersonalKnowledgeSearch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PL-14 project-local source-separated personal knowledge search"
    )
    parser.add_argument(
        "--home",
        default=os.environ.get("PERSONAL_AI_HOME"),
        help="Persistent Personal AI home directory; defaults to the personal-ai directory.",
    )
    parser.add_argument("project_id")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=50)
    return parser


def _resolve_home(raw: str | None) -> Path:
    default_home = Path(__file__).resolve().parent
    return Path(raw).expanduser().resolve() if raw else default_home


def main() -> int:
    args = build_parser().parse_args()
    result = PersonalKnowledgeSearch(_resolve_home(args.home)).ask(
        args.project_id,
        args.query,
        limit=args.limit,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
