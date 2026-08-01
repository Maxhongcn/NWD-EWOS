from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from capsule_builder.builder import build_capsule
from capsule_builder.verifier import verify_capsule


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m capsule_builder")
    subcommands = parser.add_subparsers(dest="command", required=True)

    build = subcommands.add_parser("build", help="Build a StanAI capsule")
    build.add_argument("--source", required=True, type=Path)
    build.add_argument("--output", required=True, type=Path)
    build.add_argument("--allow-unencrypted-demo", action="store_true")

    verify = subcommands.add_parser("verify", help="Verify a StanAI capsule")
    verify.add_argument("--capsule", required=True, type=Path)

    args = parser.parse_args()

    try:
        if args.command == "build":
            result = build_capsule(args.source, args.output, args.allow_unencrypted_demo)
        else:
            result = verify_capsule(args.capsule)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2, sort_keys=True), file=sys.stderr)
        raise SystemExit(1) from None

    print(json.dumps(result, indent=2, sort_keys=True))
