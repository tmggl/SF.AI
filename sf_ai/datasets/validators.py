"""Validators for SF.AI dialogue datasets.

Two entry points:

- ``validate_record(raw)`` — one record (already parsed JSON).
- ``validate_jsonl_file(path)`` — every non-blank line, returning a report.

The validators never raise on bad data; they collect issues so the caller
can decide whether to skip the file, drop the line, or stop ingestion.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sf_ai.datasets.schemas import parse_record


@dataclass(frozen=True)
class SampleIssue:
    line_number: int | None
    kind: str          # "json" | "schema" | "empty" | "encoding"
    message: str
    snippet: str = ""

    def describe(self) -> str:
        loc = f"line {self.line_number}" if self.line_number is not None else "record"
        return f"[{self.kind}] {loc}: {self.message}"


@dataclass
class ValidationReport:
    path: Path | None = None
    total_lines: int = 0
    valid_samples: int = 0
    issues: list[SampleIssue] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not self.issues

    @property
    def error_count(self) -> int:
        return len(self.issues)

    def summary(self) -> str:
        if self.path is None:
            target = "in-memory"
        else:
            target = str(self.path)
        return (
            f"{target} — {self.valid_samples}/{self.total_lines} valid, "
            f"{self.error_count} issue(s)"
        )


def validate_record(raw: Any, *, line_number: int | None = None) -> SampleIssue | None:
    """Return None if the record is valid, else a SampleIssue describing it."""
    try:
        parse_record(raw)
        return None
    except ValidationError as e:
        return SampleIssue(
            line_number=line_number,
            kind="schema",
            message=str(e.errors()[0]["msg"]) if e.errors() else "schema validation failed",
        )
    except ValueError as e:
        return SampleIssue(
            line_number=line_number,
            kind="schema",
            message=str(e),
        )


def validate_jsonl_file(path: str | Path, max_snippet: int = 80) -> ValidationReport:
    """Validate every non-blank line of a JSONL file.

    Empty/whitespace lines are skipped silently. UTF-8 is enforced.
    """
    path = Path(path)
    report = ValidationReport(path=path)

    if not path.exists():
        report.issues.append(
            SampleIssue(
                line_number=None,
                kind="encoding",
                message=f"file not found: {path}",
            )
        )
        return report

    try:
        handle = path.open("r", encoding="utf-8")
    except UnicodeDecodeError as e:
        report.issues.append(
            SampleIssue(line_number=None, kind="encoding", message=str(e))
        )
        return report

    with handle:
        for idx, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            report.total_lines += 1
            snippet = line.strip()[:max_snippet]
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as e:
                report.issues.append(
                    SampleIssue(
                        line_number=idx,
                        kind="json",
                        message=str(e.msg),
                        snippet=snippet,
                    )
                )
                continue

            issue = validate_record(raw, line_number=idx)
            if issue is None:
                report.valid_samples += 1
            else:
                # Re-attach snippet for context.
                report.issues.append(
                    SampleIssue(
                        line_number=issue.line_number,
                        kind=issue.kind,
                        message=issue.message,
                        snippet=snippet,
                    )
                )

    return report
