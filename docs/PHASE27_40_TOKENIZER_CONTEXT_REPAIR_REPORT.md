# Phase 27.40 — Tokenizer/Context Repair

## الهدف

إصلاح السبب الذي بقي بعد Phase 27.39: المصطلحات الجديدة كانت تتكسر لفظيًا
أثناء التوليد، خصوصًا:

- `الصداقة`
- `الصدق`
- `التنظيم`
- `الهدوء`

المرحلة لا تكبّر النموذج ولا تفتح runtime تلقائيًا. هي مرحلة إصلاح tokenizer
وسياق تدريب داخل `SF-10M`.

## ما حدث

أُنشئ tokenizer سيادي جديد:

```text
tokenizer: artifacts/tokenizers/sf_bpe/v5_topic_terms
vocab    : 4751
merges   : 4684
```

ثم دُرّب probe جديد:

```text
checkpoint: sf-10m-step6400
candidate_generator: sf_10m_phase27_40
training_scope: SF-10M tokenizer/context repair only
```

## protected terms

كل المصطلحات المحمية صارت قطعة واحدة مع roundtrip صحيح:

```text
max_pieces = 1
all_single_piece = true
all_roundtrip_ok = true
```

المصطلحات الحالية:

- `وعليكم السلام`
- `نفسًا هادئًا`
- `نشتغل سوا`
- `القراءة تفيد`
- `تقدّر الناس`
- `التعاون`
- `الاحترام`
- `الصبر`
- `القراءة`
- `الصداقة`
- `الصدق`
- `التنظيم`
- `الهدوء`
- `القراية`

## النتيجة

```text
status     : PASSED_TOKENIZER_CONTEXT_REPAIR_READY_FOR_GUARDED_RUNTIME_CANDIDATE
cases      : 24/24
regression : 8/8
new_topic  : 8/8
heldout    : 4/4
isolation  : 4/4
```

## القرار

هذه أول نتيجة كاملة للموضوعات المحجوبة بعد 27.38 و27.39.

لكن لا نبدّل واجهة المحادثة تلقائيًا في هذه المرحلة. القرار الصحيح:

```text
runtime_switch_allowed = true
next_phase = Phase 27.41 — guarded runtime switch design
```

أي أن المرشح جاهز لتصميم فتح محروس، وليس للتفعيل العشوائي.

## المرحلة التالية

```text
Phase 27.41 — guarded runtime switch design for phase27_40 candidate
```

الهدف القادم:

- ربط `sf_10m_phase27_40` داخل runtime خلف guard.
- فتح موضوعات التعريف الجديدة فقط في proven lanes.
- إبقاء fallback للقوالب في raw general/safety/identity.
- اختبار حي عبر `/chat/message` و`/ui/chat` قبل أي اعتماد.

## artifacts

- `artifacts/tokenizers/sf_bpe/v5_topic_terms/`
- `artifacts/reports/phase27_40_tokenizer_context_repair_report.json`
- `artifacts/samples/phase27_40_tokenizer_context_repair.md`
