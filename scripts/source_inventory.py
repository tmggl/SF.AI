#!/usr/bin/env python3
"""SF.AI — print a comprehensive local source inventory."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.source_inventory import build_source_inventory  # noqa: E402


def main() -> int:
    report = build_source_inventory()
    print("SF.AI — local source inventory")
    print(f"  phase12_status          : {report.phase12_status}")
    print(f"  source_count            : {report.source_count}")
    print(f"  chat_training_records   : {report.chat_training_records}")
    print(f"  local_reference_records : {report.local_reference_records}")
    print()

    for item in report.sources:
        print(f"- {item.name}")
        print(f"  path                    : {item.path}")
        print(f"  kind                    : {item.kind}")
        print(f"  status                  : {item.status}")
        print(f"  exists                  : {item.exists}")
        print(f"  records                 : {item.records}")
        print(f"  valid_json_records      : {item.valid_json_records}")
        print(f"  private_or_ignored      : {item.private_or_ignored}")
        print(f"  phase12_tokenizer       : {item.phase12_tokenizer_candidate}")
        print(f"  phase13_lm              : {item.phase13_lm_candidate}")
        print(f"  needs_conversion        : {item.needs_conversion}")
        print(f"  action_required         : {item.action_required}")
        if item.stats:
            print(f"  stats                   : {item.stats}")
        for note in item.notes:
            print(f"  note                    : {note}")
        print()

    if report.blockers:
        print("blockers / notes:")
        for blocker in report.blockers:
            print(f"  - {blocker}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
