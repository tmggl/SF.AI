"""Phase 27.16 — sample-isolated objective repair report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_16_report_blocks_runtime_and_scaling() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.16"
    assert report["status"] == "COMPLETED_OBJECTIVE_REPAIR_RUNTIME_BLOCKED"
    assert report["training"]["packing_mode"] == "sample_isolated"
    assert report["decision"]["runtime"] == "blocked"
    assert report["decision"]["sf50m"] == "blocked"
    assert report["generation_quality"]["step2000"]["runtime_allowed"] is False
    assert report["generation_quality"]["step6000"]["runtime_allowed"] is False


def test_phase27_16_documents_v0_11_worse_than_v0_10_eval() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json")
        .read_text(encoding="utf-8")
    )
    current = report["eval"]["checkpoints"][-1]
    previous = report["eval"]["comparison"]

    assert current["checkpoint"] == "sf-10m-step6000"
    assert current["loss"] > previous["previous_loss"]
    assert current["perplexity"] > previous["previous_perplexity"]
