# Phase 27.106 — Social Subfamily + Topic Variant Objective Design

## الخلاصة

هذه مرحلة تصميم وتنفيذ أساس renderer فقط. لا تدريب جديد.

القرار:

```text
PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_DECISION
```

النتيجة:

- المشكلة ليست حجم النموذج أولًا.
- المشكلة أن `سوالف` كانت عائلة واسعة جدًا، فخلط المولد بين التحية وفتح
  السالفة والتنظيم.
- المشكلة الثانية أن الموضوعات المكتوبة بصيغ يومية مثل `الصداقه` و`الاخوه`
  لا تدخل دائمًا كموضوع canonical.

## التصميم الجديد

نضيف داخل سياق التدريب، مع masking من loss:

```text
النطاق: سعودي
عائلة الحوار: سوالف
نوع السوالف: تحية
المستخدم: السلام عليكم
المساعد: وعليكم السلام، حيّاك الله. وش أخبارك؟ <eos>
```

السطر الجديد:

```text
نوع السوالف: <تحية|سؤال حال|فتح سالفة|شكر|هوية|قدرات>
```

لا يُحسب عليه loss. هو إشارة سياقية فقط، مثل `عائلة الحوار`.

## Social Subfamilies

| subfamily | label | أمثلة |
|---|---|---|
| `greeting` | تحية | السلام عليكم، هلا، مرحبا |
| `smalltalk` | سؤال حال | كيف الحال، كيفك، علومك |
| `open_chat` | فتح سالفة | خلنا نسولف، افتح لي سالفة |
| `thanks` | شكر | شكرا، يعطيك العافية |
| `identity` | هوية | من أنت، عرفني عليك |
| `capability` | قدرات | وش تقدر تسوي، كيف تساعدني |

## Topic Variants

أمثلة canonical:

- `الصداقه` → `الصداقة`
- `الاخوه` → `الأخوة`
- `الشجاعه` → `الشجاعة`

الهدف أن يرى النموذج:

```text
عائلة الحوار: موضوع
الموضوع المطلوب: الصداقة
```

حتى لو كتب المستخدم `الصداقه`.

## ما لم يحدث

- لا تدريب.
- لا tokenizer جديد.
- لا SF-50M.
- لا runtime release رسمي.
- لا pretrained.
- لا قوالب تخفي ضعف المولد.

## التالي

```text
Phase 27.107 — Social Subfamily + Topic Variant Gate Encoding
```

تلك المرحلة يجب أن تبني gate قبل أي training:

- renderer emits social subfamily line.
- topic variants map to canonical topic.
- assistant-only mask excludes context lines.
- held-out raw UI probes موجودة.
