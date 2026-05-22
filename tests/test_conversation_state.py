"""Phase 4 — ConversationState + ConversationStore."""

from __future__ import annotations

from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore


def test_state_starts_empty() -> None:
    s = ConversationState("s1", max_turns=4)
    assert s.is_empty()
    assert s.turns == ()


def test_state_records_turns() -> None:
    s = ConversationState("s1", max_turns=4)
    s.add_user("مرحبا", intent="chat.greeting")
    s.add_assistant("أهلًا", intent="chat.greeting")
    assert len(s.turns) == 2
    assert s.turns[0].role == "user"
    assert s.turns[1].role == "assistant"


def test_state_bounded_by_max_turns() -> None:
    s = ConversationState("s1", max_turns=3)
    for i in range(10):
        s.add_user(f"msg {i}", intent="chat.general")
    assert len(s.turns) == 3
    # Oldest dropped — last three are msg 7,8,9.
    assert s.turns[0].text == "msg 7"
    assert s.turns[-1].text == "msg 9"


def test_state_counts_intent() -> None:
    s = ConversationState("s1")
    s.add_user("مرحبا", intent="chat.greeting")
    s.add_user("هلا", intent="chat.greeting")
    s.add_user("من انت", intent="chat.identity")
    assert s.count_intent("chat.greeting") == 2
    assert s.count_intent("chat.identity") == 1
    assert s.count_intent("chat.unknown") == 0


def test_state_recent() -> None:
    s = ConversationState("s1")
    s.add_user("a")
    s.add_user("b")
    s.add_user("c")
    assert [t.text for t in s.recent(2)] == ["b", "c"]
    assert s.recent(0) == ()


def test_store_creates_and_reuses_sessions() -> None:
    store = ConversationStore(max_turns=5)
    a1 = store.get("user-123")
    a2 = store.get("user-123")
    assert a1 is a2
    b = store.get("user-456")
    assert b is not a1
    assert len(store) == 2


def test_store_anonymous_session() -> None:
    store = ConversationStore()
    a = store.get(None)
    b = store.get("")
    assert a is b  # both map to anonymous bucket


def test_store_reset() -> None:
    store = ConversationStore()
    store.get("x").add_user("hi")
    store.reset("x")
    fresh = store.get("x")
    assert fresh.is_empty()
