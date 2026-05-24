"""Phase 27.100 — bounded topic-binding repair coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_100_bounded_topic_binding_repair_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_DECISION.json"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_100_report_blocks_runtime_and_scaling() -> None:
    report = _report()
    decision = report["decision"]

    assert report["phase"] == "Phase 27.100"
    assert report["status"] == "PHASE27_100_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == "BLOCK_RUNTIME_DIAGNOSE_TOPIC_BINDING_REPAIR_RESULT"
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["heldout_runtime_gate_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.101")


def test_phase27_100_best_checkpoint_and_scores_are_recorded() -> None:
    report = _report()
    decision = report["decision"]

    assert report["objective"] == "topic_copy_contrastive_binding_objective_v1"
    assert decision["best_checkpoint"] == "sf-10m-step1800"
    assert decision["known_topic"] == "13/16"
    assert decision["fresh_topic"] == "5/10"
    assert decision["copy_anchor"] == "18/26"
    assert decision["wrong_topic_count"] == 0
    assert decision["topic_family"] == "6/10"
    assert decision["all_family"] == "37/50"
    assert decision["required_gates"] == {
        "known_topic": "16/16",
        "fresh_topic": "8/10",
        "copy_anchor": "26/26",
        "contrastive_wrong_topic_max": 0,
        "topic_family": "8/10",
        "all_family": "45/50",
    }

    best = next(row for row in report["checkpoints"] if row["checkpoint"] == "sf-10m-step1800")
    assert best["known_topic_summary"]["passed"] == 13
    assert best["fresh_topic_summary"]["passed"] == 5
    assert best["all_family"]["summary"]["family_summary"]["topic"]["passed"] == 6


def test_phase27_100_decision_artifact_matches_report() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert report["source_decision"]["decision_id"] == "PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DECISION"
    assert report["training_scope"].startswith("bounded SF-10M topic-binding repair")
