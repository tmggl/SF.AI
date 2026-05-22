"""Phase 3 — IntentDetector."""

from __future__ import annotations

from sf_ai.core.nlp import IntentDetector


def test_detects_greeting_hint() -> None:
    det = IntentDetector()
    hints = det.detect("مرحبا")
    assert any(h.intent == "chat.greeting" for h in hints)


def test_detects_capability_question() -> None:
    det = IntentDetector()
    hints = det.detect("وش تقدر تسوي")
    assert any(h.intent == "chat.capability" for h in hints)


def test_detects_who_made_you_separately_from_identity() -> None:
    det = IntentDetector()
    hints = det.detect("من صنعك")
    assert hints
    assert hints[0].intent == "chat.who_made_you"


def test_detects_help_and_confused_hints() -> None:
    det = IntentDetector()
    help_hints = det.detect("ساعدني")
    confused_hints = det.detect("مش فاهم")
    assert any(h.intent == "chat.help" for h in help_hints)
    assert any(h.intent == "chat.confused" for h in confused_hints)


def test_detects_web_search() -> None:
    det = IntentDetector()
    hints = det.detect("ابحث لي في الانترنت عن موضوع")
    assert any(h.domain_hint == "web" for h in hints)


def test_unknown_input_returns_empty() -> None:
    det = IntentDetector()
    hints = det.detect("zzz qqq")
    assert hints == ()


def test_returns_at_most_three_hints() -> None:
    det = IntentDetector()
    hints = det.detect("ابي اتعلم وابي اكتب كود وابي ابحث")
    assert len(hints) <= 3
