# PHASE12_TOKENIZER_V1_REPORT.md

## SF.AI — Phase 12 Tokenizer v1 Report

**الحالة:** اكتملت Phase 12 كتشغيل tokenizer أول، مع قيود موثقة.

## إذن التنفيذ

سامي أعطى إذنًا صريحًا شاملًا في 2026-05-22 لمتابعة التدريب والاختبارات والمراحل المسجلة في الرحلة.

الأمر المستخدم:

```bash
make train-bpe ARGS="--confirm-phase12-permission --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1 --vocab-size 8000 --name sf_bpe_v1"
```

## المخرجات

```text
artifacts/tokenizers/sf_bpe/v1/
├── vocab.json
├── merges.txt
├── meta.json
├── tokenizer_config.json
├── provenance.json
└── audit_report.json
```

## نتائج التدريب

```text
vocab_size_actual : 261
merges            : 218
words_seen        : 723
unique_words      : 64
base_alphabet     : 43
sf_origin         : true
```

## Corpus المستخدم

```text
records          : 30
training_ready   : 30
dialect          : saudi only
quality          : gold
source_files     : 2
extra_texts      : 0
```

المصادر:

- `data/corpus/chat/jsonl/first_dialogue_seed.jsonl` — 20 سجلًا.
- `data/corpus/chat/jsonl/protected_terms_seed_v1.jsonl` — 10 سجلات.

## السيادة

- لا LLM خارجي.
- لا pretrained vocab.
- لا pretrained merges.
- لا pretrained weights.
- لا embeddings جاهزة.
- لا synthetic LLM corpus إضافي.
- `sf_origin=true`.

## القيود المعروفة

هذا tokenizer مناسب كـ **v1 smoke tokenizer** لبدء Phase 13.

ليس مناسبًا بعد كـ tokenizer عربي/سعودي متوازن؛ لأن corpus الحالي لا يحتوي `msa` بعد:

```text
required_dialects: msa, saudi
present_dialects : saudi
missing          : msa
```

## القرار

```text
Phase 12 tokenizer v1: COMPLETED_WITH_LIMITS
Next: Phase 13 — Tiny LM Smoke Training
MSA expansion remains required before quality/balanced runs.
```
