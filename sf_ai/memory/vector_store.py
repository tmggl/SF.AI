"""VectorStore — abstract interface + sovereign in-memory implementation.

Phase 8 default backend is `HashingVectorStore` which uses the existing
Phase 2 HashingVectorizer (BLAKE2b → buckets) to build sparse vectors.
No pretrained embeddings ever land here.

A Qdrant-backed implementation can plug in by subclassing `VectorStore`
and persisting vectors locally. Even with Qdrant, vectors must come from
SF.AI's own encoder (Phase 6+ custom embedding model, when shipped).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sf_ai.core.semantic.hashing_vectorizer import HashingVectorizer, cosine_sparse
from sf_ai.memory.schemas import Chunk, RetrievalResult


class VectorStore(Protocol):
    def add(self, chunk: Chunk) -> None: ...
    def add_many(self, chunks: list[Chunk]) -> None: ...
    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]: ...
    def __len__(self) -> int: ...


@dataclass
class _VecEntry:
    chunk: Chunk
    vector: dict[int, float]


class HashingVectorStore:
    """In-memory store backed by the sovereign HashingVectorizer."""

    def __init__(self, vectorizer: HashingVectorizer | None = None) -> None:
        self.vectorizer = vectorizer or HashingVectorizer()
        self._entries: dict[str, _VecEntry] = {}

    # ---- index ----

    def add(self, chunk: Chunk) -> None:
        vec = self.vectorizer.transform(chunk.text)
        if not vec:
            return
        self._entries[chunk.chunk_id] = _VecEntry(chunk=chunk, vector=vec)

    def add_many(self, chunks: list[Chunk]) -> None:
        for c in chunks:
            self.add(c)

    def remove(self, chunk_id: str) -> None:
        self._entries.pop(chunk_id, None)

    # ---- query ----

    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        if not self._entries:
            return []
        q_vec = self.vectorizer.transform(query)
        if not q_vec:
            return []
        scored: list[tuple[str, float]] = []
        for cid, entry in self._entries.items():
            s = cosine_sparse(q_vec, entry.vector)
            if s > 0:
                scored.append((cid, s))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [
            RetrievalResult(chunk=self._entries[cid].chunk, score=float(s), backend="vector")
            for cid, s in scored[:top_k]
        ]

    def __len__(self) -> int:
        return len(self._entries)


class QdrantVectorStore:
    """Stub for a future Qdrant-backed implementation."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        raise NotImplementedError(
            "QdrantVectorStore is not implemented in Phase 8 default profile. "
            "Use HashingVectorStore for now. A Qdrant adapter can be added "
            "once SF.AI ships a native embedding encoder (Phase 6+)."
        )
