# AGENT_INSTRUCTIONS.md

## تعليمات الوكيل قبل أي عمل

أي Agent يدخل مشروع SF.AI يجب أن يقرأ هذه الملفات بهذا الترتيب:

1. [SF_AI_MASTER_GUIDE.md](./SF_AI_MASTER_GUIDE.md)
2. [PHASE_STATUS.md](./PHASE_STATUS.md)
3. [EXECUTION_PLAN.md](./EXECUTION_PLAN.md)
4. [PROJECT_CONSTITUTION.md](./PROJECT_CONSTITUTION.md)
5. [AGENT_HANDOFF.md](./AGENT_HANDOFF.md)

الملفات المتخصصة الأخرى تُقرأ عند لمس مجالها:

- [LANGUAGE_SEGMENTATION.md](./LANGUAGE_SEGMENTATION.md)
- [TOKENIZATION_POLICY.md](./TOKENIZATION_POLICY.md)
- [DATASET_GOVERNANCE.md](./DATASET_GOVERNANCE.md)
- [AGENT_ENGINEERING_RULES.md](./AGENT_ENGINEERING_RULES.md)
- [PROJECT_IDENTITY.md](./PROJECT_IDENTITY.md)
- [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
- [PROJECT_MAP.md](./PROJECT_MAP.md)
- [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)

## أمر أعلى حاكم — Sovereign Practical Acceleration Strategy v2

ابتداءً من Phase 27.78 وما بعدها، هذا الأمر أعلى من أي نمط تجريبي سابق:

- لا تدريب أعمى متكرر.
- لا إعادة تدريب كاملة لكل مشكلة صغيرة.
- لا إصلاح كلمة/عبارة منفردة قبل root-cause diagnosis.
- لا تدوير tokenizer versions بدون قرار هندسي واضح.
- لا benchmark inflation مع تجاهل runtime behavior.
- لا template masking لإخفاء ضعف المولد.

قبل أي تدريب جديد يجب وجود:

```text
ENGINEERING_ROOT_CAUSE_GATE
PHASE27_79_REPAIR_DESIGN_DECISION
```

الحالة الحالية:

- المرحلة الحالية: `Phase 27.79 — Objective/Curriculum/Decoding Repair Design`.
- القرار الحالي: `PHASE27_79_REPAIR_DESIGN_DECISION`.
- التالي: `Phase 27.80 — Repair Gate Encoding and Dry-Run Validation`.
- التدريب: محجوب حتى تُشفّر gates.
- runtime: محجوب تحت `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- `SF-50M`: محجوب؛ لا يفتح إلا عبر `SF-50M JUSTIFIED TRANSITION`.
- Auto-Advance Scaling Mandate: إذا نجحت بوابة الحجم التالي مستقبلًا،
  ينتقل الوكيل تلقائيًا حتى `SF-1B+` دون انتظار موافقة جديدة.

أوزان التشخيص الرسمية الحالية:

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

## بروتوكول التشغيل بالنيابة عن سامي

سامي لا يريد أن يتحول إلى منفّذ خطوات يدوية. لذلك:

- اختبر النظام بنفسك عبر الواجهة أو API.
- احفظ review exports بنفسك إذا كانت مفيدة.
- شغّل أوامر الفحص والبوابات بنفسك.
- رتّب الملفات والتقارير والتوثيق بنفسك.
- لا تطلب من سامي تنفيذ تصدير أو نقل ملفات إذا كان الوكيل يستطيع ذلك محليًا.
- ارفع فقط بعد نجاح الاختبارات وفحص الحساسية.

هذا التفويض لا يلغي الحوكمة:

- لا synthetic LLM data من مصدر خارجي أو مجهول في corpus.
- حوار الوكيل يمكن أن يكون `training_allowed=true` فقط إذا كان `owner-delegated agent-authored` بتفويض سامي، ومع provenance كامل.
- كل export أو corpus record يجب أن يحمل user ownership: `owner_user_id`, `created_by_user_id`, `target_user_id`, و`user_scope`.
- المسار الحالي single-user: `sami-local`; لا تخلط corpus أو review بين مستخدمين.
- لا تنتقل إلى phase لاحقة حتى تمر بواباتها.

## قاعدة البدء

لا تنفذ قبل أن تعرف:

- ما المرحلة الحالية؟
- ما آخر تفويض من سامي؟
- هل الطلب تدريب، crawling، نقل بيانات، أم runtime؟
- هل توجد تغييرات محلية غير مرفوعة؟
- هل توجد ملفات خاصة مستثناة؟
- هل توجد `PHASE27_79_REPAIR_DESIGN_DECISION` وهل طلبك يقع ضمن المسموح بعده؟

## Workflow إلزامي

1. اقرأ الخطة والحالة.
2. افحص git status.
3. اقرأ `docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md`.
4. افحص السيرفر قراءة فقط عبر `make server-status` إذا كان العمل يتعلق بالتشغيل.
5. افهم الفرق بين runtime وtraining.
6. لا تبدأ تدريبًا إلا إذا كان هناك gate صريح بعد 27.78 يسمح به.
7. نفّذ التعديل الأصغر الذي يخدم الطلب.
8. حدّث docs إذا غيّرت بنية أو مسارًا أو phase status.
9. أضف أو حدّث tests.
10. شغّل الاختبارات.
11. افحص الحساسية قبل commit.
12. ارفع فقط إذا نجح العمل.
13. أعط سامي ملخصًا عربيًا واضحًا.

## ممنوعات الوكيل

- لا تبدأ مرحلة خارج الخطة المسجلة بدون توثيق وإذن واضح.
- لا تنقل ملفات بدون تحديث docs.
- لا تضف dependencies بدون توثيق.
- لا تشغّل training خارج الخطة أو بدون provenance/اختبارات.
- لا تشغّل crawler إلا بإذن صريح.
- لا تكسر السيرفر إذا كان يعمل على 8123؛ إذا احتجت restart فاحفظ flags التشغيل وأعده فورًا.
- لا تضع checkpoints خارج `artifacts/`.
- لا تخلط lexicons مع datasets.
- لا تغير `.gitignore` لرفع ملفات خاصة إلا بإذن صريح.
- لا تستخدم نماذج أو tokenizers جاهزة.
- لا تفتح `SF-50M` لأن الردود ضعيفة فقط؛ capacity وزنها الحالي `1%`.
- لا تبدأ tokenizer جديدًا لأن tokenizer وزنها الحالي `4%` فقط، إلا إذا أثبت gate جديد عكس ذلك.
- لا توقف عند حجم نجح gate الخاص به؛ انتقل للحجم التالي تلقائيًا حسب السلم.

## التعامل مع كلمة “التالي”

التفويض الحالي من سامي يسمح بمتابعة المراحل المسجلة والتدريب والاختبارات دون انتظار موافقة جديدة.

إذا كان التالي خارج الخطة أو يستخدم مصدرًا خارجيًا/حساسًا مثل:

- crawling.
- رفع بيانات خاصة.
- تفعيل مجال حساس.

فيجب طلب أو انتظار إذن صريح. أما المراحل المسجلة داخليًا فتستمر مع:

- docs.
- audits.
- tests.
- reports.
- preflight checks.
- secret scan before push.

## قواعد الملفات

عند إضافة ملف جديد اسأل نفسك:

- هل هو runtime code؟ ضعه تحت `apps/` أو `sf_ai/`.
- هل هو corpus؟ ضعه تحت `data/corpus/`.
- هل هو lexicon؟ ضعه تحت `resources/lexicons/`.
- هل هو artifact؟ ضعه تحت `artifacts/`.
- هل هو report؟ ضعه تحت `docs/` أو `data/**/reports/` أو `artifacts/logs/`.
- هل يحتاج README أو CARD؟ أضفه.

## قبل push

نفّذ:

```bash
.venv/bin/python -m pytest tests
git status --short
```

وافحص ألا تظهر:

- `.env`
- secrets
- private keys
- private lexicon payloads
- checkpoints
- training logs
- tokenizer vocab/merges بدون إذن

ثم commit عربي، ثم push.
