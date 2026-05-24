# Phase 27.104 Samples

## sf-10m-step400

### Prototype Canary Failures

- id: `prototype_guard_msa_الوفاء`
  prompt: عرّف الوفاء بجملة واحدة دون ذكر الصداقة.
  response: معنى الاحترام: أن تراعي حق غيرك الأمر تحب أن يرك العمل إلى مهام صغير
  passed: False
  reason: required_topic_missing

- id: `prototype_guard_saudi_الهدوء`
  prompt: وش يعني الهدوء بجملة وحدة بدون ذكر الصداقة؟
  response: الهدوء هو إنك تتتى ى ى وقت وقت وقت ى
  passed: False
  reason: guard:repeated_phrase

### Known Topic Failures

### Fresh Topic Failures

- id: `fresh_01_msa_الوفاء`
  prompt: عرّف الوفاء بكلام بسيط.
  response: معنى الصداقة: علاقة فيها صدق واهتمام وحفظ المعروف.
  passed: False
  reason: required_topic_missing

- id: `fresh_03_msa_الصبر`
  prompt: اشرح الصبر بجملة قصيرة.
  response: معنى الصبر: اختعلى الشجاعة: عب.
  passed: False
  reason: observed_wrong_topic:الشجاعة

### All Family Failures

- id: `open_social_04`
  prompt: لنبدأ حديثًا عاديًا
  response: نستح سالفة خفيفة أن نتحدث عن عادة تحبها في يومك.
  passed: False
  reason: expected_terms_missing

- id: `open_social_05`
  prompt: ابي كلام عادي بدون موضوع كبير
  response: وش أسهواأن المطلوب الآن تحفظ قصيرة وش
  passed: False
  reason: expected_terms_missing

- id: `open_social_06`
  prompt: اختر لي شيئًا نتحدث عنه
  response: نستح حتى لو
  passed: False
  reason: expected_terms_missing

- id: `open_social_08`
  prompt: أريد حوارًا بسيطًا لا أكثر
  response: نستح حتى لو المهام، وابدأ بالأهم عشرين دقيقة.
  passed: False
  reason: expected_terms_missing

- id: `open_social_09`
  prompt: خل الجو خفيف وسولف
  response: وش وقت الصعوبة.
  passed: False
  reason: expected_terms_missing

- id: `open_social_10`
  prompt: هات فكرة لطيفة للكلام
  response: نستح سالفة خفيفة ة: الإنسان على تجلللقيقة.
  passed: False
  reason: expected_terms_missing

- id: `followup_01`
  prompt: ما وضحت لي زين
  response: يعني لا تجمع كل شيء مرة وحدة؛ خذ جزء بسيط وابدأ فيه.
  passed: False
  reason: expected_terms_missing

- id: `followup_02`
  prompt: أعد المعنى بطريقة أوضح
  response: يعني لا تجمع كل شيء مرة ة؛ خذ جزء بسيط وابدأ فيه.
  passed: False
  reason: expected_terms_missing

- id: `followup_03`
  prompt: طيب بعد كلامك وش الخطوة
  response: يعني إنك إن ودة ه.
  passed: False
  reason: expected_terms_missing

- id: `followup_08`
  prompt: تابع الشرح من النقطة الأخيرة
  response: يعني لا تجمع كل شيء مرة يرك يف.
  passed: False
  reason: expected_terms_missing

- id: `followup_10`
  prompt: أريد صياغة أبسط للفكرة
  response: يعني لا تجمع كل شيء مرة يرك فصل الأمر إلى أجزاء صغيرة.
  passed: False
  reason: expected_terms_missing

- id: `support_01`
  prompt: احس بضيق بسيط
  response: لا إنك تقالآن.
  passed: False
  reason: expected_terms_missing

- id: `support_02`
  prompt: أحتاج جملة تهدئني
  response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
  passed: False
  reason: expected_terms_missing

- id: `support_04`
  prompt: أنا مرتبك وأريد هدوءًا
  response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
  passed: False
  reason: expected_terms_missing

- id: `support_05`
  prompt: ابي اروق بدون كلام كثير
  response: لا إنك شوي واكتب اللي مضايقك بجملة قصيرة.
  passed: False
  reason: expected_terms_missing

