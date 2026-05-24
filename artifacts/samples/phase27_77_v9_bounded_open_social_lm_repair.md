# Phase 27.77 V9 Bounded Open-Social LM Repair

## Phase 27.69 new fresh shadow

### open_social_10 — FAIL

- family: open_social
- prompt: ابدأ محادثة سهلة
- response: نبدأ محام: لحظة راحة قصيرة.
- guard_reason: passed
- reason: response_family_mismatch

### followup_02 — FAIL

- family: followup
- prompt: أعد شرح النقطة ببساطة
- response: نعم، نتحدث قليلًا في موضوع بسيط.
- guard_reason: passed
- reason: expected_terms_missing

### followup_03 — FAIL

- family: followup
- prompt: ما فهمت وش تبي تقول
- response: بعدها خذ خطوة صغيرة وكمل عليها.
- guard_reason: passed
- reason: expected_terms_missing

### support_02 — FAIL

- family: support
- prompt: أشعر بتوتر وأريد طمأنينة
- response: خذ نفس وخفف الضغط خطوة خطوة.
- guard_reason: passed
- reason: expected_terms_missing

### topic_08 — FAIL

- family: topic
- prompt: الشجاعة كيف تكون
- response: الصدق يعني تقول الحقيقة وتلتزم بها.
- guard_reason: passed
- reason: expected_terms_missing

### topic_10 — FAIL

- family: topic
- prompt: وش يعني الوفاء مع الاصحاب
- response: الهدوء يعني تخفف توترك وتفكر بروية.
- guard_reason: passed
- reason: expected_terms_missing

## Phase 27.67 known shadow

### followup_06 — FAIL

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تبدأ بالسهل ثم تنتقل بعده.
- guard_reason: passed
- reason: expected_terms_missing

### support_02 — FAIL

- family: support
- prompt: أحتاج جملة تهدئني
- response: خذ نفسًا هادئًا، وستستعيد راحتك خطوة خطوة.
- guard_reason: malformed_token
- reason: guard:malformed_token

### support_08 — FAIL

- family: support
- prompt: طمئني بكلام قصير
- response: خذ نفسًا هادئًا، وستستعيد راحتك خطوة خطوة.
- guard_reason: malformed_token
- reason: guard:malformed_token

### topic_07 — FAIL

- family: topic
- prompt: اشرح الصداقة دون إطالة
- response: الصدق أن يعمل الناس معًا عن شيء لطيف من يومك.
- guard_reason: passed
- reason: expected_terms_missing

### topic_08 — FAIL

- family: topic
- prompt: الشجاعة متى تظهر
- response: الصدق يعني تقول الحقيقة بوضوح.
- guard_reason: passed
- reason: expected_terms_missing

## Phase 27.60 regression
