# PHASE27_CORPUS_EXPANSION_BATCH_006_REPORT.md

## SF.AI — Phase 27 Natural Corpus Expansion Batch 006

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_NATURAL_BATCH_006_CORPUS_GATE_PASSED`

## الهدف

إكمال حد corpus العملي `5000` بسجلّات طبيعية فقط، دون إدخال أي حوار
تشغيلي أو هندسي أو خاص بإدارة المشروع.

## ما أُضيف

- `data/corpus/chat/jsonl/dialogue_batch_v6_msa_006.jsonl`
  - `750` سجل فصيح طبيعي.
- `data/corpus/chat/jsonl/dialogue_batch_v6_saudi_006.jsonl`
  - `750` سجل سعودي طبيعي.
- بطاقتا provenance:
  - `dialogue_batch_v6_msa_006.CARD.md`
  - `dialogue_batch_v6_saudi_006.CARD.md`

## الأرقام بعد الدفعة

```text
training_ready      : 5143
msa                 : 2549
saudi               : 2594
target              : 5000
remaining_to_5000   : 0
corpus_gate         : passed
```

## التحقق

```text
filter_training_forbidden : 5143 before, 5143 after, removed=0
corpus-audit              : 5143 ready, issues=0
tokenization-audit        : 30/30 protected terms covered
phase26-readiness         : corpus_readiness=true, still NOT_READY on quality gates
phase27-dialogue-eval     : 19/19, remaining=0, batches=0
```

## القرار

Batch 006 أكملت corpus gate. لا نبدأ `SF-50M` بعد؛ المانع لم يعد حجم
البيانات، بل جودة `SF-10M` وcanary/hallucination/repetition checks.
