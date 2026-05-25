# Phase 27.125 — Synonyms Reference Adapter Local Dry-Run

## الخلاصة

تم تشغيل adapter محليًا على reference layer gitignored وإخراج
counts/hashes فقط. لا raw terms، لا query rows، لا runtime wiring،
ولا corpus/tokenizer/training.

## القرار

```text
PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION
ALLOW_PHASE27_126_SYNONYMS_REFERENCE_RUNTIME_POLICY_DESIGN_NO_ACTIVATION
```

## Metrics

- reference records: `1093`
- eval queries: `685`
- adapter index keys: `1093`
- exact lookup hits: `685`
- exact lookup rate: `1.0`
- redaction rate: `1.0`
- term leak count: `0`
- observed hash lengths: `[64]`

## الممنوع

- raw terms in git.
- query rows in git.
- runtime lookup activation.
- chat module integration.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- SF-50M transition.

## الملفات

- `resources/external_sources/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_metrics.json`
- `resources/external_sources/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_gate.json`
- `artifacts/reports/phase27_125_sinalab_synonyms_reference_adapter_local_dry_run_report.json`
- `artifacts/reports/PHASE27_125_SINALAB_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_DECISION.json`

## التالي

```text
Phase 27.126 — Synonyms Reference Runtime Policy Design, no activation
```
