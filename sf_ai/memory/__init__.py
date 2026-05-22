"""sf_ai.memory — short-term + long-term + sparse + vector + retrieval (Phase 8).

Sovereign by default:
- Short-term  : ConversationStore from Phase 4.
- Long-term   : in-memory document/chunk store.
- Sparse      : BM25 over the SF.AI tokenizer/normalizer.
- Vector      : sovereign HashingVectorStore (no pretrained embeddings).
- Hybrid      : weighted blend (default sparse_weight=0.7, vector_weight=0.3).

A Qdrant-backed VectorStore is reserved for later phases. RAG never imports
SentenceTransformers, OpenAI embeddings, or any external encoder.
"""

from sf_ai.memory.long_term import LongTermMemory, chunk_text
from sf_ai.memory.retrieval import HybridRetriever, RetrievalConfig
from sf_ai.memory.schemas import Chunk, Document, RetrievalResult
from sf_ai.memory.short_term import ConversationState, ConversationStore, Turn
from sf_ai.memory.sparse_store import SparseStore
from sf_ai.memory.vector_store import (
    HashingVectorStore,
    QdrantVectorStore,
    VectorStore,
)

__all__ = [
    "Chunk",
    "ConversationState",
    "ConversationStore",
    "Document",
    "HashingVectorStore",
    "HybridRetriever",
    "LongTermMemory",
    "QdrantVectorStore",
    "RetrievalConfig",
    "RetrievalResult",
    "SparseStore",
    "Turn",
    "VectorStore",
    "chunk_text",
]
