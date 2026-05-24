# Phase 27.69 New Fresh Shadow Canary

## open_social_01 — FAIL

- family: open_social
- prompt: وش رايك نسولف شوي
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_02 — PASS

- family: open_social
- prompt: حدثني عن شيء بسيط
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_03 — FAIL

- family: open_social
- prompt: خلنا ناخذ كلام خفيف
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_04 — PASS

- family: open_social
- prompt: افتح موضوعًا هادئًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_05 — FAIL

- family: open_social
- prompt: عطني سوالف بسيطة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_06 — PASS

- family: open_social
- prompt: أريد كلامًا وديًا قصيرًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_07 — FAIL

- family: open_social
- prompt: تكلم معي عن شي لطيف
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_08 — PASS

- family: open_social
- prompt: اختر حديثًا خفيفًا بيننا
- response: نختار موضوعًا خفيفًا ونتحدث عنه ببساطة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_09 — FAIL

- family: open_social
- prompt: ودي بموضوع سوالف
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_10 — FAIL

- family: open_social
- prompt: ابدأ محادثة سهلة
- response: نبدأ محالطيف: ما المكان الهدوءاتطيع أن شيء أراحك اليوم؟
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## open_social_11 — FAIL

- family: open_social
- prompt: هات كلام يمشي الوقت
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_12 — PASS

- family: open_social
- prompt: لنختر موضوعًا صغيرًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_01 — FAIL

- family: followup
- prompt: وضح لي مقصدك اكثر
- response: يمكننا أن تجأراحك اليوم؟ الهدوء؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_02 — FAIL

- family: followup
- prompt: أعد شرح النقطة ببساطة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — FAIL

- family: followup
- prompt: ما فهمت وش تبي تقول
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_04 — FAIL

- family: followup
- prompt: ما الخطوة بعد هذا الشرح
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_05 — FAIL

- family: followup
- prompt: طيب كمل من هنا
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_06 — FAIL

- family: followup
- prompt: اجعل الفكرة أوضح
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_07 — FAIL

- family: followup
- prompt: يعني ابدا من وين
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_08 — FAIL

- family: followup
- prompt: فسر كلامك مرة أخرى
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_09 — FAIL

- family: followup
- prompt: وش قصدك بالضبط
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_10 — FAIL

- family: followup
- prompt: اختصر لي المعنى
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_11 — FAIL

- family: followup
- prompt: ما وصلتني الفكرة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_12 — FAIL

- family: followup
- prompt: تابع من آخر جملة
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_01 — FAIL

- family: planning
- prompt: ابي ارتب اولوياتي اليوم
- response: يمكننا بسيطة ك اليوم؟ ما أكثر شيء أراحك اليوم؟
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_02 — FAIL

- family: planning
- prompt: ساعدني أرتب أعمالي
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_03 — FAIL

- family: planning
- prompt: من وين ابدا اذا المهام كثيره
- response: يمكننا أن نتكلم عن عادة بسيطة ابحديث تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_04 — FAIL

- family: planning
- prompt: كيف أقسم وقتي اليوم
- response: يمكننا أن يعمل الناس بالكلام ؟
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_05 — FAIL

- family: planning
- prompt: ابي جدول بسيط لبدايتي
- response: يمكننا أن نتكلم عن عادة بسيطة ابحديث تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_06 — FAIL

- family: planning
- prompt: أحتاج ترتيبًا سريعًا
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_07 — FAIL

- family: planning
- prompt: وش اسوي بالمهام المتراكمة
- response: يمكننا أن تجلس فيه عندما تريد الهدوء؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_08 — FAIL

- family: planning
- prompt: ضع لي بداية واضحة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: advice_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:advice_mismatch

## planning_09 — PASS

- family: planning
- prompt: خلني ابدأ بدون تشتت
- response: ابدأ بخطوة واحدة واضحة حتى يقل التشتت.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_10 — FAIL

- family: planning
- prompt: كيف أختصر قائمة عملي
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_11 — FAIL

- family: planning
- prompt: ساعدني احدد اول شي
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_12 — FAIL

- family: planning
- prompt: أريد تنظيمًا بسيطًا للمهام
- response: يمكننا أن تجلس فيه عندما تريد الهدوء؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_01 — FAIL

- family: support
- prompt: صدري ضايق وابغى اهدأ
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_02 — FAIL

- family: support
- prompt: أشعر بتوتر وأريد طمأنينة
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_03 — FAIL

- family: support
- prompt: ابي كلمة تهون علي
- response: نستطيع أن نتحدث عن شيء أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_04 — FAIL

- family: support
- prompt: أحتاج هدوءًا قبل أن أبدأ
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_05 — FAIL

- family: support
- prompt: قلقي زايد شوي
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## support_06 — FAIL

- family: support
- prompt: كيف أهدئ نفسي الآن
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## support_07 — FAIL

- family: support
- prompt: حاس بتوتر ومحتاج اروق
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_08 — FAIL

- family: support
- prompt: طمئنّي بجملة قصيرة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## support_09 — FAIL

- family: support
- prompt: ابي اهدى من التفكير
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_10 — FAIL

- family: support
- prompt: أنا متوتر من البداية
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: True
- reason: guard:support_mismatch

## support_11 — PASS

- family: support
- prompt: محتاج كلام يخفف علي
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_12 — FAIL

- family: support
- prompt: أريد راحة قصيرة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## topic_01 — FAIL

- family: topic
- prompt: ما معنى الوفاء للناس
- response: نسان على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_02 — FAIL

- family: topic
- prompt: التعاون وين يبان
- response: نستطيع أن نتحدث عن شيء أراحك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_03 — FAIL

- family: topic
- prompt: اشرح الصبر في موقف صعب
- response: نسان على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش اثره
- response: نستطيع أراحك أو خفف عنك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_05 — FAIL

- family: topic
- prompt: عرّف الهدوء بعبارة بسيطة
- response: نستطيع أن نتحدث عن شيء أراحك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_06 — FAIL

- family: topic
- prompt: الصدق ليه مهم
- response: يمكننا أن تقول الحقيقة وتلتزم بها.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_07 — FAIL

- family: topic
- prompt: ما جوهر الصداقة
- response: يمكننا أن يعمل الناس بالكلام والتصرف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_08 — FAIL

- family: topic
- prompt: الشجاعة كيف تكون
- response: نستطيع أن نتحدث عن شيء
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_09 — FAIL

- family: topic
- prompt: أعطني مثالًا على التعاون
- response: نستطيع أن يعمل الناس معًا عن عادة بسيطة ك اليوم.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_10 — FAIL

- family: topic
- prompt: وش يعني الوفاء مع الاصحاب
- response: يمكننا أن نتكلم عن عادة بسيطة اتضلهدف مشعن شيء أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_11 — FAIL

- family: topic
- prompt: ما قيمة الاحترام
- response: يمكننا أن بالكلام والتصرف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_12 — FAIL

- family: topic
- prompt: الصبر متى نحتاجه
- response: يمكننا أن تقول الحقيقة بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing
