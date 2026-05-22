# PHASE19_READINESS_REPORT.md

## SF.AI — Phase 19 SF-50M Readiness Gate

**Journey:** Phase 19 / 30
**Status:** not ready for SF-50M training
**Language track:** Arabic MSA + Saudi only
**Lexicon track:** Saudi Seed v1 + `safety_terms.yaml`

---

## القرار الهندسي

Phase 19 لا يبدأ تدريب `SF-50M` الآن.

السبب ليس إذن المستخدم؛ سامي أعطى تفويضًا عامًا للمتابعة. السبب هندسي:

- corpus الحالي صغير جدًا قياسًا على SF-50M: `255` سجلًا تدريبيًا فقط.
- الحد الأدنى العملي لهذه القفزة: `5000` سجل محكوم على الأقل.
- corpus الحالي لم يعد يفتقد `msa`، لكنه ما زال بعيدًا عن العدد والتوازن المطلوبين: `msa=200`, `saudi=55`.
- Phase 16 يسمح بالتجربة المحلية، لكنه يوضح أن النموذج الخام يحتاج بيانات أكثر.

---

## ما أُنجز

- أضيفت بوابة read-only:
  - `make phase19-readiness`
  - `GET /system/phase19-readiness`
- أضيف `sf_ai/training/phase19_readiness.py`.
- أضيف `scripts/phase19_readiness.py`.
- أضيفت اختبارات Phase 19.
- لم يبدأ أي تدريب جديد ولم تُكتب checkpoints.

---

## مختبر سامي المحلي

هذا مسار اختبار وتطوير مستمر لسامي:

- يمكن لسامي اختبار المولد الخام من الواجهة.
- يمكن تفعيل lab mode للرسائل غير الحساسة عبر:
  - `SF_ENABLE_NATIVE_GENERATOR=true`
  - `SF_NATIVE_GENERATOR_EXPERIMENTAL=true`
  - `SF_LAB_GENERATION_FOR_NON_SENSITIVE=true`
- المجالات غير الحساسة التي لم تُفعَّل بعد يمكن أن تمر إلى مولد الشات في المختبر.
- المجالات الحساسة تبقى safety-first كقرار هندسي أثناء بناء gates المتخصصة.

---

## المخرجات الحالية

متوقع من `make phase19-readiness`:

```text
status: NOT_READY_EXPAND_CORPUS_FIRST
can_start_training: false
training_records: 255
min_training_records: 5000
blockers:
  - corpus_too_small_for_sf50m
```

---

## الخطوة الصحيحة التالية

استخدم Phase 22 لتوسيع corpus مباشرة. المسار الأساسي الآن أن يؤلف الوكيل الدفعات، يراجعها، ويعتمدها بتفويض سامي الموثق، ثم يشغل audit/tests قبل الرفع. مسار review من الواجهة يبقى اختياريًا فقط:

```bash
make phase22-next-batch
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_<batch>.jsonl
make corpus-audit
make phase22-readiness
make phase19-readiness
```

عند بلوغ corpus كافٍ ومتوازن، يبدأ تدريب `SF-50M` من الصفر بأوزان سيادية فقط.
