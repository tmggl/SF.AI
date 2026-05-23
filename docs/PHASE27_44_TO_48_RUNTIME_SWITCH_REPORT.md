# Phase 27.44–27.48 — Runtime Switch Report

## الخلاصة

هذه السلسلة أصلحت مسار `SF-10M` التجريبي من دون تكبير النموذج:

- Phase 27.44: tokenizer v6 + curriculum repair؛ النتيجة `11/16`، لا runtime switch.
- Phase 27.45: semantic topic balance؛ النتيجة `9/16`، لا runtime switch.
- Phase 27.46: core dialogue stabilization؛ النتيجة `14/16`، فشل فقط في `الوفاء/الشجاعة`.
- Phase 27.47: new-topic conditioning repair؛ النتيجة `16/16` offline.
- Phase 27.48: guarded runtime switch؛ النتيجة `19/19` live API.

## القرار

`generator_trial=true` يستخدم الآن:

- generator: `sf_10m_phase27_47`
- tokenizer: `artifacts/tokenizers/sf_bpe/v6_weak_lane_terms`
- checkpoint: `artifacts/eval/phase27_47_new_topic_conditioning_repair/checkpoints/sf-10m-step4600`

الافتراضي ما زال `template`، والمولد لا يعمل إلا عند تفعيل زر `مولّد تجريبي`.

## ما يمكن اختباره

من الواجهة فعّل زر `مولّد تجريبي` ثم جرّب:

- `وش اخبارك`
- `علومك`
- `مشكور`
- `نظم وقتي`
- `ابي ارتب اولوياتي`
- `ما معنى الوفاء`
- `اشرح الشجاعة`
- `ما معنى الصداقة`
- `الصدق وش يعني`
- `انا متوتر`

هذه ليست مرحلة ذكاء عام. هي أول نواة حوار مولدة ومحمية داخل نطاق صغير، والمرحلة التالية هي Phase 27.49 لتوسيع اختبارات الواجهة الحية.
