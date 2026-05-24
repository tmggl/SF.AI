"""Phase 27.81 — balanced family pack coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_81_report_authored_full_balanced_pack_without_training() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_81_balanced_family_pack_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert report["phase"] == "Phase 27.81"
    assert report["status"] == "PHASE27_81_BALANCED_FAMILY_PACK_AUTHORED_NO_TRAINING"
    assert report["total_records"] == 2500
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False

    by_family = {}
    for item in report["generated"]:
        by_family.setdefault(item["family"], 0)
        by_family[item["family"]] += item["records"]
    assert by_family == {
        "open_social": 500,
        "followup": 500,
        "planning": 500,
        "support": 500,
        "topic": 500,
    }


def test_phase27_81_generated_records_have_explicit_family_metadata() -> None:
    sample = ROOT / "data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_saudi_010.jsonl"
    rows = [json.loads(line) for line in sample.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 250
    assert {row["provenance"]["dialogue_family"] for row in rows} == {"topic"}
    assert {row["provenance"]["dialect"] for row in rows} == {"saudi"}
    assert all(row["provenance"]["training_allowed"] is True for row in rows)
    assert all(row["provenance"]["quality"] == "gold" for row in rows)
