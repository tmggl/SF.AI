# Phase 27.40 Tokenizer/Context Repair

## reg_001 — PASS

- bucket: regression
- prompt: كيفك اليوم
- topic: -
- response: بخير ولله الحمد، أنت كيفك؟
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_002 — PASS

- bucket: regression
- prompt: شكرًا لمساعدتك
- topic: -
- response: العفو، يسعدني أن أساعدك.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_003 — PASS

- bucket: regression
- prompt: وجهني بخطوة بسيطة
- topic: -
- response: ابدأ بخطوة صغيرة وواضحة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_004 — PASS

- bucket: regression
- prompt: رتب لي يومي بسرعة
- topic: -
- response: اكتب ثلاث مهام وابدأ بالأهم.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## reg_005 — PASS

- bucket: regression
- prompt: توترت شوي وش اسوي
- topic: -
- response: الله يهونها، خذ نفس واهدأ شوي.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

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

## new_001 — PASS

- bucket: new_topic
- prompt: ما معنى الصداقة
- topic: الصداقة
- response: الصداقة علاقة طيبة تقوم على الوفاء.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_002 — PASS

- bucket: new_topic
- prompt: وش معنى الصداقة
- topic: الصداقة
- response: الصداقة إنك تلقى رفيق يوقف معك.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_003 — PASS

- bucket: new_topic
- prompt: اشرح الصدق بجملة
- topic: الصدق
- response: الصدق وضوح في القول والعمل.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_004 — PASS

- bucket: new_topic
- prompt: وش معنى الصدق
- topic: الصدق
- response: الصدق إن كلامك يكون واضح وما فيه خداع.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_005 — PASS

- bucket: new_topic
- prompt: ما معنى التنظيم
- topic: التنظيم
- response: التنظيم ترتيب الوقت والمهام بطريقة واضحة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_006 — PASS

- bucket: new_topic
- prompt: وش معنى التنظيم
- topic: التنظيم
- response: التنظيم إنك ترتب وقتك ومهامك بوضوح.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_007 — PASS

- bucket: new_topic
- prompt: ما معنى الهدوء
- topic: الهدوء
- response: الهدوء سكينة تساعدك على التفكير بوضوح.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## new_008 — PASS

- bucket: new_topic
- prompt: وش معنى الهدوء
- topic: الهدوء
- response: الهدوء إنك تهدأ وتاخذ الأمور بروية.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_001 — PASS

- bucket: heldout
- prompt: الصداقة ماذا تعني
- topic: الصداقة
- response: الصداقة مودة ووفاء بين الناس.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_002 — PASS

- bucket: heldout
- prompt: الصدق وش يعني
- topic: الصدق
- response: الصدق يعني تقول الحقيقة بوضوح.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_003 — PASS

- bucket: heldout
- prompt: اشرح التنظيم ببساطة
- topic: التنظيم
- response: التنظيم معرفة ما تفعل ومتى تبدأ.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## held_004 — PASS

- bucket: heldout
- prompt: الهدوء وش يعني
- topic: الهدوء
- response: الهدوء يعني تخفف توترك وتتكلم بروية.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## iso_001 — PASS

- bucket: isolation
- prompt: اشرح القراءة بجملة
- topic: القراءة
- response: القراءة طريق لاكتساب معرفة جديدة.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

## iso_002 — PASS

- bucket: isolation
- prompt: القراية وش تعني
- topic: القراءة
- response: القراية توسع فهمك وتزيد كلماتك.
- semantic_match: True
- topic_isolated: True
- forbidden_topics: -
- reason: passed

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
