#!/usr/bin/env python3
"""SF.AI — Phase 12 preflight audit for tokenizer training corpus."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training  # noqa: E402


def _print_counts(title: str, counts: dict[str, int]) -> None:
    print(f"{title}:")
    if not counts:
        print("  - none")
        return
    for key, count in sorted(counts.items()):
        print(f"  - {key}: {count}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Audit Saudi/MSA JSONL corpus before Phase 12 tokenizer training"
    )
    parser.add_argument(
        "--corpus",
        default="data/corpus/chat/jsonl",
        help="Directory containing JSONL dialogue files",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=20,
        help="Maximum number of issues to print",
    )
    args = parser.parse_args(argv)

    report = audit_jsonl_directory_for_training(args.corpus)

    print("SF.AI — Phase 12 corpus preflight")
    print(f"  corpus          : {args.corpus}")
    print(f"  total_records   : {report.total_records}")
    print(f"  training_ready  : {report.training_ready}")
    print(f"  issues          : {report.error_count}")
    print()
    _print_counts("dialects", report.dialect_counts)
    _print_counts("quality", report.quality_counts)
    _print_counts("sources", report.source_counts)

    if report.issues:
        print()
        print("issues:")
        for issue in report.issues[: args.max_issues]:
            print(f"  - {issue.describe()}")
        remaining = report.error_count - args.max_issues
        if remaining > 0:
            print(f"  - ... {remaining} more")

    print()
    if report.error_count == 0 and report.training_ready > 0:
        print("status: READY_FOR_PHASE_12_TOKENIZER_TRAINING")
        print("next: run `make train-bpe ARGS=\"--corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1\"`")
        return 0

    print("status: NOT_READY_FOR_TRAINING")
    print("next: add approved Saudi/MSA JSONL dialogue data, then run this audit again")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
