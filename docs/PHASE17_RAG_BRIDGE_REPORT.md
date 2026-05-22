# PHASE17_RAG_BRIDGE_REPORT.md

## SF.AI — Phase 17 Local Memory/RAG Bridge into Chat

**Date:** 2026-05-22  
**Journey:** Phase 17 / 20  
**Status:** COMPLETED_LOCAL_BRIDGE  
**Runtime generator:** `template`  
**Language/lexicon track:** `msa + saudi` only

---

## الهدف

إدخال الذاكرة والاسترجاع المحلي في الشات بدون حشر المعرفة داخل الأوزان، وبدون
أي زحف ويب تلقائي، وبدون embeddings جاهزة.

Phase 17 لا تفعّل معرفة عامة مفتوحة، بل تفتح بابًا نظيفًا:

```text
Local Document → HybridRetriever → ChatRagBridge → ChatModule
```

إذا وُجد سياق محلي مناسب، يرد الشات بصيغة واضحة:

```text
من الذاكرة المحلية:
...
المصدر: ...
```

---

## ما أُضيف

- `sf_ai/modules/chat/context_builder.py`
  - يحوّل `RetrievalResult` إلى مقتطفات عربية قصيرة.
  - يضيف مصدرًا واضحًا لكل رد.

- `sf_ai/modules/chat/rag_bridge.py`
  - يربط `HybridRetriever` مع `ChatModule`.
  - يتخطى النوايا الثابتة مثل الهوية والقدرات والتحية.
  - لا يستخدم web crawling.
  - لا يستخدم pretrained embeddings.

- `ChatModule`
  - يقبل `rag_bridge` اختياريًا.
  - إذا وُجد سياق محلي، يستبدل الرد العام برد “من الذاكرة المحلية”.
  - يضيف metadata:
    - `rag:used`
    - `rag_sources:...`
    - أو `rag:not_configured`

- API/UI
  - `POST /chat/message` يعيد حقل `rag`.
  - شاشة `/ui/chat` تعرض `rag=used/not_used`.

---

## الحالة التشغيلية

افتراضيًا:

- السيرفر لا يحمّل أي ذاكرة محلية تلقائيًا.
- `rag=not_used`.
- لا web crawling.

عند حقن `ChatRagBridge` في الاختبارات أو تشغيل خاص:

- يمكن للشات استخدام `HybridRetriever`.
- الرد يوضح أنه من الذاكرة المحلية، لا من توليد النموذج.

---

## القاموس المتبع

المسار اللغوي لم يتغير:

- العربية الفصحى `msa`.
- اللهجة السعودية `saudi`.
- `Saudi Seed v1` مرجع خاص.
- `resources/tokenization/` لحماية الكلمات السعودية.
- لا تفعيل للهجات أخرى.

---

## نتيجة الاختبارات

```text
tests/test_chat_rag_bridge.py — 6 passed
```

الاختبار الكامل لاحقًا يجب أن يبقى شرط الرفع.

---

## القرار

Phase 17 مكتملة كبنية bridge محلية.

لا يزال الاستخدام اليومي يعتمد على templates + router + composer + optional
local RAG، بينما يستطيع مختبر سامي المحلي تشغيل المولد السيادي الخام للتجربة.

المرحلة التالية:

```text
Phase 18 — Data Expansion Loop v1
```
