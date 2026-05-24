"""Phase 27.102 — topic prototype contrastive gate coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_report.json"
DECISION = ROOT / "artifacts/reports/PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_DECISION.json"
CANARY = ROOT / "eval/prompts/phase27_102_topic_prototype_contrastive_canary.json"
SPEC = ROOT / "artifacts/reports/phase27_102_topic_prototype_contrastive_gate_spec.json"


def _report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def test_phase27_102_gate_blocks_training_runtime_and_scaling() -> None:
    report = _report()
    decision = report["decision"]

    assert report["phase"] == "Phase 27.102"
    assert report["status"] == "PHASE27_102_GATE_ENCODED_CURRICULUM_PACK_ALLOWED_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert decision["engineering_decision"] == (
        "ALLOW_PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_NO_TRAINING"
    )
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["curriculum_pack_allowed"] is True
    assert decision["next_phase"].startswith("Phase 27.103")


def test_phase27_102_gate_catches_phase27_100_metric_blind_spot() -> None:
    report = _report()
    legacy = report["legacy_result_probe"]

    assert legacy["best_checkpoint"] == "sf-10m-step1800"
    assert legacy["reported_wrong_topic_count"] == 0
    assert legacy["observed_wrong_topic_count"] == 8
    assert legacy["metric_blind_spot_detected"] is True
    assert legacy["observed_wrong_topic_substitutions"] == {
        "الصداقة": 7,
        "الامتنان": 1,
    }
    assert legacy["copy_anchor_passed"] == 18
    assert legacy["copy_anchor_total"] == 26


def test_phase27_102_canary_and_spec_are_strict() -> None:
    report = _report()
    decision = json.loads(DECISION.read_text(encoding="utf-8"))
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    canary = json.loads(CANARY.read_text(encoding="utf-8"))

    assert report["decision"] == decision
    assert spec["thresholds"]["observed_wrong_topic_count"] == 0
    assert spec["thresholds"]["copy_anchor"] == "all"
    assert "required_topic_missing" in spec["metric_rules"]["reason_precedence"]
    assert canary["coverage"]["prompt_count"] == 16
    assert canary["thresholds"]["observed_wrong_topic_max"] == 0
    assert canary["thresholds"]["copy_anchor_min"] == "16/16"
    assert set(canary["prototype_decoys"]) == {"الصداقة", "الامتنان"}
    for row in canary["prompts"]:
        assert row["requested_topic"] not in row["forbidden_terms"]
        assert row["copy_anchor_required"] is True
