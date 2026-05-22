# AGENT_INSTRUCTIONS.md

## تعليمات الوكيل قبل أي عمل

أي Agent يدخل مشروع SF.AI يجب أن يقرأ هذه الملفات بهذا الترتيب:

1. [EXECUTION_PLAN.md](./EXECUTION_PLAN.md)
2. [PHASE_STATUS.md](./PHASE_STATUS.md)
3. [PROJECT_CONSTITUTION.md](./PROJECT_CONSTITUTION.md)
4. [LANGUAGE_SEGMENTATION.md](./LANGUAGE_SEGMENTATION.md)
5. [TOKENIZATION_POLICY.md](./TOKENIZATION_POLICY.md)
6. [DATASET_GOVERNANCE.md](./DATASET_GOVERNANCE.md)
7. [AGENT_ENGINEERING_RULES.md](./AGENT_ENGINEERING_RULES.md)
8. [PROJECT_IDENTITY.md](./PROJECT_IDENTITY.md)
9. [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
10. [PROJECT_MAP.md](./PROJECT_MAP.md)
11. [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)
12. [AGENT_HANDOFF.md](./AGENT_HANDOFF.md)

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
- لا تنتقل إلى phase لاحقة حتى تمر بواباتها.

## قاعدة البدء

لا تنفذ قبل أن تعرف:

- ما المرحلة الحالية؟
- ما آخر تفويض من سامي؟
- هل الطلب تدريب، crawling، نقل بيانات، أم runtime؟
- هل توجد تغييرات محلية غير مرفوعة؟
- هل توجد ملفات خاصة مستثناة؟

## Workflow إلزامي

1. اقرأ الخطة والحالة.
2. افحص git status.
3. افحص السيرفر قراءة فقط عبر `make server-status` إذا كان العمل يتعلق بالتشغيل.
4. افهم الفرق بين runtime وtraining.
5. نفّذ التعديل الأصغر الذي يخدم الطلب.
6. حدّث docs إذا غيّرت بنية أو مسارًا أو phase status.
7. أضف أو حدّث tests.
8. شغّل الاختبارات.
9. افحص الحساسية قبل commit.
10. ارفع فقط إذا نجح العمل.
11. أعط سامي ملخصًا عربيًا واضحًا.

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
