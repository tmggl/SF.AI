# Phase 27.43 Guarded Data-Backed Expansion

## weak_smalltalk_akhbarak — PASS

- bucket: weak_lane
- prompt: وش اخبارك
- response: بخير ولله الحمد، أنت كيفك؟
- guard_reason: passed
- semantic_match: True
- reason: passed

## weak_smalltalk_oloomk — PASS

- bucket: weak_lane
- prompt: علومك
- response: بخير ولله الحمد. وش تحتاج؟
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
- response: العفو، يسعدني أن أساعدك.
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
- response: ابدأ بشي بسيط وواضح.
- guard_reason: passed
- semantic_match: True
- reason: passed

## new_definition_wafa — PASS

- bucket: new_topic
- prompt: ما معنى الوفاء
- response: الوفاء أن أساعدك.
- guard_reason: passed
- semantic_match: True
- reason: passed

## new_definition_courage — FAIL

- bucket: new_topic
- prompt: اشرح الشجاعة
- response: اكتب ثلاث مهام وابدأ بالأهم.
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

## reg_friendship — FAIL

- bucket: regression
- prompt: ما معنى الصداقة
- response: الشجاعة أن ننجز معًا بدل الانفراد.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_truth — FAIL

- bucket: regression
- prompt: الصدق وش يعني
- response: يعني وقف وتوقف مع ف وتوقف تحفظ تثق فيه.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_order — FAIL

- bucket: regression
- prompt: ما معنى التنظيم
- response: الشجاعة أن ننجز معًا بدل الانفراد.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch

## reg_calm — FAIL

- bucket: regression
- prompt: الهدوء وش يعني
- response: يعني وقف وتوقف مع ف وتوقف تحفظ تثق فيه.
- guard_reason: passed
- semantic_match: False
- reason: semantic_mismatch
