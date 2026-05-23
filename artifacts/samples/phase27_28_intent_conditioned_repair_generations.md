# Phase 27.28 Intent-Conditioned Repair Generations

## Held-out 27.25 Canary

### phase27_25_msa_001 — msa — greeting — PASS

- prompt: حيّني بتحية قصيرة
- generated: أهلًا بك.
- reason: passed

### phase27_25_msa_002 — msa — smalltalk — PASS

- prompt: كيف حالك الآن
- generated: بخير، شكرًا لسؤالك.
- reason: passed

### phase27_25_msa_003 — msa — definition — PASS

- prompt: اشرح التعاون بجملة
- generated: التعاون يعني أن ننجز معًا بدل الانفراد.
- reason: passed

### phase27_25_msa_004 — msa — definition — PASS

- prompt: عرّف الاحترام باختصار
- generated: الاحترام تقدير الناس بالكلام والفعل.
- reason: passed

### phase27_25_msa_005 — msa — definition — PASS

- prompt: ما فائدة القراءة باختصار
- generated: القراءة توسع الفهم وتزيد المفردات.
- reason: passed

### phase27_25_msa_006 — msa — advice — PASS

- prompt: أحتاج نصيحة بسيطة
- generated: ابدأ بخطوة صغيرة وواضحة.
- reason: passed

### phase27_25_msa_007 — msa — planning — PASS

- prompt: كيف أرتب يومي
- generated: اكتب ثلاث مهام وابدأ بالأهم.
- reason: passed

### phase27_25_msa_008 — msa — support — PASS

- prompt: أشعر بالقلق
- generated: خذ نفسًا هادئًا واهدأ خطوة خطوة.
- reason: passed

### phase27_25_saudi_001 — saudi — greeting — PASS

- prompt: هلا كيف الحال
- generated: هلا بك، تفضل وش تحتاج؟
- reason: passed

### phase27_25_saudi_002 — saudi — definition — PASS

- prompt: وش معنى التعاون
- generated: يعني نشتغل سوا ونخفف الحمل.
- reason: passed

### phase27_25_saudi_003 — saudi — definition — PASS

- prompt: اشرح الاحترام
- generated: يعني تقدّر الناس بكلامك وتصرفك.
- reason: passed

### phase27_25_saudi_004 — saudi — definition — PASS

- prompt: وش فايدة القراءة
- generated: توسع فهمك وتزيد كلماتك.
- reason: passed

### phase27_25_saudi_005 — saudi — advice — PASS

- prompt: ابي نصيحة سريعة
- generated: ابدأ بشي بسيط ولا تكثرها.
- reason: passed

### phase27_25_saudi_006 — saudi — planning — PASS

- prompt: ودي ارتب يومي
- generated: اكتب أهم ثلاث أشياء وابدأ بالأول.
- reason: passed

### phase27_25_saudi_007 — saudi — support — PASS

- prompt: متوتر شوي
- generated: الله يهونها، خذ نفس واهدأ شوي.
- reason: passed

### phase27_25_saudi_008 — saudi — thanks — PASS

- prompt: مشكور يا بعدي
- generated: العفو، حاضر بأي وقت.
- reason: passed

## Fresh Shadow 27.27 Canary

### phase27_27_shadow_msa_001 — msa — greeting — PASS

- prompt: ابدأ معي بتحية لطيفة
- generated: أهلًا بك.
- reason: passed

### phase27_27_shadow_msa_002 — msa — smalltalk — PASS

- prompt: كيف وضعك الآن
- generated: بخير، شكرًا لسؤالك.
- reason: passed

### phase27_27_shadow_msa_003 — msa — definition — FAIL

- prompt: عرّف التعاون في عبارة
- generated: الاحترام تقدير الناس بالكلام والفعل.
- reason: missing_semantic_terms

### phase27_27_shadow_msa_004 — msa — definition — FAIL

- prompt: ما المقصود بالاحترام باختصار
- generated: أهلًا بك.
- reason: missing_semantic_terms

### phase27_27_shadow_msa_005 — msa — definition — PASS

