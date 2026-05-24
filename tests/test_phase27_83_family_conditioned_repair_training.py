"""Phase 27.83 — bounded repair training result coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_83_family_conditioned_repair_training_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_83_training_completed_but_runtime_blocked() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.83"
    assert report["status"] == "PHASE27_83_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert report["sovereignty_mode"] == "SF-native only"

    decision = report["decision"]
    assert decision["engineering_decision"] == "BLOCK_RUNTIME_DIAGNOSE_OBJECTIVE_CURRICULUM_FAILURE"
    assert decision["runtime_release_allowed"] is False
    assert decision["ui_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["best_checkpoint_by_canary"] == "sf-10m-step1200"
    assert decision["best_checkpoint_by_eval_loss"] == "sf-10m-step600"
    assert "Phase 27.84" in decision["next_phase"]


def test_phase27_83_fresh_shadow_scores_show_no_runtime_candidate() -> None:
    report = _report()
    scores = {
        row["checkpoint"]: row["fresh_shadow"]["passed"]
        for row in report["checkpoints"]
    }
    assert scores == {
        "sf-10m-step600": 7,
        "sf-10m-step1200": 11,
        "sf-10m-step1800": 3,
    }
    assert all(row["fresh_shadow"]["total"] == 60 for row in report["checkpoints"])
    assert max(scores.values()) < 60


def test_phase27_83_checkpoints_are_sovereign_local_artifacts() -> None:
    report = _report()
    for row in report["checkpoints"]:
        meta = row["meta"]
        assert meta["state_exists"] is True
        assert meta["sf_origin"] is True
        assert meta["model_name"] == "sf-10m"
        assert "init=artifacts/eval/phase27_77" in meta["notes"]
