# AGENT_INSTRUCTIONS.md

## تعليمات الوكيل قبل أي عمل

أي Agent يدخل مشروع SF.AI يجب أن يقرأ هذه الملفات بهذا الترتيب:

1. [EXECUTION_PLAN.md](./EXECUTION_PLAN.md)
2. [PHASE_STATUS.md](./PHASE_STATUS.md)
3. [PROJECT_IDENTITY.md](./PROJECT_IDENTITY.md)
4. [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
5. [PROJECT_MAP.md](./PROJECT_MAP.md)
6. [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)
7. [AGENT_HANDOFF.md](./AGENT_HANDOFF.md)

## قاعدة البدء

لا تنفذ قبل أن تعرف:

- ما المرحلة الحالية؟
- ما آخر إذن صريح من سامي؟
- هل الطلب تدريب، crawling، نقل بيانات، أم runtime؟
- هل توجد تغييرات محلية غير مرفوعة؟
- هل توجد ملفات خاصة مستثناة؟

## Workflow إلزامي

1. اقرأ الخطة والحالة.
2. افحص git status.
3. افهم الفرق بين runtime وtraining.
4. نفّذ التعديل الأصغر الذي يخدم الطلب.
5. حدّث docs إذا غيّرت بنية أو مسارًا أو phase status.
6. أضف أو حدّث tests.
7. شغّل الاختبارات.
8. افحص الحساسية قبل commit.
9. ارفع فقط إذا نجح العمل.
10. أعط سامي ملخصًا عربيًا واضحًا.

## ممنوعات الوكيل

- لا تبدأ مرحلة غير مصرح بها.
- لا تنقل ملفات بدون تحديث docs.
- لا تضف dependencies بدون توثيق.
- لا تشغّل training إلا بإذن صريح.
- لا تشغّل crawler إلا بإذن صريح.
- لا تضع checkpoints خارج `artifacts/`.
- لا تخلط lexicons مع datasets.
- لا تغير `.gitignore` لرفع ملفات خاصة إلا بإذن صريح.
- لا تستخدم نماذج أو tokenizers جاهزة.

## التعامل مع كلمة “التالي”

كلمة “التالي” وحدها لا تكفي لبدء مرحلة عالية الأثر.

إذا كان التالي:

- تدريب tokenizer.
- تدريب LM.
- crawling.
- رفع بيانات خاصة.
- تفعيل مجال حساس.

فيجب طلب أو انتظار إذن صريح. يمكن تنفيذ تجهيزات آمنة فقط:

- docs.
- audits.
- tests.
- reports.
- preflight checks.

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
