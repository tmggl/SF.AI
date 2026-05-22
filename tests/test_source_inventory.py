"""Source inventory tests — keeps corpus/reference sources from being conflated."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.datasets.source_inventory import build_source_inventory


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_source_inventory_separates_chat_tasks_and_lexicon(tmp_path: Path) -> None:
    _write_jsonl(
        tmp_path / "data/corpus/chat/jsonl/train.jsonl",
        [
            {
                "domain": "chat",
                "lang": "ar",
                "messages": [
                    {"role": "user", "content": "وشلونك؟"},
                    {"role": "assistant", "content": "بخير."},
                ],
                "provenance": {
                    "source": "sami",
                    "license": "user-provided",
                    "language": "ar",
                    "dialect": "saudi",
                    "quality": "gold",
                    "training_allowed": True,
                },
            }
        ],
    )
    _write_jsonl(
        tmp_path
        / "data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl",
        [{"task": "saudi_lexicon_lookup", "input": "وش", "output": "ماذا"}],
    )
    _write_jsonl(
        tmp_path
        / "resources/lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl",
        [
            {
                "id": "sa-1",
                "term": "وش",
                "normalized_term": "وش",
                "variants": [],
                "kind": "word",
                "category": "question",
                "dialect_labels": ["saudi_general"],
                "dialect_names_ar": ["سعودي عام"],
                "used_in_places": ["السعودية"],
                "meaning_msa": "ماذا",
                "example_saudi": "وش تبي؟",
                "register": "neutral",
                "dialectality": "high",
                "confidence": "high",
                "requires_native_review": False,
                "safety": {
                    "sensitive_or_profane": False,
                    "allow_for_generation": True,
                    "recommended_use": ["runtime_alias"],
                },
                "source_basis": "original_compilation_not_copied_from_mo3jam",
            }
        ],
    )

    report = build_source_inventory(tmp_path)
    by_name = {item.name: item for item in report.sources}

    assert report.phase12_status == "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
    assert by_name["chat_training_jsonl"].phase13_lm_candidate is True
    assert by_name["saudi_dialect_training_tasks_seed_v1"].needs_conversion is True
    assert by_name["saudi_dialect_training_tasks_seed_v1"].phase13_lm_candidate is False
    assert by_name["saudi_seed_v1_lexicon_reference"].kind == "lexicon_reference"
    assert by_name["saudi_seed_v1_lexicon_reference"].tracked_payload_allowed is False


def test_source_inventory_reports_missing_chat_corpus_as_blocker(tmp_path: Path) -> None:
    report = build_source_inventory(tmp_path)
    assert report.phase12_status == "NOT_READY_FOR_TRAINING"
    assert any("chat JSONL" in blocker for blocker in report.blockers)
    assert report.chat_training_records == 0
