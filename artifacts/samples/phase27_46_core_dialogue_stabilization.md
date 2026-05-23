# Phase 27.43 Guarded Data-Backed Expansion

## weak_smalltalk_akhbarak — PASS

- bucket: weak_lane
- prompt: وش اخبارك
- response: بخير ولله الحمد، وش أخبارك أنت؟
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_smalltalk_oloomk — PASS

- bucket: weak_lane
- prompt: علومك
- response: بخير ولله الحمد. وش ودك نسولف عنه؟
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_thanks_mashkoor — PASS

- bucket: weak_lane
- prompt: مشكور
- response: العفو، حاضر بأي وقت.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_thanks_tislam — PASS

- bucket: weak_lane
- prompt: تسلم
- response: العفو، يسعدني أساعدك.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_planning_time — PASS

- bucket: weak_lane
- prompt: نظم وقتي
- response: اكتب ثلاث مهام وابدأ بالأهم.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_planning_priorities — PASS

- bucket: weak_lane
- prompt: ابي ارتب اولوياتي
- response: ابدأ بالأهم ثم انتقل للي بعده.
- guard_reason: passed
- semantic_match: True
- reason: passed

## new_definition_wafa — FAIL

- bucket: new_topic
- prompt: ما معنى الوفاء
- response: تحفظ الود وتثبت مع من تثق به.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## new_definition_courage — FAIL

- bucket: new_topic
- prompt: اشرح الشجاعة
- response: التنظيم ترتيب الوقت والمهام بطريقة واضحة.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_smalltalk — PASS

- bucket: regression
- prompt: كيفك اليوم
- response: بخير ولله الحمد، أنت كيفك؟
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_advice — PASS

- bucket: regression
- prompt: انصحني ببداية بسيطة
- response: ابدأ بخطوة صغيرة وواضحة.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_planning — PASS

- bucket: regression
- prompt: كيف ارتب مهامي
- response: اكتب ثلاث مهام وابدأ بالأهم.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_support — PASS

- bucket: regression
- prompt: انا متوتر
- response: خذ نفسًا هادئًا واهدأ خطوة خطوة.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_friendship — PASS

- bucket: regression
- prompt: ما معنى الصداقة
- response: الصداقة علاقة طيبة تقوم على الوفاء.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_truth — PASS

- bucket: regression
- prompt: الصدق وش يعني
- response: الصدق يعني تقول الحقيقة بوضوح.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_order — PASS

- bucket: regression
- prompt: ما معنى التنظيم
- response: التنظيم ترتيب الوقت والمهام بطريقة واضحة.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_calm — PASS

- bucket: regression
- prompt: الهدوء وش يعني
- response: الهدوء يعني تخفف توترك وتتكلم بروية.
- guard_reason: passed
- semantic_match: True
- reason: passed
