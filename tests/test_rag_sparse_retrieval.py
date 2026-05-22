"""Phase 8 — Local RAG foundation: SparseStore + VectorStore + HybridRetriever."""

from __future__ import annotations

import pytest

from sf_ai.memory import (
    Chunk,
    Document,
    HashingVectorStore,
    HybridRetriever,
    LongTermMemory,
    QdrantVectorStore,
    RetrievalConfig,
    SparseStore,
    chunk_text,
)


# ---------- chunking ----------

def test_chunk_text_empty() -> None:
    assert chunk_text("") == []


def test_chunk_text_splits_on_paragraphs() -> None:
    text = "أول فقرة.\n\nثانية فقرة قصيرة.\n\nثالثة"
    chunks = chunk_text(text, max_chars=20)
    assert len(chunks) >= 2
    assert all(len(c) <= 60 for c in chunks)


def test_chunk_text_hard_splits_long_paragraph() -> None:
    text = "ا" * 50
    chunks = chunk_text(text, max_chars=10)
    assert len(chunks) == 5


# ---------- LongTermMemory ----------

def test_long_term_add_and_query() -> None:
    mem = LongTermMemory(chunk_size=200)
    doc = Document(doc_id="d1", text="مرحبا بالعالم.\n\nفقرة ثانية.",
                   source_url="https://x.test/")
    chunks = mem.add_document(doc)
    assert len(chunks) >= 1
    assert mem.get_document("d1") is doc
    assert mem.chunks_for("d1") == chunks
    assert len(mem.all_chunks()) == len(chunks)


def test_long_term_delete() -> None:
    mem = LongTermMemory()
    mem.add_document(Document(doc_id="d1", text="hi there"))
    mem.delete_document("d1")
    assert mem.get_document("d1") is None
    assert mem.all_chunks() == []


# ---------- SparseStore ----------

def test_sparse_store_retrieves_arabic_chunks() -> None:
    store = SparseStore()
    chunks = [
        Chunk(chunk_id="c1", doc_id="d1", text="السيادة المعرفية مهمة في الذكاء الاصطناعي"),
        Chunk(chunk_id="c2", doc_id="d2", text="الطعام السعودي يشمل الكبسة والمرقوق"),
        Chunk(chunk_id="c3", doc_id="d3", text="بناء النماذج من الصفر مسار طويل"),
    ]
    store.add_many(chunks)
    results = store.search("ذكاء اصطناعي السيادة", top_k=2)
    assert results
    assert results[0].chunk.chunk_id == "c1"
    assert results[0].backend == "sparse"


def test_sparse_store_remove_drops_term_frequency() -> None:
    store = SparseStore()
    chunks = [
        Chunk(chunk_id="c1", doc_id="d1", text="alpha bravo"),
        Chunk(chunk_id="c2", doc_id="d2", text="bravo charlie"),
    ]
    store.add_many(chunks)
    store.remove("c1")
    assert len(store) == 1
    res = store.search("alpha", top_k=3)
    # Removed chunk should no longer be returned.
    assert all(r.chunk.chunk_id != "c1" for r in res)


def test_sparse_store_handles_empty_query() -> None:
    store = SparseStore()
    store.add(Chunk(chunk_id="c1", doc_id="d1", text="x y z"))
    assert store.search("", top_k=3) == []


def test_sparse_store_top_k_validation() -> None:
    store = SparseStore()
    with pytest.raises(ValueError):
        store.search("q", top_k=0)


# ---------- HashingVectorStore ----------

def test_hashing_vector_store_retrieves_similar_text() -> None:
    store = HashingVectorStore()
    chunks = [
        Chunk(chunk_id="c1", doc_id="d1",
              text="السيادة المعرفية تعني بناء النموذج من الصفر"),
        Chunk(chunk_id="c2", doc_id="d2", text="الطعام السعودي ثقافة غنية"),
    ]
    store.add_many(chunks)
    res = store.search("السيادة المعرفية", top_k=1)
    assert res
    assert res[0].chunk.chunk_id == "c1"
    assert res[0].backend == "vector"


def test_qdrant_stub_raises() -> None:
    with pytest.raises(NotImplementedError):
        QdrantVectorStore()


# ---------- HybridRetriever ----------

def test_hybrid_retriever_blends_sparse_and_vector() -> None:
    retriever = HybridRetriever(config=RetrievalConfig(top_k=3))
    docs = [
        Document(doc_id="d1",
                 text="الذكاء الاصطناعي السيادي يبدأ من random init.",
                 title="A", source_url="https://x.test/a"),
        Document(doc_id="d2",
                 text="الكبسة والمرقوق من أشهر الأطباق السعودية.",
                 title="B", source_url="https://x.test/b"),
        Document(doc_id="d3",
                 text="البحث في الويب يحتاج احترام robots.txt دائمًا.",
                 title="C", source_url="https://x.test/c"),
    ]
    for d in docs:
        retriever.add_document(d)
    results = retriever.search("الذكاء الاصطناعي السيادي", top_k=2)
    assert results
    assert results[0].chunk.doc_id == "d1"
    assert results[0].backend == "hybrid"


def test_hybrid_retriever_empty_corpus_returns_nothing() -> None:
    retriever = HybridRetriever()
    assert retriever.search("anything") == []


def test_retrieval_config_validates() -> None:
    with pytest.raises(ValueError):
        RetrievalConfig(top_k=0)
    with pytest.raises(ValueError):
        RetrievalConfig(sparse_weight=-1)
    with pytest.raises(ValueError):
        RetrievalConfig(sparse_weight=0, vector_weight=0)
