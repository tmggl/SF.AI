#!/usr/bin/env python3
"""Run Phase 27 dialogue evaluation v2 and write reports."""

from __future__ import annotations

import argparse

from sf_ai.evaluation import write_phase27_dialogue_eval_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run SF.AI Phase 27 dialogue evaluation v2."
    )
    parser.add_argument(
        "--suite",
        default="eval/prompts/dialogue_v2.json",
        help="Multi-turn dialogue suite JSON.",
    )
    parser.add_argument(
        "--out",
        default="eval/reports/dialogue_eval_v2.json",
        help="Output eval report JSON.",
    )
    parser.add_argument(
        "--artifact-out",
        default="artifacts/reports/phase27_dialogue_eval_v2_report.json",
        help="Mirrored artifact report JSON.",
    )
    args = parser.parse_args()

    report = write_phase27_dialogue_eval_report(
        suite_path=args.suite,
        output=args.out,
        artifact_output=args.artifact_out,
    )
    plan = report.corpus_expansion_plan
    print("SF.AI — Phase 27 dialogue evaluation v2")
    print(f"  status                    : {report.status}")
    print(f"  scenarios                 : {report.total_scenarios}")
    print(f"  turns                     : {report.passed_turns}/{report.total_turns}")
    print(f"  pass_rate                 : {report.pass_rate:.2%}")
    print(f"  fallback_rate             : {report.fallback_rate:.2%}")
    print(f"  generator_modes           : {report.generator_modes}")
    print(f"  open_generator_ready      : {str(report.open_generator_ready).lower()}")
    print(f"  can_reopen_sf50m_gate     : {str(report.can_reopen_sf50m_gate).lower()}")
    print(f"  can_start_phase28         : {str(report.can_start_phase28).lower()}")
    print(f"  corpus_current            : {plan['current_records']}")
    print(f"  corpus_target             : {plan['target_records']}")
    print(f"  corpus_remaining          : {plan['remaining_records']}")
    print(f"  batches_needed_total      : {plan['batches_needed_total']}")
    print()
    print("blockers:")
    for blocker in report.blockers:
        print(f"  - {blocker}")
    print()
    print(f"output: {args.out}")
    print(f"artifact: {args.artifact_out}")
    return 0 if report.failed_turns == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
