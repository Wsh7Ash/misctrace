"""
cli.py — command-line entry point for misctrace.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from report import format_trace
from trace import build_trace


def main(argv=None):
    ap = argparse.ArgumentParser(prog="misctrace", description="Trace a symbol across repositories")
    ap.add_argument("start", help="Start symbol")
    ap.add_argument("target", help="Target symbol")
    ap.add_argument("repos", nargs="+", help="Repository roots to search")
    args = ap.parse_args(argv)

    repo_paths = [Path(r).resolve() for r in args.repos]
    for p in repo_paths:
        if not p.is_dir():
            print(f"Not a directory: {p}", file=sys.stderr)
            return 2

    trace = build_trace(args.start, args.target, repo_paths)
    print(format_trace(trace))
    return 0 if trace.resolved else 1


if __name__ == "__main__":
    raise SystemExit(main())
