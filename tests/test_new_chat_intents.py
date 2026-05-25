"""Phase 9 polish — coverage for the new chat intents added during the
"comfortable chat + accurate routing" pass.

Each test goes through the full Orchestrator pipeline (NLP → Router →
Module) so we exercise the same path the chat UI hits.
"""

from __future__ import annotations

import pytest

from sf_ai.core.index import load_default_registry
from sf_ai.core.orchestrator import Orchestrator, UserMessage


@pytest.fixture()
def orch() -> Orchestrator:
    # Fresh registry + modules per test → no session bleed between cases.
    return Orchestrator(registry=load_default_registry())


@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("شكرا",        "chat.thanks"),
        ("شكراً لك",   "chat.thanks"),
        ("تسلم",        "chat.thanks"),
        ("تمام",        "chat.affirmation"),
        ("الحمدلله",    "chat.affirmation"),
        ("أنا بخير",    "chat.affirmation"),
        ("أيوه",        "chat.affirmation"),
        ("اوكي",        "chat.affirmation"),
        ("لا",          "chat.negation"),
        ("مش هذا",     "chat.negation"),
        ("ساعدني",    "chat.help"),
        ("محتاج مساعدة", "chat.help"),
        ("مش فاهم",   "chat.confused"),
        ("ما فهمت",   "chat.confused"),
        ("وشلونك",    "chat.smalltalk"),
        ("كيفك",      "chat.smalltalk"),
        ("وين كنت",   "chat.presence"),
        ("هل تفهم",   "chat.understanding"),
        ("سعودي",     "chat.language_preference"),
        ("فصحى",      "chat.language_preference"),
        ("عندي؟",     "chat.clarification"),
        ("عندي سؤال", "chat.clarification"),
        ("وش تقصد",   "chat.clarification"),
        ("أريد أن أختبر الحوار العربي الفصيح.", "chat.dialogue_test"),
        ("اشرح لي خطوتنا التالية باختصار.", "chat.next_step"),
        ("ما الفرق بين تدريب النموذج وتفعيل النموذج؟", "chat.training_activation_difference"),
        ("من صنعك",   "chat.who_made_you"),
        ("من بناك",   "chat.who_made_you"),
        ("وداعا",       "chat.farewell"),
        ("في امان الله", "chat.farewell"),
    ],
)
def test_new_intent_routes_correctly(
    orch: Orchestrator, message: str, expected_intent: str
) -> None:
    result = orch.process(UserMessage(text=message, session_id=f"new-{message}"))
    assert result.domain == "chat", (
        f"{message!r} expected chat domain, got {result.domain}/{result.intent}"
    )
    assert result.intent == expected_intent, (
        f"{message!r} expected {expected_intent}, got {result.intent}"
    )
    # Whether the domain-router went via fallback or not is OK — what
    # matters is that the intent itself was identified correctly.
    assert result.debug.get("dispatch") == "module:chat"
    assert result.response, f"{message!r} produced empty response"


def test_thanks_response_is_warm() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="شكرا", session_id="th-1"))
    assert r.intent == "chat.thanks"
    # Reply uses warm wording; we just assert it's non-empty Arabic.
    assert any(ar in r.response for ar in ("العفو", "تكرم", "شكرًا", "شكرا"))


def test_who_made_you_mentions_sami() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="من صنعك", session_id="who-1"))
    assert r.intent == "chat.who_made_you"
    assert "سامي" in r.response or "SF.AI" in r.response


def test_help_response_lists_examples() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="ساعدني", session_id="help-1"))
    assert r.intent == "chat.help"
    # The help template ships example prompts; check at least one of them.
    assert "وش تقدر تسوي" in r.response or "من أنت" in r.response


def test_confused_invites_rephrase() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="مش فاهم", session_id="conf-1"))
    assert r.intent == "chat.confused"
    assert "صياغة" in r.response or "اعد" in r.response or "إعادة" in r.response or "أفهمها" in r.response


def test_negation_does_not_route_to_other_domains() -> None:
    # A bare "لا" must not accidentally route to web/medical/etc.
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="لا", session_id="neg-1"))
    assert r.domain == "chat"
    assert r.intent == "chat.negation"
    assert r.requires_safety is False


def test_wshlonk_routes_without_domain_fallback() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="وشلونك", session_id="smalltalk-wsh"))
    assert r.domain == "chat"
    assert r.intent == "chat.smalltalk"
    assert r.fallback_used is False


def test_social_templates_are_good_enough_for_direct_ui_prompts() -> None:
    orch = Orchestrator(registry=load_default_registry())

    r1 = orch.process(UserMessage(text="كيفك", session_id="social-ui"))
    r2 = orch.process(UserMessage(text="اهلا", session_id="social-ui"))
    r3 = orch.process(UserMessage(text="وين كنت", session_id="social-ui"))
    r4 = orch.process(UserMessage(text="هل تفهم", session_id="social-ui"))

    assert r1.intent == "chat.smalltalk"
    assert "كيف حالك" in r1.response or "وش ودك" in r1.response
    assert r2.intent == "chat.greeting"
    assert "أهلًا" in r2.response
    assert r3.intent == "chat.presence"
    assert "هنا" in r3.response
    assert r4.intent == "chat.understanding"
    assert "أفهم" in r4.response


def test_open_question_gets_invitation_not_previous_prompt_explanation() -> None:
    orch = Orchestrator(registry=load_default_registry())
    r = orch.process(UserMessage(text="عندي سؤال", session_id="question-open"))
    assert r.domain == "chat"
    assert r.intent == "chat.clarification"
    assert "وش سؤالك" in r.response


def test_open_question_stays_open_after_smalltalk_followup() -> None:
    orch = Orchestrator(registry=load_default_registry())
    sid = "question-after-smalltalk"
    orch.process(UserMessage(text="وشلونك", session_id=sid))
    orch.process(UserMessage(text="عندي؟", session_id=sid))
    r = orch.process(UserMessage(text="عندي سؤال", session_id=sid))
    assert r.domain == "chat"
    assert r.intent == "chat.clarification"
    assert "وش سؤالك" in r.response


def test_phase_guidance_prompts_are_current_generator_lab_guidance() -> None:
    orch = Orchestrator(registry=load_default_registry())
    dialogue = orch.process(UserMessage(text="أريد أن أختبر الحوار العربي الفصيح.", session_id="p22-dialogue"))
    next_step = orch.process(UserMessage(text="اشرح لي خطوتنا التالية باختصار.", session_id="p22-next"))
    diff = orch.process(UserMessage(text="ما الفرق بين تدريب النموذج وتفعيل النموذج؟", session_id="p22-diff"))

    assert dialogue.intent == "chat.dialogue_test"
    assert "sf_10m_phase27_81" in dialogue.response
    assert "قوالب" in dialogue.response
    assert "بصراحة" in dialogue.response
    assert next_step.intent == "chat.next_step"
    assert "Phase 27.117" in next_step.response
    assert "SinaLab Synonyms" in next_step.response
    assert "Phase 27.118" in next_step.response
    assert diff.intent == "chat.training_activation_difference"
    assert "التدريب" in diff.response
    assert "التفعيل" in diff.response
