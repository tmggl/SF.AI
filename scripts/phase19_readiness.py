#!/usr/bin/env python3
"""SF.AI — read-only Phase 19 readiness decision."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.training.phase19_readiness import build_phase19_readiness_decision  # noqa: E402


def main(argv: list[str]) -> int:
    if argv:
        print("error: phase19-readiness takes no arguments", file=sys.stderr)
        return 2

    decision = build_phase19_readiness_decision()
    print("SF.AI — Phase 19 readiness decision")
    print(f"  phase                         : {decision.phase}")
    print(f"  status                        : {decision.status}")
    print(f"  can_start_training            : {str(decision.can_start_training).lower()}")
    print(f"  lab_experiment_allowed        : {str(decision.lab_experiment_allowed).lower()}")
    print(f"  action                        : {decision.action}")
    print()
    print("corpus:")
    print(f"  path                          : {decision.corpus_path}")
    print(f"  training_records              : {decision.training_records}")
    print(f"  min_training_records          : {decision.min_training_records}")
    print(f"  issues                        : {decision.corpus_issue_count}")
    print(f"  dialect_counts                : {decision.dialect_counts}")
    missing = ", ".join(decision.missing_required_dialects) or "none"
    print(f"  missing_required_dialects     : {missing}")
    print()
    print("artifacts:")
    print(f"  tokenizer_ready               : {str(decision.tokenizer_ready).lower()}")
    print(f"  sf10m_checkpoint_ready        : {str(decision.sf10m_checkpoint_ready).lower()}")
    print(f"  phase16_eval_passed           : {str(decision.phase16_eval_passed).lower()}")
    print(
        "  phase16_runtime_activation    : "
        f"{str(decision.phase16_runtime_activation_allowed).lower()}"
    )
    print()
    print("target:")
    print(f"  model                         : {decision.target_model}")
    print(f"  context                       : {decision.target_context}")
    print(f"  d_model                       : {decision.target_d_model}")
    print(f"  layers                        : {decision.target_layers}")
    print(f"  heads                         : {decision.target_heads}")
    print(f"  device                        : {decision.device}")
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

    # Not-ready is a valid readiness decision, not a shell failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
