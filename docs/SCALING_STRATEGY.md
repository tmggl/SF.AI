# SCALING_STRATEGY.md

## SF.AI — Progressive Scaling Strategy

**Status:** governance rule, no training started
**Language track:** Arabic MSA + Saudi only
**Lexicon track:** Saudi Seed v1 + governed MSA/Saudi corpus
**Current gate:** Phase 27.97 designed the topic variable-binding objective; Phase 27.98 gate encoding next; SF-50M remains blocked.

---

## المبدأ الرسمي

> لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

SF.AI لا يكبر بالقفزات. يكبر فقط عندما تثبت المرحلة الحالية أنها تستحق الانتقال:

- بيانات كافية.
- tokenizer صالح.
- evaluation ناجح.
- safety واضح.
- runtime quality مقبولة.
- لا تكرار مرضي.
- لا هلوسة عالية.
- الجهاز والوقت مناسبين.

---

## Sovereign Practical Acceleration Strategy v2

هذا التحول هو المسار الرسمي الأعلى بعد Phase 27.77: **تسريع سيادي عملي v2**.
المشروع لا يعيد اختراع الأدوات الرياضية والهندسية العامة، لكنه لا يستورد
ذكاءً جاهزًا.

تفسير ملزم بعد تصحيح 2026-05-24:

```text
Sovereign Practical Acceleration = engineering/training/eval acceleration only
Sovereign Practical Acceleration != open-weight/pretrained model lane
```

أي مسار Qwen أو Open-Weight Acceleration أو pretrained runtime ملغى وغير
معتمد. التكبير الرسمي يبقى داخل `SF-native` فقط: أوزان SF.AI تبدأ من
تدريب المشروع، وLoRA/QLoRA إن استُخدمت لاحقًا تكون فوق أوزان SF.AI نفسها.

### ما يبقى سياديًا بالكامل

- corpus: لا بيانات حوار خارجية ولا project-workflow contamination.
- tokenizer: لا vocab جاهز ولا merges جاهزة.
- behavior/alignment/runtime: سلوك SF.AI يُبنى من بياناته وحراسه وتقييمه.
- evaluation: held-out canary محلي، مع novelty وsemantic correctness.
- Saudi/MSA dialogue behavior: فصحى + سعودي فقط في هذا المسار.

### الأدوات المسموحة للتسريع

- PyTorch وstandard Transformer engineering.
- TensorBoard محلي أو CSV/JSON logs محلية.
- schedulers وAMP/mixed precision.
- advanced decoding مثل no-repeat/repetition penalty/temperature/top-k.
- repetition control.
- curriculum tooling وdialogue-family balancing.
- held-out canary وshadow canary.
- family-conditioned dialogue.
- contrastive evaluation.
- semantic routing diagnostics.
- objective tracing وanti-collapse diagnostics.
- local RLHF-lite / DPO / ORPO / preference optimization.
- LoRA / QLoRA فوق أوزان SF.AI فقط.
- retrieval memory tooling وlocal vector retrieval.
- EOS boundary tooling.
- experiment tracking وcheckpoint selection محليًا.
- tokenizer boundary audit.
- optimization tooling لا يستورد أوزانًا أو vocab أو corpus.

### الاختصارات الممنوعة

- pretrained weights أو embeddings.
- open-weight pretrained models مثل Qwen/Llama/Mistral/Gemma.
- pretrained vocab أو pretrained tokenizer merges.
- external dialogue datasets أو synthetic LLM data خارجي.
- hidden hosted APIs أو external reasoning services.
- إدخال حوارات إدارة المشروع أو أوامر الوكيل داخل corpus الحوار العام.
- fake benchmark inflation.
- template masking لإخفاء ضعف المولد.

### ENGINEERING_ROOT_CAUSE_GATE

قبل أي تدريب جديد يجب أن يصدر:

```text
PHASE27_78_ENGINEERING_DECISION
```

### Current Scaling Decision — Phase 27.97

