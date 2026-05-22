"""Memory schemas — Phase 8 RAG.

Shared dataclasses for documents, chunks, and retrieval results. Used by
the sparse store, the in-memory long-term store, and any future Qdrant-
backed vector store.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str
    source_url: str = ""
    title: str = ""
    language: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    added_at: str = field(default_factory=_utc_now)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    position: int = 0     # index of the chunk within its document
    source_url: str = ""
    title: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float
    backend: str          # "sparse" | "vector" | "hybrid"
