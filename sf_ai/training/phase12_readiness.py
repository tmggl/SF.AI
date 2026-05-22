"""Read-only Phase 12 readiness decision.

This module intentionally does not train, write tokenizer artifacts, or mutate
server state. It exists so the API endpoint and CLI command report the same
decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.source_inventory import build_source_inventory
from sf_ai.models.tokenizer.policy_audit import audit_tokenization_policy


REQUIRED_PHASE12_PERMISSION_PHRASE = "ابدأ Phase 12"
REQUIRED_PHASE12_CONFIRMATION_FLAG = "--confirm-phase12-permission"
PHASE12_TRAIN_BPE_COMMAND = (
    'make train-bpe ARGS="--confirm-phase12-permission '
    '--corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"'
)


@dataclass(frozen=True)
class Phase12ReadinessDecision:
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
    artifacts_present: tuple[str, ...] = field(default_factory=tuple)
    required_command_after_permission: str = PHASE12_TRAIN_BPE_COMMAND
    notes: tuple[str, ...] = field(default_factory=tuple)


def _find_training_artifacts(root: Path) -> tuple[str, ...]:
    artifacts: list[str] = []
    artifact_globs = (
        "artifacts/tokenizers/*/vocab.json",
        "artifacts/tokenizers/*/merges.txt",
        "artifacts/checkpoints/**/*",
    )
    for pattern in artifact_globs:
        for path in root.glob(pattern):
            if path.is_file() and path.name != ".gitkeep":
                artifacts.append(str(path.relative_to(root)))
    return tuple(sorted(artifacts))


def build_phase12_readiness_decision(
    project_dir: str | Path | None = None,
) -> Phase12ReadinessDecision:
    """Build a read-only Phase 12 decision from current local state."""
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    inventory = build_source_inventory(root)
    tokenization = audit_tokenization_policy()

    corpus_ready = inventory.phase12_status == "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
    tokenization_ready = tokenization.status == "READY_FOR_PHASE12_TOKENIZATION_PREFLIGHT"
    protected_ready = (
        tokenization.protected_terms_total > 0
        and tokenization.protected_terms_covered == tokenization.protected_terms_total
    )
    preflight_pass = corpus_ready and tokenization_ready and protected_ready

    # This flips only after explicit human permission. A preflight pass never
    # grants training permission by itself.
    training_permission_granted = False

    return Phase12ReadinessDecision(
        phase="Phase 12 — SF-BPE Tokenizer v1 Training & Audit",
        preflight_pass=preflight_pass,
        can_train_now=preflight_pass and training_permission_granted,
        training_permission_granted=training_permission_granted,
        required_permission_phrase=REQUIRED_PHASE12_PERMISSION_PHRASE,
        required_confirmation_flag=REQUIRED_PHASE12_CONFIRMATION_FLAG,
        action=(
            "STOP_BEFORE_TRAINING"
            if preflight_pass
            else "FIX_PREFLIGHT_BEFORE_REQUESTING_PERMISSION"
        ),
        corpus_status=inventory.phase12_status,
        corpus_training_ready=inventory.chat_training_records,
        corpus_issue_count=inventory.chat_audit.error_count,
        tokenization_status=tokenization.status,
        protected_terms_total=tokenization.protected_terms_total,
        protected_terms_covered=tokenization.protected_terms_covered,
        protected_terms_coverage_ratio=round(tokenization.coverage_ratio, 4),
        source_count=inventory.source_count,
        local_reference_records=inventory.local_reference_records,
        artifacts_present=_find_training_artifacts(root),
        notes=(
            "Preflight readiness is not training permission.",
            "This decision is read-only and writes no tokenizer/checkpoint artifacts.",
            "Training commands refuse to start without --confirm-phase12-permission.",
        ),
    )
