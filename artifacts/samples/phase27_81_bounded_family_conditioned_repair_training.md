# Phase 27.81 Samples

Best checkpoint: `sf-10m-step2000`

## open_social_01 — PASS

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

## open_social_02 — PASS

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

## open_social_03 — PASS

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

## open_social_04 — PASS

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

## open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: وش الشي وش ألطف تحب تجلس فيه إذا تبي تهدأ؟
- reason: expected_terms_missing

## open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

## open_social_07 — PASS

- family: open_social
- prompt: وش سالفتك اليوم
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

## open_social_08 — PASS

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

## open_social_09 — PASS

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: أبشر، خلنا نسولف عن يومك: وش ألطف شي صار لك؟
- reason: passed

## open_social_10 — PASS

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

## followup_01 — PASS

- family: followup
- prompt: ما وضحت لي زين
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_02 — PASS

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_03 — PASS

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: يعني لا تجمع كل شيء مرة وحدة؛ خذ جزء بسيط وابدأ فيه.
- reason: passed

## followup_04 — PASS

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_05 — PASS

- family: followup
- prompt: يعني وش المطلوب مني
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

## followup_07 — PASS

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

## followup_09 — PASS

- family: followup
- prompt: وش تقصد بهالكلام
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

## followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: expected_terms_missing

## planning_01 — PASS

- family: planning
- prompt: ابي ابدأ يومي صح
- response: حدد المطلوب، اكتب المهام، وابدأ بالأهم عشرين دقيقة.
- reason: passed

## planning_02 — PASS

- family: planning
- prompt: رتب لي بداية عملية
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- reason: passed

## planning_03 — PASS

- family: planning
- prompt: عندي لخبطة بالمهام
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- reason: passed

## planning_04 — PASS

- family: planning
- prompt: كيف أضع أولوية لعملي
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- reason: passed

## planning_05 — PASS

- family: planning
- prompt: وش اول شي اسويه اليوم
- response: اكتب ثلاث مهام واضحة، وابدأ بالأهم لمدة قصيرة.
- reason: passed

## planning_06 — PASS

- family: planning
- prompt: ساعدني أختار مهمة واحدة
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم شوف اللي بعده.
- reason: passed

## planning_07 — PASS

- family: planning
- prompt: ابي طريقة سهلة للترتيب
- response: حدد المطلوب، اكتب المهام، وابدأ بالأهم عشرين دقيقة.
- reason: passed

## planning_08 — PASS

- family: planning
- prompt: دلني على خطة قصيرة
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم شوف اللي بعده.
- reason: passed

## planning_09 — PASS

- family: planning
- prompt: مهامي كثيره ومادري من وين
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم شوف اللي بعده.
- reason: passed

## planning_10 — PASS

- family: planning
- prompt: كيف أبدأ بلا تشتت
- response: حدد المطلوب، اكتب المهام، وابدأ بالأهم عشرين دقيقة.
- reason: passed
