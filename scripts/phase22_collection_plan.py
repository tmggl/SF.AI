#!/usr/bin/env python3
"""SF.AI — read-only Phase 22 corpus collection plan."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.phase22_readiness import build_phase22_collection_plan  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build a read-only Phase 22 collection plan.")
    parser.add_argument("--batch-size", type=int, default=25)
    args = parser.parse_args(argv)

    plan = build_phase22_collection_plan(batch_size=args.batch_size)
    print("SF.AI — Phase 22 collection plan")
    print(f"  phase                         : {plan.phase}")
    print(f"  status                        : {plan.status}")
    print(f"  corpus_path                   : {plan.corpus_path}")
    print(f"  current_records               : {plan.current_records}")
    print(f"  target_records                : {plan.target_records}")
    print(f"  remaining_records             : {plan.remaining_records}")
    print(f"  batch_size                    : {plan.batch_size}")
    print(f"  estimated_batches             : {plan.estimated_batches}")
    print(f"  quota_by_dialect              : {plan.quota_by_dialect}")
    print(f"  flexible_records              : {plan.flexible_records_after_minimums}")
    print(f"  synthetic_llm_data_allowed    : {str(plan.synthetic_llm_data_allowed).lower()}")
    print()
    print("recommended batch mix:")
    for item in plan.recommended_batch_mix:
        print(f"  - {item}")
    print()
    print("review rules:")
    for rule in plan.review_rules:
        print(f"  - {rule}")
    print()
    print("next commands:")
    for command in plan.next_commands:
        print(f"  - {command}")
    print()
    print("planned batches:")
    for batch in plan.planned_batches:
        print(
            "  - "
            f"#{batch.sequence:02d} {batch.batch_id} "
            f"({batch.dialect}, {batch.target_records} records, {batch.priority})"
        )
        print(f"    out: {batch.suggested_output_path}")
        print(f"    task: {batch.user_task}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
