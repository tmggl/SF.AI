"""Phase 2 — Orchestrator end-to-end."""

from __future__ import annotations

from sf_ai.core.orchestrator import Orchestrator, UserMessage, get_default_orchestrator
from sf_ai.core.index import load_default_registry


def test_orchestrator_greeting_routes_to_chat_greeting() -> None:
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="مرحبا", session_id="orch-1"))
    assert result.domain == "chat"
    assert result.intent == "chat.greeting"
    assert result.confidence > 0.0
    assert result.status == "active"
    assert result.requires_safety is False
    assert "SF.AI" in result.response
    assert result.debug.get("dispatch") == "module:chat"


def test_orchestrator_identity() -> None:
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="من انت"))
    assert result.domain == "chat"
    assert result.intent == "chat.identity"


def test_orchestrator_capability() -> None:
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="وش تقدر تسوي"))
    assert result.domain == "chat"
    assert result.intent == "chat.capability"


def test_orchestrator_unknown_falls_back_to_chat_general() -> None:
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="zzz qqq xyz"))
    assert result.domain == "chat"
    assert result.intent == "chat.general"
    assert result.fallback_used is True
    assert result.confidence == 0.0


def test_orchestrator_medical_keyword_triggers_safety() -> None:
    # "ألم" is a medical keyword. Even though medical is skeleton_only, the
    # router still scores it — the orchestrator must surface requires_safety.
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="عندي الم في الراس"))
    assert result.domain == "medical"
    assert result.requires_safety is True
    assert "حساس" in result.response or "مختص" in result.response


def test_orchestrator_skeleton_domain_explains_status() -> None:
    # "ابحث في الويب" is a phrase under the `web` (skeleton_only) domain.
    orch = Orchestrator(registry=load_default_registry())
    result = orch.process(UserMessage(text="ابحث في الويب عن موضوع"))
    assert result.domain == "web"
    assert result.status == "skeleton_only"
    # Friendly per-domain copy ships now instead of the literal
    # "skeleton_only" wording.
    assert "غير مفعَّل" in result.response or "البحث في الويب" in result.response


def test_get_default_orchestrator_is_singleton() -> None:
    a = get_default_orchestrator()
    b = get_default_orchestrator()
    assert a is b
