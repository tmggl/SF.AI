# Phase 27.35 Live UI Trial Observations

## live_001 — PASS

- message: كيفك اليوم
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: بخير ولله الحمد، أنت كيفك؟
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.smalltalk

## live_002 — PASS

- message: شكرًا لمساعدتك
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: العفو، يسعدني أن أساعدك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.thanks

## live_003 — PASS

- message: وجهني بخطوة بسيطة
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: ابدأ بخطوة صغيرة وواضحة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:advice

## live_004 — PASS

- message: رتب لي يومي بسرعة
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: اكتب ثلاث مهام وابدأ بالأهم.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:planning

## live_005 — PASS

- message: توترت شوي وش اسوي
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: الله يهونها، خذ نفس واهدأ شوي.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:support

## live_006 — PASS

- message: وش المقصود بالاحترام
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: يعني تقدّر الناس بكلامك وتصرفك.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## live_007 — PASS

- message: القراية تفيدني بشي
- generator_trial: true
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: توسع فهمك وتزيد كلماتك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## control_001 — PASS

- message: كيفك اليوم
- generator_trial: false
- generator: template
- dispatch: module:chat
- response: بخير، شكرًا لسؤالك. كيف حالك أنت؟
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:disabled

## control_002 — PASS

- message: من أنت
- generator_trial: true
- generator: template
- dispatch: module:chat
- response: أنا SF.AI — مساعد ذكاء اصطناعي يُبنى من الصفر بسيادة معرفية. ما أعتمد على نماذج خارجية، وأتعلّم من بيانات أنت تختارها.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:template_first_social_intent

## control_003 — PASS

- message: عندي ألم في الراس
- generator_trial: true
- generator: template
- dispatch: composer
- response: أرى أن سؤالك صحي/طبي. لن أعطي تشخيصًا أو وصفة. أنصحك تتواصل مع طبيب مختص. أقدر أكون معك لو حبيت تكتب وتفضفض.
- notes: -
