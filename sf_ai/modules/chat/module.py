"""ChatModule — first active domain module in SF.AI.

The Orchestrator dispatches active routing decisions here. The module:

1. Picks the intent (uses the IntentRouter's verdict, falls back to chat.general).
2. Consults ConversationState for prior turns / repeated intents.
3. Builds a reply via ChatResponseBuilder.
4. Updates state with the user turn and the assistant turn.
5. Returns a ModuleResponse the orchestrator can hand back to the API.

No external LLM here. Native generation is opt-in and experimental; templates
remain the default runtime path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.modules.chat.chat_response_builder import ChatResponseBuilder
from sf_ai.modules.chat.conversation_state import ConversationState, ConversationStore
from sf_ai.modules.chat.generation_guard import GenerationGuard
from sf_ai.modules.chat.generation_policy import GenerationPolicy
from sf_ai.modules.chat.native_generator import NativeGenerator
from sf_ai.modules.chat.rag_bridge import ChatRagBridge

_KNOWN_INTENTS: frozenset[str] = frozenset(
    {
        "chat.greeting",
        "chat.smalltalk",
        "chat.presence",
        "chat.understanding",
        "chat.identity",
        "chat.who_made_you",
        "chat.capability",
        "chat.language_preference",
        "chat.clarification",
        "chat.dialogue_test",
        "chat.next_step",
        "chat.training_activation_difference",
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
        generation_policy: GenerationPolicy | None = None,
        generation_guard: GenerationGuard | None = None,
        native_generator: NativeGenerator | None = None,
        rag_bridge: ChatRagBridge | None = None,
        max_turns: int = 12,
    ) -> None:
        self.store = store or ConversationStore(max_turns=max_turns)
        self.builder = builder or ChatResponseBuilder()
        self.generation_policy = generation_policy or GenerationPolicy.from_env()
        self.generation_guard = generation_guard or GenerationGuard()
        self.native_generator = native_generator
        if (
            self.native_generator is None
            and self.generation_policy.enabled
            and self.generation_policy.experimental_runtime
        ):
            self.native_generator = NativeGenerator()
        self.rag_bridge = rag_bridge

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

        text = reply.text
        rag_notes = self._rag_notes_no_bridge()
        if self.rag_bridge is not None:
            rag_context = self.rag_bridge.maybe_build_context(
                analysis.original_text,
                intent=intent,
            )
            rag_notes = rag_context.notes
            if rag_context.used:
                text = rag_context.text

        text, generator_notes = self._maybe_generate_native(
            fallback_text=text,
            intent=intent,
            analysis=analysis,
            rag_used=("rag:used" in rag_notes),
        )
        notes = reply.notes + rag_notes + generator_notes

        state.add_assistant(text, intent=intent, domain=self.domain)

        sid_visible = state.session_id if state.session_id != "_anonymous_" else ""
        return ModuleResponse(
            text=text,
            intent_used=reply.intent_used,
            template_index=reply.template_index,
            session_id=sid_visible,
            turn_count=len(state.turns),
            notes=notes,
        )

    def _rag_notes_no_bridge(self) -> tuple[str, ...]:
        return ("rag:not_configured",)

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

    def _maybe_generate_native(
        self,
        *,
        fallback_text: str,
        intent: str,
        analysis: NLPAnalysis,
        rag_used: bool,
    ) -> tuple[str, tuple[str, ...]]:
        """Optionally use the sovereign native generator for single-user testing.

        This path is deliberately behind two flags:
        `SF_ENABLE_NATIVE_GENERATOR=true` and
        `SF_NATIVE_GENERATOR_EXPERIMENTAL=true`.
        """
        if not self.generation_policy.enabled:
            return fallback_text, ("generator:template", "native_generator:disabled")
        if not self.generation_policy.experimental_runtime:
            return fallback_text, (
                "generator:template",
                "native_generator:experimental_runtime_disabled",
            )
        if rag_used:
            return fallback_text, ("generator:template", "native_generator:skipped_rag_used")

        decision = self.generation_policy.decide(
            domain=self.domain,
            intent=intent,
            confidence=1.0,
            domain_status="active",
            requires_safety=bool(analysis.safety_flags),
            fallback_used=False,
        )
        if not decision.allowed:
            return fallback_text, ("generator:template", f"native_generator:{decision.reason}")

        generator = self.native_generator or NativeGenerator()
        result = generator.generate(
            analysis.original_text,
            dialect=analysis.detected_dialect,
            max_new_tokens=self.generation_policy.max_new_tokens,
            temperature=self.generation_policy.temperature,
            top_k=self.generation_policy.top_k,
        )
        if not result.used:
            return fallback_text, (
                "generator:template",
                f"native_generator:{result.reason}",
            )
        verdict = self.generation_guard.inspect_for_prompt(
            analysis.original_text,
            result.text,
        )
        if not verdict.allowed:
            return fallback_text, (
                "generator:template",
                "native_generator:canary_blocked",
                f"generation_guard:{verdict.reason}",
                f"generation_repetition:{verdict.repetition_ratio:.2f}",
                f"generation_arabic:{verdict.arabic_ratio:.2f}",
            )
        return (
            result.text,
            (
                f"generator:{result.generator}",
                "native_generator:generated",
                "native_generator:canary_passed",
            ),
        )


@lru_cache(maxsize=1)
def get_default_chat_module() -> ChatModule:
    return ChatModule()
