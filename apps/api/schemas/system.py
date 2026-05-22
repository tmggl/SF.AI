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


class CorpusIssueResponse(BaseModel):
    line_number: int | None
    kind: str
    message: str
    snippet: str = ""


class CorpusAuditResponse(BaseModel):
    corpus: str
    status: str = Field(..., description="READY_FOR_PHASE_12_TOKENIZER_TRAINING | NOT_READY_FOR_TRAINING")
    total_records: int
    training_ready: int
    issue_count: int
    dialect_counts: dict[str, int]
    quality_counts: dict[str, int]
    source_counts: dict[str, int]
    issues: list[CorpusIssueResponse]
