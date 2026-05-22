"""Phase 3 — TypoCorrector."""

from __future__ import annotations

from sf_ai.core.nlp import TypoCorrector


def test_corrects_known_pattern() -> None:
    tc = TypoCorrector()
    out, corrections = tc.correct("ابي اسوي بايثن")
    assert "بايثون" in out
    assert any(c.original == "بايثن" and c.corrected == "بايثون" for c in corrections)


def test_does_not_correct_unknown_tokens() -> None:
    tc = TypoCorrector()
    out, corrections = tc.correct("هذا نص عادي بدون اخطاء")
    assert out == "هذا نص عادي بدون اخطاء"
    assert corrections == ()


def test_soft_hints_are_reported_but_not_applied() -> None:
    tc = TypoCorrector()
    out, corrections = tc.correct("احسن انجاز")
    # 'احسن' is a soft_hint, not an auto-apply.
    assert out == "احسن انجاز"
    assert any(c.original == "احسن" for c in corrections)
    soft = next(c for c in corrections if c.original == "احسن")
    assert soft.confidence < tc.apply_threshold


def test_fuzzy_against_vocab() -> None:
    tc = TypoCorrector()
    vocab = ["python", "docker", "django"]
    corr = tc.fuzzy_against("docke", vocab)
    assert corr is not None
    assert corr.corrected == "docker"
    assert corr.confidence >= tc.fuzzy_threshold


def test_fuzzy_returns_none_when_too_distant() -> None:
    tc = TypoCorrector()
    assert tc.fuzzy_against("xyz", ["python", "docker"]) is None
