# SF_AI_MASTER_GUIDE.md

## الملف الرئيسي التسلسلي لمشروع SF.AI

هذا هو ملف الدخول الأول لأي Agent أو مهندس يعمل على SF.AI.

القاعدة الجديدة:

```text
اقرأ هذا الملف أولًا.
ثم ارجع للملفات التفصيلية فقط عند الحاجة.
```

السبب: ملفات المشروع كثيرة لأنها نشأت على مراحل: دستور، قواعد هندسية، خطة
تنفيذ، lifecycle، status، handoff، scaling. هذا مفيد كتوثيق متخصص، لكنه
مربك كنقطة بداية. لذلك هذا الملف يجمع الهدف، القواعد، التسلسل، الحالة
الحالية، والقرار التالي في مسار واحد.

---

## 1. الهوية

SF.AI مشروع لبناء نموذج لغوي سيادي مولد لسامي، من الصفر، بالعربية أولًا.

العبارة الحاكمة:

```text
نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.
```

المقصود:

- نستخدم PyTorch، أدوات تدريب، schedulers، decoding، tracking محلي، RAG محلي.
- لا نستخدم pretrained weights.
- لا نستخدم pretrained tokenizer أو vocab أو merges.
- لا نستخدم LLM خارجي.
- لا نستخدم hosted reasoning API.
- لا نستخدم datasets حوارية خارجية.
- لا نُدخل محادثات إدارة المشروع أو أسلوب سامي التشغيلي في corpus الحوار.

---

## 2. الهدف الأعلى

الهدف النهائي:

```text
نموذج لغوي سيادي مولد، يحاور بالعربية الفصحى واللهجة السعودية، ثم يكبر
تدريجيًا حتى SF-1B+ عبر gates حقيقية.
```

ليس الهدف:

- chatbot قوالب.
- keyword bot.
- واجهة فوق نموذج أجنبي.
- تحسين benchmark شكلي.
- إخفاء ضعف المولد بقوالب.

---

## 3. الحالة الحالية المختصرة

```text
المرحلة الحالية: Phase 27.78
الاسم: Engineering Root Cause Gate
الاستراتيجية الملزمة: Sovereign Practical Acceleration Strategy v2
القرار الرسمي: PHASE27_78_ENGINEERING_DECISION
المسار اللغوي: msa + saudi فقط
القاموس: Saudi Seed v1
السيرفر المحلي: http://127.0.0.1:8123/ui/chat
```

القرار الحالي:

- لا تدريب جديد الآن.
- لا tokenizer جديد الآن.
- لا runtime release الآن.
- لا انتقال إلى `SF-50M` الآن.
- التالي: `Phase 27.79 — Objective/Curriculum/Decoding Repair Design`.

أوزان السبب الجذري في Phase 27.78:

| العامل | الوزن |
|---|---:|
| family mixing | 22% |
| objective | 18% |
| curriculum | 16% |
| weak generalization | 14% |
| semantic routing | 10% |
| decoding | 7% |
| tokenizer | 4% |
| EOS | 4% |
| memorization | 2% |
| repetition | 2% |
| capacity | 1% |

الاستنتاج:

```text
المشكلة ليست حجم النموذج الآن. المشكلة هندسية/تعليمية في الهدف، المنهج،
توازن عائلات الحوار، وdecoding. لذلك لا SF-50M قبل إصلاح هذه الطبقات.
```

---

## 4. القواعد غير القابلة للكسر

