# CORPUS_OPERATIONAL_FILTER_REPORT.md

## SF.AI — Operational/Internal Corpus Filter

**Journey:** Phase 27 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Status:** `COMPLETED_POLICY_APPLIED_TO_CURRENT_CORPUS`

## القرار

بناءً على توجيه سامي، أصبح ممنوعًا نهائيًا إدخال أي حوار تشغيلي أو هندسي
أو خاص بإدارة مشروع SF.AI داخل corpus الحوار العامة أو أي corpus تدريبية
مستقبلية.

أي سجل من هذا النوع يصنّف:

```text
training_forbidden_operational_internal_dialogue
```

ولا يحفظ كـ review-only ولا يحول لاحقًا إلى تدريب.

## ما يمنعه الفلتر

- أوامر مثل: `التالي`, `اكمل`, `ارفع`.
- مصطلحات داخلية مثل: `phase`, `gates`, `corpus`, `tokenizer`, `pytest`,
  `commit`, `readiness`.
- حوار عن إدارة المشروع أو تشغيل الوكيل.
- agent workflow patterns.
- Persona خاصة بسامي أو طريقة إدارته للمشروع.
- نقاشات هندسية داخلية عن النموذج أو التدريب أو القوالب.

## ما نريده بدل ذلك

- حوار بشري طبيعي عام.
- سوالف عادية.
- فصحى طبيعية.
- سعودي طبيعي.
- أسئلة وأجوبة شائعة.
- شرح يومي عام.
- تفاعل طبيعي غير هندسي.

## نتيجة تنظيف corpus الحالية

```text
records_before_cleaning : 1550
records_after_cleaning  : 643
records_removed_total   : 907
msa_after_cleaning      : 299
saudi_after_cleaning    : 344
gold_after_cleaning     : 31
silver_after_cleaning   : 612
```

## أدوات الحماية المضافة

- `detect_training_forbidden_operational_terms` داخل `sf_ai/datasets/corpus_governance.py`.
- `scripts/filter_training_forbidden_corpus.py` لحذف السجلات المخالفة من JSONL.
- `scripts/sanitize_corpus_provenance.py` لتنظيف provenance من ألفاظ phase/agent.
- مولدات Phase 27 القديمة (`phase27_write_expansion_batch_001/002/003.py`)
  عُطلت عند التشغيل لأنها قد تعيد إنتاج نمط تشغيلي ممنوع.
- `prepare_dialogue_batch` يرفض تحويل review exports التشغيلية إلى training.
- `POST /chat/review-export` يرفض حفظ review export يحتوي هذا النمط.
- اختبارات جديدة في:
  - `tests/test_corpus_governance.py`
  - `tests/test_dialogue_batch_preparation.py`
  - `tests/test_chat_ui.py`

## التحقق بعد التنظيف الأصلي

```text
corpus-audit        : 643/643 training-ready, issues=0
tokenization-audit  : 30/30 protected terms covered
phase26-readiness   : NOT_READY, corpus below 5000
phase27 eval        : 19/19, remaining=4357, batches=9
```

## الحالة بعد Batch 004 الطبيعي

أضيفت دفعة طبيعية جديدة بحجم `1500` سجل (`750` فصحى + `750` سعودي).
بعد تشغيل الفلتر مرة أخرى لم يُحذف أي سجل من الدفعة الجديدة:

```text
corpus-audit        : 2143/2143 training-ready, issues=0
msa                 : 1049
saudi               : 1094
phase27 eval        : 19/19, remaining=2857, batches=2 عند batch_size=1500
```

## القرار التالي

Phase 27 تستمر، لكن الدفعات القادمة يجب أن تكون **طبيعية فقط**. لا تُستخدم
Batch 001/002/003 كأسلوب تأليف قادم؛ الطريق الصحيح هو الاستمرار على
دفعات طبيعية كبيرة مثل Batch 004: سوالف وأسئلة يومية عامة بلا أي إدارة
مشروع أو مصطلحات هندسية داخل الحوار.
