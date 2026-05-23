# Phase 27.52 Natural Dialogue Objective Repair

## followup_free_choice — FAIL

- bucket: followup
- dialect: saudi
- prompt: الي تحب
- response: ما تفكر في كل شيء مرة وحدة.
- overlap: 0.0
- reason: expected_terms_missing

## followup_continue — FAIL

- bucket: followup
- dialect: msa
- prompt: كمل كلامك
- response: اكتب ثلاث أولويات، ثم ابدأ بما لا يحتمل التأجيل.
- overlap: 0.0
- reason: expected_terms_missing

## followup_why — FAIL

- bucket: followup
- dialect: saudi
- prompt: طيب ليه؟
- response: بعدها خذ خطوة ثانية صغيرة ولا تستعجل النتيجة.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## followup_meaning — FAIL

- bucket: followup
- dialect: saudi
- prompt: يعني كيف؟
- response: ابدأ بما لا يحتمل التففها عليك: اختر أمرًا واحدًا الآن واترك الباقي لاحقًا.
- overlap: 0.0
- reason: expected_terms_missing

## social_chat — FAIL

- bucket: open_social
- dialect: saudi
- prompt: سولف معي شوي
- response: حياك. نقدر نسولف عن يومك أو عن شيء خفيف تحبه.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## social_topic_choice — FAIL

- bucket: open_social
- dialect: saudi
- prompt: وش ودك نسولف عنه؟
- response: حياك. نقدر نسولامنح نفسك راحة قصيرة، ثم عد لما تستطيع فعله.
- overlap: 0.0
- reason: expected_terms_missing

## social_new_topic — FAIL

- bucket: open_social
- dialect: msa
- prompt: هات موضوع خفيف
- response: الفكرة بسيطة: حدد خطوة واحدة، نفذها، ثم انتقل لما بعدها.
- overlap: 0.0
- reason: expected_terms_missing

## social_today — FAIL

- bucket: open_social
- dialect: saudi
- prompt: يومي كان طويل
- response: اكتب أهم شيين عندك اليوم وابدأ بالأقرب والأسهل.
- overlap: 0.0
- reason: expected_terms_missing

## topic_courage_simple — PASS

- bucket: topic
- dialect: msa
- prompt: اخبرني عن الشجاعة بأسلوب بسيط
- response: أنت مو عدم خوف؛ الشجاعة إنك تسوي الصح رغم الخوف.
- overlap: 0.2
- reason: passed

## topic_friendship_talk — FAIL

- bucket: topic
- dialect: saudi
- prompt: وش رأيك نتكلم عن الصداقة
- response: الفكرة بسيطة: حدد خطوة واحدة، نفذها، ثم انتقل لما بعدها.
- overlap: 0.0
- reason: expected_terms_missing

## topic_honesty_example — PASS

- bucket: topic
- dialect: msa
- prompt: اعطني مثال بسيط عن الصدق
- response: الصدق مثل إنك تقول الحقيقة حتى لو كان الكلام صعب.
- overlap: 0.2
- reason: passed

## topic_calm_life — PASS

- bucket: topic
- dialect: saudi
- prompt: الهدوء في اليوم وش يفيدني؟
- response: الهدوء يخليك تفكر أوضح وترد بدون استعجال.
- overlap: 0.2
- reason: passed

## planning_day_start — PASS

- bucket: planning
- dialect: msa
- prompt: اشرح لي كيف ابدأ يومي
- response: ابدأ بعمل واحد مهم، ثم خذ راحة قصيرة، ثم كمل التالي.
- overlap: 0.2
- reason: passed

## planning_confused — PASS

- bucket: planning
- dialect: saudi
- prompt: أنا محتار من وين أبدأ
- response: ب: ابدأ بأصغر خطوة تفتح لك مس دقائق.
- overlap: 0.2
- reason: passed

## planning_many_tasks — FAIL

- bucket: planning
- dialect: msa
- prompt: عندي أشياء كثيرة ومتشتت
- response: الفكرة بسيطة: حدد خطوة واحدة، نفذها، ثم انتقل لما بعدها.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## planning_light — FAIL

- bucket: planning
- dialect: saudi
- prompt: رتب لي بداية بسيطة بدون تعقيد
- response: الفكرة بسيطة: حدد خطوة واحدة، نفذها، ثم انتقل لما بعدها.
- overlap: 0.1667
- reason: expected_terms_missing

## support_tired — FAIL

- bucket: support
- dialect: saudi
- prompt: تعبان شوي واحتاج كلام يهديني
- response: أنت مو مطالب تحل كل شيء الآن. اهدأ وخذ دقيقة لنفسك.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## support_anxious — FAIL

- bucket: support
- dialect: msa
- prompt: كيف أهدأ إذا توترت؟
- response: المقصود إنك تختار خطوة بسيطة وتنفذها بدل ما تفكر في كل شيء مرة وحدة.
- overlap: 0.0
- reason: expected_terms_missing

## support_pressure — FAIL

- bucket: support
- dialect: saudi
- prompt: حاس بضغط اليوم
- response: هونها عليك. خذ نفس هادي وخلنا نبدأ بشي واحد.
- overlap: 0.0
- reason: low_prompt_overlap:0.00

## support_short — FAIL

- bucket: support
- dialect: msa
- prompt: طمني بكلام بسيط
- response: أنت تستطيع أن تبدأ بهدوء. لا يلزم حل كل شيء دفعة واحدة.
- overlap: 0.0
- reason: guard:corpus_artifact
