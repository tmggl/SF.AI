# Phase 27.111 — Qabas Lexicon Bootstrap Design

## الخلاصة

صُمم مسار Qabas كمعجم مساعد للمفردات والموضوعات، لكن لم يتم
استيراد أي مدخلات فعلية لأن الترخيص الأساسي يحتاج حسمًا.

## قرار المرحلة

```text
PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION
BLOCK_QABAS_IMPORT_ALLOW_PHASE27_112_LICENSE_RESOLUTION_GATE
```

## سبب الحجب

- Masader metadata تعرض Qabas بترخيص `Apache-1.0`.
- صفحة SinaLab resources تعرض Qabas بترخيص `CC-BY-ND-4.0`.
- لذلك يمنع المشروع أي import فعلي حتى تثبت رخصة artifact القابل للتحميل.

## المسموح الآن

- source card.
- field mapping design.
- dedupe/quality gates.
- تخطيط مسارات candidate terms/topics بعد حل الترخيص.

## الممنوع الآن

- إدخال raw Qabas entries.
- إدخال Qabas في `data/corpus`.
- استعمال Qabas كـ tokenizer vocab أو merges.
- تدريب أو runtime release.

## الملفات

- `resources/external_sources/qabas_source_card_phase27_111.json`
- `resources/external_sources/phase27_111_qabas_lexicon_bootstrap_design.json`
- `artifacts/reports/phase27_111_qabas_lexicon_bootstrap_design_report.json`
- `artifacts/reports/PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION.json`
- `resources/lexicons/imported/qabas_bootstrap/README.md`

## التالي

```text
Phase 27.112 — Qabas Primary License Resolution Gate, no training
```
