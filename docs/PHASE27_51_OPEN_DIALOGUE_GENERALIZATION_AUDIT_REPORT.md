# Phase 27.51 — Open-Dialogue Generalization Audit

## الهدف

اختبار الفرق بين:

- مولد يرد داخل مسارات محروسة/ضيقة.
- نموذج حواري طبيعي لا يحتاج قالبًا ولا كلمة مفتاحية ولا topic lane محفوظ.

هذه المرحلة لا تدرب نموذجًا جديدًا. دورها منع الوهم: لا نعتبر `SF-10M Phase 27.47` حوارًا ذكيًا عامًا لمجرد أنه يجيب بعض الأسئلة السهلة.

## النتيجة

**الحالة:** `FAILED_OPEN_DIALOGUE_GENERALIZATION_AUDIT_TRAINING_REQUIRED`

| المسار | النجاح |
|--------|--------|
| Live API generator-only | `3/22` |
| Raw checkpoint بلا intent/topic conditioning | `3/22` |
| Raw natural prompts فقط | `1/20` |

## ماذا كشف الاختبار؟

- الواجهة ما زالت صادقة: لا تعرض قوالب، والحالات غير المدعومة ترجع `generator_blocked`.
- checkpoint نفسه لا يعمم بعد على الحوار الطبيعي المفتوح.
- كثير من الردود الخام تسقط في جمل محفوظة أو مخلوطة مثل:
  - `ابدأ بالأهم ثم انتقل للي بعده.`
  - `الله يعافيك، حاضر بأي وقت.`
  - خلط تعريفات مثل الصداقة/الهدوء داخل سؤال مختلف.
- نجاح keyword lane أو topic lane لا يكفي لاعتبار النموذج ذكيًا.

## القرار

لا ننتقل إلى `SF-50M` ولا Phase 28.

الخطوة التالية:

**Phase 27.52 — Natural Dialogue Objective Repair**

الهدف أن يتعلم النموذج محادثة طبيعية قصيرة:

- متابعة الكلام: `طيب ليه؟`, `يعني كيف؟`, `كمل`.
- سوالف عامة: `سولف معي`, `هات موضوع خفيف`.
- ردود اجتماعية غير محفوظة.
- شرح بسيط مع أمثلة.
- دعم نفسي يومي غير طبي.
- تخطيط بسيط بصيغ متعددة.

## القاعدة الجديدة لهذه المرحلة وما بعدها

أي بوابة حوار مولد لا تُقبل إذا كانت تعتمد فقط على:

- exact prompts.
- keyword lanes.
- topic whitelist.
- required term فقط بدون ملاءمة سياقية.

يجب وجود اختبار raw/unconditioned أو held-out natural prompts يثبت أن checkpoint تعلم نمط الحوار لا نصًا محفوظًا.

## الملفات

- التقرير الآلي: `artifacts/reports/phase27_51_open_dialogue_generalization_audit.json`
- العينات: `artifacts/samples/phase27_51_open_dialogue_generalization_audit.md`
- الأمر: `make phase27-open-dialogue-generalization-audit`
