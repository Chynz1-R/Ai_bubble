from __future__ import annotations

import argparse
import sys

from .engine import AURELIAEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aurelia",
        description="Generate a structured, safety-first analysis for a problem statement.",
    )
    parser.add_argument("problem", nargs="+", help="Problem statement to analyze")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    problem = " ".join(args.problem)
    analysis = AURELIAEngine().analyze(problem)
    print(analysis.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
