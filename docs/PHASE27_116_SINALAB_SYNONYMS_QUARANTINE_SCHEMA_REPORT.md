# Phase 27.116 — Synonyms Quarantine Checksum and Schema Dry-Run

## الخلاصة

تم تنزيل artifact في quarantine محلي git-ignored، وحُسب checksum، وفُحص schema فقط.
لم يتم نقل raw rows إلى corpus، ولم يبدأ tokenizer أو training.

## القرار

```text
PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION
ALLOW_PHASE27_117_SYNONYMS_SAMPLE_QUALITY_AND_DEDUPE_REVIEW_NO_TRAINING
```

## Artifact

- المصدر: `https://github.com/SinaLab/Synonyms`
- الملف: `Synonyms Dataset.xlsx`
- الحجم: `306625` bytes
- sha256: `a8622546d057f60d2cee0db3b8fdc79cf30303db6ae83001be1634215bb00035`
- quarantine path: `resources/external_sources/quarantine/sinalab_synonyms/raw/Synonyms Dataset.xlsx` (غير مرفوع إلى git)

## Schema Dry-Run

- sheets: `1`
- first sheet: `Sheet1`
- dimension: `A1:I4511`
- estimated rows: `4511`
- estimated columns: `9`

## الممنوع

- raw entry import.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime release.

## الملفات

- `resources/external_sources/phase27_116_sinalab_synonyms_quarantine_manifest.json`
- `resources/external_sources/phase27_116_sinalab_synonyms_schema_dry_run.json`
- `resources/external_sources/phase27_116_sinalab_synonyms_attribution.json`
- `artifacts/reports/phase27_116_sinalab_synonyms_quarantine_schema_report.json`
- `artifacts/reports/PHASE27_116_SINALAB_SYNONYMS_QUARANTINE_SCHEMA_DECISION.json`

## التالي

```text
Phase 27.117 — Synonyms Sample Quality and Dedupe Review, no training
```
