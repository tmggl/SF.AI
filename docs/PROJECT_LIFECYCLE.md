# PROJECT_LIFECYCLE.md

## دورة حياة SF.AI

هذه الوثيقة تشرح المسار الكامل من البيانات إلى runtime.

```text
corpus
→ tokenizer
→ training
→ checkpoint
→ eval
→ runtime
```

كل خطوة لها مدخلات ومخرجات وحدود.

## 1. Corpus

المكان:

```text
data/corpus/
```

المدخلات المقبولة:

- JSONL.
- UTF-8.
- `provenance.source`.
- `provenance.license`.
- `provenance.language`.
- `provenance.dialect`.
- `provenance.quality`.
- `provenance.training_allowed=true`.

قبل التدريب:

```bash
make source-inventory
make corpus-audit
make tokenization-audit
```

وقبل Phase 12 تحديدًا:

```text
docs/PROJECT_CONSTITUTION.md
docs/LANGUAGE_SEGMENTATION.md
docs/TOKENIZATION_POLICY.md
resources/tokenization/tokenization_rules.yaml
resources/tokenization/protected_terms_saudi.txt
resources/tokenization/preferred_merges.txt
```

مخرجات corpus stage:

- training-ready samples.
- audit report.
- معرفة واضحة بالمصادر والموانع.

## 2. Tokenizer

المكان:

```text
sf_ai/models/tokenizer/
artifacts/tokenizers/
```

القاعدة:

- tokenizer يتدرب من corpus محلي فقط.
- لا يستخدم vocab جاهز.
- لا يستخدم merges جاهزة.
- artifacts تخرج إلى `artifacts/tokenizers/`.

لا يبدأ إلا بإذن صريح.

مخرجات tokenizer:

```text
vocab.json
merges.txt
tokenizer_config.json
meta/provenance
audit_report
```

## 3. Training

المكان:

```text
sf_ai/training/
```

المدخلات:

- corpus جاهز.
- tokenizer سيادي.
- training config.

القواعد:

- لا pretrained weights.
- start from random initialization.
- لا تحميل models من الإنترنت.
- logs إلى `artifacts/logs/`.
- checkpoints إلى `artifacts/checkpoints/`.

## 4. Checkpoint

المكان:

```text
artifacts/checkpoints/
```

كل checkpoint يجب أن يحتوي metadata واضحة:

- `sf_origin=true`.
- corpus reference.
- tokenizer reference.
- config.
- date.
- training command.
- eval status.

checkpoint غير موثق لا يدخل runtime.

## 5. Eval

المكان:

```text
sf_ai/training/evaluate_*.py
artifacts/logs/
docs/
```

التقييم قبل runtime إلزامي:

- loss.
- overfit sanity.
- prompt sanity.
- Saudi/MSA style checks.
- safety checks.
- hallucination notes.

eval لا يساوي قبول runtime. هو شرط قبل القبول.

## 6. Runtime

المكان:

```text
apps/api/
sf_ai/core/
sf_ai/modules/
```

runtime يستخدم checkpoint فقط بعد:

- training ناجح.
- eval ناجح.
- safety gate.
- توثيق.
- إذن تفعيل.

حتى ذلك الوقت يبقى الشات:

- router.
- templates.
- composer.
- safety replies.

## نقاط الفصل

| المرحلة | تكتب أين؟ | تقرأ من أين؟ |
|---------|-----------|--------------|
| corpus audit | reports/logs | `data/corpus/` |
| tokenizer training | `artifacts/tokenizers/` | `data/corpus/` |
| LM training | `artifacts/checkpoints/`, `artifacts/logs/` | corpus + tokenizer |
| eval | `artifacts/logs/`, `docs/` | checkpoint |
| runtime | لا يكتب artifacts تدريب | checkpoint مفعّل فقط |

## Gates

لا ينتقل artifact إلى المرحلة التالية إلا إذا:

- نجحت الاختبارات.
- اكتمل audit.
- لا توجد أسرار أو ملفات خاصة في git.
- وُثقت المخرجات.
- أعطى سامي الإذن إذا كانت خطوة عالية الأثر.

## الحالة الحالية

- corpus seed صغير موجود: `first_dialogue_seed.jsonl`.
- `corpus-audit` جاهز بنيويًا: 30/30، لكن `phase12-readiness` يطلب إضافة `msa`.
- Phase 12 لم تبدأ.
- tokenizer training ممنوع حتى إذن صريح.
