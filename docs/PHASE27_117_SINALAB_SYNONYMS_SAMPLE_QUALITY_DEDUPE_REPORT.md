# Phase 27.117 — Synonyms Sample Quality and Dedupe Review

## الخلاصة

تم فحص جودة وتكرار SinaLab Synonyms من داخل quarantine فقط.
التقرير ينشر أرقامًا وإحصاءات فقط ولا ينشر raw terms أو raw rows.

## القرار

```text
PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION
ALLOW_PHASE27_118_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_NO_TRAINING
```

## Quality

- candidate rows: `3010`
- sample window: `200`
- Arabic term ratio: `1.0`
- average score range: `0.0..100.0`
- operational contamination hits: `0`

## Dedupe

- unique normalized terms: `1697`
- internal duplicate terms: `1313`
- protected Saudi exact overlap count: `1`
- Saudi Seed exact overlap count: `40`

## الممنوع

- raw entry import.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime release.

## الملفات

- `resources/external_sources/phase27_117_sinalab_synonyms_sample_quality.json`
- `resources/external_sources/phase27_117_sinalab_synonyms_dedupe_review.json`
- `artifacts/reports/phase27_117_sinalab_synonyms_sample_quality_dedupe_report.json`
- `artifacts/reports/PHASE27_117_SINALAB_SYNONYMS_SAMPLE_QUALITY_DEDUPE_DECISION.json`

## التالي

```text
Phase 27.118 — Synonyms Reference Extraction Design, no training
```
