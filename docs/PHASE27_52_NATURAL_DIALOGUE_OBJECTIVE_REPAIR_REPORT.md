# Phase 27.52 — Natural Dialogue Objective Repair

## الهدف

رفع التدريب بشكل آمن داخل `SF-10M` للوصول أسرع بدون كسر استراتيجية التدرج:

- لا تكبير حجم النموذج.
- لا `SF-50M`.
- لا بيانات خارجية.
- لا pretrained.
- لا intent/topic keyword lanes في التدريب.
- تدريب أطول داخل نفس الحجم: `9200` خطوة بدل `4600` في Phase 27.47.

## النتيجة

**الحالة:** `PARTIAL_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_KEEP_PHASE27_47_RUNTIME`

| المقياس | القيمة |
|---------|--------|
| model | `SF-10M` |
| tokenizer | `artifacts/tokenizers/sf_bpe/v6_weak_lane_terms` |
| checkpoint | `sf-10m-step9200` |
| train records | `6400` |
| unique train pairs | `40` |
| steps | `9200` |
| multiplier vs Phase 27.47 | `2.00x` |
| held-out natural eval | `5/20` |

## ماذا تحسن؟

Phase 27.51 raw natural كان `1/20`.

Phase 27.52 وصل إلى `5/20`:

- topic: `3/4`
- planning: `2/4`
- followup: `0/4`
- open_social: `0/4`
- support: `0/4`

## ماذا يعني ذلك؟

زيادة الخطوات وحدها ليست كافية. التدريب وصل loss شبه صفري، لكن النموذج ما زال:

- يخلط جملًا من categories مختلفة.
- ينجح أكثر في الموضوعات الواضحة.
- يفشل في السوالف الطبيعية والمتابعة والدعم.
- يحتاج بيانات أكثر تنوعًا وهدفًا حواريًا أفضل، لا مجرد خطوات أكثر.

## القرار

لا يتم فتح `sf_10m_phase27_52` في الواجهة.

runtime يبقى على `sf_10m_phase27_47` المحروس، مع حقيقة واضحة:

> Phase 27.52 حسّن المؤشر لكنه لم يصل إلى حوار مقنع.

## التالي

**Phase 27.53 — Natural Dialogue Diversity Expansion**

الأولوية:

- رفع عدد الأزواج الفريدة بدل تكرار نفس الأربعين زوجًا.
- تغطية follow-up/open-social/support بعبارات كثيرة.
- تقليل الخلط بين planning/support/topic.
- إعادة تقييم raw natural بلا intent/topic conditioning.

## الملفات

- التقرير الآلي: `artifacts/reports/phase27_52_natural_dialogue_objective_repair_report.json`
- العينات: `artifacts/samples/phase27_52_natural_dialogue_objective_repair.md`
- checkpoint المحلي غير المرفوع: `artifacts/eval/phase27_52_natural_dialogue_objective_repair/checkpoints/sf-10m-step9200/state.pt`
- الأمر: `make phase27-natural-dialogue-objective-repair`
