"""Phase 3 — NLPPipeline end-to-end."""

from __future__ import annotations

from sf_ai.core.nlp import NLPPipeline, get_default_pipeline


def test_pipeline_basic_arabic() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("مرحبا كيف الحال")
    assert a.original_text == "مرحبا كيف الحال"
    assert a.normalized_text == "مرحبا كيف الحال"
    assert a.language == "ar"
    assert a.tokens


def test_pipeline_normalizes_tashkeel() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("مَرْحَبًا")
    assert a.normalized_text == "مرحبا"
    assert "مرحبا" in a.canonical_text


def test_pipeline_handles_arabizi() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("shlon")
    # canonical should contain Arabic form after arabizi + dialect rewrite.
    assert "شلون" in a.canonical_text or "كيف" in a.canonical_text
    assert any(al.dialect == "saudi" for al in a.aliases)


def test_pipeline_dialect_signal() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("شلونك")
    assert any(al.dialect == "saudi" for al in a.aliases)
    assert a.detected_dialect == "saudi"
    assert "كيف حالك" in a.canonical_text


def test_pipeline_typo_correction() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("ابي بايثن")
    assert "بايثون" in a.corrected_text
    assert any(c.corrected == "بايثون" for c in a.corrections)


def test_pipeline_safety_flag_medical() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("عندي الم في الراس")
    assert any(flag.startswith("medical:") for flag in a.safety_flags)


def test_pipeline_intent_hints_emitted() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("مرحبا")
    assert any(h.intent == "chat.greeting" for h in a.intent_hints)


def test_pipeline_protects_code_tokens() -> None:
    p = NLPPipeline()
    a = p.analyze_user_text("ابي docker و python")
    assert "docker" in a.canonical_text
    assert "python" in a.canonical_text


def test_default_pipeline_is_singleton() -> None:
    assert get_default_pipeline() is get_default_pipeline()
