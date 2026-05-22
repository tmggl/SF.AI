"""GET /system/status — phase status and high-level capability flags.

Phase 1 returns a static snapshot. From Phase 2 onward this will read
from the Capability Registry and live components.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends

from apps.api.dependencies import Settings, get_settings
from apps.api.schemas.system import (
    ComponentStatus,
    CorpusAuditResponse,
    CorpusIssueResponse,
    Phase12ReadinessResponse,
    SourceInventoryItemResponse,
    SourceInventoryResponse,
    SystemStatusResponse,
)
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.datasets.source_inventory import build_source_inventory
from sf_ai.training.phase12_readiness import build_phase12_readiness_decision

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=SystemStatusResponse)
def system_status(settings: Settings = Depends(get_settings)) -> SystemStatusResponse:
    saudi_seed_enabled = (
        os.getenv("ENABLE_SAUDI_SEED_V1_LEXICON", "").strip().lower()
        in {"1", "true", "yes", "on"}
    )
    return SystemStatusResponse(
        project=settings.project_name,
        env=settings.env,
        current_phase="Phase 17 — Local Memory/RAG Bridge into Chat",
        current_phase_status="completed_local_bridge",
        next_phase="Phase 18 — Data Expansion Loop v1",
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
            ComponentStatus(name="coding_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="data_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="files_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="legal_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="medical_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="finance_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="education_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="religion_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="social_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="writing_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="translation_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="image_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="audio_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="security_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="business_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="ecommerce_module", status="skeleton_only", phase="Phase 10"),
            ComponentStatus(name="corpus_governance", status="active", phase="Phase 11"),
            ComponentStatus(name="training_corpus", status="waiting_for_user_data", phase="Phase 11"),
            ComponentStatus(name="phase12_corpus_preflight", status="active", phase="Phase 12"),
            ComponentStatus(name="native_generator", status="ready_offline", phase="Phase 15"),
            ComponentStatus(name="generation_policy", status="active", phase="Phase 15"),
            ComponentStatus(name="evaluation_harness", status="active", phase="Phase 16"),
            ComponentStatus(name="rag", status="active", phase="Phase 8"),
            ComponentStatus(name="chat_rag_bridge", status="ready_offline", phase="Phase 17"),
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