Phase 27.97 لا يفتح حجمًا أكبر. القرار الحالي هو:

```text
PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_DECISION
ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING
```

السبب: Phase 27.96 شخّصت فشل 27.95 كخلل ربط متغير الموضوع لا كحد سعة.
كل إخفاقات topic تقريبًا تمر من الحارس، لكن النموذج يستبدل الموضوع المطلوب
بموضوعات مجاورة: `wrong_topic_substitution_count=11`، وأكثر بديل خاطئ
`الصداقة=6`. لذلك صممت Phase 27.97 objective
`topic_copy_contrastive_binding_objective_v1`: يجب أن ينسخ الرد الموضوع
المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا، ويُسقط أي رد يذكر موضوعًا مجاورًا
قبل المطلوب. يبقى `SF-50M` محجوبًا، ولا يسمح بتدريب جديد قبل Phase 27.98
كترميز بوابة وتدقيق metadata.

ويجب أن يحدد أوزان الأسباب التالية:

- capacity.
- objective.
- curriculum.
- tokenizer.
- decoding.
- family mixing.
- memorization.
- weak generalization.
- EOS.
- repetition.
- semantic routing.

إذا كان السبب الأكبر objective/training/decoding/family balance، يمنع
التكبير ويُنفذ إصلاح بنيوي. إذا بقي family mixing أو weak generalization
أو semantic collapse بعد التشخيص والإصلاح الصحيح، تُفتح بوابة:

```text
SF-50M JUSTIFIED TRANSITION
```

### القرار العملي قبل أي تكبير

لا فتح `SF-50M` رسمي قبل إثبات limit حقيقي لـ `SF-10M` بعد إصلاح:

- tokenizer.
- EOS/clean-stop.
- generalization.
- dialogue-family balance.
- decoding/no-repeat runtime controls.
- open_social stability.

إذا فشل `SF-10M` بعد هذه الإصلاحات وبوابات held-out، يُفتح Gate رسمي
لـ `SF-50M`. إذا لم تُفهم العلة بعد، فالخطوة الصحيحة inspection أو
curriculum/eval repair، لا تكبير الحجم.

### NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS

لا تفعيل runtime ولا واجهة مولّدة قبل نجاح held-out/shadow canaries في:

- held-out dialogue quality.
- runtime usability.
- clean-stop.
- semantic correctness.
- family stability.
- open_social naturalness.
- followup continuity.
- canary pass rate.
- human conversation realism.

لا تُقبل `loss` أو `perplexity` أو micro-probe وحدها كدليل نجاح.

---

## السلم الرسمي للأحجام

| الترتيب | الحجم | متى يُنظر فيه؟ |
|---------|------|----------------|
| 1 | `SF-10M` | إثبات pipeline وتدريب جودة أولي |
| 2 | `SF-50M` | بعد نجاح 10M وجود corpus أقوى |
| 3 | `SF-100M-class` / `SF-120M` | بعد نجاح 50M في الحوار والتقييم |
| 4 | `SF-350M` | بعد corpus كبير وتقييم متعدد الأدوار |
| 5 | `SF-700M` | بعد ثبات runtime وموارد واضحة |
| 6 | `SF-1B+` | فقط بعد نجاح كل ما سبق، لا كقفزة مبكرة |

لا يوجد مسار رسمي يقفز من `SF-10M` إلى `3B` أو `1B+` مباشرة.

---

## Auto-Advance Scaling Mandate

سامي فوّض المشروع رسميًا: **عندما تفتح بوابة الحجم التالي بنجاح، ينتقل
الوكيل تلقائيًا إلى الحجم التالي في السلم دون انتظار موافقة جديدة.**

هذا التفويض يسرّع الوصول إلى الهدف الأعظم `SF-1B+`، لكنه لا يلغي gates:

