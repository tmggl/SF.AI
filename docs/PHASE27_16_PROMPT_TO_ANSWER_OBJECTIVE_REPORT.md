# Phase 27.16 — Prompt-to-Answer Objective Repair

## القرار

`COMPLETED_OBJECTIVE_REPAIR_RUNTIME_BLOCKED`

هذه المرحلة أصلحت جزءًا هندسيًا مهمًا في objective، لكنها لم تنتج بعد مولدًا صالحًا للواجهة.

## ما الذي تغير؟

- أضيف `--packing-mode` إلى التدريب والتقييم:
  - `packed`: الوضع القديم، يعبئ النصوص بكفاءة.
  - `sample_isolated`: الوضع الجديد، يمنع أن تعبر نافذة التدريب من حوار إلى حوار آخر.
- درّبنا `SF-10M v0.11` على:
  - `stream_format=dialogue`
  - `loss_scope=assistant`
  - `packing_mode=sample_isolated`
  - split ثابت: `train=5343`, `eval=600`

## نتائج التدريب

```text
model      = SF-10M v0.11
steps      = 6000
device     = mps
last_loss  = 3.1785
```

## نتائج eval

| checkpoint | loss | perplexity |
|------------|------|------------|
| step1000 | 5.4265 | 227.35 |
| step2000 | 5.1707 | 176.03 |
| step3000 | 4.9630 | 143.02 |
| step4000 | 4.6046 | 99.95 |
| step5000 | 4.4191 | 83.02 |
| step6000 | 4.0573 | 57.82 |

المقارنة المهمة:

- `v0.10` كان أفضل رقميًا: loss `3.0452`, ppl `21.01`.
- `v0.11` أكثر نظافة من ناحية sample isolation، لكنه أسوأ رقميًا.

## نتائج canary

```text
step2000: 2/10, runtime_allowed=false
step6000: 0/10, runtime_allowed=false
```

حتى نجاح `2/10` في step2000 ليس مقنعًا للواجهة؛ بعض المعاينات بقيت مثل:

```text
الزبدة: اطلب ...
```

وهذا يعني أن النموذج ما زال يتعلم أنماطًا سطحية بدل ربط السؤال بجواب مناسب.

## القرار العملي

- لا تفعيل للمولد في `/ui/chat`.
- لا تدريب `SF-50M`.
- لا توسعة حجم النموذج.
- الخطوة التالية: Phase 27.17 — micro-probe دقيق لأزواج سؤال/جواب قصيرة، مع شرط exact/semantic match قبل أي تدريب واسع.

## الملفات

- `sf_ai/training/train_tiny_lm.py`
- `sf_ai/training/evaluate_tiny_lm.py`
- `tests/test_train_tiny_lm_objective.py`
- `artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json`
- `eval/reports/generation_quality_v1_v0_11_step2000.json`
- `eval/reports/generation_quality_v1_v0_11_step6000.json`
