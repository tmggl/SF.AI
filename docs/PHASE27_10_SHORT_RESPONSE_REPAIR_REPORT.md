# Phase 27.10 — Short Response Repair Report

## القرار

```text
COMPLETED_NUMERIC_IMPROVEMENT_GENERATION_STILL_BLOCKED
```

تمت محاولة إصلاح fragments عبر دفعة قصيرة مركزة وتدريب `SF-10M v0.7`.
النتيجة الرقمية تحسنت، لكن التوليد ما زال محجوبًا.

## البيانات

أضيفت دفعة short-response repair:

```text
records = 300
msa     = 150
saudi   = 150
quality = gold
```

أصبح corpus:

```text
total_records  = 5543
training_ready = 5543
msa            = 2749
saudi          = 2794
gold           = 431
silver         = 5112
```

وأصبح split:

```text
train = 4973
eval  = 570
```

## تحليل tokenization

الـ tokenizer يعيد roundtrip صحيحًا للكلمات المشوهة؛ المشكلة ليست فقدان decode
مباشر، بل أن النموذج يتعلم/ينتج fragments غير صالحة مثل:

```text
الطرو
حارين
استعجه
حياذكر
بععجه
الموقت
تزعريف
```

لذلك تم توسيع `GenerationGuard` لحجب fragments الجديدة.

## تدريب `SF-10M v0.7`

```text
model          = sf-10m
train_records  = 4973
eval_records   = 570
steps          = 4000
loss           = 8.4840 → 3.1259
best train log = 2.4569
```

## تقييم held-out eval split

| checkpoint | eval loss | perplexity |
|---|---:|---:|
| step1000 | 6.1050 | 448.09 |
| step2000 | 5.4491 | 232.54 |
| step3000 | 5.3479 | 210.17 |
| step4000 | 4.7512 | 115.72 |

أفضل checkpoint رقميًا: `sf-10m-step4000`.

## Generation Quality Harness

بعد تشديد الحارس على fragments الجديدة:

```text
generator       = sf_10m_v0_7
checkpoint      = sf-10m-step4000
prompts         = 10
passed          = 0
runtime_allowed = false
primary reason  = model_artifact_fragment
```

## القرار العملي

- لا يتم تفعيل `SF-10M v0.7` في الواجهة.
- لا يبدأ `SF-50M`.
- التحسن الرقمي حقيقي، لكنه لا يكفي للحوار.

## التالي

الخطوة التالية يجب أن تكون إصلاحًا معماريًا/تدريبيًا أعمق:

- تجربة objective أو batching يمنع مزج أنماط الردود القصيرة.
- فحص decoding constraints دون إخفاء المشكلة.
- تدريب أصغر جدًا على corpus gold فقط للمقارنة، لا للتفعيل.
