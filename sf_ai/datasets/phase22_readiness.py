"""Read-only Phase 22 readiness for Gold Dialogue Corpus v2.

Phase 22 is data work, not model training. This gate tells us whether the
governed chat corpus is large and balanced enough to justify tokenizer v2.
It never generates data and never writes training artifacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import ceil
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training


TARGET_RECORDS = 500
MIN_PER_DIALECT = 200
REQUIRED_DIALECTS = ("msa", "saudi")
REQUIRED_QUALITIES = ("gold", "silver")


@dataclass(frozen=True)
class Phase22ReadinessDecision:
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
    missing_required_dialects: tuple[str, ...]
    dialect_shortfalls: dict[str, int]
    corpus_issue_count: int
    allowed_dialects: tuple[str, ...]
    allowed_qualities: tuple[str, ...]
    synthetic_llm_data_allowed: bool
    action: str
    recommended_commands: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["missing_required_dialects"] = list(self.missing_required_dialects)
        data["allowed_dialects"] = list(self.allowed_dialects)
        data["allowed_qualities"] = list(self.allowed_qualities)
        data["recommended_commands"] = list(self.recommended_commands)
        data["blockers"] = list(self.blockers)
        data["notes"] = list(self.notes)
        return data


@dataclass(frozen=True)
class Phase22PlannedBatch:
    sequence: int
    batch_id: str
    dialect: str
    target_records: int
    priority: str
    suggested_review_path: str
    suggested_output_path: str
    prepare_command: str
    user_task: str

    def to_json(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class Phase22CollectionPlan:
    phase: str
    status: str
    corpus_path: str
    current_records: int
    target_records: int
    remaining_records: int
    batch_size: int
    estimated_batches: int
    quota_by_dialect: dict[str, int]
    flexible_records_after_minimums: int
    recommended_batch_mix: tuple[str, ...]
    review_rules: tuple[str, ...]
    next_commands: tuple[str, ...]
    planned_batches: tuple[Phase22PlannedBatch, ...]
    synthetic_llm_data_allowed: bool
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["recommended_batch_mix"] = list(self.recommended_batch_mix)
        data["review_rules"] = list(self.review_rules)
        data["next_commands"] = list(self.next_commands)
        data["planned_batches"] = [batch.to_json() for batch in self.planned_batches]
        data["notes"] = list(self.notes)
        return data


def build_phase22_readiness_decision(
    project_dir: str | Path | None = None,
) -> Phase22ReadinessDecision:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    corpus_path = root / "data/corpus/chat/jsonl"
    corpus = audit_jsonl_directory_for_training(corpus_path)

    dialect_counts = dict(corpus.dialect_counts)
    quality_counts = dict(corpus.quality_counts)
    source_counts = dict(corpus.source_counts)
    missing_dialects = tuple(
        dialect for dialect in REQUIRED_DIALECTS if dialect_counts.get(dialect, 0) == 0
    )
    dialect_shortfalls = {
        dialect: max(0, MIN_PER_DIALECT - dialect_counts.get(dialect, 0))
        for dialect in REQUIRED_DIALECTS
    }
    remaining_records = max(0, TARGET_RECORDS - corpus.training_ready)

    blockers: list[str] = []
    if corpus.error_count:
        blockers.append("corpus_has_governance_issues")
    if corpus.training_ready < TARGET_RECORDS:
        blockers.append("corpus_below_phase22_target")
    if missing_dialects:
        blockers.append("missing_required_msa_or_saudi")
    if any(shortfall > 0 for shortfall in dialect_shortfalls.values()):
        blockers.append("dialect_balance_below_minimum")
    if not any(quality_counts.get(q, 0) for q in REQUIRED_QUALITIES):
        blockers.append("missing_gold_or_silver_quality")

    can_start = not blockers
    status = (
        "READY_FOR_PHASE23_TOKENIZER_V2"
        if can_start
        else "NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2"
    )
    action = (
        "START_PHASE23_TOKENIZER_V2"
        if can_start
        else "COLLECT_AND_REVIEW_USER_AUTHORED_MSA_SAUDI_DIALOGUES"
    )

    return Phase22ReadinessDecision(
        phase="Phase 22 — Gold Dialogue Corpus v2",
        status=status,
        can_start_phase23=can_start,
        corpus_path=str(corpus_path.relative_to(root)),
        training_records=corpus.training_ready,
        target_records=TARGET_RECORDS,
        remaining_records=remaining_records,
        min_per_dialect=MIN_PER_DIALECT,
        dialect_counts=dialect_counts,
        quality_counts=quality_counts,
        source_counts=source_counts,
        missing_required_dialects=missing_dialects,
        dialect_shortfalls=dialect_shortfalls,
        corpus_issue_count=corpus.error_count,
        allowed_dialects=REQUIRED_DIALECTS,
        allowed_qualities=REQUIRED_QUALITIES,
        synthetic_llm_data_allowed=False,
        action=action,
        recommended_commands=(
            "test real conversations in /ui/chat, then export with the تصدير button",
            "review exported JSONL manually; keep only user-authored/user-approved records",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_<n>.jsonl --quality silver --dialect saudi --training-allowed\"",
            "make corpus-audit",
            "make phase22-readiness",
        ),
        blockers=tuple(blockers),
        notes=(
            "This gate is read-only and starts no training.",
            "Do not fill the corpus with AI-generated synthetic dialogue.",
            "Phase 22 must add MSA coverage before tokenizer v2.",
            "Saudi Seed v1 is a reference lexicon, not direct chat corpus.",
        ),
    )


def build_phase22_collection_plan(
    project_dir: str | Path | None = None,
    *,
    batch_size: int = 25,
) -> Phase22CollectionPlan:
    """Return a concrete collection plan without creating any dialogue data."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    decision = build_phase22_readiness_decision(project_dir)
    quota_by_dialect = {
        dialect: shortfall
        for dialect, shortfall in decision.dialect_shortfalls.items()
        if shortfall > 0
    }
    required_minimums = sum(quota_by_dialect.values())
    flexible = max(0, decision.remaining_records - required_minimums)
    estimated_batches = ceil(decision.remaining_records / batch_size) if decision.remaining_records else 0

    mix: list[str] = []
    for dialect, count in sorted(quota_by_dialect.items()):
        batches = ceil(count / batch_size)
        mix.append(f"{batches} batch(es) for {dialect} minimum coverage ({count} records)")
    if flexible:
        mix.append(f"{ceil(flexible / batch_size)} flexible batch(es) after minimums ({flexible} records)")
    if not mix:
        mix.append("minimum quotas already satisfied")
    planned_batches = _build_phase22_planned_batches(
        quota_by_dialect=quota_by_dialect,
        flexible_records=flexible,
        batch_size=batch_size,
    )

    return Phase22CollectionPlan(
        phase="Phase 22 — Gold Dialogue Corpus v2 Collection Plan",
        status=(
            "COLLECTION_COMPLETE_READY_FOR_PHASE23_RECHECK"
            if decision.can_start_phase23
            else "COLLECT_REVIEWED_MSA_SAUDI_DIALOGUE_BATCHES"
        ),
        corpus_path=decision.corpus_path,
        current_records=decision.training_records,
        target_records=decision.target_records,
        remaining_records=decision.remaining_records,
        batch_size=batch_size,
        estimated_batches=estimated_batches,
        quota_by_dialect=quota_by_dialect,
        flexible_records_after_minimums=flexible,
        recommended_batch_mix=tuple(mix),
        review_rules=(
            "Only user-authored or user-approved dialogue enters corpus.",
            "No synthetic LLM data.",
            "Every record needs source, license, quality, dialect, and training_allowed=true.",
            "Sensitive medical/legal/finance/security/religion records stay out of general chat corpus.",
            "Keep current dialect scope to msa + saudi only.",
        ),
        next_commands=(
            "export reviewed sessions from /ui/chat using the تصدير button",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl --quality silver --dialect msa --training-allowed\"",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_saudi_001.jsonl --quality silver --dialect saudi --training-allowed\"",
            "make corpus-audit",
            "make phase22-readiness",
        ),
        planned_batches=planned_batches,
        synthetic_llm_data_allowed=False,
        notes=(
            "This plan is read-only and does not generate corpus records.",
            "The fastest useful path is to add MSA first, because current corpus is Saudi-only.",
            "Phase 23 remains blocked until phase22-readiness passes.",
        ),
    )


