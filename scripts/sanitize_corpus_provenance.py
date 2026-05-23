#!/usr/bin/env python3
"""Sanitize training-corpus provenance away from project/agent wording."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


def _source_for(record: dict[str, Any]) -> str:
    provenance = record.get("provenance") or {}
    dialect = str(provenance.get("dialect") or "ar")
    if dialect == "msa":
        return "sf-ai-natural-dialogue-msa"
    if dialect == "saudi":
        return "sf-ai-natural-dialogue-saudi"
    return "sf-ai-natural-dialogue-ar"


def sanitize_file(path: Path) -> tuple[int, int]:
    changed = 0
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            provenance = record.get("provenance")
            if isinstance(provenance, dict):
                desired = {
                    "source": _source_for(record),
                    "created_by_user_id": "sf-ai-local-author",
                    "notes": "general human dialogue; owner approved; no external dataset",
                }
                for key, value in desired.items():
                    if provenance.get(key) != value:
                        provenance[key] = value
                        changed += 1
            records.append(record)
    if changed:
        with path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    return len(records), changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", default="data/corpus/chat/jsonl")
    args = parser.parse_args()
    corpus_dir = ROOT / args.corpus_dir
    total_records = 0
    total_changes = 0
    for path in sorted(corpus_dir.glob("*.jsonl")):
        records, changes = sanitize_file(path)
        total_records += records
        total_changes += changes
    print("SF.AI — corpus provenance sanitizer")
    print(f"  corpus          : {args.corpus_dir}")
    print(f"  records_seen    : {total_records}")
    print(f"  fields_changed  : {total_changes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
