# SCALING_STRATEGY.md

## SF.AI — Progressive Scaling Strategy

**Status:** governance rule, no training started
**Language track:** Arabic MSA + Saudi only
**Lexicon track:** Saudi Seed v1 + governed MSA/Saudi corpus

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

## السلم الرسمي للأحجام

| الترتيب | الحجم | متى يُنظر فيه؟ |
|---------|------|----------------|
| 1 | `SF-10M` | إثبات pipeline وتدريب جودة أولي |
| 2 | `SF-50M` | بعد نجاح 10M وجود corpus أقوى |
| 3 | `SF-120M` | بعد نجاح 50M في الحوار والتقييم |
| 4 | `SF-350M` | بعد corpus كبير وتقييم متعدد الأدوار |
| 5 | `SF-700M` | بعد ثبات runtime وموارد واضحة |
| 6 | `SF-1B+` | فقط بعد نجاح كل ما سبق، لا كقفزة مبكرة |

لا يوجد مسار رسمي يقفز من `SF-10M` إلى `3B` أو `1B+` مباشرة.

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
