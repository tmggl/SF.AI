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


def test_phase27_55_sf50m_diagnostic_micro_probe_keeps_full_scaling_blocked() -> None:
    report = _report("phase27_55_sf50m_diagnostic_micro_probe_report.json")
    assert report["phase"] == "Phase 27.55"
    assert report["status"] == "FAILED_DIAGNOSTIC_CAPACITY_SIGNAL_KEEP_SF50M_FULL_BLOCKED"
    assert report["training_started"] is True
    assert report["training_scope"] == "bounded diagnostic micro-probe only; not full SF-50M scaling"
    assert report["progressive_scaling_respected"] is True
    assert report["models"]["sf-10m"]["summary"]["passed"] == 3
    assert report["models"]["sf-10m"]["summary"]["total"] == 20
    assert report["models"]["sf-50m"]["summary"]["passed"] == 4
    assert report["models"]["sf-50m"]["summary"]["total"] == 20
    assert report["comparison"]["delta_passed"] == 1
    assert report["comparison"]["diagnostic_capacity_signal"] is False
    assert report["comparison"]["strong_enough_for_full_sf50m"] is False
    assert report["runtime_switch_allowed"] is False
    assert report["sf50m_full_training_allowed"] is False
    assert report["sf50m_diagnostic_continuation_allowed"] is False
    assert report["phase28_allowed"] is False


