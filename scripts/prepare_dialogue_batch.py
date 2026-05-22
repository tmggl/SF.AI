#!/usr/bin/env python3
"""Prepare reviewed chat exports into governed training JSONL."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.dialogue_batch import prepare_dialogue_batch  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare reviewed SF.AI chat exports into training JSONL."
    )
    parser.add_argument("--input", required=True, help="Review JSONL exported from chat UI.")
    parser.add_argument(
        "--out",
        default="data/corpus/chat/jsonl/dialogue_batch_v1.jsonl",
        help="Training JSONL output path. Written only with --training-allowed.",
    )
    parser.add_argument(
        "--report",
        default="artifacts/reports/dialogue_batch_report.json",
        help="Report JSON path.",
    )
    parser.add_argument(
        "--source",
        default="sf-ai-user-reviewed-dialogue",
        help="Provenance source for prepared records.",
    )
    parser.add_argument(
        "--license",
        default="user-provided",
        help="License/provenance label for prepared records.",
    )
    parser.add_argument("--dialect", choices=["msa", "saudi"], default="saudi")
    parser.add_argument("--quality", choices=["gold", "silver", "bronze"], default="silver")
    parser.add_argument(
        "--training-allowed",
        action="store_true",
        help="Required to write training JSONL. Without it, only a report is written.",
    )
    parser.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include safety-flagged records. Default is to skip them.",
    )
    args = parser.parse_args(argv)

    report = prepare_dialogue_batch(
        input_path=args.input,
        output_path=args.out,
        report_path=args.report,
        source=args.source,
        license_name=args.license,
        dialect=args.dialect,
        quality=args.quality,
        training_allowed=args.training_allowed,
        include_sensitive=args.include_sensitive,
    )

    print("SF.AI — Phase 18 dialogue batch preparation")
    print(f"  input              : {report.input_path}")
    print(f"  output             : {report.output_path}")
    print(f"  report             : {args.report}")
    print(f"  total_records      : {report.total_records}")
    print(f"  written_records    : {report.written_records}")
    print(f"  skipped_records    : {report.skipped_records}")
    print(f"  training_allowed   : {str(report.training_allowed).lower()}")
    print(f"  quality            : {report.quality}")
    print(f"  dialect            : {report.dialect}")
    if report.skipped_reasons:
        print("  skipped_reasons:")
        for reason, count in sorted(report.skipped_reasons.items()):
            print(f"    - {reason}: {count}")
    if not args.training_allowed:
        print()
        print("note: no training JSONL was written; pass --training-allowed after review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
