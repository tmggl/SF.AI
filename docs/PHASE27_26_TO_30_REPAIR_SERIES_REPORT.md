# Phase 27.26–27.30 — Repair Series Report

## القرار النهائي الحالي

```text
FAILED_FRESH_MIXED_SHADOW_BLOCK_RUNTIME
```

المولد تحسن بوضوح، لكنه لم يصل بعد إلى مستوى تشغيله في الواجهة.

## التسلسل

| المرحلة | الهدف | النتيجة | القرار |
|---------|-------|---------|--------|
| Phase 27.26 | إصلاح عائلات held-out دون نسخ prompts الاختبار | held-out `9/16`, micro `32/32` | runtime محظور |
| Phase 27.27 | إصلاح أوسع مع shadow canary جديد | held-out `16/16`, shadow `9/16`, micro `32/32` | runtime محظور |
| Phase 27.28 | intent conditioning: `النظام: النية` | held-out `16/16`, shadow `12/16`, micro `32/32` | runtime محظور |
| Phase 27.29 | topic conditioning للتعريفات: `النظام: المصطلح` | old/shadow/definition مرت، لكن وُجد shadow leakage | runtime محظور |
| Phase 27.30 | fresh mixed shadow canary بلا تدريب | `16/18` | runtime محظور |

## ماذا تعلمنا؟

- `intent` conditioning مفيد: shadow تحسن من `9/16` إلى `12/16`.
- `topic` conditioning مفيد للتعريفات، لكنه يحتاج اختبارًا غير مسرب دائمًا.
- checkpoint Phase 27.29 قوي على تعريفات التعاون/الاحترام/القراءة، لكن fresh mixed shadow كشف بقاء فشلين:
  - `شكرًا لمساعدتك` خرجت مشوهة: `أساعدمل`.
  - `كيفك اليوم` خرجت ناقصة: `بخير ول`.

## القرار

- لا تفعيل runtime.
- لا `SF-50M`.
- لا تجربة واجهة مولدة الآن.
- الواجهة تبقى `template`.

## التالي

```text
Phase 27.31 — Broader Natural Intent/Topic Dataset
```

الهدف: بناء دفعة طبيعية أوسع للفصحى والسعودي تغطي:

- الشكر بصيغ أكثر.
- سؤال الحال بصيغ سعودية أكثر.
- تعريفات مع topic conditioning.
- تحية/نصيحة/تخطيط/دعم بدون حفظ ضيق.

ثم تدريب جديد وfresh mixed shadow جديد قبل أي runtime.

## الملفات

- `scripts/phase27_26_heldout_objective_repair.py`
- `scripts/phase27_27_broader_heldout_repair.py`
- `scripts/phase27_28_intent_conditioned_repair.py`
- `scripts/phase27_29_topic_conditioned_definition_repair.py`
- `scripts/phase27_30_fresh_mixed_shadow_canary.py`
- `artifacts/reports/phase27_26_heldout_objective_repair_report.json`
- `artifacts/reports/phase27_27_broader_heldout_repair_report.json`
- `artifacts/reports/phase27_28_intent_conditioned_repair_report.json`
- `artifacts/reports/phase27_29_topic_conditioned_definition_repair_report.json`
- `artifacts/reports/phase27_30_fresh_mixed_shadow_canary_report.json`