def test_phase27_56_objective_format_tokenizer_diagnosis_identifies_blockers() -> None:
    report = _report("phase27_56_objective_format_tokenizer_diagnosis_report.json")
    assert report["phase"] == "Phase 27.56"
    assert report["status"] == "COMPLETED_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["capacity_result"]["delta_passed"] == 1
    assert report["capacity_result"]["capacity_alone_failed"] is True
    assert report["model_diagnosis"]["sf-50m"]["strict_passed"] == 4
    assert report["model_diagnosis"]["sf-50m"]["relaxed_semantic_passed"] == 9
    assert report["model_diagnosis"]["sf-50m"]["expected_terms_missing_count"] == 9
    assert report["model_diagnosis"]["sf-50m"]["response_family_confusion_count"] == 11
    assert report["tokenization_diagnosis"]["critical_aggressive_split_count"] == 9
    assert report["root_cause_assessment"]["capacity_is_primary_fix"] is False
    assert report["root_cause_assessment"]["objective_alignment_blocker"] is True
    assert report["root_cause_assessment"]["eval_overlap_rule_too_strict"] is True
    assert report["root_cause_assessment"]["tokenizer_saudi_social_terms_need_repair"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["sf50m_full_training_allowed"] is False
    assert report["decisions"]["next_training_allowed"] is False


def test_phase27_57_repair_pack_covers_tokenizer_eval_and_format() -> None:
    report = _report("phase27_57_tokenizer_eval_format_repair_pack_report.json")
    assert report["phase"] == "Phase 27.57"
    assert report["status"] == "COMPLETED_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_READY_FOR_RETRAINING_GATE"
    assert report["training_started"] is False
    assert report["runtime_switch_allowed"] is False
    assert report["protected_phrase_pack"]["total"] == 18
    assert len(report["protected_phrase_pack"]["covered_critical_terms"]) == 9
    assert report["protected_phrase_pack"]["missing_critical_terms"] == []
    assert report["semantic_alignment_pack"]["prompt_overlap_required"] is False
    assert report["semantic_alignment_pack"]["cross_family_blocking_enabled"] is True
    assert report["semantic_alignment_pack"]["ready_for_eval_replacement"] is True
    assert report["response_family_pack"]["forbidden_collapse_count"] == 5
    assert report["response_family_pack"]["ready_for_format_probe"] is True
    assert report["decisions"]["next_training_allowed"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["sf50m_full_training_allowed"] is False


def test_phase27_58_tokenizer_v7_probe_blocks_runtime_on_alignment_failure() -> None:
    report = _report("phase27_58_tokenizer_bounded_alignment_probe_report.json")
    assert report["phase"] == "Phase 27.58"
    assert report["status"] == "FAILED_TOKENIZER_V7_BOUNDED_ALIGNMENT_PROBE_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v7_phase27_58"
    assert report["tokenizer"]["sf_origin"] is True
    assert report["tokenizer"]["protected_terms_count"] == 53
    assert report["protected_phrase_behavior"]["phase27_57_max_pieces"] == 1
    assert report["protected_phrase_behavior"]["phase27_57_all_single_piece"] is True
    assert report["summary"]["passed"] == 4
    assert report["summary"]["total"] == 15
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 0
    assert report["summary"]["family_summary"]["followup"]["passed"] == 0
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["broader_canary_allowed"] is False


def test_phase27_59_bounded_alignment_repair_passes_but_keeps_runtime_blocked() -> None:
    report = _report("phase27_59_bounded_alignment_repair_report.json")
    assert report["phase"] == "Phase 27.59"
    assert report["status"] == "PASSED_BOUNDED_ALIGNMENT_REPAIR_READY_FOR_BROADER_CANARY_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v7_phase27_58"
    assert report["train_records"] == 2880
    assert report["repair_pair_count"] == 24
    assert report["summary"]["passed"] == 15
    assert report["summary"]["total"] == 15
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 3
    assert report["summary"]["family_summary"]["followup"]["passed"] == 3
    assert report["summary"]["family_summary"]["topic"]["passed"] == 3
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["broader_canary_allowed"] is True


def test_phase27_60_broader_canary_blocks_runtime_on_generalization_failure() -> None:
    report = _report("phase27_60_broader_natural_dialogue_canary_report.json")
    assert report["phase"] == "Phase 27.60"
    assert report["status"] == "FAILED_BROADER_NATURAL_DIALOGUE_CANARY_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["evaluation_only"] is True
    assert report["checkpoint_name"] == "sf-10m-step6400"
    assert report["summary"]["passed"] == 12
    assert report["summary"]["total"] == 30
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 5
    assert report["summary"]["family_summary"]["support"]["passed"] == 0
    assert report["summary"]["family_summary"]["topic"]["passed"] == 2
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["guarded_runtime_review_allowed"] is False


def test_phase27_61_broader_repair_improves_but_blocks_runtime() -> None:
    report = _report("phase27_61_broader_generalization_repair_report.json")
    assert report["phase"] == "Phase 27.61"
    assert report["status"] == "FAILED_BROADER_GENERALIZATION_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v7_phase27_58"
    assert report["summary"]["passed"] == 18
    assert report["summary"]["total"] == 30
    assert report["summary"]["family_summary"]["planning"]["passed"] == 6
    assert report["summary"]["family_summary"]["support"]["passed"] == 6
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 2
    assert report["summary"]["family_summary"]["topic"]["passed"] == 1
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["shadow_canary_allowed"] is False


def test_phase27_62_family_balance_regresses_and_blocks_runtime() -> None:
    report = _report("phase27_62_family_balance_repair_report.json")
    assert report["phase"] == "Phase 27.62"
    assert report["status"] == "FAILED_FAMILY_BALANCE_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v7_phase27_58"
    assert report["summary"]["passed"] == 10
    assert report["summary"]["total"] == 30
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 6
    assert report["summary"]["family_summary"]["support"]["passed"] == 0
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["fresh_shadow_canary_allowed"] is False


def test_phase27_63_interleaved_curriculum_improves_and_blocks_runtime() -> None:
    report = _report("phase27_63_interleaved_family_curriculum_report.json")
    assert report["phase"] == "Phase 27.63"
    assert report["status"] == "IMPROVED_INTERLEAVED_FAMILY_CURRICULUM_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v7_phase27_58"
    assert report["summary"]["passed"] == 26
    assert report["summary"]["total"] == 30
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 6
    assert report["summary"]["family_summary"]["planning"]["passed"] == 6
    assert report["summary"]["family_summary"]["support"]["passed"] == 6
    assert report["summary"]["family_summary"]["topic"]["passed"] == 3
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["fresh_shadow_canary_allowed"] is False


def test_phase27_64_topic_lexical_inspection_requires_tokenizer_v8() -> None:
    report = _report("phase27_64_topic_lexical_tokenizer_inspection_report.json")
    assert report["phase"] == "Phase 27.64"
    assert report["status"] == "COMPLETED_TOPIC_LEXICAL_INSPECTION_TOKENIZER_V8_REQUIRED_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["phase27_63_summary"]["passed"] == 26
    assert report["decisions"]["tokenizer_v8_required"] is True
    assert report["decisions"]["tokenizer_v8_probe_allowed_next"] is True
    assert report["decisions"]["lm_training_allowed_now"] is False
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["critical_latest_rows"]["التعاون"]["piece_count"] == 3
    assert report["critical_latest_rows"]["التعاون"]["protected_in_meta"] is False
    assert report["critical_latest_rows"]["الاحترام"]["piece_count"] == 4
    assert report["critical_latest_rows"]["الاحترام"]["protected_in_meta"] is False
    assert report["v7_regressed_from_v6"]["التعاون"] is True
    assert report["v7_regressed_from_v6"]["الاحترام"] is True


def test_phase27_65_tokenizer_v8_topic_probe_passes_without_lm_training() -> None:
    report = _report("phase27_65_tokenizer_v8_topic_probe_report.json")
    assert report["phase"] == "Phase 27.65"
    assert report["status"] == "PASSED_TOKENIZER_V8_TOPIC_PROBE_READY_FOR_BOUNDED_LM_TOPIC_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["training_scope"].startswith("tokenizer-only")
    assert report["lm_training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["summary"]["critical_terms_single_piece"] == 2
    assert report["summary"]["critical_terms_total"] == 2
    assert report["summary"]["topic_terms_single_piece"] == 8
    assert report["summary"]["topic_terms_total"] == 8
    assert report["summary"]["boundary_roundtrip_passed"] == 6
    assert report["summary"]["boundary_roundtrip_total"] == 6
    assert report["critical_rows"]["التعاون"]["piece_count"] == 1
    assert report["critical_rows"]["التعاون"]["protected_in_config"] is True
    assert report["critical_rows"]["الاحترام"]["piece_count"] == 1
    assert report["critical_rows"]["الاحترام"]["protected_in_config"] is True
    assert report["decisions"]["bounded_lm_topic_repair_allowed_next"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False


def test_phase27_66_v8_bounded_topic_repair_passes_and_blocks_runtime() -> None:
    report = _report("phase27_66_v8_bounded_topic_repair_report.json")
    assert report["phase"] == "Phase 27.66"
    assert report["status"] == "PASSED_V8_BOUNDED_TOPIC_REPAIR_READY_FOR_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["checkpoint_name"] == "sf-10m-step6200"
    assert report["summary"]["passed"] == 30
    assert report["summary"]["total"] == 30
    assert report["summary"]["pass_rate"] == 1.0
    assert report["summary"]["reason_counts"] == {"passed": 30}
    assert report["summary"]["family_summary"]["topic"]["passed"] == 6
    assert report["summary"]["family_summary"]["topic"]["total"] == 6
    assert report["decisions"]["fresh_shadow_canary_allowed"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False


def test_phase27_67_fresh_shadow_canary_blocks_runtime_after_failure() -> None:
    report = _report("phase27_67_fresh_shadow_canary_report.json")
    assert report["phase"] == "Phase 27.67"
    assert report["status"] == "FAILED_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["checkpoint_name"] == "sf-10m-step6200"
    assert report["summary"]["passed"] == 30
    assert report["summary"]["total"] == 50
    assert report["novelty_summary"]["novel"] == 50
    assert report["novelty_summary"]["total"] == 50
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 4
    assert report["summary"]["family_summary"]["followup"]["passed"] == 4
    assert report["summary"]["family_summary"]["topic"]["passed"] == 9
    assert report["decisions"]["guarded_runtime_review_allowed"] is False
    assert report["decisions"]["repair_required_before_runtime"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False


def test_phase27_68_shadow_failure_repair_passes_known_shadow_and_blocks_runtime() -> None:
    report = _report("phase27_68_shadow_failure_repair_report.json")
    assert report["phase"] == "Phase 27.68"
    assert report["status"] == "PASSED_SHADOW_FAILURE_REPAIR_READY_FOR_NEW_FRESH_SHADOW_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["checkpoint_name"] == "sf-10m-step5600"
    assert report["shadow_summary"]["passed"] == 50
    assert report["shadow_summary"]["total"] == 50
    assert report["regression_summary"]["passed"] == 30
    assert report["regression_summary"]["total"] == 30
    assert report["shadow_summary"]["family_summary"]["open_social"]["passed"] == 10
    assert report["shadow_summary"]["family_summary"]["support"]["passed"] == 10
    assert report["decisions"]["new_fresh_shadow_allowed"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False


def test_phase27_69_new_fresh_shadow_canary_is_strong_but_blocks_runtime() -> None:
    report = _report("phase27_69_new_fresh_shadow_canary_report.json")
    assert report["phase"] == "Phase 27.69"
    assert report["status"] == "STRONG_NEW_FRESH_SHADOW_CANARY_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["checkpoint_name"] == "sf-10m-step5600"
    assert report["novelty_summary"]["novel"] == 60
    assert report["novelty_summary"]["total"] == 60
    assert report["summary"]["passed"] == 56
    assert report["summary"]["total"] == 60
    assert report["summary"]["family_summary"]["open_social"]["passed"] == 8
    assert report["summary"]["family_summary"]["open_social"]["total"] == 12
    assert report["summary"]["family_summary"]["planning"]["passed"] == 12
    assert report["summary"]["family_summary"]["support"]["passed"] == 12
    assert report["summary"]["family_summary"]["topic"]["passed"] == 12
    assert report["decisions"]["guarded_live_api_review_allowed"] is False
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False


def test_phase27_70_open_social_repair_fails_and_blocks_runtime() -> None:
    report = _report("phase27_70_open_social_repair_report.json")
    assert report["phase"] == "Phase 27.70"
    assert report["status"] == "FAILED_OPEN_SOCIAL_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["init_checkpoint_name"] == "sf-10m-step5600"
    assert report["checkpoint_name"] == "sf-10m-step240"
    assert report["selected_repair_families"] == ["open_social"]
    assert report["phase27_69_summary"]["passed"] == 55
    assert report["phase27_69_summary"]["total"] == 60
    assert report["phase27_67_summary"]["passed"] == 48
    assert report["phase27_67_summary"]["total"] == 50
    assert report["phase27_60_summary"]["passed"] == 30
    assert report["phase27_60_summary"]["total"] == 30
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["repair_required_before_runtime"] is True


def test_phase27_71_candidate_selection_blocks_runtime_without_stable_candidate() -> None:
    report = _report("phase27_71_candidate_selection_report.json")
    assert report["phase"] == "Phase 27.71"
    assert report["status"] == "NO_STABLE_CANDIDATE_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["selected_candidate"]["name"] == "phase27_68_shadow_failure_repair"
    assert report["selected_candidate"]["score"] == 136
    assert report["selected_candidate"]["total"] == 140
    assert report["selected_candidate"]["phase27_69_summary"]["passed"] == 56
    assert report["selected_candidate"]["phase27_67_summary"]["passed"] == 50
    assert report["selected_candidate"]["phase27_60_summary"]["passed"] == 30
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["phase27_72_training_allowed"] is True


def test_phase27_72_stability_first_repair_improves_but_blocks_runtime() -> None:
    report = _report("phase27_72_stability_first_repair_report.json")
    assert report["phase"] == "Phase 27.72"
    assert report["status"] == "IMPROVED_STABILITY_FIRST_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["init_checkpoint_name"] == "sf-10m-step5600"
    assert report["checkpoint_name"] == "sf-10m-step64"
    assert report["phase27_69_summary"]["passed"] == 58
    assert report["phase27_69_summary"]["total"] == 60
    assert report["phase27_67_summary"]["passed"] == 50
    assert report["phase27_67_summary"]["total"] == 50
    assert report["phase27_60_summary"]["passed"] == 30
    assert report["phase27_60_summary"]["total"] == 30
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["live_runtime_review_allowed"] is False


def test_phase27_73_open_social_failure_inspection_blocks_runtime() -> None:
    report = _report("phase27_73_open_social_failure_inspection_report.json")
    assert report["phase"] == "Phase 27.73"
    assert report["status"] == "COMPLETED_OPEN_SOCIAL_FAILURE_INSPECTION_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["source_report"] == "artifacts/reports/phase27_72_stability_first_repair_report.json"
    assert report["source_total_passed"] == 138
    assert report["source_total"] == 140
    assert report["remaining_failures_count"] == 2
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["phase28_allowed"] is False
    assert report["decisions"]["guard_gap_fixed"] is True
    assert report["diagnosis_summary"]["remaining_semantic_failures_count"] == 1


def test_phase27_74_open_social_semantic_collapse_repair_blocks_runtime() -> None:
    report = _report("phase27_74_open_social_semantic_collapse_repair_report.json")
    assert report["phase"] == "Phase 27.74"
    assert report["status"] == "FAILED_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["init_checkpoint_name"] == "sf-10m-step64"
    selected = report["selected_candidate"]
    assert selected["candidate"] == "gentle_48"
    assert selected["phase27_69_summary"]["passed"] == 56
    assert selected["phase27_67_summary"]["passed"] == 49
    assert selected["phase27_60_summary"]["passed"] == 30
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["sf50m_allowed"] is False
    assert report["decisions"]["phase28_allowed"] is False
    assert report["decisions"]["repair_required_before_runtime"] is True


def test_phase27_75_open_social_strategy_inspection_requires_tokenizer_v9() -> None:
    report = _report("phase27_75_open_social_strategy_inspection_report.json")
    assert report["phase"] == "Phase 27.75"
    assert report["status"] == "COMPLETED_OPEN_SOCIAL_STRATEGY_INSPECTION_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v8_phase27_65"
    assert report["protected_pack"] == "resources/tokenization/protected_phrases_phase27_75.txt"
    assert report["protected_pack_active_in_rules"] is True
    assert report["failure_summary"]["total"] == 5
    assert report["failure_summary"]["by_family"] == {"open_social": 5}
    assert report["diagnosis"]["primary"] == "tokenizer_v8_open_social_boundary_fragments"
    assert report["diagnosis"]["bisalfah_decodes_as"] == "بس الفة"
    assert report["decisions"]["tokenizer_v9_required_next"] is True
    assert report["decisions"]["lm_repair_allowed_before_tokenizer_v9"] is False
    assert report["decisions"]["runtime_switch_allowed"] is False


def test_phase27_76_tokenizer_v9_open_social_boundary_probe_passes() -> None:
    report = _report("phase27_76_tokenizer_v9_open_social_boundary_probe_report.json")
    assert report["phase"] == "Phase 27.76"
    assert report["status"] == (
        "PASSED_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_READY_FOR_BOUNDED_LM_REPAIR_RUNTIME_BLOCKED"
    )
    assert report["training_started"] is True
    assert report["lm_training_started"] is False
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v9_phase27_76"
    assert report["summary"]["open_social_roundtrip_passed"] == 17
    assert report["summary"]["open_social_roundtrip_total"] == 17
    assert report["summary"]["protected_pack_single_piece"] == 15
    assert report["summary"]["protected_pack_total"] == 15
    assert report["summary"]["topic_single_piece"] == 8
    assert report["summary"]["critical_topic_protected"] == 2
    assert report["decisions"]["tokenizer_v9_passed"] is True
    assert report["decisions"]["bounded_lm_open_social_repair_allowed_next"] is True
    assert report["decisions"]["runtime_switch_allowed"] is False


def test_phase27_77_v9_bounded_open_social_lm_repair_blocks_runtime() -> None:
    report = _report("phase27_77_v9_bounded_open_social_lm_repair_report.json")
    assert report["phase"] == "Phase 27.77"
    assert report["status"] == "FAILED_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_RUNTIME_BLOCKED"
    assert report["training_started"] is True
    assert report["tokenizer"] == "artifacts/tokenizers/sf_bpe/v9_phase27_76"
    assert report["checkpoint_name"] == "sf-10m-step6200"
    assert report["phase27_69_summary"]["passed"] == 54
    assert report["phase27_69_summary"]["total"] == 60
    assert report["phase27_67_summary"]["passed"] == 45
    assert report["phase27_67_summary"]["total"] == 50
    assert report["phase27_60_summary"]["passed"] == 30
    assert report["phase27_60_summary"]["total"] == 30
    assert report["decisions"]["runtime_switch_allowed"] is False
    assert report["decisions"]["ui_open_allowed"] is False
    assert report["decisions"]["live_runtime_review_allowed"] is False
    assert report["decisions"]["repair_required_before_runtime"] is True


def test_phase27_78_engineering_root_cause_gate_blocks_training_runtime_and_scaling() -> None:
    report = _report("phase27_78_engineering_root_cause_gate_report.json")
    assert report["phase"] == "Phase 27.78"
    assert report["strategy"] == "Sovereign Practical Acceleration Strategy v2"
    assert report["gate"] == "ENGINEERING_ROOT_CAUSE_GATE"
    assert report["status"] == "PHASE27_78_ENGINEERING_DECISION_READY_TRAINING_BLOCKED_RUNTIME_BLOCKED"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert report["summary"]["failure_count"] == 11
    assert report["summary"]["failure_by_diagnosis"]["topic_semantic_substitution"] == 4
    assert report["summary"]["failure_by_diagnosis"]["followup_flow_instability"] == 3
    assert report["summary"]["failure_by_diagnosis"]["guard_false_positive_tanween"] == 2
    assert report["decision"]["decision_id"] == "PHASE27_78_ENGINEERING_DECISION"
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False
    assert report["decision"]["root_cause_weights_percent"]["family_mixing"] == 22
    assert report["decision"]["root_cause_weights_percent"]["capacity"] == 1


def test_phase27_79_repair_design_keeps_training_blocked_and_defines_next_gates() -> None:
    report = _report("phase27_79_objective_curriculum_decoding_design_report.json")
    assert report["phase"] == "Phase 27.79"
    assert report["strategy"] == "Sovereign Practical Acceleration Strategy v2"
    assert report["gate"] == "OBJECTIVE_CURRICULUM_DECODING_REPAIR_DESIGN"
    assert report["status"] == "PHASE27_79_REPAIR_DESIGN_READY_NEXT_GATE_ENCODING_NO_TRAINING"
    assert report["training_started"] is False
    assert report["tokenizer_training_started"] is False
    assert report["runtime_changed"] is False
    assert report["objective_design"]["name"] == "family_conditioned_prompt_to_answer_objective_v1"
    assert report["curriculum_design"]["name"] == "interleaved_family_curriculum_v2"
    assert report["decoding_design"]["name"] == "semantic_guarded_decoding_v1"
    assert "objective spec validator" in report["gate_design"]["must_implement"]
    assert report["decision"]["decision_id"] == "PHASE27_79_REPAIR_DESIGN_DECISION"
    assert report["decision"]["new_training_allowed"] is False
    assert report["decision"]["runtime_release_allowed"] is False
    assert report["decision"]["sf50m_justified_transition"] is False
    assert "Phase 27.80" in report["decision"]["next_phase"]
