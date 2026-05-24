"""Phase 27.84 — objective/curriculum failure diagnosis coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_84_objective_curriculum_failure_diagnosis_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_84_blocks_training_and_identifies_family_signal_gap() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.84"
    assert report["status"] == "PHASE27_84_DIAGNOSED_OBJECTIVE_CURRICULUM_FAILURE_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False
    assert report["decision"]["engineering_decision"] == (
        "DESIGN_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_BEFORE_ANY_TRAINING"
    )

    conditioning = report["evidence"]["conditioning_probe"]
    assert conditioning["metadata_dialogue_family"] == "planning"
    assert conditioning["dialect_condition_visible_to_model"] is True
    assert conditioning["family_condition_visible_to_model"] is False


def test_phase27_84_root_cause_weights_prioritize_objective_not_capacity() -> None:
    weights = _report()["root_cause_weights"]

    assert weights["objective_family_signal_missing"] == 30
    assert weights["curriculum_sampling_not_family_conditioned_in_text"] == 24
    assert weights["model_capacity"] == 4
    assert weights["objective_family_signal_missing"] > weights["model_capacity"]


def test_phase27_84_evidence_shows_loss_quality_mismatch_and_collapse() -> None:
    evidence = _report()["evidence"]

    assert evidence["pack_balanced"] is True
    assert evidence["family_signal_missing"] is True
    assert evidence["collapse_after_balanced_data"] is True
    assert evidence["loss_quality_mismatch"] is True
    assert evidence["best_checkpoint"]["checkpoint"] == "sf-10m-step1200"
    assert evidence["best_checkpoint"]["dominant_family"] == "planning"
    assert evidence["best_checkpoint"]["fresh_shadow_passed"] == 11
