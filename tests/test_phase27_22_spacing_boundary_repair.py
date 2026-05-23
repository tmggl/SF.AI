"""Phase 27.22 — spacing/boundary repair report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_22_report_shows_spacing_improvement_but_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_22_spacing_boundary_repair_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.22"
    assert report["status"] == "PARTIAL_SPACING_BOUNDARY_REPAIR_BLOCK_RUNTIME"
    assert report["previous_phase27_21"]["passed"] == 25
    assert report["current"]["passed"] == 29
    assert report["current"]["exact_clean"] == 29
    assert report["current"]["semantic_match"] == 30
    assert report["current"]["guard_passed"] == 32
    assert report["delta"]["passed"] == 4
    assert report["glued_spacing_markers_remaining"] == []
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False


def test_phase27_22_remaining_failures_are_semantic_or_lexical() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_22_spacing_boundary_repair_report.json")
        .read_text(encoding="utf-8")
    )
    failed = [row for row in report["results"] if not row["passed"]]

    assert len(failed) == 3
    reasons = {row["reason"] for row in failed}
    assert reasons == {"missing_semantic_terms", "not_exact_clean"}
    generated = "\n".join(row["generated"] for row in failed)
    assert "سواونخفف" not in generated
    assert "تفيدوتوسع" not in generated
    assert "هادئًاوابدأ" not in generated
    assert "الاحتردم" in generated
