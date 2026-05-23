# Phase 27.7 — Fixed Split + Gold Social Canary Report

## القرار

```text
COMPLETED_QUALITY_GATE_RUNTIME_BLOCKED
```

هذه مرحلة جودة قبل التدريب التالي، وليست تدريب نموذج جديد.

## ما أضيف

- split ثابت للحوار: `data/corpus/chat/splits/dialogue_split_v1.json`.
- CLI: `scripts/build_dialogue_split.py`.
- Make target: `make build-dialogue-split`.
- دعم `--split-manifest` و`--split-name` في التدريب والتقييم.
- دفعة gold social صغيرة: 100 سجل طبيعي (`50` فصيح + `50` سعودي).
- canary أقوى عبر `GenerationGuard.inspect_for_prompt()`.

## corpus

```text
total_records  = 5243
training_ready = 5243
issues         = 0
msa            = 2599
saudi          = 2644
gold           = 131
silver         = 5112
```

## split

```text
method = sha256_bucket
salt   = sf-ai-dialogue-v1
train  = 4703
eval   = 540
```

التوزيع:

```text
train: saudi=2360, msa=2343
eval : saudi=284,  msa=256
```

## runtime

لا يوجد تفعيل مولّد في الواجهة بعد. المرحلة منعت مشكلتين قبل تدريب `v0.6`:

- تقييم غير مفصول عن التدريب.
- ردود مولّدة عربية الشكل لكنها غير متصلة بالسؤال.

## التالي

درّب `SF-10M v0.6` على:

```bash
--split-manifest data/corpus/chat/splits/dialogue_split_v1.json --split-name train
```

ثم قيّمه على:

```bash
--split-manifest data/corpus/chat/splits/dialogue_split_v1.json --split-name eval
```

لا يبدأ `SF-50M` قبل نجاح split/canary/runtime quality.
