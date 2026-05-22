"""Phase 11 corpus governance checks for sovereign LM training.

Schema validation answers: "is this JSONL structurally valid?"
Governance answers: "is this sample allowed into the first Saudi/MSA training
pack for a sovereign generative model?"
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sf_ai.datasets.schemas import SimpleSample, StructuredSample, parse_record
from sf_ai.datasets.validators import SampleIssue, validate_record


TRAINING_LANGS: frozenset[str] = frozenset({"ar"})
TRAINING_DIALECTS: frozenset[str] = frozenset({"msa", "saudi"})
TRAINING_QUALITIES: frozenset[str] = frozenset({"gold", "silver", "bronze"})


@dataclass
class CorpusGovernanceReport:
    path: Path | None = None
    total_records: int = 0
    training_ready: int = 0
    issues: list[SampleIssue] = field(default_factory=list)
    dialect_counts: dict[str, int] = field(default_factory=dict)
    quality_counts: dict[str, int] = field(default_factory=dict)
    source_counts: dict[str, int] = field(default_factory=dict)

    @property
    def is_clean(self) -> bool:
        return not self.issues

    @property
    def error_count(self) -> int:
        return len(self.issues)

    def summary(self) -> str:
        target = "in-memory" if self.path is None else str(self.path)
        return (
            f"{target} — {self.training_ready}/{self.total_records} "
            f"training-ready, {self.error_count} governance issue(s)"
        )


def _issue(line_number: int | None, message: str, snippet: str = "") -> SampleIssue:
    return SampleIssue(
        line_number=line_number,
        kind="governance",
        message=message,
        snippet=snippet,
    )


def audit_record_for_training(
    raw: Any,
    *,
    line_number: int | None = None,
    max_snippet: int = 80,
) -> list[SampleIssue]:
    """Return governance issues for one already-parsed JSON record."""
    schema_issue = validate_record(raw, line_number=line_number)
    if schema_issue is not None:
        return [schema_issue]

    sample = parse_record(raw)
    snippet = json.dumps(raw, ensure_ascii=False)[:max_snippet]
    issues: list[SampleIssue] = []

    provenance = sample.provenance
    if provenance is None:
        issues.append(_issue(line_number, "missing provenance", snippet))
        return issues

    if not provenance.source:
        issues.append(_issue(line_number, "missing provenance.source", snippet))
    if not provenance.license:
        issues.append(_issue(line_number, "missing provenance.license", snippet))

    language = provenance.language or (
        sample.lang if isinstance(sample, StructuredSample) else None
    )
    if language not in TRAINING_LANGS:
        issues.append(
            _issue(
                line_number,
                f"language must be one of {sorted(TRAINING_LANGS)}, got {language!r}",
                snippet,
            )
        )

    dialect = provenance.dialect
    if dialect not in TRAINING_DIALECTS:
        issues.append(
            _issue(
                line_number,
                f"dialect must be one of {sorted(TRAINING_DIALECTS)}, got {dialect!r}",
                snippet,
            )
        )

    quality = provenance.quality
    if quality not in TRAINING_QUALITIES:
        issues.append(
            _issue(
                line_number,
                f"quality must be one of {sorted(TRAINING_QUALITIES)}, got {quality!r}",
                snippet,
            )
        )

    if isinstance(sample, StructuredSample) and sample.domain != "chat":
        issues.append(_issue(line_number, "Phase 11 accepts chat domain only", snippet))

    messages = (
        sample.messages if isinstance(sample, StructuredSample) else sample.to_messages()
    )
    roles = {m.role for m in messages}
    if "user" not in roles or "assistant" not in roles:
        issues.append(
            _issue(
                line_number,
                "training dialogue must include at least one user and one assistant message",
                snippet,
            )
        )

    return issues


def audit_jsonl_file_for_training(path: str | Path) -> CorpusGovernanceReport:
    """Audit a JSONL file for Phase 11 training readiness."""
    path = Path(path)
    report = CorpusGovernanceReport(path=path)
    if not path.exists():
        report.issues.append(
            SampleIssue(
                line_number=None,
                kind="encoding",
                message=f"file not found: {path}",
            )
        )
        return report

    with path.open("r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            report.total_records += 1
            snippet = line.strip()[:80]
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

            issues = audit_record_for_training(raw, line_number=idx)
            if issues:
                report.issues.extend(issues)
                continue

            sample = parse_record(raw)
            provenance = sample.provenance
            assert provenance is not None
            report.training_ready += 1
            report.dialect_counts[provenance.dialect or "unknown"] = (
                report.dialect_counts.get(provenance.dialect or "unknown", 0) + 1
            )
            report.quality_counts[provenance.quality or "unknown"] = (
                report.quality_counts.get(provenance.quality or "unknown", 0) + 1
            )
            report.source_counts[provenance.source or "unknown"] = (
                report.source_counts.get(provenance.source or "unknown", 0) + 1
            )

    return report


def audit_jsonl_directory_for_training(
    path: str | Path,
    *,
    pattern: str = "*.jsonl",
) -> CorpusGovernanceReport:
    """Audit all JSONL files in a directory for Phase 12 readiness.

    The aggregate report intentionally treats "no JSONL files" as a governance
    issue, because Phase 12 must not start tokenizer training on an empty corpus.
    """
    path = Path(path)
    report = CorpusGovernanceReport(path=path)

    if not path.exists():
        report.issues.append(
            SampleIssue(
                line_number=None,
                kind="encoding",
                message=f"directory not found: {path}",
            )
        )
        return report

    files = sorted(p for p in path.glob(pattern) if p.is_file())
    if not files:
        report.issues.append(
            SampleIssue(
                line_number=None,
                kind="empty",
                message=f"no JSONL files found in: {path}",
            )
        )
        return report

    for file_path in files:
        file_report = audit_jsonl_file_for_training(file_path)
        report.total_records += file_report.total_records
        report.training_ready += file_report.training_ready

        for dialect, count in file_report.dialect_counts.items():
            report.dialect_counts[dialect] = report.dialect_counts.get(dialect, 0) + count
        for quality, count in file_report.quality_counts.items():
            report.quality_counts[quality] = report.quality_counts.get(quality, 0) + count
        for source, count in file_report.source_counts.items():
            report.source_counts[source] = report.source_counts.get(source, 0) + count

        for issue in file_report.issues:
            report.issues.append(
                SampleIssue(
                    line_number=issue.line_number,
                    kind=issue.kind,
                    message=f"{file_path.name}: {issue.message}",
                    snippet=issue.snippet,
                )
            )

    return report
