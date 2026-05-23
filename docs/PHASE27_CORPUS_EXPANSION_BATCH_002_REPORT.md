# PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md

## SF.AI — Phase 27 Corpus Expansion Batch 002

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_LARGE_BATCH_002_READY_FOR_NEXT_EXPANSION`

## الهدف

رفع سرعة توسعة corpus من دفعات صغيرة إلى دفعات كبيرة محكومة. بعد نجاح
Batch 001، اعتمدنا Batch 002 بحجم `500` سجل: `250` عربي فصيح و`250`
سعودي، مع إبقاء كل سجل داخل الحوكمة نفسها.

## قرار حجم الدفعة

- الحجم السابق: `50` سجلًا لكل batch (`25` فصيح + `25` سعودي).
- الحجم المعتمد الآن: `500` سجل لكل batch (`250` فصيح + `250` سعودي).
- الحد الأعلى الحالي: `500` سجل لكل batch.
- لا نرفع إلى `2000` سجل في batch واحد إلا بعد نجاح دفعتين كبيرتين `500`
  بدون مشاكل audit أو تكرار واضح.

## ما أُضيف

- `data/corpus/chat/jsonl/dialogue_batch_v3_msa_002.jsonl`
  - `250` سجل فصيح.
- `data/corpus/chat/jsonl/dialogue_batch_v3_saudi_002.jsonl`
  - `250` سجل سعودي.
- بطاقتا provenance:
  - `dialogue_batch_v3_msa_002.CARD.md`
  - `dialogue_batch_v3_saudi_002.CARD.md`

## المحتوى اللغوي

الدفعة تغطي كلامًا عامًا شائعًا لا يقتصر على أسلوب سامي وحده:

- محادثة يومية.
- طلب اختصار وشرح.
- تصحيح سوء الفهم.
- أسئلة عن معنى المصطلحات.
- ترتيب يوم أو قرار.
- متابعة سياقية.
- حدود التدريب والتشغيل.
- سلامة عامة للطب/القانون/المال.
- مفردات سعودية شائعة مثل: `وش`, `وشلون`, `ليه`, `طيب`, `الحين`,
  `أبشر`, `ترى`, `عادي`, `زبدة`.

## الأرقام بعد الدفعة

```text
training_ready      : 1050
msa                 : 525
saudi               : 525
target              : 5000
remaining_to_5000   : 3950
batch_size_current  : 500
batches_remaining   : 8
needed_msa          : 1975
needed_saudi        : 1975
```

## التحقق

```text
validate msa_002             : 250/250 valid, issues=0
validate saudi_002           : 250/250 valid, issues=0
corpus-audit                 : 1050 ready, issues=0
tokenization-audit           : 30/30 protected terms covered
phase26-readiness            : still NOT_READY, corpus below 5000
phase27-dialogue-eval        : 19/19, remaining=3950, batches=8
```

## القرار

Batch 002 ناجحة ومناسبة للاستمرار. لا نبدأ تدريب `SF-50M` بعد؛ القرار
الصحيح هو تنفيذ Batch 003 بحجم `500` سجل آخر، ثم إعادة audits والاختبارات.