- لا انتقال إذا لم يصدر `ENGINEERING_ROOT_CAUSE_GATE`.
- لا انتقال إذا كان سبب الفشل objective/curriculum/decoding/family balance.
- لا انتقال إذا لم تنجح held-out/shadow canaries.
- لا انتقال إذا لم ينجح runtime usability.
- لا انتقال إذا لم تكن الموارد جاهزة.
- لا انتقال إذا احتاجت الخطوة pretrained أو data خارجية.

السلم التلقائي:

```text
SF-10M
→ SF-50M
→ SF-100M-class / SF-120M
→ SF-350M
→ SF-700M
→ SF-1B+
```

`SF-100M-class` هو اسم عملي للحجم الذي طلبه سامي بـ “M100”. التنفيذ
المعماري الحالي يسمي هذا المستوى `SF-120M`، إلا إذا صدر تقرير معماري لاحق
يعتمد `SF-100M` حرفيًا.

القاعدة: **لا تنتظر إذنًا جديدًا عندما تنجح البوابة، ولا تقفز عندما تفشل.**

---

## Scaling Gates

قبل أي انتقال إلى حجم أكبر، يجب أن تمر البوابة كاملة:

1. **corpus readiness**
   سجلات كافية، موثقة، مسموحة للتدريب، ومتوازنة بين `msa` و`saudi`.

2. **tokenization audit**
   protected terms محفوظة، الكلمات السعودية الشائعة لا تُكسر بعنف، ولا vocab جاهز.

3. **evaluation suite**
   prompt tests + multi-turn dialogue tests + comparison مع المرحلة السابقة.

4. **safety checks**
   المجالات الحساسة لا تتحول إلى نصائح تخصصية، والرفض الآمن يعمل.

5. **runtime quality**
   الردود داخل الواجهة لا تتدهور مقارنة بالقوالب أو النموذج السابق.

6. **hallucination checks**
   النموذج لا يدّعي معرفة أو أفعالًا غير موجودة في النظام.

7. **repetition checks**
   لا تكرار مثل `المعنى/وأين/يستخدم؟` أو loops طويلة.

8. **resource readiness**
   الجهاز، الوقت، التخزين، checkpoint policy، وresume plan جاهزة.

9. **dialogue-family balance**
   لا تنهار عائلة إلى أخرى: `open_social`, `followup`, `planning`,
   `support`, و`topic` تُقاس منفصلة ومجتمعة.

10. **clean-stop and decoding checks**
    EOS يعمل، ولا تكرار مرضي، وno-repeat/repetition controls مفعلة في
    runtime المرشح.

إذا فشل gate واحد، يبقى النموذج عند الحجم الحالي ويتم تحسين البيانات أو التدريب بدل التكبير.

---

## لماذا البيانات أهم من الحجم في البداية؟

النموذج الصغير مع بيانات جيدة يكشف مشاكل اللغة بسرعة:

- هل corpus طبيعي؟
- هل tokenizer يكسر السعودي؟
- هل الردود تتكرر؟
- هل التقييم يقيس ما نريده؟
- هل runtime يخلط بين القالب والمولد؟

أما النموذج الكبير مع corpus ضعيف فيكبر الخطأ بدل أن يحله. الحجم لا يخلق معرفة موثوقة من بيانات قليلة؛ غالبًا يزيد القدرة على تكرار الانحرافات والهلوسة.

---

## لماذا 3B قبل corpus قوية خطأ؟

القفز إلى `3B` قبل corpus قوية خطأ هندسي لأن:

- تكلفة التدريب أعلى بكثير.
- الأخطاء تصبح أغلى في التشخيص.
- corpus الضعيف ينتج نموذجًا أكبر لكنه ليس أذكى.
- Apple Silicon المحلي قد يصبح عنق زجاجة للذاكرة والوقت.
- التقييم الضعيف قد يعطي وهم تقدم.
- runtime سيبدو مثيرًا لحظيًا لكنه غير موثوق.

الطريق الصحيح: نثبت جودة `10M`، ثم نرفع إلى `50M`، ثم `120M`، وهكذا.

---

## كيف يقرر النظام أنه جاهز للحجم التالي؟