## sf-10m-step800

### Prototype Canary Failures

- id: `prototype_guard_saudi_التعاون`
  prompt: وش يعني التعاون بجملة وحدة بدون ذكر الصداقة؟
  response: التعاون هو إنك تساعد غيرك ويتتهونون الموقف فع.
  passed: False
  reason: guard:malformed_token

- id: `prototype_guard_msa_الاحترام`
  prompt: عرّف الاحترام بجملة واحدة دون ذكر الصداقة.
  response: معنى الاحترام: إنك تعطي كل شخص قدره في الحديث اللي هو هو هو يعني على تهور.
  passed: False
  reason: guard:repeated_phrase

### Known Topic Failures

- id: `known_saudi_التعاون`
  prompt: وش يعني التعاون باختصار؟
  response: معنى التعاون: إنك تساعد غيرك ويتتهونون الموقف على الشي ور.
  passed: False
  reason: guard:malformed_token

- id: `known_msa_الصبر`
  prompt: اشرح لي الصبر بجملة قصيرة.
  response: الصبر هو هو إبطالهدوء: الصبر يعني إنك تتحمل رغم التعب بدون ته
  passed: False
  reason: observed_wrong_topic:الهدوء

### Fresh Topic Failures

- id: `fresh_02_saudi_التعاون`
  prompt: وش معنى التعاون في الحياة اليومية؟
  response: التعاون يعني إنك تساعد غيرك ويتتهونون الموقف على الشي ور.
  passed: False
  reason: guard:malformed_token

- id: `fresh_04_saudi_الاحترام`
  prompt: وش يعني الاحترام؟
  response: معنى الوفاء: إنك تقدر الناس بكلامك وتصرفك.
  passed: False
  reason: required_topic_missing

### All Family Failures

- id: `open_social_01`
  prompt: ودي اسمع منك سوالف خفيفة
  response: وش الشي إنك إنك إن ك.
  passed: False
  reason: expected_terms_missing

- id: `open_social_04`
  prompt: لنبدأ حديثًا عاديًا
  response: نستح سالفة خفيفة ة: الإنسان على الصواب مع إدراك الخوف.
  passed: False
  reason: expected_terms_missing

- id: `open_social_05`
  prompt: ابي كلام عادي بدون موضوع كبير
  response: معنى
  passed: False
  reason: expected_terms_missing

- id: `open_social_06`
  prompt: اختر لي شيئًا نتحدث عنه
  response: نسان قليلًا قبل التصرف.
  passed: False
  reason: expected_terms_missing

- id: `open_social_07`
  prompt: وش سالفتك اليوم
  response: وش الشي إنك إن كلامك وتصرفكر أوضح.
  passed: False
  reason: expected_terms_missing

- id: `open_social_08`
  prompt: أريد حوارًا بسيطًا لا أكثر
  response: نستح حتى لو كنت خاوف.
  passed: False
  reason: expected_terms_missing

- id: `open_social_09`
  prompt: خل الجو خفيف وسولف
  response: وش كل اللي غيرك إنك تساعد غيرللواحتى لو كنت خايف.
  passed: False
  reason: expected_terms_missing

- id: `open_social_10`
  prompt: هات فكرة لطيفة للكلام
  response: نستح حتى يوى أن نتكلم عن عادة تحبها في يومك.
  passed: False
  reason: expected_terms_missing

- id: `followup_01`
  prompt: ما وضحت لي زين
  response: يعني الشجاعة: إن البداية تكون طيبة منه.
  passed: False
  reason: expected_terms_missing

- id: `followup_02`
  prompt: أعد المعنى بطريقة أوضح
  response: يعني القصة.
  passed: False
  reason: expected_terms_missing

- id: `followup_03`
  prompt: طيب بعد كلامك وش الخطوة
  response: يعني القصمرة إن البداية تكون إنك تسوي الصح حتى لو كنت خايف.
  passed: False
  reason: expected_terms_missing

- id: `followup_06`
  prompt: بسّطها لي أكثر
  response: يعني لا تجمع كل شيء مرة وأسهل، ثم تبدأ بالجزء الواضح.
  passed: False
  reason: expected_terms_missing

