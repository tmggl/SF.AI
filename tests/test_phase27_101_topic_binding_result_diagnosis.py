"""Phase 27.101 — topic-binding result diagnosis coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_101_topic_binding_result_diagnosis_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_DECISION.json"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_101_report_blocks_training_runtime_and_scaling() -> None:
    report = _report()
    decision = report["decision"]

    assert report["phase"] == "Phase 27.101"
    assert report["status"] == "PHASE27_101_DIAGNOSED_COPY_ANCHOR_CURRICULUM_GAP_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == (
        "DESIGN_TOPIC_PROTOTYPE_CONTRASTIVE_COPY_ANCHOR_GATE_BEFORE_ANY_TRAINING"
    )
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["heldout_runtime_gate_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["next_phase"].startswith("Phase 27.102")


def test_phase27_101_scores_and_blind_spot_are_recorded() -> None:
    report = _report()

    assert report["best_checkpoint"] == "sf-10m-step1800"
    assert report["score_summary"]["known_topic"] == "13/16"
    assert report["score_summary"]["fresh_topic"] == "5/10"
    assert report["score_summary"]["copy_anchor"] == "18/26"
    assert report["score_summary"]["reported_wrong_topic_count"] == 0
    assert report["score_summary"]["observed_wrong_topic_count"] == 8
    assert report["score_summary"]["topic_family"] == "6/10"
    assert report["score_summary"]["all_family"] == "37/50"

    signals = report["diagnosis_signals"]
    assert signals["wrong_topic_metric_blind_spot"] is True
    assert signals["topic_prototype_attraction"] is True
    assert report["topic_failure_counts"]["wrong_topic_substitutions"] == {
        "الصداقة": 7,
        "الامتنان": 1,
    }


def test_phase27_101_decision_artifact_matches_report() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert report["source_report"].endswith("phase27_100_bounded_topic_binding_repair_report.json")
    assert "fix wrong-topic metric precedence before any training" in report["allowed_next_actions"]
