# Phase 27.69 New Fresh Shadow Canary

## open_social_01 — FAIL

- family: open_social
- prompt: وش رايك نسولف شوي
- response: ابدأ بالأهم، وبعد ما تخلواترك الباقي لوقت لاحق.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_02 — FAIL

- family: open_social
- prompt: حدثني عن شيء بسيط
- response: حدد دة راحة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_03 — FAIL

- family: open_social
- prompt: خلنا ناخذ كلام خفيف
- response: حدد دة لوقت لاحقعادي يبعد أن تنتك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_04 — FAIL

- family: open_social
- prompt: افتح موضوعًا هادئًا
- response: ابدأ بالأهم، وبعد ما تح سالفة خفيفة أول جزء راجع دة ر.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_05 — FAIL

- family: open_social
- prompt: عطني سوالف بسيطة
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_06 — FAIL

- family: open_social
- prompt: أريد كلامًا وديًا قصيرًا
- response: حدد دة أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_07 — FAIL

- family: open_social
- prompt: تكلم معي عن شي لطيف
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_08 — PASS

- family: open_social
- prompt: اختر حديثًا خفيفًا بيننا
- response: نختار موضوعًا
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_09 — FAIL

- family: open_social
- prompt: ودي بموضوع سوالف
- response: حدد دة أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_10 — FAIL

- family: open_social
- prompt: ابدأ محادثة سهلة
- response: نبدأ موضوع خفيف: اكتب المهام، وابدأ بالأهم عشدة يول.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## open_social_11 — FAIL

- family: open_social
- prompt: هات كلام يمشي الوقت
- response: حدد دة لوقت لاحقوابدأ بالأهم
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_12 — FAIL

- family: open_social
- prompt: لنختر موضوعًا صغيرًا
- response: حدد دة أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — FAIL

- family: followup
- prompt: وضح لي مقصدك اكثر
- response: حدد دة لوقت لاحقيرة، وابدأ بالأهم قبل الأشياء الجانراجع بالأهم، وابدأ بالأهم عشرين دقيقة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_02 — FAIL

- family: followup
- prompt: أعد شرح النقطة ببساطة
- response: حدد دة أراحك بهدوء: إلى يرة، وابدأ بالأهم قبل الأشياء السهلة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — FAIL

- family: followup
- prompt: ما فهمت وش تبي تقول
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_04 — FAIL

- family: followup
- prompt: ما الخطوة بعد هذا الشرح
- response: حدد دة أراحك اليوم؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_05 — FAIL

- family: followup
- prompt: طيب كمل من هنا
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_06 — FAIL

- family: followup
- prompt: اجعل الفكرة أوضح
- response: حدد دة أراحك بهدوء: إلى يرة، وابدأ بالأهم قبل الأشياء السهلة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_07 — FAIL

- family: followup
- prompt: يعني ابدا من وين
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_08 — FAIL

- family: followup
- prompt: فسر كلامك مرة أخرى
- response: حدد دة مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_09 — FAIL

- family: followup
- prompt: وش قصدك بالضبط
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_10 — FAIL

- family: followup
- prompt: اختصر لي المعنى
- response: حدد دة أراحك بهدوء: إلى مهام صغيرة، وابدأ بالأهم قبل الأشياء الجشيء بعد أن تنت
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## followup_11 — FAIL

- family: followup
- prompt: ما وصلتني الفكرة
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_12 — FAIL

- family: followup
- prompt: تابع من آخر جملة
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_01 — PASS

- family: planning
- prompt: ابي ارتب اولوياتي اليوم
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — PASS

- family: planning
- prompt: ساعدني أرتب أعمالي
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_03 — PASS

- family: planning
- prompt: من وين ابدا اذا المهام كثيره
- response: حدد دة لوقت لاحقوابدأ بالأهم عشدة دقيقة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_04 — PASS

- family: planning
- prompt: كيف أقسم وقتي اليوم
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_05 — FAIL

- family: planning
- prompt: ابي جدول بسيط لبدايتي
- response: ابدأ بالأهم، وبعد ما تخلواترك الباقي لوقت لاحقرتب رتب انانانالجزء الإقصيرًا.
- guard_reason: malformed_token
- expected_ok: True
- family_ok: True
- reason: guard:malformed_token

