"""Pydantic schemas for /health and /system endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    project: str
    phase: str


class ComponentStatus(BaseModel):
    name: str
    status: str = Field(..., description="active | planned | skeleton_only | disabled")
    phase: str | None = Field(default=None, description="المرحلة المسؤولة عن المكون")


class SystemStatusResponse(BaseModel):
    project: str
    env: str
    current_phase: str
    current_phase_status: str
    next_phase: str
    sovereign: bool
    uses_external_llm: bool
    uses_pretrained_weights: bool
    uses_pretrained_embeddings: bool
    uses_pretrained_tokenizer: bool
    components: list[ComponentStatus]
