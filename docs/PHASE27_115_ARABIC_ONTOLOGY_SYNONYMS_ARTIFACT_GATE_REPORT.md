# Phase 27.115 — Arabic Ontology/Synonyms Artifact Gate

## الخلاصة

هذه مرحلة metadata-only. لم يتم تنزيل raw entries، ولم يُضاف أي corpus، ولم يبدأ تدريب.

## القرار

```text
PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION
ALLOW_PHASE27_116_SYNONYMS_ARTIFACT_QUARANTINE_SCHEMA_DRY_RUN_NO_IMPORT
```

## Arabic Ontology

- القرار: `BLOCK_IMPORT_REQUEST_ONLY_NO_DIRECT_ARTIFACT`.
- السبب: الوصول الظاهر عبر صفحة/نموذج طلب أو API token، ولا يوجد artifact مباشر مع checksum.

## SinaLab Synonyms

- القرار: `ALLOW_QUARANTINE_CHECKSUM_SCHEMA_DRY_RUN_ONLY`.
- السبب: GitHub repo مرصود وفيه `LICENSE` و`README` و`Synonyms Dataset.xlsx`، لكن لا يوجد checksum بعد.
- المسموح التالي فقط: تنزيل quarantine محسوب checksum + فحص schema بدون نقل raw rows إلى corpus.

## الممنوع

- training.
- runtime release.
- tokenizer vocab/merges من مصدر خارجي.
- إدخال raw entries إلى `data/corpus`.
- استخدام المصدر لتوليد حوارات تلقائية.

## Field Mapping

تم تصميم field mapping منفصل للمصدرين مع `training_allowed=false` و`tokenizer_vocab_allowed=false`.

## الملفات

- `resources/external_sources/phase27_115_arabic_ontology_synonyms_artifact_gate.json`
- `resources/external_sources/phase27_115_arabic_ontology_synonyms_field_mapping_design.json`
- `artifacts/reports/phase27_115_arabic_ontology_synonyms_artifact_gate_report.json`
- `artifacts/reports/PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION.json`

## التالي

```text
Phase 27.116 — Synonyms Artifact Quarantine Checksum and Schema Dry-Run, no import/training
```
