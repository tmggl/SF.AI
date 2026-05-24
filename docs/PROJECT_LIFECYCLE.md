# PROJECT_LIFECYCLE.md

## دورة حياة SF.AI

هذه الوثيقة تشرح المسار الكامل من البيانات إلى runtime.

```text
corpus
→ tokenizer
→ training
→ checkpoint
→ eval
→ engineering root-cause gate
→ scaling gate
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
- `provenance.owner_user_id`.
- `provenance.created_by_user_id`.
- `provenance.target_user_id`.
- `provenance.user_scope`.

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
resources/tokenization/protected_terms_msa_candidate.txt
resources/tokenization/preferred_merges.txt
resources/tokenization/preferred_merges_msa_candidate.txt
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
- بعد Phase 27.78: لا يبدأ training جديد قبل `ENGINEERING_ROOT_CAUSE_GATE`
  وقرار يسمح به.

الحالة الحالية:

```text
PHASE27_78_ENGINEERING_DECISION.new_training_allowed = false
```

إذن أي عمل بعده يجب أن يكون design/gates/diagnostics أولًا، لا تدريب.

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

بعد Phase 27.78، eval لا يكتفي بـ loss/perplexity/micro-probe. يجب أن
يتضمن:

- held-out dialogue quality.
- runtime usability.
- clean-stop.
- semantic correctness.
- family stability.
- open_social naturalness.
- followup continuity.
- canary pass rate.
- human conversation realism.

## 5.5 Engineering Root-Cause Gate

هذه خطوة إلزامية بين eval وأي تدريب/تكبير/runtime جديد.

مدخلاتها:

- held-out/shadow canary reports.
- family confusion analysis.
- decoding/repetition/EOS inspection.
- tokenizer boundary audit.
- semantic routing diagnostics.
- objective tracing.
- regression summary.

مخرجاتها:

- Decision Report.
- Root Cause Report.
- Allowed/Blocked Actions.
- Runtime Decision.
- Regression Summary.

الحالة الحالية:

```text
Phase 27.78 — Engineering Root Cause Gate
PHASE27_78_ENGINEERING_DECISION
```

القرار الحالي يمنع training وruntime و`SF-50M`.

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
- `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- توثيق.
- إذن تفعيل.

حتى ذلك الوقت يبقى الشات:

- router.
- templates.
- composer.
- safety replies.

## 7. Progressive Scaling Strategy / Scaling Gate

Progressive Scaling Strategy هو المبدأ الحاكم للتكبير. وScaling Gate يقرر هل نكبر النموذج أم نبقى على الحجم الحالي.

القاعدة:

> لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

قبل الانتقال يجب أن تنجح:

- corpus readiness.
- tokenization audit.
- evaluation suite.
- safety checks.
- runtime quality.
- hallucination checks.
- repetition checks.
- resource readiness.
- `ENGINEERING_ROOT_CAUSE_GATE` يثبت أن capacity هي السبب الأكبر أو أن
  `SF-50M JUSTIFIED TRANSITION` صدر رسميًا.

إذا فشل gate، يعود المشروع إلى:

- توسيع corpus.
- تحسين tokenizer.
- تعديل eval.
- إعادة تدريب الحجم نفسه.
- تحسين runtime canary/fallback.
- إصلاح objective/curriculum/decoding/family balance إذا كانت هي السبب الأكبر.

## 7.1 Auto-Advance Scaling Mandate

إذا نجحت بوابة الحجم التالي، فدورة الحياة تنتقل تلقائيًا للحجم التالي دون
انتظار موافقة جديدة:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

هذا لا يختصر gates. هو يختصر الانتظار الإداري فقط. عند فشل أي gate، تعود
الدورة إلى التشخيص/الإصلاح بدل التكبير.

## نقاط الفصل

| المرحلة | تكتب أين؟ | تقرأ من أين؟ |
|---------|-----------|--------------|
| corpus audit | reports/logs | `data/corpus/` |
| tokenizer training | `artifacts/tokenizers/` | `data/corpus/` |
| LM training | `artifacts/checkpoints/`, `artifacts/logs/` | corpus + tokenizer |
| eval | `artifacts/logs/`, `docs/` | checkpoint |
| scaling gate | `docs/`, `artifacts/reports/` | eval + corpus + resources |
| runtime | لا يكتب artifacts تدريب | checkpoint مفعّل فقط |

## Gates

لا ينتقل artifact إلى المرحلة التالية إلا إذا:

- نجحت الاختبارات.
- اكتمل audit.
- لا توجد أسرار أو ملفات خاصة في git.
- وُثقت المخرجات.
- أعطى سامي الإذن إذا كانت خطوة عالية الأثر.
- نجحت scaling gate قبل أي حجم أكبر.

## الحالة الحالية

- المرحلة الحالية: `Phase 27.79 — Objective/Curriculum/Decoding Repair Design`.
- القرار الحالي: `PHASE27_79_REPAIR_DESIGN_DECISION`.
- corpus الحالي: `5943` سجلًا (`msa=2949`, `saudi=2994`).
- التدريب الجديد: محجوب.
- tokenizer الجديد: محجوب.
- runtime release: محجوب.
- `SF-50M`: محجوب لأن capacity وزنها الحالي `1%`.
- التالي: `Phase 27.80 — Repair Gate Encoding and Dry-Run Validation`.
