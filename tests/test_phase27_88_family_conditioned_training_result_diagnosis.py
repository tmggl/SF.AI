"""Phase 27.88 — family-conditioned training result diagnosis coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_88_family_conditioned_training_result_diagnosis_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_88_diagnoses_sequential_curriculum_and_blocks_training() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.88"
    assert report["status"] == "PHASE27_88_DIAGNOSED_SEQUENTIAL_CURRICULUM_COLLAPSE_NO_TRAINING"
    assert report["training_started"] is False
    assert report["runtime_changed"] is False

    decision = report["decision"]
    assert decision["engineering_decision"] == (
        "DESIGN_STRATIFIED_ROUND_ROBIN_CURRICULUM_BEFORE_ANY_TRAINING"
    )
    assert decision["new_training_allowed"] is False
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["sampler_implementation_allowed"] is True
    assert "Phase 27.89" in decision["next_phase"]


def test_phase27_88_topic_is_underexposed_in_first_1800_samples() -> None:
    report = _report()
    counts = report["first_1800_family_counts"]

    assert counts["موضوع"] == 5
    assert counts["متابعة"] == 451
    assert counts["تنظيم"] == 452
    assert report["evidence"]["topic_underexposed_before_step1800"] is True


def test_phase27_88_checkpoint_windows_explain_family_collapse() -> None:
    report = _report()
    windows = report["checkpoint_training_windows"]
    align = {row["checkpoint"]: row for row in report["checkpoint_alignment"]}

    assert windows["sf-10m-step1200"]["dominant_family"] == "تنظيم"
    assert align["sf-10m-step1200"]["pass_dominant_family"] == "planning"
    assert align["sf-10m-step1200"]["aligned"] is True
    assert windows["sf-10m-step1800"]["dominant_family"] == "دعم"
    assert align["sf-10m-step1800"]["pass_dominant_family"] == "support"
    assert align["sf-10m-step1800"]["aligned"] is True


def test_phase27_88_weights_keep_capacity_low() -> None:
    weights = _report()["root_cause_weights"]

    assert weights["sequential_curriculum_ordering"] == 38
    assert weights["checkpoint_recency_bias"] == 22
    assert weights["topic_underexposure_before_step1800"] == 16
    assert weights["model_capacity"] == 4
