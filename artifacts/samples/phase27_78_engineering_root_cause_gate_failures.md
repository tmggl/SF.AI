# Phase 27.78 Engineering Root Cause Gate — Failure Samples

## phase27_69 / open_social_10 — residual_artifact_fragment

- family: `open_social`
- dialect: `msa`
- reason: `response_family_mismatch`
- guard_reason: `passed`
- prompt: ابدأ محادثة سهلة
- response: نبدأ محام: لحظة راحة قصيرة.

## phase27_69 / followup_02 — followup_flow_instability

- family: `followup`
- dialect: `msa`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: أعد شرح النقطة ببساطة
- response: نعم، نتحدث قليلًا في موضوع بسيط.

## phase27_69 / followup_03 — followup_flow_instability

- family: `followup`
- dialect: `saudi`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: ما فهمت وش تبي تقول
- response: بعدها خذ خطوة صغيرة وكمل عليها.

## phase27_69 / support_02 — support_semantic_weakness

- family: `support`
- dialect: `msa`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: أشعر بتوتر وأريد طمأنينة
- response: خذ نفس وخفف الضغط خطوة خطوة.

## phase27_69 / topic_08 — topic_semantic_substitution

- family: `topic`
- dialect: `saudi`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: الشجاعة كيف تكون
- response: الصدق يعني تقول الحقيقة وتلتزم بها.

## phase27_69 / topic_10 — topic_semantic_substitution

- family: `topic`
- dialect: `saudi`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: وش يعني الوفاء مع الاصحاب
- response: الهدوء يعني تخفف توترك وتفكر بروية.

## phase27_67 / followup_06 — followup_flow_instability

- family: `followup`
- dialect: `msa`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: بسّطها لي أكثر
- response: أقصد أن تبدأ بالسهل ثم تنتقل بعده.

## phase27_67 / support_02 — guard_false_positive_tanween

- family: `support`
- dialect: `msa`
- reason: `guard:malformed_token`
- guard_reason: `malformed_token`
- prompt: أحتاج جملة تهدئني
- response: خذ نفسًا هادئًا، وستستعيد راحتك خطوة خطوة.

## phase27_67 / support_08 — guard_false_positive_tanween

- family: `support`
- dialect: `msa`
- reason: `guard:malformed_token`
- guard_reason: `malformed_token`
- prompt: طمئني بكلام قصير
- response: خذ نفسًا هادئًا، وستستعيد راحتك خطوة خطوة.

## phase27_67 / topic_07 — topic_semantic_substitution

- family: `topic`
- dialect: `msa`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: اشرح الصداقة دون إطالة
- response: الصدق أن يعمل الناس معًا عن شيء لطيف من يومك.

## phase27_67 / topic_08 — topic_semantic_substitution

- family: `topic`
- dialect: `saudi`
- reason: `expected_terms_missing`
- guard_reason: `passed`
- prompt: الشجاعة متى تظهر
- response: الصدق يعني تقول الحقيقة بوضوح.
