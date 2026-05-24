# Phase 27.67 Fresh Shadow Canary

## open_social_01 — PASS

- family: open_social
- prompt: ودي اسمع منك سوالف خفيفة
- response: تفضل، نبدأ بكلام خفيف عن يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_02 — PASS

- family: open_social
- prompt: ابدأ معي كلامًا لطيفًا
- response: تفضل، نبدأ بكلام خفيف عن يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_03 — FAIL

- family: open_social
- prompt: افتح لي سالفة بسيطة
- response: خلنا نبدأ بقولك وتصرفك يكون فيه تقدير.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## open_social_04 — FAIL

- family: open_social
- prompt: لنبدأ حديثًا عاديًا
- response: حياك، نسولف عن يومك أو عن شيء خفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## open_social_05 — FAIL

- family: open_social
- prompt: ابي كلام عادي بدون موضوع كبير
- response: ابدأ بالجزء السهل ثم كمل.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_06 — PASS

- family: open_social
- prompt: اختر لي شيئًا نتحدث عنه
- response: نقدر نسولف عن يومك أو عن موضوع تحبه.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_07 — FAIL

- family: open_social
- prompt: وش سالفتك اليوم
- response: خلنا نبدأ بس الفة قصيرة وخفيفة.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## open_social_08 — FAIL

- family: open_social
- prompt: أريد حوارًا بسيطًا لا أكثر
- response: الاحترام تقدير الناس بالكلام والتصرف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## open_social_09 — PASS

- family: open_social
- prompt: خل الجو خفيف وسولف
- response: حياك، نسولف عن يومك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## open_social_10 — FAIL

- family: open_social
- prompt: هات فكرة لطيفة للكلام
- response: الاحترام تقدير الناس بالكلام والتصرف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_01 — FAIL

- family: followup
- prompt: ما وضحت لي زين
- response: حياك، نسولف عن يومك أو عن شيء خفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_02 — FAIL

- family: followup
- prompt: أعد المعنى بطريقة أوضح
- response: حياك، نسولف عن يومك أو عن شيء خفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_03 — PASS

- family: followup
- prompt: طيب بعد كلامك وش الخطوة
- response: أقصد باختصار: خذ أول خطوة: اختر شي واحد واضح وابدأ منه.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_04 — FAIL

- family: followup
- prompt: ما الفكرة التي تريدها بالضبط
- response: ابدأ بالقريب ثم خطوة صغيرة وتكمل بدون استعجال.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## followup_05 — FAIL

- family: followup
- prompt: يعني وش المطلوب مني
- response: نقدر نسولف عن يومك أو عن شيء خفيف.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_06 — PASS

- family: followup
- prompt: بسّطها لي أكثر
- response: أقصد أن تبدأ بخطوة واضحة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_07 — FAIL

- family: followup
- prompt: ما دخلت مخي اشرحها
- response: تنفس بهدوء وفعلك.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## followup_08 — FAIL

- family: followup
- prompt: تابع الشرح من النقطة الأخيرة
- response: ابدأ بالقريب ثم خطوة صغيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## followup_09 — PASS

- family: followup
- prompt: وش تقصد بهالكلام
- response: أقصد باختصار: خذ أول جزء واضح وابدأ منه.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## followup_10 — PASS

- family: followup
- prompt: أريد صياغة أبسط للفكرة
- response: أبسطها لك: ابدأ بالجزء السهل ثم أكمل.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_01 — PASS

- family: planning
- prompt: ابي ابدأ يومي صح
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_02 — FAIL

- family: planning
- prompt: رتب لي بداية عملية
- response: الصدق أن تقول الحقيقة وتلتزم بها.
- guard_reason: planning_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:planning_mismatch

## planning_03 — FAIL

- family: planning
- prompt: عندي لخبطة بالمهام
- response: ابدأ بالجزء واضح وابدأ فيه.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## planning_04 — PASS

- family: planning
- prompt: كيف أضع أولوية لعملي
- response: اكتب خطة قصيرة: مهمة أولى ثم خطوة بعدها.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_05 — PASS

- family: planning
- prompt: وش اول شي اسويه اليوم
- response: ابدأ بقولك وتثبت مع وجود الخوف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_06 — PASS

- family: planning
- prompt: ساعدني أختار مهمة واحدة
- response: اختر المهمة الأهم والأقرب للتنفيذ.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_07 — PASS

