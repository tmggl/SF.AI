# Phase 27.110 — Licensed Ingestion Design

## الخلاصة

صُمم مسار إدخال المصادر المجانية بدون إدخال نصوص تدريب خارجية.

القرار:

```text
PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION
```

## القرارات

- Qabas مسموح كتصميم lexicon/topic/protected-terms فقط.
- Tashkeela محجوب للتدريب حتى حل تعارض الترخيص.
- Masader يبقى metadata/source-discovery فقط.
- OSIAN وSaudiNewsNet مقيدان non-commercial/eval أو vocabulary-only.
- أي مصدر unknown/custom/with-fee محجوب عن free lane.

## الممنوع

- إدخال نص خارجي إلى `data/corpus` الآن.
- استيراد tokenizer vocab أو merges.
- تدريب جديد أو runtime release.

## التالي

```text
Phase 27.111 — Qabas Lexicon Bootstrap Design, no training
```
