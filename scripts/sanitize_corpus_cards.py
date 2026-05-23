#!/usr/bin/env python3
"""Rewrite chat corpus CARD files with natural-dialogue-only metadata."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "data/corpus/chat/jsonl"


def _count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def _infer_dialect(name: str) -> str:
    if "saudi" in name:
        return "saudi"
    if "msa" in name:
        return "msa"
    return "msa + saudi"


def sanitize_cards(corpus_dir: Path = CORPUS_DIR) -> int:
    changed = 0
    for card_path in sorted(corpus_dir.glob("*.CARD.md")):
        jsonl_path = card_path.with_suffix("").with_suffix(".jsonl")
        dialect = _infer_dialect(card_path.name)
        count = _count_jsonl(jsonl_path)
        source = (
            "sf-ai-natural-dialogue-saudi"
            if dialect == "saudi"
            else "sf-ai-natural-dialogue-msa"
            if dialect == "msa"
            else "sf-ai-natural-dialogue-mixed"
        )
        text = "\n".join(
            [
                f"# {jsonl_path.name}",
                "",
                "- records: " + str(count),
                "- dialect: " + dialect,
                "- language: ar",
                "- quality: silver",
                "- license: owner-approved-for-sf-ai-training",
                "- training_allowed: true",
                "- owner_user_id: sami-local",
                "- target_user_id: sami-local",
                "- source: " + source,
                "- content_scope: everyday natural human dialogue only",
                "- operational_internal_dialogue: forbidden",
                "- external_sources: none",
                "- pretrained_model_outputs: none",
                "",
            ]
        )
        if card_path.read_text(encoding="utf-8") != text:
            card_path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    changed = sanitize_cards()
    print("SF.AI — corpus CARD sanitizer")
    print(f"  cards_changed : {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
