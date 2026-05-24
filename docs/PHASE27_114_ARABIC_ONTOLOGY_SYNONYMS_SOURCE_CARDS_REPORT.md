# Phase 27.114 — Arabic Ontology/Synonyms Source Cards

## الخلاصة

أُنشئت source cards وlicense matrix لـ Arabic Ontology وSinaLab Synonyms.
لا يوجد import فعلي ولا تدريب.

## القرار

```text
PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION
ALLOW_PHASE27_115_ARTIFACT_GATE_AND_FIELD_MAPPING_NO_IMPORT
```

## المصدران

- `arabic_ontology`: مرشح concept/topic semantics بعد artifact gate.
- `sinalab_synonyms`: مرشح semantic alternatives/eval بعد artifact gate.

## الممنوع الآن

- تنزيل artifact أو raw entries.
- إدخال corpus.
- tokenizer vocab أو merges.
- تدريب أو runtime release.

## الملفات

- `resources/external_sources/source_cards/arabic_ontology_phase27_114.json`
- `resources/external_sources/source_cards/sinalab_synonyms_phase27_114.json`
- `resources/external_sources/phase27_114_arabic_ontology_synonyms_license_matrix.json`
- `artifacts/reports/phase27_114_arabic_ontology_synonyms_source_cards_report.json`
- `artifacts/reports/PHASE27_114_ARABIC_ONTOLOGY_SYNONYMS_SOURCE_CARDS_DECISION.json`

## التالي

```text
Phase 27.115 — Arabic Ontology/Synonyms Artifact Gate and Field Mapping, no training
```
