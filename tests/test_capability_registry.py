"""Phase 2 — Capability Registry loading and integrity tests."""

from __future__ import annotations

from sf_ai.core.index import load_default_registry


def test_registry_loads() -> None:
    reg = load_default_registry()
    assert reg.meta.version
    assert reg.meta.fallback.domain == "chat"
    assert reg.meta.fallback.intent == "chat.general"


def test_registry_has_twenty_domains() -> None:
    reg = load_default_registry()
    names = set(reg.domain_names())
    expected = {
        "chat", "coding", "data", "files", "web", "research",
        "legal", "medical", "finance", "education", "religion",
        "social", "productivity", "writing", "translation",
        "image", "audio", "security", "business", "ecommerce",
    }
    assert expected <= names, f"missing domains: {expected - names}"


def test_chat_is_active_and_others_skeleton() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    assert chat.status == "active"
    assert chat.requires_safety is False
    # Every active domain right now must be chat (and only chat).
    actives = [d.name for d in reg.active_domains()]
    assert actives == ["chat"]


def test_sensitive_domains_marked_safety() -> None:
    reg = load_default_registry()
    for name in ("legal", "medical", "finance", "security", "religion"):
        d = reg.get_domain(name)
        assert d is not None, f"missing domain {name}"
        assert d.requires_safety is True, f"{name} should require safety"
        assert d.status == "skeleton_only", f"{name} should be skeleton_only"


def test_chat_has_required_intents() -> None:
    reg = load_default_registry()
    chat = reg.get_domain("chat")
    assert chat is not None
    intent_names = {i.name for i in chat.intents}
    for required in (
        "chat.greeting",
        "chat.smalltalk",
        "chat.identity",
        "chat.capability",
        "chat.general",
    ):
        assert required in intent_names, f"chat missing intent: {required}"

    fb = chat.fallback_intent
    assert fb is not None and fb.name == "chat.general"
