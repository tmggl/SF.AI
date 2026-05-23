"""Phase 27.20 — protected-phrase tokenizer strategy."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_20_tokenizer_strategy import build_report
from sf_ai.models.tokenizer.policy_audit import load_plain_terms


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_20_protected_phrase_file_matches_hygiene_blockers() -> None:
    phrases = load_plain_terms(
        ROOT / "resources/tokenization/protected_phrases_phase27_20.txt"
    )
    assert phrases == [
        "وعليكم السلام",
        "نفسًا هادئًا",
        "نشتغل سوا",
        "القراءة تفيد",
        "تقدّر الناس",
    ]


def test_phase27_20_report_blocks_runtime_and_sf50m() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_20_tokenizer_strategy_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.20"
    assert report["status"] == (
        "COMPLETED_PROTECTED_PHRASE_STRATEGY_READY_FOR_TOKENIZER_V3"
    )
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert report["protected_phrases_total"] == 5
    assert report["missing_from_policy"] == []
    assert report["unexpected_policy_terms"] == []
    assert report["current_v2_behavior"]["max_pieces"] > 1
    assert report["protected_phrase_strategy_behavior"]["all_single_piece"] is True
    assert report["protected_phrase_strategy_behavior"]["all_roundtrip_ok"] is True


def test_phase27_20_build_report_is_deterministic() -> None:
    report = build_report()
    assert report["protected_phrases"] == report["hygiene_focus_terms"]
    assert report["protected_phrase_strategy_behavior"]["max_pieces"] == 1
    assert report["runtime_allowed"] is False
