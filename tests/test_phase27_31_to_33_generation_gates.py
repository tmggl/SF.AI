"""Phase 27.31–27.33 generation-gate reports."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _report(name: str) -> dict:
    path = ROOT / "artifacts/reports" / name
    assert path.exists(), f"missing report: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase27_31_records_partial_natural_repair() -> None:
    report = _report("phase27_31_natural_intent_topic_dataset_report.json")
    assert report["phase"] == "Phase 27.31"
    assert report["runtime_allowed"] is False
    assert report["natural_shadow_27_31"]["passed"] == 20
    assert report["natural_shadow_27_31"]["eval_records"] == 20
    assert report["micro_probe_regression"]["passed"] == 32
    assert report["micro_probe_regression"]["eval_records"] == 32
    assert report["training"]["fresh_mixed_prompt_leakage"] == []
    assert report["training"]["natural_shadow_prompt_leakage"] == []


def test_phase27_32_records_balanced_calibration_blocker() -> None:
    report = _report("phase27_32_balanced_natural_calibration_report.json")
    assert report["phase"] == "Phase 27.32"
    assert report["runtime_allowed"] is False
    assert report["definition_shadow_27_29"]["passed"] == 6
    assert report["definition_shadow_27_29"]["eval_records"] == 6
    assert report["calibration_shadow_27_32"]["passed"] == 12
    assert report["calibration_shadow_27_32"]["eval_records"] == 12
    assert report["training"]["fresh_mixed_prompt_leakage"] == []
    assert report["training"]["calibration_shadow_prompt_leakage"] == []


def test_phase27_33_passes_all_generation_gates_without_leakage() -> None:
    report = _report("phase27_33_advice_micro_stabilization_report.json")
    assert report["phase"] == "Phase 27.33"
    assert report["runtime_allowed"] is True
    assert report["limited_runtime_trial_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["checkpoint_name"] == "sf-10m-step9800"
    assert report["fresh_mixed_shadow_27_30"]["passed"] == 18
    assert report["fresh_mixed_shadow_27_30"]["eval_records"] == 18
    assert report["natural_shadow_27_31"]["passed"] == 20
    assert report["natural_shadow_27_31"]["eval_records"] == 20
    assert report["calibration_shadow_27_32"]["passed"] == 12
    assert report["calibration_shadow_27_32"]["eval_records"] == 12
    assert report["advice_shadow_27_33"]["passed"] == 4
    assert report["advice_shadow_27_33"]["eval_records"] == 4
    assert report["micro_probe_regression"]["passed"] == 32
    assert report["micro_probe_regression"]["eval_records"] == 32
    assert report["training"]["fresh_mixed_prompt_leakage"] == []
    assert report["training"]["natural_shadow_prompt_leakage"] == []
    assert report["training"]["calibration_shadow_prompt_leakage"] == []
    assert report["training"]["advice_shadow_prompt_leakage"] == []
