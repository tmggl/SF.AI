"""Phase 2 — DomainRouter & IntentRouter."""

from __future__ import annotations

from sf_ai.core.index import load_default_registry
from sf_ai.core.router import DomainRouter, IntentRouter


def test_domain_router_greeting() -> None:
    reg = load_default_registry()
    router = DomainRouter(reg)
    res = router.route("مرحبا")
    assert res.domain == "chat"
    assert res.fallback_used is False
    assert res.score > 0.0
    assert res.confidence > 0.0
    assert any(s.kind.value == "keyword" for s in res.matched_signals)


def test_domain_router_identity_phrase() -> None:
    reg = load_default_registry()
    router = DomainRouter(reg)
    res = router.route("من انت")
    assert res.domain == "chat"
    # "من انت" is a phrase for chat → expect phrase signal with +5.
    assert any(s.kind.value == "phrase" for s in res.matched_signals)
    assert res.score >= 5.0


def test_domain_router_unknown_fallbacks_to_chat() -> None:
    reg = load_default_registry()
    router = DomainRouter(reg)
    res = router.route("xyz123 qqq")
    assert res.domain == "chat"
    assert res.fallback_used is True
    assert res.score == 0.0
    assert res.confidence == 0.0


def test_domain_router_empty_input_fallback() -> None:
    reg = load_default_registry()
    router = DomainRouter(reg)
    res = router.route("")
    assert res.domain == "chat"
    assert res.fallback_used is True


def test_intent_router_picks_greeting() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    iresult = IntentRouter().route(chat, "مرحبا")
    assert iresult.intent == "chat.greeting"
    assert iresult.score > 0.0


def test_intent_router_picks_identity() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    iresult = IntentRouter().route(chat, "من انت")
    assert iresult.intent == "chat.identity"


def test_intent_router_picks_capability() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    iresult = IntentRouter().route(chat, "وش تقدر تسوي")
    assert iresult.intent == "chat.capability"


def test_intent_router_falls_back_to_general() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    iresult = IntentRouter().route(chat, "xyz nothing relevant")
    assert iresult.intent == "chat.general"
    assert iresult.fallback_used is True
