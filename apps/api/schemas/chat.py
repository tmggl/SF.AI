"""Pydantic schemas for the /chat endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="رسالة المستخدم النصية")
    session_id: str | None = Field(default=None, description="معرف جلسة اختياري")
    user_id: str | None = Field(default=None, description="معرف المستخدم/المالك اختياري")
    generator_trial: bool = Field(
        default=False,
        description="Phase 27.48 guarded local generator trial for the single-user UI; default runtime remains template",
    )


class ChatResponse(BaseModel):
    domain: str
    intent: str
    confidence: float
    matched_signals: list[str] = Field(default_factory=list)
    route_reason: str
    response: str
    requires_safety: bool = False
    status: str = "active"
    fallback_used: bool = False
    dispatch: str = Field(default="composer", description="composer | module:<name> | composer_no_module")
    generator: str = Field(
        default="template",
        description="template | sf_10m_v0_1 | sf_10m_v0_2 | sf_10m_phase27_33 | sf_10m_phase27_40 | sf_10m_phase27_47",
    )
    rag: str = Field(default="not_used", description="used | not_used")
    debug: dict[str, str] = Field(default_factory=dict)
    echo: str | None = Field(default=None, description="نص المستخدم الأصلي للتشخيص")


class ReviewExportSaveRequest(BaseModel):
    session_id: str | None = Field(default=None, description="UI session id")
    user_id: str | None = Field(default=None, description="UI owner/exporting user id")
    record: dict[str, Any] = Field(..., description="Single JSONL review-export record")


class ReviewExportSaveResponse(BaseModel):
    saved: bool
    path: str
    filename: str
    training_allowed: bool
    status: str
