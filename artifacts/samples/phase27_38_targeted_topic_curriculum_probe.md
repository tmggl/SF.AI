# Phase 27.38 Targeted Topic Curriculum/Probe

## reg_001 — PASS

- bucket: regression
- prompt: كيفك اليوم
- topic: -
- response: بخير، شكرًا لسؤالك.
- reason: passed

## reg_002 — PASS

- bucket: regression
- prompt: شكرًا لمساعدتك
- topic: -
- response: العفو، يسعدني أن أساعدك.
- reason: passed

## reg_003 — PASS

- bucket: regression
- prompt: وجهني بخطوة بسيطة
- topic: -
- response: ابدأ بخطوة صغيرة وواضحة.
- reason: passed

## reg_004 — PASS

- bucket: regression
- prompt: رتب لي يومي بسرعة
- topic: -
- response: اكتب ثلاث مهام وابدأ بالأهم.
- reason: passed

## reg_005 — PASS

- bucket: regression
- prompt: توترت شوي وش اسوي
- topic: -
- response: الله يهونها، خذ نفس واهدأ شوي.
- reason: passed

## reg_006 — PASS

- bucket: regression
- prompt: وش المقصود بالاحترام
- topic: الاحترام
- response: يعني تقدّر الناس بكلامك وتصرفك.
- reason: passed

## reg_007 — FAIL

- bucket: regression
- prompt: ما معنى التعاون
- topic: التعاون
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## reg_008 — FAIL

- bucket: regression
- prompt: ما معنى الصبر
- topic: الصبر
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## new_001 — FAIL

- bucket: new_topic
- prompt: ما معنى الصداقة
- topic: الصداقة
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## new_002 — FAIL

- bucket: new_topic
- prompt: وش معنى الصداقة
- topic: الصداقة
- response: يعني تقدّر الناس بكلامك وتصرفك.
- reason: semantic_mismatch

## new_003 — FAIL

- bucket: new_topic
- prompt: اشرح الصدق بجملة
- topic: الصدق
- response: خذ نفسًا هادئًا واهدأ خطوة الناس بالكلام والفعل.
- reason: semantic_mismatch

## new_004 — FAIL

- bucket: new_topic
- prompt: وش معنى الصدق
- topic: الصدق
- response: يعني كلامك وتصرفك.
- reason: semantic_mismatch

## new_005 — FAIL

- bucket: new_topic
- prompt: ما معنى التنظيم
- topic: التنظيم
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## new_006 — FAIL

- bucket: new_topic
- prompt: وش معنى التنظيم
- topic: التنظيم
- response: يعني تقدّر الناس بكلامك وتصرفك.
- reason: semantic_mismatch

## new_007 — FAIL

- bucket: new_topic
- prompt: ما معنى الهدوء
- topic: الهدوء
- response: اكتب تقدير القراءة توسع الفهم وتزيد المفردات.
- reason: semantic_mismatch

## new_008 — FAIL

- bucket: new_topic
- prompt: وش معنى الهدوء
- topic: الهدوء
- response: يعني تقدّر الناس بكلامك وتصرفك.
- reason: semantic_mismatch

## held_001 — FAIL

- bucket: heldout
- prompt: الصداقة ماذا تعني
- topic: الصداقة
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## held_002 — FAIL

- bucket: heldout
- prompt: الصدق وش يعني
- topic: الصدق
- response: الله يهونها، خذ نفس واهدأ شوي.
- reason: semantic_mismatch

## held_003 — FAIL

- bucket: heldout
- prompt: اشرح التنظيم ببساطة
- topic: التنظيم
- response: الاحترام تقدير الناس بالكلام والفعل.
- reason: semantic_mismatch

## held_004 — FAIL

- bucket: heldout
- prompt: الهدوء وش يعني
- topic: الهدوء
- response: يعني تقدّر الناس بكلامك وتصرفك.
- reason: semantic_mismatch
