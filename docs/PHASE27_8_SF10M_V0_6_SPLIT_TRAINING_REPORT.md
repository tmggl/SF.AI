# Phase 27.8 — SF-10M v0.6 Split Training Report

## القرار

```text
COMPLETED_WITH_NUMERIC_IMPROVEMENT_RUNTIME_BLOCKED
```

تم تدريب `SF-10M v0.6` على `train split` فقط، ثم تقييمه على `eval split`
المعزول. النتيجة الرقمية تحسنت، لكن عينات التوليد ما زالت غير صالحة للحوار.

## إعداد التدريب

```text
model          = sf-10m
params         = 7,444,992
tokenizer      = artifacts/tokenizers/sf_bpe/v2
corpus         = data/corpus/chat/jsonl
split_manifest = data/corpus/chat/splits/dialogue_split_v1.json
train_records  = 4703
eval_records   = 540
loss_scope     = assistant
steps          = 4000
batch_size     = 4
seq_len        = 64
device         = mps
seed           = 20260523
```

## نتيجة التدريب

```text
first logged loss = 8.4743
step 400          = 5.9331
step 800          = 4.8538
step 2000         = 3.7962
step 3600         = 2.7407
last loss         = 3.7460
```

## تقييم held-out eval split

| checkpoint | eval loss | perplexity |
|---|---:|---:|
| step1000 | 6.0635 | 429.90 |
| step2000 | 5.5189 | 249.37 |
| step3000 | 5.4055 | 222.63 |
| step4000 | 5.0227 | 151.82 |

أفضل checkpoint رقميًا: `sf-10m-step4000`.

## Canary

تم اختبار 10 prompts اجتماعية/يومية على `sf-10m-step4000`.

```text
allowed_by_canary = 0/10
primary block reason = model_artifact_fragment
```

أمثلة fragments محجوبة:

```text
الطرو
حارين
استعجه
مستمستم
رتنا
تًا
```

## القرار العملي

- لا يتم تفعيل `SF-10M v0.6` في واجهة الشات.
- لا يبدأ `SF-50M` بعد.
- التحسن الرقمي يؤكد أن split/assistant-target يعملان أفضل، لكن جودة النص
  تحتاج معالجة بيانات/هدف تدريب إضافية قبل التكبير.

## التالي

ابدأ مرحلة إصلاح جودة قبل التكبير:

- بناء eval suite للتوليد القصير مع canary آلي.
- زيادة gold social عالي الجودة بدل زيادة silver فقط.
- فحص tokenizer/decoding للفواصل واللواحق المشوهة.
- تجربة تدريب أقصر/انتقائي على gold social لمعرفة هل تتحسن الردود الاجتماعية.
