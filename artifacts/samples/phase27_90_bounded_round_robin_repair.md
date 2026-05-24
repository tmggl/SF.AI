# Phase 27.90 Samples

## sf-10m-step600

### open_social_01 — FAIL

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- reason: expected_terms_missing

### open_social_02 — FAIL

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- reason: expected_terms_missing

### open_social_03 — PASS

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_04 — FAIL

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: نستطيع أن نتحدث عن شيء صغير أسعدعدك أو خفف عنك اليوم.
- reason: guard:malformed_token

### open_social_05 — PASS

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: نبدأ بحديث خفيف عن يومك، ما الشيء الذي حدث لك؟
- reason: passed

### open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_07 — FAIL

- family: open_social
- prompt: وش سالفتك اليوم
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- reason: expected_terms_missing

### open_social_08 — FAIL

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: نستطيع أن نتحدث عن شيء صغير أسعدك أو خفف عنك اليوم.
- reason: expected_terms_missing

### open_social_09 — PASS

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_10 — FAIL

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: يمكننا أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: expected_terms_missing

### followup_01 — PASS

- family: followup
- prompt: ما وضحت لي زين
- response: أقصد الفكرة ببساطة: خذ جزءًا من الموضوع وتعامل معه أولًا.
- reason: passed

### followup_02 — PASS

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_03 — FAIL

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: أقصد باختصار: الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

### followup_04 — PASS

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_05 — PASS

- family: followup
- prompt: يعني وش المطلوب مني
- response: يعني المطلوب خطوة صغيرة وواضحة الآن.
- reason: passed

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

### followup_07 — FAIL

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: معنى العمل لا تجمع كل شيء في لحظة واحدالأمر كّ: اختر منه مهمة قصيرة وابدأ بها.
- reason: expected_terms_missing

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

### followup_09 — PASS

- family: followup
- prompt: وش تقصد بهالكلام
- response: أقصد باختصار: الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

## sf-10m-step1200

### open_social_01 — FAIL

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: نقدر نقدر نقدر وش ودعن عادة تحبها في يومك.
- reason: guard:repeated_phrase

### open_social_02 — PASS

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_03 — PASS

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_04 — PASS

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: نستهدأ، شيء صار لك؟
- reason: expected_terms_missing

### open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_07 — PASS

- family: open_social
- prompt: وش سالفتك اليوم
- response: نقدر نسولف عن يومك أو عن عادة تحبها في يومك.
- reason: passed

### open_social_08 — PASS

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_09 — FAIL

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: نقدر نقدر نقدر وش ودحك اليوم؟
- reason: guard:repeated_phrase

### open_social_10 — PASS

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: نبدأ بكلام خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### followup_01 — PASS

- family: followup
- prompt: ما وضحت لي زين
- response: أقصد الفكرة ببساطة: خذ جزءًا واحدًا من الموضوع وتعامل معه أولًا.
- reason: passed

### followup_02 — PASS

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_03 — PASS

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: أقصد المعنى ببساطة، ونوضواضح وابدأ بخطوة أبسط.
- reason: passed

### followup_04 — PASS

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_05 — FAIL

- family: followup
- prompt: يعني وش المطلوب مني
- response: ابدأ بشي صغير وواضح وابدأ فيه.
- reason: response_family_mismatch

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

### followup_07 — PASS

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: أقصد الفكرة ببساطة: خذ جزءًا واحدًا من الموضوع وتعامل معه أولًا.
- reason: passed

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

### followup_09 — PASS

- family: followup
- prompt: وش تقصد بهالكلام
- response: أقصد باختصار: تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: passed

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: أقصد أن تجعل الأمر أصغر وأسهل، ثم تبدأ بالجزء الواضح.
- reason: expected_terms_missing

## sf-10m-step1800

### open_social_01 — PASS

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

### open_social_02 — PASS

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_03 — PASS

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

### open_social_04 — PASS

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: نبدأ حديثًا عادي نفتح مك.
- reason: passed

### open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: وش المكان الذي تحب تجلس فيه إذا تبي تهدأ؟
- reason: expected_terms_missing

### open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: نبدأ حديثًا خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_07 — PASS

- family: open_social
- prompt: وش سالفتك اليوم
- response: نقدر نفتح سالفة خفيفة عن عادة تحبها في يومك.
- reason: passed

### open_social_08 — PASS

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_09 — PASS

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: أبشر، خلنا نسولف عن عادة ك: وش ألطف شي صار لك؟
- reason: passed

### open_social_10 — PASS

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: موضوع خفيف: وش المكان اللي تحب تجلس فيه إذا تريد الهدوء؟
- reason: passed

### followup_01 — PASS

- family: followup
- prompt: ما وضحت لي زين
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

### followup_02 — PASS

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: أقصد خل الموضوع أصغوضح الفكرة بخطوة أبسط.
- reason: passed

### followup_03 — PASS

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: يعني لا تجمع كل شيء مرة وحدة؛ خذ جزء بسيط وابدأ فيه.
- reason: passed

### followup_04 — PASS

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالأهم قبل الأشياء الجانبية.
- reason: passed

### followup_05 — PASS

- family: followup
- prompt: يعني وش المطلوب مني
- response: يعني لا تجمع كل شيء مرة وحدة؛ خذ جزء بسيط وابدأ فيه.
- reason: passed

### followup_06 — PASS

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالجزء الواضح قدل.
- reason: passed

### followup_07 — PASS

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالأهم قبل الأشياء الجانبية.
- reason: expected_terms_missing

### followup_09 — PASS

- family: followup
- prompt: وش تقصد بهالكلام
- response: أقصد خل الموضوع أصغر، وابدأ بالجزء الواضح قدامك.
- reason: passed

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالأهم قبل الأشياء شيء قصيرة.
- reason: expected_terms_missing