- prompt: اذكر فائدة القراءة سريعًا
- generated: القراءة توسع الفهم وتزيد المفردات.
- reason: passed

### phase27_27_shadow_msa_006 — msa — advice — PASS

- prompt: أعطني نصيحة خفيفة
- generated: ابدأ بخطوة صغيرة ثم أكمل.
- reason: passed

### phase27_27_shadow_msa_007 — msa — planning — PASS

- prompt: كيف أرتب مهامي اليوم
- generated: اكتب ثلاث مهام وابدأ بالأقرب.
- reason: passed

### phase27_27_shadow_msa_008 — msa — support — PASS

- prompt: أنا متوتر قليلًا
- generated: خذ نفسًا هادئًا واهدأ خطوة خطوة.
- reason: passed

### phase27_27_shadow_saudi_001 — saudi — greeting — PASS

- prompt: هلا وش أقدر أقول
- generated: هلا بك، تفضل وش تحتاج؟
- reason: passed

### phase27_27_shadow_saudi_002 — saudi — definition — FAIL

- prompt: التعاون وش يقصدون فيه
- generated: العفو، حاضر بأي وقت.
- reason: missing_semantic_terms

### phase27_27_shadow_saudi_003 — saudi — definition — FAIL

- prompt: الاحترام وش يعني
- generated: العفو، حاضر بأي وقت.
- reason: missing_semantic_terms

### phase27_27_shadow_saudi_004 — saudi — definition — PASS

- prompt: وش أستفيد من القراءة
- generated: توسع فهمك وتزيد كلماتك.
- reason: passed

### phase27_27_shadow_saudi_005 — saudi — advice — PASS

- prompt: عطني نصيحة بسيطة
- generated: ابدأ بشي بسيط ولا تكثرها.
- reason: passed

### phase27_27_shadow_saudi_006 — saudi — planning — PASS

- prompt: ابي أرتب مهامي
- generated: اكتب أهم ثلاث أشياء وابدأ بالأول.
- reason: passed

### phase27_27_shadow_saudi_007 — saudi — support — PASS

- prompt: حاس بتوتر شوي
- generated: الله يهونها، خذ نفس واهدأ شوي.
- reason: passed

### phase27_27_shadow_saudi_008 — saudi — thanks — PASS

- prompt: يعطيك العافية
- generated: العفو، حاضر بأي وقت.
- reason: passed

## Micro-Probe Regression

### phase27_17_msa_001 — msa — micro — PASS

- prompt: السلام عليكم
- generated: وعليكم السلام، أهلًا بك.
- reason: passed

### phase27_17_msa_002 — msa — micro — PASS

- prompt: كيف حالك اليوم
- generated: بخير، شكرًا لسؤالك.
- reason: passed

### phase27_17_msa_003 — msa — micro — PASS

- prompt: أريد نصيحة قصيرة
- generated: ابدأ بخطوة صغيرة وواضحة.
- reason: passed

### phase27_17_msa_004 — msa — micro — PASS

- prompt: ما معنى الصبر
- generated: الصبر هو الثبات عند الصعوبة.
- reason: passed

### phase27_17_msa_005 — msa — micro — PASS

- prompt: أشعر بتوتر بسيط
- generated: خذ نفسًا هادئًا وابدأ بالأهم.
- reason: passed

### phase27_17_msa_006 — msa — micro — PASS

- prompt: أريد ترتيب يومي
- generated: اكتب ثلاث مهام وابدأ بالأقرب.
- reason: passed

### phase27_17_msa_007 — msa — micro — PASS

- prompt: هل تفهم كلامي
- generated: نعم، أفهم كلامك وأرد بوضوح.
- reason: passed

### phase27_17_msa_008 — msa — micro — PASS

- prompt: اشرح لي التعاون
- generated: التعاون يعني أن ننجز معًا بدل الانفراد.
- reason: passed

### phase27_17_msa_009 — msa — micro — PASS

- prompt: ماذا أفعل عند الزحمة
- generated: اخرج مبكرًا واترك وقتًا إضافيًا.
- reason: passed

### phase27_17_msa_010 — msa — micro — PASS

