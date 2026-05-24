# Phase 27.69 New Fresh Shadow Canary

## open_social_01 — PASS

- family: open_social
- prompt: وش رايك نسولف شوي
- response: نعم، نتحدث قليلًا في موضوع بسيط.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_02 — PASS

- family: open_social
- prompt: حدثني عن شيء بسيط
- response: أكيد، نسولف عن شيء خفيف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_03 — PASS

- family: open_social
- prompt: خلنا ناخذ كلام خفيف
- response: خلنا نبدأ بس الفة قصيرة وخفيفة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_04 — PASS

- family: open_social
- prompt: افتح موضوعًا هادئًا
- response: نختار موضوعاموضوععن موضوع بسيط وخفيفًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_05 — PASS

- family: open_social
- prompt: عطني سوالف بسيطة
- response: نعم، نتحدث قليلًا في موضوع بسيط.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_06 — PASS

- family: open_social
- prompt: أريد كلامًا وديًا قصيرًا
- response: نفتح موضوعًا لطيفًا ونتحدث عنه بهدوء.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_07 — PASS

- family: open_social
- prompt: تكلم معي عن شي لطيف
- response: أبشر، نسولف عن موضوع عادي وخفيف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_08 — FAIL

- family: open_social
- prompt: اختر حديثًا خفيفًا بيننا
- response: التعاون مشاركة الجهد بين الناس.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_09 — FAIL

- family: open_social
- prompt: ودي بموضوع سوالف
- response: خلنا نبدأ بمالنبوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_10 — FAIL

- family: open_social
- prompt: ابدأ محادثة سهلة
- response: التعاون مشاركة الجهد بين الناس.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_11 — PASS

- family: open_social
- prompt: هات كلام يمشي الوقت
- response: خلنا نبدأ بس الفة قصيرة وخفيفة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_12 — FAIL

- family: open_social
- prompt: لنختر موضوعًا صغيرًا
- response: التعاون مشاركة الجهد بين الناس.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — PASS

- family: followup
- prompt: وضح لي مقصدك اكثر
- response: أقصد المعنى ببساطة وبخطوة واضحة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_02 — PASS

- family: followup
- prompt: أعد شرح النقطة ببساطة
- response: نوضح الفكرة ببساطة: خطوة واضحة ثم متابعة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_03 — PASS

- family: followup
- prompt: ما فهمت وش تبي تقول
- response: أقصد الفكرة ببساطة: خذ خطوة واضحة ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_04 — PASS

- family: followup
- prompt: ما الخطوة بعد هذا الشرح
- response: الفكرة ببساطة: خطوة واضحة ثم متابعة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_05 — PASS

- family: followup
- prompt: طيب كمل من هنا
- response: أقصد باختصار: خذ أول خطوة وافهمها ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_06 — PASS

- family: followup
- prompt: اجعل الفكرة أوضح
- response: أقصد أن الفكرة ببساطة: خطوة واضحة ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_07 — PASS

- family: followup
- prompt: يعني ابدا من وين
- response: أقصد خذ أول خطوة واضحة ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_08 — PASS

- family: followup
- prompt: فسر كلامك مرة أخرى
- response: أبسطها لك: ابدأ بالجزء السهل ثم أكمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_09 — PASS

- family: followup
- prompt: وش قصدك بالضبط
- response: أقصد باختصار: خذ أول جزء واضح وابدأ منه.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_10 — PASS

- family: followup
- prompt: اختصر لي المعنى
- response: نعم، أبسطها: ابدأ بالقريب ثم انتقل لما بعده.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_11 — PASS

- family: followup
- prompt: ما وصلتني الفكرة
- response: يعني المطلوب خطوة واضحة ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_12 — PASS

- family: followup
- prompt: تابع من آخر جملة
- response: أقصد أن تختار خطوة واضحة قبل التفاصيل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_01 — PASS

- family: planning
- prompt: ابي ارتب اولوياتي اليوم
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — PASS

- family: planning
- prompt: ساعدني أرتب أعمالي
- response: اختر مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_03 — PASS

- family: planning
- prompt: من وين ابدا اذا المهام كثيره
- response: ابدأ بالأهم، وخله خطوة صغيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_04 — PASS

- family: planning
- prompt: كيف أقسم وقتي اليوم
- response: اكتب خطة قصيرة: مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_05 — PASS

- family: planning
- prompt: ابي جدول بسيط لبدايتي
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_06 — PASS

- family: planning
- prompt: أحتاج ترتيبًا سريعًا
- response: اختر مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_07 — PASS

