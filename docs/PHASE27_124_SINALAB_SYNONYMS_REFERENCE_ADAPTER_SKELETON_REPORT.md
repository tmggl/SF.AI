# Phase 27.124 — Synonyms Reference Adapter Skeleton

## الخلاصة

تمت إضافة skeleton code للـ adapter فقط. الاختبار تم على سجلات
synthetic عربية غير مأخوذة من المصدر. لا يوجد runtime wiring، ولا
ChatModule integration، ولا corpus/tokenizer/training.

## القرار

```text
PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION
ALLOW_PHASE27_125_SYNONYMS_REFERENCE_ADAPTER_LOCAL_DRY_RUN_NO_RUNTIME
```

## Contract Checks

- adapter class: `SinaLabSynonymsReferenceAdapter`
- synthetic record count: `2`
- synthetic index keys: `5`
- max results default/cap: `5/10`
- redaction when terms requested: `True`
- terms included: `False`

## الممنوع

- raw source records.
- raw terms in git.
- query rows in git.
- runtime lookup activation.
- chat module integration.
- data/corpus writes.
- tokenizer vocab/merges.
- training.
- SF-50M transition.

## الملفات

- `sf_ai/reference_layers/sinalab_synonyms.py`
- `resources/external_sources/phase27_124_sinalab_synonyms_reference_adapter_skeleton_metrics.json`
- `resources/external_sources/phase27_124_sinalab_synonyms_reference_adapter_skeleton_gate.json`
- `artifacts/reports/phase27_124_sinalab_synonyms_reference_adapter_skeleton_report.json`
- `artifacts/reports/PHASE27_124_SINALAB_SYNONYMS_REFERENCE_ADAPTER_SKELETON_DECISION.json`

## التالي

```text
Phase 27.125 — Synonyms Reference Adapter Local Dry-Run, no runtime
```
