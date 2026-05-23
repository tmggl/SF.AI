# Phase 27.24 — Minimal Lexical Stabilization

## القرار

```text
PASSED_MINIMAL_LEXICAL_STABILIZATION_HOLD_RUNTIME_FOR_CANARY
```

هذه المرحلة نجحت في micro-probe الداخلي، لكنها لا تفتح المولد في الواجهة بعد.
السبب: نحتاج canary أوسع خارج الـ 32 سؤالًا قبل أن يصبح المولد عقل runtime.

## الهدف

علاج آخر خللين من Phase 27.23:

- `التعاون`
- `الاحترام`

بدون توسعة corpus عام، وبدون قفز إلى `SF-50M`.

## ما أُنجز

دُرّب tokenizer جديد محدود باسم:

```text
artifacts/tokenizers/sf_bpe/v4_min_lexical
```

الحماية كانت ضيقة جدًا:

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
التعاون
الاحترام
```

ثم دُرّب probe داخلي متوازن على:

- قاعدة 32 prompt/answer مكررة لحماية الأسئلة التي كانت تنجح.
- أمثلة contrastive محدودة للفصحى/السعودي.

## النتيجة

قبل Phase 27.24:

```text
passed       = 30/32
exact_clean  = 30/32
semantic     = 30/32
guard_passed = 31/32
```

بعد Phase 27.24:

```text
passed       = 32/32
exact_clean  = 32/32
semantic     = 32/32
guard_passed = 32/32
```

## ما يعنيه ذلك

هذا أول micro-probe في المسار يصل إلى `32/32`.

لكنه لا يعني أن المولد جاهز للواجهة الواسعة. يعني فقط:

- المسار التدريبي يستطيع تعلم prompt → answer قصير بدقة.
- tokenizer minimal أفضل من حماية عبارات واسعة.
- يمكن الانتقال إلى canary أوسع قبل runtime.

## قرار runtime

```text
runtime_allowed = false
sf50m_allowed   = false
```

لا يتم فتح الواجهة للمولد حتى ينجح Phase 27.25 held-out generation-quality canary.

## التالي

```text
Phase 27.25 — Held-out Generation Quality Canary
```

هدفها اختبار المولد خارج نفس الـ 32 سؤالًا:

- أسئلة قريبة لم يرها التدريب.
- تحيات وسوالف قصيرة.
- فصحى وسعودي فقط.
- فحص تكرار وهلوسة وكسور lexical.

## الملفات

- `scripts/phase27_24_minimal_lexical_stabilization.py`
- `resources/tokenization/protected_phrases_phase27_24.txt`
- `artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json`
- `artifacts/samples/phase27_24_minimal_lexical_stabilization_generations.md`
- `artifacts/tokenizers/sf_bpe/v4_min_lexical/`
