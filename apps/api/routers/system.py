"""GET /system/status — phase status and high-level capability flags.

Phase 1 returns a static snapshot. From Phase 2 onward this will read
from the Capability Registry and live components.
"""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import APIRouter, Depends

from apps.api.dependencies import Settings, get_settings
from apps.api.schemas.system import (
    ComponentStatus,
    CorpusAuditResponse,
    CorpusIssueResponse,
    DomainGateResponse,
    Phase12ReadinessResponse,
    Phase19ReadinessResponse,
    Phase20GatesResponse,
    Phase22CollectionPlanResponse,
    Phase22CompletionGateResponse,
    Phase22NextBatchBriefResponse,
    Phase22ReadinessResponse,
    Phase22ReviewExportItemResponse,
    Phase22ReviewIntakeResponse,
    Phase26ReadinessResponse,
    Phase27DialogueEvalResponse,
    SourceInventoryItemResponse,
    SourceInventoryResponse,
    SystemStatusResponse,
)
from sf_ai.core.activation import build_phase20_activation_gates
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.datasets.phase22_readiness import (
    build_phase22_collection_plan,
    build_phase22_completion_gate,
    build_phase22_next_batch_brief,
    build_phase22_readiness_decision,
)
from sf_ai.datasets.phase22_review_intake import build_phase22_review_intake_report
from sf_ai.datasets.source_inventory import build_source_inventory
from sf_ai.evaluation import run_phase27_dialogue_eval
from sf_ai.training.phase12_readiness import build_phase12_readiness_decision
from sf_ai.training.phase19_readiness import build_phase19_readiness_decision
from sf_ai.training.phase23_tokenizer import build_phase23_tokenizer_audit
from sf_ai.training.phase26_readiness import build_phase26_scaling_decision

