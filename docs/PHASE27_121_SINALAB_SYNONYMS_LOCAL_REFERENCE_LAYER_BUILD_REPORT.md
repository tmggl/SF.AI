# Phase 27.121 — Synonyms Local Reference Layer Build

## الخلاصة

تم بناء reference records محلية فقط داخل مسار gitignored.
المرفوع يحتوي counts/hashes فقط ولا يحتوي raw terms.

## القرار

```text
PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION
ALLOW_PHASE27_122_SYNONYMS_REFERENCE_QUERY_AND_EVAL_GATE_NO_TRAINING
```

## Build Counts

- local reference records: `1093`
- local eval candidates: `685`
- high quality: `685`
- medium quality: `408`
- low quality: `0`

## Local Files

- reference records JSONL: gitignored, contains terms locally only.
- eval candidates JSONL: gitignored, contains terms locally only.
- committed reports expose hashes/counts only.

## الممنوع

- raw terms in git.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime lookup activation.
- SF-50M transition.

## الملفات المرفوعة

- `resources/external_sources/phase27_121_sinalab_synonyms_local_reference_layer_build_manifest.json`
- `resources/external_sources/phase27_121_sinalab_synonyms_local_reference_layer_validation.json`
- `artifacts/reports/phase27_121_sinalab_synonyms_local_reference_layer_build_report.json`
- `artifacts/reports/PHASE27_121_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_DECISION.json`

## التالي

```text
Phase 27.122 — Synonyms Reference Query and Eval Gate, no training
```