يقرر عبر تقرير gate، لا عبر الحماس:

```text
current_model_eval_passed = true
corpus_ready = true
tokenizer_audit_passed = true
safety_passed = true
hallucination_rate <= threshold
repetition_rate <= threshold
runtime_canary_passed = true
resources_ready = true
```

إذا كانت كل القيم صحيحة، يُسمح بفتح مرحلة الحجم التالي. إذا لا، تكون الخطوة الصحيحة:

- توسيع corpus.
- تحسين tokenizer.
- تعديل eval.
- إعادة تدريب الحجم نفسه.
- تحسين canary/fallback.

---

## شروط الانتقال من SF-10M إلى SF-50M

قبل `SF-50M` يجب توفر:

- corpus محكوم لا يقل عمليًا عن `5000` سجل حوار أو قرار gate موثق يخفض الحد لأسباب قوية.
- وجود `msa` و`saudi` في corpus، لا سعودي فقط.
- tokenizer حديث يمر `tokenization-audit`.
- `SF-10M v0.2` أو أحدث يثبت تحسنًا على `SF-10M v0.1`.
- evaluation suite تنجح، بما فيها safety وSaudi/MSA style.
- repetition checks تنجح ضد عينة `المعنى/وأين`.
- hallucination checks تنجح.
- runtime canary لا يخدع المستخدم بردود رديئة.
- held-out canary دائم وغير مرئي للتدريب يثبت جودة الحوار، خصوصًا
  `open_social` وsemantic correctness.
- no-repeat/repetition controls موثقة ومفعلة في runtime المرشح.
- الجهاز والتخزين والوقت كافية، مع checkpoint/resume plan.

حتى تتحقق هذه الشروط، يبقى المشروع في تحسين البيانات أو إعادة تدريب `SF-10M`.

---

## قرار Phase 27.54

Phase 27.54 طبقت هذه القاعدة بعد ثلاث نتائج متتابعة:

- Phase 27.51: raw natural `1/20`.
- Phase 27.52: raw natural `5/20` بعد `9200` خطوة.
- Phase 27.53: raw natural `2/36` بعد `10,540` سجلًا فريدًا و`18,000` خطوة.

القرار الرسمي:

- لا تدريب `SF-50M` كامل الآن.
- لا Phase 28 الآن.
- لا runtime switch لأي مرشح جديد.
- المسموح فقط Phase 27.55 كـ diagnostic micro-probe مضبوط، يقارن `SF-50M` ضد `SF-10M` بنفس البيانات والتقييم، ولا يعتبر انتقالًا رسميًا للحجم الأكبر.

سبب القرار: زيادة البيانات وحدها لم تنقذ `SF-10M` في الحوار المفتوح، لكن هذا لا يثبت وحده أن الحل هو التكبير. يجب فصل أثر السعة عن أثر objective/format/tokenization قبل صرف وقت تدريب أكبر.

---

## قرار Phase 27.55

Phase 27.55 نفذت المقارنة التشخيصية المسموحة:

- نفس tokenizer: `v6_weak_lane_terms`.
- نفس corpus التشخيصي: `6400` سجل من `40` زوجًا.
- نفس خطوات التدريب: `700` لكل نموذج.
- نفس eval: `20` prompt حوار طبيعي.

النتيجة:

- `SF-10M`: `3/20`.
- `SF-50M`: `4/20`.
- الفرق: `+1` فقط.

القرار الرسمي:

- لا runtime switch.
- لا تدريب `SF-50M` كامل.
- لا Phase 28.
- لا محاولة سعة جديدة قبل Phase 27.56.

سبب القرار: السعة وحدها لم تثبت أنها تحل الحوار المفتوح. المشكلة ما زالت في objective/format/tokenization أو في تصميم بيانات/تقييم الحوار، لذلك الإصلاح القادم يجب أن يعزل هذه الأسباب قبل أي تكلفة تدريب أكبر.

---

## قرار Phase 27.56