1. Runtime لا يساوي Training.
2. لا pretrained weights.
3. لا pretrained vocab.
4. لا pretrained tokenizer merges.
5. لا external dialogue datasets.
6. لا hidden hosted APIs.
7. لا external reasoning services.
8. لا project workflow/operator dialogue contamination.
9. لا fake benchmark inflation.
10. لا template masking لإخفاء ضعف المولد.
11. لا phase جديدة بدون توثيق في الخطة والحالة.
12. لا تدريب جديد قبل `ENGINEERING_ROOT_CAUSE_GATE` يسمح به.
13. لا runtime release بدون `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
14. لا تكبير حجم قبل scaling gate.
15. checkpoints داخل `artifacts/` فقط، ولا تُرفع ملفات `state.pt`.
16. corpus داخل `data/corpus/` فقط.
17. lexicons داخل `resources/lexicons/` فقط.
18. reports منفصلة في `docs/` أو `artifacts/reports/`.
19. tests إلزامية قبل push.
20. فحص أسرار إلزامي قبل push.

---

## 5. استراتيجية التسريع السيادي v2

مسموح رسميًا لتسريع الهندسة:

- PyTorch.
- AMP / mixed precision.
- TensorBoard المحلي.
- schedulers.
- experiment tracking محلي.
- advanced decoding.
- repetition control.
- curriculum tooling.
- held-out canary.
- shadow canary.
- family-conditioned dialogue.
- contrastive evaluation.
- semantic routing diagnostics.
- objective tracing.
- anti-collapse diagnostics.
- local RLHF-lite / DPO / ORPO / preference optimization.
- LoRA / QLoRA على أوزان SF.AI فقط، وليس فوق نموذج خارجي.
- retrieval memory tooling.
- local vector retrieval.
- dialogue family balancing.
- EOS boundary tooling.
- checkpoint selector.
- tokenizer boundary audit.

المنع لا يزال مطلقًا على:

- pretrained weights.
- pretrained vocab.
- pretrained tokenizer merges.
- external dialogue datasets.
- hosted hidden APIs.
- external reasoning services.

---

## 6. اللغة والبيانات

المسار الحالي:

```text
msa + saudi فقط
```

القواعد:

- لا تفعيل للهجات أخرى runtime/training قبل قرار صريح.
- Arabizi له normalization خاص.
- code منفصل عن الحوار.
- corpus الحوار = تفاعل بشري طبيعي عام فقط.
- ممنوع إدخال محادثات تشغيلية أو هندسية أو خاصة بسامي.
- ممنوع إدخال أوامر مثل: التالي، اكمل، ارفع، phase، gates، corpus،
  tokenizer، pytest، commit، readiness.
- كل record تدريبي يحتاج: `source`, `license`, `quality`,
  `training_allowed`, `dialect`, وownership fields.

القاموس الحالي:

- `Saudi Seed v1` مرجع سعودي خاص من تأليف/تفويض سامي.
- `safety_terms.yaml` بوابة حساسة.
- ملفات tokenization policy تحت `resources/tokenization/`.

---

## 7. دورة الحياة

السلسلة الرسمية:

```text
corpus
→ corpus audit
→ tokenizer training/audit
→ LM training
→ checkpoint
→ evaluation
→ held-out/shadow canary
→ runtime gate
→ guarded runtime
→ live UI probes
```

لا يوجد اختصار يتجاوز evaluation أو canaries.

---

## 8. سلم النموذج والتكبير التلقائي

السلم الرسمي:

```text
SF-10M
→ SF-50M
→ SF-100M-class / SF-120M
→ SF-350M
→ SF-700M
→ SF-1B+
```

تفويض سامي الرسمي:

```text
إذا نجحت بوابة الحجم التالي، ينتقل الوكيل تلقائيًا للحجم التالي دون انتظار
موافقة جديدة، حتى SF-1B+.
```

لكن التفويض مشروط:

- لا تكبير إذا root-cause يقول إن المشكلة ليست capacity.
- لا تكبير إذا فشلت held-out أو shadow canary.
- لا تكبير إذا runtime usability غير مقبول.
- لا تكبير إذا الموارد غير جاهزة.
- لا تكبير إذا احتاجت الخطوة بيانات أو أوزان خارجية.

`M100` في كلام سامي يعني `SF-100M-class`. المستوى المعماري المسجل حاليًا
هو `SF-120M` ما لم يصدر تقرير معماري يعتمد `SF-100M` حرفيًا.

---

## 9. التسلسل التاريخي المختصر

| النطاق | النتيجة |
|---|---|
| Phase 0-5 | تأسيس المشروع، FastAPI، Orchestrator، Router، Composer، corpus schemas |
| Phase 5.5-6 | طبقة تدريب سيادية، tokenizer/transformer scaffolding |
| Phase 7-8 | Web/RAG محليان، غير مفعلين تلقائيًا |
| Phase 9 | واجهة محادثة |
| Phase 10 | skeleton domains |
| Phase 11 | corpus governance |
| Phase 12-14 | tokenizer v1 وSF-10M v0.1 تجارب محدودة |
| Phase 15-18 | adapter، eval، RAG bridge، data loop |
| Phase 19-21 | بوابات SF-50M وخارطة التوليد |
| Phase 22-24 | corpus v2، tokenizer v2، SF-10M v0.2 |
| Phase 25-26 | canary حجب runtime، وSF-50M not ready |
| Phase 27-27.77 | سلسلة طويلة لتحسين الحوار، tokenizer، objective، family balance، canaries |
| Phase 27.78 | root-cause gate أوقف التدريب الأعمى والتكبير |

الدرس الأساسي من Phase 27:

```text
المولد تحسن في probes محددة، لكنه لا يزال غير ثابت في الحوار المفتوح.
لذلك نصلح بنية الهدف والمنهج والتقييم قبل أي تدريب جديد.
```

---

## 10. المرحلة التالية

المرحلة التالية الرسمية:

```text
Phase 27.79 — Objective/Curriculum/Decoding Repair Design
```

مطلوب منها:

- Decision Report.
- Root Cause Report update.
- Allowed/Blocked Actions.
- Runtime Decision.
- Regression Summary.
- تصميم objective جديد أو معدل.
- تصميم curriculum عائلي متوازن.
- تصميم decoding controls.
- family confusion analysis.
- held-out/shadow canary definitions.

ممنوع في 27.79 حتى يصدر قرار:

- تدريب جديد.
- tokenizer جديد.
- runtime switch.
- SF-50M full training.

---

## 11. Workflow أي Agent

أي Agent يدخل المشروع يفعل التالي بالترتيب:

1. اقرأ هذا الملف كاملًا.
2. اقرأ `docs/PHASE_STATUS.md` للتفاصيل الزمنية.
3. اقرأ `docs/EXECUTION_PLAN.md` إذا ستعدل الخطة.
4. اقرأ `docs/PROJECT_CONSTITUTION.md` إذا ستغير مبدأ حاكم.
5. اقرأ `docs/SCALING_STRATEGY.md` إذا الموضوع تدريب أو حجم نموذج.
6. اقرأ `docs/DATASET_GOVERNANCE.md` إذا ستلمس corpus.
7. اقرأ `docs/TOKENIZATION_POLICY.md` إذا ستلمس tokenizer.
8. افحص `git status --short`.
9. احمِ تغييرات غيرك ولا ترجعها.
10. نفذ العمل.
11. شغل الاختبارات المناسبة، وغالبًا full tests قبل push.
12. افحص الأسرار والملفات الحساسة.
13. commit عربي واضح.
14. push فقط إذا نجحت الاختبارات والفحص.

---

## 12. خريطة الملفات السريعة

| المسار | الدور |
|---|---|
| `apps/api/` | FastAPI والواجهة |
| `sf_ai/core/` | orchestrator/router/nlp/composer/index |
| `sf_ai/modules/chat/` | ChatModule ومسار الحوار |
| `sf_ai/models/` | tokenizer/transformer |
| `sf_ai/training/` | training configs/checkpoints utilities |
| `sf_ai/datasets/` | loaders/schemas/validators |
| `resources/lexicons/` | القواميس |
| `resources/tokenization/` | قواعد tokenization |
| `data/corpus/` | corpus تدريبي فقط |
| `artifacts/checkpoints/` | checkpoints محلية، لا ترفع state.pt |
| `artifacts/reports/` | تقارير آلية |
| `docs/` | قرارات وتقارير وخطة |
| `tests/` | اختبارات |
| `scripts/` | أدوات CLI |

---

## 13. الملفات التفصيلية المرجعية

هذا الملف هو نقطة الدخول. الملفات التالية تفصيلية:

- `docs/PHASE_STATUS.md` للحالة التاريخية الدقيقة.
- `docs/EXECUTION_PLAN.md` للخطة الكاملة.
- `docs/PROJECT_CONSTITUTION.md` للدستور.
- `docs/ENGINEERING_RULES.md` لقواعد الهندسة.
- `docs/AGENT_ENGINEERING_RULES.md` لقواعد الوكلاء.
- `docs/SCALING_STRATEGY.md` للتكبير.
- `docs/PROJECT_LIFECYCLE.md` لدورة الحياة.
- `docs/DATASET_GOVERNANCE.md` للبيانات.
- `docs/TOKENIZATION_POLICY.md` للـ tokenizer.
- `docs/AGENT_HANDOFF.md` كسجل تسليم تاريخي.
- `NEXT_AGENT_PROMPT.md` كنص مختصر لبدء Agent جديد.

---

## 14. جملة التوجيه المختصرة

إذا ضاق الوقت، تذكّر هذا:

```text
SF.AI يبني عقلًا سياديًا عربيًا/سعوديًا من الصفر. لا تدريب ولا تكبير ولا
runtime قبل gates حقيقية. وعند نجاح gate الحجم، نكبر تلقائيًا حتى SF-1B+.
```
