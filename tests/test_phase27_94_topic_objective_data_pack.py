"""Phase 27.94 — topic-objective data pack tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_94_topic_objective_data_pack import WAFA_SAUDI_PAIRS

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v11_topic_objective_wafa_saudi_011.jsonl"


def test_phase27_94_pack_has_only_saudi_wafa_topic_records() -> None:
    rows = [json.loads(line) for line in PACK.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == len(WAFA_SAUDI_PAIRS) == 10
    assert {row["provenance"]["dialect"] for row in rows} == {"saudi"}
    assert {row["provenance"]["topic_term"] for row in rows} == {"الوفاء"}
    assert {row["provenance"]["dialogue_family"] for row in rows} == {"topic"}
    assert all(row["provenance"]["quality"] == "gold" for row in rows)
    assert all(row["provenance"]["training_allowed"] is True for row in rows)
    assert all("الوفاء" in row["messages"][0]["content"] for row in rows)
    assert all(row["messages"][1]["content"].count("الوفاء") == 1 for row in rows)


def test_phase27_94_report_allows_only_next_bounded_training() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_94_topic_objective_data_pack_report.json")
        .read_text(encoding="utf-8")
    )
    decision = report["decision"]

    assert report["phase"] == "Phase 27.94"
    assert report["status"] == "PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_READY_FOR_BOUNDED_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["records_authored"] == 10
    assert report["file_audit"]["training_ready"] == 10
    assert report["post_pack_phase27_93_gate"]["training_data_ready"] is True
    assert report["post_pack_phase27_93_gate"]["shortfalls"] == {}
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING"
    )
    assert decision["phase27_95_training_allowed"] is True
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False


def test_phase27_94_split_manifest_includes_new_pack() -> None:
    manifest = json.loads(
        (ROOT / "data/corpus/chat/splits/dialogue_split_v1.json").read_text(encoding="utf-8")
    )
    pack_entries = [
        row for row in manifest["records"] if row["file"] == "dialogue_batch_v11_topic_objective_wafa_saudi_011.jsonl"
    ]

    assert manifest["total_records"] == 8645
    assert len(pack_entries) == 10
    assert {row["dialect"] for row in pack_entries} == {"saudi"}
    assert {row["quality"] for row in pack_entries} == {"gold"}
    assert {row["dialogue_family"] for row in pack_entries} == {"topic"}
