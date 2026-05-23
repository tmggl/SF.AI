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


def test_phase27_34_guarded_runtime_trial_passes_ui_smoke() -> None:
    report = _report("phase27_34_guarded_runtime_trial_report.json")
    assert report["phase"] == "Phase 27.34"
    assert report["status"] == "PASSED_GUARDED_RUNTIME_TRIAL_READY_FOR_UI_TEST"
    assert report["ui_test_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["summary"]["passed"] == 9
    assert report["summary"]["total"] == 9
    assert report["summary"]["generator_passed"] == 7
    assert report["summary"]["template_controls_passed"] == 2
    assert report["trial_policy"]["request_flag"] == "generator_trial=true"
    assert report["trial_policy"]["candidate_generator"] == "sf_10m_phase27_33"


def test_phase27_35_live_ui_trial_observations_pass() -> None:
    report = _report("phase27_35_live_ui_trial_observations_report.json")
    assert report["phase"] == "Phase 27.35"
    assert report["status"] == "PASSED_LIVE_UI_TRIAL_READY_FOR_USER_OBSERVATION"
    assert report["ui_user_test_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["summary"]["ui_passed"] is True
    assert report["summary"]["cases_passed"] == 10
    assert report["summary"]["cases_total"] == 10
    assert report["summary"]["generator_cases_passed"] == 7
    assert report["summary"]["generator_cases"] == 7
    assert report["summary"]["template_controls_passed"] == 3
    assert report["summary"]["template_controls"] == 3


def test_phase27_36_live_ui_triage_quality_floor_passes() -> None:
    report = _report("phase27_36_live_ui_triage_report.json")
    assert report["phase"] == "Phase 27.36"
    assert report["status"] == "PASSED_LIVE_UI_TRIAGE_QUALITY_FLOOR_ACTIVE"
    assert report["user_test_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["summary"]["cases_passed"] == 27
    assert report["summary"]["cases_total"] == 27
    assert report["summary"]["generated_passed"] == 18
    assert report["summary"]["generated_total"] == 18
    assert report["summary"]["quality_floor_passed"] == 5
    assert report["summary"]["quality_floor_total"] == 5
    assert report["summary"]["controls_passed"] == 4
    assert report["summary"]["controls_total"] == 4
    assert report["triage_decision"]["quality_floor"] == (
        "block raw chat.general and unsupported definition topics"
    )


def test_phase27_37_supported_topic_expansion_passes() -> None:
    report = _report("phase27_37_supported_topic_expansion_report.json")
    assert report["phase"] == "Phase 27.37"
    assert report["status"] == "PASSED_SUPPORTED_TOPIC_EXPANSION_QUALITY_GATED"
    assert report["user_test_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["expanded_topics"] == ["الصبر"]
    assert report["semantic_topic_guard"] is True
    assert report["summary"]["cases_passed"] == 21
    assert report["summary"]["cases_total"] == 21
    assert report["summary"]["new_topic_passed"] == 3
    assert report["summary"]["new_topic_total"] == 3
    assert report["summary"]["quality_floor_passed"] == 5
    assert report["summary"]["quality_floor_total"] == 5


def test_phase27_38_targeted_topic_curriculum_probe_records_blocker() -> None:
    report = _report("phase27_38_targeted_topic_curriculum_probe_report.json")
    assert report["phase"] == "Phase 27.38"
    assert report["status"] == "PARTIAL_TARGETED_TOPIC_CURRICULUM_KEEP_CURRENT_RUNTIME"
    assert report["training_started"] is True
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["checkpoint_name"] == "sf-10m-step2400"
    assert report["summary"]["passed"] == 6
    assert report["summary"]["total"] == 20
    assert report["summary"]["bucket_summary"]["regression"]["passed"] == 6
    assert report["summary"]["bucket_summary"]["regression"]["total"] == 8
    assert report["summary"]["bucket_summary"]["new_topic"]["passed"] == 0
    assert report["summary"]["bucket_summary"]["new_topic"]["total"] == 8
    assert report["summary"]["bucket_summary"]["heldout"]["passed"] == 0
    assert report["summary"]["bucket_summary"]["heldout"]["total"] == 4


def test_phase27_39_topic_isolation_repair_records_blocker() -> None:
    report = _report("phase27_39_topic_isolation_repair_report.json")
    assert report["phase"] == "Phase 27.39"
    assert report["status"] == "PARTIAL_TOPIC_ISOLATION_KEEP_CURRENT_RUNTIME"
    assert report["training_started"] is True
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["checkpoint_name"] == "sf-10m-step6400"
    assert report["summary"]["passed"] == 10
    assert report["summary"]["total"] == 24
    assert report["summary"]["bucket_summary"]["regression"]["passed"] == 4
    assert report["summary"]["bucket_summary"]["regression"]["total"] == 8
    assert report["summary"]["bucket_summary"]["new_topic"]["passed"] == 2
    assert report["summary"]["bucket_summary"]["new_topic"]["total"] == 8
    assert report["summary"]["bucket_summary"]["heldout"]["passed"] == 1
    assert report["summary"]["bucket_summary"]["heldout"]["total"] == 4
    assert report["summary"]["bucket_summary"]["isolation"]["passed"] == 3
    assert report["summary"]["bucket_summary"]["isolation"]["total"] == 4


def test_phase27_40_tokenizer_context_repair_passes_candidate_gate() -> None:
    report = _report("phase27_40_tokenizer_context_repair_report.json")
    assert report["phase"] == "Phase 27.40"
    assert report["status"] == "PASSED_TOKENIZER_CONTEXT_REPAIR_READY_FOR_GUARDED_RUNTIME_CANDIDATE"
    assert report["training_started"] is True
    assert report["runtime_switch_allowed"] is True
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["checkpoint_name"] == "sf-10m-step6400"
    assert report["candidate_generator"] == "sf_10m_phase27_40"
    assert report["tokenizer"]["sf_origin"] is True
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v5_topic_terms"
    assert report["protected_phrase_behavior"]["max_pieces"] == 1
    assert report["protected_phrase_behavior"]["all_roundtrip_ok"] is True
    assert report["summary"]["passed"] == 24
    assert report["summary"]["total"] == 24
    assert report["summary"]["bucket_summary"]["regression"]["passed"] == 8
    assert report["summary"]["bucket_summary"]["new_topic"]["passed"] == 8
    assert report["summary"]["bucket_summary"]["heldout"]["passed"] == 4
    assert report["summary"]["bucket_summary"]["isolation"]["passed"] == 4
