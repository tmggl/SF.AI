# Phase 27.58 Tokenizer Bounded Alignment Probe

## open_social_01 — FAIL

- family: open_social
- prompt: وش ودك نسولف عنه
- response: خلنا نبدأ بسؤال بسيط: وش تحتاج؟
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_02 — FAIL

- family: open_social
- prompt: هات سالفة خفيفة
- response: العفو، حاضر بأي وقت.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_03 — FAIL

- family: open_social
- prompt: أريد كلامًا خفيفًا
- response: ابدأ بخطوة صغيرة ثم أكمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — FAIL

- family: followup
- prompt: يعني كيف
- response: نكمل: اختر خطوة واحدة، نفذها، ثم قيّم النتيجة.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## followup_02 — FAIL

- family: followup
- prompt: اشرحها أكثر
- response: العفو، يسعدني أن أساعدك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — FAIL

- family: followup
- prompt: طيب بعدين
- response: العفو، حاضر بأي وقت.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## planning_01 — PASS

- family: planning
- prompt: كيف أنظم يومي
- response: اكتب ثلاث مهام وابدأ بالأهم.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — PASS

- family: planning
- prompt: ابي ارتب يومي
- response: اكتب أهم ثلاث أشياء وابدأ بالأول.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_03 — FAIL

- family: planning
- prompt: دلني على بداية عملية
- response: اختر واحدة صغيرة وواضحة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_01 — PASS

- family: support
- prompt: توترت شوي
- response: الله يهونها، خذ نفس واهدأ شوي.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_02 — FAIL

- family: support
- prompt: أحتاج أهدأ
- response: خذ نفسًا هادئًا واهدأ الآن.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## support_03 — FAIL

- family: support
- prompt: طمني
- response: ابدأ بشي بسيط وواضح.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_01 — FAIL

- family: topic
- prompt: ما معنى الصداقة
- response: الصدق أن تقول الحقيقة بوضوح ل.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## topic_02 — PASS

- family: topic
- prompt: الشجاعة وش تعني
- response: الشجاعة إنك تسوي الصح حتى لو كنت خايف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_03 — FAIL

- family: topic
- prompt: اشرح الصدق
- response: الشجاعة أن تقول طيبة تقوم الآن.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing
