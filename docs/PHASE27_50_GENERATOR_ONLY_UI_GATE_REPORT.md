# Phase 27.50 — Generator-Only UI Lab Gate

## الخلاصة

تحويل `/chat/message` والواجهة إلى مختبر مولّد فقط:

- لا زر `مولّد تجريبي`.
- لا `generator_trial=false` من الواجهة.
- لا إجابات template في `/chat/message`.
- إذا لم يستطع `sf_10m_phase27_47` الرد، ترجع الاستجابة فارغة مع `generator=generator_blocked`.

## النتيجة

```text
cases = 7/7
runtime_default = generator_only_lab
candidate_generator = sf_10m_phase27_47
template_answers_allowed = false
```

## Smoke حي

```text
وش الاخبار   -> sf_10m_phase27_47 | بخير ولله الحمد، أنت كيفك؟
علومك        -> sf_10m_phase27_47 | بخير ولله الحمد. وش ودك نسولف عنه؟
نظم وقتي    -> sf_10m_phase27_47 | اكتب ثلاث مهام وابدأ بالأهم.
من أنت       -> generator_blocked | empty
ما معنى الكرم -> generator_blocked | empty
```

## القرار

الواجهة الآن تصلح لاختبار المولد فقط. أي رد ظاهر في المحادثة يجب أن يكون من
`sf_10m_phase27_47`. القوالب لم تعد تظهر في `/chat/message`.

## التالي

Phase 27.51 — targeted natural-prompt expansion plan for the generator-only lab.
