#!/usr/bin/env python3
"""SF.AI — strict read-only Phase 22 completion gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.phase22_readiness import build_phase22_completion_gate  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify whether Phase 22 is fully complete before Phase 23."
    )
    parser.add_argument("--batch-size", type=int, default=25)
    args = parser.parse_args(argv)

    gate = build_phase22_completion_gate(batch_size=args.batch_size)
    print("SF.AI — Phase 22 completion gate")
    print(f"  phase                         : {gate.phase}")
    print(f"  status                        : {gate.status}")
    print(f"  can_advance_phase23           : {str(gate.can_advance_phase23).lower()}")
    print(f"  readiness_status              : {gate.readiness_status}")
    print(f"  corpus_path                   : {gate.corpus_path}")
    print(f"  training_records              : {gate.training_records}")
    print(f"  target_records                : {gate.target_records}")
    print(f"  remaining_records             : {gate.remaining_records}")
    print(f"  dialect_counts                : {gate.dialect_counts}")
    print(f"  dialect_shortfalls            : {gate.dialect_shortfalls}")
    print(f"  current_next_batch            : {gate.current_next_batch or 'none'}")
    print()
    print("completion checks:")
    for name, passed in gate.completion_checks.items():
        print(f"  - {name}: {str(passed).lower()}")
    print()
    print("missing requirements:")
    if gate.missing_requirements:
        for item in gate.missing_requirements:
            print(f"  - {item}")
    else:
        print("  - none")
    print()
    print("required before advance:")
    for item in gate.required_before_advance:
        print(f"  - {item}")
    print()
    print("notes:")
    for note in gate.notes:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
