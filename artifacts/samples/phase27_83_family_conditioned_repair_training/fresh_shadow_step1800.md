# Phase 27.69 New Fresh Shadow Canary

## open_social_01 — FAIL

- family: open_social
- prompt: وش رايك نسولف شوي
- response: لا أ، خذ نفس تقدير واهدهدر نفسك أن المطلوب جزء راجع يومك.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## open_social_02 — FAIL

- family: open_social
- prompt: حدثني عن شيء بسيط
- response: وقت وقت وقت ح سالفة خفيفة عادي استاستاستانانبية. منح نفسك أن المطلوب بالكلام بالكلام قصيرة.
- guard_reason: malformed_token
- expected_ok: True
- family_ok: False
- reason: guard:malformed_token

## open_social_03 — FAIL

- family: open_social
- prompt: خلنا ناخذ كلام خفيف
- response: لا لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_04 — FAIL

- family: open_social
- prompt: افتح موضوعًا هادئًا
- response: لا س انانانذكّر نفسك أن المطلوب قصيرة.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## open_social_05 — FAIL

- family: open_social
- prompt: عطني سوالف بسيطة
- response: لا اليوم. انانانذكّر نفسك أن المطلوب جزء راجع يومك.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## open_social_06 — FAIL

- family: open_social
- prompt: أريد كلامًا وديًا قصيرًا
- response: وقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_07 — FAIL

- family: open_social
- prompt: تكلم معي عن شي لطيف
- response: لا اليوم. عادي خفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## open_social_08 — FAIL

- family: open_social
- prompt: اختر حديثًا خفيفًا بيننا
- response: نختار موضوعًا خفف خفف خفف تنفس بهدوء وااستاستاستعد للانانانتقل لما لما لما قصيرة.
- guard_reason: malformed_token
- expected_ok: True
- family_ok: False
- reason: guard:malformed_token

## open_social_09 — FAIL

- family: open_social
- prompt: ودي بموضوع سوالف
- response: خففها على نفسك، خذ نفس وابدأ وابدأ م، وواضح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_10 — FAIL

- family: open_social
- prompt: ابدأ محادثة سهلة
- response: نبدأ مببطتنفس بهدوء ياستوابدأ وابدأ م، تقديلا وقت وقت وقت ه.
- guard_reason: repeated_phrase
- expected_ok: True
- family_ok: False
- reason: guard:repeated_phrase

## open_social_11 — FAIL

- family: open_social
- prompt: هات كلام يمشي الوقت
- response: لا أ، خذ نفس بذكّر نفسك أن المطلوب الآن وتوتوتشيء مرة
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## open_social_12 — FAIL

- family: open_social
- prompt: لنختر موضوعًا صغيرًا
- response: تنفس ببطقصيرة. قصيرة. قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — FAIL

- family: followup
- prompt: وضح لي مقصدك اكثر
- response: خففها على نفسك، خذ نفس وابدأ ضغط خطوة صغيرة وق الموضوع ألا تجلوقت لاحق
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## followup_02 — FAIL

- family: followup
- prompt: أعد شرح النقطة ببساطة
- response: تنفس ببطوتنكمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — FAIL

- family: followup
- prompt: ما فهمت وش تبي تقول
- response: خففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_04 — FAIL

- family: followup
- prompt: ما الخطوة بعد هذا الشرح
- response: خذ نفس أن تقول ببطوتوتوتوقت وقت وقت واضح.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## followup_05 — FAIL

- family: followup
- prompt: طيب كمل من هنا
- response: خففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_06 — FAIL

- family: followup
- prompt: اجعل الفكرة أوضح
- response: خذ نفس نكمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_07 — FAIL

- family: followup
- prompt: يعني ابدا من وين
- response: لا خذ نفس واحدة واضحة قبل قبل واترك الباقي لوقت لاحقشيء واضح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_08 — FAIL

