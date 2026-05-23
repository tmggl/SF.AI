"""Phase 27.14 — sovereign quality tooling adoption."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_14_quality_tooling import build_report
from sf_ai.training.experiment_tracker import LocalExperimentTracker


def test_phase27_14_quality_tooling_report_and_registry(tmp_path: Path) -> None:
    registry = tmp_path / "experiment_registry.jsonl"
    report = build_report(registry_path=registry)

    assert report["phase"] == "Phase 27.14"
    assert report["status"] == "completed_tooling_adoption_decision_no_training"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["training_started"] is False
    assert report["runtime_generator_enabled"] is False
    assert report["uses_external_ai"] is False
    assert len(report["tools"]) == 10

    by_tool = {item["tool"]: item for item in report["tools"]}
    assert by_tool["assistant_eos_stop_boundary"]["status"] == "implemented_phase27_12"
    assert by_tool["local_experiment_tracker"]["status"] == "implemented_phase27_14"
    assert by_tool["curriculum_sampler"]["status"] == "planned_phase27_15"
    assert report["blocking_policy"]["start_sf50m"].startswith("blocked")

    records = LocalExperimentTracker(registry).read_all()
    assert [r.phase for r in records] == [
        "Phase 27.12 — Assistant Boundary/EOS Repair",
        "Phase 27.13",
    ]
    assert records[1].metrics["generation_passed"] == 3
    assert records[1].gates["runtime_allowed"] is False


def test_phase27_14_committed_report_shape_if_present() -> None:
    path = Path("artifacts/reports/phase27_14_quality_tooling_decision_report.json")
    if not path.exists():
        return
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["phase"] == "Phase 27.14"
    assert report["blocking_policy"]["activate_runtime_generator"].startswith("blocked")
