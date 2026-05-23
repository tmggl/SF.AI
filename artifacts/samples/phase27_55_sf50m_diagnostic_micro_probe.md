# Phase 27.55 SF-50M Diagnostic Micro-Probe

## sf-10m — 3/20

### followup_free_choice — FAIL

- bucket: followup
- dialect: saudi
- prompt: الي تحب
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.0
- reason: expected_terms_missing

### followup_continue — FAIL

- bucket: followup
- dialect: msa
- prompt: كمل كلامك
- response: ابدأ بكل سرور. أخبرني عن يومك أو عن فكرة تشغل بالك.
- overlap: 0.0
- reason: expected_terms_missing

### followup_why — FAIL

- bucket: followup
- dialect: saudi
- prompt: طيب ليه؟
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.0
- reason: expected_terms_missing

### followup_meaning — FAIL

- bucket: followup
- dialect: saudi
- prompt: يعني كيف؟
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.0
- reason: expected_terms_missing

### social_chat — FAIL

- bucket: open_social
- dialect: saudi
- prompt: سولف معي شوي
- response: حياك. نقدر نسولف عن يومك أو عن شيء خفيف تحبه.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### social_topic_choice — FAIL

- bucket: open_social
- dialect: saudi
- prompt: وش ودك نسولف عنه؟
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.25
- reason: expected_terms_missing

### social_new_topic — FAIL

- bucket: open_social
- dialect: msa
- prompt: هات موضوع خفيف
- response: ابدأ بكل شيء دفعة واحدة.
- overlap: 0.0
- reason: guard:corpus_artifact

### social_today — FAIL

- bucket: open_social
- dialect: saudi
- prompt: يومي كان طويل
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.0
- reason: expected_terms_missing

### topic_courage_simple — PASS

- bucket: topic
- dialect: msa
- prompt: اخبرني عن الشجاعة بأسلوب بسيط
- response: الشجاعة إنك تواجه الموقف الصحيح رغم وجود الخوف.
- overlap: 0.2
- reason: passed

### topic_friendship_talk — FAIL

- bucket: topic
- dialect: saudi
- prompt: وش رأيك نتكلم عن الصداقة
- response: ابدأ بشي واحد واضح، وبعده قيّم وش صار.
- overlap: 0.2
- reason: expected_terms_missing

### topic_honesty_example — FAIL

- bucket: topic
- dialect: msa
- prompt: اعطني مثال بسيط عن الصدق
- response: ابدأ من نقطة واحدة ولا تختار خطوة تفتح كل شيء مرة وحدة.
- overlap: 0.0
- reason: expected_terms_missing

### topic_calm_life — FAIL

- bucket: topic
- dialect: saudi
- prompt: الهدوء في اليوم وش يفيدني؟
- response: أنت مو مطالب تحل كل شيء الآن. اهدأ وخذ دقيقة لنفسك.
- overlap: 0.0
- reason: expected_terms_missing

### planning_day_start — PASS

- bucket: planning
- dialect: msa
- prompt: اشرح لي كيف ابدأ يومي
- response: ابدأ بمهمة واحدة واضحة، ولا تفتح كل الأعمال في وقت واحد.
- overlap: 0.2
- reason: passed

### planning_confused — PASS

- bucket: planning
- dialect: saudi
- prompt: أنا محتار من وين أبدأ
- response: ابدأ بمهمة واحدة واضحة، ولا تفتح كل الأعمال في وقت واحد.
- overlap: 0.2
- reason: passed

### planning_many_tasks — FAIL

- bucket: planning
- dialect: msa
- prompt: عندي أشياء كثيرة ومتشتت
- response: ابدأ بكل سرور. أخبرني عن يومك أو عن يومك شغل بالك.
- overlap: 0.0
- reason: expected_terms_missing

### planning_light — FAIL

- bucket: planning
- dialect: saudi
- prompt: رتب لي بداية بسيطة بدون تعقيد
- response: ابدأ بعمل واحد مهم، ثم خذ راحة قصيرة، ثم كمل التالي.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_tired — FAIL

- bucket: support
- dialect: saudi
- prompt: تعبان شوي واحتاج كلام يهديني
- response: أنت مو مطالب تحل كل شيء الآن. اهدأ وخذ دقيقة لنفسك.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_anxious — FAIL

- bucket: support
- dialect: msa
- prompt: كيف أهدأ إذا توترت؟
- response: ابدأ ببطء، خفف الحركة، وابدأ بخطوة واحدة فقط.
- overlap: 0.0
- reason: expected_terms_missing

### support_pressure — FAIL

- bucket: support
- dialect: saudi
- prompt: حاس بضغط اليوم
- response: هونها عليك. خذ نفس هادي وخلنا نبدأ بشي واحد.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_short — FAIL

- bucket: support
- dialect: msa
- prompt: طمني بكلام بسيط
- response: ابدأ بكل شيء دفعة واحدة.
- overlap: 0.0
- reason: guard:corpus_artifact

## sf-50m — 4/20

### followup_free_choice — FAIL

