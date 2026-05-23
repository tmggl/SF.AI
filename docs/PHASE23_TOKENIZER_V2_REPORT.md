# PHASE23_TOKENIZER_V2_REPORT.md

## SF.AI — Phase 23 Tokenizer v2 Retrain & Audit

**Journey:** Phase 23 / 30  
**Status:** `COMPLETED_READY_FOR_PHASE24`  
**Language track:** Arabic MSA + Saudi only  
**Lexicon track:** Saudi Seed v1 as reference, not direct chat corpus  
**Model training started:** no

---

## الهدف

إعادة تدريب SF-BPE tokenizer من corpus Phase 22 المتوازن، بدل الاعتماد على
tokenizer v1 الصغير الذي تدرب على 30 سجلًا سعوديًا فقط.

Phase 23 لا يدرّب نموذجًا لغويًا. هذه المرحلة تجهز tokenizer v2 فقط.

---

## أمر التدريب

```bash
make train-bpe ARGS="--confirm-phase23-tokenizer --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v2 --vocab-size 8000 --name sf_bpe_v2"
```

ثم:

```bash
make phase23-tokenizer-audit
```

---

## المخرجات

```text
artifacts/tokenizers/sf_bpe/v2/
├── vocab.json
├── merges.txt
├── meta.json
├── tokenizer_config.json
├── provenance.json
└── audit_report.json
```

---

## نتائج التدريب

```text
vocab_size_actual : 4493
merges            : 4386
words_seen        : 23190
unique_words      : 2492
base_alphabet     : 107
sf_origin         : true
```

## Corpus المستخدم

```text
records          : 500
training_ready   : 500
dialects         : msa=250, saudi=250
quality          : gold=52, silver=448
source_files     : 22
extra_texts      : 0
```

ملاحظة بعد Phase 27: ملف `audit_report.json` داخل artifact قد يُعاد توليده
ليقرأ corpus الحالي بعد تنظيف الحوارات التشغيلية (`2143` سجلًا)، لكن tokenizer v2 نفسه تدرب
فعليًا على corpus Phase 22 عند `500` سجل. لا تعامل تحديث audit الحالي كتدريب
tokenizer جديد.

---

## مقارنة v1/v2

| المعيار | v1 | v2 |
|---------|----|----|
| records | 30 | 500 |
| dialects | saudi فقط | msa + saudi |
| vocab | 261 | 4493 |
| merges | 218 | 4386 |
| words_seen | 723 | 23190 |
| unique_words | 64 | 2492 |

تحسن protected Saudi terms:

```text
average_tokens_v1: 4.0
average_tokens_v2: 2.3
max_tokens_v1    : 10
max_tokens_v2    : 6
roundtrip_failures: none
aggressive_splits: none
```

---

## السيادة

- لا LLM خارجي.
- لا pretrained vocab.
- لا pretrained merges.
- لا pretrained weights.
- لا embeddings جاهزة.
- لا synthetic LLM corpus.
- `sf_origin=true`.

---

## القرار

```text
Phase 23 tokenizer v2: COMPLETED_READY_FOR_PHASE24
Next: Phase 24 — SF-10M v0.2 Quality Training
```

تنبيه مهم: tokenizer v2 ليس مولدًا حواريًا. الشات لا يصبح ذكيًا بمجرد
تغيير tokenizer. التحسن الحقيقي يظهر بعد Phase 24/25 عندما يُدرّب نموذج
جودة ويُختبر ضد التكرار والهلوسة.