- family: followup
- prompt: فسر كلامك مرة أخرى
- response: خذ نفس نكمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_09 — FAIL

- family: followup
- prompt: وش قصدك بالضبط
- response: لا لوقت لاحقنفسًا ثم اختر ثلاث الأهم، ك بهدوء: خذ نفس نكمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_10 — FAIL

- family: followup
- prompt: اختصر لي المعنى
- response: تنفس ببطانانانوابدأ بالأهم ثم اختر ثلاث نفسًا ثم ذكّر نفسك أن المطلوب خطوة صغيرة فقط.
- guard_reason: malformed_token
- expected_ok: True
- family_ok: False
- reason: guard:malformed_token

## followup_11 — FAIL

- family: followup
- prompt: ما وصلتني الفكرة
- response: نفسًا ثم عد االآن.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_12 — FAIL

- family: followup
- prompt: تابع من آخر جملة
- response: نسان ببمهمة واحدة واضحة وابدأ بالأهم لمركّر نفسك أن المطلوب خطوة صغيرة الشيء
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## planning_01 — FAIL

- family: planning
- prompt: ابي ارتب اولوياتي اليوم
- response: خذ نفس شوي ببواترك الباقي لوقت وقت وقت م، وابدأ ، ر نفسك أن المطلوب خطوة صغيرة وق صغ
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## planning_02 — FAIL

- family: planning
- prompt: ساعدني أرتب أعمالي
- response: خذ نفس ببطنسان وابدأ بالأهم ثم اختر ثلاث مهام بس
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## planning_03 — FAIL

- family: planning
- prompt: من وين ابدا اذا المهام كثيره
- response: خففها على نفسك، خذ نفس وابدأ وابدأ وابدأ م، م، م، شيء واضح.
- guard_reason: repeated_phrase
- expected_ok: True
- family_ok: False
- reason: guard:repeated_phrase

## planning_04 — FAIL

- family: planning
- prompt: كيف أقسم وقتي اليوم
- response: خفففها على نفسك، خذ نفس وابدأ وابدأ وابدأ ستفمشمشالأمر ألا اليوم.
- guard_reason: malformed_token
- expected_ok: True
- family_ok: False
- reason: guard:malformed_token

## planning_05 — FAIL

- family: planning
- prompt: ابي جدول بسيط لبدايتي
- response: لا لوقت لاحقًا، ًا، ًا، م، م، م، واترك الباقي لوقت وقت وقت مهام صغ
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## planning_06 — FAIL

- family: planning
- prompt: أحتاج ترتيبًا سريعًا
- response: خفها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_07 — FAIL

- family: planning
- prompt: وش اسوي بالمهام المتراكمة
- response: خففها على نفسك، خذ نفس وابدأ وابدأ وابدأ م، ك اليوم؟
- guard_reason: repeated_phrase
- expected_ok: True
- family_ok: False
- reason: guard:repeated_phrase

## planning_08 — FAIL

- family: planning
- prompt: ضع لي بداية واضحة
- response: خففها على التفكير بوضوح.
- guard_reason: advice_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:advice_mismatch

## planning_09 — FAIL

- family: planning
- prompt: خلني ابدأ بدون تشتت
- response: خفففها على طيبة طيبة طيبة واهتمام وقت لاحقنفسًا ثم عد ك الموضوع ألا اليوم.
- guard_reason: repeated_phrase
- expected_ok: False
- family_ok: False
- reason: guard:repeated_phrase

## planning_10 — FAIL

- family: planning
- prompt: كيف أختصر قائمة عملي
- response: خفففها على نفسك، خذ نفس وابدأ وابدأ ستفمشواضح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_11 — FAIL

- family: planning
- prompt: ساعدني احدد اول شي
- response: خفففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_12 — FAIL

- family: planning
- prompt: أريد تنظيمًا بسيطًا للمهام
- response: ًا، ًا، ًا، م: خذ نفس بذكّر نفسك أن المطلوب ذككّّر عادة
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_01 — FAIL