Phase 27.56 شخّصت سبب فشل Phase 27.55 بدون تدريب جديد:

- `SF-50M strict`: `4/20`.
- `SF-50M relaxed` بدون شرط overlap: `9/20`.
- `expected_terms_missing`: `9`.
- `response_family_confusion`: `11`.
- critical tokenizer splits: `9`.

القرار الرسمي:

- لا تدريب جديد الآن.
- لا runtime switch.
- لا `SF-50M` كامل.
- لا Phase 28.
- لا محاولة سعة جديدة قبل إصلاح tokenizer/eval/format.

سبب القرار: هناك فشل في أدوات القياس والتمثيل نفسها. معيار overlap يرفض ردودًا طبيعية، tokenizer يكسر عبارات سعودية/حواريّة، والنموذج يخلط عائلات الردود. أي تدريب قبل إصلاح هذه الطبقات سيقيس الخطأ أو يكرره.

## قرار Phase 27.78 — ENGINEERING_ROOT_CAUSE_GATE

Phase 27.78 أوقفت التدريب الأعمى رسميًا وأصدرت:

```text
PHASE27_78_ENGINEERING_DECISION
```

الأوزان التقريبية للأسباب:

- family mixing: `22%`.
- objective: `18%`.
- curriculum: `16%`.
- weak generalization: `14%`.
- semantic routing: `10%`.
- decoding: `7%`.
- tokenizer: `4%`.
- EOS: `4%`.
- memorization: `2%`.
- repetition: `2%`.
- capacity: `1%`.

القرار الرسمي:

- الاستمرار على `SF-10M`.
- منع `SF-50M` الآن.
- منع أي تدريب جديد حتى تُشفّر gates لإصلاح objective/curriculum/decoding.
- منع tokenizer جزئي جديد لأن tokenizer ليس السبب الأكبر حاليًا.
- منع runtime release تحت `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.

---

## قرار Phase 27.57

Phase 27.57 أصلحت طبقات القياس والتمثيل قبل التدريب:

- protected phrases: `18`.
- critical coverage: `9/9`.
- prompt-overlap gate: disabled.
- semantic alignment: enabled.
- response-family collapse checks: `5`.

القرار الرسمي:

- يسمح فقط بـ Phase 27.58 كتدريب محدود للـ tokenizer/probe.
- لا runtime switch.
- لا `SF-50M` كامل.
- لا Phase 28.

سبب القرار: أصبح لدينا repair pack يغطي عيوب Phase 27.56، لكن لم يُختبر بعد على tokenizer/model جديد. الخطوة التالية يجب أن تختبر الحزمة ضمن probe محدود قبل أي توسع.

## قرار Phase 27.58

Phase 27.58 نفذت التدريب المحدود المسموح:

- tokenizer v7: نجح في حماية عبارات Phase 27.57 (`max_pieces=1`).
- bounded alignment probe: فشل `4/15`.
- `open_social` و`followup` لم ينجحا (`0/3` لكل منهما).

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة للمرشح.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.59 إصلاح alignment قبل أي محاولة تكبير.

## قرار Phase 27.59

Phase 27.59 أصلحت alignment المحدود:

- bounded alignment repair: نجح `15/15`.
- عائلات `open_social/followup/topic` عادت للردود الصحيحة داخل الاختبار المحدود.

قرار scaling:

- لا رفع حجم.
- لا runtime switch بعد.
- لا فتح واجهة للمرشح حتى يمر canary طبيعي أوسع.
- التالي Phase 27.60 broader natural-dialogue canary.

## قرار Phase 27.60

Phase 27.60 اختبرت التعميم الطبيعي الأوسع:

- broader canary: فشل `12/30`.
- أقوى فشل في `support=0/6`, `topic=2/6`, `planning=2/6`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة للمرشح.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.61 إصلاح generalization الطبيعي قبل أي توسع.

## قرار Phase 27.61

Phase 27.61 حسّنت canary الأوسع:

- broader canary: تحسن من `12/30` إلى `18/30`.
- `planning=6/6` و`support=6/6`.
- بقيت المشكلة في توازن العائلات: `open_social=2/6`, `followup=3/6`, `topic=1/6`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.62 لإصلاح توازن العائلات قبل أي توسع.

## قرار Phase 27.62–27.63

Phase 27.62 اختبرت توازن العائلات بالعدد فقط:

- broader canary: تراجع إلى `10/30`.
- السبب: ترتيب corpus الكتلي سحب النموذج نحو `open_social` وأضعف support/planning/topic.

Phase 27.63 أصلحت ترتيب curriculum إلى interleaved:

- broader canary: تحسن إلى `26/30`.
- `open_social=6/6`, `planning=6/6`, `support=6/6`, `followup=5/6`, `topic=3/6`.
- الفشل المتبقي: lexical/tokenization collapse في `التعاون` و`الاحترام`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.64 لفحص حماية tokenizer v8 للمصطلحات الموضوعية قبل أي توسع.

## قرار Phase 27.64

Phase 27.64 فحصت فشل `topic` المتبقي دون تدريب:

- `التعاون` في tokenizer v7: `3` قطع وغير محمية.
- `الاحترام` في tokenizer v7: `4` قطع وغير محمية.
- كلاهما كان single-piece في tokenizer v6.

قرار scaling:

- لا رفع حجم.
- لا LM training الآن.
- لا runtime switch.
- لا فتح واجهة.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.65 لتدريب tokenizer v8 فقط ثم bounded topic probe.

## قرار Phase 27.65

Phase 27.65 دربت tokenizer v8 فقط:

- critical terms: `2/2`.
- topic terms: `8/8`.
- boundary roundtrip: `6/6`.
- لا LM training.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.66 bounded LM topic repair على tokenizer v8، ثم broader canary.

## قرار Phase 27.66

Phase 27.66 دربت LM repair محدودًا على tokenizer v8:

- tokenizer: `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
- model size: `SF-10M` فقط.
- steps: `6200`.
- broader canary: `30/30`.
- family summary: followup `6/6`, open_social `6/6`, planning `6/6`, support `6/6`, topic `6/6`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة على checkpoint الجديد.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.67 fresh shadow canary بأسئلة طبيعية غير مرئية؛ فقط إذا نجح fresh canary نراجع runtime switch.

