"""Local experiment tracker for sovereign SF.AI training runs.

This module intentionally writes plain JSONL under ``artifacts/reports``.
It has no network calls, no external service dependency, and no model logic.
Its job is to make training decisions auditable: which corpus/checkpoint was
used, which gates passed, and why runtime/scaling was allowed or blocked.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExperimentRecord:
    phase: str
    name: str
    status: str
    language_track: tuple[str, ...]
    lexicon_track: str
    model: str = ""
    checkpoint: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    gates: dict[str, Any] = field(default_factory=dict)
    decision: str = ""

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["language_track"] = list(self.language_track)
        return data

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> "ExperimentRecord":
        return cls(
            phase=str(raw["phase"]),
            name=str(raw["name"]),
            status=str(raw["status"]),
            language_track=tuple(str(x) for x in raw.get("language_track", ())),
            lexicon_track=str(raw.get("lexicon_track", "")),
            model=str(raw.get("model", "")),
            checkpoint=str(raw.get("checkpoint", "")),
            metrics=dict(raw.get("metrics", {})),
            gates=dict(raw.get("gates", {})),
            decision=str(raw.get("decision", "")),
        )


class LocalExperimentTracker:
    """Append/read JSONL experiment records locally."""

    def __init__(self, path: str | Path = "artifacts/reports/experiment_registry.jsonl") -> None:
        self.path = Path(path)

    def write_all(self, records: list[ExperimentRecord]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        text = "".join(json.dumps(r.to_json(), ensure_ascii=False) + "\n" for r in records)
        self.path.write_text(text, encoding="utf-8")

    def read_all(self) -> list[ExperimentRecord]:
        if not self.path.exists():
            return []
        records: list[ExperimentRecord] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(ExperimentRecord.from_json(json.loads(line)))
        return records


def phase27_12_record(report: dict[str, Any]) -> ExperimentRecord:
    return ExperimentRecord(
        phase=str(report["phase"]),
        name="Assistant Boundary/EOS Repair Probe",
        status=str(report["status"]),
        language_track=tuple(report.get("language_track", ())),
        lexicon_track=str(report.get("lexicon_track", "")),
        model="sf-10m",
        checkpoint=str(report.get("checkpoint_name", "")),
        metrics={
            "records": report.get("records"),
            "passed": report.get("passed"),
            "pass_rate": report.get("pass_rate"),
            "guard_passed": report.get("guard_passed"),
            "guard_pass_rate": report.get("guard_pass_rate"),
        },
        gates={
            "runtime_allowed": False,
            "sf50m_allowed": False,
            "clean_stop_gate_passed": False,
        },
        decision=str(report.get("decision", "")),
    )


def phase27_13_record(report: dict[str, Any]) -> ExperimentRecord:
    training = report.get("training", {})
    eval_report = report.get("eval", {})
    generation = report.get("generation_quality", {})
    best = {}
    for item in eval_report.get("checkpoints", []):
        if item.get("name") == eval_report.get("best_checkpoint"):
            best = item
            break
    return ExperimentRecord(
        phase=str(report["phase"]),
        name=str(report["name"]),
        status=str(report["status"]),
        language_track=tuple(report.get("language_track", ())),
        lexicon_track=str(report.get("lexicon_track", "")),
        model=str(training.get("model", "")),
        checkpoint=str(eval_report.get("best_checkpoint", "")),
        metrics={
            "steps": training.get("steps"),
            "eval_loss": best.get("loss"),
            "perplexity": best.get("perplexity"),
            "generation_passed": generation.get("passed"),
            "generation_total": generation.get("total"),
            "generation_pass_rate": generation.get("pass_rate"),
        },
        gates={
            "runtime_allowed": bool(generation.get("runtime_allowed", False)),
            "sf50m_allowed": bool((report.get("quality_decision", {}) or {}).get("start_sf50m", False)),
            "boundary_eos_target": bool(training.get("boundary_eos_target", False)),
            "dialect_conditioning": bool(training.get("dialect_conditioning", False)),
        },
        decision=str((report.get("quality_decision", {}) or {}).get("reason", "")),
    )
