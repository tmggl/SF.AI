#!/usr/bin/env python3
"""SF.AI — Validate a chat dataset directory or JSONL file.

Usage:
    python scripts/validate_dataset.py data/corpus/chat/jsonl
    python scripts/validate_dataset.py data/corpus/chat/jsonl/my_file.jsonl

Prints a per-file summary and exits with code 1 if any issues were found.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make repo root importable when invoked directly.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets import ChatDataset, validate_jsonl_file  # noqa: E402


def _validate_path(target: Path) -> int:
    if target.is_file():
        report = validate_jsonl_file(target)
        print(report.summary())
        for issue in report.issues:
            print("  -", issue.describe())
        return 0 if report.is_clean else 1

    if not target.exists():
        print(f"error: path does not exist: {target}", file=sys.stderr)
        return 2

    dataset = ChatDataset(root=target)
    files = dataset.jsonl_files()
    if not files:
        print(f"no .jsonl files under {target}")
        return 0

    bad = 0
    for report in dataset.validate_all():
        print(report.summary())
        if not report.is_clean:
            bad += 1
            for issue in report.issues:
                print("  -", issue.describe())

    stats = dataset.stats()
    print(
        f"\nTotals: files={stats.files}, valid={stats.valid_samples}, "
        f"messages user={stats.user_messages}/assistant={stats.assistant_messages}"
        f"/system={stats.system_messages}, chars={stats.total_chars}"
    )
    return 0 if bad == 0 else 1


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_dataset.py <path-to-jsonl-or-dir>", file=sys.stderr)
        return 2
    return _validate_path(Path(argv[1]))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
