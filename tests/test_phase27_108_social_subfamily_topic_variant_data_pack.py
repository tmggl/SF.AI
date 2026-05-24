"""Phase 27.108 — social subfamily/topic variant data pack coverage."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from sf_ai.datasets.corpus_governance import (
    TRAINING_FORBIDDEN_OPERATIONAL_TERMS,
    audit_jsonl_file_for_training,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_108_social_subfamily_topic_variant_data_pack_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION.json"
DOC = ROOT / "docs/PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_REPORT.md"
PACKS = {
    "social_msa": ROOT / "data/corpus/chat/jsonl/dialogue_batch_v14_social_subfamily_msa_014.jsonl",
    "social_saudi": ROOT / "data/corpus/chat/jsonl/dialogue_batch_v14_social_subfamily_saudi_014.jsonl",
    "topic_msa": ROOT / "data/corpus/chat/jsonl/dialogue_batch_v14_topic_variants_msa_014.jsonl",
    "topic_saudi": ROOT / "data/corpus/chat/jsonl/dialogue_batch_v14_topic_variants_saudi_014.jsonl",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_phase27_108_decision_allows_audit_only() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.108"
    assert report["status"] == "PHASE27_108_DATA_PACK_READY_FOR_AUDIT_NO_TRAINING"
    assert report["decision"] == decision
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_109_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_AUDIT_NO_TRAINING"
    )
    assert decision["phase27_109_audit_allowed"] is True
    assert decision["bounded_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert "Phase 27.109" in decision["next_phase"]


def test_phase27_108_pack_counts_and_balance() -> None:
    report = _json(REPORT)
    summary = report["summary"]

    assert summary["total_records"] == 480
    assert summary["dialect_counts"] == {"msa": 240, "saudi": 240}
    assert set(summary["social_subfamily_counts"].values()) == {30}
    assert set(summary["topic_counts"].values()) == {30}
    assert summary["quality"] == {"gold": 480, "silver": 0, "bronze": 0}

    rows = [row for path in PACKS.values() for row in _rows(path)]
    assert len(rows) == 480
    assert Counter(row["provenance"]["dialect"] for row in rows) == {"msa": 240, "saudi": 240}
    assert Counter(row["provenance"]["quality"] for row in rows) == {"gold": 480}


def test_phase27_108_social_subfamilies_are_explicit() -> None:
    rows = _rows(PACKS["social_msa"]) + _rows(PACKS["social_saudi"])
    counts = Counter(
        (row["provenance"]["dialect"], row["provenance"]["dialogue_subfamily"])
        for row in rows
    )

    assert len(rows) == 360
    assert set(counts.values()) == {30}
    assert set(subfamily for _dialect, subfamily in counts) == {
        "greeting",
        "smalltalk",
        "open_chat",
        "thanks",
        "identity",
        "capability",
    }
    assert all(row["provenance"]["dialogue_family"] == "open_social" for row in rows)


def test_phase27_108_topic_variants_keep_canonical_topic() -> None:
    rows = _rows(PACKS["topic_msa"]) + _rows(PACKS["topic_saudi"])
    counts = Counter(
        (row["provenance"]["dialect"], row["provenance"]["topic_canonical"])
        for row in rows
    )

    assert len(rows) == 120
    assert set(counts.values()) == {30}
    assert set(topic for _dialect, topic in counts) == {"الصداقة", "الأخوة"}
    assert all(row["provenance"]["dialogue_family"] == "topic" for row in rows)
    assert all(row["provenance"]["topic_variant"] for row in rows)
    assert any(row["provenance"]["topic_variant"] == "الصداقه" for row in rows)
    assert any(row["provenance"]["topic_variant"] == "الاخوه" for row in rows)


def test_phase27_108_governance_clean_and_no_operational_dialogue() -> None:
    for path in PACKS.values():
        audit = audit_jsonl_file_for_training(path)
        assert audit.error_count == 0
        assert audit.training_ready == audit.total_records

        for row in _rows(path):
            message_text = "\n".join(msg["content"] for msg in row["messages"])
            forbidden = [
                term for term in TRAINING_FORBIDDEN_OPERATIONAL_TERMS if term in message_text
            ]
            assert forbidden == []
            provenance = row["provenance"]
            assert provenance["license"] == "owner-approved-for-sf-ai-training"
            assert provenance["training_allowed"] is True
            assert provenance["owner_user_id"] == "sami-local"
            assert provenance["created_by_user_id"] == "sf-ai-local-author"
            assert provenance["target_user_id"] == "sami-local"
            assert provenance["user_scope"] == "single_user"


def test_phase27_108_doc_exists_and_names_next_phase() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "Phase 27.108" in text
    assert "PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION" in text
    assert "Phase 27.109" in text
