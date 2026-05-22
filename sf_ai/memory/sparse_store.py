"""SparseStore — BM25-style retrieval, pure Python.

Sovereign: no embeddings, no external models. Tokens come from the same
LightTokenizer / normalizer used by the NLP layer, so a query in Arabic
matches a corpus normalized the same way.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sf_ai.core.nlp import ArabicNormalizer, LightTokenizer
from sf_ai.memory.schemas import Chunk, RetrievalResult


@dataclass
class _DocStats:
    chunk_id: str
    term_freq: dict[str, int]
    length: int


class SparseStore:
    """BM25 over a collection of Chunks. Pure Python; rebuild on add."""

    def __init__(
        self,
        *,
        k1: float = 1.5,
        b: float = 0.75,
        normalize: bool = True,
        tokenizer: LightTokenizer | None = None,
        normalizer: ArabicNormalizer | None = None,
    ) -> None:
        self.k1 = k1
        self.b = b
        self.normalize = normalize
        self.tokenizer = tokenizer or LightTokenizer(drop_stopwords=True)
        self.normalizer = normalizer or ArabicNormalizer()
        self._chunks: dict[str, Chunk] = {}
        self._stats: dict[str, _DocStats] = {}
        self._doc_freq: dict[str, int] = {}
        self._avg_len: float = 0.0

    # ---- preprocessing ----

    def _tokenize(self, text: str) -> list[str]:
        if self.normalize:
            text = self.normalizer.normalize(text)
        return self.tokenizer.tokenize(text)

    # ---- index ----

    def add(self, chunk: Chunk) -> None:
        toks = self._tokenize(chunk.text)
        if not toks:
            return
        freq: dict[str, int] = {}
        for t in toks:
            freq[t] = freq.get(t, 0) + 1
        self._chunks[chunk.chunk_id] = chunk
        self._stats[chunk.chunk_id] = _DocStats(
            chunk_id=chunk.chunk_id, term_freq=freq, length=len(toks)
        )
        for t in set(toks):
            self._doc_freq[t] = self._doc_freq.get(t, 0) + 1
        self._refresh_avg_len()

    def add_many(self, chunks: list[Chunk]) -> None:
        for c in chunks:
            self.add(c)

    def remove(self, chunk_id: str) -> None:
        stats = self._stats.pop(chunk_id, None)
        if stats is None:
            return
        self._chunks.pop(chunk_id, None)
        for t in set(stats.term_freq):
            new = self._doc_freq.get(t, 0) - 1
            if new <= 0:
                self._doc_freq.pop(t, None)
            else:
                self._doc_freq[t] = new
        self._refresh_avg_len()

    def _refresh_avg_len(self) -> None:
        if not self._stats:
            self._avg_len = 0.0
            return
        total = sum(s.length for s in self._stats.values())
        self._avg_len = total / len(self._stats)

    # ---- query ----

    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        if not self._stats:
            return []

        q_toks = self._tokenize(query)
        if not q_toks:
            return []
        N = len(self._stats)

        scored: list[tuple[str, float]] = []
        for cid, stats in self._stats.items():
            score = 0.0
            for t in q_toks:
                tf = stats.term_freq.get(t)
                if not tf:
                    continue
                df = self._doc_freq.get(t, 0)
                if df <= 0:
                    continue
                idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
                denom = tf + self.k1 * (
                    1.0 - self.b + self.b * (stats.length / max(self._avg_len, 1.0))
                )
                score += idf * (tf * (self.k1 + 1.0)) / denom
            if score > 0:
                scored.append((cid, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        out: list[RetrievalResult] = []
        for cid, s in scored[:top_k]:
            out.append(
                RetrievalResult(chunk=self._chunks[cid], score=float(s), backend="sparse")
            )
        return out

    def __len__(self) -> int:
        return len(self._chunks)
