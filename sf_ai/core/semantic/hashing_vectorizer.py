"""Deterministic hashing vectorizer — sparse, local, no external model.

We map tokens to a fixed number of buckets using a stable hash, then expose
cosine similarity over the resulting sparse vectors. This is a sovereign
substitute for "embedding"-style similarity until SF.AI trains its own
custom encoder in a later phase.
"""

from __future__ import annotations

import hashlib
import math

from sf_ai.core.config import HASHING_VECTOR_BUCKETS
from sf_ai.core.semantic.lexical_similarity import simple_tokenize
from sf_ai.core.semantic.types import SparseVector


def _stable_bucket(token: str, buckets: int) -> int:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % buckets


class HashingVectorizer:
    """Stateless hashing vectorizer with fixed bucket count."""

    def __init__(self, buckets: int = HASHING_VECTOR_BUCKETS) -> None:
        if buckets <= 0:
            raise ValueError("buckets must be positive")
        self.buckets = buckets

    def transform(self, text: str) -> SparseVector:
        """Token counts mapped into a sparse bucket vector."""
        vec: SparseVector = {}
        for tok in simple_tokenize(text):
            idx = _stable_bucket(tok, self.buckets)
            vec[idx] = vec.get(idx, 0.0) + 1.0
        return vec


def cosine_sparse(a: SparseVector, b: SparseVector) -> float:
    """Cosine similarity between two sparse vectors. Returns 0 if either is empty."""
    if not a or not b:
        return 0.0
    # Iterate over the smaller dict for the dot product.
    if len(a) > len(b):
        a, b = b, a
    dot = 0.0
    for idx, val in a.items():
        other = b.get(idx)
        if other is not None:
            dot += val * other
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
