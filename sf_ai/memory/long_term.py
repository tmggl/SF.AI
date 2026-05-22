"""LongTermMemory — in-memory document/chunk store (Phase 8).

Pure Python, no external dependency. A future Qdrant-backed implementation
will conform to the same `add_document` / `chunks_for` / `all_chunks` shape.
"""

from __future__ import annotations

import hashlib
from threading import Lock

from sf_ai.memory.schemas import Chunk, Document


def _chunk_id(doc_id: str, position: int) -> str:
    h = hashlib.blake2b(f"{doc_id}#{position}".encode("utf-8"), digest_size=8).hexdigest()
    return f"{doc_id}:{position}:{h}"


def chunk_text(text: str, *, max_chars: int = 800) -> list[str]:
    """Split text into bounded chunks at paragraph/sentence boundaries.

    Cheap-and-cheerful for Phase 8. Better chunking (semantic) lands later.
    """
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for p in paragraphs:
        if buf_len + len(p) + 2 <= max_chars:
            buf.append(p)
            buf_len += len(p) + 2
        else:
            if buf:
                chunks.append("\n\n".join(buf))
                buf, buf_len = [], 0
            if len(p) <= max_chars:
                buf.append(p)
                buf_len = len(p)
            else:
                # Hard split over-long paragraph into windows of max_chars.
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i : i + max_chars])
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


class LongTermMemory:
    """Thread-safe in-memory document/chunk store."""

    def __init__(self, *, chunk_size: int = 800) -> None:
        self.chunk_size = chunk_size
        self._docs: dict[str, Document] = {}
        self._chunks: dict[str, list[Chunk]] = {}
        self._lock = Lock()

    # ---- write ----

    def add_document(self, doc: Document) -> list[Chunk]:
        pieces = chunk_text(doc.text, max_chars=self.chunk_size)
        chunks = [
            Chunk(
                chunk_id=_chunk_id(doc.doc_id, i),
                doc_id=doc.doc_id,
                text=piece,
                position=i,
                source_url=doc.source_url,
                title=doc.title,
                metadata=dict(doc.metadata),
            )
            for i, piece in enumerate(pieces)
        ]
        with self._lock:
            self._docs[doc.doc_id] = doc
            self._chunks[doc.doc_id] = chunks
        return chunks

    def delete_document(self, doc_id: str) -> None:
        with self._lock:
            self._docs.pop(doc_id, None)
            self._chunks.pop(doc_id, None)

    # ---- read ----

    def get_document(self, doc_id: str) -> Document | None:
        return self._docs.get(doc_id)

    def chunks_for(self, doc_id: str) -> list[Chunk]:
        return list(self._chunks.get(doc_id, ()))

    def all_chunks(self) -> list[Chunk]:
        out: list[Chunk] = []
        for chunks in self._chunks.values():
            out.extend(chunks)
        return out

    def all_documents(self) -> list[Document]:
        return list(self._docs.values())

    def __len__(self) -> int:
        return len(self._docs)
