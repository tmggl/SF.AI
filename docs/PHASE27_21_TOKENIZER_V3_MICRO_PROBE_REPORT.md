# Phase 27.21 — Tokenizer v3 Protected-Phrase Retrain + Micro-Probe

## القرار

```text
FAILED_TOKENIZER_V3_MICRO_PROBE_BLOCK_RUNTIME
```

هذه المرحلة درّبت tokenizer v3 سياديًا مع protected phrases من Phase 27.20،
ثم أعادت micro-probe على `SF-10M` باستخدام tokenizer v3.

## ماذا نجح؟

Tokenizer v3 نجح في الهدف اللغوي المباشر:

```text
tokenizer_path = artifacts/tokenizers/sf_bpe/v3
vocab_size     = 4706
merges         = 4648
sf_origin      = true
protected      = 5
max_pieces     = 1
all_roundtrip  = true
```

العبارات المحمية:

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
```

## ماذا فشل؟

المولد لم يجتز micro-probe:

```text
passed       = 25/32
exact_clean  = 26/32
semantic     = 30/32
guard_passed = 31/32
```

أسباب الفشل:

```text
not_exact_clean              = 4
missing_semantic_terms       = 2
guard:model_artifact_fragment = 1
```

## أمثلة فشل مهمة

```text
prompt    : أشعر بتوتر بسيط
expected  : خذ نفسًا هادئًا وابدأ بالأهم.
generated : خذ نفسًا هادئًاوابدأ بالأهم.
reason    : not_exact_clean
```

```text
prompt    : اشرح لي التعاون
expected  : التعاون يعني أن ننجز معًا بدل الانفراد.
generated : التعانشتغل سواونخفف الحمل.
reason    : missing_semantic_terms
```

```text
prompt    : وش يعني تعاون
expected  : يعني نشتغل سوا ونخفف الحمل.
generated : يعني نشتغل سواونخفف الحمل.
reason    : not_exact_clean
```

```text
prompt    : القراءة وش تفيد
expected  : توسع فهمك وتزيد كلماتك.
generated : القراءة تفيدوتوسع فهمك.
reason    : missing_semantic_terms
```

## التشخيص

Phase 27.20/27.21 أثبتتا أن protected phrases تعالج تمثيل العبارات داخل
tokenizer، لكنها لا تكفي وحدها لجعل النموذج يلتزم بالمسافات والجواب الصحيح.

المشكلة الآن أضيق:

- لصق كلمات بعد protected phrase مثل `سواونخفف` و`تفيدوتوسع`.
- خلط صيغة الجواب بين الفصحى والسعودي في أسئلة التعاون.
- بقاء artifact fragment واحد رغم صحة الجملة دلاليًا.

## قرار runtime

```text
runtime_allowed = false
sf50m_allowed   = false
```

لا تعرّض الواجهة المولد بعد. الواجهة تظل على router/templates حتى يمر
المولد من canary أوسع.

## التالي

```text
Phase 27.22 — Spacing/Boundary Loss Repair
```

هدف المرحلة التالية:

- علاج لصق الكلمات بعد protected phrases.
- إضافة probe يختبر المسافة بعد العبارات المحمية.
- عدم تكبير النموذج قبل نجاح clean spacing + semantic pass.

## الملفات

- `scripts/phase27_21_tokenizer_v3_micro_probe.py`
- `artifacts/tokenizers/sf_bpe/v3/`
- `artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json`
- `artifacts/samples/phase27_21_tokenizer_v3_micro_probe_generations.md`
