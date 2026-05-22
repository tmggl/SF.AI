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
