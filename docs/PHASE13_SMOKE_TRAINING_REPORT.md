# PHASE13_SMOKE_TRAINING_REPORT.md

## SF.AI — Phase 13 Tiny LM Smoke Training

**الحالة:** اكتملت كاختبار حياة للنموذج، لا كنسخة استخدام.

## الهدف

إثبات أن pipeline التدريب السيادي يعمل end-to-end:

- tokenizer سيادي من Phase 12.
- نموذج random init.
- corpus محلي.
- loss ينخفض.
- checkpoint يحفظ ويُحمّل.
- توليد قصير غير فارغ.

## الأمر المستخدم

```bash
make train-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v1 --corpus data/corpus/chat/jsonl --size sf-10m --seq-len 16 --batch-size 2 --steps 20 --warmup 2 --save-every 10 --checkpoints artifacts/checkpoints/smoke_lm --seed 20260522"
```

## النتيجة

```text
device      : mps
model       : sf-10m
parameters  : 6,361,600
steps       : 20
first loss  : 5.6638
last loss   : 4.7539
checkpoint  : artifacts/checkpoints/smoke_lm/sf-10m-step20
```

## التقييم

```text
batches     : 5
loss        : 4.4346
perplexity  : 84.32
generation  : non-empty, UTF-8 valid
```

عينة التوليد محفوظة في:

```text
artifacts/samples/smoke_generations.md
```

والتقرير الآلي محفوظ في:

```text
artifacts/reports/smoke_training_report.json
```

## القيود

- corpus صغير جدًا: 30 سجلًا.
- corpus الحالي سعودي فقط ويفتقد `msa`.
- التوليد متكرر وغير صالح للمحادثة.
- checkpoint غير مربوط بالـ ChatModule.
- checkpoint state غير مرفوع إلى git لأنه artifact تدريبي كبير.

## القرار

```text
Phase 13 smoke training: PASS
Suitable for runtime chat: NO
Next: Phase 14 or MSA corpus expansion before quality training
```
