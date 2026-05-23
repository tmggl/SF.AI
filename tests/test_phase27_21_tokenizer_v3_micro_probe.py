"""Phase 27.21 — tokenizer v3 protected-phrase micro-probe."""

from __future__ import annotations

import json
from pathlib import Path

from sf_ai.models.tokenizer import BPETokenizer


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_21_tokenizer_v3_protects_phrases() -> None:
    tokenizer = BPETokenizer.load(ROOT / "artifacts/tokenizers/sf_bpe/v3")
    phrases = [
        "وعليكم السلام",
        "نفسًا هادئًا",
        "نشتغل سوا",
        "القراءة تفيد",
        "تقدّر الناس",
    ]

    for phrase in phrases:
        ids = tokenizer.encode(phrase)
        assert len(ids) == 1, phrase
        assert tokenizer.decode(ids) == phrase


def test_phase27_21_report_blocks_runtime() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.21"
    assert report["status"] == "FAILED_TOKENIZER_V3_MICRO_PROBE_BLOCK_RUNTIME"
    assert report["tokenizer"]["path"] == "artifacts/tokenizers/sf_bpe/v3"
    assert report["tokenizer"]["sf_origin"] is True
    assert report["tokenizer"]["vocab_size"] == 4706
    assert report["protected_phrase_behavior"]["all_single_piece"] is True
    assert report["protected_phrase_behavior"]["all_roundtrip_ok"] is True
    assert report["protected_phrase_behavior"]["max_pieces"] == 1
    assert report["passed"] == 25
    assert report["eval_records"] == 32
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False


def test_phase27_21_failures_identify_spacing_boundary_issue() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json")
        .read_text(encoding="utf-8")
    )
    failed = [row for row in report["results"] if not row["passed"]]
    generated = "\n".join(row["generated"] for row in failed)

    assert "سواونخفف" in generated
    assert "تفيدوتوسع" in generated or "هادئًاوابدأ" in generated
    assert report["reason_counts"]["not_exact_clean"] == 4
    assert report["reason_counts"]["missing_semantic_terms"] == 2