## قرار Phase 27.67

Phase 27.67 اختبرت checkpoint Phase 27.66 بدون تدريب جديد:

- prompts: `50`.
- novelty: `50/50`.
- fresh shadow canary: `30/50`.
- family summary: open_social `4/10`, followup `4/10`, planning `7/10`, support `6/10`, topic `9/10`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة على checkpoint الجديد.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.68 إصلاح موجّه للفشل؛ فشل fresh prompts يعني أن البيانات/الهدف أهم من الحجم الآن.

## قرار Phase 27.68

Phase 27.68 دربت إصلاحًا محدودًا على فشل Phase 27.67:

- model size: `SF-10M`.
- tokenizer: `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
- steps: `5600`.
- known shadow Phase 27.67: `50/50`.
- regression Phase 27.60: `30/30`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة على checkpoint الجديد.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.69 fresh shadow جديد بأسئلة غير مرئية؛ لأن Phase 27.68 رأى فشل 27.67 أثناء التدريب.

## قرار Phase 27.69

Phase 27.69 اختبرت checkpoint Phase 27.68 بدون تدريب جديد:

- prompts: `60`.
- novelty: `60/60`.
- new fresh shadow: `56/60`.
- family summary: followup `12/12`, open_social `8/12`, planning `12/12`, support `12/12`, topic `12/12`.

قرار scaling:

- لا رفع حجم.
- لا runtime switch.
- لا فتح واجهة على checkpoint الجديد.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.70 إصلاح ضيق لـ open_social؛ النجاح الجزئي لا يكفي لتجاوز بوابة runtime.
