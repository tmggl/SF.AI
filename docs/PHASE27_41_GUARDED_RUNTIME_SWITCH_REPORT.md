# Phase 27.41 — Guarded Runtime Switch

## الهدف

فتح مرشح Phase 27.40 (`sf_10m_phase27_40`) داخل مسار الواجهة/API الاختياري فقط:

- `POST /chat/message` مع `generator_trial=true`
- زر `مولّد تجريبي` في `/ui/chat`

هذا ليس runtime افتراضيًا. القالب/router يبقيان المسار الافتراضي، والـ guard/fallback يمنعان المسارات غير المثبتة.

## المرشح المفتوح

- tokenizer: `artifacts/tokenizers/sf_bpe/v5_topic_terms`
- checkpoint: `artifacts/eval/phase27_40_tokenizer_context_repair/checkpoints/sf-10m-step6400`
- generator metadata: `sf_10m_phase27_40`
- اللغة: `msa + saudi`
- القاموس: `Saudi Seed v1`

## نتيجة البوابة الحية

الأمر:

```bash
make phase27-guarded-runtime-switch
```

النتيجة:

```text
PASSED_GUARDED_RUNTIME_SWITCH_PHASE27_40
22/22 passed
```

- generated lanes: `17/17`
- template/safety controls: `5/5`
- `SF-50M`: غير مسموح بعد
- training جديد: لم يحدث في هذه المرحلة

## أمثلة يمكن اختبارها من الواجهة

فعّل زر `مولّد تجريبي` ثم اكتب:

- `كيفك اليوم`
- `ما معنى الصداقة`
- `وش معنى التنظيم`
- `ما معنى الهدوء`
- `الصدق وش يعني`
- `وجهني بخطوة بسيطة`
- `رتب لي يومي بسرعة`
- `توترت شوي وش اسوي`

إذا ظهر في التشخيص:

```text
مولّد SF-10M Phase 27.40
```

فالرد جاء من المولد المحلي السيادي. إذا ظهر:

```text
قالب ثابت - ليس مولدًا
```

فهذا fallback مقصود بسبب guard أو لأن السؤال خارج المسارات المثبتة.

## القرار

Phase 27.41 مكتملة.

الخطوة التالية: Phase 27.42 — مراقبة أوسع من الواجهة وإضافة probes أكثر قبل التفكير في أي توسيع حجم.
