# Phase 27.112 — Qabas Primary License Resolution Gate

## الخلاصة

حُسمت البوابة بشكل محافظ: Qabas يبقى `reference-only` ولا يدخل
كمداخل فعلية أو corpus أو tokenizer vocab.

## القرار

```text
PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION
BLOCK_QABAS_IMPORT_REFERENCE_ONLY_OPEN_PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES
```

## الأدلة

- Masader metadata: `Apache-1.0`.
- SinaLab resources primary page: `CC-BY-ND-4.0`.
- صفحة Qabas/About لا تعرض رخصة artifact أو شروط استخدام قابلة للحسم.

## لماذا حُجب الاستيراد؟

- الترخيص الأساسي المرصود يحتوي `ND`، وهذا يمنع المشتقات.
- يوجد تضارب مع Masader metadata.
- لا توجد رخصة artifact قابلة للتحميل محفوظة محليًا تحسم النزاع.

## المسموح

- استخدام Qabas كمرجع metadata/source-discovery فقط.
- الاستمرار في البحث عن مصادر lexical permissive بترخيص أوضح.

## الممنوع

- raw Qabas entries.
- Qabas داخل `data/corpus`.
- Qabas كـ tokenizer vocab أو merges.
- تدريب أو runtime release.

## التالي

```text
Phase 27.113 — Permissive Lexical Alternatives Intake Gate, no training
```