- family: planning
- prompt: ابي طريقة سهلة للترتيب
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_08 — FAIL

- family: planning
- prompt: دلني على خطة قصيرة
- response: خلنا نبدأ بحديث لطيف عن شيء خفيف.
- guard_reason: advice_mismatch
- expected_ok: False
- family_ok: False
- reason: guard:advice_mismatch

## planning_09 — PASS

- family: planning
- prompt: مهامي كثيره ومادري من وين
- response: ابدأ بقولك وتفكر بروية.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## planning_10 — PASS

- family: planning
- prompt: كيف أبدأ بلا تشتت
- response: اختر المهمة الأهم والأقرب للتنفيذ.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_01 — PASS

- family: support
- prompt: احس بضيق بسيط
- response: تنفس بهدوء وخفها عليك خطوة خطوة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_02 — PASS

- family: support
- prompt: أحتاج جملة تهدئني
- response: تنفس بهدوء وفعلًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_03 — FAIL

- family: support
- prompt: مضغوط شوي وش اسوي
- response: بعدها خذ لحظة قصيرة.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_04 — FAIL

- family: support
- prompt: أنا مرتبك وأريد هدوءًا
- response: تنفس بهدوء وامنح نفسك لحظة راحة.
- guard_reason: planning_mismatch
- expected_ok: True
- family_ok: True
- reason: guard:planning_mismatch

## support_05 — FAIL

- family: support
- prompt: ابي اروق بدون كلام كثير
- response: ابدأ بثلاث مهام، واختر الأهم أولًا.
- guard_reason: passed
- expected_ok: False
- family_ok: False
- reason: expected_terms_missing

## support_06 — PASS

- family: support
- prompt: كيف أستعيد تركيزي بهدوء
- response: تنفس بهدوء وخذ لحظة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_07 — PASS

- family: support
- prompt: توترت من البداية
- response: تنفس بهدوء وابدأ بخطوة صغيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_08 — PASS

- family: support
- prompt: طمئني بكلام قصير
- response: تنفس بهدوء وفعلًا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## support_09 — FAIL

- family: support
- prompt: احس اني مشتت ومتوتر
- response: ابدأ بالأهم، وخله خطوة واحدة الآن.
- guard_reason: passed
- expected_ok: True
- family_ok: False
- reason: response_family_mismatch

## support_10 — PASS

- family: support
- prompt: أريد أن أهدأ قليلًا
- response: تنفس بهدوء وخذ لحظة قصيرة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_01 — PASS

- family: topic
- prompt: فسر الوفاء بجملة قصيرة
- response: الوفاء حفظ للعهد وثبات في الود.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_02 — PASS

- family: topic
- prompt: وش هو التعاون بين الناس
- response: التعاون يعني نساعد بعض وننجز سوا.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_03 — FAIL

- family: topic
- prompt: عرّف الصبر تعريفًا بسيطًا
- response: الاحترام تقدير الناس بذوق وتقدير.
- guard_reason: passed
- expected_ok: False
- family_ok: True
- reason: expected_terms_missing

## topic_04 — PASS

- family: topic
- prompt: الاحترام كيف تفهمه
- response: الاحترام يعني تقدّر الناس بقولك وفعلك.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_05 — PASS

- family: topic
- prompt: ما معنى الهدوء في الحياة
- response: الهدوء سكينة تساعدك على التفكير بوضوح.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_06 — PASS

- family: topic
- prompt: الصدق وش فايدته
- response: الصدق يعني تقول الحقيقة بوضوح.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_07 — PASS

- family: topic
- prompt: اشرح الصداقة دون إطالة
- response: الصداقة رفقة طيبة واهتمام وقت الحاجة.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_08 — PASS

- family: topic
- prompt: الشجاعة متى تظهر
- response: الشجاعة إنك تسوي الصح حتى لو كنت خايف.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_09 — PASS

- family: topic
- prompt: أعطني معنى التعاون ببساطة
- response: التعاون أن يعمل الناس معًا لهدف واضح.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed

## topic_10 — PASS

- family: topic
- prompt: وش معنى الوفاء باختصار
- response: الوفاء إنك تحفظ العهد وتثبت مع الناس.
- guard_reason: passed
- expected_ok: True
- family_ok: True
- reason: passed
