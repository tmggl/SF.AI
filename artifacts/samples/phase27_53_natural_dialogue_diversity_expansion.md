# Phase 27.53 Natural Dialogue Diversity Expansion

## social_saudi_1 — PASS

- bucket: open_social
- dialect: saudi
- prompt: سولف معي شوي عن يومك
- response: خلنا نتكلم عن اليوم، ولا تنتظر : أهم شي تخليه قريب من حياتك مو كلام بعيد.
- overlap: 0.2
- reason: passed

## social_saudi_2 — FAIL

- bucket: open_social
- dialect: saudi
- prompt: هات سالفة خفيفة عن الشغل
- response: نقدر نًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.2
- reason: expected_terms_missing

## social_msa_1 — FAIL

- bucket: open_social
- dialect: msa
- prompt: أريد حديثًا خفيفًا عن القراءة
- response: نقدر نًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.2
- reason: expected_terms_missing

## social_msa_2 — FAIL

- bucket: open_social
- dialect: msa
- prompt: اقترح موضوعًا بسيطًا نتكلم عنه
- response: حسنًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## follow_saudi_1 — FAIL

- bucket: followup
- dialect: saudi
- prompt: يعني وش أسوي بعدها
- response: خفف الجملة قصيرة، ثم قل الفكرة الأساسية بلطف ووضوح.
- overlap: 0.0
- reason: expected_terms_missing

## follow_saudi_2 — FAIL

- bucket: followup
- dialect: saudi
- prompt: وضح لي أكثر بدون لف
- response: السبب، ثم ما تريد الوصول إليه.
- overlap: 0.0
- reason: expected_terms_missing

## follow_msa_1 — FAIL

- bucket: followup
- dialect: msa
- prompt: لم أفهم الفكرة جيدًا
- response: خلنا نتكلم عن شيء بسيط حدث في يومك، : أهم شي تخليه قريب من حياتك مباشرة، واشكر الشخص على وقته.
- overlap: 0.0
- reason: expected_terms_missing

## follow_msa_2 — FAIL

- bucket: followup
- dialect: msa
- prompt: ما الخطوة التالية
- response: فائدة الفكرة تظهر عندما يساعدك على فهم نفسك أو ترتب يومك بوضوح.
- overlap: 0.0
- reason: expected_terms_missing

## planning_saudi_1 — FAIL

- bucket: planning
- dialect: saudi
- prompt: يومي زحمة ومشاويري كثيرة
- response: ابدأ بما تستطيع فعله اليوم، ولا تنتظر أن تكون الظروف كاملة.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## planning_saudi_2 — FAIL

- bucket: planning
- dialect: saudi
- prompt: كيف أنظم وقتي بدون توتر
- response: اجعل الجملة قصيرة، واذكر الشيء المطلوب بدل الدوران حوله.
- overlap: 0.0
- reason: expected_terms_missing

## planning_msa_1 — FAIL

- bucket: planning
- dialect: msa
- prompt: لدي أعمال كثيرة ولا أعرف البداية
- response: لا بأس. ابدأ بكلمة واحدة عن شعورك الآن، وسأساعدك نرتبها.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## planning_msa_2 — FAIL

- bucket: planning
- dialect: msa
- prompt: ساعدني أرتب الدراسة هذا الأسبوع
- response: اكتب الفكرة الأولى، ثم السبب، ثم ما تريد الوصول إليه.
- overlap: 0.0
- reason: expected_terms_missing

## support_saudi_1 — FAIL

- bucket: support
- dialect: saudi
- prompt: حاس بضغط واحتاج تهدئة
- response: خلنا نتكلم عن شيء بسيط حدث في يومك، : أهم شي تخليه قريب من حياتك مباشرة، واشكر الشخص على وقته.
- overlap: 0.0
- reason: expected_terms_missing

## support_saudi_2 — FAIL

- bucket: support
- dialect: saudi
- prompt: متضايق شوي وش أسوي
- response: خفف الجملة قصيرة، ثم قل الفكرة الأساسية بلطف ووضوح.
- overlap: 0.0
- reason: expected_terms_missing

## support_msa_1 — FAIL

- bucket: support
- dialect: msa
- prompt: أشعر بتوتر وأحتاج كلامًا مطمئنًا
- response: خلنا نتكلم عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## support_msa_2 — FAIL

- bucket: support
- dialect: msa
- prompt: اليوم كان مرهقًا وأريد راحة
- response: خلنا نتكلم عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## writing_saudi_1 — FAIL

- bucket: writing
- dialect: saudi
- prompt: اكتب لي اعتذار لطيف لصديق
- response: تقدر تقول: هلا، حبيت أرسل لك نتيجة واضحة بسرعة. وأقربدون لف.
- overlap: 0.0
- reason: expected_terms_missing

## writing_saudi_2 — FAIL

- bucket: writing
- dialect: saudi
- prompt: صغ لي رد شكر قصير
- response: صيغة مناسبة: أقدّر أسهل عليك الحين وأقرب لاحتياجك؟
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## writing_msa_1 — FAIL

