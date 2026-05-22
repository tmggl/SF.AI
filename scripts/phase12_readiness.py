#!/usr/bin/env python3
"""SF.AI — read-only Phase 12 readiness decision."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.training.phase12_readiness import build_phase12_readiness_decision  # noqa: E402


def main(argv: list[str]) -> int:
    if argv:
        print("error: phase12-readiness takes no arguments", file=sys.stderr)
        return 2

    decision = build_phase12_readiness_decision()
    print("SF.AI — Phase 12 readiness decision")
    print(f"  phase                         : {decision.phase}")
    print(f"  preflight_pass                : {str(decision.preflight_pass).lower()}")
    print(f"  can_train_now                 : {str(decision.can_train_now).lower()}")
    print(
        "  training_permission_granted   : "
        f"{str(decision.training_permission_granted).lower()}"
    )
    print(f"  required_permission_phrase    : {decision.required_permission_phrase}")
    print(f"  required_confirmation_flag    : {decision.required_confirmation_flag}")
    print(f"  action                        : {decision.action}")
    print()
    print("corpus:")
    print(f"  status                        : {decision.corpus_status}")
    print(f"  training_ready                : {decision.corpus_training_ready}")
    print(f"  issues                        : {decision.corpus_issue_count}")
    print(f"  dialect_counts                : {decision.corpus_dialect_counts}")
    print(f"  required_dialects             : {', '.join(decision.required_dialects)}")
    missing = ", ".join(decision.missing_required_dialects) or "none"
    print(f"  missing_required_dialects     : {missing}")
    print(f"  language_balance_status       : {decision.language_balance_status}")
    print()
    print("tokenization:")
    print(f"  status                        : {decision.tokenization_status}")
    print(f"  protected_terms_total         : {decision.protected_terms_total}")
    print(f"  protected_terms_covered       : {decision.protected_terms_covered}")
    print(f"  coverage_ratio                : {decision.protected_terms_coverage_ratio:.2%}")
    print()
    print("sources:")
    print(f"  source_count                  : {decision.source_count}")
    print(f"  local_reference_records       : {decision.local_reference_records}")
    print()
    print("artifacts:")
    if decision.artifacts_present:
        for artifact in decision.artifacts_present:
            print(f"  - {artifact}")
    else:
        print("  - none")
    print()
    print("command after explicit permission only:")
    print(f"  {decision.required_command_after_permission}")
    print()
    print("notes:")
    for note in decision.notes:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
