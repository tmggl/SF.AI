# Phase 27.34 Guarded Runtime Trial Samples

## trial_001 — PASS

- message: كيفك اليوم
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: بخير ولله الحمد، أنت كيفك؟
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.smalltalk

## trial_002 — PASS

- message: شكرًا لمساعدتك
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: العفو، يسعدني أن أساعدك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.thanks

## trial_003 — PASS

- message: وجهني بخطوة بسيطة
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: ابدأ بخطوة صغيرة وواضحة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:advice

## trial_004 — PASS

- message: رتب لي يومي بسرعة
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: اكتب ثلاث مهام وابدأ بالأهم.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:planning

## trial_005 — PASS

- message: توترت شوي وش اسوي
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: الله يهونها، خذ نفس واهدأ شوي.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:support

## trial_006 — PASS

- message: وش المقصود بالاحترام
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: يعني تقدّر الناس بكلامك وتصرفك.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## trial_007 — PASS

- message: القراية تفيدني بشي
- generator: sf_10m_phase27_33
- dispatch: module:chat
- response: توسع فهمك وتزيد كلماتك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## control_001 — PASS

- message: من أنت
- generator: template
- dispatch: module:chat
- response: أنا SF.AI — مساعد ذكاء اصطناعي يُبنى من الصفر بسيادة معرفية. ما أعتمد على نماذج خارجية، وأتعلّم من بيانات أنت تختارها.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:template_first_social_intent

## control_002 — PASS

- message: عندي ألم في الراس
- generator: template
- dispatch: composer
- response: أرى أن سؤالك صحي/طبي. لن أعطي تشخيصًا أو وصفة. أنصحك تتواصل مع طبيب مختص. أقدر أكون معك لو حبيت تكتب وتفضفض.
- notes: -
