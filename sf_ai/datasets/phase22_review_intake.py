"""Read-only Phase 22 review-export intake scanner.

This module inspects files exported from the chat UI review area and explains
which ones are candidates for manual conversion into governed training JSONL.
It never writes corpus records and never changes training artifacts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.core.config import PROJECT_DIR
from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.datasets.schemas import StructuredSample, parse_record

REVIEW_DIR = Path("data/corpus/chat/review")
ALLOWED_DIALECTS = ("msa", "saudi")


@dataclass(frozen=True)
class ReviewExportItem:
    path: str
    records: int
    valid_json_records: int
    schema_valid_records: int
    records_with_user_and_assistant: int
    training_allowed_false: int
    training_allowed_true: int
    training_allowed_missing: int
    raw_generator_assistant_records: int
    safety_flagged_estimate: int
    user_turns: int
    assistant_turns: int
    dialogue_quality_score: int
    dialogue_quality_label: str
    status: str
    dialogue_quality_blockers: tuple[str, ...] = field(default_factory=tuple)
    recommended_actions: tuple[str, ...] = field(default_factory=tuple)
    suggested_msa_command: str = ""
    suggested_saudi_command: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["recommended_actions"] = list(self.recommended_actions)
        data["notes"] = list(self.notes)
        return data


@dataclass(frozen=True)
class Phase22ReviewIntakeReport:
    phase: str
    status: str
    review_path: str
    review_files: int
    candidate_files: int
    total_review_records: int
    total_valid_json_records: int
    total_schema_valid_records: int
    total_user_assistant_records: int
    total_raw_generator_assistant_records: int
    total_safety_flagged_estimate: int
    average_dialogue_quality_score: float
    synthetic_llm_data_allowed: bool
    files: tuple[ReviewExportItem, ...]
    recommended_next_commands: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["files"] = [item.to_json() for item in self.files]
        data["recommended_next_commands"] = list(self.recommended_next_commands)
        data["notes"] = list(self.notes)
        return data


def build_phase22_review_intake_report(
    project_dir: str | Path | None = None,
    *,
    review_dir: str | Path | None = None,
    max_files: int | None = None,
) -> Phase22ReviewIntakeReport:
    """Scan review exports and return a read-only intake report."""
    root = Path(project_dir) if project_dir is not None else PROJECT_DIR
    review_path = Path(review_dir) if review_dir is not None else root / REVIEW_DIR
    if not review_path.is_absolute():
        review_path = root / review_path

    files = sorted(review_path.glob("*.jsonl")) if review_path.exists() else []
    if max_files is not None:
        files = files[:max(0, max_files)]

    items = tuple(_scan_review_file(path, root=root) for path in files)
    candidate_count = sum(1 for item in items if item.status == "candidate_review_export")
    total_records = sum(item.records for item in items)
    valid_json_records = sum(item.valid_json_records for item in items)
    schema_valid_records = sum(item.schema_valid_records for item in items)
    user_assistant_records = sum(item.records_with_user_and_assistant for item in items)
    safety_flagged = sum(item.safety_flagged_estimate for item in items)
    raw_generator_records = sum(item.raw_generator_assistant_records for item in items)
    avg_quality = (
        round(sum(item.dialogue_quality_score for item in items) / len(items), 2)
        if items
        else 0.0
    )

    if not items:
        status = "NO_REVIEW_EXPORTS_FOUND"
    elif any(item.training_allowed_true for item in items):
        status = "REVIEW_EXPORT_HAS_TRAINING_ALLOWED_TRUE"
    elif raw_generator_records:
        status = "REVIEW_EXPORT_HAS_RAW_GENERATOR_OUTPUT"
    elif candidate_count:
        status = "REVIEW_EXPORTS_READY_FOR_MANUAL_REVIEW"
    else:
        status = "NO_CANDIDATE_REVIEW_EXPORTS"

    return Phase22ReviewIntakeReport(
        phase="Phase 22 — Gold Dialogue Corpus v2 Review Intake",
        status=status,
        review_path=str(review_path.relative_to(root)) if _is_relative_to(review_path, root) else str(review_path),
        review_files=len(items),
        candidate_files=candidate_count,
        total_review_records=total_records,
        total_valid_json_records=valid_json_records,
        total_schema_valid_records=schema_valid_records,
        total_user_assistant_records=user_assistant_records,
        total_raw_generator_assistant_records=raw_generator_records,
        total_safety_flagged_estimate=safety_flagged,
        average_dialogue_quality_score=avg_quality,
        synthetic_llm_data_allowed=False,
        files=items,
        recommended_next_commands=(
            "make phase22-review-intake",
            "manually review candidate files; keep only Sami-authored or Sami-approved dialogue",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_msa_002.jsonl --quality silver --dialect msa --training-allowed\"",
            "make prepare-dialogue-batch ARGS=\"--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_saudi_001.jsonl --quality silver --dialect saudi --training-allowed\"",
            "make corpus-audit && make phase22-readiness",
        ),
        notes=(
            "This report is read-only and does not prepare training JSONL.",
            "Review exports must normally keep training_allowed=false until manual approval.",
            "Exports containing sf_10m_v0_1/sf_10m_v0_2 raw output are review evidence, not quality training candidates.",
            "Quality score estimates whether a review export is useful for the next dialogue-training corpus.",
            "Allowed dialect targets remain msa + saudi only.",
            "Saudi Seed v1 remains a reference lexicon, not direct chat corpus.",
        ),
    )


def _scan_review_file(path: Path, *, root: Path) -> ReviewExportItem:
    records = 0
    valid_json = 0
    schema_valid = 0
    with_user_and_assistant = 0
    training_false = 0
    training_true = 0
    training_missing = 0
    raw_generator_records = 0
    safety_flagged = 0
    user_turns = 0
    assistant_turns = 0
    user_chars = 0
    assistant_chars = 0
    notes: list[str] = []

    if not path.exists():
        return ReviewExportItem(
            path=str(path),
            records=0,
            valid_json_records=0,
            schema_valid_records=0,
            records_with_user_and_assistant=0,
            training_allowed_false=0,
            training_allowed_true=0,
            training_allowed_missing=0,
            raw_generator_assistant_records=0,
            safety_flagged_estimate=0,
            user_turns=0,
            assistant_turns=0,
            dialogue_quality_score=0,
            dialogue_quality_label="missing",
            dialogue_quality_blockers=("missing_file",),
            status="missing",
            recommended_actions=("check the review export path",),
        )

    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            records += 1
            try:
                raw = json.loads(line)
            except json.JSONDecodeError:
                notes.append(f"line:{line_no}:invalid_json")
                continue

            valid_json += 1
            try:
                sample = parse_record(raw)
            except Exception:
                notes.append(f"line:{line_no}:schema_invalid")
                continue

            schema_valid += 1
            if _contains_raw_generator_output(raw):
                raw_generator_records += 1
                notes.append(f"line:{line_no}:contains_raw_sf10m_output")
            messages = sample.messages if isinstance(sample, StructuredSample) else sample.to_messages()
            if _has_user_and_assistant(messages):
                with_user_and_assistant += 1
            else:
                notes.append(f"line:{line_no}:missing_user_or_assistant")

            joined = "\n".join(str(m.content) for m in messages)
            if _has_safety_terms(joined):
                safety_flagged += 1

            for msg in messages:
                content = str(getattr(msg, "content", "")).strip()
                if getattr(msg, "role", "") == "user":
                    user_turns += 1
                    user_chars += len(content)
                elif getattr(msg, "role", "") == "assistant":
                    assistant_turns += 1
                    assistant_chars += len(content)

            provenance = getattr(sample, "provenance", None)
            training_allowed = getattr(provenance, "training_allowed", None) if provenance is not None else None
            if training_allowed is True:
                training_true += 1
                notes.append(f"line:{line_no}:review_export_training_allowed_true")
            elif training_allowed is False:
                training_false += 1
            else:
                training_missing += 1
                notes.append(f"line:{line_no}:training_allowed_missing")

    if records == 0:
        status = "empty_or_invalid"
    elif training_true:
        status = "review_payload_should_not_be_training_allowed"
    elif raw_generator_records:
        status = "raw_generator_review_export_not_training_candidate"
    elif schema_valid == 0 or with_user_and_assistant == 0:
        status = "not_candidate_needs_schema_or_roles"
    elif safety_flagged == schema_valid:
        status = "needs_sensitive_review"
    else:
        status = "candidate_review_export"

    rel = str(path.relative_to(root)) if _is_relative_to(path, root) else str(path)
    quality_score, quality_label, quality_blockers = _dialogue_quality(
        schema_valid=schema_valid,
        with_user_and_assistant=with_user_and_assistant,
        user_turns=user_turns,
        assistant_turns=assistant_turns,
        user_chars=user_chars,
        assistant_chars=assistant_chars,
        training_true=training_true,
        training_missing=training_missing,
        raw_generator_records=raw_generator_records,
        safety_flagged=safety_flagged,
    )
    return ReviewExportItem(
        path=rel,
        records=records,
        valid_json_records=valid_json,
        schema_valid_records=schema_valid,
        records_with_user_and_assistant=with_user_and_assistant,
        training_allowed_false=training_false,
        training_allowed_true=training_true,
        training_allowed_missing=training_missing,
        raw_generator_assistant_records=raw_generator_records,
        safety_flagged_estimate=safety_flagged,
        user_turns=user_turns,
        assistant_turns=assistant_turns,
        dialogue_quality_score=quality_score,
        dialogue_quality_label=quality_label,
        dialogue_quality_blockers=quality_blockers,
        status=status,
        recommended_actions=_recommended_actions(path=rel, status=status),
        suggested_msa_command=_prepare_command(rel, "msa"),
        suggested_saudi_command=_prepare_command(rel, "saudi"),
        notes=tuple(notes[:20]),
    )


def _recommended_actions(*, path: str, status: str) -> tuple[str, ...]:
    if status == "candidate_review_export":
        return (
            "review manually for ownership, quality, and dialect",
            f"convert only after approval: {path}",
            "run corpus-audit after conversion",
        )
    if status == "review_payload_should_not_be_training_allowed":
        return (
            "keep review exports as training_allowed=false until manual approval",
            "re-export or correct provenance before conversion",
        )
    if status == "raw_generator_review_export_not_training_candidate":
        return (
            "keep this file as lab evidence only",
            "do not convert raw SF-10M output into quality dialogue training data",
            "collect a new template or human-approved session for Phase 22 corpus",
        )
    if status == "needs_sensitive_review":
        return (
            "review sensitive records manually",
            "exclude medical/legal/finance/security/religion content from general chat corpus",
        )
    return ("fix JSONL schema or export a fresh review file from /ui/chat",)


def _prepare_command(path: str, dialect: str) -> str:
    if dialect not in ALLOWED_DIALECTS:
        raise ValueError(f"dialect must be one of {ALLOWED_DIALECTS}")
    suffix = "msa" if dialect == "msa" else "saudi"
    return (
        "make prepare-dialogue-batch "
        f"ARGS=\"--input {path} "
        f"--out data/corpus/chat/jsonl/dialogue_batch_v2_{suffix}_001.jsonl "
        f"--quality silver --dialect {dialect} --training-allowed\""
    )


def _has_user_and_assistant(messages: list[Any]) -> bool:
    roles = {getattr(m, "role", "") for m in messages}
    return "user" in roles and "assistant" in roles


def _contains_raw_generator_output(raw: dict[str, Any]) -> bool:
    review_meta = raw.get("review_metadata") if isinstance(raw, dict) else None
    if isinstance(review_meta, dict):
        counts = review_meta.get("assistant_generator_counts") or {}
        if int(counts.get("sf_10m_v0_1") or 0) > 0:
            return True
        if int(counts.get("sf_10m_v0_2") or 0) > 0:
            return True
        if review_meta.get("contains_raw_generator_output") is True:
            return True

    messages = raw.get("messages") if isinstance(raw, dict) else None
    if not isinstance(messages, list):
        return False
    for message in messages:
        if not isinstance(message, dict):
            continue
        if message.get("role") == "assistant" and message.get("generator") in {
            "sf_10m_v0_1",
            "sf_10m_v0_2",
        }:
            return True
    return False


def _dialogue_quality(
    *,
    schema_valid: int,
    with_user_and_assistant: int,
    user_turns: int,
    assistant_turns: int,
    user_chars: int,
    assistant_chars: int,
    training_true: int,
    training_missing: int,
    raw_generator_records: int,
    safety_flagged: int,
) -> tuple[int, str, tuple[str, ...]]:
    score = 100
    blockers: list[str] = []
    if schema_valid == 0:
        score -= 60
        blockers.append("schema_invalid")
    if with_user_and_assistant == 0:
        score -= 50
        blockers.append("missing_user_or_assistant")
    if raw_generator_records:
        score -= 60
        blockers.append("contains_raw_generator_output")
    if safety_flagged:
        score -= 35
        blockers.append("safety_review_required")
    if training_true:
        score -= 25
        blockers.append("review_export_has_training_allowed_true")
    if training_missing:
        score -= 10
        blockers.append("training_allowed_missing")
    if user_turns < 3:
        score -= 20
        blockers.append("needs_at_least_3_user_turns")
    if assistant_turns < 3:
        score -= 20
        blockers.append("needs_at_least_3_assistant_turns")

    avg_user = user_chars / user_turns if user_turns else 0
    avg_assistant = assistant_chars / assistant_turns if assistant_turns else 0
    if avg_user < 12:
        score -= 8
        blockers.append("user_turns_too_short")
    if avg_assistant < 35:
        score -= 12
        blockers.append("assistant_turns_too_short")

    score = max(0, min(100, score))
    if score >= 85 and not blockers:
        label = "gold_candidate"
    elif score >= 70:
        label = "silver_candidate"
    elif score >= 45:
        label = "needs_more_turns_or_review"
    else:
        label = "not_training_quality_candidate"
    return score, label, tuple(blockers)


def _has_safety_terms(text: str) -> bool:
    data = load_lexicon("safety_terms.yaml") or {}
    flags = data.get("flags") or {}
    lowered = text.lower()
    tokens = set(text.split()) | set(lowered.split())
    for terms in flags.values():
        for term in terms or ():
            needle = str(term).strip()
            if not needle:
                continue
            if " " in needle:
                if needle in text or needle.lower() in lowered:
                    return True
            elif needle in tokens or needle.lower() in tokens:
                return True
    return False


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