router = APIRouter(prefix="/system", tags=["system"])
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.get("/status", response_model=SystemStatusResponse)
def system_status(settings: SettingsDep) -> SystemStatusResponse:
    saudi_seed_enabled = (
        os.getenv("ENABLE_SAUDI_SEED_V1_LEXICON", "").strip().lower()
        in {"1", "true", "yes", "on"}
    )
    return SystemStatusResponse(
        project=settings.project_name,
        env=settings.env,
        current_phase="Phase 27.113 — Permissive Lexical Alternatives Intake Gate",
        current_phase_status=(
            "phase27_113_permissive_lexical_alternatives_ready_no_import"
        ),
        next_phase="Phase 27.114 — Arabic Ontology/Synonyms Source Cards and License Matrix, no training",
        sovereign=True,
        uses_external_llm=False,
        uses_pretrained_weights=False,
        uses_pretrained_embeddings=False,
        uses_pretrained_tokenizer=False,
        components=[
            ComponentStatus(name="api", status="active"),
            ComponentStatus(name="orchestrator", status="active", phase="Phase 2"),
            ComponentStatus(name="router", status="active", phase="Phase 2"),
            ComponentStatus(name="semantic_explorer", status="active", phase="Phase 2"),
            ComponentStatus(name="capability_registry", status="active", phase="Phase 2"),
            ComponentStatus(name="response_composer", status="active", phase="Phase 2"),
            ComponentStatus(name="planner", status="skeleton_only", phase="Phase 2"),
            ComponentStatus(name="nlp_layer", status="active", phase="Phase 3"),
            ComponentStatus(name="arabic_normalizer", status="active", phase="Phase 3"),
            ComponentStatus(name="arabizi_mapper", status="active", phase="Phase 3"),
            ComponentStatus(name="dialect_mapper", status="active", phase="Phase 3"),
            ComponentStatus(name="typo_corrector", status="active", phase="Phase 3"),
            ComponentStatus(name="intent_detector", status="active", phase="Phase 3"),
            ComponentStatus(name="safety_scanner", status="active", phase="Phase 3"),
            ComponentStatus(name="chat_module", status="active", phase="Phase 4"),
            ComponentStatus(name="conversation_state", status="active", phase="Phase 4"),
            ComponentStatus(name="dataset_pipeline", status="active", phase="Phase 5"),
            ComponentStatus(name="dataset_validators", status="active", phase="Phase 5"),
            ComponentStatus(name="dataset_cleaners", status="active", phase="Phase 5"),
            ComponentStatus(name="dataset_loaders", status="active", phase="Phase 5"),
            ComponentStatus(name="tokenizer", status="active", phase="Phase 5.5"),
            ComponentStatus(name="bpe_tokenizer", status="active", phase="Phase 5.5"),
            ComponentStatus(name="device_manager", status="active", phase="Phase 5.5"),
            ComponentStatus(name="checkpoint_manager", status="active", phase="Phase 5.5"),
            ComponentStatus(name="training_config", status="active", phase="Phase 5.5"),
            ComponentStatus(name="native_model", status="active", phase="Phase 6"),
            ComponentStatus(name="tiny_transformer", status="active", phase="Phase 6"),
            ComponentStatus(name="train_tiny_lm", status="active", phase="Phase 6"),
            ComponentStatus(name="evaluate_tiny_lm", status="active", phase="Phase 6"),
            ComponentStatus(name="web_research", status="ready_offline", phase="Phase 7"),
            ComponentStatus(name="crawler_base", status="active", phase="Phase 7"),
            ComponentStatus(name="robots_policy", status="active", phase="Phase 7"),
            ComponentStatus(name="rate_limiter", status="active", phase="Phase 7"),
            ComponentStatus(name="article_extractor", status="active", phase="Phase 7"),
            ComponentStatus(name="rule_based_summarizer", status="active", phase="Phase 7"),
            ComponentStatus(name="citation_builder", status="active", phase="Phase 7"),
            ComponentStatus(name="research_module", status="ready_offline", phase="Phase 7"),
            ComponentStatus(name="web_module", status="ready_offline", phase="Phase 7"),
            ComponentStatus(name="long_term_memory", status="active", phase="Phase 8"),
            ComponentStatus(name="sparse_store", status="active", phase="Phase 8"),
            ComponentStatus(name="hashing_vector_store", status="active", phase="Phase 8"),
            ComponentStatus(name="hybrid_retriever", status="active", phase="Phase 8"),
            ComponentStatus(
                name="saudi_seed_v1_lexicon",
                status="active" if saudi_seed_enabled else "ready_offline",
                phase="Phase 3.6",
            ),
            ComponentStatus(name="chat_ui", status="active", phase="Phase 9"),
            ComponentStatus(
                name="phase24_sf10m_v0_2",
                status="completed_runtime_blocked",
                phase="Phase 24",
            ),
            ComponentStatus(
                name="phase25_generation_canary",
                status="active_runtime_guard",
                phase="Phase 25",
            ),
            ComponentStatus(
                name="phase26_readiness",
                status="completed_training_blocked",
                phase="Phase 26",
            ),
            ComponentStatus(
                name="phase27_dialogue_eval_v2",
                status="completed_with_blockers",
                phase="Phase 27",
            ),
            ComponentStatus(
                name="phase27_7_fixed_dialogue_split",
                status="active_quality_gate",
                phase="Phase 27.7",
            ),
            ComponentStatus(
                name="phase27_7_prompt_aware_canary",
                status="active_runtime_guard",
                phase="Phase 27.7",
            ),
            ComponentStatus(
                name="phase27_8_sf10m_v0_6",
                status="completed_runtime_blocked",
                phase="Phase 27.8",
            ),
            ComponentStatus(
                name="phase27_9_generation_quality_harness",
                status="active_runtime_gate",
                phase="Phase 27.9",
            ),
            ComponentStatus(
                name="phase27_10_short_response_repair",
                status="completed_runtime_blocked",
                phase="Phase 27.10",
            ),
            ComponentStatus(
                name="phase27_11_objective_probe",
                status="completed_stop_boundary_blocked",
                phase="Phase 27.11",
            ),
            ComponentStatus(
                name="phase27_12_assistant_eos_repair",
                status="completed_partial_runtime_blocked",
                phase="Phase 27.12",
            ),
            ComponentStatus(
                name="phase27_13_sf10m_v0_8_boundary_eos_training",
                status="completed_eval_improved_runtime_blocked",
                phase="Phase 27.13",
            ),
            ComponentStatus(
                name="phase27_14_sovereign_quality_tooling",
                status="completed_no_training",
                phase="Phase 27.14",
            ),
            ComponentStatus(
                name="phase27_15_social_lexical_curriculum",
                status="completed_eval_improved_runtime_blocked",
                phase="Phase 27.15",
            ),
            ComponentStatus(
                name="phase27_16_prompt_to_answer_objective",
                status="completed_objective_repair_runtime_blocked",
                phase="Phase 27.16",
            ),
            ComponentStatus(
                name="phase27_17_prompt_answer_micro_probe",
                status="completed_breakthrough_runtime_blocked",
                phase="Phase 27.17",
            ),
            ComponentStatus(
                name="phase27_18_tokenization_decoding_hygiene",
                status="completed_hygiene_audit_runtime_blocked",
                phase="Phase 27.18",
            ),
            ComponentStatus(
                name="phase27_19_hygiene_repair_probe",
                status="completed_repair_probe_runtime_blocked",
                phase="Phase 27.19",
            ),
            ComponentStatus(
                name="phase27_20_tokenizer_protected_phrase_strategy",
                status="completed_ready_for_tokenizer_v3_runtime_blocked",
                phase="Phase 27.20",
            ),
            ComponentStatus(
                name="phase27_21_tokenizer_v3_micro_probe",
                status="completed_micro_probe_failed_runtime_blocked",
                phase="Phase 27.21",
            ),
            ComponentStatus(
                name="phase27_22_spacing_boundary_repair",
                status="completed_partial_repair_runtime_blocked",
                phase="Phase 27.22",
            ),
            ComponentStatus(
                name="phase27_23_semantic_lexical_repair",
                status="completed_partial_repair_runtime_blocked",
                phase="Phase 27.23",
            ),
            ComponentStatus(
                name="phase27_24_minimal_lexical_stabilization",
                status="completed_micro_probe_passed_runtime_blocked",
                phase="Phase 27.24",
            ),
            ComponentStatus(
                name="phase27_25_heldout_generation_canary",
                status="completed_failed_runtime_blocked",
                phase="Phase 27.25",
            ),
            ComponentStatus(
                name="phase27_26_heldout_objective_repair",
                status="completed_partial_runtime_blocked",
                phase="Phase 27.26",
            ),
            ComponentStatus(
                name="phase27_27_broader_heldout_repair",
                status="completed_old_heldout_passed_shadow_blocked",
                phase="Phase 27.27",
            ),
            ComponentStatus(
                name="phase27_28_intent_conditioned_repair",
                status="completed_intent_conditioning_partial_runtime_blocked",
                phase="Phase 27.28",
            ),
            ComponentStatus(
                name="phase27_29_topic_conditioned_definition_repair",
                status="completed_topic_conditioning_leakage_blocked",
                phase="Phase 27.29",
            ),
            ComponentStatus(
                name="phase27_30_fresh_mixed_shadow_canary",
                status="completed_16_of_18_runtime_blocked",
                phase="Phase 27.30",
            ),
            ComponentStatus(
                name="phase27_31_natural_intent_topic_dataset",
                status="completed_partial_runtime_blocked",
                phase="Phase 27.31",
            ),
            ComponentStatus(
                name="phase27_32_balanced_natural_calibration",
                status="completed_partial_runtime_blocked",
                phase="Phase 27.32",
            ),
            ComponentStatus(
                name="phase27_33_advice_micro_stabilization",
                status="completed_all_generation_gates_passed_trial_design_ready",
                phase="Phase 27.33",
            ),
            ComponentStatus(
                name="phase27_34_guarded_runtime_trial",
                status="completed_ready_for_ui_test",
                phase="Phase 27.34",
            ),
            ComponentStatus(
                name="phase27_35_live_ui_trial_observations",
                status="completed_ready_for_user_observation",
                phase="Phase 27.35",
            ),
            ComponentStatus(
                name="phase27_36_live_ui_triage",
                status="completed_quality_floor_active",
                phase="Phase 27.36",
            ),
            ComponentStatus(
                name="phase27_37_supported_topic_expansion",
                status="completed_quality_gated",
                phase="Phase 27.37",
            ),
            ComponentStatus(
                name="phase27_38_targeted_topic_curriculum_probe",
                status="completed_partial_keep_current_runtime",
                phase="Phase 27.38",
            ),
            ComponentStatus(
                name="phase27_39_topic_isolation_repair",
                status="completed_partial_keep_current_runtime",
                phase="Phase 27.39",
            ),
            ComponentStatus(
                name="phase27_40_tokenizer_context_repair",
                status="completed_candidate_opened_in_guarded_trial",
                phase="Phase 27.40",
            ),
            ComponentStatus(
                name="phase27_41_guarded_runtime_switch",
                status="completed_candidate_opened_in_guarded_trial",
                phase="Phase 27.41",
            ),
            ComponentStatus(
                name="phase27_42_live_ui_broader_probes",
                status="completed_live_ui_broader_probes_guarded",
                phase="Phase 27.42",
            ),
            ComponentStatus(
                name="phase27_43_guarded_data_backed_expansion",
                status="completed_partial_keep_phase27_40_runtime",
                phase="Phase 27.43",
            ),
            ComponentStatus(
                name="phase27_44_tokenizer_curriculum_repair",
                status="completed_partial_keep_phase27_40_runtime",
                phase="Phase 27.44",
            ),
            ComponentStatus(
                name="phase27_45_semantic_topic_balance_repair",
                status="completed_partial_keep_phase27_40_runtime",
                phase="Phase 27.45",
            ),
            ComponentStatus(
                name="phase27_46_core_dialogue_stabilization",
                status="completed_partial_keep_phase27_40_runtime",
                phase="Phase 27.46",
            ),
            ComponentStatus(
                name="phase27_47_new_topic_conditioning_repair",
                status="completed_ready_for_guarded_switch",
                phase="Phase 27.47",
            ),
            ComponentStatus(
                name="phase27_48_guarded_runtime_switch",
                status="completed_guarded_runtime_switch_phase27_47",
                phase="Phase 27.48",
            ),
            ComponentStatus(
                name="phase27_49_broader_live_ui_probes",
                status="completed_broader_live_ui_probes_phase27_47",
                phase="Phase 27.49",
            ),
            ComponentStatus(
                name="phase27_50_generator_only_ui_gate",
                status="completed_generator_only_ui_gate",
                phase="Phase 27.50",
            ),
            ComponentStatus(
                name="phase27_51_open_dialogue_generalization_audit",
                status="completed_failed_training_required",
                phase="Phase 27.51",
            ),
            ComponentStatus(
                name="phase27_52_natural_dialogue_objective_repair",
                status="completed_partial_keep_phase27_47_runtime",
                phase="Phase 27.52",
            ),
            ComponentStatus(
                name="phase27_53_natural_dialogue_diversity_expansion",
                status="completed_partial_keep_phase27_47_runtime",
                phase="Phase 27.53",
            ),
            ComponentStatus(
                name="phase27_54_capacity_objectivity_gate",
                status="completed_full_scaling_blocked_diagnostic_micro_probe_allowed",
                phase="Phase 27.54",
            ),
            ComponentStatus(
                name="phase27_55_sf50m_diagnostic_micro_probe",
                status="completed_diagnostic_capacity_signal_failed_full_sf50m_blocked",
                phase="Phase 27.55",
            ),
            ComponentStatus(
                name="phase27_56_objective_format_tokenizer_diagnosis",
                status="completed_objective_format_tokenizer_diagnosis_runtime_blocked",
                phase="Phase 27.56",
            ),
            ComponentStatus(
                name="phase27_57_tokenizer_eval_format_repair_pack",
                status="completed_repair_pack_ready_for_bounded_retraining_gate",
                phase="Phase 27.57",
            ),
            ComponentStatus(
                name="phase27_58_tokenizer_bounded_alignment_probe",
                status="failed_bounded_alignment_probe_runtime_blocked",
                phase="Phase 27.58",
            ),
            ComponentStatus(
                name="phase27_59_bounded_alignment_repair",
                status="passed_bounded_alignment_repair_runtime_blocked",
                phase="Phase 27.59",
            ),
            ComponentStatus(
                name="phase27_60_broader_natural_dialogue_canary",
                status="failed_broader_natural_dialogue_canary_runtime_blocked",
                phase="Phase 27.60",
            ),
            ComponentStatus(
                name="phase27_61_broader_generalization_repair",
                status="failed_broader_generalization_repair_runtime_blocked",
                phase="Phase 27.61",
            ),
            ComponentStatus(
                name="phase27_62_family_balance_repair",
                status="failed_family_balance_repair_runtime_blocked",
                phase="Phase 27.62",
            ),
            ComponentStatus(
                name="phase27_63_interleaved_family_curriculum",
                status="improved_interleaved_family_curriculum_runtime_blocked",
                phase="Phase 27.63",
            ),
            ComponentStatus(
                name="phase27_64_topic_lexical_tokenizer_inspection",
                status="completed_topic_lexical_inspection_tokenizer_v8_required_runtime_blocked",
                phase="Phase 27.64",
            ),
            ComponentStatus(
                name="phase27_65_tokenizer_v8_topic_probe",
                status="passed_tokenizer_v8_topic_probe_ready_for_bounded_lm_topic_repair_runtime_blocked",
                phase="Phase 27.65",
            ),
            ComponentStatus(
                name="phase27_66_v8_bounded_topic_repair",
                status="passed_v8_bounded_topic_repair_ready_for_fresh_shadow_canary_runtime_blocked",
                phase="Phase 27.66",
            ),
            ComponentStatus(
                name="phase27_67_fresh_shadow_canary",
                status="failed_fresh_shadow_canary_runtime_blocked",
                phase="Phase 27.67",
            ),
            ComponentStatus(
                name="phase27_68_shadow_failure_repair",
                status="passed_shadow_failure_repair_ready_for_new_fresh_shadow_runtime_blocked",
                phase="Phase 27.68",
            ),
            ComponentStatus(
                name="phase27_69_new_fresh_shadow_canary",
                status="strong_new_fresh_shadow_canary_runtime_blocked",
                phase="Phase 27.69",
            ),
            ComponentStatus(
                name="phase27_70_open_social_repair",
                status="failed_open_social_repair_runtime_blocked",
                phase="Phase 27.70",
            ),
            ComponentStatus(
                name="phase27_71_candidate_selection",
                status="no_stable_candidate_runtime_blocked",
                phase="Phase 27.71",
            ),
            ComponentStatus(
                name="phase27_72_stability_first_repair",
                status="improved_stability_first_repair_runtime_blocked",
                phase="Phase 27.72",
            ),
            ComponentStatus(
                name="phase27_73_open_social_failure_inspection",
                status="completed_open_social_failure_inspection_runtime_blocked",
                phase="Phase 27.73",
            ),
            ComponentStatus(
                name="phase27_74_open_social_semantic_collapse_repair",
                status="failed_open_social_semantic_collapse_repair_runtime_blocked",
                phase="Phase 27.74",
            ),
            ComponentStatus(
                name="phase27_75_open_social_strategy_inspection",
                status="completed_open_social_strategy_inspection_runtime_blocked",
                phase="Phase 27.75",
            ),
            ComponentStatus(
                name="phase27_76_tokenizer_v9_open_social_boundary_probe",
                status="passed_tokenizer_v9_open_social_boundary_probe_runtime_blocked",
                phase="Phase 27.76",
            ),
            ComponentStatus(
                name="phase27_77_v9_bounded_open_social_lm_repair",
                status="failed_v9_bounded_open_social_lm_repair_runtime_blocked",
                phase="Phase 27.77",
            ),
            ComponentStatus(
                name="phase27_78_engineering_root_cause_gate",
                status="phase27_78_engineering_decision_training_blocked",
                phase="Phase 27.78",
            ),
            ComponentStatus(
                name="phase27_79_objective_curriculum_decoding_design",
                status="phase27_79_objective_curriculum_decoding_plan_training_blocked",
                phase="Phase 27.79",
            ),
            ComponentStatus(
                name="phase27_80_repair_gate_validation",
                status="gates_passed_after_family_balance_remediation",
                phase="Phase 27.80",
            ),
            ComponentStatus(
                name="phase27_80_bounded_family_conditioned_repair_gate",
                status="gates_passed_bounded_training_allowed_next",
                phase="Phase 27.80",
            ),
            ComponentStatus(
                name="phase27_81_bounded_family_conditioned_repair_training",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.81",
            ),
            ComponentStatus(
                name="phase27_81_balanced_family_pack",
                status="authored_2500_gold_records_gates_passed",
                phase="Phase 27.81",
            ),
            ComponentStatus(
                name="phase27_82_family_conditioned_training_decision",
                status="allows_phase27_83_bounded_training_no_runtime",
                phase="Phase 27.82",
            ),
            ComponentStatus(
                name="phase27_83_family_conditioned_repair_training",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.83",
            ),
            ComponentStatus(
                name="phase27_84_objective_curriculum_failure_diagnosis",
                status="diagnosed_family_signal_missing_no_training",
                phase="Phase 27.84",
            ),
            ComponentStatus(
                name="phase27_85_explicit_family_conditioning_design",
                status="renderer_gate_allowed_no_training",
                phase="Phase 27.85",
            ),
            ComponentStatus(
                name="phase27_86_family_conditioning_renderer_gate",
                status="renderer_gate_passed_training_allowed_next_no_runtime",
                phase="Phase 27.86",
            ),
            ComponentStatus(
                name="phase27_87_bounded_family_conditioned_repair",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.87",
            ),
            ComponentStatus(
                name="phase27_88_family_conditioned_result_diagnosis",
                status="diagnosed_sequential_curriculum_collapse_no_training",
                phase="Phase 27.88",
            ),
            ComponentStatus(
                name="phase27_89_stratified_round_robin_sampler_gate",
                status="passed_training_allowed_next_runtime_blocked",
                phase="Phase 27.89",
            ),
            ComponentStatus(
                name="phase27_90_bounded_round_robin_repair",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.90",
            ),
            ComponentStatus(
                name="phase27_91_round_robin_result_diagnosis",
                status="diagnosed_topic_collapse_no_training",
                phase="Phase 27.91",
            ),
            ComponentStatus(
                name="phase27_92_topic_objective_repair_design",
                status="design_ready_no_training",
                phase="Phase 27.92",
            ),
            ComponentStatus(
                name="phase27_93_topic_objective_gate_encoding",
                status="gate_passed_training_allowed_next_after_data_pack",
                phase="Phase 27.93",
            ),
            ComponentStatus(
                name="phase27_94_topic_objective_data_pack",
                status="data_pack_ready_for_bounded_training_no_runtime",
                phase="Phase 27.94",
            ),
            ComponentStatus(
                name="phase27_95_bounded_topic_objective_repair",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.95",
            ),
            ComponentStatus(
                name="phase27_96_topic_objective_result_diagnosis",
                status="diagnosed_topic_variable_binding_failure_no_training",
                phase="Phase 27.96",
            ),
            ComponentStatus(
                name="phase27_97_topic_variable_binding_objective_design",
                status="topic_binding_objective_design_ready_no_training",
                phase="Phase 27.97",
            ),
            ComponentStatus(
                name="phase27_98_topic_binding_gate_encoding",
                status="passed_training_allowed_next_no_runtime",
                phase="Phase 27.98",
            ),
            ComponentStatus(
                name="phase27_99_topic_metadata_copy_anchor_repair",
                status="done_training_allowed_next_no_runtime",
                phase="Phase 27.99",
            ),
            ComponentStatus(
                name="phase27_100_bounded_topic_binding_repair",
                status="trained_runtime_blocked_diagnosis_required",
                phase="Phase 27.100",
            ),
            ComponentStatus(
                name="phase27_101_topic_binding_result_diagnosis",
                status="diagnosed_metric_blind_spot_no_training",
                phase="Phase 27.101",
            ),
            ComponentStatus(
                name="phase27_102_topic_prototype_contrastive_gate",
                status="gate_encoded_curriculum_pack_allowed_no_training",
                phase="Phase 27.102",
            ),
            ComponentStatus(
                name="phase27_103_topic_prototype_contrastive_curriculum_pack",
                status="ready_for_bounded_training_no_runtime",
                phase="Phase 27.103",
            ),
            ComponentStatus(
                name="phase27_104_bounded_topic_prototype_contrastive_repair",
                status="trained_topic_clean_all_family_regressed_runtime_blocked",
                phase="Phase 27.104",
            ),
            ComponentStatus(
                name="phase27_105_raw_ui_lab_result_diagnosis",
                status="diagnosed_raw_ui_lab_failures_no_training",
                phase="Phase 27.105",
            ),
            ComponentStatus(
                name="phase27_106_social_subfamily_topic_variant_design",
                status="design_ready_gate_encoding_no_training",
                phase="Phase 27.106",
            ),
            ComponentStatus(
                name="phase27_107_social_subfamily_topic_variant_gate",
                status="gate_passed_data_pack_allowed_no_training",
                phase="Phase 27.107",
            ),
            ComponentStatus(
                name="phase27_108_social_subfamily_topic_variant_data_pack",
                status="data_pack_ready_for_audit_no_training",
                phase="Phase 27.108",
            ),
            ComponentStatus(
                name="phase27_109_free_linguistic_resource_intake_gate",
                status="free_resource_intake_ready_no_training",
                phase="Phase 27.109",
            ),
            ComponentStatus(
                name="phase27_110_licensed_ingestion_design",
                status="licensed_ingestion_design_ready_no_training",
                phase="Phase 27.110",
            ),
            ComponentStatus(
                name="phase27_111_qabas_lexicon_bootstrap_design",
                status="qabas_bootstrap_design_ready_import_blocked",
                phase="Phase 27.111",
            ),
            ComponentStatus(
                name="phase27_112_qabas_primary_license_resolution_gate",
                status="qabas_reference_only_import_blocked",
                phase="Phase 27.112",
            ),
            ComponentStatus(
                name="phase27_113_permissive_lexical_alternatives_intake_gate",
                status="permissive_lexical_alternatives_ready_no_import",
                phase="Phase 27.113",
            ),
            ComponentStatus(name="coding_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="data_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="files_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="legal_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="medical_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="finance_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="education_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="religion_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="social_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="productivity_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="writing_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="translation_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="image_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="audio_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="security_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="business_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="ecommerce_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="corpus_governance", status="active", phase="Phase 11"),
            ComponentStatus(name="training_corpus", status="active", phase="Phase 22"),
            ComponentStatus(name="phase12_corpus_preflight", status="active", phase="Phase 12"),
            ComponentStatus(name="native_generator", status="ready_offline", phase="Phase 15"),
            ComponentStatus(name="generation_policy", status="active", phase="Phase 15"),
            ComponentStatus(name="evaluation_harness", status="active", phase="Phase 16"),
            ComponentStatus(name="rag", status="active", phase="Phase 8"),
            ComponentStatus(name="chat_rag_bridge", status="ready_offline", phase="Phase 17"),
            ComponentStatus(name="dialogue_batch_preparation", status="active", phase="Phase 18"),
            ComponentStatus(name="chat_review_export", status="internal_only", phase="Phase 18"),
            ComponentStatus(name="chat_review_local_save", status="internal_only", phase="Phase 22"),
            ComponentStatus(name="phase19_readiness", status="active", phase="Phase 19"),
            ComponentStatus(name="domain_activation_gates", status="active", phase="Phase 20"),
            ComponentStatus(name="generative_roadmap", status="active", phase="Phase 21"),
            ComponentStatus(name="phase22_readiness", status="active", phase="Phase 22"),
            ComponentStatus(name="phase22_collection_plan", status="active", phase="Phase 22"),
            ComponentStatus(name="phase22_next_batch", status="active", phase="Phase 22"),
            ComponentStatus(name="phase22_completion_gate", status="active", phase="Phase 22"),
            ComponentStatus(name="phase22_review_intake", status="active", phase="Phase 22"),
            ComponentStatus(name="phase22_dialogue_quality_gate", status="active", phase="Phase 22"),
            ComponentStatus(name="phase23_tokenizer_v2", status="active", phase="Phase 23"),
            ComponentStatus(name="phase23_tokenizer_audit", status="active", phase="Phase 23"),
        ],
    )


@router.get("/corpus-audit", response_model=CorpusAuditResponse)
def corpus_audit() -> CorpusAuditResponse:
    """Live Phase 12 preflight status for the local chat JSONL corpus."""
    corpus = "data/corpus/chat/jsonl"
    report = audit_jsonl_directory_for_training(corpus)
    ready = report.error_count == 0 and report.training_ready > 0

    return CorpusAuditResponse(
        corpus=corpus,
        status=(
            "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
            if ready
            else "NOT_READY_FOR_TRAINING"
        ),
        total_records=report.total_records,
        training_ready=report.training_ready,
        issue_count=report.error_count,
        dialect_counts=report.dialect_counts,
        quality_counts=report.quality_counts,
        source_counts=report.source_counts,
        issues=[
            CorpusIssueResponse(
                line_number=issue.line_number,
                kind=issue.kind,
                message=issue.message,
                snippet=issue.snippet,
            )
            for issue in report.issues[:50]
        ],
    )


@router.get("/source-inventory", response_model=SourceInventoryResponse)
def source_inventory() -> SourceInventoryResponse:
    """Comprehensive local data/reference source inventory."""
    report = build_source_inventory()
    return SourceInventoryResponse(
        phase12_status=report.phase12_status,
        source_count=report.source_count,
        chat_training_records=report.chat_training_records,
        local_reference_records=report.local_reference_records,
        blockers=list(report.blockers),
        sources=[
            SourceInventoryItemResponse(
                name=item.name,
                path=item.path,
                kind=item.kind,
                exists=item.exists,
                records=item.records,
                valid_json_records=item.valid_json_records,
                private_or_ignored=item.private_or_ignored,
                tracked_payload_allowed=item.tracked_payload_allowed,
                phase12_tokenizer_candidate=item.phase12_tokenizer_candidate,
                phase13_lm_candidate=item.phase13_lm_candidate,
                needs_conversion=item.needs_conversion,
                needs_governance_audit=item.needs_governance_audit,
                status=item.status,
                action_required=item.action_required,
                notes=list(item.notes),
                stats=item.stats,
            )
            for item in report.sources
        ],
    )


@router.get("/phase12-readiness", response_model=Phase12ReadinessResponse)
def phase12_readiness() -> Phase12ReadinessResponse:
    """One-stop Phase 12 decision endpoint.

    This is deliberately read-only. It reports readiness and the permission
    boundary, but it never starts tokenizer training and never writes artifacts.
    """
    decision = build_phase12_readiness_decision()

    return Phase12ReadinessResponse(
        phase=decision.phase,
        preflight_pass=decision.preflight_pass,
        can_train_now=decision.can_train_now,
        training_permission_granted=decision.training_permission_granted,
        required_permission_phrase=decision.required_permission_phrase,
        required_confirmation_flag=decision.required_confirmation_flag,
        action=decision.action,
        corpus_status=decision.corpus_status,
        corpus_training_ready=decision.corpus_training_ready,
        corpus_issue_count=decision.corpus_issue_count,
        corpus_dialect_counts=decision.corpus_dialect_counts,
        required_dialects=list(decision.required_dialects),
        missing_required_dialects=list(decision.missing_required_dialects),
        language_balance_status=decision.language_balance_status,
        tokenization_status=decision.tokenization_status,
        protected_terms_total=decision.protected_terms_total,
        protected_terms_covered=decision.protected_terms_covered,
        protected_terms_coverage_ratio=decision.protected_terms_coverage_ratio,
        source_count=decision.source_count,
        local_reference_records=decision.local_reference_records,
        artifacts_present=list(decision.artifacts_present),
        required_command_after_permission=decision.required_command_after_permission,
        notes=list(decision.notes),
    )


@router.get("/phase19-readiness", response_model=Phase19ReadinessResponse)
def phase19_readiness() -> Phase19ReadinessResponse:
    """Read-only Phase 19 decision before any SF-50M candidate training."""
    decision = build_phase19_readiness_decision()
    return Phase19ReadinessResponse(
        phase=decision.phase,
        status=decision.status,
        can_start_training=decision.can_start_training,
        lab_experiment_allowed=decision.lab_experiment_allowed,
        corpus_path=decision.corpus_path,
        training_records=decision.training_records,
        min_training_records=decision.min_training_records,
        corpus_issue_count=decision.corpus_issue_count,
        dialect_counts=decision.dialect_counts,
        missing_required_dialects=list(decision.missing_required_dialects),
        tokenizer_ready=decision.tokenizer_ready,
        sf10m_checkpoint_ready=decision.sf10m_checkpoint_ready,
        phase16_eval_passed=decision.phase16_eval_passed,
        phase16_runtime_activation_allowed=decision.phase16_runtime_activation_allowed,
        target_model=decision.target_model,
        target_context=decision.target_context,
        target_d_model=decision.target_d_model,
        target_layers=decision.target_layers,
        target_heads=decision.target_heads,
        device=decision.device,
        action=decision.action,
        recommended_commands=list(decision.recommended_commands),
        blockers=list(decision.blockers),
        notes=list(decision.notes),
    )


@router.get("/phase26-readiness", response_model=Phase26ReadinessResponse)
def phase26_readiness() -> Phase26ReadinessResponse:
    """Read-only Phase 26 scaling gate before any SF-50M training."""
    decision = build_phase26_scaling_decision()
    return Phase26ReadinessResponse(**decision.to_json())


@router.get("/phase27-dialogue-eval", response_model=Phase27DialogueEvalResponse)
def phase27_dialogue_eval() -> Phase27DialogueEvalResponse:
    """Read-only Phase 27 multi-turn dialogue eval and corpus expansion plan."""
    report = run_phase27_dialogue_eval()
    return Phase27DialogueEvalResponse(**report.to_json())


@router.get("/phase20-gates", response_model=Phase20GatesResponse)
def phase20_gates() -> Phase20GatesResponse:
    """Read-only Phase 20 decision for skeleton domain activation."""
    decision = build_phase20_activation_gates()
    return Phase20GatesResponse(
        phase=decision.phase,
        status=decision.status,
        language_track=list(decision.language_track),
        lexicon_track=decision.lexicon_track,
        total_domains=decision.total_domains,
        active_domains=list(decision.active_domains),
        ready_offline_domains=list(decision.ready_offline_domains),
        candidate_domains=list(decision.candidate_domains),
        blocked_domains=list(decision.blocked_domains),
        sensitive_domains=list(decision.sensitive_domains),
        can_activate_any_domain=decision.can_activate_any_domain,
        gates=[
            DomainGateResponse(
                domain=gate.domain,
                current_status=gate.current_status,
                requires_safety=gate.requires_safety,
                manifest_present=gate.manifest_present,
                registry_present=gate.registry_present,
                data_ready=gate.data_ready,
                safety_policy_ready=gate.safety_policy_ready,
                tests_ready=gate.tests_ready,
                ui_indication_ready=gate.ui_indication_ready,
                fallback_path_ready=gate.fallback_path_ready,
                allowed_tools_declared=gate.allowed_tools_declared,
                can_activate_now=gate.can_activate_now,
                recommended_status=gate.recommended_status,
                action=gate.action,
                blockers=list(gate.blockers),
                notes=list(gate.notes),
            )
            for gate in decision.gates
        ],
        notes=list(decision.notes),
    )


@router.get("/phase22-readiness", response_model=Phase22ReadinessResponse)
def phase22_readiness() -> Phase22ReadinessResponse:
    """Read-only Phase 22 decision before tokenizer v2 or quality training."""
    decision = build_phase22_readiness_decision()
    return Phase22ReadinessResponse(
        phase=decision.phase,
        status=decision.status,
        can_start_phase23=decision.can_start_phase23,
        corpus_path=decision.corpus_path,
        training_records=decision.training_records,
        target_records=decision.target_records,
        remaining_records=decision.remaining_records,
        min_per_dialect=decision.min_per_dialect,
        dialect_counts=decision.dialect_counts,
        quality_counts=decision.quality_counts,
        source_counts=decision.source_counts,
        missing_required_dialects=list(decision.missing_required_dialects),
        dialect_shortfalls=decision.dialect_shortfalls,
        corpus_issue_count=decision.corpus_issue_count,
        allowed_dialects=list(decision.allowed_dialects),
        allowed_qualities=list(decision.allowed_qualities),
        synthetic_llm_data_allowed=decision.synthetic_llm_data_allowed,
        action=decision.action,
        recommended_commands=list(decision.recommended_commands),
        blockers=list(decision.blockers),
        notes=list(decision.notes),
    )


@router.get("/phase22-collection-plan", response_model=Phase22CollectionPlanResponse)
def phase22_collection_plan(batch_size: int = 25) -> Phase22CollectionPlanResponse:
    """Read-only plan for collecting reviewed MSA/Saudi corpus batches."""
    plan = build_phase22_collection_plan(batch_size=batch_size)
    return Phase22CollectionPlanResponse(
        phase=plan.phase,
        status=plan.status,
        corpus_path=plan.corpus_path,
        current_records=plan.current_records,
        target_records=plan.target_records,
        remaining_records=plan.remaining_records,
        batch_size=plan.batch_size,
        estimated_batches=plan.estimated_batches,
        quota_by_dialect=plan.quota_by_dialect,
        flexible_records_after_minimums=plan.flexible_records_after_minimums,
        recommended_batch_mix=list(plan.recommended_batch_mix),
        review_rules=list(plan.review_rules),
        next_commands=list(plan.next_commands),
        planned_batches=[batch.to_json() for batch in plan.planned_batches],
        synthetic_llm_data_allowed=plan.synthetic_llm_data_allowed,
        notes=list(plan.notes),
    )


@router.get("/phase22-next-batch", response_model=Phase22NextBatchBriefResponse)
def phase22_next_batch(batch_size: int = 25) -> Phase22NextBatchBriefResponse:
    """Immediate Phase 22 authoring brief for the next reviewed batch."""
    brief = build_phase22_next_batch_brief(batch_size=batch_size)
    return Phase22NextBatchBriefResponse(
        phase=brief.phase,
        status=brief.status,
        next_batch=brief.next_batch.to_json() if brief.next_batch else None,
        why_this_batch=brief.why_this_batch,
        acceptance_checklist=list(brief.acceptance_checklist),
        suggested_topics=list(brief.suggested_topics),
        ui_instructions=list(brief.ui_instructions),
        after_export_commands=list(brief.after_export_commands),
        warnings=list(brief.warnings),
    )


@router.get("/phase22-completion-gate", response_model=Phase22CompletionGateResponse)
def phase22_completion_gate(batch_size: int = 25) -> Phase22CompletionGateResponse:
    """Strict read-only completion gate before Phase 23."""
    gate = build_phase22_completion_gate(batch_size=batch_size)
    return Phase22CompletionGateResponse(
        phase=gate.phase,
        status=gate.status,
        can_advance_phase23=gate.can_advance_phase23,
        readiness_status=gate.readiness_status,
        corpus_path=gate.corpus_path,
        training_records=gate.training_records,
        target_records=gate.target_records,
        remaining_records=gate.remaining_records,
        dialect_counts=gate.dialect_counts,
        dialect_shortfalls=gate.dialect_shortfalls,
        current_next_batch=gate.current_next_batch,
        completion_checks=gate.completion_checks,
        missing_requirements=list(gate.missing_requirements),
        required_before_advance=list(gate.required_before_advance),
        notes=list(gate.notes),
    )


@router.get("/phase22-review-intake", response_model=Phase22ReviewIntakeResponse)
def phase22_review_intake(max_files: int | None = None) -> Phase22ReviewIntakeResponse:
    """Read-only scan of chat review exports before corpus conversion."""
    report = build_phase22_review_intake_report(max_files=max_files)
    return Phase22ReviewIntakeResponse(
        phase=report.phase,
        status=report.status,
        review_path=report.review_path,
        review_files=report.review_files,
        candidate_files=report.candidate_files,
        total_review_records=report.total_review_records,
        total_valid_json_records=report.total_valid_json_records,
        total_schema_valid_records=report.total_schema_valid_records,
        total_user_assistant_records=report.total_user_assistant_records,
        total_raw_generator_assistant_records=report.total_raw_generator_assistant_records,
        total_safety_flagged_estimate=report.total_safety_flagged_estimate,
        average_dialogue_quality_score=report.average_dialogue_quality_score,
        synthetic_llm_data_allowed=report.synthetic_llm_data_allowed,
        files=[
            Phase22ReviewExportItemResponse(
                path=item.path,
                records=item.records,
                valid_json_records=item.valid_json_records,
                schema_valid_records=item.schema_valid_records,
                records_with_user_and_assistant=item.records_with_user_and_assistant,
                training_allowed_false=item.training_allowed_false,
                training_allowed_true=item.training_allowed_true,
                training_allowed_missing=item.training_allowed_missing,
                raw_generator_assistant_records=item.raw_generator_assistant_records,
                safety_flagged_estimate=item.safety_flagged_estimate,
                user_turns=item.user_turns,
                assistant_turns=item.assistant_turns,
                dialogue_quality_score=item.dialogue_quality_score,
                dialogue_quality_label=item.dialogue_quality_label,
                dialogue_quality_blockers=list(item.dialogue_quality_blockers),
                status=item.status,
                recommended_actions=list(item.recommended_actions),
                suggested_msa_command=item.suggested_msa_command,
                suggested_saudi_command=item.suggested_saudi_command,
                notes=list(item.notes),
            )
            for item in report.files
        ],
        recommended_next_commands=list(report.recommended_next_commands),
        notes=list(report.notes),
    )


@router.get("/phase23-tokenizer-audit")
def phase23_tokenizer_audit() -> dict[str, object]:
    """Read-only Phase 23 tokenizer v2 audit summary."""
    return build_phase23_tokenizer_audit().to_json()
