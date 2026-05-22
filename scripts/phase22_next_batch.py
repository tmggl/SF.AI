#!/usr/bin/env python3
"""SF.AI — read-only Phase 22 next-batch authoring brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.phase22_readiness import build_phase22_next_batch_brief  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Show the immediate Phase 22 authoring/review task."
    )
    parser.add_argument("--batch-size", type=int, default=25)
    args = parser.parse_args(argv)

    brief = build_phase22_next_batch_brief(batch_size=args.batch_size)
    print("SF.AI — Phase 22 next batch")
    print(f"  phase                         : {brief.phase}")
    print(f"  status                        : {brief.status}")
    if brief.next_batch is None:
        print("  next_batch                    : none")
    else:
        b = brief.next_batch
        print(f"  next_batch                    : {b.batch_id}")
        print(f"  dialect                       : {b.dialect}")
        print(f"  target_records                : {b.target_records}")
        print(f"  output                        : {b.suggested_output_path}")
    print(f"  why                           : {brief.why_this_batch}")
    print()
    print("acceptance checklist:")
    for item in brief.acceptance_checklist:
        print(f"  - {item}")
    print()
    print("suggested topics (not training data):")
    for topic in brief.suggested_topics:
        print(f"  - {topic}")
    print()
    print("ui instructions:")
    for item in brief.ui_instructions:
        print(f"  - {item}")
    print()
    print("after direct batch write:")
    for command in brief.after_export_commands:
        print(f"  - {command}")
    print()
    print("warnings:")
    for warning in brief.warnings:
        print(f"  - {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