- family: planning
- prompt: وش اسوي بالمهام المتراكمة
- response: اكتب المهام، واختر الأهم ثم ابدأ بقولك وتصرفك يكون فيه تقدير.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_08 — PASS

- family: planning
- prompt: ضع لي بداية واضحة
- response: رتب البداية هكذا: اختر مهمة واحدة وابدأ بها.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_09 — PASS

- family: planning
- prompt: خلني ابدأ بدون تشتت
- response: ابدأ بثلاث مهام، واختر الأهم ثم أكموضوع بسيط وفعل
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_10 — PASS

- family: planning
- prompt: كيف أختصر قائمة عملي
- response: اختر مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_11 — PASS

- family: planning
- prompt: ساعدني احدد اول شي
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_12 — PASS

- family: planning
- prompt: أريد تنظيمًا بسيطًا للمهام
- response: اكتب خطة قصيرة: مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_01 — PASS

- family: support
- prompt: صدري ضايق وابغى اهدأ
- response: خذ نفسًا هادئًا وخفف الضغط خطوة خطوة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_02 — PASS

- family: support
- prompt: أشعر بتوتر وأريد طمأنينة
- response: تنفس بهدوء وخذ لحظة راحة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_03 — PASS

- family: support
- prompt: ابي كلمة تهون علي
- response: خذ نفسًا بسيطًا وخلها تهدأ شوي.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_04 — PASS

- family: support
- prompt: أحتاج هدوءًا قبل أن أبدأ
- response: تنفس بهدوء وامنح نفسك لحظة راحة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_05 — PASS

- family: support
- prompt: قلقي زايد شوي
- response: هونها على نفسك وخذ نفس هادئ.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_06 — PASS

- family: support
- prompt: كيف أهدئ نفسي الآن
- response: تنفس بهدوء وخذ لحظة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_07 — PASS

- family: support
- prompt: حاس بتوتر ومحتاج اروق
- response: خذ نفسًا بسيطًا وخلها تهدأ شوي.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_08 — PASS

- family: support
- prompt: طمئنّي بجملة قصيرة
- response: تنفس بهدوء وخذ لحظة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_09 — PASS

- family: support
- prompt: ابي اهدى من التفكير
- response: خذ نفسًا وركز على خطوة واحدة الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_10 — PASS

- family: support
- prompt: أنا متوتر من البداية
- response: تنفس بهدوء وابدأ بخطوة صغيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_11 — PASS

- family: support
- prompt: محتاج كلام يخفف علي
- response: خذ نفسًا هادئًا وخففها عليك خطوة خطوة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_12 — PASS

- family: support
- prompt: أريد راحة قصيرة
- response: تنفس بهدوء وخذ لحظة راحة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_01 — PASS

- family: topic
- prompt: ما معنى الوفاء للناس
- response: الوفاء حفظ للعهد وثبات في الود.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_02 — PASS

- family: topic
- prompt: التعاون وين يبان
- response: التعاون إنك تساعد غيرك وتنجزون سوا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_03 — PASS

- family: topic
- prompt: اشرح الصبر في موقف صعب
- response: الصبر ثبات وهدوء وقت الصعوبة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_04 — PASS

- family: topic
- prompt: الاحترام وش اثره
- response: الاحترام يعني تقدّر الناس بقولك وفعلك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_05 — PASS

- family: topic
- prompt: عرّف الهدوء بعبارة بسيطة
- response: الهدوء سكينة تساعدك على التفكير بوضوح.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_06 — PASS

- family: topic
- prompt: الصدق ليه مهم
- response: الصدق يعني تقول الحقيقة وتلتزم بها.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_07 — PASS

- family: topic
- prompt: ما جوهر الصداقة
- response: الصداقة رفقة طيبة واهتمام وقت الحاجة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_08 — PASS

- family: topic
- prompt: الشجاعة كيف تكون
- response: الشجاعة تظهر حين تفعل الصواب مع وجود الخوف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_09 — PASS

- family: topic
- prompt: أعطني مثالًا على التعاون
- response: التعاون مشاركة الجهد بين الناس.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_10 — PASS

- family: topic
- prompt: وش يعني الوفاء مع الاصحاب
- response: الوفاء إنك تساعد غيرك وتنجزون سوا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_11 — PASS

- family: topic
- prompt: ما قيمة الاحترام
- response: الاحترام معاملة الناس بذوق وتقدير.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_12 — PASS

- family: topic
- prompt: الصبر متى نحتاجه
- response: الصبر إنك تتحمل وتكمل بدون استعجال.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed
