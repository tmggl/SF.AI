"""Phase 27.87 — bounded family-conditioned SF-10M repair coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report() -> dict:
    return json.loads(
        (
            ROOT
            / "artifacts/reports/phase27_87_bounded_family_conditioned_repair_report.json"
        ).read_text(encoding="utf-8")
    )


def test_phase27_87_blocks_runtime_after_weak_fresh_shadow() -> None:
    report = _report()

    assert report["phase"] == "Phase 27.87"
    assert report["status"] == "PHASE27_87_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED"
    assert report["training_started"] is True
    assert report["training_completed"] is True
    assert report["runtime_changed"] is False
    assert report["family_conditioning_runtime_eval"] is True

    decision = report["decision"]
    assert decision["engineering_decision"] == (
        "BLOCK_RUNTIME_DIAGNOSE_FAMILY_CONDITIONED_TRAINING_RESULT"
    )
    assert decision["runtime_release_allowed"] is False
    assert decision["sf50m_justified_transition"] is False
    assert decision["tokenizer_retrain_allowed"] is False
    assert decision["best_fresh_shadow_passed"] == 10
    assert decision["best_fresh_shadow_total"] == 50
    assert "Phase 27.88" in decision["next_phase"]


def test_phase27_87_records_all_three_checkpoints() -> None:
    report = _report()
    checkpoints = {row["checkpoint"]: row for row in report["checkpoints"]}

    assert set(checkpoints) == {
        "sf-10m-step600",
        "sf-10m-step1200",
        "sf-10m-step1800",
    }
    assert checkpoints["sf-10m-step600"]["summary"]["passed"] == 10
    assert checkpoints["sf-10m-step1200"]["summary"]["passed"] == 10
    assert checkpoints["sf-10m-step1800"]["summary"]["passed"] == 7
    assert all(row["meta"]["sf_origin"] is True for row in checkpoints.values())


def test_phase27_87_failure_is_family_collapse_not_runtime_success() -> None:
    report = _report()
    step600 = next(row for row in report["checkpoints"] if row["checkpoint"] == "sf-10m-step600")
    step1200 = next(row for row in report["checkpoints"] if row["checkpoint"] == "sf-10m-step1200")

    assert step600["summary"]["family_summary"]["open_social"]["passed"] == 9
    assert step600["summary"]["family_summary"]["planning"]["passed"] == 0
    assert step1200["summary"]["family_summary"]["planning"]["passed"] == 10
    assert step1200["summary"]["family_summary"]["open_social"]["passed"] == 0


def test_phase27_87_samples_artifact_exists() -> None:
    path = ROOT / "artifacts/samples/phase27_87_bounded_family_conditioned_repair.md"
    text = path.read_text(encoding="utf-8")
    assert "Phase 27.87 Samples" in text
    assert "open_social_01" in text
    assert "sf-10m-step600" in text
