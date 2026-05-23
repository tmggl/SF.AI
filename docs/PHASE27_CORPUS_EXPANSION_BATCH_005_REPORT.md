# PHASE27_CORPUS_EXPANSION_BATCH_005_REPORT.md

## SF.AI — Phase 27 Natural Corpus Expansion Batch 005

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_NATURAL_BATCH_005_1500`

## الهدف

الاستمرار في رفع corpus الطبيعي بسرعة محكومة بعد نجاح Batch 004، مع
إبقاء كل الرسائل التدريبية في نطاق الحديث البشري اليومي فقط.

## ما أُضيف

- `data/corpus/chat/jsonl/dialogue_batch_v5_msa_005.jsonl`
  - `750` سجل فصيح طبيعي.
- `data/corpus/chat/jsonl/dialogue_batch_v5_saudi_005.jsonl`
  - `750` سجل سعودي طبيعي.
- بطاقتا provenance:
  - `dialogue_batch_v5_msa_005.CARD.md`
  - `dialogue_batch_v5_saudi_005.CARD.md`

## الأرقام بعد الدفعة

```text
training_ready      : 3643
msa                 : 1799
saudi               : 1844
target              : 5000
remaining_to_5000   : 1357
batch_size_current  : 1500
batches_remaining   : 1
needed_msa          : 701
needed_saudi        : 656
```

## التحقق

```text
filter_training_forbidden : 3643 before, 3643 after, removed=0
corpus-audit              : 3643 ready, issues=0
tokenization-audit        : 30/30 protected terms covered
phase26-readiness         : still NOT_READY, corpus below 5000
phase27-dialogue-eval     : 19/19, remaining=1357, batches=1
```

## القرار

Batch 005 ناجحة. المتبقي للوصول إلى حد `5000` صار `1357` سجلًا، أي دفعة
طبيعية كبيرة واحدة تقريبًا قبل إعادة تقييم بوابة Phase 26.
