"""Pydantic schemas for the /chat endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="رسالة المستخدم النصية")
    session_id: str | None = Field(default=None, description="معرف جلسة اختياري")


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
    debug: dict[str, str] = Field(default_factory=dict)
    echo: str | None = Field(default=None, description="نص المستخدم الأصلي للتشخيص")
