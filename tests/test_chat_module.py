"""Phase 4 — ChatModule end-to-end (without the Orchestrator)."""

from __future__ import annotations

from sf_ai.core.nlp import get_default_pipeline
from sf_ai.modules.chat import ChatModule


def _module() -> ChatModule:
    return ChatModule()  # fresh store


def test_greeting_response_is_arabic_and_mentions_sfai() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("مرحبا")
    out = mod.handle(analysis, intent="chat.greeting", session_id="t1")
    assert "SF.AI" in out.text
    assert out.intent_used == "chat.greeting"
    assert out.template_index == 0
    assert out.turn_count == 2  # user + assistant
    assert out.session_id == "t1"


def test_repeated_greeting_uses_second_template() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("مرحبا")
    first = mod.handle(analysis, intent="chat.greeting", session_id="t1")
    second = mod.handle(analysis, intent="chat.greeting", session_id="t1")
    assert first.template_index == 0
    assert second.template_index == 1


def test_identity_response_describes_sovereignty() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("من انت")
    out = mod.handle(analysis, intent="chat.identity", session_id="t1")
    assert "SF.AI" in out.text
    assert "سيادة" in out.text or "خارجي" in out.text


def test_capability_response_is_honest_about_phase() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("وش تقدر تسوي")
    out = mod.handle(analysis, intent="chat.capability", session_id="t1")
    assert "حاليًا" in out.text
    assert "السعودية" in out.text
    assert "توليد حر" in out.text


def test_language_preference_focuses_on_saudi_and_msa() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("سعودي")
    out = mod.handle(analysis, intent="chat.language_preference", session_id="t1")
    assert "الفصحى" in out.text
    assert "السعود" in out.text


def test_short_clarification_followup_after_smalltalk_explains_prompt() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    smalltalk = pipe.analyze_user_text("وشلونك")
    mod.handle(smalltalk, intent="chat.smalltalk", session_id="t1")
    analysis = pipe.analyze_user_text("عندي؟")
    out = mod.handle(analysis, intent="chat.clarification", session_id="t1")
    assert "قصدي" in out.text or "أقصد" in out.text


def test_open_question_clarification_invites_question() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("عندي سؤال")
    out = mod.handle(analysis, intent="chat.clarification", session_id="t1")
    assert "وش سؤالك" in out.text


def test_farewell_arabic() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("وداعا")
    out = mod.handle(analysis, intent="chat.farewell", session_id="t1")
    assert out.intent_used == "chat.farewell"
    assert out.text


def test_unknown_intent_falls_back_to_general() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("اي شيء عشوائي")
    out = mod.handle(analysis, intent="chat.unknown_intent", session_id="t1")
    assert out.intent_used == "chat.general"


def test_session_isolation() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("مرحبا")
    a = mod.handle(analysis, intent="chat.greeting", session_id="alice")
    b = mod.handle(analysis, intent="chat.greeting", session_id="bob")
    # Both are the first greeting from their own session.
    assert a.template_index == 0
    assert b.template_index == 0


def test_dialect_note_added_for_gulf() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("شلونك")
    # Even when the routed intent is smalltalk, the gulf detection should
    # surface as a note for the dev panel.
    out = mod.handle(analysis, intent="chat.smalltalk", session_id="t1")
    assert any(note.startswith("dialect:") for note in out.notes)


def test_repeated_intent_adds_hint_after_threshold() -> None:
    pipe = get_default_pipeline()
    mod = _module()
    analysis = pipe.analyze_user_text("اي شيء")
    # 4 occurrences of chat.general — threshold is 3, so the 4th should
    # have the soft hint appended.
    out_a = mod.handle(analysis, intent="chat.general", session_id="t1")
    out_b = mod.handle(analysis, intent="chat.general", session_id="t1")
    out_c = mod.handle(analysis, intent="chat.general", session_id="t1")
    out_d = mod.handle(analysis, intent="chat.general", session_id="t1")
    assert "repeat_hint" not in out_a.notes
    # By the 4th turn (prior_count >= 3), hint appears.
    assert "repeat_hint" in out_d.notes
