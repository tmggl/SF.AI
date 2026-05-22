"""RAG bridge for ChatModule.

This bridge is local-only. It never crawls the web, never calls external
embeddings, and only reads from a provided HybridRetriever.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.memory import HybridRetriever
from sf_ai.modules.chat.context_builder import BuiltContext, ContextBuilder


PINNED_INTENTS = frozenset(
    {
        "chat.greeting",
        "chat.smalltalk",
        "chat.identity",
        "chat.who_made_you",
        "chat.capability",
        "chat.language_preference",
        "chat.thanks",
        "chat.affirmation",
        "chat.negation",
        "chat.farewell",
    }
)


@dataclass(frozen=True)
class RagBridgeConfig:
    top_k: int = 3
    min_score: float = 0.35
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.top_k < 1:
            raise ValueError("top_k must be >= 1")
        if self.min_score < 0:
            raise ValueError("min_score must be >= 0")


class ChatRagBridge:
    """Small adapter between ChatModule and HybridRetriever."""

    def __init__(
        self,
        retriever: HybridRetriever,
        *,
        context_builder: ContextBuilder | None = None,
        config: RagBridgeConfig | None = None,
    ) -> None:
        self.retriever = retriever
        self.context_builder = context_builder or ContextBuilder()
        self.config = config or RagBridgeConfig()

    def maybe_build_context(self, query: str, *, intent: str) -> BuiltContext:
        if not self.config.enabled:
            return BuiltContext(used=False, notes=("rag:disabled",))
        if intent in PINNED_INTENTS:
            return BuiltContext(used=False, notes=("rag:pinned_intent",))
        if not query.strip():
            return BuiltContext(used=False, notes=("rag:empty_query",))
        if len(self.retriever) == 0:
            return BuiltContext(used=False, notes=("rag:empty_index",))

        hits = [
            h
            for h in self.retriever.search(query, top_k=self.config.top_k)
            if h.score >= self.config.min_score
        ]
        if not hits:
            return BuiltContext(used=False, notes=("rag:no_hits",))
        return self.context_builder.build(hits)
