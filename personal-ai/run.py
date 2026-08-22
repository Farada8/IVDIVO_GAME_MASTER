from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.bootstrap import bootstrap


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IVDIVO Personal AI Production bootstrap")
    parser.add_argument(
        "--home",
        default=os.environ.get("PERSONAL_AI_HOME"),
        help="Persistent home directory; defaults to the personal-ai directory.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    default_home = Path(__file__).resolve().parent
    home = Path(args.home).expanduser().resolve() if args.home else default_home
    result = bootstrap(home)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
