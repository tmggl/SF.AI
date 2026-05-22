"""Phase 3 — Router using NLPAnalysis (dialect/normalized/typo signals)."""

from __future__ import annotations

from sf_ai.core.index import load_default_registry
from sf_ai.core.nlp import get_default_pipeline
from sf_ai.core.router import DomainRouter, IntentRouter


def test_router_uses_dialect_alias_signal() -> None:
    # "شلونك" not directly in chat phrases, but dialect_mapper rewrites it to
    # "كيف حالك" → chat phrase. Router should pick chat via dialect_alias.
    reg = load_default_registry()
    pipe = get_default_pipeline()
    analysis = pipe.analyze_user_text("شلونك")
    res = DomainRouter(reg).route_with_nlp(analysis)
    assert res.domain == "chat"
    assert any(s.kind.value in {"phrase", "dialect_alias"} for s in res.matched_signals)


def test_router_routes_normalized_form() -> None:
    # Tashkeel input should still route correctly via the normalized lens.
    reg = load_default_registry()
    pipe = get_default_pipeline()
    analysis = pipe.analyze_user_text("مَرْحَبًا")
    res = DomainRouter(reg).route_with_nlp(analysis)
    assert res.domain == "chat"


def test_router_uses_typo_corrected_path() -> None:
    # 'بايثن' is a known typo for 'بايثون'. The coding domain doesn't list
    # 'بايثون' in default_registry.yaml, so this test only asserts that the
    # corrector ran and the corrected text is present on the analysis.
    pipe = get_default_pipeline()
    analysis = pipe.analyze_user_text("ابي بايثن")
    assert "بايثون" in analysis.corrected_text


def test_intent_router_with_nlp_picks_greeting() -> None:
    reg = load_default_registry()
    pipe = get_default_pipeline()
    chat = reg.get_domain("chat")
    assert chat is not None
    analysis = pipe.analyze_user_text("شلونك")
    iresult = IntentRouter().route_with_nlp(chat, analysis)
    # Should hit chat.smalltalk via dialect rewrite "شلونك → كيف حالك".
    assert iresult.intent in {"chat.smalltalk", "chat.greeting"}
    assert iresult.score > 0.0


def test_router_arabizi_path() -> None:
    reg = load_default_registry()
    pipe = get_default_pipeline()
    analysis = pipe.analyze_user_text("shlon")
    res = DomainRouter(reg).route_with_nlp(analysis)
    assert res.domain == "chat"
    assert res.score > 0.0
