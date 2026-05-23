"""POST /chat/message — Phase 4. Active chat domain → ChatModule."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from apps.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ReviewExportSaveRequest,
    ReviewExportSaveResponse,
)
from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.index import load_default_registry
from sf_ai.core.orchestrator import Orchestrator, UserMessage, get_default_orchestrator
from sf_ai.datasets.corpus_governance import detect_training_forbidden_operational_terms
from sf_ai.modules.chat import ChatModule, GenerationPolicy, NativeGenerator, NativeGeneratorConfig

router = APIRouter(prefix="/chat", tags=["chat"])
REVIEW_EXPORT_DIR = PROJECT_DIR / "data/corpus/chat/review"


@router.post(
    "/message",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat_message(payload: ChatRequest) -> ChatResponse:
    # Phase 27.50: the single-user lab chat surface is generator-first. We no
    # longer expose a template/default toggle from /chat/message; if the
    # guarded native generator cannot answer, the API returns an empty response
    # with explicit metadata instead of silently showing a template.
    orchestrator = _get_guarded_trial_orchestrator()
    result = orchestrator.process(
        UserMessage(text=payload.message, session_id=payload.session_id)
    )
    debug = dict(result.debug)
    response_text = result.response
    generator = debug.get("generator", "template")
    dispatch = debug.get("dispatch", "composer")
    if generator == "template":
        response_text = ""
        generator = "generator_blocked"
        dispatch = "module:chat_lab"
        debug["generator"] = generator
        if "module_notes" in debug:
            debug["module_notes"] = debug["module_notes"].replace(
                "generator:template",
                "generator:generator_blocked",
            )
        debug["generator_only_blocked"] = "true"
        debug["fixed_reply_suppressed"] = "true"
    return ChatResponse(
        domain=result.domain,
        intent=result.intent,
        confidence=round(result.confidence, 4),
        matched_signals=list(result.matched_signals),
        route_reason=result.route_reason,
        response=response_text,
        requires_safety=result.requires_safety,
        status=result.status,
        fallback_used=result.fallback_used,
        dispatch=dispatch,
        generator=generator,
        rag=debug.get("rag", "not_used"),
        debug=debug,
        echo=payload.message,
    )


@lru_cache(maxsize=1)
def _get_guarded_trial_orchestrator() -> Orchestrator:
    """Build the Phase 27.47 local generator path for the lab chat API.

    Phase 27.50 makes this the only visible /chat/message path. If the guarded
    generator cannot answer, the endpoint suppresses legacy template text and
    returns `generator_blocked` with an empty response.
    """
    policy = GenerationPolicy(
        enabled=True,
        experimental_runtime=True,
        canary=True,
        guarded_runtime_trial=True,
        min_confidence=0.0,
        max_new_tokens=24,
        temperature=1.0,
        top_k=0,
        candidate_generator="sf_10m_phase27_47",
    )
    generator = NativeGenerator(
        NativeGeneratorConfig(
            tokenizer_path=PROJECT_DIR / "artifacts/tokenizers/sf_bpe/v6_weak_lane_terms",
            checkpoints_root=PROJECT_DIR
            / "artifacts/eval/phase27_47_new_topic_conditioning_repair/checkpoints",
            checkpoint_name="sf-10m-step4600",
            generator_name="sf_10m_phase27_47",
            model_size="sf-10m",
            seq_len=64,
            max_new_tokens=24,
            temperature=1.0,
            top_k=0,
            no_repeat_ngram_size=3,
            repetition_penalty=1.1,
            dialogue_prompt=True,
        )
    )
    chat_module = ChatModule(generation_policy=policy, native_generator=generator)
    return Orchestrator(
        registry=load_default_registry(),
        modules={"chat": chat_module},
    )


@router.post(
    "/review-export",
    response_model=ReviewExportSaveResponse,
    status_code=status.HTTP_201_CREATED,
)
def save_review_export(payload: ReviewExportSaveRequest) -> ReviewExportSaveResponse:
    """Save a UI review export locally without admitting it to training."""
    record = payload.record
    _validate_review_export_record(record, user_id=payload.user_id)

    session = _safe_slug(
        payload.session_id
        or _nested_str(record, "review_metadata", "session_id")
        or "session"
    )
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    filename = f"sfai_chat_review_{session}_{stamp}.jsonl"

    REVIEW_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REVIEW_EXPORT_DIR / filename
    path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
    rel = path.relative_to(PROJECT_DIR) if path.is_relative_to(PROJECT_DIR) else path

    return ReviewExportSaveResponse(
        saved=True,
        path=str(rel),
        filename=filename,
        training_allowed=False,
        status="saved_for_manual_review_only",
    )


def _validate_review_export_record(
    record: dict[str, object],
    *,
    user_id: str | None = None,
) -> None:
    if record.get("domain") != "chat":
        raise HTTPException(status_code=400, detail="review export must be domain=chat")
    messages = record.get("messages")
    if not isinstance(messages, list) or not messages:
        raise HTTPException(status_code=400, detail="review export must contain messages")
    has_user = any(isinstance(m, dict) and m.get("role") == "user" for m in messages)
    has_assistant = any(isinstance(m, dict) and m.get("role") == "assistant" for m in messages)
    if not (has_user and has_assistant):
        raise HTTPException(status_code=400, detail="review export needs user and assistant turns")

    provenance = record.get("provenance")
    if not isinstance(provenance, dict):
        raise HTTPException(status_code=400, detail="review export must include provenance")
    if provenance.get("training_allowed") is not False:
        raise HTTPException(status_code=400, detail="review exports must keep training_allowed=false")
    if provenance.get("quality") != "needs_review":
        raise HTTPException(status_code=400, detail="review exports must keep quality=needs_review")

    review_metadata = record.get("review_metadata")
    if not isinstance(review_metadata, dict):
        raise HTTPException(status_code=400, detail="review export must include review_metadata")
    meta_owner = _str_from_mapping(review_metadata, "owner_user_id")
    meta_exporter = _str_from_mapping(review_metadata, "exported_by_user_id")
    meta_target = _str_from_mapping(review_metadata, "target_user_id")
    meta_scope = _str_from_mapping(review_metadata, "user_scope")

    prov_owner = _str_from_mapping(provenance, "owner_user_id")
    prov_creator = _str_from_mapping(provenance, "created_by_user_id")
    prov_target = _str_from_mapping(provenance, "target_user_id")
    prov_scope = _str_from_mapping(provenance, "user_scope")

    if not all((meta_owner, meta_exporter, meta_target, meta_scope)):
        raise HTTPException(
            status_code=400,
            detail="review export must include user ownership metadata",
        )
    if not all((prov_owner, prov_creator, prov_target, prov_scope)):
        raise HTTPException(
            status_code=400,
            detail="review export provenance must include user ownership fields",
        )
    if meta_scope != "single_user" or prov_scope != "single_user":
        raise HTTPException(status_code=400, detail="review export must use user_scope=single_user")
    if len({meta_owner, meta_exporter, meta_target, prov_owner, prov_creator, prov_target}) != 1:
        raise HTTPException(status_code=400, detail="review export user ownership fields must match")
    if user_id is not None and user_id != meta_owner:
        raise HTTPException(status_code=400, detail="request user_id must match export owner_user_id")
    if detect_training_forbidden_operational_terms(record):
        raise HTTPException(
            status_code=400,
            detail="review export is training_forbidden_operational_internal_dialogue",
        )


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())[:64]
    return slug or "session"


def _nested_str(record: dict[str, object], parent: str, child: str) -> str | None:
    obj = record.get(parent)
    if isinstance(obj, dict):
        value = obj.get(child)
        if isinstance(value, str):
            return value
    return None


def _str_from_mapping(obj: dict[str, object], key: str) -> str | None:
    value = obj.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
