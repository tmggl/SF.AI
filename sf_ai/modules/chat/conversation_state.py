"""ConversationState — short-term per-session memory.

Phase 4 keeps the last N turns of each session in process memory. Phase 8/9
can swap the store implementation for Redis without changing the interface.
"""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from threading import Lock


@dataclass(frozen=True)
class Turn:
    role: str   # "user" | "assistant"
    text: str
    intent: str | None = None
    domain: str | None = None
    ts: float = field(default_factory=time.time)


class ConversationState:
    """One session's short-term memory. Bounded by `max_turns`."""

    def __init__(self, session_id: str, max_turns: int = 12) -> None:
        self.session_id = session_id
        self.max_turns = max_turns
        self._turns: deque[Turn] = deque(maxlen=max_turns)

    def add_user(self, text: str, *, intent: str | None = None, domain: str | None = None) -> None:
        self._turns.append(Turn(role="user", text=text, intent=intent, domain=domain))

    def add_assistant(
        self, text: str, *, intent: str | None = None, domain: str | None = None
    ) -> None:
        self._turns.append(Turn(role="assistant", text=text, intent=intent, domain=domain))

    @property
    def turns(self) -> tuple[Turn, ...]:
        return tuple(self._turns)

    def recent(self, n: int) -> tuple[Turn, ...]:
        if n <= 0:
            return ()
        items = list(self._turns)
        return tuple(items[-n:])

    def count_intent(self, intent: str, *, role: str | None = "user") -> int:
        """Count turns matching `intent`. By default counts user turns only.

        Counting only user turns is the right notion of "how many times has
        the user expressed this intent". Pass role=None to count both sides.
        """
        if role is None:
            return sum(1 for t in self._turns if t.intent == intent)
        return sum(1 for t in self._turns if t.intent == intent and t.role == role)

    def is_empty(self) -> bool:
        return not self._turns


class ConversationStore:
    """Thread-safe in-memory bag of ConversationState objects."""

    def __init__(self, max_turns: int = 12) -> None:
        self._states: dict[str, ConversationState] = {}
        self._max_turns = max_turns
        self._lock = Lock()

    def get(self, session_id: str | None) -> ConversationState:
        """Return (and create if missing) the state for a session id.

        A null/empty session_id maps to a shared anonymous session so callers
        without persistence still get coherent multi-turn behavior in one
        request — but in practice anonymous sessions don't accumulate context
        across HTTP requests.
        """
        sid = session_id or "_anonymous_"
        with self._lock:
            state = self._states.get(sid)
            if state is None:
                state = ConversationState(session_id=sid, max_turns=self._max_turns)
                self._states[sid] = state
            return state

    def reset(self, session_id: str) -> None:
        with self._lock:
            self._states.pop(session_id, None)

    def __len__(self) -> int:
        return len(self._states)
