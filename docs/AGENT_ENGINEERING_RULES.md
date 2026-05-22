# AGENT_ENGINEERING_RULES.md

## قواعد الوكلاء الهندسية واللغوية

هذه نسخة عملية مختصرة لأي Agent قبل العمل.

## اقرأ أولًا

1. [EXECUTION_PLAN.md](./EXECUTION_PLAN.md)
2. [PHASE_STATUS.md](./PHASE_STATUS.md)
3. [PROJECT_CONSTITUTION.md](./PROJECT_CONSTITUTION.md)
4. [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
5. [LANGUAGE_SEGMENTATION.md](./LANGUAGE_SEGMENTATION.md)
6. [TOKENIZATION_POLICY.md](./TOKENIZATION_POLICY.md)
7. [DATASET_GOVERNANCE.md](./DATASET_GOVERNANCE.md)
8. [PROJECT_MAP.md](./PROJECT_MAP.md)
9. [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)

## لا تفعل

- لا تنفذ مرحلة غير مصرح بها.
- لا تبدأ Phase 12 إلا بإذن صريح.
- لا تشغّل tokenizer training من كلمة “التالي”.
- لا تغير tokenizer rules بدون توثيق.
- لا تكسر protected terms.
- لا تضف dependency بلا justification.
- لا تنقل corpus إلى resources.
- لا تنقل lexicon إلى corpus بدون conversion وprovenance.
- لا تضف لهجات runtime/training غير `msa` و`saudi` بلا قرار صريح.
- لا تستخدم pretrained بأي شكل.

## عند تعديل tokenization

قبل أي تعديل:

- اقرأ `docs/TOKENIZATION_POLICY.md`.
- اقرأ `resources/tokenization/tokenization_rules.yaml`.
- راجع `protected_terms_saudi.txt`.
- راجع `preferred_merges.txt`.

بعد أي تعديل:

- حدّث docs.
- أضف tests.
- شغّل pytest.
- اذكر في commit سبب التعديل.

## عند تعديل datasets

- تحقق من `source/license/quality/training_allowed`.
- شغّل `make corpus-audit`.
- لا تبدأ training.
- لا ترفع corpus خاص إلا إذا كان مقصودًا ومصرحًا.

## عند إضافة dependency

وثّق:

- لماذا نحتاجها.
- هل تحمل pretrained data/model؟
- هل تحتاج شبكة؟
- هل تعمل offline؟
- أين تُستخدم؟

إذا فيها pretrained أو model download: ارفضها أو اطلب قرارًا صريحًا.

## قبل الرفع

```bash
.venv/bin/python -m pytest tests
make corpus-audit
make source-inventory
git status --short
```

ثم افحص الحساسية:

- لا `.env`.
- لا private keys.
- لا checkpoints.
- لا full private lexicon payloads.
- لا tokenizer vocab/merges بدون إذن.

## تشغيل السيرفر

لا تكسر السيرفر أثناء العمل.

قبل أي محاولة تشغيل:

```bash
make server-status
```

إذا كان المنفذ `8123` يستمع و`/health` يرد، اتركه يعمل ولا تعمل restart.

إذا كان متوقفًا فعلًا، استخدم:

```bash
make server-start
```

هذا الأمر يبدأ السيرفر داخل `screen` فقط إذا لم يكن المنفذ يعمل.

ممنوع استخدام:

- `pkill`
- kill PID
- restart

إلا إذا طلب سامي ذلك صراحة، أو إذا كان السيرفر متوقفًا أصلًا ولا يوجد listener على 8123.
