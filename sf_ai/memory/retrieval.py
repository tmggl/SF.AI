"""HybridRetriever — combines sparse (BM25) + sovereign vector (hashing).

Strategy: run both backends, normalize each list to [0, 1], blend with a
weighted sum, then return the top-K unique chunks. The default weights
favor sparse retrieval because it's the more discriminative signal until
SF.AI ships its own neural encoder.
"""

from __future__ import annotations

from dataclasses import dataclass

from sf_ai.memory.long_term import LongTermMemory
from sf_ai.memory.schemas import Chunk, Document, RetrievalResult
from sf_ai.memory.sparse_store import SparseStore
from sf_ai.memory.vector_store import HashingVectorStore, VectorStore


def _normalize(scores: list[float]) -> list[float]:
    if not scores:
        return scores
    mx = max(scores)
    if mx <= 0:
        return [0.0 for _ in scores]
    return [s / mx for s in scores]


@dataclass(frozen=True)
class RetrievalConfig:
    top_k: int = 5
    sparse_weight: float = 0.7
    vector_weight: float = 0.3

    def __post_init__(self) -> None:
        if self.top_k < 1:
            raise ValueError("top_k must be >= 1")
        if self.sparse_weight < 0 or self.vector_weight < 0:
            raise ValueError("weights must be >= 0")
        if self.sparse_weight + self.vector_weight <= 0:
            raise ValueError("at least one weight must be > 0")


class HybridRetriever:
    """One-stop retrieval over LongTermMemory + Sparse + Vector backends."""

    def __init__(
        self,
        *,
        memory: LongTermMemory | None = None,
        sparse: SparseStore | None = None,
        vector: VectorStore | None = None,
        config: RetrievalConfig | None = None,
    ) -> None:
        self.memory = memory or LongTermMemory()
        self.sparse = sparse or SparseStore()
        self.vector = vector or HashingVectorStore()
        self.config = config or RetrievalConfig()

    # ---- ingest ----

    def add_document(self, doc: Document) -> list[Chunk]:
        chunks = self.memory.add_document(doc)
        self.sparse.add_many(chunks)
        self.vector.add_many(chunks)
        return chunks

    # ---- query ----

    def search(self, query: str, *, top_k: int | None = None) -> list[RetrievalResult]:
        k = top_k or self.config.top_k
        sparse_hits = self.sparse.search(query, top_k=k * 2)
        vector_hits = self.vector.search(query, top_k=k * 2)

        sparse_scores = _normalize([h.score for h in sparse_hits])
        vector_scores = _normalize([h.score for h in vector_hits])

        merged: dict[str, dict[str, float | Chunk]] = {}
        for h, ns in zip(sparse_hits, sparse_scores):
            slot = merged.setdefault(
                h.chunk.chunk_id, {"sparse": 0.0, "vector": 0.0, "chunk": h.chunk}
            )
            slot["sparse"] = float(slot.get("sparse", 0.0)) + ns
        for h, nv in zip(vector_hits, vector_scores):
            slot = merged.setdefault(
                h.chunk.chunk_id, {"sparse": 0.0, "vector": 0.0, "chunk": h.chunk}
            )
            slot["vector"] = float(slot.get("vector", 0.0)) + nv

        out: list[RetrievalResult] = []
        for cid, info in merged.items():
            score = (
                self.config.sparse_weight * float(info["sparse"])  # type: ignore[arg-type]
                + self.config.vector_weight * float(info["vector"])  # type: ignore[arg-type]
            )
            if score <= 0:
                continue
            out.append(
                RetrievalResult(
                    chunk=info["chunk"],  # type: ignore[arg-type]
                    score=score,
                    backend="hybrid",
                )
            )
        out.sort(key=lambda r: r.score, reverse=True)
        return out[:k]

    def __len__(self) -> int:
        return len(self.memory)
