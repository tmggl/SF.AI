# PHASE19_READINESS_REPORT.md

## SF.AI — Phase 19 SF-50M Readiness Gate

**Journey:** Phase 19 / 20
**Status:** not ready for SF-50M training
**Language track:** Arabic MSA + Saudi only
**Lexicon track:** Saudi Seed v1 + `safety_terms.yaml`

---

## القرار

Phase 19 لا يبدأ تدريب `SF-50M` الآن.

السبب ليس إذن المستخدم؛ سامي أعطى تفويضًا عامًا للمتابعة. السبب هندسي:

- corpus الحالي صغير جدًا: `30` سجل تدريبي فقط.
- الحد الأدنى العملي لهذه القفزة: `5000` سجل محكوم على الأقل.
- corpus الحالي سعودي فقط ويفتقد `msa`.
- Phase 16 يسمح بالتجربة المحلية، لكنه لا يثبت جودة نموذج يومية.

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

## وضع مختبر سامي المحلي

السيرفر المحلي ليس منتجًا عامًا. لذلك:

- يمكن لسامي اختبار المولد الخام من الواجهة.
- يمكن تفعيل lab mode للرسائل غير الحساسة عبر:
  - `SF_ENABLE_NATIVE_GENERATOR=true`
  - `SF_NATIVE_GENERATOR_EXPERIMENTAL=true`
  - `SF_LAB_GENERATION_FOR_NON_SENSITIVE=true`
- المجالات غير الحساسة التي لم تُفعَّل بعد يمكن أن تمر إلى مولد الشات في المختبر.
- المجالات الحساسة تبقى safety-first حتى لا ينتج النموذج الخام نصًا عالي المخاطر بلا gate.

---

## المخرجات الحالية

متوقع من `make phase19-readiness`:

```text
status: NOT_READY_EXPAND_CORPUS_FIRST
can_start_training: false
training_records: 30
min_training_records: 5000
blockers:
  - corpus_too_small_for_sf50m
  - missing_required_msa_or_saudi_balance
```

---

## الخطوة الصحيحة التالية

استخدم Phase 18 data loop لتوسيع corpus:

1. اختبر من الواجهة.
2. صدّر المحادثة بزر `تصدير`.
3. راجع الملف.
4. حضّره:

```bash
make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v1.jsonl --quality silver --dialect saudi --training-allowed"
```

5. شغّل:

```bash
make corpus-audit
make phase19-readiness
```

عند بلوغ corpus كافٍ ومتوازن، يبدأ تدريب `SF-50M` من الصفر بأوزان سيادية فقط.
