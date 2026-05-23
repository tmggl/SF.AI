"""ChatDataset — high-level wrapper for chat corpora.

Phase 5 features:
- Discovery: list JSONL files under a corpus subtree.
- Validation: run validate_jsonl_file across all of them.
- Streaming: iterate cleaned samples for downstream consumers (Phase 5.5
  tokenizer training, Phase 6 model training).
- Stats: count samples, lengths, role distribution.

The dataset is **read-only**. SF.AI never modifies user-provided files.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

from sf_ai.datasets.cleaners import SampleCleaner
from sf_ai.datasets.loaders import iter_chat_samples
from sf_ai.datasets.schemas import (
    ChatMessage,
    SimpleSample,
    StructuredSample,
)
from sf_ai.datasets.validators import ValidationReport, validate_jsonl_file


@dataclass
class DatasetStats:
    files: int = 0
    valid_samples: int = 0
    skipped_samples: int = 0
    user_messages: int = 0
    assistant_messages: int = 0
    system_messages: int = 0
    total_chars: int = 0
    issues_by_kind: dict[str, int] = field(default_factory=dict)

    def record_message(self, msg: ChatMessage) -> None:
        self.total_chars += len(msg.content)
        if msg.role == "user":
            self.user_messages += 1
        elif msg.role == "assistant":
            self.assistant_messages += 1
        elif msg.role == "system":
            self.system_messages += 1


class ChatDataset:
    def __init__(
        self,
        root: str | Path,
        cleaner: SampleCleaner | None = None,
    ) -> None:
        self.root = Path(root)
        self.cleaner = cleaner or SampleCleaner()

    # ----- discovery -----

    def jsonl_files(self) -> list[Path]:
        if not self.root.exists():
            return []
        return sorted(self.root.rglob("*.jsonl"))

    # ----- validation -----

    def validate_all(self) -> list[ValidationReport]:
        return [validate_jsonl_file(p) for p in self.jsonl_files()]

    # ----- streaming -----

    def iter_samples(
        self, *, clean: bool = True
    ) -> Iterator[SimpleSample | StructuredSample]:
        for path in self.jsonl_files():
            for sample in iter_chat_samples(path):
                if not clean:
                    yield sample
                    continue
                try:
                    yield self.cleaner.clean(sample)
                except ValueError:
                    # Cleaning emptied the sample; skip.
                    continue

    def iter_messages(self, *, clean: bool = True) -> Iterator[ChatMessage]:
        """Flatten samples into a single stream of ChatMessage rows."""
        for sample in self.iter_samples(clean=clean):
            if isinstance(sample, StructuredSample):
                yield from sample.messages
            else:
                yield from sample.to_messages()

    def iter_dialogue_texts(self, *, clean: bool = True) -> Iterator[str]:
        """Stream whole dialogues with explicit Arabic role markers.

        LM training needs to learn "user asks → assistant answers". Flattening
        every message independently teaches local phrasing but discards the
        conversational contract. This format keeps each sample together while
        staying plain UTF-8 text for the sovereign tokenizer/model stack.
        """
        for sample in self.iter_samples(clean=clean):
            messages = (
                sample.messages
                if isinstance(sample, StructuredSample)
                else sample.to_messages()
            )
            lines: list[str] = _dialect_condition_lines(sample)
            for msg in messages:
                content = msg.content.strip()
                if not content:
                    continue
                if msg.role == "user":
                    lines.append(f"المستخدم: {content}")
                elif msg.role == "assistant":
                    lines.append(f"المساعد: {content}")
                elif msg.role == "system":
                    lines.append(f"النظام: {content}")
            if lines:
                yield "\n".join(lines) + "\n"

    # ----- stats -----

    def stats(self) -> DatasetStats:
        stats = DatasetStats()
        for path in self.jsonl_files():
            stats.files += 1
            report = validate_jsonl_file(path)
            stats.skipped_samples += report.error_count
            for issue in report.issues:
                stats.issues_by_kind[issue.kind] = (
                    stats.issues_by_kind.get(issue.kind, 0) + 1
                )
            for sample in iter_chat_samples(path):
                stats.valid_samples += 1
                if isinstance(sample, StructuredSample):
                    for msg in sample.messages:
                        stats.record_message(msg)
                else:
                    for msg in sample.to_messages():
                        stats.record_message(msg)
        return stats


def _dialect_condition_lines(sample: SimpleSample | StructuredSample) -> list[str]:
    """Return a plain Arabic conditioning line for current MSA/Saudi training."""
    provenance = getattr(sample, "provenance", None)
    dialect = (getattr(provenance, "dialect", "") or "").strip().lower()
    if dialect == "msa":
        return ["النطاق: فصحى"]
    if dialect == "saudi":
        return ["النطاق: سعودي"]
    return []
