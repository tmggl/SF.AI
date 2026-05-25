# Phase 27.122 — Synonyms Reference Query and Eval Gate

## الخلاصة

تم بناء query/eval index مؤقت في الذاكرة من reference layer المحلي.
المرفوع يحتوي metrics/counts فقط ولا يحتوي raw terms أو query rows.

## القرار

```text
PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION
ALLOW_PHASE27_123_SYNONYMS_REFERENCE_ADAPTER_DESIGN_NO_RUNTIME
```

## Metrics

- reference records: `1093`
- eval queries: `685`
- unique index keys: `1093`
- duplicate index keys: `0`
- exact lookup rate: `1.0`
- quality match rate: `1.0`

## الممنوع

- raw terms in git.
- query rows in git.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime lookup activation.
- SF-50M transition.

## الملفات

- `resources/external_sources/phase27_122_sinalab_synonyms_reference_query_eval_metrics.json`
- `resources/external_sources/phase27_122_sinalab_synonyms_reference_query_eval_gate.json`
- `artifacts/reports/phase27_122_sinalab_synonyms_reference_query_eval_gate_report.json`
- `artifacts/reports/PHASE27_122_SINALAB_SYNONYMS_REFERENCE_QUERY_EVAL_GATE_DECISION.json`

## التالي

```text
Phase 27.123 — Synonyms Reference Adapter Design, no runtime
```
