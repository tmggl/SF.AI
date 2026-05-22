"""sf_ai.core.semantic — local-only similarity tools.

No pretrained embeddings. Phase 2 ships:
- lexical_similarity (Jaccard / token overlap)
- hashing_vectorizer (sparse, fully deterministic)
- semantic_explorer (combines signals)

Designed to be replaced/augmented later by a custom SF.AI embedding model
trained from scratch — see Phase 6+.
"""

from sf_ai.core.semantic.hashing_vectorizer import HashingVectorizer, cosine_sparse
from sf_ai.core.semantic.lexical_similarity import (
    jaccard,
    normalized_simple,
    overlap_count,
    simple_tokenize,
)
from sf_ai.core.semantic.semantic_explorer import SemanticExplorer, SignalMatch

__all__ = [
    "HashingVectorizer",
    "SemanticExplorer",
    "SignalMatch",
    "cosine_sparse",
    "jaccard",
    "normalized_simple",
    "overlap_count",
    "simple_tokenize",
]
