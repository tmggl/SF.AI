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


def test_phase27_41_guarded_runtime_switch_passes_live_gate() -> None:
    report = _report("phase27_41_guarded_runtime_switch_report.json")
    assert report["phase"] == "Phase 27.41"
    assert report["status"] == "PASSED_GUARDED_RUNTIME_SWITCH_PHASE27_40"
    assert report["training_started"] is False
    assert report["runtime_default"] == "template"
    assert report["request_flag"] == "generator_trial=true"
    assert report["candidate_generator"] == "sf_10m_phase27_40"
    assert report["candidate_tokenizer"] == "artifacts/tokenizers/sf_bpe/v5_topic_terms"
    assert report["sf50m_allowed"] is False
    assert report["user_test_allowed"] is True
    assert report["summary"]["passed"] == 22
    assert report["summary"]["total"] == 22
    generated = [row for row in report["rows"] if row["actual_generator"] == "sf_10m_phase27_40"]
    controls = [row for row in report["rows"] if row["actual_generator"] == "template"]
    assert len(generated) == 17
    assert len(controls) == 5
    assert all(row["passed"] for row in report["rows"])


def test_phase27_42_live_ui_broader_probes_pass_guarded_gate() -> None:
    report = _report("phase27_42_live_ui_broader_probes_report.json")
    assert report["phase"] == "Phase 27.42"
    assert report["status"] == "PASSED_LIVE_UI_BROADER_PROBES_GUARDED"
    assert report["training_started"] is False
    assert report["runtime_default"] == "template"
    assert report["candidate_generator"] == "sf_10m_phase27_40"
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["summary"]["passed"] == 29
    assert report["summary"]["total"] == 29
    assert report["summary"]["bucket_summary"]["guarded_fallback"]["passed"] == 2
    assert report["summary"]["bucket_summary"]["quality_floor"]["passed"] == 3
    assert report["summary"]["bucket_summary"]["generated_definition"]["passed"] == 9
    assert all(row["passed"] for row in report["rows"])


def test_phase27_43_guarded_data_backed_expansion_blocks_runtime_switch() -> None:
    report = _report("phase27_43_guarded_data_backed_expansion_report.json")
    assert report["phase"] == "Phase 27.43"
    assert report["status"] == "PARTIAL_GUARDED_DATA_BACKED_EXPANSION_KEEP_PHASE27_40_RUNTIME"
    assert report["training_started"] is True
    assert report["candidate_generator"] == "sf_10m_phase27_43"
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["summary"]["passed"] == 10
    assert report["summary"]["total"] == 16
    assert report["summary"]["bucket_summary"]["weak_lane"]["passed"] == 4
    assert report["summary"]["bucket_summary"]["regression"]["passed"] == 6
    assert report["summary"]["bucket_summary"]["new_topic"]["passed"] == 0


def test_phase27_44_tokenizer_curriculum_repair_records_partial_result() -> None:
    report = _report("phase27_44_tokenizer_curriculum_repair_report.json")
    assert report["phase"] == "Phase 27.44"
    assert report["status"] == "PARTIAL_TOKENIZER_CURRICULUM_REPAIR_KEEP_PHASE27_40_RUNTIME"
    assert report["training_started"] is True
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
    assert report["protected_phrase_behavior"]["max_pieces"] == 1
    assert report["protected_phrase_behavior"]["all_roundtrip_ok"] is True
    assert report["runtime_switch_allowed"] is False
    assert report["summary"]["passed"] == 11
    assert report["summary"]["total"] == 16
    assert report["summary"]["bucket_summary"]["weak_lane"]["passed"] == 6


def test_phase27_45_semantic_topic_balance_records_regression() -> None:
    report = _report("phase27_45_semantic_topic_balance_repair_report.json")
    assert report["phase"] == "Phase 27.45"
    assert report["status"] == "PARTIAL_SEMANTIC_TOPIC_BALANCE_KEEP_PHASE27_40_RUNTIME"
    assert report["training_started"] is True
    assert report["runtime_switch_allowed"] is False
    assert report["summary"]["passed"] == 9
    assert report["summary"]["total"] == 16


