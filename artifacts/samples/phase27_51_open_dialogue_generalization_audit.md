# Phase 27.51 Open-Dialogue Generalization Audit

## live_api / followup_free_choice — FAIL

- bucket: followup
- prompt: الي تحب
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / followup_free_choice — FAIL

- bucket: followup
- prompt: الي تحب
- generator: sf_10m_phase27_47
- response: ابدأ بالأهم ثم انتقل للي بعده.
- reason: forbidden_terms_present

## live_api / followup_continue — FAIL

- bucket: followup
- prompt: كمل كلامك
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / followup_continue — FAIL

- bucket: followup
- prompt: كمل كلامك
- generator: sf_10m_phase27_47
- response: ابدأ بشي بسيط وواضح.
- reason: low_prompt_overlap:0.00

## live_api / followup_why — FAIL

- bucket: followup
- prompt: طيب ليه؟
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / followup_why — FAIL

- bucket: followup
- prompt: طيب ليه؟
- generator: sf_10m_phase27_47
- response: ابدأ بشي بسيط وواضح.
- reason: low_prompt_overlap:0.00

## live_api / followup_meaning — FAIL

- bucket: followup
- prompt: يعني كيف؟
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / followup_meaning — FAIL

- bucket: followup
- prompt: يعني كيف؟
- generator: sf_10m_phase27_47
- response: الهدوء سكيالصداقة رفقة طيبة تقوم على الوفاء.
- reason: canned_phrase

## live_api / social_chat — FAIL

- bucket: open_social
- prompt: سولف معي شوي
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / social_chat — FAIL

- bucket: open_social
- prompt: سولف معي شوي
- generator: sf_10m_phase27_47
- response: ابدأ بالأهم ثم انتقل للي بعده.
- reason: canned_phrase

## live_api / social_topic_choice — FAIL

- bucket: open_social
- prompt: وش ودك نسولف عنه؟
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / social_topic_choice — FAIL

- bucket: open_social
- prompt: وش ودك نسولف عنه؟
- generator: sf_10m_phase27_47
- response: الهدوء يعني تخفف توترك وتتكلم بروية.
- reason: low_prompt_overlap:0.00

## live_api / social_new_topic — FAIL

- bucket: open_social
- prompt: هات موضوع خفيف
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / social_new_topic — FAIL

- bucket: open_social
- prompt: هات موضوع خفيف
- generator: sf_10m_phase27_47
- response: ابدأ الله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / social_today — FAIL

- bucket: open_social
- prompt: يومي كان طويل
- generator: sf_10m_phase27_47
- response: اكتب أولوياتك ثم ابدأ بالأهم.
- reason: canned_phrase

## raw_unconditioned / social_today — FAIL

- bucket: open_social
- prompt: يومي كان طويل
- generator: sf_10m_phase27_47
- response: ابدأ بشي بسيط وواضح.
- reason: low_prompt_overlap:0.00

## live_api / topic_courage_simple — FAIL

- bucket: topic
- prompt: اخبرني عن الشجاعة بأسلوب بسيط
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / topic_courage_simple — FAIL

- bucket: topic
- prompt: اخبرني عن الشجاعة بأسلوب بسيط
- generator: sf_10m_phase27_47
- response: الشجاعة إنك الصداقة رفقة طيبة تقوم على الوفاء. على الالله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / topic_friendship_talk — FAIL

- bucket: topic
- prompt: وش رأيك نتكلم عن الصداقة
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / topic_friendship_talk — FAIL

- bucket: topic
- prompt: وش رأيك نتكلم عن الصداقة
- generator: sf_10m_phase27_47
- response: الصداقة رفقة طيبة ووقفة وقت الحاجة.
- reason: canned_phrase

## live_api / topic_honesty_example — FAIL

- bucket: topic
- prompt: اعطني مثال بسيط عن الصدق
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / topic_honesty_example — FAIL

- bucket: topic
- prompt: اعطني مثال بسيط عن الصدق
- generator: sf_10m_phase27_47
- response: الصدق أن تقول الحقيقة بوضوح.
- reason: canned_phrase

## live_api / topic_calm_life — FAIL

- bucket: topic
- prompt: الهدوء في اليوم وش يفيدني؟
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / topic_calm_life — PASS

