# Phase 27.109 — Free Linguistic Resource Intake Gate

## الخلاصة

تم اعتماد مسار تسريع مجاني سيادي يعتمد على مصادر لغوية جاهزة، لا عقول جاهزة.

القرار:

```text
PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION
```

المبدأ:

- مسموح: metadata، معاجم، corpora مرخصة، أدوات تنظيف وتشخيص.
- ممنوع: pretrained weights، pretrained tokenizer/vocab/merges، API خارجي.
- لا يدخل أي نص خارجي إلى `data/corpus` قبل gate ترخيص وتنظيف.

## المرشحون

```json
{
  "candidate_vocabulary_and_topic_bootstrap": 1,
  "approved_metadata_catalogue_only": 1,
  "candidate_msa_text_after_license_and_cleaning_gate": 1,
  "restricted_noncommercial_eval_or_vocabulary_only": 1,
  "candidate_eval_and_error_pattern_resource": 1,
  "candidate_dialect_vocab_eval_only_until_provenance_gate": 1,
  "blocked_until_license_lane_selected": 1
}
```

## الأفضل الآن

1. Masader: فهرس مجاني لاكتشاف المصادر وتصنيف الترخيص.
2. Qabas: معجم عربي كبير للموضوعات والكلمات المحمية.
3. Tashkeela: فصحى مشكولة لتحسين orthography/tokenization بعد تنظيف.
4. مصادر اللهجة السعودية: لا تدخل إلا بعد provenance/privacy/license gate.

## التالي

```text
Phase 27.110 — Qabas/Masader/Tashkeela Licensed Ingestion Design
```