- bucket: followup
- dialect: saudi
- prompt: الي تحب
- response: أنت مو مطالب تحل كل شيء الآن. اهدأ وخذ دقيقة لنفسك.
- overlap: 0.0
- reason: expected_terms_missing

### followup_continue — FAIL

- bucket: followup
- dialect: msa
- prompt: كمل كلامك
- response: رتبها حسب الأهمية، ثم اختر أول عمل وتقدّم فيه قليلًا.
- overlap: 0.0
- reason: expected_terms_missing

### followup_why — FAIL

- bucket: followup
- dialect: saudi
- prompt: طيب ليه؟
- response: رتبها حسب الأهمية، ثم اختر أول عمل وتقدّم فيه قليلًا.
- overlap: 0.0
- reason: expected_terms_missing

### followup_meaning — FAIL

- bucket: followup
- dialect: saudi
- prompt: يعني كيف؟
- response: رتبها حسب الأهمية، ثم اختر أول عمل وتقدّم فيه قليلًا.
- overlap: 0.0
- reason: expected_terms_missing

### social_chat — FAIL

- bucket: open_social
- dialect: saudi
- prompt: سولف معي شوي
- response: حياك. نقدر نسولف عن يومك أو عن شيء خفيف تحبه.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### social_topic_choice — FAIL

- bucket: open_social
- dialect: saudi
- prompt: وش ودك نسولف عنه؟
- response: حياك. نقدر نسولتحبه.
- overlap: 0.0
- reason: expected_terms_missing

### social_new_topic — FAIL

- bucket: open_social
- dialect: msa
- prompt: هات موضوع خفيف
- response: أقصد أن تحفظ المعروف ولا تنسى من وقف معك.
- overlap: 0.0
- reason: expected_terms_missing

### social_today — FAIL

- bucket: open_social
- dialect: saudi
- prompt: يومي كان طويل
- response: اكتب أهم شيين عندك اليوم وابدأ بالأقرب والأسهل.
- overlap: 0.0
- reason: expected_terms_missing

### topic_courage_simple — PASS

- bucket: topic
- dialect: msa
- prompt: اخبرني عن الشجاعة بأسلوب بسيط
- response: الشجاعة أن تواجه الموقف الصحيح رغم الخوف.
- overlap: 0.2
- reason: passed

### topic_friendship_talk — FAIL

- bucket: topic
- dialect: saudi
- prompt: وش رأيك نتكلم عن الصداقة
- response: الهدوء يخليك تفكر أوضح وترد بدون استعجال.
- overlap: 0.0
- reason: expected_terms_missing

### topic_honesty_example — FAIL

- bucket: topic
- dialect: msa
- prompt: اعطني مثال بسيط عن الصدق
- response: أنت تستطيع أن تبدأ بهدوء. لا يلزم حل كل شيء دفعة واحدة.
- overlap: 0.0
- reason: guard:corpus_artifact

### topic_calm_life — PASS

- bucket: topic
- dialect: saudi
- prompt: الهدوء في اليوم وش يفيدني؟
- response: الهدوء يخليك تفكر أوضح وترد بدون استعجال.
- overlap: 0.2
- reason: passed

### planning_day_start — PASS

- bucket: planning
- dialect: msa
- prompt: اشرح لي كيف ابدأ يومي
- response: ابدأ بمهمة واحدة واضحة، ولا تفتح كل الأعمال في وقت واحد.
- overlap: 0.2
- reason: passed

### planning_confused — PASS

- bucket: planning
- dialect: saudi
- prompt: أنا محتار من وين أبدأ
- response: ابدأ بأصغر خطوة تفتح لك الطريق، حتى لو كانت خمس دقائق.
- overlap: 0.2
- reason: passed

### planning_many_tasks — FAIL

- bucket: planning
- dialect: msa
- prompt: عندي أشياء كثيرة ومتشتت
- response: رتبها حسب الأهمية، ثم اختر أول عمل وتقدّم فيه قليلًا.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### planning_light — FAIL

- bucket: planning
- dialect: saudi
- prompt: رتب لي بداية بسيطة بدون تعقيد
- response: خذ نفسًا هادئًا، ثم اسأل نفسك: ما الخطوة الصغيرة الممكنة الآن؟
- overlap: 0.0
- reason: expected_terms_missing

### support_tired — FAIL

- bucket: support
- dialect: saudi
- prompt: تعبان شوي واحتاج كلام يهديني
- response: أنت مو مطالب تحل كل شيء الآن. اهدأ وخذ دقيقة لنفسك.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_anxious — FAIL

- bucket: support
- dialect: msa
- prompt: كيف أهدأ إذا توترت؟
- response: تنفس ببطء، خفف الحركة، وابدأ بخطوة واحدة فقط.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_pressure — FAIL

- bucket: support
- dialect: saudi
- prompt: حاس بضغط اليوم
- response: هونها عليك. خذ نفس هادي وخلنا نبدأ بشي واحد.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

### support_short — FAIL

- bucket: support
- dialect: msa
- prompt: طمني بكلام بسيط
- response: أنت تستطيع أن تبدأ بهدوء. لا يلزم حل كل شيء دفعة واحدة.
- overlap: 0.0
- reason: guard:corpus_artifact
