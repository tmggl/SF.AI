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
    corpus_dialect_counts: dict[str, int]
    required_dialects: list[str]
    missing_required_dialects: list[str]
    language_balance_status: str
    tokenization_status: str
    protected_terms_total: int
    protected_terms_covered: int
    protected_terms_coverage_ratio: float
    source_count: int
    local_reference_records: int
    artifacts_present: list[str]
    required_command_after_permission: str
    notes: list[str]


class Phase19ReadinessResponse(BaseModel):
    phase: str
    status: str
    can_start_training: bool
    lab_experiment_allowed: bool
    corpus_path: str
    training_records: int
    min_training_records: int
    corpus_issue_count: int
    dialect_counts: dict[str, int]
    missing_required_dialects: list[str]
    tokenizer_ready: bool
    sf10m_checkpoint_ready: bool
    phase16_eval_passed: bool
    phase16_runtime_activation_allowed: bool
    target_model: str
    target_context: int
    target_d_model: int
    target_layers: int
    target_heads: int
    device: str
    action: str
    recommended_commands: list[str]
    blockers: list[str]
    notes: list[str]


class DomainGateResponse(BaseModel):
    domain: str
    current_status: str
    requires_safety: bool
    manifest_present: bool
    registry_present: bool
    data_ready: bool
    safety_policy_ready: bool
    tests_ready: bool
    ui_indication_ready: bool
    fallback_path_ready: bool
    allowed_tools_declared: bool
    can_activate_now: bool
    recommended_status: str
    action: str
    blockers: list[str]
    notes: list[str]


class Phase20GatesResponse(BaseModel):
    phase: str
    status: str
    language_track: list[str]
    lexicon_track: str
    total_domains: int
    active_domains: list[str]
    ready_offline_domains: list[str]
    candidate_domains: list[str]
    blocked_domains: list[str]
    sensitive_domains: list[str]
    can_activate_any_domain: bool
    gates: list[DomainGateResponse]
    notes: list[str]


class Phase22ReadinessResponse(BaseModel):
    phase: str
    status: str
    can_start_phase23: bool
    corpus_path: str
    training_records: int
    target_records: int
    remaining_records: int
    min_per_dialect: int
    dialect_counts: dict[str, int]
    quality_counts: dict[str, int]
    source_counts: dict[str, int]
    missing_required_dialects: list[str]
    dialect_shortfalls: dict[str, int]
    corpus_issue_count: int
    allowed_dialects: list[str]
    allowed_qualities: list[str]
    synthetic_llm_data_allowed: bool
    action: str
    recommended_commands: list[str]
    blockers: list[str]
    notes: list[str]
