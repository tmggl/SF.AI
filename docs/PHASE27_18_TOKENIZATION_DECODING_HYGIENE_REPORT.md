# Phase 27.18 — Tokenization/Decoding Hygiene Repair

## القرار

```text
COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS
```

هذه المرحلة لا تكبر النموذج ولا تفعّل المولد. الهدف هو فهم سبب فشل
`5/32` من Phase 27.17: هل المشكلة في عدم فهم السؤال، أم في كسور لفظية
وتجزئة/decoding؟

## ما أضيف

- `resources/tokenization/hygiene_terms_phase27_18.txt`
- `scripts/phase27_18_hygiene_audit.py`
- `make phase27-hygiene-audit`
- توسيع `GenerationGuard` بكسور Phase 27.17 المرصودة.

## نتيجة audit

```text
terms_total             = 26
average_pieces          = 3.5385
roundtrip_failures      = 0
aggressive_split_terms  = 5
uncovered_bad_fragments = 0
runtime_allowed         = false
```

المصطلحات التي تتجزأ بقوة في tokenizer v2:

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
```

## التشخيص

- لا يوجد فشل round-trip؛ tokenizer يستطيع العودة للنص.
- لكن بعض العبارات المهمة تتجزأ إلى 5-8 قطع، وهذا يزيد احتمال كسور decoding.
- كل الكسور المرصودة من Phase 27.17 أصبحت محجوبة في `GenerationGuard`.

أمثلة الكسور المحجوبة:

```text
وعليكأهلًا
التعاعاون
القراد. ءة
هوش تحتاجججبعيادة
```

## القرار العملي

- لا تفعيل للمولد في `/ui/chat`.
- لا تدريب `SF-50M`.
- لا Phase 28.
- المرحلة التالية: Phase 27.19 — Hygiene Repair Corpus/Probe، بحيث نضيف عينات تدريب مركزة على المصطلحات الخمسة ثم نعيد micro-probe.

## الملفات

- `resources/tokenization/hygiene_terms_phase27_18.txt`
- `scripts/phase27_18_hygiene_audit.py`
- `artifacts/reports/phase27_18_tokenization_hygiene_report.json`
- `tests/test_phase27_18_hygiene_audit.py`
