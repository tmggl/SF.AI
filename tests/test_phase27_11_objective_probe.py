"""Phase 27.11 — objective/decoding probe tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_11_objective_probe import _exact_or_clean_stop


ROOT = Path(__file__).resolve().parents[1]


def test_exact_or_clean_stop_requires_reply_boundary() -> None:
    assert _exact_or_clean_stop("وعليكم السلام، أهلًا بك.", "وعليكم السلام، أهلًا بك.")
    assert _exact_or_clean_stop("وعليكم السلام، أهلًا بك. حسنًا", "وعليكم السلام، أهلًا بك.")
    assert not _exact_or_clean_stop(
        "وعليكم السلام، أهلًا بك. باختصار. باختصار. باختصار.",
        "وعليكم السلام، أهلًا بك.",
    )
    assert not _exact_or_clean_stop("مرحبًا بك، تف", "مرحبًا بك، تفضل.")


def test_phase27_11_report_blocks_scaling_until_clean_stop() -> None:
    report_path = ROOT / "artifacts/reports/phase27_11_objective_probe_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["phase"].startswith("Phase 27.11")
    assert report["status"] == "FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["records"] == 16
    assert report["passed"] == 0
    assert report["pass_rate"] == 0.0
    assert report["reason_counts"]["overgenerates_after_expected"] >= 1
    assert "boundary/EOS" in report["decision"]
