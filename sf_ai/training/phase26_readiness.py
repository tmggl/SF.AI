"""Read-only Phase 26 SF-50M readiness/scaling decision.

Phase 26 is intentionally a gate before it is a training run. The previous
phase proved that SF-10M v0.2 can be guarded, but the real model output was
still blocked. Jumping to SF-50M without more corpus and quality evidence would
violate the Progressive Scaling Strategy.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training
from sf_ai.models.transformer import config_for_size
from sf_ai.training.device import DeviceManager


MIN_SF50M_RECORDS = 5_000
REQUIRED_DIALECTS = ("msa", "saudi")
PHASE24_REPORT = Path("artifacts/reports/sf_10m_v0_2_training_report.json")
PHASE25_REPORT = Path("artifacts/reports/phase25_generation_canary_report.json")
TOKENIZER_V2_DIR = Path("artifacts/tokenizers/sf_bpe/v2")


@dataclass(frozen=True)
class Phase26ScalingDecision:
    phase: str
    status: str
    language_track: tuple[str, ...]
    target_model: str
    can_start_sf50m_training: bool
    recommended_action: str
    corpus: dict[str, object]
    tokenizer: dict[str, object]
    phase24: dict[str, object]
    phase25: dict[str, object]
    scaling_gates: dict[str, bool]
    target_config: dict[str, object]
    resource_estimate: dict[str, object]
    blockers: tuple[str, ...] = field(default_factory=tuple)
    recommended_commands: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["language_track"] = list(self.language_track)
        data["blockers"] = list(self.blockers)
        data["recommended_commands"] = list(self.recommended_commands)
        data["notes"] = list(self.notes)
        return data


def build_phase26_scaling_decision(
    project_dir: str | Path | None = None,
) -> Phase26ScalingDecision:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    corpus_root = root / "data/corpus/chat/jsonl"
    corpus_report = audit_jsonl_directory_for_training(corpus_root)
    dialect_counts = dict(corpus_report.dialect_counts)
    missing_dialects = tuple(
        dialect for dialect in REQUIRED_DIALECTS if dialect_counts.get(dialect, 0) == 0
    )

    tokenizer_dir = root / TOKENIZER_V2_DIR
    tokenizer_meta = _read_json(tokenizer_dir / "meta.json")
    tokenizer_audit = _read_json(tokenizer_dir / "audit_report.json")
    tokenizer_ready = all(
        (tokenizer_dir / name).exists()
        for name in (
            "meta.json",
            "vocab.json",
            "merges.txt",
            "tokenizer_config.json",
            "provenance.json",
            "audit_report.json",
        )
    ) and tokenizer_audit.get("status") == "COMPLETED_READY_FOR_PHASE24"

    phase24 = _read_json(root / PHASE24_REPORT)
    phase25 = _read_json(root / PHASE25_REPORT)
    phase24_training_passed = bool(
        (phase24.get("decision") or {}).get("phase24_training_passed")
    )
    phase24_runtime_allowed = bool(
        (phase24.get("decision") or {}).get("suitable_for_chat_runtime")
    )
    phase25_guard_passed = bool(
        (phase25.get("decision") or {}).get("phase25_canary_infrastructure_passed")
    )
    phase25_open_chat_allowed = bool(
        (phase25.get("decision") or {}).get("sf_10m_v0_2_suitable_for_open_chat")
    )

    target_cfg = config_for_size(
        "sf-50m",
        vocab_size=int(tokenizer_meta.get("vocab_size") or 8000),
        max_seq_len=512,
    )
    device = DeviceManager(preference="auto").select()

    corpus_ready = (
        corpus_report.error_count == 0
        and corpus_report.training_ready >= MIN_SF50M_RECORDS
        and not missing_dialects
    )
    tokenization_audit_passed = tokenizer_ready
    evaluation_suite_passed = phase24_training_passed and phase25_guard_passed
    runtime_quality_passed = phase24_runtime_allowed and phase25_open_chat_allowed
    safety_checks_passed = bool(phase25.get("runtime_default", {}).get("canary_enabled_by_default") is False)
    hallucination_checks_passed = False
    repetition_checks_passed = not bool((phase24.get("generation_quality") or {}).get("contains_repetition"))
    resource_readiness = device.name in {"mps", "cuda", "cpu"}

    scaling_gates = {
        "corpus_readiness": corpus_ready,
        "tokenization_audit": tokenization_audit_passed,
        "evaluation_suite": evaluation_suite_passed,
        "safety_checks": safety_checks_passed,
        "runtime_quality": runtime_quality_passed,
        "hallucination_checks": hallucination_checks_passed,
        "repetition_checks": repetition_checks_passed,
        "resource_readiness": resource_readiness,
    }

    blockers: list[str] = []
    if corpus_report.error_count:
        blockers.append("corpus_has_governance_issues")
    if corpus_report.training_ready < MIN_SF50M_RECORDS:
        blockers.append("corpus_below_sf50m_minimum")
    if missing_dialects:
        blockers.append("missing_required_msa_or_saudi")
    if not tokenizer_ready:
        blockers.append("tokenizer_v2_not_ready")
    if not phase24_training_passed:
        blockers.append("phase24_training_not_passed")
    if not phase24_runtime_allowed:
        blockers.append("phase24_runtime_quality_blocked")
    if not phase25_guard_passed:
        blockers.append("phase25_canary_guard_missing_or_failed")
    if not phase25_open_chat_allowed:
        blockers.append("phase25_real_model_blocked")
    if not hallucination_checks_passed:
        blockers.append("hallucination_checks_missing")
    if not repetition_checks_passed:
        blockers.append("repetition_checks_failed")

    can_start = not blockers
    status = "READY_FOR_SF50M_TRAINING" if can_start else "NOT_READY_IMPROVE_SF10M_AND_CANARY"
    action = (
        "START_SF50M_TRAINING"
        if can_start
        else "DO_NOT_TRAIN_SF50M_YET_IMPROVE_SF10M_CANARY"
    )

    return Phase26ScalingDecision(
        phase="Phase 26 — SF-50M v0.1 Dialogue Model Readiness",
        status=status,
        language_track=REQUIRED_DIALECTS,
        target_model="sf-50m",
        can_start_sf50m_training=can_start,
        recommended_action=action,
        corpus={
            "path": str(corpus_root.relative_to(root)),
            "training_records": corpus_report.training_ready,
            "min_training_records": MIN_SF50M_RECORDS,
            "issue_count": corpus_report.error_count,
            "dialects": dialect_counts,
            "quality": dict(corpus_report.quality_counts),
            "missing_required_dialects": list(missing_dialects),
        },
        tokenizer={
            "path": str(TOKENIZER_V2_DIR),
            "ready": tokenizer_ready,
            "status": tokenizer_audit.get("status", ""),
            "vocab_size": tokenizer_meta.get("vocab_size"),
            "merges": tokenizer_meta.get("merges"),
            "sf_origin": tokenizer_meta.get("sf_origin") is True,
        },
        phase24={
            "status": phase24.get("status", ""),
            "training_passed": phase24_training_passed,
            "runtime_allowed": phase24_runtime_allowed,
            "eval_loss": (phase24.get("evaluation") or {}).get("loss"),
            "perplexity": (phase24.get("evaluation") or {}).get("perplexity"),
        },
        phase25={
            "status": phase25.get("status", ""),
            "canary_guard_passed": phase25_guard_passed,
            "open_chat_allowed": phase25_open_chat_allowed,
            "real_model_guard_reason": (phase25.get("real_model_smoke") or {}).get("guard_reason", ""),
        },
        scaling_gates=scaling_gates,
        target_config={
            "name": target_cfg.name,
            "max_seq_len": target_cfg.max_seq_len,
            "d_model": target_cfg.d_model,
            "n_heads": target_cfg.n_heads,
            "n_layers": target_cfg.n_layers,
            "ff_mult": target_cfg.ff_mult,
            "vocab_size": target_cfg.vocab_size,
            "sovereign": target_cfg.sovereign,
        },
        resource_estimate={
            "device": device.name,
            "device_note": device.notes,
            "training_allowed_by_resources": resource_readiness,
            "checkpoint_root": "artifacts/checkpoints/sf_50m_v0_1",
        },
        blockers=tuple(blockers),
        recommended_commands=(
            "make corpus-audit",
            "make phase23-tokenizer-audit",
            "make phase26-readiness",
            "repair SF-10M assistant-target quality",
            "repeat SF-10M quality training/canary",
        ),
        notes=(
            "This decision is read-only and starts no training.",
            "Phase 25 protected the UI by blocking real SF-10M v0.2 output.",
            "Progressive Scaling Strategy blocks SF-50M until current-tier quality gates pass.",
            "Language track remains msa + saudi only.",
        ),
    )


def write_phase26_report(
    project_dir: str | Path | None = None,
    *,
    out: str | Path = "artifacts/reports/phase26_sf50m_readiness_report.json",
) -> Phase26ScalingDecision:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    decision = build_phase26_scaling_decision(root)
    out_path = root / out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(decision.to_json(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return decision


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}
