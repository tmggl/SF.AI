# Phase 27.53 — Natural Dialogue Diversity Expansion

## الهدف

تنفيذ طلب التوسعة الكبيرة للحوار الطبيعي:

- آلاف الأزواج الفريدة بدل تكرار عشرات قليلة.
- فصحى + سعودي بالتساوي.
- تغطية محادثات الناس العامة: سوالف، متابعة، تنظيم، دعم عام، كتابة ردود، قرارات يومية، تعلم، موضوعات بسيطة.
- لا بيانات خارجية.
- لا pretrained.
- لا حوارات تشغيل/مشروع.
- لا intent/topic keyword lanes في التدريب.

## حجم البيانات

| البند | القيمة |
|------|--------|
| unique train records | `10,540` |
| msa | `5,270` |
| saudi | `5,270` |
| tokenizer | `artifacts/tokenizers/sf_bpe/v6_weak_lane_terms` |
| model | `SF-10M` |
| steps | `18,000` |
| checkpoint | `sf-10m-step18000` |

## النتيجة

**الحالة:** `PARTIAL_NATURAL_DIALOGUE_DIVERSITY_KEEP_PHASE27_47_RUNTIME`

| eval | النتيجة |
|------|---------|
| raw held-out natural | `2/36` |
| open_social | `1/4` |
| open_general | `1/4` |
| decision | `0/4` |
| followup | `0/4` |
| learning | `0/4` |
| planning | `0/4` |
| support | `0/4` |
| topic | `0/4` |
| writing | `0/4` |

## ماذا تعلمنا؟

Phase 27.52 أثبت أن تكرار أمثلة قليلة لا يكفي.

Phase 27.53 أثبت أن ضخ تنوع كبير داخل `SF-10M` بهذه البنية والهدف لا يكفي أيضًا.

المشكلة لم تعد "نحتاج كلمات أكثر" فقط. ظهرت علامات:

- خلط أجزاء من ردود مختلفة.
- فقدان ارتباط prompt بالرد.
- انهيار في writing/decision/support/followup.
- توليد fragments مثل `نقدر نًا` و`أقربدون لف`.

## القرار

لا يتم فتح `sf_10m_phase27_53` في الواجهة.

runtime يبقى على `sf_10m_phase27_47` المحروس.

لا ننتقل إلى Phase 28. ولا نفتح `SF-50M` تلقائيًا بلا بوابة.

## التالي

**Phase 27.54 — Capacity/Objectivity Gate**

الهدف:

- تحديد هل الفشل بسبب حجم `SF-10M` أم بسبب صيغة الهدف/التوكنة/التقييم.
- تجربة أصغر مقارنة مضبوطة قبل أي تكبير كبير.
- إن سُمح بالانتقال إلى `SF-50M` لاحقًا، يكون عبر تقرير يثبت أن السعة هي العامل المحدد لا مجرد جودة البيانات.

## الملفات

- التقرير الآلي: `artifacts/reports/phase27_53_natural_dialogue_diversity_expansion_report.json`
- العينات: `artifacts/samples/phase27_53_natural_dialogue_diversity_expansion.md`
- checkpoint المحلي غير المرفوع: `artifacts/eval/phase27_53_natural_dialogue_diversity_expansion/checkpoints/sf-10m-step18000/state.pt`
- corpus الداخلي المحلي غير المرفوع: `artifacts/eval/phase27_53_natural_dialogue_diversity_expansion/corpus/phase27_19_hygiene_repair_probe.jsonl`
- الأمر: `make phase27-natural-dialogue-diversity-expansion`
