"""Read-only Phase 19 readiness gate.

Phase 19 is the first jump from the smoke-sized SF-10M run to an SF-50M
candidate. The gate is intentionally practical: it does not train, mutate
checkpoints, or pretend that a larger model fixes a tiny corpus.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.models.transformer import config_for_size
from sf_ai.training.device import DeviceManager


MIN_PHASE19_RECORDS = 5_000
REQUIRED_DIALECTS = ("msa", "saudi")


@dataclass(frozen=True)
class Phase19ReadinessDecision:
    phase: str
    status: str
    can_start_training: bool
    lab_experiment_allowed: bool
    corpus_path: str
    training_records: int
    min_training_records: int
    corpus_issue_count: int
    dialect_counts: dict[str, int]
    missing_required_dialects: tuple[str, ...]
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
    recommended_commands: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["missing_required_dialects"] = list(self.missing_required_dialects)
        data["recommended_commands"] = list(self.recommended_commands)
        data["blockers"] = list(self.blockers)
        data["notes"] = list(self.notes)
        return data


def build_phase19_readiness_decision(
    project_dir: str | Path | None = None,
) -> Phase19ReadinessDecision:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    corpus_path = root / "data/corpus/chat/jsonl"
    corpus = audit_jsonl_directory_for_training(corpus_path)
    dialect_counts = dict(corpus.dialect_counts)
    missing_dialects = tuple(
        dialect for dialect in REQUIRED_DIALECTS if dialect_counts.get(dialect, 0) == 0
    )

    tokenizer_dir = root / "artifacts/tokenizers/sf_bpe/v1"
    tokenizer_ready = all(
        (tokenizer_dir / name).exists()
        for name in ("meta.json", "vocab.json", "merges.txt")
    )

    sf10m_dir = root / "artifacts/checkpoints/sf_10m_v0_1/sf-10m-step33"
    sf10m_checkpoint_ready = (sf10m_dir / "meta.json").exists() and (
        sf10m_dir / "state.pt"
    ).exists()

    eval_report = _read_json(root / "eval/reports/sf_10m_eval_v1.json")
    phase16_eval_passed = eval_report.get("status") == "PASS_WITH_RUNTIME_BLOCKED"
    phase16_runtime_activation_allowed = bool(
        eval_report.get("runtime_activation_allowed", False)
    )

    target_cfg = config_for_size("sf-50m", vocab_size=8_000, max_seq_len=512)
    device = DeviceManager(preference="auto").select()

    blockers: list[str] = []
    if corpus.error_count:
        blockers.append("corpus_has_governance_issues")
    if corpus.training_ready < MIN_PHASE19_RECORDS:
        blockers.append("corpus_too_small_for_sf50m")
    if missing_dialects:
        blockers.append("missing_required_msa_or_saudi_balance")
    if not tokenizer_ready:
        blockers.append("tokenizer_v1_missing")
    if not sf10m_checkpoint_ready:
        blockers.append("sf10m_checkpoint_missing")
    if not phase16_eval_passed:
        blockers.append("phase16_eval_report_missing_or_failed")

    can_start = not blockers
    status = "READY_FOR_SF50M_TRAINING" if can_start else "NOT_READY_EXPAND_CORPUS_FIRST"
    action = (
        "START_SF50M_TRAINING"
        if can_start
        else "USE_PHASE18_LOOP_TO_GROW_REVIEWED_MSA_SAUDI_CORPUS"
    )

    return Phase19ReadinessDecision(
        phase="Phase 19 — SF-50M Candidate Training",
        status=status,
        can_start_training=can_start,
        lab_experiment_allowed=True,
        corpus_path=str(corpus_path.relative_to(root)),
        training_records=corpus.training_ready,
        min_training_records=MIN_PHASE19_RECORDS,
        corpus_issue_count=corpus.error_count,
        dialect_counts=dialect_counts,
        missing_required_dialects=missing_dialects,
        tokenizer_ready=tokenizer_ready,
        sf10m_checkpoint_ready=sf10m_checkpoint_ready,
        phase16_eval_passed=phase16_eval_passed,
        phase16_runtime_activation_allowed=phase16_runtime_activation_allowed,
        target_model=target_cfg.name,
        target_context=target_cfg.max_seq_len,
        target_d_model=target_cfg.d_model,
        target_layers=target_cfg.n_layers,
        target_heads=target_cfg.n_heads,
        device=device.name,
        action=action,
        recommended_commands=(
            "make phase22-next-batch",
            "add owner-approved MSA/Saudi dialogue batches with full provenance",
            "make corpus-audit",
            "make phase19-readiness",
        ),
        blockers=tuple(blockers),
        notes=(
            "This command is read-only and starts no training.",
            "Sami's lab runtime may test the raw generator, but SF-50M training needs much more governed corpus.",
            "Arabic MSA + Saudi remain the active language track.",
        ),
    )


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}