- prompt: كيف أتعلم عادة جديدة
- generated: كررها يوميًا ولو لمدة قصيرة.
- reason: passed

### phase27_17_msa_011 — msa — micro — PASS

- prompt: ما فائدة القراءة
- generated: القراءة توسع الفهم وتزيد المفردات.
- reason: passed

### phase27_17_msa_012 — msa — micro — PASS

- prompt: أريد جوابا مختصرا
- generated: نعم، سأجيبك باختصار.
- reason: passed

### phase27_17_msa_013 — msa — micro — PASS

- prompt: كيف أهدأ قبل النوم
- generated: خفف الإضاءة واترك الهاتف قليلًا.
- reason: passed

### phase27_17_msa_014 — msa — micro — PASS

- prompt: ما معنى الاحترام
- generated: الاحترام تقدير الناس بالكلام والفعل.
- reason: passed

### phase27_17_msa_015 — msa — micro — PASS

- prompt: أريد تشجيعا بسيطا
- generated: أنت قادر، ابدأ ولا تنتظر الكمال.
- reason: passed

### phase27_17_msa_016 — msa — micro — PASS

- prompt: شكرا لك
- generated: العفو، يسعدني أن أساعدك.
- reason: passed

### phase27_17_saudi_001 — saudi — micro — PASS

- prompt: هلا والله
- generated: هلا بك، تفضل وش تحتاج؟
- reason: passed

### phase27_17_saudi_002 — saudi — micro — PASS

- prompt: كيفك
- generated: بخير ولله الحمد، أنت كيفك؟
- reason: passed

### phase27_17_saudi_003 — saudi — micro — PASS

- prompt: وش تنصحني اليوم
- generated: ابدأ بشي واحد بسيط ولا تكثرها.
- reason: passed

### phase27_17_saudi_004 — saudi — micro — PASS

- prompt: وش معنى الصبر
- generated: الصبر إنك تثبت وقت الصعوبة.
- reason: passed

### phase27_17_saudi_005 — saudi — micro — PASS

- prompt: متضايق شوي
- generated: الله يهونها، خذ نفس واهدأ شوي.
- reason: passed

### phase27_17_saudi_006 — saudi — micro — PASS

- prompt: ابي ارتب يومي
- generated: اكتب أهم ثلاث أشياء وابدأ بالأول.
- reason: passed

### phase27_17_saudi_007 — saudi — micro — PASS

- prompt: تفهم كلامي
- generated: إيه أفهمك، وبرد عليك بوضوح.
- reason: passed

### phase27_17_saudi_008 — saudi — micro — PASS

- prompt: وش يعني تعاون
- generated: يعني نشتغل سوا ونخفف الحمل.
- reason: passed

### phase27_17_saudi_009 — saudi — micro — PASS

- prompt: الزحمة تعبتني
- generated: اطلع بدري وخل عندك وقت زيادة.
- reason: passed

### phase27_17_saudi_010 — saudi — micro — PASS

- prompt: ابي اتعلم عادة
- generated: كررها كل يوم حتى لو شوي.
- reason: passed

### phase27_17_saudi_011 — saudi — micro — PASS

- prompt: القراءة وش تفيد
- generated: توسع فهمك وتزيد كلماتك.
- reason: passed

### phase27_17_saudi_012 — saudi — micro — PASS

- prompt: ابي جواب قصير
- generated: تم، بعطيك جواب مختصر.
- reason: passed

### phase27_17_saudi_013 — saudi — micro — PASS

- prompt: ما انام بسرعة
- generated: خفف الجوال وخلي الجو أهدأ.
- reason: passed

### phase27_17_saudi_014 — saudi — micro — PASS

- prompt: وش معنى الاحترام
- generated: يعني تقدّر الناس بكلامك وتصرفك.
- reason: passed

### phase27_17_saudi_015 — saudi — micro — PASS

- prompt: حمسني بكلمة
- generated: تقدر، ابدأ بخطوة ولا توقف.
- reason: passed

### phase27_17_saudi_016 — saudi — micro — PASS

- prompt: مشكور
- generated: العفو، حاضر بأي وقت.
- reason: passed
