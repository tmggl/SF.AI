"""Phase 27.103 — topic prototype contrastive curriculum pack coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_pack_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_DECISION.json"
MANIFEST = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_manifest.json"
SCHEDULE = ROOT / "artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_schedule.json"
PACK = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_103_pack_allows_next_bounded_training_but_blocks_runtime() -> None:
    report = _json(REPORT)
    decision = _json(DECISION)

    assert report["phase"] == "Phase 27.103"
    assert report["status"] == (
        "PHASE27_103_TOPIC_PROTOTYPE_CURRICULUM_PACK_READY_FOR_BOUNDED_TRAINING"
    )
    assert report["decision"] == decision
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_TRAINING"
    )
    assert decision["phase27_104_training_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.104")


def test_phase27_103_pack_is_balanced_and_governance_clean() -> None:
    report = _json(REPORT)
    quality = report["quality"]
    audit = report["file_audit"]

    assert report["records_authored"] == 192
    assert quality["balanced"] is True
    assert quality["records_per_dialect"] == {"msa": 96, "saudi": 96}
    assert set(quality["records_per_topic"].values()) == {24}
    assert set(quality["records_per_topic_dialect"].values()) == {12}
    assert quality["copy_anchor_bad_count"] == 0
    assert quality["wrong_topic_leak_count"] == 0
    assert quality["duplicate_pair_count"] == 0
    assert audit["total_records"] == 192
    assert audit["training_ready"] == 192
    assert audit["error_count"] == 0
    assert audit["issues"] == []


def test_phase27_103_manifest_schedule_and_pack_match() -> None:
    report = _json(REPORT)
    manifest = _json(MANIFEST)
    schedule = _json(SCHEDULE)
    rows = [json.loads(line) for line in PACK.read_text(encoding="utf-8").splitlines()]

    assert manifest["pack_file"] == report["authored_file"]
    assert manifest["records"] == 192
    assert manifest["quality_rules"]["assistant_wrong_topic_leak_max"] == 0
    assert manifest["quality_rules"]["records_per_topic"] == 24
    assert manifest["quality_rules"]["records_per_topic_dialect"] == 12
    assert schedule["total_records"] == 192
    assert schedule["adjacent_same_topic_count"] == 0
    assert set(schedule["first_64_topic_counts"].values()) == {8}
    assert schedule["first_64_dialect_counts"] == {"msa": 32, "saudi": 32}
    assert len(rows) == 192
    assert {
        row["provenance"]["source"]
        for row in rows
    } == {"sf-ai-topic-prototype-contrastive-curriculum-v1"}
    assert all(row["provenance"]["quality"] == "gold" for row in rows)
    assert all(row["provenance"]["training_allowed"] is True for row in rows)