- id: `followup_07`
  prompt: ما دخلت مخي اشرحها
  response: يعني المطلوب إذا عندقدام إن كلامك ك ويتهور.
  passed: False
  reason: expected_terms_missing

- id: `followup_08`
  prompt: تابع الشرح من النقطة الأخيرة
  response: يعني لا تجمع كل شيء مرة قدام الناس.
  passed: False
  reason: expected_terms_missing

- id: `followup_10`
  prompt: أريد صياغة أبسط للفكرة
  response: يعني لا تجمع كل شيء مرة وأسهل، ثم تبدأ معتّر ى
  passed: False
  reason: expected_terms_missing

## sf-10m-step1200

### Prototype Canary Failures

### Known Topic Failures

### Fresh Topic Failures

- id: `fresh_04_saudi_الاحترام`
  prompt: وش يعني الاحترام؟
  response: معنى الوفاء: إنك تقدر الناس بكلامك وتصرفك.
  passed: False
  reason: required_topic_missing

### All Family Failures

- id: `open_social_01`
  prompt: ودي اسمع منك سوالف خفيفة
  response: وش الشي اللي اللي ريحك اليوم؟
  passed: False
  reason: expected_terms_missing

- id: `open_social_05`
  prompt: ابي كلام عادي بدون موضوع كبير
  response: معنى ر.
  passed: False
  reason: expected_terms_missing

- id: `open_social_06`
  prompt: اختر لي شيئًا نتحدث عنه
  response: نسان قليلًا قبل التصرف.
  passed: False
  reason: expected_terms_missing

- id: `open_social_07`
  prompt: وش سالفتك اليوم
  response: وش الشي اللي اللي اللي والموضوع وتإن ونى
  passed: False
  reason: guard:repeated_phrase

- id: `open_social_09`
  prompt: خل الجو خفيف وسولف
  response: وش كل اللي غيرك إنك تساعد على على الشي تهور.
  passed: False
  reason: expected_terms_missing

- id: `open_social_10`
  prompt: هات فكرة لطيفة للكلام
  response: نستح حتى يالمهام، وابدأ بالأهم عشرين دعلى تجلإنالمطلف ف ف ون
  passed: False
  reason: expected_terms_missing

- id: `followup_01`
  prompt: ما وضحت لي زين
  response: يعني الكل شيء مرة لا تجمع من الموضوع ك
  passed: False
  reason: expected_terms_missing

- id: `followup_02`
  prompt: أعد المعنى بطريقة أوضح
  response: يعني الكل قريب: الإقدام على الصواب مع إدراك الخوف.
  passed: False
  reason: expected_terms_missing

- id: `followup_03`
  prompt: طيب بعد كلامك وش الخطوة
  response: يعني الكل واصل الأمر إلى أجء صغيرة.
  passed: False
  reason: expected_terms_missing

- id: `followup_06`
  prompt: بسّطها لي أكثر
  response: يعني لا تجمع كل شيء مرة يرك فصل الأمر إلى أجء صغيرة.
  passed: False
  reason: expected_terms_missing

- id: `followup_07`
  prompt: ما دخلت مخي اشرحها
  response: يعني المطلوب إذا عندقدام إن بياللي
  passed: False
  reason: expected_terms_missing

- id: `followup_08`
  prompt: تابع الشرح من النقطة الأخيرة
  response: يعني لا تجمع كل شيء مرة قدام على الصواب مع إدراك الخوف.
  passed: False
  reason: expected_terms_missing

- id: `followup_10`
  prompt: أريد صياغة أبسط للفكرة
  response: يعني لا تجمع كل شيء مرة يرك فسّم العمل إلى مهام صغيرة، وابدأ بالأهم قبل الأشياء السهل، ثم تبدأ
  passed: False
  reason: expected_terms_missing

- id: `support_01`
  prompt: احس بضيق بسيط
  response: اهدأ شوي واهدأ، بعدها ابدأ بشي واحد بسيط. ر.
  passed: False
  reason: expected_terms_missing

- id: `support_02`
  prompt: أحتاج جملة تهدئني
  response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
  passed: False
  reason: expected_terms_missing
