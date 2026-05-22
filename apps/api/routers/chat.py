"""POST /chat/message — Phase 4. Active chat domain → ChatModule."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from apps.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ReviewExportSaveRequest,
    ReviewExportSaveResponse,
)
from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.orchestrator import UserMessage, get_default_orchestrator

router = APIRouter(prefix="/chat", tags=["chat"])
REVIEW_EXPORT_DIR = PROJECT_DIR / "data/corpus/chat/review"


@router.post(
    "/message",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat_message(payload: ChatRequest) -> ChatResponse:
    orchestrator = get_default_orchestrator()
    result = orchestrator.process(
        UserMessage(text=payload.message, session_id=payload.session_id)
    )
    return ChatResponse(
        domain=result.domain,
        intent=result.intent,
        confidence=round(result.confidence, 4),
        matched_signals=list(result.matched_signals),
        route_reason=result.route_reason,
        response=result.response,
        requires_safety=result.requires_safety,
        status=result.status,
        fallback_used=result.fallback_used,
        dispatch=result.debug.get("dispatch", "composer"),
        generator=result.debug.get("generator", "template"),
        rag=result.debug.get("rag", "not_used"),
        debug=result.debug,
        echo=payload.message,
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
