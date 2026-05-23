# Phase 27.19 Hygiene Repair Probe Generations

## phase27_17_msa_001 — msa — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، أهلًا بك.
- generated: وعليكالسلم، أهلًا بك.
- exact_clean: False
- semantic_match: False
- reason: guard:greeting_mismatch

## phase27_17_msa_002 — msa — PASS

- prompt: كيف حالك اليوم
- expected: بخير، شكرًا لسؤالك.
- generated: بخير، شكرًا لسؤالك.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_003 — msa — PASS

- prompt: أريد نصيحة قصيرة
- expected: ابدأ بخطوة صغيرة وواضحة.
- generated: ابدأ بخطوة صغيرة وواضحة.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_004 — msa — PASS

- prompt: ما معنى الصبر
- expected: الصبر هو الثبات عند الصعوبة.
- generated: الصبر هو الثبات عند الصعوبة.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_005 — msa — PASS

- prompt: أشعر بتوتر بسيط
- expected: خذ نفسًا هادئًا وابدأ بالأهم.
- generated: خذ نفسًا هادئًا وابدأ بالأهم.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_006 — msa — PASS

- prompt: أريد ترتيب يومي
- expected: اكتب ثلاث مهام وابدأ بالأقرب.
- generated: اكتب ثلاث مهام وابدأ بالأقرب.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_007 — msa — PASS

- prompt: هل تفهم كلامي
- expected: نعم، أفهم كلامك وأرد بوضوح.
- generated: نعم، أفهم كلامك وأرد بوضوح.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_008 — msa — FAIL

- prompt: اشرح لي التعاون
- expected: التعاون يعني أن ننجز معًا بدل الانفراد.
- generated: التعاي واحد بسيط ولا تكثرها.
- exact_clean: False
- semantic_match: False
- reason: missing_semantic_terms

## phase27_17_msa_009 — msa — FAIL

- prompt: ماذا أفعل عند الزحمة
- expected: اخرج مبكرًا واترك وقتًا إضافيًا.
- generated: اخرج مبكرًا واترك وقتًا إضافيًا.
- exact_clean: True
- semantic_match: True
- reason: guard:model_artifact_fragment

## phase27_17_msa_010 — msa — PASS

- prompt: كيف أتعلم عادة جديدة
- expected: كررها يوميًا ولو لمدة قصيرة.
- generated: كررها يوميًا ولو لمدة قصيرة.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_011 — msa — FAIL

- prompt: ما فائدة القراءة
- expected: القراءة توسع الفهم وتزيد المفردات.
- generated: القراراءراءتفيد وتزيد المفردات.
- exact_clean: False
- semantic_match: False
- reason: guard:malformed_token

## phase27_17_msa_012 — msa — PASS

- prompt: أريد جوابا مختصرا
- expected: نعم، سأجيبك باختصار.
- generated: نعم، سأجيبك باختصار.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_013 — msa — PASS

- prompt: كيف أهدأ قبل النوم
- expected: خفف الإضاءة واترك الهاتف قليلًا.
- generated: خفف الإضاءة واترك الهاتف قليلًا.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_014 — msa — PASS

- prompt: ما معنى الاحترام
- expected: الاحترام تقدير الناس بالكلام والفعل.
- generated: الاحترام تقدير الناس بالكلام والفعل.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_015 — msa — PASS

- prompt: أريد تشجيعا بسيطا
- expected: أنت قادر، ابدأ ولا تنتظر الكمال.
- generated: أنت قادر، ابدأ ولا تنتظر الكمال.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_msa_016 — msa — PASS

- prompt: شكرا لك
- expected: العفو، يسعدني أن أساعدك.
- generated: العفو، يسعدني أن أساعدك.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_001 — saudi — FAIL

- prompt: هلا والله
- expected: هلا بك، تفضل وش تحتاج؟
- generated: هون، حاضر بأي وقت.
- exact_clean: False
- semantic_match: False
- reason: missing_semantic_terms

## phase27_17_saudi_002 — saudi — PASS

- prompt: كيفك
- expected: بخير ولله الحمد، أنت كيفك؟
- generated: بخير ولله الحمد، أنت كيفك؟
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_003 — saudi — PASS

- prompt: وش تنصحني اليوم
- expected: ابدأ بشي واحد بسيط ولا تكثرها.
- generated: ابدأ بشي واحد بسيط ولا تكثرها.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_004 — saudi — PASS

- prompt: وش معنى الصبر
- expected: الصبر إنك تثبت وقت الصعوبة.
- generated: الصبر إنك تثبت وقت الصعوبة.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_005 — saudi — PASS

- prompt: متضايق شوي
- expected: الله يهونها، خذ نفس واهدأ شوي.
- generated: الله يهونها، خذ نفس واهدأ شوي.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_006 — saudi — PASS

- prompt: ابي ارتب يومي
- expected: اكتب أهم ثلاث أشياء وابدأ بالأول.
- generated: اكتب أهم ثلاث أشياء وابدأ بالأول.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_007 — saudi — PASS

- prompt: تفهم كلامي
- expected: إيه أفهمك، وبرد عليك بوضوح.
- generated: إيه أفهمك، وبرد عليك بوضوح.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_008 — saudi — PASS

- prompt: وش يعني تعاون
- expected: يعني نشتغل سوا ونخفف الحمل.
- generated: يعني نشتغل سوا ونخفف الحمل.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_009 — saudi — PASS

- prompt: الزحمة تعبتني
- expected: اطلع بدري وخل عندك وقت زيادة.
- generated: اطلع بدري وخل عندك وقت زيادة.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_010 — saudi — PASS

- prompt: ابي اتعلم عادة
- expected: كررها كل يوم حتى لو شوي.
- generated: كررها كل يوم حتى لو شوي.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_011 — saudi — PASS

- prompt: القراءة وش تفيد
- expected: توسع فهمك وتزيد كلماتك.
- generated: توسع فهمك وتزيد كلماتك.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_012 — saudi — PASS

- prompt: ابي جواب قصير
- expected: تم، بعطيك جواب مختصر.
- generated: تم، بعطيك جواب مختصر.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_013 — saudi — PASS

- prompt: ما انام بسرعة
- expected: خفف الجوال وخلي الجو أهدأ.
- generated: خفف الجوال وخلي الجو أهدأ.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_014 — saudi — PASS

- prompt: وش معنى الاحترام
- expected: يعني تقدّر الناس بكلامك وتصرفك.
- generated: يعني تقدّر الناس بكلامك وتصرفك.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_015 — saudi — PASS

- prompt: حمسني بكلمة
- expected: تقدر، ابدأ بخطوة ولا توقف.
- generated: تقدر، ابدأ بخطوة ولا توقف.
- exact_clean: True
- semantic_match: True
- reason: passed

## phase27_17_saudi_016 — saudi — PASS

- prompt: مشكور
- expected: العفو، حاضر بأي وقت.
- generated: العفو، حاضر بأي وقت.
- exact_clean: True
- semantic_match: True
- reason: passed
