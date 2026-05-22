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


class SourceInventoryItemResponse(BaseModel):
    name: str
    path: str
    kind: str
    exists: bool
    records: int
    valid_json_records: int
    private_or_ignored: bool
    tracked_payload_allowed: bool
    phase12_tokenizer_candidate: bool
    phase13_lm_candidate: bool
    needs_conversion: bool
    needs_governance_audit: bool
    status: str
    action_required: str
    notes: list[str]
    stats: dict[str, object]


class SourceInventoryResponse(BaseModel):
    phase12_status: str
    source_count: int
    chat_training_records: int
    local_reference_records: int
    blockers: list[str]
    sources: list[SourceInventoryItemResponse]


class Phase12ReadinessResponse(BaseModel):
    phase: str
    preflight_pass: bool
    can_train_now: bool
    training_permission_granted: bool
    required_permission_phrase: str
    required_confirmation_flag: str
    action: str
    corpus_status: str
    corpus_training_ready: int
    corpus_issue_count: int
    tokenization_status: str
    protected_terms_total: int
    protected_terms_covered: int
    protected_terms_coverage_ratio: float
    source_count: int
    local_reference_records: int
    artifacts_present: list[str]
    required_command_after_permission: str
    notes: list[str]
