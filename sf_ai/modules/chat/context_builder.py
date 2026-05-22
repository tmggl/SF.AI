"""ContextBuilder — formats local RAG snippets for chat.

Phase 17 deliberately keeps retrieval separate from generation. The context
builder takes retrieved chunks and produces a short Arabic answer that clearly
labels the source as local memory, not model knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.memory.schemas import RetrievalResult


@dataclass(frozen=True)
class LocalContextSnippet:
    text: str
    title: str
    source_url: str
    score: float
    backend: str

    @property
    def source_label(self) -> str:
        if self.title and self.source_url:
            return f"{self.title} — {self.source_url}"
        if self.title:
            return self.title
        if self.source_url:
            return self.source_url
        return "ذاكرة محلية"


@dataclass(frozen=True)
class BuiltContext:
    used: bool
    text: str = ""
    snippets: tuple[LocalContextSnippet, ...] = ()
    notes: tuple[str, ...] = ()


class ContextBuilder:
    """Turn retrieved chunks into a compact Arabic local-memory response."""

    def __init__(self, *, max_snippets: int = 2, max_chars_per_snippet: int = 260) -> None:
        if max_snippets < 1:
            raise ValueError("max_snippets must be >= 1")
        if max_chars_per_snippet < 80:
            raise ValueError("max_chars_per_snippet must be >= 80")
        self.max_snippets = max_snippets
        self.max_chars_per_snippet = max_chars_per_snippet

    def build(self, hits: list[RetrievalResult]) -> BuiltContext:
        snippets = tuple(
            self._snippet_from_hit(hit)
            for hit in hits[: self.max_snippets]
            if hit.chunk.text.strip()
        )
        if not snippets:
            return BuiltContext(used=False, notes=("rag:no_context",))

        lines = ["من الذاكرة المحلية:"]
        for idx, snip in enumerate(snippets, start=1):
            lines.append(f"{idx}. {snip.text}")
        source_labels = _dedupe(s.source_label for s in snippets)
        lines.append("")
        lines.append("المصدر: " + " ؛ ".join(source_labels))
        notes = (
            "rag:used",
            f"rag_snippets:{len(snippets)}",
            "rag_sources:" + "|".join(source_labels),
        )
        return BuiltContext(
            used=True,
            text="\n".join(lines),
            snippets=snippets,
            notes=notes,
        )

    def _snippet_from_hit(self, hit: RetrievalResult) -> LocalContextSnippet:
        text = _compact(hit.chunk.text)
        if len(text) > self.max_chars_per_snippet:
            text = text[: self.max_chars_per_snippet].rstrip() + "..."
        return LocalContextSnippet(
            text=text,
            title=hit.chunk.title,
            source_url=hit.chunk.source_url,
            score=hit.score,
            backend=hit.backend,
        )


def _compact(text: str) -> str:
    return " ".join(text.split())


def _dedupe(items) -> list[str]:  # type: ignore[no-untyped-def]
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out
