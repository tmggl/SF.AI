# Phase 27.107 — Social Subfamily + Topic Variant Gate Encoding

## الخلاصة

مرّت بوابة التصميم التنفيذية. لا تدريب في هذه المرحلة.

القرار:

```text
PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_DECISION
```

النتيجة:

- renderer يدعم `نوع السوالف`.
- topic variants تتحول إلى canonical topic.
- canary الواجهة الخام موجودة.
- التالي ليس تدريبًا، بل data pack محكوم.

## Canary

ملف canary:

```text
artifacts/reports/phase27_107_social_subfamily_topic_variant_canary.json
```

يغطي:

- `السلام عليكم` → greeting.
- `كيف الحال` → smalltalk.
- `خلنا نسولف` → open_chat.
- `من أنت` → identity.
- `وش تقدر تسوي` → capability.
- `الصداقه` → الصداقة.
- `الاخوه` → الأخوة.

## القرار الهندسي

```text
ALLOW_PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_NO_TRAINING
```

المسموح:

- تأليف data pack سيادي gold.
- فصحى + سعودي فقط.
- source/license/quality/training_allowed إلزامية.

الممنوع:

- training جديد.
- runtime release رسمي.
- SF-50M.
- tokenizer retrain.
- pretrained/open-weight.

## التالي

```text
Phase 27.108 — Social Subfamily + Topic Variant Data Pack
```

الحد الأدنى:

- `420` سجل gold.
- `30` سجل لكل social subfamily لكل لهجة.
- `30` سجل لكل topic variant topic لكل لهجة.
