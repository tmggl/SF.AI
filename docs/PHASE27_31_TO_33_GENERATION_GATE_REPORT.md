# Phase 27.31–27.33 — Natural Generation Gate Report

## الهدف

رفع مولد `SF-10M` من نجاح جزئي في Phase 27.30 (`16/18`) إلى نجاح معملي كامل على بوابات توليد محلية، بدون:

- استخدام pretrained weights أو tokenizer خارجي.
- إدخال بيانات تشغيلية/هندسية داخل corpus الحوار.
- نسخ أسئلة shadow الجديدة داخل التدريب.
- فتح runtime للواجهة قبل تصميم trial محروس.

## المسار

| Phase | الهدف | النتيجة | القرار |
|---|---|---:|---|
| Phase 27.31 | Natural intent/topic dataset للشكر وسؤال الحال | natural shadow `20/20`, micro `32/32`, لكن fresh mixed `15/18` | runtime محجوب |
| Phase 27.32 | Balanced natural calibration للتعريف/التخطيط/الدعم السعودي | definition `6/6`, calibration `12/12`, لكن fresh mixed `16/18` وmicro `29/32` | runtime محجوب |
| Phase 27.33 | Advice + micro stabilization | كل البوابات مرت | جاهز لتصميم guarded runtime trial |

## نتيجة Phase 27.33

Checkpoint:

```text
artifacts/eval/phase27_33_advice_micro_stabilization/checkpoints/sf-10m-step9800
```

النتائج:

| Gate | النتيجة |
|---|---:|
| heldout_27_25 | `16/16` |
| shadow_27_27 | `16/16` |
| definition_shadow_27_29 | `6/6` |
| fresh_mixed_shadow_27_30 | `18/18` |
| natural_shadow_27_31 | `20/20` |
| calibration_shadow_27_32 | `12/12` |
| advice_shadow_27_33 | `4/4` |
| micro_probe_regression | `32/32` |
| prompt leakage | none |

## ماذا يعني النجاح؟

يعني أن `SF-10M` بدأ يعطي ردودًا قصيرة مفهومة داخل نطاقات محدودة:

- تحية.
- سؤال حال.
- تعريفات بسيطة: التعاون، الاحترام، القراءة.
- نصيحة قصيرة.
- ترتيب يوم بسيط.
- دعم/تهدئة خفيفة.
- شكر.

## ماذا لا يعني النجاح؟

لا يعني أن المولد صار مفتوحًا للواجهة افتراضيًا. لا يزال المطلوب في Phase 27.34:

- تصميم guarded runtime trial.
- تفعيل محدود باختيار صريح.
- fallback تلقائي إلى templates عند فشل guard.
- إظهار metadata واضح: هل الرد من template أم من `SF-10M`.
- قياس من الواجهة قبل أي تعميم.

## القرار

Phase 27.33 يرفع الحالة من:

```text
runtime blocked
```

إلى:

```text
ready for guarded runtime trial design
```

لكن لا يسمح بـ `SF-50M` ولا Phase 28 حتى تثبت جودة runtime الفعلية من الواجهة.
