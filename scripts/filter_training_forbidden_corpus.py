#!/usr/bin/env python3
"""Remove operational/internal records from training corpus JSONL files.

The public dialogue corpus must teach natural Arabic/Saudi conversation, not
SF.AI project management, agent workflow, commits, phases, gates, or Sami's
private operating style. This script rewrites training JSONL files in place
and writes a counts-only report. Removed text is intentionally not archived.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sf_ai.datasets.corpus_governance import (  # noqa: E402
    detect_training_forbidden_operational_terms,
)


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def _update_card_count(jsonl_path: Path, count: int) -> bool:
    card = jsonl_path.with_suffix(".CARD.md")
    if not card.exists():
        return False
    lines = card.read_text(encoding="utf-8").splitlines()
    changed = False
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- records:"):
            out.append(f"- records: {count}")
            changed = True
        else:
            out.append(line)
    if changed:
        card.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def filter_corpus(corpus_dir: Path) -> dict[str, Any]:
    report: dict[str, Any] = {
        "policy": "training_forbidden_operational_internal_dialogue",
        "corpus_dir": str(corpus_dir),
        "files_scanned": 0,
        "records_before": 0,
        "records_after": 0,
        "records_removed": 0,
        "terms": {},
        "files": [],
        "note": (
            "Removed records are intentionally not archived as review-only; "
            "they are forbidden for training corpus use."
        ),
    }
    term_counts: Counter[str] = Counter()
    for path in sorted(corpus_dir.glob("*.jsonl")):
        records = _iter_jsonl(path)
        kept: list[dict[str, Any]] = []
        removed = 0
        for record in records:
            terms = detect_training_forbidden_operational_terms(record)
            if terms:
                removed += 1
                term_counts.update(terms)
            else:
                kept.append(record)

        if removed:
            _write_jsonl(path, kept)
            _update_card_count(path, len(kept))

        report["files_scanned"] += 1
        report["records_before"] += len(records)
        report["records_after"] += len(kept)
        report["records_removed"] += removed
        if removed or len(records) == 0:
            report["files"].append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "before": len(records),
                    "after": len(kept),
                    "removed": removed,
                }
            )

    report["terms"] = dict(sorted(term_counts.items(), key=lambda item: (-item[1], item[0])))
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", default="data/corpus/chat/jsonl")
    parser.add_argument(
        "--report",
        default="artifacts/reports/corpus_operational_filter_report.json",
    )
    args = parser.parse_args(argv)

    report = filter_corpus(ROOT / args.corpus_dir)
    report_path = ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("SF.AI — corpus operational/internal filter")
    print(f"  corpus          : {args.corpus_dir}")
    print(f"  files_scanned   : {report['files_scanned']}")
    print(f"  records_before  : {report['records_before']}")
    print(f"  records_after   : {report['records_after']}")
    print(f"  records_removed : {report['records_removed']}")
    print(f"  report          : {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
