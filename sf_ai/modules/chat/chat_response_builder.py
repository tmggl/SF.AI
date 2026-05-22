"""ChatResponseBuilder — picks the right pattern and trims it to fit the turn.

This is rule-based by design. Phase 6 (SF native LM) will plug into the same
interface but generate instead of select.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.core.nlp.types import NLPAnalysis
from sf_ai.modules.chat.chat_patterns import (
    AFFIRMATION,
    CAPABILITY,
    CLARIFICATION,
    CLARIFICATION_OPEN_QUESTION,
    CONFUSED,
    DIALECT_NOTES,
    FAREWELL,
    GENERAL,
    GREETING,
    HELP,
    IDENTITY,
    LANGUAGE_PREFERENCE,
    NEGATION,
    REPEATED_NOTICE,
    SMALLTALK,
    THANKS,
    WHO_MADE_YOU,
)
from sf_ai.modules.chat.conversation_state import ConversationState


_SMALLTALK_PROMPTS = ("عندك أنت", "أنت كيف حالك", "انت كيف حالك")


_INTENT_TO_PATTERN: dict[str, tuple[str, ...]] = {
    "chat.greeting": GREETING,
    "chat.smalltalk": SMALLTALK,
    "chat.identity": IDENTITY,
    "chat.who_made_you": WHO_MADE_YOU,
    "chat.capability": CAPABILITY,
    "chat.language_preference": LANGUAGE_PREFERENCE,
    "chat.clarification": CLARIFICATION,
    "chat.help": HELP,
    "chat.confused": CONFUSED,
    "chat.thanks": THANKS,
    "chat.affirmation": AFFIRMATION,
    "chat.negation": NEGATION,
    "chat.farewell": FAREWELL,
    "chat.general": GENERAL,
}

# Threshold: after this many occurrences of the same intent we append the
# repeated-notice hint. Soft signal, not a wall.
_REPEAT_HINT_AT = 3


@dataclass(frozen=True)
class BuiltReply:
    text: str
    template_index: int
    intent_used: str
    notes: tuple[str, ...] = ()


class ChatResponseBuilder:
    def build(
        self,
        analysis: NLPAnalysis,
        intent: str,
        state: ConversationState,
    ) -> BuiltReply:
        patterns = _INTENT_TO_PATTERN.get(intent) or GENERAL
        if intent == "chat.clarification":
            patterns = self._clarification_patterns(analysis, state)
        prior_count = state.count_intent(intent)
        idx = min(prior_count, len(patterns) - 1)
        text = patterns[idx]

        notes: list[str] = []

        # Soft repeat-hint after the threshold (chat.identity excluded —
        # there's only one identity message, no need to nag).
        if prior_count >= _REPEAT_HINT_AT and intent != "chat.identity":
            text = f"{text}\n\n{REPEATED_NOTICE}"
            notes.append("repeat_hint")

        # Optional dialect acknowledgement note (NOT spoken to the user,
        # surfaced only on metadata so the dev panel can show it).
        dialect = analysis.detected_dialect
        if dialect in DIALECT_NOTES and dialect != "unknown":
            notes.append(f"dialect:{DIALECT_NOTES[dialect]}")

        # Language tag, useful for the dev panel.
        if analysis.language:
            notes.append(f"language:{analysis.language}")

        return BuiltReply(text=text, template_index=idx, intent_used=intent, notes=tuple(notes))

    def _clarification_patterns(
        self,
        analysis: NLPAnalysis,
        state: ConversationState,
    ) -> tuple[str, ...]:
        """Pick clarification wording from short-term context.

        `عندي؟` after a smalltalk prompt means "what do you mean by at you?",
        while `عندي سؤال` is an opener and should invite the user to ask.
        """
        norm = analysis.normalized_text
        has_question_word = any(word in norm for word in ("سؤال", "سوال", "طلب"))
        recent_assistant = [
            t.text for t in state.recent(6)
            if getattr(t, "role", "") == "assistant"
        ]
        follows_smalltalk = any(
            marker in text
            for text in recent_assistant
            for marker in _SMALLTALK_PROMPTS
        )
        if follows_smalltalk and not has_question_word:
            return CLARIFICATION
        return CLARIFICATION_OPEN_QUESTION
