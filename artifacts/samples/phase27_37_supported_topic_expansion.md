# Phase 27.37 Supported Topic Expansion

## gen_001 — PASS

- bucket: generated
- message: كيفك اليوم
- generator: sf_10m_phase27_33
- response: بخير ولله الحمد، أنت كيفك؟
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.smalltalk

## gen_002 — PASS

- bucket: generated
- message: وش أخبارك
- generator: sf_10m_phase27_33
- response: بخير ولله الحمد، أنت كيفك؟
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.smalltalk

## gen_003 — PASS

- bucket: generated
- message: شكرًا لمساعدتك
- generator: sf_10m_phase27_33
- response: العفو، يسعدني أن أساعدك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:chat.thanks

## gen_004 — PASS

- bucket: generated
- message: يعطيك العافية
- generator: sf_10m_phase27_33
- response: العفو، حاضر بأي وقت.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:thanks

## gen_005 — PASS

- bucket: generated
- message: وجهني بخطوة بسيطة
- generator: sf_10m_phase27_33
- response: ابدأ بخطوة صغيرة وواضحة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:advice

## gen_006 — PASS

- bucket: generated
- message: رتب لي يومي بسرعة
- generator: sf_10m_phase27_33
- response: اكتب ثلاث مهام وابدأ بالأهم.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:planning

## gen_007 — PASS

- bucket: generated
- message: توترت شوي وش اسوي
- generator: sf_10m_phase27_33
- response: الله يهونها، خذ نفس واهدأ شوي.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:support

## gen_008 — PASS

- bucket: generated
- message: وش المقصود بالاحترام
- generator: sf_10m_phase27_33
- response: يعني تقدّر الناس بكلامك وتصرفك.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## gen_009 — PASS

- bucket: generated
- message: ما معنى التعاون
- generator: sf_10m_phase27_33
- response: التعاون يعني أن ننجز معًا بدل الانفراد.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## gen_010 — PASS

- bucket: generated
- message: القراية تفيدني بشي
- generator: sf_10m_phase27_33
- response: توسع فهمك وتزيد كلماتك.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## new_001 — PASS

- bucket: new_topic
- message: ما معنى الصبر
- generator: sf_10m_phase27_33
- response: الصبر هو الثبات عند الصعوبة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## new_002 — PASS

- bucket: new_topic
- message: الصبر وش يعني
- generator: sf_10m_phase27_33
- response: الصبر إنك تثبت وقت بوضوح.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## new_003 — PASS

- bucket: new_topic
- message: وش المقصود بالصبر
- generator: sf_10m_phase27_33
- response: الصبر إنك تثبت وقت الصعوبة.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:sf_10m_phase27_33,native_generator:generated,native_generator:canary_passed,native_generator:intent:definition

## floor_001 — PASS

- bucket: quality_floor
- message: عرف الصبر
- generator: template
- response: فهمت عليك بشكل عام. قدراتي محدودة، فعطِني تفصيل أكثر عشان أرد عليك بدقة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:template,native_generator:canary_blocked,generation_guard:definition_topic_mismatch,native_generator:intent:definition

## floor_002 — PASS

- bucket: quality_floor
- message: اشرح لي الصبر ببساطة
- generator: template
- response: فهمت عليك بشكل عام. قدراتي محدودة، فعطِني تفصيل أكثر عشان أرد عليك بدقة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:template,native_generator:canary_blocked,generation_guard:definition_topic_mismatch,native_generator:intent:definition

## floor_003 — PASS

- bucket: quality_floor
- message: وش معنى الصداقة
- generator: template
- response: فهمت عليك بشكل عام. قدراتي محدودة، فعطِني تفصيل أكثر عشان أرد عليك بدقة.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:trial_unsupported_definition_topic

## floor_004 — PASS

- bucket: quality_floor
- message: اشرح الصدق
- generator: template
- response: فهمت عليك بشكل عام. قدراتي محدودة، فعطِني تفصيل أكثر عشان أرد عليك بدقة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:template,native_generator:trial_unsupported_definition_topic

## floor_005 — PASS

- bucket: quality_floor
- message: موضوع مفتوح
- generator: template
- response: فهمت عليك بشكل عام. قدراتي محدودة، فعطِني تفصيل أكثر عشان أرد عليك بدقة.
- notes: dialect:الفصحى,language:ar,rag:not_configured,generator:template,native_generator:trial_unsupported_general

## control_001 — PASS

- bucket: control
- message: من أنت
- generator: template
- response: أنا SF.AI — مساعد ذكاء اصطناعي يُبنى من الصفر بسيادة معرفية. ما أعتمد على نماذج خارجية، وأتعلّم من بيانات أنت تختارها.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:template_first_social_intent

## control_002 — PASS

- bucket: control
- message: وش تقدر تسوي
- generator: template
- response: حاليًا أقدر: أفهم العربية الفصحى واللهجة السعودية، أصحّح أخطاء إملائية بسيطة، أوجّه السؤال داخل النظام، وأعطيك ردًا موضوعيًا. ما زلت لست نموذج توليد حر؛ أنا الآن نظام قواعد وتوجيه، والتوليد الذكي يحتاج تدريب النموذج السيادي على بياناتك.
- notes: dialect:السعودية,language:ar,rag:not_configured,generator:template,native_generator:template_first_social_intent

## control_003 — PASS

- bucket: control
- message: عندي ألم في الراس
- generator: template
- response: أرى أن سؤالك صحي/طبي. لن أعطي تشخيصًا أو وصفة. أنصحك تتواصل مع طبيب مختص. أقدر أكون معك لو حبيت تكتب وتفضفض.
- notes: -
