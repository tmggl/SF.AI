# Phase 27.43 — Guarded Data-Backed Expansion

## الهدف

إضافة تدريب صغير موجه للمسارات الضعيفة التي كشفها Phase 27.42، دون تكبير النموذج ودون تبديل runtime إلا إذا اجتاز المرشح البوابة كاملة.

## ما حدث

- استُخدم tokenizer v5:
  - `artifacts/tokenizers/sf_bpe/v5_topic_terms`
- دُرّب مرشح جديد:
  - `sf_10m_phase27_43`
  - checkpoint محلي: `artifacts/eval/phase27_43_guarded_data_backed_expansion/checkpoints/sf-10m-step4800`
- أضيفت أمثلة موجهة لمسارات:
  - `وش اخبارك`
  - `علومك`
  - `مشكور`
  - `تسلم`
  - `نظم وقتي`
  - `ابي ارتب اولوياتي`
  - `الوفاء`
  - `الشجاعة`

## النتيجة

```text
PARTIAL_GUARDED_DATA_BACKED_EXPANSION_KEEP_PHASE27_40_RUNTIME
10/16 passed
```

- weak_lane: `4/6`
- regression: `6/8`
- new_topic: `0/2`

## التشخيص

المرشح الجديد غير مستقر:

- بعض social prompts انجرفت إلى تعريفات.
- `الوفاء` و`الشجاعة` انهارت إلى موضوعات قديمة مثل `الصدق/التنظيم`.
- هذا يعني أن إضافة أمثلة فقط ليست كافية؛ نحتاج tokenizer/curriculum repair منفصل قبل فتح موضوعات جديدة.

## القرار

- لا runtime switch.
- الواجهة تبقى على `sf_10m_phase27_40` داخل `generator_trial=true`.
- لا `SF-50M`.
- لا Phase 28.

## التالي

Phase 27.44 — Tokenizer/Curriculum Repair for Weak-Lane Stability.
