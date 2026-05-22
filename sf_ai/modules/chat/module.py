"""ChatModule — first active domain module in SF.AI.

The Orchestrator dispatches active routing decisions here. The module:

1. Picks the intent (uses the IntentRouter's verdict, falls back to chat.general).
2. Consults ConversationState for prior turns / repeated intents.
3. Builds a reply via ChatResponseBuilder.
4. Updates state with the user turn and the assistant turn.
5. Returns a ModuleResponse the orchestrator can hand back to the API.

No LLM here. When SF Native LM ships (Phase 6) it will plug in by replacing
ChatResponseBuilder's generation backend; the public ChatModule API stays.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.modules.chat.chat_response_builder import ChatResponseBuilder
from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore


_KNOWN_INTENTS: frozenset[str] = frozenset(
    {
        "chat.greeting",
        "chat.smalltalk",
        "chat.identity",
        "chat.who_made_you",
        "chat.capability",
        "chat.language_preference",
        "chat.clarification",
        "chat.help",
        "chat.confused",
        "chat.thanks",
        "chat.affirmation",
        "chat.negation",
        "chat.farewell",
        "chat.general",
    }
)


@dataclass(frozen=True)
class ModuleResponse:
    text: str
    intent_used: str
    template_index: int
    session_id: str
    turn_count: int
    notes: tuple[str, ...] = field(default_factory=tuple)


class ChatModule:
    """Active module for the `chat` domain."""

    domain = "chat"

    def __init__(
        self,
        store: ConversationStore | None = None,
        builder: ChatResponseBuilder | None = None,
        max_turns: int = 12,
    ) -> None:
        self.store = store or ConversationStore(max_turns=max_turns)
        self.builder = builder or ChatResponseBuilder()

    def handle(
        self,
        analysis: NLPAnalysis,
        *,
        intent: str,
        session_id: str | None,
    ) -> ModuleResponse:
        # Normalize intent — anything unknown collapses to chat.general so
        # we never produce an empty reply.
        if intent not in _KNOWN_INTENTS:
            intent = "chat.general"

        state = self.store.get(session_id)

        # Record the user turn BEFORE building, so count_intent reflects history.
        state.add_user(analysis.original_text, intent=intent, domain=self.domain)

        # Build reply: note that count_intent now includes the current user
        # turn, so the first occurrence of the intent has count==1.
        # ChatResponseBuilder treats count as "prior occurrences" — we subtract 1.
        # To keep the builder simple, we temporarily pop, build, then push back.
        # Simpler: pass count_intent - 1 logic happens inside the builder by
        # virtue of state being updated after assistant. So flip the order:
        # we recorded already; let the builder use `prior_count = count - 1`.
        prior_count = state.count_intent(intent) - 1
        reply = self._build_with_prior_count(analysis, intent, state, prior_count)

        state.add_assistant(reply.text, intent=intent, domain=self.domain)

        sid_visible = state.session_id if state.session_id != "_anonymous_" else ""
        return ModuleResponse(
            text=reply.text,
            intent_used=reply.intent_used,
            template_index=reply.template_index,
            session_id=sid_visible,
            turn_count=len(state.turns),
            notes=reply.notes,
        )

    def _build_with_prior_count(
        self,
        analysis: NLPAnalysis,
        intent: str,
        state: ConversationState,
        prior_count: int,
    ):
        # Lightweight wrapper so the builder can see the "before this user
        # turn was added" count without us having to refactor ConversationState.
        class _StateView:
            def __init__(self, real_state: ConversationState, pc: int) -> None:
                self._state = real_state
                self._pc = pc

            def count_intent(self, intent_name: str) -> int:
                # Builder asks for this intent only.
                if intent_name == intent:
                    return self._pc
                return self._state.count_intent(intent_name)

            @property
            def session_id(self) -> str:
                return self._state.session_id

            def recent(self, n: int):
                return self._state.recent(n)

        return self.builder.build(analysis, intent, _StateView(state, prior_count))  # type: ignore[arg-type]


@lru_cache(maxsize=1)
def get_default_chat_module() -> ChatModule:
    return ChatModule()
