"""Read-only Phase 22 readiness for Gold Dialogue Corpus v2.

Phase 22 is data work, not model training. This gate tells us whether the
governed chat corpus is large and balanced enough to justify tokenizer v2.
It never generates data and never writes training artifacts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from math import ceil
from pathlib import Path

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.corpus_governance import audit_jsonl_directory_for_training


TARGET_RECORDS = 500
MIN_PER_DIALECT = 200
REQUIRED_DIALECTS = ("msa", "saudi")
REQUIRED_QUALITIES = ("gold", "silver")
AUTHORING_BANK_PATH = Path("resources/phase22_authoring/msa_prompt_bank_v1.json")


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
class Phase22CompletionGate:
    phase: str
    status: str
    can_advance_phase23: bool
    readiness_status: str
    corpus_path: str
    training_records: int
    target_records: int
    remaining_records: int
    dialect_counts: dict[str, int]
    dialect_shortfalls: dict[str, int]
    current_next_batch: str | None
    completion_checks: dict[str, bool]
    missing_requirements: tuple[str, ...]
    required_before_advance: tuple[str, ...]
    notes: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["missing_requirements"] = list(self.missing_requirements)
        data["required_before_advance"] = list(self.required_before_advance)
        data["notes"] = list(self.notes)
        return data


@dataclass(frozen=True)
class Phase22NextBatchBrief:
    phase: str
    status: str
    next_batch: Phase22PlannedBatch | None
    why_this_batch: str
    acceptance_checklist: tuple[str, ...]
    suggested_topics: tuple[str, ...]
    ui_instructions: tuple[str, ...]
    after_export_commands: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["next_batch"] = self.next_batch.to_json() if self.next_batch else None
        data["acceptance_checklist"] = list(self.acceptance_checklist)
        data["suggested_topics"] = list(self.suggested_topics)
        data["ui_instructions"] = list(self.ui_instructions)
        data["after_export_commands"] = list(self.after_export_commands)
        data["warnings"] = list(self.warnings)
        return data


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
        else "COLLECT_OWNER_APPROVED_MSA_SAUDI_DIALOGUES"
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
            "write or collect owner-approved MSA/Saudi dialogue records with full provenance",
            "review exported JSONL manually; keep only user-authored/user-approved/owner-delegated records",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_<n>.jsonl --quality silver --dialect saudi --training-allowed\"",
            "make corpus-audit",
            "make phase22-readiness",
        ),
        blockers=tuple(blockers),
        notes=(
            "This gate is read-only and starts no training.",
            "Do not fill the corpus with external or unprovenanced synthetic dialogue.",
            "Owner-delegated agent-authored records are allowed only with transparent provenance.",
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

    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
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
        corpus_path=root / decision.corpus_path,
    )
    first_output = (
        planned_batches[0].suggested_output_path
        if planned_batches
        else "data/corpus/chat/jsonl/<no_batches_remaining>.jsonl"
    )
    first_dialect = (
        "msa"
        if planned_batches and planned_batches[0].dialect == "msa_or_saudi"
        else planned_batches[0].dialect
        if planned_batches
        else "msa"
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
            "Only user-authored, user-approved, or owner-delegated agent-authored dialogue enters corpus.",
            "No external or unprovenanced synthetic LLM data.",
            "Owner-delegated agent-authored records must disclose source/license/notes.",
            "Every record needs source, license, quality, dialect, and training_allowed=true.",
            "Sensitive medical/legal/finance/security/religion records stay out of general chat corpus.",
            "Keep current dialect scope to msa + saudi only.",
        ),
        next_commands=(
            "write or export reviewed sessions, then convert only clean records",
            f"make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out {first_output} --quality silver --dialect {first_dialect} --training-allowed\"",
            "make corpus-audit",
            "make phase22-readiness",
        ),
        planned_batches=planned_batches,
        synthetic_llm_data_allowed=False,
        notes=(
            "This plan is read-only and does not generate corpus records.",
            "The fastest useful path is to keep filling MSA until its minimum coverage is met.",
            "Phase 23 remains blocked until phase22-readiness passes.",
        ),
    )


def build_phase22_next_batch_brief(
    project_dir: str | Path | None = None,
    *,
    batch_size: int = 25,
) -> Phase22NextBatchBrief:
    """Return the immediate authoring task for Phase 22 without creating data."""
    plan = build_phase22_collection_plan(project_dir, batch_size=batch_size)
    next_batch = plan.planned_batches[0] if plan.planned_batches else None
    if next_batch is None:
        return Phase22NextBatchBrief(
            phase="Phase 22 — Next Batch Brief",
            status="NO_BATCHES_REMAINING_RECHECK_READINESS",
            next_batch=None,
            why_this_batch="All planned batches are complete according to the current readiness gate.",
            acceptance_checklist=(),
            suggested_topics=(),
            ui_instructions=(),
            after_export_commands=("make phase22-readiness",),
            warnings=("Do not start Phase 23 until phase22-readiness passes.",),
        )

    return Phase22NextBatchBrief(
        phase="Phase 22 — Next Batch Brief",
        status="AUTHOR_NEXT_REVIEW_BATCH",
        next_batch=next_batch,
        why_this_batch=_why_batch_is_next(next_batch),
        acceptance_checklist=(
            f"Collect exactly {next_batch.target_records} reviewed dialogue records for this batch.",
            "Each record must be user-authored, explicitly user-approved, or owner-delegated agent-authored.",
            "Each record must contain at least one user turn and one assistant turn.",
            "Prefer sessions with at least 3 user turns and 3 assistant turns before export.",
            "Keep dialect inside the current scope: msa or saudi only.",
            "Use quality=silver unless the record is manually reviewed as gold.",
            "Keep medical/legal/finance/security/religion content out of this general chat corpus.",
            "No raw sf_10m_v0_1 output enters quality training data.",
        ),
        suggested_topics=_suggested_topics(next_batch.dialect),
        ui_instructions=(
            "Open http://127.0.0.1:8123/ui/chat.",
            "Keep the stable UI on generator=template; this is corpus collection, not generator evaluation.",
            "Write or review natural conversations in the requested dialect.",
            "Watch the جودة التصدير panel; export only when the score is useful for review.",
            "Save the exported JSONL under data/corpus/chat/review/ for manual review.",
        ),
        after_export_commands=(
            "make phase22-review-intake",
            next_batch.prepare_command,
            "make corpus-audit",
            "make phase22-readiness",
        ),
        warnings=(
            "This brief is not training data.",
            "Suggested topics are prompts for authoring/review; they are not corpus records by themselves.",
            "Do not run tokenizer or model training during this step.",
        ),
    )


def build_phase22_completion_gate(
    project_dir: str | Path | None = None,
    *,
    batch_size: int = 25,
) -> Phase22CompletionGate:
    """Strict Phase 22 completion gate; read-only and training-free."""
    decision = build_phase22_readiness_decision(project_dir)
    plan = build_phase22_collection_plan(project_dir, batch_size=batch_size)
    brief = build_phase22_next_batch_brief(project_dir, batch_size=batch_size)
    current_next_batch = brief.next_batch.batch_id if brief.next_batch else None

    completion_checks = {
        "corpus_target_met": decision.training_records >= decision.target_records,
        "no_corpus_governance_issues": decision.corpus_issue_count == 0,
        "required_dialects_present": not decision.missing_required_dialects,
        "dialect_balance_met": all(
            shortfall == 0 for shortfall in decision.dialect_shortfalls.values()
        ),
        "gold_or_silver_quality_present": any(
            decision.quality_counts.get(q, 0) > 0 for q in REQUIRED_QUALITIES
        ),
        "synthetic_llm_data_forbidden": decision.synthetic_llm_data_allowed is False,
        "collection_plan_available": plan.estimated_batches >= 0,
        "next_batch_brief_available": bool(current_next_batch) or decision.can_start_phase23,
        "phase23_blocked_until_ready": decision.can_start_phase23 is False
        or decision.status == "READY_FOR_PHASE23_TOKENIZER_V2",
    }

    missing = list(decision.blockers)
    if current_next_batch:
        missing.append(f"complete_next_batch:{current_next_batch}")
    if not completion_checks["collection_plan_available"]:
        missing.append("phase22_collection_plan_unavailable")
    if not completion_checks["next_batch_brief_available"]:
        missing.append("phase22_next_batch_brief_unavailable")

    can_advance = decision.can_start_phase23 and all(completion_checks.values())
    status = (
        "PHASE22_COMPLETE_READY_FOR_PHASE23"
        if can_advance
        else "PHASE22_INCOMPLETE_DO_NOT_ADVANCE"
    )

    return Phase22CompletionGate(
        phase="Phase 22 — Completion Gate",
        status=status,
        can_advance_phase23=can_advance,
        readiness_status=decision.status,
        corpus_path=decision.corpus_path,
        training_records=decision.training_records,
        target_records=decision.target_records,
        remaining_records=decision.remaining_records,
        dialect_counts=decision.dialect_counts,
        dialect_shortfalls=decision.dialect_shortfalls,
        current_next_batch=current_next_batch,
        completion_checks=completion_checks,
        missing_requirements=tuple(dict.fromkeys(missing)),
        required_before_advance=(
            "complete all planned Phase 22 batches with user-authored/user-approved records",
            "run make phase22-review-intake on review exports",
            "convert only reviewed exports with make prepare-dialogue-batch",
            "run make corpus-audit",
            "run make phase22-readiness",
            "run make phase22-completion-gate",
        ),
        notes=(
            "This gate is read-only and starts no training.",
            "Do not move to Phase 23 until status is PHASE22_COMPLETE_READY_FOR_PHASE23.",
            "Current Phase 22 scope remains msa + saudi only.",
            "Saudi Seed v1 remains a reference lexicon, not direct chat corpus.",
        ),
    )


def _build_phase22_planned_batches(
    *,
    quota_by_dialect: dict[str, int],
    flexible_records: int,
    batch_size: int,
    corpus_path: Path,
) -> tuple[Phase22PlannedBatch, ...]:
    """Build a deterministic batch-by-batch checklist without writing data."""
    batches: list[Phase22PlannedBatch] = []
    dialect_batch_counts: dict[str, int] = _existing_batch_indexes(corpus_path)

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

    flexible_index = dialect_batch_counts.get("flex", 0)
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
            "كلها user-authored أو user-approved أو owner-delegated، "
            "بدون synthetic LLM data خارجي أو مجهول."
        ),
    )


def _why_batch_is_next(batch: Phase22PlannedBatch) -> str:
    if batch.dialect == "msa":
        return "MSA coverage is below the Phase 22 minimum, so the first priority is filling msa minimum coverage."
    if batch.dialect == "saudi":
        return "Saudi coverage is below the Phase 22 minimum after MSA minimum batches."
    return "Minimum dialect coverage is planned first; flexible batches fill the remaining target toward 500 records."


def _existing_batch_indexes(corpus_path: Path) -> dict[str, int]:
    indexes = {"msa": 0, "saudi": 0, "flex": 0}
    if not corpus_path.exists():
        return indexes
    for path in corpus_path.glob("dialogue_batch_v2_*.jsonl"):
        stem = path.stem.removeprefix("dialogue_batch_v2_")
        parts = stem.rsplit("_", 1)
        if len(parts) != 2:
            continue
        dialect, raw_index = parts
        if dialect not in indexes or not raw_index.isdigit():
            continue
        indexes[dialect] = max(indexes[dialect], int(raw_index))
    return indexes


def _suggested_topics(dialect: str) -> tuple[str, ...]:
    if dialect == "msa":
        bank = _load_authoring_prompt_bank("msa")
        if bank:
            return bank
        return (
            "شرح الفرق بين runtime وtraining وtokenizer بلغة فصحى بسيطة.",
            "حوار عن تنظيم خطوة يومية في مشروع تقني.",
            "سؤال وجواب عن سبب جمع corpus قبل تدريب النموذج.",
            "حوار دعم قصير: المستخدم مرتبك والمساعد يطلب توضيحًا بأدب.",
            "طلب تلخيص قرار هندسي دون استخدام مصطلحات أجنبية كثيرة.",
            "حوار عن تفضيل العربية الفصحى والسعودية فقط في هذه المرحلة.",
        )
    if dialect == "saudi":
        return (
            "سؤال سعودي طبيعي عن وش الخطوة الجاية في المشروع.",
            "حوار قصير عن تجربة الواجهة ولماذا الردود الحالية قوالب.",
            "طلب توضيح سعودي للفرق بين القاموس وبيانات التدريب.",
            "حوار سعودي عن جمع محادثات من استخدام سامي اليومي.",
            "سؤال متابعة قصير مثل: يعني وش أسوي الحين؟",
            "حوار سعودي فيه تصحيح فهم بدون مبالغة أو وعود.",
        )
    return (
        "اختر فصحى أو سعودي حسب النقص الذي يظهر في phase22-readiness.",
        "غط موضوعات المشروع اليومية: خطة، تدريب، توكنزر، واجهة، مراجعة.",
        "اكتب حوارًا طبيعيًا من استخدام سامي، لا نصًا مصطنعًا للملء.",
    )


def _load_authoring_prompt_bank(dialect: str) -> tuple[str, ...]:
    """Load non-training authoring prompts for Phase 22, if present."""
    path = PROJECT_DIR / AUTHORING_BANK_PATH
    if not path.exists():
        return ()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ()
    if raw.get("training_allowed") is not False:
        return ()
    if raw.get("synthetic_llm_data") is not False:
        return ()
    dialects = raw.get("dialects")
    if not isinstance(dialects, dict):
        return ()
    items = dialects.get(dialect)
    if not isinstance(items, list):
        return ()
    prompts: list[str] = []
    for item in items:
        if isinstance(item, str) and item.strip():
            prompts.append(item.strip())
    return tuple(prompts)
