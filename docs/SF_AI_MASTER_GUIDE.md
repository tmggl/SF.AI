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

### 1.1 تصحيح ملزم: لا Open-Weight Lane

تم إلغاء أي تفسير سابق يفتح مسار `open-weight acceleration` أو Qwen أو
أي pretrained runtime. المقصود بـ **Sovereign Practical Acceleration** هو
تسريع الهندسة والتشخيص والتدريب فقط، لا استيراد عقل جاهز.

ممنوع رسميًا:

- Qwen / Llama / Mistral / Gemma أو أي open-weight pretrained model.
- أي runtime فوق نموذج جاهز.
- أي tokenizer/vocab/merges جاهزة.
- أي fine-tune أو LoRA فوق نموذج خارجي.

المسموح: أدوات هندسية عامة فقط، مثل PyTorch وTensorBoard وAMP وschedulers
وdecoding/curriculum/eval tooling، بشرط أن تكون أوزان SF.AI نفسها من
تدريب SF-native.

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
المرحلة الحالية: Phase 27.101
الاسم: Topic Binding Repair Result Diagnosis
الاستراتيجية الملزمة: Sovereign Practical Acceleration Strategy v2
القرار الرسمي: PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_DECISION
المسار اللغوي: msa + saudi فقط
القاموس: Saudi Seed v1
السيرفر المحلي: http://127.0.0.1:8123/ui/chat
```

القرار الحالي:

- تم تدريب Phase 27.95 bounded topic-objective SF-10M repair training، ثم شُخص فشله في Phase 27.96.
- لا tokenizer جديد الآن.
- لا runtime release الآن.
- لا انتقال إلى `SF-50M` الآن.
- نتيجة 27.81: أضيف 2500 سجل gold متوازن (`500` لكل family، `250/250`
  فصحى/سعودي)، وأعيد بناء split، ومرّت Phase 27.80 gates.
- نتيجة 27.82: فُحصت prerequisites السيادية وصدرت خطة تدريب 27.83 دون بدء التدريب.
- نتيجة 27.83: التدريب اكتمل، لكن best fresh shadow = `11/60`; runtime محجوب.
- نتيجة 27.84: family metadata لم تكن ظاهرة داخل نص التدريب، لذلك لم يصبح التوازن conditioning فعليًا.
- نتيجة 27.85: صُممت صيغة `عائلة الحوار: سوالف/متابعة/تنظيم/دعم/موضوع` كسياق masked.
- نتيجة 27.86: renderer gate نجحت؛ `render_dialogue_text` يطبع العائلة في no-split وsplit-manifest، وassistant-only loss يخفي السياق عن الهدف.
- نتيجة 27.87: تدريب SF-10M المقيّد اكتمل، لكن أفضل fresh shadow = `10/50`; runtime وSF-50M محجوبان.
- نتيجة 27.88: شُخّص الفشل كـ sequential curriculum collapse؛ `موضوع` ظهر 5 مرات فقط في أول 1800 عينة.
- نتيجة 27.89: أضيف `--split-order family_round_robin` ومرّت gate؛ أول 1800 عينة صارت `360` لكل family، وكل نافذة 600 فيها `120` لكل family.
- نتيجة 27.90: تدريب SF-10M محدود بالـ round-robin رفع fresh shadow إلى `35/50`، لكن topic بقي `1/10` والبوابة `45/50` لم تمر.
- نتيجة 27.91: التشخيص أثبت أن `9/15` من الإخفاقات من عائلة topic، وأكبر سبب `topic_semantic_collapse=48%`.
- نتيجة 27.92: صُمم objective مخصص لعائلة `topic` باسم `topic_anchor_prompt_to_answer_objective_v1`، مع شرط `الموضوع المطلوب: <topic_term>` وبوابات canary قبل أي تدريب.
- نتيجة 27.93: أضيف سطر `الموضوع المطلوب: <topic_term>` إلى renderer لعائلة topic، ومرّ dry-run للـ renderer/masking/canary.
- نتيجة 27.94: أضيفت `10` سجلات سعودية gold لموضوع `الوفاء`، وأُغلقت فجوة البيانات المحددة دون تدريب ودون runtime.
- corpus الحالي: `8453` (`msa=4199`, `saudi=4254`, `gold=3341`, `silver=5112`).
- إعادة بوابة 27.93 بعد 27.94: `training_data_ready=true`, `shortfalls={}`, و`الوفاء` صار `total=22`, `msa=12`, `saudi=10`.
- نتيجة 27.95: تدريب SF-10M محدود اكتمل، لكن البوابات فشلت: known topic `10/16`, fresh topic `4/10`, all-family `33/50`.
- نتيجة 27.96: التشخيص أثبت `topic_variable_binding_failure`: لا حارس يحجب الإخفاقات، بل النموذج يستبدل الموضوع المطلوب بموضوعات مجاورة. `wrong_topic_substitution_count=11`, وأكثر بديل خاطئ `الصداقة=6`.
- نتيجة 27.97: صُمم objective جديد `topic_copy_contrastive_binding_objective_v1` يفرض نسخ الموضوع المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا من رد المساعد، ويمنع نجاح الرد إذا ذكر موضوعًا مجاورًا قبل الموضوع المطلوب. القرار يسمح فقط بـ Phase 27.98 لترميز البوابة وتدقيق metadata، بلا تدريب.
- نتيجة 27.98: رُمزت بوابة الموضوع ونجحت آلية renderer/masking/canary، لكنها منعت التدريب لأن `500` سجل topic لا تحمل `topic_term` صريحًا. القرار يسمح فقط بإصلاح metadata وcopy-anchor في Phase 27.99، بلا تدريب.
- نتيجة 27.99: أضيف `topic_term` الصريح إلى `500` سجل topic وتأكدت copy-anchor؛ إعادة بوابة 27.98 صارت `training_ready=true` بلا runtime.
- نتيجة 27.100: تدريب topic-binding المقيّد اكتمل، لكنه لم يمر بوابات runtime:
  known `13/16`, fresh `5/10`, copy-anchor `18/26`, reported wrong-topic `0`,
  topic-family `6/10`, all-family `37/50`.
- نتيجة 27.101: التشخيص كشف blind spot في metric؛ observed wrong-topic `8`
  (`الصداقة=7`, `الامتنان=1`) رغم أن التقرير السابق سجّل `0`.
- التالي: `Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate`.

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

تم تحميل حزمة الأدوات المحلية المسرّعة في البيئة:

- `tensorboard` للتتبع المحلي.
- `tqdm` لعرض تقدم التشغيل.
- `psutil` لمراقبة موارد الجهاز.
- `safetensors` لحفظ tensors بأمان لاحقًا.
- `rich` لتقارير CLI أوضح.

تقرير الفحص: `docs/SOVEREIGN_ACCELERATION_TOOLKIT_LOADED.md`.

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
| Phase 27.79-27.99 | إصلاحات objective/curriculum/family/topic حتى إصلاح metadata، بلا runtime |

الدرس الأساسي من Phase 27:

```text
المولد تحسن في probes محددة، لكنه لا يزال غير ثابت في الحوار المفتوح.
لذلك نصلح بنية الهدف والمنهج والتقييم قبل أي تدريب جديد.
```

---

## 10. المرحلة التالية

المرحلة التالية الرسمية:

```text
Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate
```

مطلوب منها:

- إصلاح/ترميز blind spot في wrong-topic metric قبل أي تدريب.
- تصميم gate يفرض observed wrong-topic `0` لا reported فقط.
- تصميم canary لتمييز topic prototype attraction مثل `الصداقة`.
- تحديد شروط تدريب لاحق إن مرّت البوابة فقط.

ممنوع في 27.102 قبل القرار:

- تدريب جديد.
- runtime release.
- tokenizer retrain.
- SF-50M.
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