def test_phase27_46_core_dialogue_stabilization_nearly_passes() -> None:
    report = _report("phase27_46_core_dialogue_stabilization_report.json")
    assert report["phase"] == "Phase 27.46"
    assert report["status"] == "PARTIAL_CORE_DIALOGUE_STABILIZATION_KEEP_PHASE27_40_RUNTIME"
    assert report["training_started"] is True
    assert report["runtime_switch_allowed"] is False
    assert report["summary"]["passed"] == 14
    assert report["summary"]["bucket_summary"]["weak_lane"]["passed"] == 6
    assert report["summary"]["bucket_summary"]["regression"]["passed"] == 8
    assert report["summary"]["bucket_summary"]["new_topic"]["passed"] == 0


def test_phase27_47_new_topic_conditioning_passes_offline_gate() -> None:
    report = _report("phase27_47_new_topic_conditioning_repair_report.json")
    assert report["phase"] == "Phase 27.47"
    assert report["status"] == "PASSED_NEW_TOPIC_CONDITIONING_READY_FOR_GUARDED_SWITCH"
    assert report["training_started"] is True
    assert report["candidate_generator"] == "sf_10m_phase27_47"
    assert report["runtime_switch_allowed"] is True
    assert report["conditioning_repair"]["added_topic_line_for"] == ["الوفاء", "الشجاعة"]
    assert report["summary"]["passed"] == 16
    assert report["summary"]["total"] == 16


def test_phase27_48_guarded_runtime_switch_passes_live_gate() -> None:
    report = _report("phase27_48_guarded_runtime_switch_report.json")
    assert report["phase"] == "Phase 27.48"
    assert report["status"] == "PASSED_GUARDED_RUNTIME_SWITCH_PHASE27_47"
    assert report["training_started"] is False
    assert report["runtime_default"] == "template"
    assert report["request_flag"] == "generator_trial=true"
    assert report["candidate_generator"] == "sf_10m_phase27_47"
    assert report["candidate_tokenizer"] == "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms"
    assert report["sf50m_allowed"] is False
    assert report["user_test_allowed"] is True
    assert report["summary"]["passed"] == 19
    assert report["summary"]["total"] == 19
    assert report["summary"]["bucket_summary"]["generated_weak"]["passed"] == 6
    assert report["summary"]["bucket_summary"]["generated_new_topic"]["passed"] == 2
    assert report["summary"]["bucket_summary"]["generated_regression"]["passed"] == 8
    assert all(row["passed"] for row in report["rows"])


def test_phase27_49_broader_live_ui_probes_pass() -> None:
    report = _report("phase27_49_broader_live_ui_probes_report.json")
    assert report["phase"] == "Phase 27.49"
    assert report["status"] == "PASSED_BROADER_LIVE_UI_PROBES_PHASE27_47"
    assert report["training_started"] is False
    assert report["runtime_default"] == "template"
    assert report["request_flag"] == "generator_trial=true"
    assert report["candidate_generator"] == "sf_10m_phase27_47"
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False
    assert report["user_test_allowed"] is True
    assert report["summary"]["passed"] == 33
    assert report["summary"]["total"] == 33
    assert report["summary"]["bucket_summary"]["generated_social"]["passed"] == 7
    assert report["summary"]["bucket_summary"]["generated_task"]["passed"] == 8
    assert report["summary"]["bucket_summary"]["generated_definition"]["passed"] == 11
    assert all(row["passed"] for row in report["rows"])


def test_phase27_50_generator_only_ui_gate_passes() -> None:
    report = _report("phase27_50_generator_only_ui_gate_report.json")
    assert report["phase"] == "Phase 27.50"
    assert report["status"] == "PASSED_GENERATOR_ONLY_UI_GATE"
    assert report["training_started"] is False
    assert report["runtime_default"] == "generator_only_lab"
    assert report["candidate_generator"] == "sf_10m_phase27_47"
    assert report["template_answers_allowed"] is False
    assert report["summary"]["passed"] == 7
    assert report["summary"]["total"] == 7
    assert all(row["actual_generator"] != "template" for row in report["rows"])
    assert all(row["passed"] for row in report["rows"])


