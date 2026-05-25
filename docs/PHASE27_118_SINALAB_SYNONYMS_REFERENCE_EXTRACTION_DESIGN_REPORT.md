# Phase 27.118 — Synonyms Reference Extraction Design

## الخلاصة

تم تصميم مسار reference extraction فقط، دون استخراج فعلي ودون نشر raw terms.
الهدف أن تكون المرحلة التالية dry-run counts فقط قبل أي reference artifact حقيقي.

## القرار

```text
PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION
ALLOW_PHASE27_119_SYNONYMS_REFERENCE_EXTRACTION_DRY_RUN_COUNTS_NO_TRAINING
```

## Inputs

- candidate rows: `3010`
- unique normalized candidate terms: `1697`
- internal duplicate terms: `1313`
- Saudi Seed exact overlap count: `40`

## Design Rules

- target lane: `reference_layer_only`.
- drop exact overlap with Saudi Seed v1 and protected Saudi terms before any future use.
- collapse duplicates by normalized term.
- commit counts and manifests only in the next dry-run.
- raw terms stay unpublished unless a later explicit gate allows a local reference artifact.

## الممنوع

- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime release.
- raw terms in git reports.

## الملفات

- `resources/external_sources/phase27_118_sinalab_synonyms_reference_extraction_design.json`
- `resources/external_sources/phase27_118_sinalab_synonyms_reference_extraction_gate.json`
- `artifacts/reports/phase27_118_sinalab_synonyms_reference_extraction_design_report.json`
- `artifacts/reports/PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION.json`

## التالي

```text
Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts, no training
```
