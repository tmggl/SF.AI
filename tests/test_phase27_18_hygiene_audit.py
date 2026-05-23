"""Phase 27.18 — tokenization/decoding hygiene audit."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.phase27_18_hygiene_audit import build_report
from sf_ai.modules.chat.generation_guard import GenerationGuard


ROOT = Path(__file__).resolve().parents[1]


def test_phase27_18_report_blocks_runtime_with_hygiene_findings() -> None:
    report = json.loads(
        (ROOT / "artifacts/reports/phase27_18_tokenization_hygiene_report.json")
        .read_text(encoding="utf-8")
    )

    assert report["phase"] == "Phase 27.18"
    assert report["status"] == "COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS"
    assert report["language_track"] == ["msa", "saudi"]
    assert report["lexicon_track"] == "Saudi Seed v1"
    assert report["terms_total"] == 26
    assert report["roundtrip_failures"] == []
    assert report["uncovered_bad_fragments"] == []
    assert report["runtime_allowed"] is False
    assert report["sf50m_allowed"] is False
    assert "وعليكم السلام" in report["aggressive_split_terms"]


def test_phase27_18_guard_blocks_observed_bad_fragments() -> None:
    guard = GenerationGuard(min_chars=4)
    for fragment in (
        "وعليكأهلًا السم، أهلًا بك.",
        "التعاعاون يعني أن ننجز معًا بدل الانفراد.",
        "القراد. ءة توسع الفهم وتزيد المفردات.",
        "هوش تحتاجججبعيادة.",
    ):
        verdict = guard.inspect(fragment)
        assert verdict.allowed is False
        assert verdict.reason in {"model_artifact_fragment", "malformed_token"}


def test_phase27_18_build_report_is_deterministic() -> None:
    report = build_report()
    assert report["terms_total"] == 26
    assert report["aggressive_split_terms"] == [
        "وعليكم السلام",
        "نفسًا هادئًا",
        "نشتغل سوا",
        "القراءة تفيد",
        "تقدّر الناس",
    ]
