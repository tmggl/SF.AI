"""Inventory of local data/reference sources for the sovereign training plan.

This module separates three things that are easy to accidentally mix:

1. Chat dialogue JSONL ready for Phase 12/13 gates.
2. Saudi dialect task packs derived from the user's lexicon.
3. Private lexicon/reference payloads used for runtime lookup and future data work.

The inventory is deliberately metadata-only: counts, paths, eligibility, and
next actions. It does not publish or transform private data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.core.config import PROJECT_DIR
from sf_ai.datasets.corpus_governance import (
    CorpusGovernanceReport,
    audit_jsonl_directory_for_training,
)
from sf_ai.datasets.saudi_seed import SAUDI_SEED_JSONL, saudi_seed_stats


CHAT_JSONL_DIR = Path("data/corpus/chat/jsonl")
SAUDI_DIALECT_TASKS = Path(
    "data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl"
)
SAUDI_SEED_REFERENCE = Path(
    "resources/lexicons/imported/saudi_seed_v1/saudi_dialect_lexicon_full_seed_v1.jsonl"
)
MO3JAM_IMPORTED_DIR = Path("resources/lexicons/imported/mo3jam")


@dataclass(frozen=True)
class SourceInventoryItem:
    name: str
    path: str
    kind: str
    exists: bool
    records: int = 0
    valid_json_records: int = 0
    private_or_ignored: bool = False
    tracked_payload_allowed: bool = False
    phase12_tokenizer_candidate: bool = False
    phase13_lm_candidate: bool = False
    needs_conversion: bool = False
    needs_governance_audit: bool = True
    status: str = "missing"
    action_required: str = ""
    notes: tuple[str, ...] = ()
    stats: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceInventoryReport:
    chat_audit: CorpusGovernanceReport
    sources: tuple[SourceInventoryItem, ...]
    phase12_status: str
    blockers: tuple[str, ...]

    @property
    def source_count(self) -> int:
        return len(self.sources)

    @property
    def local_reference_records(self) -> int:
        return sum(
            item.records
            for item in self.sources
            if item.kind in {"lexicon_reference", "dialect_task_pack"}
        )

    @property
    def chat_training_records(self) -> int:
        return self.chat_audit.training_ready


def _count_jsonl(path: Path) -> tuple[int, int]:
    if not path.exists():
        return (0, 0)

    records = 0
    valid = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            records += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                continue
            valid += 1
    return records, valid


def build_source_inventory(project_dir: str | Path | None = None) -> SourceInventoryReport:
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR

    chat_dir = root / CHAT_JSONL_DIR
    chat_audit = audit_jsonl_directory_for_training(chat_dir)
    chat_ready = chat_audit.error_count == 0 and chat_audit.training_ready > 0

    sources: list[SourceInventoryItem] = [
        SourceInventoryItem(
            name="chat_training_jsonl",
            path=str(CHAT_JSONL_DIR),
            kind="chat_dialogue_corpus",
            exists=chat_dir.exists(),
            records=chat_audit.total_records,
            valid_json_records=chat_audit.total_records,
            private_or_ignored=True,
            tracked_payload_allowed=False,
            phase12_tokenizer_candidate=chat_ready,
            phase13_lm_candidate=chat_ready,
            needs_conversion=False,
            needs_governance_audit=True,
            status="ready" if chat_ready else "not_ready",
            action_required=(
                "ابدأ Phase 12 بعد إذن صريح."
                if chat_ready
                else "أضف ملفات JSONL حوارية فصحى/سعودية مع provenance كامل."
            ),
            notes=(
                "هذا هو المصدر الوحيد المعتمد الآن لتدريب tokenizer/LM دون تحويل.",
                "الملفات داخل هذا المسار خاصة وممنوعة من الرفع افتراضيًا.",
            ),
            stats={
                "training_ready": chat_audit.training_ready,
                "issues": chat_audit.error_count,
                "dialects": chat_audit.dialect_counts,
                "qualities": chat_audit.quality_counts,
            },
        )
    ]

    tasks_path = root / SAUDI_DIALECT_TASKS
    task_records, task_valid = _count_jsonl(tasks_path)
    tasks_ready = tasks_path.exists() and task_records > 0 and task_records == task_valid
    sources.append(
        SourceInventoryItem(
            name="saudi_dialect_training_tasks_seed_v1",
            path=str(SAUDI_DIALECT_TASKS),
            kind="dialect_task_pack",
            exists=tasks_path.exists(),
            records=task_records,
            valid_json_records=task_valid,
            private_or_ignored=True,
            tracked_payload_allowed=False,
            phase12_tokenizer_candidate=tasks_ready,
            phase13_lm_candidate=False,
            needs_conversion=True,
            needs_governance_audit=True,
            status="reference_ready" if tasks_ready else "missing_or_invalid",
            action_required=(
                "حوّله إلى schema حواري/تعليمي مع provenance قبل LM training."
                if tasks_ready
                else "أعد توليد أو أضف ملف مهام اللهجة السعودية."
            ),
            notes=(
                "هذا ليس chat corpus مباشرًا؛ هو مهام مشتقة من القاموس السعودي.",
                "يمكن استخدامه كمرشح tokenizer لأنه نص سعودي محلي، لكن LM يحتاج تحويلًا وحوكمة.",
            ),
        )
    )

    seed_path = root / SAUDI_SEED_REFERENCE
    seed_stats = saudi_seed_stats(seed_path if seed_path.exists() else SAUDI_SEED_JSONL)
    sources.append(
        SourceInventoryItem(
            name="saudi_seed_v1_lexicon_reference",
            path=str(SAUDI_SEED_REFERENCE),
            kind="lexicon_reference",
            exists=seed_path.exists(),
            records=seed_stats.entries_total,
            valid_json_records=seed_stats.entries_total,
            private_or_ignored=True,
            tracked_payload_allowed=False,
            phase12_tokenizer_candidate=False,
            phase13_lm_candidate=False,
            needs_conversion=True,
            needs_governance_audit=True,
            status="reference_ready" if seed_stats.entries_total else "missing",
            action_required=(
                "استخدمه كمرجع لهجي وكمصدر لتوليد مهام مشتقة محكومة، لا كحوار مباشر."
                if seed_stats.entries_total
                else "أضف القاموس الخاص محليًا إن لم يكن موجودًا."
            ),
            notes=(
                "القاموس السعودي الخاص موجود محليًا وممنوع رفع payload الكامل.",
                "runtime-safe subset فقط يدخل DialectMapper.",
            ),
            stats={
                "safe_runtime": seed_stats.entries_safe_runtime,
                "by_confidence": seed_stats.by_confidence,
                "by_dialect": seed_stats.by_dialect,
                "sensitive_count": seed_stats.sensitive_count,
                "requires_review_count": seed_stats.requires_review_count,
            },
        )
    )

    mo3jam_dir = root / MO3JAM_IMPORTED_DIR
    mo3jam_payloads = [
        p
        for p in mo3jam_dir.glob("*")
        if p.is_file() and p.name != ".gitkeep"
    ] if mo3jam_dir.exists() else []
    sources.append(
        SourceInventoryItem(
            name="mo3jam_saudi_import_slot",
            path=str(MO3JAM_IMPORTED_DIR),
            kind="external_lexicon_slot",
            exists=mo3jam_dir.exists(),
            records=len(mo3jam_payloads),
            valid_json_records=0,
            private_or_ignored=True,
            tracked_payload_allowed=False,
            phase12_tokenizer_candidate=False,
            phase13_lm_candidate=False,
            needs_conversion=True,
            needs_governance_audit=True,
            status="empty_permission_gated" if not mo3jam_payloads else "needs_review",
            action_required=(
                "لا تستورد من Mo3jam إلا بإذن صريح وتشغيل importer permission-gated."
            ),
            notes=(
                "المجلد مخصص للاستيراد المستقبلي فقط.",
                "Crawler/importer يبقى permission-gated.",
            ),
        )
    )

    blockers: list[str] = []
    if not chat_ready:
        blockers.append("لا يوجد chat JSONL جاهز بتنسيق Phase 11.")
    if tasks_ready:
        blockers.append(
            "يوجد ملف مهام سعودي محلي، لكنه يحتاج تحويل/حوكمة قبل استخدامه كـ LM corpus."
        )
    if seed_stats.entries_total:
        blockers.append(
            "يوجد قاموس سعودي محلي خاص؛ يستخدم كمرجع، ولا يرفع ولا يدخل كحوار مباشر."
        )

    return SourceInventoryReport(
        chat_audit=chat_audit,
        sources=tuple(sources),
        phase12_status=(
            "READY_FOR_PHASE_12_TOKENIZER_TRAINING"
            if chat_ready
            else "NOT_READY_FOR_TRAINING"
        ),
        blockers=tuple(blockers),
    )
