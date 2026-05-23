# PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md

## SF.AI — Phase 27 Corpus Expansion Batch 001

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_BATCH_001_READY_FOR_NEXT_EXPANSION`

## الهدف

تنفيذ أول خطوة عملية من خطة Phase 27 بعد أن قررت البوابة أن `SF-50M`
غير جاهز. هذه الخطوة تضيف بيانات حوارية محكومة فقط، ولا تبدأ تدريبًا.

## ما أُضيف

```text
data/corpus/chat/jsonl/dialogue_batch_v3_msa_001.jsonl    25 records
data/corpus/chat/jsonl/dialogue_batch_v3_saudi_001.jsonl  25 records
```

وأضيفت بطاقات الحوكمة:

```text
dialogue_batch_v3_msa_001.CARD.md
dialogue_batch_v3_saudi_001.CARD.md
```

## العدادات بعد الدفعة

```text
training_ready      : 550
msa                 : 275
saudi               : 275
gold                : 52
silver              : 498
remaining_to_5000   : 4450
batches_remaining   : 178
needed_msa          : 2225
needed_saudi        : 2225
```

## الحوكمة

- `source=sf-ai-owner-delegated-agent-authored-phase27-msa-v1`
- `source=sf-ai-owner-delegated-agent-authored-phase27-saudi-v1`
- `license=owner-approved-for-sf-ai-training`
- `quality=silver`
- `training_allowed=true`
- `owner_user_id=created_by_user_id=target_user_id=sami-local`
- `user_scope=single_user`

## التحقق

```text
validate_dataset msa_001    : 25/25 valid
validate_dataset saudi_001  : 25/25 valid
corpus-audit                : 550 ready, issues=0
phase27-dialogue-eval       : 19/19 baseline, generator=template
phase26-readiness           : still NOT_READY for SF-50M
```

## القرار

لا يبدأ تدريب. نستمر في توسعة corpus بدفعات صغيرة محكومة حتى نقترب من
`5000` سجل، ثم نعيد Phase 26 readiness قبل أي `SF-50M`.
