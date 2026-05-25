# Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts

## الخلاصة

تم تنفيذ dry-run counts فقط حسب تصميم 27.118. لا توجد raw terms أو reference records.

## القرار

```text
PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION
ALLOW_PHASE27_120_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATED_NO_TRAINING
```

## Counts

- input candidate rows: `3010`
- eligible before duplicate collapse: `1570`
- reference candidates after filters: `1093`
- eval candidates after filters: `685`

## Filter Drops

- score below reference: `1391`
- Saudi Seed overlap: `81`
- protected Saudi overlap: `1`
- duplicate dropped after filters: `316`

## الممنوع

- raw terms in reports.
- reference records written.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime release.

## الملفات

- `resources/external_sources/phase27_119_sinalab_synonyms_reference_dry_run_counts.json`
- `resources/external_sources/phase27_119_sinalab_synonyms_filter_drop_counts.json`
- `artifacts/reports/phase27_119_sinalab_synonyms_reference_dry_run_counts_report.json`
- `artifacts/reports/PHASE27_119_SINALAB_SYNONYMS_REFERENCE_DRY_RUN_COUNTS_DECISION.json`

## التالي

```text
Phase 27.120 — Synonyms Local Reference Layer Build Gate, no training
```