def _build_phase22_planned_batches(
    *,
    quota_by_dialect: dict[str, int],
    flexible_records: int,
    batch_size: int,
) -> tuple[Phase22PlannedBatch, ...]:
    """Build a deterministic batch-by-batch checklist without writing data."""
    batches: list[Phase22PlannedBatch] = []
    dialect_batch_counts: dict[str, int] = {}

    for dialect in REQUIRED_DIALECTS:
        count = quota_by_dialect.get(dialect, 0)
        while count > 0:
            target = min(batch_size, count)
            dialect_batch_counts[dialect] = dialect_batch_counts.get(dialect, 0) + 1
            index = dialect_batch_counts[dialect]
            batches.append(
                _planned_batch(
                    sequence=len(batches) + 1,
                    batch_id=f"{dialect}_{index:03d}",
                    dialect=dialect,
                    target_records=target,
                    priority=f"minimum_{dialect}",
                )
            )
            count -= target

    flexible_index = 0
    remaining_flexible = flexible_records
    while remaining_flexible > 0:
        target = min(batch_size, remaining_flexible)
        flexible_index += 1
        batches.append(
            _planned_batch(
                sequence=len(batches) + 1,
                batch_id=f"flex_{flexible_index:03d}",
                dialect="msa_or_saudi",
                target_records=target,
                priority="flexible_after_minimums",
            )
        )
        remaining_flexible -= target

    return tuple(batches)


def _planned_batch(
    *,
    sequence: int,
    batch_id: str,
    dialect: str,
    target_records: int,
    priority: str,
) -> Phase22PlannedBatch:
    suggested_output_path = (
        f"data/corpus/chat/jsonl/dialogue_batch_v2_{batch_id}.jsonl"
    )
    command_dialect = "msa" if dialect == "msa_or_saudi" else dialect
    command = (
        "make prepare-dialogue-batch "
        "ARGS=\"--input data/corpus/chat/review/<exported_file>.jsonl "
        f"--out {suggested_output_path} "
        "--quality silver "
        f"--dialect {command_dialect} "
        "--training-allowed\""
    )
    task_dialect = {
        "msa": "اكتب/راجع حوارات عربية فصحى طبيعية.",
        "saudi": "اكتب/راجع حوارات سعودية طبيعية من استخدامك أنت.",
        "msa_or_saudi": "اكتب/راجع حوارات فصحى أو سعودية حسب النقص بعد الحد الأدنى.",
    }.get(dialect, "اكتب/راجع حوارات عربية ضمن نطاق المشروع.")
    return Phase22PlannedBatch(
        sequence=sequence,
        batch_id=batch_id,
        dialect=dialect,
        target_records=target_records,
        priority=priority,
        suggested_review_path="data/corpus/chat/review/<exported_file>.jsonl",
        suggested_output_path=suggested_output_path,
        prepare_command=command,
        user_task=(
            f"{task_dialect} الهدف {target_records} سجلًا، "
            "كلها user-authored أو user-approved، بدون synthetic LLM data."
        ),
    )