## planning_06 — FAIL

- family: planning
- prompt: أحتاج ترتيبًا سريعًا
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## planning_07 — PASS

- family: planning
- prompt: وش اسوي بالمهام المتراكمة
- response: حدد دة لوقت لاحقوابدأ بالأهم عشدة رين دقيقة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_08 — PASS

- family: planning
- prompt: ضع لي بداية واضحة
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_09 — PASS

- family: planning
- prompt: خلني ابدأ بدون تشتت
- response: اكتب المهام، وابدأ بالأهم عشدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_10 — PASS

- family: planning
- prompt: كيف أختصر قائمة عملي
- response: حدد دة مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_11 — PASS

- family: planning
- prompt: ساعدني احدد اول شي
- response: ابدأ بالأهم، وبعد ما تخلواترك الباقي لوقت لاحقأول جزء راجع قصيرًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_12 — PASS

- family: planning
- prompt: أريد تنظيمًا بسيطًا للمهام
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_01 — FAIL

- family: support
- prompt: صدري ضايق وابغى اهدأ
- response: حدد دة لوقت لاحقمهام صغيرة، وابدأ بالأهم قبل الأشياء الجانيق
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_02 — FAIL

- family: support
- prompt: أشعر بتوتر وأريد طمأنينة
- response: حدد دة مهام واضحة، لوقت لاحققصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_03 — FAIL

- family: support
- prompt: ابي كلمة تهون علي
- response: حدد دة لوقت لاحقمهام صغيرة، وابدأ بالأهم قبل الأشياء هاراجع
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_04 — FAIL

- family: support
- prompt: أحتاج هدوءًا قبل أن أبدأ
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_05 — FAIL

- family: support
- prompt: قلقي زايد شوي
- response: اكتب المهام، وابدأ بالأهم عشدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_06 — FAIL

- family: support
- prompt: كيف أهدئ نفسي الآن
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_07 — FAIL

- family: support
- prompt: حاس بتوتر ومحتاج اروق
- response: ابدأ بالأهم، وبعد ما تخلمهام صغلوقت لاحق.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_08 — FAIL

- family: support
- prompt: طمئنّي بجملة قصيرة
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_09 — FAIL

- family: support
- prompt: ابي اهدى من التفكير
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_10 — FAIL

- family: support
- prompt: أنا متوتر من البداية
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_11 — FAIL

- family: support
- prompt: محتاج كلام يخفف علي
- response: حدد دة لوقت لاحقوابدأ بالأهم
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_12 — FAIL

- family: support
- prompt: أريد راحة قصيرة
- response: اكتب ثلاث مهام واضحة، هام، وابدأ بالأهم عشدة دة يول. دقيقة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_01 — FAIL

- family: topic
- prompt: ما معنى الوفاء للناس
- response: حدد قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_02 — FAIL

- family: topic
- prompt: التعاون وين يبان
- response: حدد دة تقدّر الناس ثلاث ر.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_03 — FAIL

- family: topic
- prompt: اشرح الصبر في موقف صعب
- response: حدد دة فة وقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش اثره
- response: حدد دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_05 — FAIL

- family: topic
- prompt: عرّف الهدوء بعبارة بسيطة
- response: حدد قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_06 — FAIL

- family: topic
- prompt: الصدق ليه مهم
- response: حدد دة ك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_07 — FAIL

- family: topic
- prompt: ما جوهر الصداقة
- response: اكتب ثلاث مهام واضحة، فة وقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_08 — FAIL

- family: topic
- prompt: الشجاعة كيف تكون
- response: حدد دة دة لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_09 — FAIL

- family: topic
- prompt: أعطني مثالًا على التعاون
- response: اكتب المهام، وابدأ بالأهم قبل قبل الأشياء للتنفيذ.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_10 — FAIL

- family: topic
- prompt: وش يعني الوفاء مع الاصحاب
- response: حدد دة لوقت لاحقر.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_11 — FAIL

- family: topic
- prompt: ما قيمة الاحترام
- response: اكتب المهام، وابدأ بالأهم عشقصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_12 — FAIL

- family: topic
- prompt: الصبر متى نحتاجه
- response: حدد دة لوقت لاحقر.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing
