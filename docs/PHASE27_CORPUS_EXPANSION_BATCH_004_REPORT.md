# PHASE27_CORPUS_EXPANSION_BATCH_004_REPORT.md

## SF.AI — Phase 27 Natural Corpus Expansion Batch 004

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_NATURAL_BATCH_004_1500`

## الهدف

رفع سرعة توسعة corpus من دفعات `500` إلى دفعة `1500` سجل، مع منع كامل
لأي حوار تشغيلي أو هندسي أو خاص بإدارة المشروع داخل الرسائل التدريبية.

## ما أُضيف

- `data/corpus/chat/jsonl/dialogue_batch_v4_msa_004.jsonl`
  - `750` سجل فصيح طبيعي.
- `data/corpus/chat/jsonl/dialogue_batch_v4_saudi_004.jsonl`
  - `750` سجل سعودي طبيعي.
- بطاقتا provenance بصيغة طبيعية محايدة:
  - `dialogue_batch_v4_msa_004.CARD.md`
  - `dialogue_batch_v4_saudi_004.CARD.md`

## المحتوى اللغوي

- اعتذار وتلطيف خلاف.
- سؤال عن حال شخص.
- تهنئة ومواساة.
- طلب مساعدة أو موعد.
- رفض مهذب.
- ترتيب يومي بسيط.
- شرح يومي قريب.
- عبارات سعودية عامة مثل: `وش`, `ليه`, `بس`, `حياك`, `الله يعافيك`.

## الأرقام بعد الدفعة

```text
training_ready      : 2143
msa                 : 1049
saudi               : 1094
target              : 5000
remaining_to_5000   : 2857
batch_size_current  : 1500
batches_remaining   : 2
needed_msa          : 1451
needed_saudi        : 1406
```

## التحقق

```text
filter_training_forbidden : 2143 before, 2143 after, removed=0
corpus-audit              : 2143 ready, issues=0
tokenization-audit        : 30/30 protected terms covered
phase26-readiness         : still NOT_READY, corpus below 5000
phase27-dialogue-eval     : 19/19, remaining=2857, batches=2
pytest                    : run after this report in the final verification pass
```

## القرار

Batch 004 ناجحة كدفعة طبيعية كبيرة. لا نبدأ `SF-50M` بعد؛ المسار الصحيح
هو الاستمرار بدفعات طبيعية كبيرة حتى الاقتراب من `5000` ثم إعادة بوابة
Phase 26.
