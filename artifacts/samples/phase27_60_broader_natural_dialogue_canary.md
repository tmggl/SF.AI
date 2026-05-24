# Phase 27.60 Broader Natural-Dialogue Canary

## open_social_01 — FAIL

- family: open_social
- prompt: ابي اسولف شوي
- response: ابدأ بشي واحد واضح، ثم انتقل للخطوة التالية.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_02 — PASS

- family: open_social
- prompt: خلنا نفتح موضوع بسيط
- response: نبدأ بحديث خفيف عن شيء لطيف في يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_03 — PASS

- family: open_social
- prompt: حدثني حديثًا لطيفًا
- response: نبدأ بموضوع بسيط وخفيف عن يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_04 — PASS

- family: open_social
- prompt: وش عندك كلام خفيف
- response: عندي موضوع خفيف: وش أفضل شي صار في يومك؟
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_05 — PASS

- family: open_social
- prompt: افتح معي حوارًا قصيرًا
- response: نبدأ بحديث خفيف عن شيء لطيف في يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_06 — PASS

- family: open_social
- prompt: ما عندي موضوع سولف انت
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_01 — PASS

- family: followup
- prompt: ما فهمت قصدك
- response: أقصد لا تستعجل؛ خذ الجزء الأول وافهمه ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_02 — PASS

- family: followup
- prompt: هل توضح لي الفكرة
- response: أقصد أن تبدأ بالواضح ثم تنتقل لما بعده.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_03 — FAIL

- family: followup
- prompt: وبعدين وش اسوي
- response: خذ نفسًا هادئًا وخفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_04 — PASS

- family: followup
- prompt: أكمل شرحك
- response: أقصد أن الفكرة أبسط: ابدأ بالجزء الواضح ثم أكمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_05 — FAIL

- family: followup
- prompt: طيب وش تقصد بالضبط
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_06 — FAIL

- family: followup
- prompt: فسرها بطريقة أبسط
- response: ابدأ بالجزء الواضح ثم أكمل.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## planning_01 — PASS

- family: planning
- prompt: ابي اخلي يومي مرتب
- response: ابدأ بشي واحد واضح، ثم انتقل للخطوة التالية.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — FAIL

- family: planning
- prompt: ساعدني أبدأ عملي اليوم
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_03 — FAIL

- family: planning
- prompt: عندي اشياء كثيره وش ابدا فيه
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_04 — FAIL

- family: planning
- prompt: أريد خطة صغيرة لبداية اليوم
- response: خفيف عن يومك.
- guard_reason: advice_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:advice_mismatch

## planning_05 — FAIL

- family: planning
- prompt: رتب لي اول خطوه
- response: خفيف عن يومك.
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_06 — PASS

- family: planning
- prompt: كيف أختار أول مهمة
- response: اكتب ثلاث مهام وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_01 — FAIL

- family: support
- prompt: ضايق صدري شوي
- response: خفيف من يومك ونسولف عنه.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_02 — FAIL

- family: support
- prompt: أشعر بضغط وأحتاج هدوءًا
- response: خفيف من يومك ونسولف عنه.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_03 — FAIL

- family: support
- prompt: ابي كلام يطمني
- response: ابدأ بشي واحد واضح، ثم انتقل للخطوة التالية.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_04 — FAIL

- family: support
- prompt: أنا قلق من البداية
- response: خفيف من يومك ونسولف عنه.
- guard_reason: advice_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:advice_mismatch

## support_05 — FAIL

- family: support
- prompt: حاس اني مشتت
- response: خفيف من يومك ونسولف عنه.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_06 — FAIL

- family: support
- prompt: كيف أهدأ دون تعقيد
- response: اكتب ثلاث مهام وابدأ بالأهم.
- guard_reason: support_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:support_mismatch

## topic_01 — FAIL

- family: topic
- prompt: عرّف لي الوفاء
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_02 — FAIL

- family: topic
- prompt: وش معنى التعاون
- response: خذ الجزء الأول وافهمه ثم كمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_03 — FAIL

- family: topic
- prompt: ما المقصود بالصبر
- response: خفيف عن يومك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش هو
- response: خفيف من يومك ونسولف عنه.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_05 — PASS

- family: topic
- prompt: اشرح الهدوء بجملة
- response: الهدوء سكينة تخفف التوتر وتوضح التفكير.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_06 — PASS

- family: topic
- prompt: وش يعني الصدق ببساطه
- response: الصدق إن كلامك يكون واضح وما فيه خداع.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed
