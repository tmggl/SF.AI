#!/usr/bin/env python3
"""SF.AI — read-only Phase 22 review-export intake scanner."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.phase22_review_intake import build_phase22_review_intake_report  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Scan reviewed chat exports before any corpus conversion."
    )
    parser.add_argument(
        "--review-dir",
        default="data/corpus/chat/review",
        help="Directory containing review JSONL exports.",
    )
    parser.add_argument("--max-files", type=int, default=None)
    args = parser.parse_args(argv)

    report = build_phase22_review_intake_report(
        review_dir=args.review_dir,
        max_files=args.max_files,
    )

    print("SF.AI — Phase 22 review intake")
    print(f"  phase                         : {report.phase}")
    print(f"  status                        : {report.status}")
    print(f"  review_path                   : {report.review_path}")
    print(f"  review_files                  : {report.review_files}")
    print(f"  candidate_files               : {report.candidate_files}")
    print(f"  total_review_records          : {report.total_review_records}")
    print(f"  total_valid_json_records      : {report.total_valid_json_records}")
    print(f"  total_schema_valid_records    : {report.total_schema_valid_records}")
    print(f"  user_assistant_records        : {report.total_user_assistant_records}")
    print(f"  raw_generator_records         : {report.total_raw_generator_assistant_records}")
    print(f"  safety_flagged_estimate       : {report.total_safety_flagged_estimate}")
    print(f"  average_quality_score         : {report.average_dialogue_quality_score}")
    print(f"  synthetic_llm_data_allowed    : {str(report.synthetic_llm_data_allowed).lower()}")
    print()
    print("review files:")
    if not report.files:
        print("  - none")
    for item in report.files:
        print(f"  - {item.path}")
        print(f"      status                    : {item.status}")
        print(f"      records                   : {item.records}")
        print(f"      valid_json_records        : {item.valid_json_records}")
        print(f"      schema_valid_records      : {item.schema_valid_records}")
        print(f"      user_assistant_records    : {item.records_with_user_and_assistant}")
        print(f"      training_allowed_false    : {item.training_allowed_false}")
        print(f"      training_allowed_true     : {item.training_allowed_true}")
        print(f"      raw_generator_records     : {item.raw_generator_assistant_records}")
        print(f"      user_turns                : {item.user_turns}")
        print(f"      assistant_turns           : {item.assistant_turns}")
        print(f"      quality_score             : {item.dialogue_quality_score}")
        print(f"      quality_label             : {item.dialogue_quality_label}")
        if item.dialogue_quality_blockers:
            print("      quality_blockers:")
            for blocker in item.dialogue_quality_blockers:
                print(f"        - {blocker}")
        print(f"      suggested_msa_command     : {item.suggested_msa_command}")
        print(f"      suggested_saudi_command   : {item.suggested_saudi_command}")
    print()
    print("recommended next commands:")
    for command in report.recommended_next_commands:
        print(f"  - {command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