def test_phase27_51_open_dialogue_generalization_audit_blocks_scaling() -> None:
    report = _report("phase27_51_open_dialogue_generalization_audit.json")
    assert report["phase"] == "Phase 27.51"
    assert report["status"] == "FAILED_OPEN_DIALOGUE_GENERALIZATION_AUDIT_TRAINING_REQUIRED"
    assert report["training_started"] is False
    assert report["template_answers_allowed"] is False
    assert report["keyword_lane_success_is_not_enough"] is True
    assert report["candidate_generator"] == "sf_10m_phase27_47"
    assert report["summary"]["live_api"]["passed"] == 3
    assert report["summary"]["live_api"]["total"] == 22
    assert report["summary"]["raw_unconditioned"]["natural_passed"] == 1
    assert report["summary"]["raw_unconditioned"]["natural_total"] == 20


def test_phase27_52_natural_dialogue_objective_repair_stays_guarded() -> None:
    report = _report("phase27_52_natural_dialogue_objective_repair_report.json")
    assert report["phase"] == "Phase 27.52"
    assert report["status"] == "PARTIAL_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_KEEP_PHASE27_47_RUNTIME"
    assert report["training_started"] is True
    assert report["model_size"] == "sf-10m"
    assert report["progressive_scaling_respected"] is True
    assert report["candidate_generator"] == "sf_10m_phase27_52"
    assert report["training_budget"]["steps"] == 9200
    assert report["training_budget"]["step_multiplier_vs_phase27_47"] == 2.0
    assert report["no_keyword_lane_claim"]["intent_conditioning_used_in_training"] is False
    assert report["no_keyword_lane_claim"]["topic_conditioning_used_in_training"] is False
    assert report["summary"]["passed"] == 5
    assert report["summary"]["total"] == 20
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False


def test_phase27_53_natural_dialogue_diversity_expansion_stays_guarded() -> None:
    report = _report("phase27_53_natural_dialogue_diversity_expansion_report.json")
    assert report["phase"] == "Phase 27.53"
    assert report["status"] == "PARTIAL_NATURAL_DIALOGUE_DIVERSITY_KEEP_PHASE27_47_RUNTIME"
    assert report["training_started"] is True
    assert report["model_size"] == "sf-10m"
    assert report["progressive_scaling_respected"] is True
    assert report["candidate_generator"] == "sf_10m_phase27_53"
    assert report["unique_train_records"] == 10540
    assert report["dialect_counts"] == {"msa": 5270, "saudi": 5270}
    assert report["training_budget"]["steps"] == 18000
    assert report["governance"]["external_data_used"] is False
    assert report["governance"]["operational_dialogue_excluded"] is True
    assert report["summary"]["passed"] == 2
    assert report["summary"]["total"] == 36
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["phase28_allowed"] is False


def test_phase27_54_capacity_objectivity_gate_blocks_full_scaling() -> None:
    report = _report("phase27_54_capacity_objectivity_gate_report.json")
    assert report["phase"] == "Phase 27.54"
    assert report["training_started"] is False
    assert report["progressive_scaling_strategy_respected"] is True
    assert report["observations"]["phase27_51"]["raw_natural_passed"] == 1
    assert report["observations"]["phase27_52"]["passed"] == 5
    assert report["observations"]["phase27_53"]["passed"] == 2
    assert report["diagnosis"]["data_volume_alone_helped"] is False
    assert report["diagnosis"]["broad_diversity_regressed_vs_phase27_52"] is True
    assert report["diagnosis"]["direct_full_scaling_would_be_blind"] is True
    assert report["scaling_gates"]["evaluation_suite"]["passed"] is False
    assert report["scaling_gates"]["runtime_quality"]["passed"] is False
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["sf50m_full_training_allowed"] is False
    assert report["decisions"]["phase28_allowed"] is False
    assert report["decisions"]["sf50m_diagnostic_micro_probe_allowed"] is True
    assert report["decisions"]["diagnostic_micro_probe_is_not_runtime_scaling"] is True
