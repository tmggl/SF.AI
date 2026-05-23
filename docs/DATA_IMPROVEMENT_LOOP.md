# DATA_IMPROVEMENT_LOOP.md

## SF.AI — Phase 18 Data Expansion Loop v1

**Journey:** Phase 18 / 30
**Status:** completed as governed data loop
**Language track:** Arabic MSA + Saudi only
**Runtime learning:** disabled

---

## الهدف

بناء دورة تحسين بيانات من اختبار سامي المباشر بدون تعلم تلقائي خفي.

القاعدة:

> المحادثة لا تدخل التدريب إلا إذا امتلكت provenance كاملًا ومرت بفحص
> governance مع `training_allowed=true`.

تحديث Phase 27.10: سامي فوّض الوكيل أن يؤلف ويراجع ويعتمد دفعات corpus
مباشرة. لذلك لم يعد حفظ/تصدير سامي اليدوي شرطًا للتقدم، وأُزيلت أزرار
الحفظ/التصدير من `/ui/chat`. أي مسار review export باقٍ كأداة داخلية
للوكيل فقط.

---

## مسار البيانات

```text
agent-authored governed batch
  → data/corpus/chat/jsonl/dialogue_batch_v2_*.jsonl
  → scripts/validate_dataset.py
  → make corpus-audit
  → training لاحقًا

internal review path
  → agent-only review payload
  → data/corpus/chat/review/*.jsonl
  → scripts/prepare_dialogue_batch.py
  → data/corpus/chat/jsonl/*.jsonl
  → make corpus-audit
```

---

## واجهة الشات

لا تعرض `/ui/chat` زر تصدير أو حفظ للمراجعة. الواجهة مخصصة لاختبار الحوار
والتشخيص فقط، حتى لا يختلط اختبار سامي اليدوي بمسارات corpus.

أي review payload داخلي يجب أن يضع:

```json
"training_allowed": false
"quality": "needs_review"
"license": "user-review-required"
```

هذا مقصود: الملف للتقييم اليدوي، وليس للتدريب.

ملفات `data/corpus/**/review/*.jsonl` مستثناة من git افتراضيًا حتى لا تُرفع
محادثات حقيقية بالخطأ. العينة الوحيدة المسموحة في المستودع هي
`data/corpus/chat/review/sample_review_export.jsonl`.

---

## تحضير batch تدريبي

مثال بعد مراجعة الملف:

```bash
make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/sfai_chat_review.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v1.jsonl --quality silver --dialect saudi --training-allowed"
```

بدون `--training-allowed`:

- لا يكتب training JSONL.
- يكتب تقريرًا فقط في `artifacts/reports/dialogue_batch_report.json`.

---

## فلاتر السلامة

السكربت يتجاوز السجلات الحساسة افتراضيًا:

- medical
- legal
- finance
- religion
- security

يمكن تجاوز هذا فقط بـ `--include-sensitive`، لكن هذا غير مناسب للتدريب العام
إلا بسياسة مستقلة.

---

## المخرجات

- `scripts/prepare_dialogue_batch.py`
- `data/corpus/chat/review/README.md`
- `artifacts/reports/dialogue_batch_report.json`
- `sf_ai/datasets/dialogue_batch.py`

---

## شروط قبول سجل تدريبي

- يحتوي user + assistant.
- `domain=chat`.
- `lang=ar`.
- `dialect ∈ {msa, saudi}`.
- `quality ∈ {gold, silver, bronze}`.
- `training_allowed=true`.
- source/license موجودان.

---

## الاختبار الاختياري من الواجهة

الوكيل يستطيع تشغيل هذه الجمل بنفسه عند الحاجة لفحص الواجهة، وليست شرطًا على سامي:

- `وش رايك اليوم`
- `قل لي جملة قصيرة`
- `سولف معي`
- `وش تقدر تسوي`

أي ملف ناتج يبقى للمراجعة فقط حتى يتم تحضيره بالسكريبت. في Phase 22،
المسار الأساسي هو الدفعات المباشرة ذات `owner-delegated agent-authored`.
