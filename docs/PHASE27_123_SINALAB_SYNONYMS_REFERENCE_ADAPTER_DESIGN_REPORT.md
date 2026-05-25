# Phase 27.123 — Synonyms Reference Adapter Design

## الخلاصة

تم تصميم عقد adapter فقط. لا يوجد كود adapter، ولا runtime wiring،
ولا قراءة terms في هذه المرحلة.

## القرار

```text
PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION
ALLOW_PHASE27_124_SYNONYMS_REFERENCE_ADAPTER_SKELETON_NO_RUNTIME
```

## Adapter Contract

- adapter: `SinaLabSynonymsReferenceAdapter`
- max results default: `5`
- max results cap: `10`
- default quality band: `high`
- output committed reports: counts/booleans/hashes only.

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

- `resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_spec.json`
- `resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_policy.json`
- `resources/external_sources/phase27_123_sinalab_synonyms_reference_adapter_design_gate.json`
- `artifacts/reports/phase27_123_sinalab_synonyms_reference_adapter_design_report.json`
- `artifacts/reports/PHASE27_123_SINALAB_SYNONYMS_REFERENCE_ADAPTER_DESIGN_DECISION.json`

## التالي

```text
Phase 27.124 — Synonyms Reference Adapter Skeleton, no runtime
```
