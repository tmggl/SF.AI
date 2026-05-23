# Phase 27.43 Guarded Data-Backed Expansion

## weak_smalltalk_akhbarak — PASS

- bucket: weak_lane
- prompt: وش اخبارك
- response: بخير ولله الحمدك وقت الخوف.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_smalltalk_oloomk — PASS

- bucket: weak_lane
- prompt: علومك
- response: بخير ولله الحمدك وقت الخوف.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_thanks_mashkoor — FAIL

- bucket: weak_lane
- prompt: مشكور
- response: ناس معًا لتامل.
- guard_reason: thanks_mismatch
- semantic_match: False
- reason: guard:thanks_mismatch

## weak_thanks_tislam — FAIL

- bucket: weak_lane
- prompt: تسلم
- response: ناس معًا لتامل.
- guard_reason: thanks_mismatch
- semantic_match: False
- reason: guard:thanks_mismatch

## weak_planning_time — PASS

- bucket: weak_lane
- prompt: نظم وقتي
- response: اكتب ثلاث مهام وابدأ بكلامك وتزيد المفردات.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_planning_priorities — PASS

- bucket: weak_lane
- prompt: ابي ارتب اولوياتي
- response: اكتب أهم ثلاث أشياء وابدأ بالأول.
- guard_reason: passed
- semantic_match: True
- reason: passed

## new_definition_wafa — FAIL

- bucket: new_topic
- prompt: ما معنى الوفاء
- response: الهدوء سكينة تساعدك على التفكير بوضوح.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## new_definition_courage — FAIL

- bucket: new_topic
- prompt: اشرح الشجاعة
- response: الصداقة مودة ووفاء بين الناس.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_smalltalk — FAIL

- bucket: regression
- prompt: كيفك اليوم
- response: اكتب أهم ثلاث أشياء وابدأ بالأول.
- guard_reason: social_smalltalk_mismatch
- semantic_match: False
- reason: guard:social_smalltalk_mismatch

## reg_advice — FAIL

- bucket: regression
- prompt: انصحني ببداية بسيطة
- response: في الود ودة مل.
- guard_reason: advice_mismatch
- semantic_match: False
- reason: guard:advice_mismatch

## reg_planning — PASS

- bucket: regression
- prompt: كيف ارتب مهامي
- response: اكتب ثلاث مهام وابدأ بكلامك وتر.
- guard_reason: passed
- semantic_match: True
- reason: passed

## reg_support — FAIL

- bucket: regression
- prompt: انا متوتر
- response: الصدق وضوح في واب وقت الخوالعمإنك تثبت معك.
- guard_reason: support_mismatch
- semantic_match: False
- reason: guard:support_mismatch

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
