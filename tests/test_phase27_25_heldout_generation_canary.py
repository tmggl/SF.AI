"""Phase 27.25 — held-out generation canary report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_25_heldout_canary_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_25_heldout_generation_canary_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.25"
    assert report["status"] == "FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME"
    assert report["previous_phase27_24"]["passed"] == 32
    assert report["current"]["passed"] == 8
    assert report["current"]["eval_records"] == 16
    assert report["current"]["semantic_match"] == 8
    assert report["current"]["guard_passed"] == 15
    assert report["runtime_allowed"] is False
    assert report["limited_runtime_trial_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert "Phase 27.26" in report["next_phase"]


def test_phase27_25_failures_identify_generalization_gap() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_25_heldout_generation_canary_report.json")
        .read_text(encoding="utf-8")
    )
    failures = report["failures"]
    prompts = {row["prompt"] for row in failures}

    assert len(failures) == 8
    assert "أحتاج نصيحة بسيطة" in prompts
    assert "كيف أرتب يومي" in prompts
    assert "متوتر شوي" in prompts
    assert report["current"]["category_breakdown"]["definition"] == {
        "passed": 6,
        "total": 6,
    }
