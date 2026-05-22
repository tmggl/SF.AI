# SEMANTIC_EXPLORER.md

## Semantic Explorer — SF.AI

طبقة الـ similarity الدلالي في SF.AI **محلية بالكامل**. لا تستخدم:
- ❌ pretrained embeddings
- ❌ sentence-transformers
- ❌ أي encoder جاهز

تستخدم فقط:
- ✅ Lexical similarity (Jaccard / token overlap)
- ✅ Phrase containment على نص مُطبَّع
- ✅ Fuzzy matching عبر `difflib.SequenceMatcher`
- ✅ Hashing vectorizer سيادي (BLAKE2b deterministic)

---

## المكونات

### lexical_similarity.py
- `normalized_simple(text)` — تطبيع خفيف (NFC + lower + collapse spaces). الـ Phase 3 يضيف ArabicNormalizer كامل فوقه.
- `simple_tokenize(text)` — تقسيم على whitespace بعد التطبيع.
- `overlap_count(a, b)` — عدد tokens المشتركة (multiset-safe).
- `jaccard(a, b)` — Jaccard على token sets.
- `contains_phrase(text, phrase)` — substring match على النص المُطبَّع.

### hashing_vectorizer.py
- `HashingVectorizer(buckets=2048)` — يحوّل النص إلى sparse vector عبر BLAKE2b → bucket mod.
- `cosine_sparse(a, b)` — cosine بين sparse dicts.

**لماذا hashing بدلًا من embeddings جاهزة؟** لأنه deterministic، خفيف، محلي، ولا يحمل معرفة متعلمة من جهة خارجية. سيُستبدل لاحقًا بـ SF custom embedding model مدرّب من الصفر.

### semantic_explorer.py
`SemanticExplorer.score_candidate(text, candidate)` يجرب الإشارات بالترتيب ويرجع أقواها كـ `SignalMatch(candidate, score, signal)`:

1. `phrase` (containment) → 1.0
2. `token` (Jaccard ≥ 0.5) → قيمة Jaccard
3. `fuzzy` (SequenceMatcher ≥ 0.85) → النسبة
4. `hashing` (cosine > 0) → القيمة

`best_match(text, candidates)` يختار أعلى Score من القائمة.

---

## مبدأ التصميم

الطبقة مصممة لتكون **قابلة للاستبدال**:

- Phase 2: الطريقة الحالية كافية لتمييز عبارات وكلمات معروفة.
- Phase 6+: سيدخل SF Native Encoder (PyTorch، random init، مدرَّب على corpus SF.AI فقط).
- Phase 8: RAG يستخدم نفس الـ interface (lexical / hashing الآن، neural لاحقًا).

---

## مثال

```python
from sf_ai.core.semantic import SemanticExplorer

explorer = SemanticExplorer()
match = explorer.score_candidate("مرحبا كيف حالك", "كيف حالك")
# SignalMatch(candidate='كيف حالك', score=1.0, signal='phrase')

match = explorer.score_candidate("مرحبا كيف الحال", "كيف حالك")
# SignalMatch(candidate='كيف حالك', score=0.86, signal='fuzzy')
```

---

## المحظورات

- ❌ لا تنزّل sentence-transformers.
- ❌ لا تستورد أي pretrained encoder.
- ❌ لا تستخدم OpenAI/Cohere embeddings APIs.
- ❌ لا تستخدم HuggingFace pretrained models.

إن احتجنا embeddings أعلى جودة، السبيل الوحيد المسموح: **تدريب encoder خاص بـ SF.AI من الصفر** (Phase 6+).
