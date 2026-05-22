#!/usr/bin/env python3
"""SF.AI — read-only Phase 20 domain activation gates."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.core.activation import build_phase20_activation_gates  # noqa: E402


def main(argv: list[str]) -> int:
    if argv:
        print("error: phase20-gates takes no arguments", file=sys.stderr)
        return 2

    decision = build_phase20_activation_gates()
    print("SF.AI — Phase 20 domain activation gates")
    print(f"  phase                         : {decision.phase}")
    print(f"  status                        : {decision.status}")
    print(f"  language_track                : {', '.join(decision.language_track)}")
    print(f"  lexicon_track                 : {decision.lexicon_track}")
    print(f"  total_domains                 : {decision.total_domains}")
    print(f"  active_domains                : {', '.join(decision.active_domains) or 'none'}")
    print(
        "  ready_offline_domains         : "
        f"{', '.join(decision.ready_offline_domains) or 'none'}"
    )
    print(
        "  candidate_domains             : "
        f"{', '.join(decision.candidate_domains) or 'none'}"
    )
    print(f"  can_activate_any_domain       : {str(decision.can_activate_any_domain).lower()}")
    print()
    print("domain gates:")
    for gate in decision.gates:
        blockers = ", ".join(gate.blockers) or "none"
        print(
            f"  - {gate.domain:12} "
            f"status={gate.current_status:13} "
            f"can_activate={str(gate.can_activate_now).lower():5} "
            f"recommended={gate.recommended_status} "
            f"blockers={blockers}"
        )
    print()
    print("notes:")
    for note in decision.notes:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
