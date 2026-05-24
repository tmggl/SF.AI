# Phase 27.62 Family-Balance Repair

## open_social_01 — PASS

- family: open_social
- prompt: ابي اسولف شوي
- response: أكيد، نسولف عن موضوع خفيف من يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_02 — PASS

- family: open_social
- prompt: خلنا نفتح موضوع بسيط
- response: نبدأ بموضوع بسيط وخفيف، وش ودك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_03 — PASS

- family: open_social
- prompt: حدثني حديثًا لطيفًا
- response: نبدأ بحديث لطيف عن شيء خفيف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_04 — PASS

- family: open_social
- prompt: وش عندك كلام خفيف
- response: عندي كلام خفيف: نسولف عن يومك أو موقف بسيط.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_05 — PASS

- family: open_social
- prompt: افتح معي حوارًا قصيرًا
- response: نفتح حواخفيقصيرًا عن موضوع بسيط.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_06 — PASS

- family: open_social
- prompt: ما عندي موضوع سولف انت
- response: أبشر، نسولف عن يومك أو عن شيء خفيف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_01 — FAIL

- family: followup
- prompt: ما فهمت قصدك
- response: عندي نسولف سوالف عاد كلام أو عن خفيخفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_02 — FAIL

- family: followup
- prompt: هل توضح لي الفكرة
- response: نبدأ بكلام سوالف عن أخذ خذ خذ وخفي
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — FAIL

- family: followup
- prompt: وبعدين وش اسوي
- response: خلنا نبدأ عن يومك ة قصيرة شيء خفينبدأ
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_04 — PASS

- family: followup
- prompt: أكمل شرحك
- response: نكمل: عن در موضوع يومك. شيء خفيأو خفيف خفيف
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_05 — PASS

- family: followup
- prompt: طيب وش تقصد بالضبط
- response: أقصد نبدأ
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_06 — FAIL

- family: followup
- prompt: فسرها بطريقة أبسط
- response: أبسطها لك: ابدأ بالجزء السثم أكموضوعوخفيفة. قة ة واواوابدأ شيء قصيرًا ونتحدث عنه قليلًا نختار
- guard_reason: malformed_token
- expected_ok: True
- family_ok: False
- reason: guard:malformed_token

## planning_01 — FAIL

- family: planning
- prompt: ابي اخلي يومي مرتب
- response: خذ لطيفًا عن موضوع وارًا قصيرًا ف.
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_02 — FAIL

- family: planning
- prompt: ساعدني أبدأ عملي اليوم
- response: نبدأ عن عن عن موضوع وارًا وخفي
- guard_reason: repeated_phrase
- expected_ok: False
- family_ok: False
- reason: guard:repeated_phrase

## planning_03 — FAIL

- family: planning
- prompt: عندي اشياء كثيره وش ابدا فيه
- response: نفنبدأ ف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_04 — PASS

- family: planning
- prompt: أريد خطة صغيرة لبداية اليوم
- response: ابدأ عن نبدأ موضوع وافهواضحة موضوع
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_05 — FAIL

- family: planning
- prompt: رتب لي اول خطوه
- response: أبسطها نبدأ نبدأ موضوع
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_06 — FAIL

- family: planning
- prompt: كيف أختار أول مهمة
- response: نبدأ عن عن عن موضوع وارًا وخفي
- guard_reason: repeated_phrase
- expected_ok: False
- family_ok: False
- reason: guard:repeated_phrase

## support_01 — FAIL

- family: support
- prompt: ضايق صدري شوي
- response: نختار نسولف عن يومك عن عن تح بسيط. بسيط. ف،
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_02 — FAIL

- family: support
- prompt: أشعر بضغط وأحتاج هدوءًا
- response: نختار بس نبدأ عن ونتحدث ونتحدث بسيط. بسيط.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_03 — FAIL

- family: support
- prompt: ابي كلام يطمني
- response: أبشر، نسولف عن يومك أو عن موضوع ف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_04 — FAIL

- family: support
- prompt: أنا قلق من البداية
- response: نختار نبدأ وابدأ بعن ونتحدث عنه بسيط. بسيط.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## support_05 — FAIL

- family: support
- prompt: حاس اني مشتت
- response: خذ خذ تح وارًا وارًا نبدأ وارًا
- guard_reason: repetition
- expected_ok: False
- family_ok: False
- reason: guard:repetition

## support_06 — FAIL

- family: support
- prompt: كيف أهدأ دون تعقيد
- response: نبدأ حديث حديث ًا يومك. عن موضوع ف.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## topic_01 — FAIL

- family: topic
- prompt: عرّف لي الوفاء
- response: التالجزء جزء أبسطها ق
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_02 — FAIL

- family: topic
- prompt: وش معنى التعاون
- response: ح بموضوع عن موضوع نسولف نسولف يومك بفي خفيف
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_03 — FAIL

- family: topic
- prompt: ما المقصود بالصبر
- response: التالالفكرة تبدأ تح ف، واوابدأ عن عن أو وخفيواوابدأ وخفيك؟ كلام موضوع بسيط.
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش هو
- response: البموضوع خفيف نبدأ نبدأ نبدأ خفيسواواوا
- guard_reason: malformed_token
- expected_ok: False
- family_ok: False
- reason: guard:malformed_token

## topic_05 — FAIL

- family: topic
- prompt: اشرح الهدوء بجملة
- response: في نبدأ بكلام خفيتح وافهخذ وخفينبدأ قليلًا ف، بسيط. بسيط. وارًا ك؟ ف. موضوع خفيف ونتحدث قصيرًا قصيرًا بسيط.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_06 — PASS

- family: topic
- prompt: وش يعني الصدق ببساطه
- response: الصدق كلام نبدأ تح ف، ف،
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed
