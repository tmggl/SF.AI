# Phase 27.87 Samples

## sf-10m-step600

### open_social_01 — PASS

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

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

### open_social_05 — PASS

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: نبدأ بحديث خفيف عن يومك، ما الشيء الهدوء؟
- reason: passed

### open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: موضوع لطيف: ما المكان الذي تحب أن تجلس فيه عندما تريد الهدوء؟
- reason: passed

### open_social_07 — PASS

- family: open_social
- prompt: وش سالفتك اليوم
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_08 — PASS

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### open_social_09 — FAIL

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: نستطيع أن نتحدث عن شيء أراحك اليوم؟
- reason: expected_terms_missing

### open_social_10 — PASS

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: passed

### followup_01 — PASS

- family: followup
- prompt: ما وضحت لي زين
- response: أقصد خل أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: passed

### followup_02 — FAIL

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: expected_terms_missing

### followup_03 — FAIL

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: مثال: أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: expected_terms_missing

### followup_04 — FAIL

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: expected_terms_missing

### followup_05 — FAIL

- family: followup
- prompt: يعني وش المطلوب مني
- response: أقصد خل الموضوع أراحك اليوم؟ الهدوء؟
- reason: expected_terms_missing

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: مثال: أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: expected_terms_missing

### followup_07 — FAIL

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: مثال: أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: expected_terms_missing

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: موضوع لطيف: ما المكان الذي تحب أن تجلس فيه عندما تريد الهدوء؟
- reason: expected_terms_missing

### followup_09 — FAIL

- family: followup
- prompt: وش تقصد بهالكلام
- response: مثال: أن نتكلم عن عادة بسيطة تحبها في يومك.
- reason: expected_terms_missing

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: نبدأ بحديث خفيف عن يومك، ما الشيء اللطيف الذي حدث لك؟
- reason: expected_terms_missing

## sf-10m-step1200

### open_social_01 — FAIL

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: ابدأ بالأهم، وبعد ما تح سالفة خفيفة أول جزء راجع باقي المهام.
- reason: response_family_mismatch

### open_social_02 — FAIL

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم راجع اللي بعده.
- reason: expected_terms_missing

### open_social_03 — FAIL

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: ابدأ بالأهم، وبعد ما تح سالفة خفيفة أول جزء راجع دة المهام.
- reason: expected_terms_missing

### open_social_04 — FAIL

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: ابدأ بالأهم، وبعد ما تح سالفة خفيفة أول جزء راجع الأشياء المهام.
- reason: expected_terms_missing

### open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: ابدأ بالأهم، وبعد ما تهدأ؟
- reason: expected_terms_missing

### open_social_06 — FAIL

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: اختر ثلاث مهام بس ، وابدأ بها.
- reason: expected_terms_missing

### open_social_07 — FAIL

- family: open_social
- prompt: وش سالفتك اليوم
- response: ابدأ بالأهم، وبعد ما تح سالفة خفيفة أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### open_social_08 — FAIL

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم راجع اللي بعده.
- reason: expected_terms_missing

### open_social_09 — FAIL

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### open_social_10 — FAIL

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم راجع اللي بعده.
- reason: expected_terms_missing

### followup_01 — FAIL

- family: followup
- prompt: ما وضحت لي زين
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### followup_02 — FAIL

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع الأشياء المهام.
- reason: expected_terms_missing

### followup_03 — FAIL

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: response_family_mismatch

### followup_04 — FAIL

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: حدد الهدف، وب، اكتب المهام، وابدأ بالأهم عشرين دقيقة.
- reason: expected_terms_missing

### followup_05 — FAIL

- family: followup
- prompt: يعني وش المطلوب مني
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع سالفة خفيفة المهام.
- reason: response_family_mismatch

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: ابدأ بالأهم، وبعد ما تخللمأول جزء راجع الأشياء المهام.
- reason: response_family_mismatch

### followup_07 — FAIL

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: اختر ثلاث مهام بس ، وابدأ بالأهم ثم راجع اللي بعده.
- reason: expected_terms_missing

### followup_09 — FAIL

- family: followup
- prompt: وش تقصد بهالكلام
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع سالفة خفيفة المهام.
- reason: expected_terms_missing

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: ابدأ بالأهم، وبعد ما تخللمأول جزء راجع الأشياء المهام.
- reason: expected_terms_missing

## sf-10m-step1800

### open_social_01 — FAIL

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_02 — FAIL

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: خذ نفس شوي واهدأ، بعدها ابدأ بالجزء راجع لوقت
- reason: expected_terms_missing

### open_social_03 — FAIL

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_04 — FAIL

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: خذ نفس شوي واهدأ، بعدها ابدأ بالجزء راجع المهاتحمل نفسك كل
- reason: expected_terms_missing

### open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_06 — FAIL

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_07 — FAIL

- family: open_social
- prompt: وش سالفتك اليوم
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_08 — FAIL

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### open_social_09 — FAIL

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: خفها على نفسك، خذ نفس وابدأ بالأهم عشالجانبية.
- reason: expected_terms_missing

### open_social_10 — FAIL

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: خفها على نفسك، خذ نفس وابدأ بالأهم واترك الباقي لوقت م، م، م،
- reason: expected_terms_missing

### followup_01 — FAIL

- family: followup
- prompt: ما وضحت لي زين
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### followup_02 — FAIL

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: ابدأ ببطيقًا، ما تخلتحمل نفسك كل شيء مرة الأقرب لك،
- reason: expected_terms_missing

### followup_03 — FAIL

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: ابدأ بالأهم، وذكّر نفسك نفس وابدأ بالأهم ابدأ بشي صغير م. أقولبالكلام قصيرة.
- reason: response_family_mismatch

### followup_04 — FAIL

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing

### followup_05 — FAIL

- family: followup
- prompt: يعني وش المطلوب مني
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: response_family_mismatch

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: ابدأ ببطيقًا، ما يرة، واص ك.
- reason: response_family_mismatch

### followup_07 — FAIL

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: القصتح سالفة خفيفة عن عادة تحمل نفسك كل شيء مرة الأقرب لك،
- reason: expected_terms_missing

### followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: لا
- reason: guard:too_short

### followup_09 — FAIL

- family: followup
- prompt: وش تقصد بهالكلام
- response: ابدأ بالأهم، وبعد ما تخلص أول جزء راجع باقي المهام.
- reason: expected_terms_missing

### followup_10 — FAIL

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- reason: expected_terms_missing