- bucket: writing
- dialect: msa
- prompt: اكتب لي طلب موعد بصيغة مهذبة
- response: تقدر تقول: هلا، حبيت أرسل لك نتيجة بدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## writing_msa_2 — FAIL

- bucket: writing
- dialect: msa
- prompt: كيف أرد على مجاملة جميلة
- response: اجعل الجملة قصيرة، واذكر الشيء المطلوب بدل الدوران حوله.
- overlap: 0.0
- reason: expected_terms_missing

## decision_saudi_1 — FAIL

- bucket: decision
- dialect: saudi
- prompt: أرتاح شوي ولا أبدأ الحين
- response: حسنًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## decision_saudi_2 — FAIL

- bucket: decision
- dialect: saudi
- prompt: أرسل الرسالة الحين ولا أنتظر
- response: خلنا نتكلم عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## decision_msa_1 — FAIL

- bucket: decision
- dialect: msa
- prompt: هل أقرأ قليلًا أم أمشي عشر دقائق
- response: حسنًا. أخبرني عن شيء بسيط حدث في يومك، ونبدأ منه.
- overlap: 0.0
- reason: expected_terms_missing

## decision_msa_2 — FAIL

- bucket: decision
- dialect: msa
- prompt: أجهز للغد أم أنهي عمل اليوم
- response: لا بأس. ابدأ بكلمة واحدة عن شعورك الآن، وسأساعدك نرتبها.
- overlap: 0.0
- reason: expected_terms_missing

## topic_saudi_1 — FAIL

- bucket: topic
- dialect: saudi
- prompt: تكلم عن الوفاء بمثال قريب
- response: خلنا نتكلم عن وقت: أهم شي تخليه قريب من حياتك مو كلام بعيد.
- overlap: 0.4
- reason: expected_terms_missing

## topic_saudi_2 — FAIL

- bucket: topic
- dialect: saudi
- prompt: وش فايدة الهدوء في التعامل
- response: خفف حوله.
- overlap: 0.0
- reason: expected_terms_missing

## topic_msa_1 — FAIL

- bucket: topic
- dialect: msa
- prompt: حدثني عن الشجاعة دون تعقيد
- response: ابدأ بتحية قصيرة، ثم قل الفكرة الأساسية بلطف ووضوح.
- overlap: 0.0
- reason: expected_terms_missing

## topic_msa_2 — FAIL

- bucket: topic
- dialect: msa
- prompt: أعطني مثالًا عن الاحترام
- response: خلنا نتكلم عن الأكلأهم شي تخليه قريب من حياتك مو كلام بعيد.
- overlap: 0.25
- reason: expected_terms_missing

## learning_saudi_1 — FAIL

- bucket: learning
- dialect: saudi
- prompt: علمني طريقة بسيطة لتحسين التركيز
- response: ابدأ بتحسين الوقت بخطوة صغيرة كل يوم، وزدها إذا صارت سهلة.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## learning_saudi_2 — FAIL

- bucket: learning
- dialect: saudi
- prompt: كيف أتعلم القراءة بشكل أحسن
- response: اجعل الجملة قصيرة، واذكر الشيء المطلوب بدل الدوران حوله.
- overlap: 0.0
- reason: expected_terms_missing

## learning_msa_1 — FAIL

- bucket: learning
- dialect: msa
- prompt: كيف أحسن عاداتي بهدوء
- response: اجعل الجملة قصيرة، واذكر الشيء المطلوب بدل الدوران حوله.
- overlap: 0.0
- reason: expected_terms_missing

## learning_msa_2 — FAIL

- bucket: learning
- dialect: msa
- prompt: اشرح لي طريقة بسيطة للمذاكرة
- response: السبب، ثم ما تريد الوصول إليه.
- overlap: 0.0
- reason: expected_terms_missing

## general_saudi_1 — FAIL

- bucket: open_general
- dialect: saudi
- prompt: مدري وش أقول بس ودي أتكلم
- response: خفف حوله.
- overlap: 0.0
- reason: expected_terms_missing

## general_saudi_2 — FAIL

- bucket: open_general
- dialect: saudi
- prompt: أبي نصيحة عامة تنفعني اليوم
- response: ابدأ بما تستطيع فعله اليوم، ولا تنتظر أن تكون الظروف كاملة.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## general_msa_1 — PASS

- bucket: open_general
- dialect: msa
- prompt: لا أعرف كيف أبدأ الكلام
- response: لا بأس. ابدأ بكلمة واحدة عن شعورك الآن، وسأساعدك نرتبها.
- overlap: 0.4
- reason: passed

## general_msa_2 — FAIL

- bucket: open_general
- dialect: msa
- prompt: أحتاج ردًا قصيرًا ومهذبًا
- response: قل: شكرًا لك، وصلتني فكرتك، وسأرد عليك قريبًا.
- overlap: 0.0
- reason: low_prompt_overlap:0.00
