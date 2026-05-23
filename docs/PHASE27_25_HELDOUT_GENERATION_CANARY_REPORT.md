# Phase 27.25 — Held-out Generation Quality Canary

## القرار

```text
FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME
```

هذه المرحلة لم تدرّب نموذجًا جديدًا. اختبرت checkpoint Phase 27.24 على أسئلة
قريبة لكنها غير موجودة في micro-probe الأصلي.

## لماذا هذه المرحلة مهمة؟

Phase 27.24 وصل إلى `32/32`، وهذا أثبت أن المسار يستطيع حفظ/إخراج أزواج
prompt → answer قصيرة بدقة. لكن هذا لا يكفي لفتح الواجهة. نحتاج معرفة هل
النموذج يعمم على صياغات جديدة.

## النتيجة

```text
passed       = 8/16
semantic     = 8/16
guard_passed = 15/16
```

## أين نجح؟

نجح في تعريفات قريبة من التدريب:

- التعاون.
- الاحترام.
- القراءة.
- بعض التحية والشكر السعودي.

## أين فشل؟

فشل في التعميم على:

- تحية فصحى بصياغة مختلفة.
- سؤال حال فصيح جديد.
- النصيحة العامة.
- ترتيب اليوم.
- الدعم عند القلق/التوتر.

أمثلة:

```text
prompt    : أحتاج نصيحة بسيطة
generated : التعاون يعني أن ننجز معًا بدل الانفراد.
reason    : missing_semantic_terms
```

```text
prompt    : كيف أرتب يومي
generated : خفف الإضاءة واترك الهاتف قليلًا.
reason    : missing_semantic_terms
```

```text
prompt    : متوتر شوي
generated : تقدر، ابدأ بخطوة ولا توقف.
reason    : missing_semantic_terms
```

## التشخيص

النموذج خرج من مرحلة الكسور اللفظية المباشرة في micro-probe، لكنه ما زال
يميل إلى اختيار جواب محفوظ من عائلة قريبة بدل فهم intent الجديد.

هذا يعني:

- نجاح `32/32` كان ضروريًا ومفيدًا.
- لكنه ليس كافيًا لتفعيل المولد في الواجهة.
- المشكلة الحالية: generalization/objective coverage، لا tokenizer وحده.

## قرار runtime

```text
runtime_allowed = false
limited_runtime_trial_allowed = false
sf50m_allowed = false
```

الواجهة تبقى على router/templates. لا يتم عرض المولد للمستخدم كعقل الشات بعد.

## التالي

```text
Phase 27.26 — Held-out Objective Repair and Generalization Training
```

هدفها:

- تدريب repair صغير على عائلات فشلت في held-out.
- عدم إدخال محادثات تشغيلية.
- الحفاظ على MSA + Saudi فقط.
- إعادة canary 27.25 حتى يتجاوز الأسئلة الجديدة.

## الملفات

- `scripts/phase27_25_heldout_generation_canary.py`
- `artifacts/reports/phase27_25_heldout_generation_canary_report.json`
- `artifacts/samples/phase27_25_heldout_generation_canary_generations.md`
