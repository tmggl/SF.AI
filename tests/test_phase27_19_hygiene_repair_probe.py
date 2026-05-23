"""Phase 27.19 — hygiene repair probe report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_19_repair_probe_blocks_runtime_without_regression_claim() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_19_hygiene_repair_probe_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.19"
    assert report["status"] == "FAILED_HYGIENE_REPAIR_PROBE_BLOCK_RUNTIME"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["train_records"] == 52
    assert report["repair_records"] == 20
    assert report["eval_records"] == 32
    assert report["passed"] == 27
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False


def test_phase27_19_repair_focus_terms_match_hygiene_audit() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_19_hygiene_repair_probe_report.json")
        .read_text(encoding="utf-8")
    )
    assert report["repair_focus_terms"] == [
        "وعليكم السلام",
        "نفسًا هادئًا",
        "نشتغل سوا",
        "القراءة تفيد",
        "تقدّر الناس",
    ]
    reasons = report["reason_counts"]
    assert reasons["passed"] == 27
    assert "guard:malformed_token" in reasons
    assert "missing_semantic_terms" in reasons
