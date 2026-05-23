# Phase 27.22 — Spacing/Boundary Loss Repair

## القرار

```text
PARTIAL_SPACING_BOUNDARY_REPAIR_BLOCK_RUNTIME
```

هذه المرحلة لم تدرّب نموذجًا جديدًا. أصلحت decoding/guard ثم أعادت تقييم
checkpoint Phase 27.21 نفسه لمعرفة أثر إصلاح boundary.

## ما أُصلح

1. `BPETokenizer.decode` صار يضيف حد كلمة بعد protected phrase token.
   هذا يمنع التصاق:

```text
هادئًاوابدأ
سواونخفف
تفيدوتوسع
```

2. `GenerationGuard` لم يعد يحجب نهاية فصحى صحيحة مثل `وقتًا` بسبب fragment
قديم عام جدًا (`تًا`).

## النتيجة

قبل الإصلاح في Phase 27.21:

```text
passed       = 25/32
exact_clean  = 26/32
semantic     = 30/32
guard_passed = 31/32
```

بعد الإصلاح:

```text
passed       = 29/32
exact_clean  = 29/32
semantic     = 30/32
guard_passed = 32/32
glued_left   = 0
```

التحسن:

```text
passed_delta       = +4
exact_clean_delta  = +3
guard_delta        = +1
```

## ما بقي يفشل

```text
prompt    : اشرح لي التعاون
expected  : التعاون يعني أن ننجز معًا بدل الانفراد.
generated : التعانشتغل سوا ونخفف الحمل.
reason    : missing_semantic_terms
```

```text
prompt    : ما معنى الاحترام
expected  : الاحترام تقدير الناس بالكلام والفعل.
generated : الاحتردم تقدير الناس بالكلام والفعل.
reason    : not_exact_clean
```

```text
prompt    : القراءة وش تفيد
expected  : توسع فهمك وتزيد كلماتك.
generated : القراءة تفيد وتوسع فهمك.
reason    : missing_semantic_terms
```

## التشخيص

إصلاح spacing نجح. المشكلة المتبقية صارت semantic/lexical confusion:

- خلط بين فصحى وسعودي في prompt التعاون.
- تحريف كلمة `الاحترام` إلى `الاحتردم`.
- جواب القراءة السعودي يذكر الفهم، لكنه لا يذكر `كلماتك`.

## قرار runtime

```text
runtime_allowed = false
sf50m_allowed   = false
```

لا يفتح المولد في الواجهة حتى ينجح micro-probe كاملًا ثم canary أوسع.

## التالي

```text
Phase 27.23 — Semantic/Lexical Confusion Repair
```

هدفها:

- علاج الخلط الدلالي في `التعاون`.
- علاج تحريف `الاحترام`.
- علاج جواب `القراءة وش تفيد`.
- الوصول إلى `32/32` في micro-probe قبل أي تجربة واجهة.

## الملفات

- `scripts/phase27_22_spacing_boundary_repair.py`
- `artifacts/reports/phase27_22_spacing_boundary_repair_report.json`
- `artifacts/samples/phase27_22_spacing_boundary_repair_generations.md`
