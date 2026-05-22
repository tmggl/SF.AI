# RAG_PLAN.md

## SF.AI — Local RAG Foundation (Phase 8)

> **القاعدة:** الـ RAG لا يكسر السيادة طالما **vectors محلية أو من SF.AI**. إن استورد embedding model خارجي، يكسر السيادة فورًا.

---

## لماذا RAG وليس Knowledge in Weights

| السؤال | المسار المفضَّل |
|--------|----------------|
| "ما عاصمة الصين؟" | استرجاع من corpus موثَّق (Phase 7 article ingest + Phase 8 retrieval) |
| "اشرح كلمة شلون" | DialectMapper (Phase 3) + saudi_seed_v1 (Phase 3.6) — lookup مباشر |
| "كيف حالك" | ChatModule (Phase 4) — يتعلمها النموذج في الأوزان |
| "اكتب رد ودود" | النموذج (Phase 6) — شكل اللغة |
| "لخّص لي هذا المقال: <URL>" | Phase 7 ResearchModule + (لاحقًا) Phase 8 retrieval لتوسيع السياق |

**الفلسفة:** النموذج يتعلم **شكل اللغة**؛ النظام يأتي بـ **المحتوى**.

---

## المكونات

موقعها: [sf_ai/memory/](../sf_ai/memory/)

| ملف | المسؤولية |
|------|-----------|
| `schemas.py` | `Document`, `Chunk`, `RetrievalResult` |
| `short_term.py` | re-exports `ConversationStore` (Phase 4) |
| `long_term.py` | `LongTermMemory` (in-memory) + `chunk_text()` بانقسام فقرات/جمل |
| `sparse_store.py` | `SparseStore` — BM25 على tokenizer + ArabicNormalizer (Phase 3) |
| `vector_store.py` | `HashingVectorStore` (افتراضي) + `QdrantVectorStore` stub |
| `retrieval.py` | `HybridRetriever` يخلط sparse + vector بأوزان |

---

## ما هو سيادي وما ليس كذلك

### مسموح (سيادي)
- `SparseStore` — BM25 يستخدم `LightTokenizer` + `ArabicNormalizer` (Phase 3). 100% rule-based.
- `HashingVectorStore` — يستخدم `HashingVectorizer` (Phase 2: BLAKE2b → buckets). deterministic، صفر معرفة متعلمة.
- `LongTermMemory` — تخزين بسيط in-memory للوثائق والـ chunks.
- `HybridRetriever` — يخلط backendين سياديين فقط.

### ممنوع (يكسر السيادة)
- ❌ `sentence-transformers`
- ❌ OpenAI / Cohere embeddings APIs
- ❌ HuggingFace pretrained encoders
- ❌ أي `from_pretrained()` على encoder
- ❌ Qdrant **مع** embeddings مستوردة

### المسار المسموح لـ Qdrant
عند الانتقال لـ Qdrant مستقبلًا:
1. SF.AI يدرّب encoder عصبي من الصفر (Phase 6+) أو يستخدم نفس HashingVectorizer.
2. الـ vectors التي تذهب إلى Qdrant **من إنتاجنا فقط**.
3. لا `model.encode()` من مكتبة خارجية.

`QdrantVectorStore` في `vector_store.py` يرفع `NotImplementedError` افتراضيًا — تفعيله قرار Phase خاص.

---

## التدفق

```
user message
   │
   ▼ NLPPipeline.analyze_user_text → NLPAnalysis
   │
   ▼ Orchestrator routes domain/intent
   │
   ▼ (Phase 8 hook) HybridRetriever.search(canonical_text)
   │     ├── SparseStore (BM25)        → top-K
   │     └── HashingVectorStore        → top-K
   │     └── merge normalized scores → top-K hybrid
   │
   ▼ Module decides whether to use the retrieved chunks
   │     (Phase 4 chat: ignores them)
   │     (Phase 7 research: composes with them)
   │
   ▼ ResponseComposer / ChatResponseBuilder
   │
   ▼ Final response
```

في Phase 8 الحالي، الـ retriever مبني وقابل للاستدعاء، لكن **لا يُدخَل تلقائيًا** في الـ Orchestrator. الـ wiring قرار صريح في Phase 10/11.

---

## API برمجي

```python
from sf_ai.memory import (
    Document,
    HybridRetriever,
    RetrievalConfig,
)

retriever = HybridRetriever(config=RetrievalConfig(top_k=3))

# Ingest.
retriever.add_document(Document(
    doc_id="d1",
    text="نص الوثيقة هنا...",
    title="عنوان",
    source_url="https://x.test/doc-1",
    language="ar",
))

# Query.
hits = retriever.search("ابحث عن X")
for hit in hits:
    print(hit.score, hit.backend, hit.chunk.title, hit.chunk.text[:80])
```

---

## الإعدادات الافتراضية

| المتغير | القيمة | لماذا |
|---------|--------|-------|
| `chunk_size` | 800 حرف | يوازن بين الـ context و BM25 IDF |
| `top_k` | 5 | عدد منطقي للـ chunks المسترجَعة |
| `sparse_weight` | 0.7 | BM25 أقوى من hashing على نصوص قصيرة |
| `vector_weight` | 0.3 | يكمّل sparse عند مرادفات قريبة |
| `k1` | 1.5 | معيار BM25 |
| `b` | 0.75 | معيار BM25 |
| `buckets` (HashingVectorizer) | 2048 | من Phase 2 config |

---

## ما لم يُنفَّذ في Phase 8 (مقصود)

- ❌ Qdrant فعّال — stub فقط.
- ❌ persistence على disk — كل شيء in-memory.
- ❌ neural encoder — ينتظر Phase 6 ينضج.
- ❌ تكامل تلقائي مع ChatModule — قرار صريح لاحقًا.
- ❌ multi-tenant isolation — حاليًا single store.

---

## الاختبارات

```
tests/test_rag_sparse_retrieval.py — 14 passed
```

تغطية: chunking / LongTermMemory add+delete / SparseStore (Arabic retrieval + remove + empty query + top_k validation) / HashingVectorStore (Arabic similarity + Qdrant stub raises) / HybridRetriever (blend + empty corpus + config validation).
