"""Phase 18 dialogue batch preparation.

Converts explicitly reviewed chat exports into training JSONL. Nothing here
learns from runtime chat automatically; callers must pass `training_allowed`
when they intend to write training data.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.core.nlp._lexicons import load_lexicon
from sf_ai.datasets.corpus_governance import detect_training_forbidden_operational_terms
from sf_ai.datasets.schemas import ChatMessage, StructuredSample, parse_record


ALLOWED_QUALITIES = frozenset({"gold", "silver", "bronze"})
ALLOWED_DIALECTS = frozenset({"msa", "saudi"})


@dataclass(frozen=True)
class PreparedDialogue:
    record: dict[str, Any]
    source_line: int


@dataclass
class DialogueBatchReport:
    input_path: str
    output_path: str
    total_records: int = 0
    written_records: int = 0
    skipped_records: int = 0
    training_allowed: bool = False
    quality: str = "silver"
    dialect: str = "saudi"
    skipped_reasons: dict[str, int] = field(default_factory=dict)

    def add_skip(self, reason: str) -> None:
        self.skipped_records += 1
        self.skipped_reasons[reason] = self.skipped_reasons.get(reason, 0) + 1

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def prepare_dialogue_batch(
    *,
    input_path: str | Path,
    output_path: str | Path,
    report_path: str | Path,
    source: str,
    license_name: str,
    dialect: str,
    quality: str,
    training_allowed: bool,
    owner_user_id: str = "sami-local",
    target_user_id: str | None = None,
    include_sensitive: bool = False,
) -> DialogueBatchReport:
    """Prepare reviewed dialogue JSONL for training.

    If `training_allowed` is false, no training output is written. A report is
    still written so the user can see what would be accepted.
    """
    if quality not in ALLOWED_QUALITIES:
        raise ValueError(f"quality must be one of {sorted(ALLOWED_QUALITIES)}")
    if dialect not in ALLOWED_DIALECTS:
        raise ValueError(f"dialect must be one of {sorted(ALLOWED_DIALECTS)}")

    input_path = Path(input_path)
    output_path = Path(output_path)
    report_path = Path(report_path)
    report = DialogueBatchReport(
        input_path=str(input_path),
        output_path=str(output_path),
        training_allowed=training_allowed,
        quality=quality,
        dialect=dialect,
    )

    prepared: list[PreparedDialogue] = []
    for line_no, raw in _iter_jsonl(input_path):
        report.total_records += 1
        try:
            sample = parse_record(raw)
        except Exception:
            report.add_skip("schema_invalid")
            continue

        messages = (
            sample.messages
            if isinstance(sample, StructuredSample)
            else sample.to_messages()
        )
        if not _has_user_and_assistant(messages):
            report.add_skip("missing_user_or_assistant")
            continue
        joined = "\n".join(m.content for m in messages)
        if not include_sensitive and _has_safety_terms(joined):
            report.add_skip("safety_flagged")
            continue
        if detect_training_forbidden_operational_terms(raw):
            report.add_skip("training_forbidden_operational_internal_dialogue")
            continue
        input_provenance = getattr(sample, "provenance", None)
        created_by_user_id = (
            getattr(input_provenance, "created_by_user_id", None)
            or getattr(input_provenance, "owner_user_id", None)
            or owner_user_id
        )
        effective_target_user_id = (
            target_user_id
            or getattr(input_provenance, "target_user_id", None)
            or owner_user_id
        )

        prepared.append(
            PreparedDialogue(
                source_line=line_no,
                record={
                    "domain": "chat",
                    "lang": "ar",
                    "messages": [
                        {"role": m.role, "content": m.content.strip()}
                        for m in messages
                        if m.content.strip()
                    ],
                    "provenance": {
                        "source": source,
                        "license": license_name,
                        "language": "ar",
                        "dialect": dialect,
                        "quality": quality,
                        "training_allowed": True,
                        "owner_user_id": owner_user_id,
                        "created_by_user_id": created_by_user_id,
                        "target_user_id": effective_target_user_id,
                        "user_scope": "single_user",
                        "notes": f"prepared_from_review_export_line:{line_no}",
                    },
                },
            )
        )

    report.written_records = len(prepared) if training_allowed else 0
    if training_allowed and prepared:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            for item in prepared:
                handle.write(json.dumps(item.record, ensure_ascii=False) + "\n")
    elif not training_allowed:
        report.add_skip("training_allowed_flag_missing")
        report.skipped_records -= 1

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report.to_json(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def _iter_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    if not path.exists():
        raise FileNotFoundError(path)
    out: list[tuple[int, dict[str, Any]]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            out.append((line_no, json.loads(line)))
    return out


def _has_user_and_assistant(messages: list[ChatMessage]) -> bool:
    roles = {m.role for m in messages}
    return "user" in roles and "assistant" in roles


def _has_safety_terms(text: str) -> bool:
    """Token/phrase safety check for data prep.

    The runtime scanner intentionally catches substrings for routing safety,
    but data preparation should avoid false positives such as the common
    prefix in "المحادثة". Single-word terms must match a full token here;
    multi-word terms are matched as phrases.
    """
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
