# Phase 27.39 Topic-Isolation Repair

## reg_001 — FAIL

- bucket: regression
- prompt: كيفك اليوم
- topic: -
- response: ابدأ بشي بسيط وواضح.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: guard:social_smalltalk_mismatch

## reg_002 — FAIL

- bucket: regression
- prompt: شكرًا لمساعدتك
- topic: -
- response: ابدأ بخطوة صغيرة ثم ة تساعدك على الاحتمال.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: guard:thanks_mismatch

## reg_003 — PASS

- bucket: regression
- prompt: وجهني بخطوة بسيطة
- topic: -
- response: ابدأ بخطوة صغيرة وواضحة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_004 — FAIL

- bucket: regression
- prompt: رتب لي يومي بسرعة
- topic: -
- response: القراءة طريق التول.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## reg_005 — FAIL

- bucket: regression
- prompt: توترت شوي وش اسوي
- topic: -
- response: خذ الأموقت الحاجة.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## reg_006 — PASS

- bucket: regression
- prompt: وش المقصود بالاحترام
- topic: الاحترام
- response: الاحترام إنك تقدّر الناس بكلامك وتصرفك.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_007 — PASS

- bucket: regression
- prompt: ما معنى التعاون
- topic: التعاون
- response: التعاون يعني أن يعمل الناس معًا لتخفيف الحمل.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_008 — PASS

- bucket: regression
- prompt: ما معنى الصبر
- topic: الصبر
- response: الصبر يعني الثبات وقت الصعوبة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_001 — FAIL

- bucket: new_topic
- prompt: ما معنى الصداقة
- topic: الصداقة
- response: الصداعلاقة طيبة تقوم على الوفاء.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## new_002 — FAIL

- bucket: new_topic
- prompt: وش معنى الصداقة
- topic: الصداقة
- response: الصداطيقة إنك تلقى رفيق يوقف معك.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## new_003 — FAIL

- bucket: new_topic
- prompt: اشرح الصدق بجملة
- topic: الصدق
- response: الصد راالقول والعمل.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## new_004 — FAIL

- bucket: new_topic
- prompt: وش معنى الصدق
- topic: الصدق
- response: الصدك وتلتزم والعموما فيه خداع.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## new_005 — FAIL

- bucket: new_topic
- prompt: ما معنى التنظيم
- topic: التنظيم
- response: التنيعترتيب الوقت والمهام بطريقة واضحة.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## new_006 — PASS

- bucket: new_topic
- prompt: وش معنى التنظيم
- topic: التنظيم
- response: التنق إنك ترتب وقتك ومهامك بوضوح.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_007 — FAIL

- bucket: new_topic
- prompt: ما معنى الهدوء
- topic: الهدوء
- response: الهدوء: القراءة طريوتات.
- semantic_match: True
- topic_isolated: False
- forbidden_topics: القراءة
- reason: topic_leakage

## new_008 — PASS

- bucket: new_topic
- prompt: وش معنى الهدوء
- topic: الهدوء
- response: الهدوءالنتخفف تفيدك وتتكلم بروية.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_001 — FAIL

- bucket: heldout
- prompt: الصداقة ماذا تعني
- topic: الصداقة
- response: الصداوقمودة ووفاء بين الناس.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## held_002 — PASS

- bucket: heldout
- prompt: الصدق وش يعني
- topic: الصدق
- response: الصدترتب يعني تقول الحقيقة بوضوح.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_003 — FAIL

- bucket: heldout
- prompt: اشرح التنظيم ببساطة
- topic: التنظيم
- response: التنق وضوح ما تفعل ومتى تبدأ.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## held_004 — FAIL

- bucket: heldout
- prompt: الهدوء وش يعني
- topic: الهدوء
- response: الهدوءتوسع فهمك وتزيد كلماتك.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## iso_001 — PASS

- bucket: isolation
- prompt: اشرح القراءة بجملة
- topic: القراءة
- response: القراءة طريق لاكتساب معرفة جديدة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## iso_002 — FAIL

- bucket: isolation
- prompt: القراية وش تعني
- topic: القراءة
- response: القرافا يعني تخفف توترك وتتكلم بروية.
- semantic_match: False
- topic_isolated: True
- forbidden_topics: -
- reason: semantic_mismatch

## iso_003 — PASS

- bucket: isolation
- prompt: اشرح الاحترام بجملة
- topic: الاحترام
- response: الاحترام معاملة الناس بقدر وذوق.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## iso_004 — PASS

- bucket: isolation
- prompt: فسر التعاون بالسعودي
- topic: التعاون
- response: التعاون إنك تساعد غيرك وتنجزون سوا.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed
