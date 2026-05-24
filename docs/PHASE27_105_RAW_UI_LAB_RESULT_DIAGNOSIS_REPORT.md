# Phase 27.105 — Raw UI Lab Result Diagnosis

## الخلاصة

اختبار الواجهة الحي أكد أن الردود الظاهرة تأتي من:

```text
مولّد SF-10M Phase 27.81
```

وليست من `chat_patterns.py`. السرعة طبيعية لأن النموذج صغير (`SF-10M`) ومحمل محليًا في الذاكرة. السرعة لا تعني قالبًا.

لكن الجودة ما زالت غير كافية لإطلاق رسمي.

## ما ثبت من اختبار الواجهة

- `نظم وقتي` ينجح كمسار تنظيم بسيط.
- `أنا متوتر` و`كيف أهدأ؟` ينجحان كدعم قصير.
- `عرف الصداقة بجملة قصيرة` و`وش يعني الوفاء؟` ينجحان حين يكون الطلب واضحًا كتعريف.
- `السلام عليكم` يفشل كتحية مباشرة ويذهب إلى سالفة عامة.
- `الاخوه` غير مغطاة كموضوع وتنهار إلى `chat.general`.
- `الصداقه` كانت تفشل بسبب شكل إملائي، ثم صُلحت بتمريرها للمولد كـ `الصداقة` مع `intent=definition`.

## الإصلاح غير التدريبي الذي طُبق

- لا قوالب.
- لا تدريب جديد.
- لا tokenizer جديد.
- لا checkpoint جديد.

التغيير فقط في conditioning قبل المولد:

- الموضوع المعروف المكتوب وحده مثل `الصداقه` يتحول إلى:
  - `intent=definition`
  - `topic=الصداقة`
  - prompt normalized: `الصداقة`
- `نظم وقتي` يبقى `planning` ولا يلتقطه مسار الموضوع.
- `كيف الحال` يدخل كـ `smalltalk`.

## Root Cause

الأوزان التقريبية:

| السبب | الوزن |
|---|---:|
| social subfamily objective missing | 28 |
| topic variant + orthography conditioning gap | 22 |
| family mixing / weak generalization | 18 |
| identity/capability/greeting training gap | 12 |
| decoding not main issue | 8 |
| tokenizer orthography fragility | 7 |
| model capacity | 5 |

القرار: المشكلة ليست capacity أولًا. لا يوجد مبرر لـ SF-50M الآن.

## القرار

```text
PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_DECISION
```

- raw lab يبقى مفتوحًا لك وحدك للاختبار.
- official runtime release: ممنوع.
- SF-50M: ممنوع.
- تدريب جديد: ممنوع قبل التصميم التالي.
- قوالب تخفي ضعف المولد: ممنوعة.

## التالي

```text
Phase 27.106 — Social Subfamily + Topic Variant Objective Design
```

هدفها:

- تقسيم `سوالف` إلى: تحية، سؤال حال، فتح سالفة، شكر، هوية، قدرات.
- إضافة topic variants: `الصداقة/الصداقه`, `الأخوة/الاخوه`, وما يشبهها.
- بناء canary من نفس أسلوب اختبار سامي في الواجهة.
- السماح بتدريب محدود فقط إذا نجحت البوابات.
