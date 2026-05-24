# Phase 27.113 — Permissive Lexical Alternatives Intake Gate

## الخلاصة

بعد حجب Qabas، صُنفت بدائل lexical مرخصة أو محتملة بدون أي import.

## القرار

```text
PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES_INTAKE_GATE_DECISION
ALLOW_PHASE27_114_SOURCE_CARDS_FOR_ARABIC_ONTOLOGY_AND_SYNONYMS_NO_IMPORT
```

## المرشحون المسموحون للمرحلة التالية فقط

- `arabic_ontology`: source card/license matrix فقط.
- `sinalab_synonyms`: source card/license matrix فقط.

## المحجوب أو المقيد

- `qabas`: reference-only بسبب `CC-BY-ND-4.0`.
- `arabic_wordnet_v4`: محجوب لأنه model-derived عبر Gemini رغم CC-BY-4.0.
- `omw_arabic_wordnet_v2`: مقيد ShareAlike.
- `salma_wsd`: eval/text-lane فقط، وليس lexicon import.

## الممنوع

- لا corpus.
- لا tokenizer vocab أو merges.
- لا تدريب.
- لا runtime release.

## التالي

```text
Phase 27.114 — Arabic Ontology/Synonyms Source Cards and License Matrix, no training
```
