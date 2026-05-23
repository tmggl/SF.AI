# PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md

## SF.AI — Phase 27 Corpus Expansion Batch 003

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `SUPERSEDED_BY_OPERATIONAL_FILTER`

## الهدف

تأكيد أن حجم `500` سجل لكل دفعة قابل للاستمرار بدون كسر الحوكمة أو
التوازن اللغوي. Batch 003 تضيف محتوى يوميًا عامًا أكثر، لا يقتصر على
حديث المشروع، حتى يتعلم النموذج لاحقًا حوارًا طبيعيًا أوسع.

## ما أُضيف

- `data/corpus/chat/jsonl/dialogue_batch_v3_msa_003.jsonl`
  - `250` سجل فصيح.
- `data/corpus/chat/jsonl/dialogue_batch_v3_saudi_003.jsonl`
  - `250` سجل سعودي.
- بطاقتا provenance:
  - `dialogue_batch_v3_msa_003.CARD.md`
  - `dialogue_batch_v3_saudi_003.CARD.md`

## المحتوى اللغوي

- رسائل اجتماعية قصيرة.
- طلب توضيح بدون اعتراض.
- ترتيب قرارات يومية.
- الاعتذار والرد المهذب.
- أمثلة ومعاني حسب السياق.
- مقارنة الخيارات.
- تصحيح الأسلوب أو المعنى.
- أسئلة متابعة مرتبطة بالسياق.
- رفض آمن مع بديل مفيد.
- مفردات سعودية عامة مثل: `وش`, `ليه`, `بس`, `عادي`, `الزبدة`,
  `هلا`, `خلنا`, `أبي`, `جاوب عربي`.

## الأرقام بعد الدفعة قبل التنظيف

```text
training_ready      : 1550
msa                 : 775
saudi               : 775
target              : 5000
remaining_to_5000   : 3450
batch_size_current  : 500
batches_remaining   : 7
needed_msa          : 1725
needed_saudi        : 1725
```

## الحالة الحالية بعد سياسة منع الحوارات التشغيلية

بعد هذه الدفعة صدر قرار حاكم يمنع أي حوار تشغيلي/هندسي/خاص بإدارة
المشروع من الدخول في corpus التدريب. لذلك حُذف هذا النمط نهائيًا من
الدُفعات السابقة بدل اعتباره review-only.

```text
training_ready_after_cleaning : 643
msa_after_cleaning            : 299
saudi_after_cleaning          : 344
removed_operational_records   : 907
remaining_to_5000             : 4357
batches_remaining_at_500      : 9
```

التقرير الحاكم: [CORPUS_OPERATIONAL_FILTER_REPORT.md](./CORPUS_OPERATIONAL_FILTER_REPORT.md).

## التحقق

```text
validate msa_003             : 250/250 valid, issues=0
validate saudi_003           : 250/250 valid, issues=0
corpus-audit                 : 1550 ready, issues=0
tokenization-audit           : 30/30 protected terms covered
phase26-readiness            : still NOT_READY, corpus below 5000
phase27-dialogue-eval        : 19/19, remaining=3450, batches=7
```

## القرار المحدّث

Batch 003 كانت ناجحة تقنيًا قبل السياسة الجديدة، لكنها لم تعد مرجعًا
أسلوبيًا للدُفعات القادمة. لا نبدأ `SF-50M` بعد؛ الخطوة التالية هي
Batch 004 بحوار بشري طبيعي فقط: سوالف يومية، فصحى طبيعية، وسعودي طبيعي
بلا أوامر تشغيلية ولا مصطلحات هندسية.
