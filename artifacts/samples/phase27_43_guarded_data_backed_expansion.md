# Phase 27.43 Guarded Data-Backed Expansion

## weak_smalltalk_akhbarak — FAIL

- bucket: weak_lane
- prompt: وش اخبارك
- response: الصداقة إنك تتحإنك تثبت رفيق يوقف معك.
- guard_reason: social_smalltalk_mismatch
- semantic_match: False
- reason: guard:social_smalltalk_mismatch

## weak_smalltalk_oloomk — FAIL

- bucket: weak_lane
- prompt: علومك
- response: الصدق أن تقول الحقيقة وتاخذ الأمور بروية.
- guard_reason: social_smalltalk_mismatch
- semantic_match: False
- reason: guard:social_smalltalk_mismatch

## weak_thanks_mashkoor — PASS

- bucket: weak_lane
- prompt: مشكور
- response: العفو، يسعدني أن تقول الحمل.
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_thanks_tislam — PASS

- bucket: weak_lane
- prompt: تسلم
- response: العفو، يسعدني أن تقول الحموفاء بين الناس.
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
- response: ابدأ بخطوة صغيرة وواضحة.
- guard_reason: passed
- semantic_match: True
- reason: passed

## new_definition_wafa — FAIL

- bucket: new_topic
- prompt: ما معنى الوفاء
- response: الصدق أن تقول الحقيقة وتاخذ الأمة تساعدك على التوتات.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## new_definition_courage — FAIL

- bucket: new_topic
- prompt: اشرح الشجاعة
- response: التنظيم معرفة ما تفعل ومتى تبدأ.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_smalltalk — FAIL

- bucket: regression
- prompt: كيفك اليوم
- response: الصداقة علاقة طيبة ووقرفداع.
- guard_reason: social_smalltalk_mismatch
- semantic_match: False
- reason: guard:social_smalltalk_mismatch

## reg_advice — FAIL

- bucket: regression
- prompt: انصحني ببداية بسيطة
- response: بخير، شكرًا لسؤالك.
- guard_reason: advice_mismatch
- semantic_match: False
- reason: guard:advice_mismatch

## reg_planning — PASS

- bucket: regression
- prompt: كيف ارتب مهامي
- response: اكتب ثلاث مهام وابدأ بكلامك يكون تقدير الناس.
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
