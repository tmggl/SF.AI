"""POST /chat/message — Phase 4. Active chat domain → ChatModule."""

from __future__ import annotations

from fastapi import APIRouter, status

from apps.api.schemas.chat import ChatRequest, ChatResponse
from sf_ai.core.orchestrator import UserMessage, get_default_orchestrator

router = APIRouter(prefix="/chat", tags=["chat"])


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
