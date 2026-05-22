# PHASE14_SF10M_V0_1_REPORT.md

## SF.AI — Phase 14 SF-10M v0.1 Training Run

**الحالة:** اكتملت مع قيود. هذا ليس نموذج استخدام، بل أول تشغيل مسمى لـ SF-10M v0.1.

## الأمر المستخدم

```bash
make train-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v1 --corpus data/corpus/chat/jsonl --size sf-10m --seq-len 16 --batch-size 2 --steps 80 --warmup 4 --save-every 20 --checkpoints artifacts/checkpoints/sf_10m_v0_1 --seed 20260522"
```

## النتيجة

```text
device          : mps
model           : sf-10m
parameters      : 6,361,600
requested steps : 80
completed steps : 33
first loss      : 5.6638
last loss       : 4.7535
checkpoint      : artifacts/checkpoints/sf_10m_v0_1/sf-10m-step33
```

سبب عدم الوصول إلى 80 خطوة: corpus الحالي صغير جدًا، وانتهت batches عند 33 خطوة.

## التقييم

```text
batches     : 5
loss        : 4.0777
perplexity  : 59.01
generation  : non-empty, UTF-8 valid
```

عينة التوليد:

```text
artifacts/samples/sf_10m_generations.md
```

التقرير الآلي:

```text
artifacts/reports/sf_10m_training_report.json
```

## Metadata

Checkpoint metadata المحلي يحتوي:

- `sf_origin=true`
- tokenizer path داخل `notes`
- corpus path داخل `notes`
- `training_data_hash`
- `config_hash`
- training steps

ملفات `state.pt` غير مرفوعة إلى git لأنها checkpoints تدريبية كبيرة ومقصودة البقاء محلية.

## القيود

- corpus صغير جدًا: 30 سجلًا.
- corpus سعودي فقط ويفتقد `msa`.
- التوليد متكرر.
- غير صالح للشات.
- لا يتم تفعيل ChatModule به.

## القرار

```text
Phase 14 SF-10M v0.1: COMPLETED_WITH_LIMITS
Suitable for runtime chat: NO
Recommended next: MSA corpus expansion before a quality run, or Phase 15 adapter skeleton without activation
```
