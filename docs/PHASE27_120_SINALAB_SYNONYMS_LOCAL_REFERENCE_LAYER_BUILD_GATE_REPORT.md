# Phase 27.120 — Synonyms Local Reference Layer Build Gate

## الخلاصة

تمت بوابة بناء reference layer محلي فقط. لا يوجد بناء records في هذه المرحلة،
ولا raw terms في git، ولا corpus/tokenizer/training/runtime.

## القرار

```text
PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION
ALLOW_PHASE27_121_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GITIGNORED_NO_TRAINING
```

## Gate

- gate passed: `True`
- reference path: `resources/external_sources/reference_layers/sinalab_synonyms`
- max local reference records next: `1093`
- max local eval candidates next: `685`
- storage mode: `local_gitignored_reference_layer_only`

## المسموح في المرحلة التالية فقط

- بناء records محلية داخل مسار gitignored.
- كتابة manifests/reports committed تحتوي counts/schema فقط.
- منع raw terms من أي ملف مرفوع.

## الممنوع

- data/corpus writes.
- tokenizer vocab/merges.
- training.
- runtime lookup activation.
- SF-50M transition.
- raw terms in committed files.
- raw terms in git.

## الملفات

- `resources/external_sources/phase27_120_sinalab_synonyms_local_reference_layer_build_gate.json`
- `resources/external_sources/phase27_120_sinalab_synonyms_local_reference_layer_schema.json`
- `artifacts/reports/phase27_120_sinalab_synonyms_local_reference_layer_build_gate_report.json`
- `artifacts/reports/PHASE27_120_SINALAB_SYNONYMS_LOCAL_REFERENCE_LAYER_BUILD_GATE_DECISION.json`

## التالي

```text
Phase 27.121 — Synonyms Local Reference Layer Build, gitignored, no training
```
