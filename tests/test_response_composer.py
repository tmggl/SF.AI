"""Phase 2 — ResponseComposer."""

from __future__ import annotations

from sf_ai.core.composer import ResponseComposer, ResponseStyle
from sf_ai.core.index import load_default_registry


def _chat_domain():
    return load_default_registry().get_domain("chat")


def test_compose_greeting_is_arabic() -> None:
    composer = ResponseComposer()
    chat = _chat_domain()
    assert chat is not None
    reply = composer.compose(chat, "chat.greeting", intent_fallback=False, domain_fallback=False)
    assert "SF.AI" in reply.text
    assert reply.style == ResponseStyle.ARABIC_FORMAL
    assert reply.safety_flag is False


def test_compose_identity_mentions_sovereign_phase() -> None:
    composer = ResponseComposer()
    chat = _chat_domain()
    assert chat is not None
    reply = composer.compose(chat, "chat.identity", intent_fallback=False, domain_fallback=False)
    assert "SF.AI" in reply.text


def test_compose_capability_describes_current_capabilities() -> None:
    composer = ResponseComposer()
    chat = _chat_domain()
    assert chat is not None
    reply = composer.compose(chat, "chat.capability", intent_fallback=False, domain_fallback=False)
    assert "Phase" in reply.text or "حاليًا" in reply.text


def test_compose_skeleton_domain_explains_status() -> None:
    reg = load_default_registry()
    web = reg.get_domain("web")
    assert web is not None
    composer = ResponseComposer()
    reply = composer.compose(web, "web.search", intent_fallback=True, domain_fallback=False)
    # Friendly per-domain text now ships instead of a literal "skeleton_only"
    # technical phrase. Assert the meaning rather than the exact wording.
    assert "غير مفعَّل" in reply.text or "ليس مفعَّلًا" in reply.text or "بنيويًا" in reply.text
    assert reply.safety_flag is False


def test_compose_safety_domain_raises_flag() -> None:
    reg = load_default_registry()
    medical = reg.get_domain("medical")
    assert medical is not None
    composer = ResponseComposer()
    reply = composer.compose(medical, "medical.general", intent_fallback=True, domain_fallback=False)
    assert reply.safety_flag is True
    assert "حساس" in reply.text or "مختص" in reply.text


def test_compose_unknown_intent_falls_back_to_general() -> None:
    composer = ResponseComposer()
    chat = _chat_domain()
    assert chat is not None
    reply = composer.compose(chat, "chat.unknown_xyz", intent_fallback=True, domain_fallback=False)
    # Should still return a chat-like reply.
    assert reply.text
    assert reply.safety_flag is False
