#!/usr/bin/env python3
"""Run Phase 16 evaluation and write eval/reports/sf_10m_eval_v1.json."""

from __future__ import annotations

import argparse

from sf_ai.evaluation import write_phase16_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SF.AI Phase 16 evaluation.")
    parser.add_argument(
        "--chat-prompts",
        default="eval/prompts/saudi_msa_chat_v1.jsonl",
        help="Arabic/Saudi chat prompt suite JSONL.",
    )
    parser.add_argument(
        "--safety-prompts",
        default="eval/prompts/safety_v1.jsonl",
        help="Safety prompt suite JSONL.",
    )
    parser.add_argument(
        "--out",
        default="eval/reports/sf_10m_eval_v1.json",
        help="Output report JSON.",
    )
    args = parser.parse_args()

    report = write_phase16_report(
        chat_prompts=args.chat_prompts,
        safety_prompts=args.safety_prompts,
        output=args.out,
    )
    print("SF.AI — Phase 16 evaluation")
    print(f"  status                      : {report.status}")
    print(f"  cases                       : {report.passed_cases}/{report.total_cases}")
    print(f"  pass_rate                   : {report.pass_rate:.2%}")
    print(f"  runtime_activation_allowed  : {str(report.runtime_activation_allowed).lower()}")
    print(f"  generator_candidate         : {report.generator_gate['candidate']}")
    print(f"  generator_reason            : {report.generator_gate['reason']}")
    print(f"  output                      : {args.out}")
    return 0 if report.failed_cases == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
