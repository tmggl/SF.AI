# Phase 27.61 Broader Generalization Repair

## open_social_01 — PASS

- family: open_social
- prompt: ابي اسولف شوي
- response: أكيد، نقدر نسولف عن موضوع خفيف من يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_02 — FAIL

- family: open_social
- prompt: خلنا نفتح موضوع بسيط
- response: تقدر تهدأ خطوة صغيرة وكمل عليها.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_03 — PASS

- family: open_social
- prompt: حدثني حديثًا لطيفًا
- response: نبدأ بحديث قصير عن موضوع لطيف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_04 — FAIL

- family: open_social
- prompt: وش عندك كلام خفيف
- response: الوفاء حفظ للعهد وثبات في الود.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_05 — FAIL

- family: open_social
- prompt: افتح معي حوارًا قصيرًا
- response: تهدأ، خذ نفس وذكّر نفسك أنها خطوة وتعدي.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_06 — FAIL

- family: open_social
- prompt: ما عندي موضوع سولف انت
- response: تقدر تهدأ خطوة صغيرة وكمل عليها.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — FAIL

- family: followup
- prompt: ما فهمت قصدك
- response: الوفاء حفظ للعهد وثبات ود.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_02 — FAIL

- family: followup
- prompt: هل توضح لي الفكرة
- response: الوفاء أن تحفظ العهد وتثبت مع من تثق به.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — PASS

- family: followup
- prompt: وبعدين وش اسوي
- response: بعدها اختر خطوة صغيرة وكمل عليها.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_04 — FAIL

- family: followup
- prompt: أكمل شرحك
- response: الوفاء حفظ للعهد وثبات في الود.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_05 — PASS

- family: followup
- prompt: طيب وش تقصد بالضبط
- response: أقصد الفكرة ببساطة: ابدأ بالواضح ثم كمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_06 — PASS

- family: followup
- prompt: فسرها بطريقة أبسط
- response: أقصد أن تبدأ بالجزء السهل ثم تنتقل لما بعده.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_01 — PASS

- family: planning
- prompt: ابي اخلي يومي مرتب
- response: اكتب أهم ثلاث مهام وابدأ بالأهم.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — PASS

- family: planning
- prompt: ساعدني أبدأ عملي اليوم
- response: اختر مهمة واحدة واضحة وابدأ بها الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_03 — PASS

- family: planning
- prompt: عندي اشياء كثيره وش ابدا فيه
- response: ابدأ بالأهم، وخله خطوة صغيرة وواضحة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_04 — PASS

- family: planning
- prompt: أريد خطة صغيرة لبداية اليوم
- response: اكتب خطة قصيرة: مهمة أولى ثم خطوة بعدها.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_05 — PASS

- family: planning
- prompt: رتب لي اول خطوه
- response: أول خطوة: اختر شي واحد واضح وابدأ فيه.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_06 — PASS

- family: planning
- prompt: كيف أختار أول مهمة
- response: اختر المهمة الأهم والأقرب للتنفيذ.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_01 — PASS

- family: support
- prompt: ضايق صدري شوي
- response: خذ نفسًا هادئًا، وخففها عليك خطوة خطوة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_02 — PASS

- family: support
- prompt: أشعر بضغط وأحتاج هدوءًا
- response: تنفس بهدوء، وابدأ بخطوة صغيرة حتى يقل القلق.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_03 — PASS

- family: support
- prompt: ابي كلام يطمني
- response: تقدر تهدأ، خذ نفس وذكّر نفسك أنها خطوة وتعدي.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_04 — PASS

- family: support
- prompt: أنا قلق من البداية
- response: تنفس بهدوء، وابدأ بخطوة صغيرة حتى يقل القلق.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_05 — PASS

- family: support
- prompt: حاس اني مشتت
- response: خذ نفسًا وركز على خطوة واحدة الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_06 — PASS

- family: support
- prompt: كيف أهدأ دون تعقيد
- response: تنفس بهدوء وخذ لحظة قصيرة قبل أي قرار.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_01 — PASS

- family: topic
- prompt: عرّف لي الوفاء
- response: الوفاء أن تحفظ العهد وتثبت مع من تثق به.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_02 — FAIL

- family: topic
- prompt: وش معنى التعاون
- response: التعاونخفف الحمل.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## topic_03 — FAIL

- family: topic
- prompt: ما المقصود بالصبر
- response: الصبر ثبات وهدوء وقت الصعوبة.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## topic_04 — FAIL

- family: topic
- prompt: الاحترام وش هو
- response: الاحتحياك، نفتح نفسك لحظة راحة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_05 — FAIL

- family: topic
- prompt: اشرح الهدوء بجملة
- response: الصبر قوة تساعدك على الثبات وقت الضيق.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## topic_06 — FAIL

- family: topic
- prompt: وش يعني الصدق ببساطه
- response: تقدر تهدأ خطوة خطوة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing
