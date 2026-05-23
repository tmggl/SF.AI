# Phase 27.39 — Topic-Isolation Repair

## الهدف

إصلاح فشل Phase 27.38 بطريقة أدق: ليس فقط إضافة أمثلة للموضوعات المحجوبة،
بل فصل موضوعات التعريف عن بعضها حتى لا يخلط النموذج بين:

- `التعاون`
- `الصبر`
- `الاحترام`
- `القراءة`
- `الصداقة`
- `الصدق`
- `التنظيم`
- `الهدوء`

هذه ليست مرحلة تكبير نموذج. لا `SF-50M` ولا Phase 28.

## ما حدث

دُرّب probe جديد داخل `SF-10M` على curriculum متوازن للموضوعات الثمانية:

```text
checkpoint: sf-10m-step6400
candidate_generator: sf_10m_phase27_39
training_scope: targeted SF-10M topic-isolation probe only
```

ثم صُحّح القياس نفسه حتى لا يحجب guard سؤالًا تعريفيًا يحتوي "بالسعودي"،
وحتى لا يعتبر "معاملة" تسربًا من "معًا".

## النتيجة

```text
status     : PARTIAL_TOPIC_ISOLATION_KEEP_CURRENT_RUNTIME
cases      : 10/24
regression : 4/8
new_topic  : 2/8
heldout    : 1/4
isolation  : 3/4
```

## التشخيص

تحسن الانهيار الموضوعي مقارنة بـ Phase 27.38، إذ عاد `التعاون` و`الصبر`
للنجاح في regression. لكن المرشح ما زال غير صالح للواجهة بسبب:

- كسور لفظية داخل كلمات مهمة مثل `الصداقة`, `الصدق`, `التنظيم`.
- فقدان بعض المسارات الاجتماعية بسبب ضغط curriculum التعريفي.
- بقاء تسرب موضوعي محدود، مثل خلط `الهدوء` مع `القراءة`.

لذلك:

```text
runtime_switch_allowed = false
```

## القرار

لا نبدّل مولّد الواجهة. يبقى runtime التجريبي على checkpoint السابق
`sf_10m_phase27_33` مع فتح `الصبر` المحروس من Phase 27.37 فقط.

## المرحلة التالية

```text
Phase 27.40 — tokenizer/context repair for topic isolation
```

التركيز التالي:

- حماية المصطلحات الجديدة التي تتكسر لفظيًا.
- تقليل ضغط تعريفات الموضوعات على المسارات الاجتماعية.
- إعادة probe بعد إصلاح tokenizer/context قبل أي runtime switch.

## artifacts

- `artifacts/reports/phase27_39_topic_isolation_repair_report.json`
- `artifacts/samples/phase27_39_topic_isolation_repair.md`
