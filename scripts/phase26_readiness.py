#!/usr/bin/env python3
"""SF.AI — read-only Phase 26 SF-50M scaling decision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.training.phase26_readiness import write_phase26_report  # noqa: E402


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Phase 26 SF-50M readiness gate")
    parser.add_argument(
        "--out",
        default="artifacts/reports/phase26_sf50m_readiness_report.json",
        help="Where to write the read-only readiness report JSON",
    )
    args = parser.parse_args(argv)

    decision = write_phase26_report(out=args.out)
    print("SF.AI — Phase 26 SF-50M readiness decision")
    print(f"  phase                         : {decision.phase}")
    print(f"  status                        : {decision.status}")
    print(
        "  can_start_sf50m_training      : "
        f"{str(decision.can_start_sf50m_training).lower()}"
    )
    print(f"  recommended_action            : {decision.recommended_action}")
    print()
    print("corpus:")
    print(f"  records                       : {decision.corpus['training_records']}")
    print(f"  minimum                       : {decision.corpus['min_training_records']}")
    print(f"  dialects                      : {decision.corpus['dialects']}")
    print()
    print("phase gates:")
    for key, value in decision.scaling_gates.items():
        print(f"  {key:<30}: {str(value).lower()}")
    print()
    print("target:")
    print(f"  model                         : {decision.target_model}")
    print(f"  config                        : {decision.target_config}")
    print(f"  device                        : {decision.resource_estimate['device']}")
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