- family: support
- prompt: صدري ضايق وابغى اهدأ
- response: لا لوقت الحاجة.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_02 — PASS

- family: support
- prompt: أشعر بتوتر وأريد طمأنينة
- response: خذ نفس شوي واهدأ، بعدها ابدأ بذكّر نفسك أن المطلوب نفسك أن الن
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_03 — PASS

- family: support
- prompt: ابي كلمة تهون علي
- response: لا وقت الحاجة. تخلعن يقالعمل نفسك أنة، وابدأ بالأهم واضح.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_04 — FAIL

- family: support
- prompt: أحتاج هدوءًا قبل أن أبدأ
- response: وقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_05 — FAIL

- family: support
- prompt: قلقي زايد شوي
- response: لا أ، خذ نفس ييينفسك لحظة ثم اختر عادة وقت وقت وقت م، م، مل مل مل نفسك لحظة قصيرة.
- guard_reason: repeated_phrase
- expected_ok: True
- family_ok: True
- reason: guard:repeated_phrase

## support_06 — FAIL

- family: support
- prompt: كيف أهدئ نفسي الآن
- response: وقت وقت وقت ح سالفة خفيفة عادي استاستاستانانبية. الاحترام قصيرة.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## support_07 — PASS

- family: support
- prompt: حاس بتوتر ومحتاج اروق
- response: لا الأهم أولًا. ح سالفة خفيفة عادي نفسًا ثم اختر ثلاث يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_08 — FAIL

- family: support
- prompt: طمئنّي بجملة قصيرة
- response: بها.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_09 — FAIL

- family: support
- prompt: ابي اهدى من التفكير
- response: لا لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_10 — FAIL

- family: support
- prompt: أنا متوتر من البداية
- response: وقت الحاجة.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_11 — FAIL

- family: support
- prompt: محتاج كلام يخفف علي
- response: لا ها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_12 — FAIL

- family: support
- prompt: أريد راحة قصيرة
- response: وقت وقت وقت الحاجة. عن عادة ما ثم اختر ثلاث يومك.
- guard_reason: repeated_phrase
- expected_ok: False
- family_ok: False
- reason: guard:repeated_phrase

## topic_01 — FAIL

- family: topic
- prompt: ما معنى الوفاء للناس
- response: خذ نفس أن نفسًا ثم اختر ثلاث ذكًّا ًا عن عادة ًا، ًا، ًا، ثبات وهدوء وهدوء وهدوء وقت وقت وقت لاحق
- guard_reason: repeated_phrase
- expected_ok: False
- family_ok: False
- reason: guard:repeated_phrase

## topic_02 — FAIL

- family: topic
- prompt: التعاون وين يبان
- response: خففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_03 — FAIL

- family: topic
- prompt: اشرح الصبر في موقف صعب
- response: خذ نفس أن قصيرة. قصيرة. قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش اثره
- response: خفها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_05 — FAIL

- family: topic
- prompt: عرّف الهدوء بعبارة بسيطة
- response: خذ نفس أن يعيعالصعوبة.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## topic_06 — FAIL

- family: topic
- prompt: الصدق ليه مهم
- response: خففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_07 — FAIL

- family: topic
- prompt: ما جوهر الصداقة
- response: خفها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_08 — FAIL

- family: topic
- prompt: الشجاعة كيف تكون
- response: لا لوقت الحاجة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_09 — FAIL

- family: topic
- prompt: أعطني مثالًا على التعاون
- response: خذ نفس أن قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_10 — FAIL

- family: topic
- prompt: وش يعني الوفاء مع الاصحاب
- response: خففها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_11 — FAIL

- family: topic
- prompt: ما قيمة الاحترام
- response: خذ نفس أن قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_12 — FAIL

- family: topic
- prompt: الصبر متى نحتاجه
- response: خفها على التفكير بوضوح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing
