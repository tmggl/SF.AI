"""Phase 12 preflight report must gate training permission."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_phase12_preflight_report_exists_and_blocks_training() -> None:
    report = ROOT / "docs/PHASE12_PREFLIGHT_REPORT.md"
    text = report.read_text(encoding="utf-8")
    assert "Phase 12 corpus/tokenization preflight: PASS" in text
    assert "Phase 12 language-balance gate: MISSING msa" in text
    assert "Training permission: GRANTED" in text
    assert "Action now: Phase 12 tokenizer v1 completed with limits" in text
    assert "make train-bpe" in text
    assert "لا تنفذ إلا بعد إذن صريح" in text
