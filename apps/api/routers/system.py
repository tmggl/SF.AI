"""GET /system/status — phase status and high-level capability flags.

Phase 1 returns a static snapshot. From Phase 2 onward this will read
from the Capability Registry and live components.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends

from apps.api.dependencies import Settings, get_settings
from apps.api.schemas.system import ComponentStatus, SystemStatusResponse

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
        current_phase="Phase 11 — Sovereign Corpus Governance & Saudi/MSA Dialogue Pack",
        current_phase_status="completed",
        next_phase="Phase 12 — SF-BPE Tokenizer v1 Training & Audit (after JSONL data + explicit permission)",
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
            ComponentStatus(name="rag", status="planned", phase="Phase 8"),
        ],
    )
