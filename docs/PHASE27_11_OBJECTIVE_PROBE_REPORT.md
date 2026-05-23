# Phase 27.11 — Objective/Decoding Diagnosis Report

## القرار

```text
FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING
```

هذه مرحلة تشخيص، وليست تكبيرًا للنموذج. الهدف كان معرفة هل يستطيع
`SF-10M` حفظ ردود قصيرة جدًا من corpus gold صغير إذا عزلناه عن corpus العام.

## الإعداد

```text
language_track      = msa + saudi
lexicon_track       = Saudi Seed v1
records             = 16
records_per_dialect = 8
source              = Phase 27.10 short-response repair gold batch
checkpoint          = sf-10m-step1000
```

تم التدريب على micro-corpus ذهبي فقط داخل `artifacts/eval/phase27_11_objective_probe/`
حتى لا يدخل هذا كـ corpus عام جديد.

## النتيجة

```text
clean_stop_passed = 0/16
guard:repetition = 6
overgenerates_after_expected = 10
```

النموذج حفظ بدايات بعض الردود، لكنه لم يعرف أين يتوقف. أمثلة:

```text
expected : مرحبًا بك، تفضل.
generated: مرحبًا بك، تفضل. ل. ل. ل. ل. فضل من فضلك. . . . . . .
```

```text
expected : وعليكم السلام، أهلًا بك.
generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار...
```

## التشخيص

المشكلة الحالية ليست فقط نقص بيانات أو حجم نموذج. يوجد خلل واضح في تعليم
حدود رد المساعد:

- لا توجد إشارة نهاية رد صريحة يتعلمها النموذج كهدف.
- decoding لا يملك stop token موثوقًا.
- النموذج قد يحفظ prefix صحيحًا ثم يواصل توليد حشو أو تكرار.

## القرار العملي

- لا يتم تفعيل `SF-10M` في الواجهة.
- لا يبدأ `SF-50M`.
- الانتقال التالي يجب أن يكون إصلاح `assistant reply boundary / EOS`.

## الملفات

- `scripts/phase27_11_objective_probe.py`
- `artifacts/reports/phase27_11_objective_probe_report.json`
- `artifacts/samples/phase27_11_objective_probe_generations.md`

## المرحلة التالية

Phase 27.12 يجب أن تضيف:

- رمز نهاية رد مساعد سيادي داخل تنسيق الحوار.
- loss target يتعلم نهاية الرد، لا المحتوى فقط.
- decoding يتوقف عند هذا الحد.
- probe يعيد الاختبار حتى يصل إلى clean-stop pass قبل أي تكبير.
