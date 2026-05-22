#!/usr/bin/env python3
"""SF.AI — read-only Phase 22 Gold Dialogue Corpus v2 readiness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.phase22_readiness import build_phase22_readiness_decision  # noqa: E402


def main(argv: list[str]) -> int:
    if argv:
        print("error: phase22-readiness takes no arguments", file=sys.stderr)
        return 2

    decision = build_phase22_readiness_decision()
    print("SF.AI — Phase 22 Gold Dialogue Corpus v2 readiness")
    print(f"  phase                         : {decision.phase}")
    print(f"  status                        : {decision.status}")
    print(f"  can_start_phase23             : {str(decision.can_start_phase23).lower()}")
    print(f"  action                        : {decision.action}")
    print()
    print("corpus:")
    print(f"  path                          : {decision.corpus_path}")
    print(f"  training_records              : {decision.training_records}")
    print(f"  target_records                : {decision.target_records}")
    print(f"  remaining_records             : {decision.remaining_records}")
    print(f"  min_per_dialect               : {decision.min_per_dialect}")
    print(f"  issues                        : {decision.corpus_issue_count}")
    print(f"  dialect_counts                : {decision.dialect_counts}")
    print(f"  dialect_shortfalls            : {decision.dialect_shortfalls}")
    print(f"  quality_counts                : {decision.quality_counts}")
    missing = ", ".join(decision.missing_required_dialects) or "none"
    print(f"  missing_required_dialects     : {missing}")
    print(f"  synthetic_llm_data_allowed    : {str(decision.synthetic_llm_data_allowed).lower()}")
    print()
    print("blockers:")
    if decision.blockers:
        for blocker in decision.blockers:
            print(f"  - {blocker}")
    else:
        print("  - none")
    print()
    print("recommended next commands:")
    for command in decision.recommended_commands:
        print(f"  - {command}")
    print()
    print("notes:")
    for note in decision.notes:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
