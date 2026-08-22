from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from review import MultiModelReviewService


def _home(raw: str | None) -> Path:
    default = Path(__file__).resolve().parent
    return Path(raw).expanduser().resolve() if raw else default


def _request(path: str) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("review request JSON must contain an object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PL-10 isolated multi-model review lifecycle")
    parser.add_argument("--home", default=os.environ.get("PERSONAL_AI_HOME"))
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Freeze review input and critic definitions")
    start.add_argument("project_id")
    start.add_argument("request_json")

    critic = sub.add_parser("critic", help="Run exactly one isolated critic")
    critic.add_argument("project_id")
    critic.add_argument("review_id")
    critic.add_argument("critic_id")
    critic.add_argument("--allow-network", action="store_true")

    aggregate = sub.add_parser("aggregate", help="Aggregate only after all critics are terminal")
    aggregate.add_argument("project_id")
    aggregate.add_argument("review_id")

    status = sub.add_parser("status", help="Read persisted review state")
    status.add_argument("project_id")
    status.add_argument("review_id")

    run = sub.add_parser("run", help="Start, run all critics, then aggregate")
    run.add_argument("project_id")
    run.add_argument("request_json")
    run.add_argument("--allow-network", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    service = MultiModelReviewService(_home(args.home))
    if args.command == "start":
        result = service.start(args.project_id, _request(args.request_json))
    elif args.command == "critic":
        result = service.run_critic(
            args.project_id,
            args.review_id,
            args.critic_id,
            allow_network=args.allow_network,
        )
    elif args.command == "aggregate":
        result = service.aggregate(args.project_id, args.review_id)
    elif args.command == "status":
        result = service.load(args.project_id, args.review_id)
    elif args.command == "run":
        result = service.run_all(
            args.project_id,
            _request(args.request_json),
            allow_network=args.allow_network,
        )
    else:  # pragma: no cover
        raise RuntimeError("unsupported review command")
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