- bucket: topic
- prompt: الهدوء في اليوم وش يفيدني؟
- generator: sf_10m_phase27_47
- response: الهدوء يعني تخفف توترك وتتكلم بروية.
- reason: passed

## live_api / planning_day_start — FAIL

- bucket: planning
- prompt: اشرح لي كيف ابدأ يومي
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / planning_day_start — FAIL

- bucket: planning
- prompt: اشرح لي كيف ابدأ يومي
- generator: sf_10m_phase27_47
- response: ابدأ الله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / planning_confused — FAIL

- bucket: planning
- prompt: أنا محتار من وين أبدأ
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / planning_confused — FAIL

- bucket: planning
- prompt: أنا محتار من وين أبدأ
- generator: sf_10m_phase27_47
- response: ابدأ الله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / planning_many_tasks — FAIL

- bucket: planning
- prompt: عندي أشياء كثيرة ومتشتت
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / planning_many_tasks — FAIL

- bucket: planning
- prompt: عندي أشياء كثيرة ومتشتت
- generator: sf_10m_phase27_47
- response: ابدأ الله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / planning_light — PASS

- bucket: planning
- prompt: رتب لي بداية بسيطة بدون تعقيد
- generator: sf_10m_phase27_47
- response: ابدأ
- reason: passed

## raw_unconditioned / planning_light — FAIL

- bucket: planning
- prompt: رتب لي بداية بسيطة بدون تعقيد
- generator: sf_10m_phase27_47
- response: الهدوء سكيالصداقة علاقة طيبة تقوم على الوفاء.
- reason: low_prompt_overlap:0.00

## live_api / support_tired — FAIL

- bucket: support
- prompt: تعبان شوي واحتاج كلام يهديني
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / support_tired — FAIL

- bucket: support
- prompt: تعبان شوي واحتاج كلام يهديني
- generator: sf_10m_phase27_47
- response: ابدأ بالأهم ثم انتقل للي بعده. الشجاعة إنك مد، أنت كيفك؟
- reason: canned_phrase

## live_api / support_anxious — FAIL

- bucket: support
- prompt: كيف أهدأ إذا توترت؟
- generator: sf_10m_phase27_47
- response: خذ نفسًا هادئًا واهدأ خطوة خطوة.
- reason: expected_terms_missing

## raw_unconditioned / support_anxious — FAIL

- bucket: support
- prompt: كيف أهدأ إذا توترت؟
- generator: sf_10m_phase27_47
- response: ابدأ بالأهم ثم انتقل للي بعده. على الوفاء. على الف.
- reason: expected_terms_missing

## live_api / support_pressure — FAIL

- bucket: support
- prompt: حاس بضغط اليوم
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / support_pressure — FAIL

- bucket: support
- prompt: حاس بضغط اليوم
- generator: sf_10m_phase27_47
- response: ابدأ الله يعافيك، حاضر بأي وقت.
- reason: canned_phrase

## live_api / support_short — FAIL

- bucket: support
- prompt: طمني بكلام بسيط
- generator: generator_blocked
- response: (empty)
- reason: generator:generator_blocked

## raw_unconditioned / support_short — FAIL

- bucket: support
- prompt: طمني بكلام بسيط
- generator: sf_10m_phase27_47
- response: ابدأ الصداقة علاقة طيبة تقوم على الوفاء. خذ نفسًا هادئًا واهدأ خطوة خطوة.
- reason: low_prompt_overlap:0.00

## live_api / identity_general — PASS

- bucket: control_blocked
- prompt: من أنت؟
- generator: generator_blocked
- response: (empty)
- reason: passed

## raw_unconditioned / identity_general — PASS

- bucket: control_blocked
- prompt: من أنت؟
- generator: not_scored_control
- response: (empty)
- reason: control_not_raw_scored

## live_api / capability_general — PASS

- bucket: control_blocked
- prompt: وش تقدر تسوي؟
- generator: generator_blocked
- response: (empty)
- reason: passed

## raw_unconditioned / capability_general — PASS

- bucket: control_blocked
- prompt: وش تقدر تسوي؟
- generator: not_scored_control
- response: (empty)
- reason: control_not_raw_scored
