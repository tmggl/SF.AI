# Phase 27.25 Held-out Generation Canary

## phase27_25_msa_001 — msa — greeting — FAIL

- prompt: حيّني بتحية قصيرة
- expected_terms: أهلًا
- generated: خفف الإضاءة واترك الهاتف قليلًا.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_msa_002 — msa — smalltalk — FAIL

- prompt: كيف حالك الآن
- expected_terms: بخير
- generated: خفف الإضاءة واترك الهاتف قليلًا.
- guard_reason: social_smalltalk_mismatch
- semantic_match: False
- reason: guard:social_smalltalk_mismatch

## phase27_25_msa_003 — msa — definition — PASS

- prompt: اشرح التعاون بجملة
- expected_terms: التعاون, معًا
- generated: التعاون يعني أن ننجز معًا بدل الانفراد.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_msa_004 — msa — definition — PASS

- prompt: عرّف الاحترام باختصار
- expected_terms: الاحترام, تقدير
- generated: الاحترام تقدير الناس بالكلام والفعل.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_msa_005 — msa — definition — PASS

- prompt: ما فائدة القراءة باختصار
- expected_terms: الفهم, المفردات
- generated: القراءة توسع الفهم وتزيد المفردات.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_msa_006 — msa — advice — FAIL

- prompt: أحتاج نصيحة بسيطة
- expected_terms: ابدأ, خطوة
- generated: التعاون يعني أن ننجز معًا بدل الانفراد.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_msa_007 — msa — planning — FAIL

- prompt: كيف أرتب يومي
- expected_terms: ثلاث, مهام
- generated: خفف الإضاءة واترك الهاتف قليلًا.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_msa_008 — msa — support — FAIL

- prompt: أشعر بالقلق
- expected_terms: نفس, اهدأ
- generated: التعاون يعني أن ننجز معًا بدل الانفراد.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_saudi_001 — saudi — greeting — PASS

- prompt: هلا كيف الحال
- expected_terms: هلا, تحتاج
- generated: هلا بك، تفضل وش تحتاج؟
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_saudi_002 — saudi — definition — PASS

- prompt: وش معنى التعاون
- expected_terms: سوا, الحمل
- generated: يعني نشتغل سوا ونخفف الحمل.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_saudi_003 — saudi — definition — PASS

- prompt: اشرح الاحترام
- expected_terms: تقدّر, تصرفك
- generated: يعني تقدّر الناس بكلامك وتصرفك.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_saudi_004 — saudi — definition — PASS

- prompt: وش فايدة القراءة
- expected_terms: فهمك, كلماتك
- generated: توسع فهمك وتزيد كلماتك.
- guard_reason: passed
- semantic_match: True
- reason: passed

## phase27_25_saudi_005 — saudi — advice — FAIL

- prompt: ابي نصيحة سريعة
- expected_terms: ابدأ, بسيط
- generated: يعني نشتغل سوا ونخفف الحمل.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_saudi_006 — saudi — planning — FAIL

- prompt: ودي ارتب يومي
- expected_terms: ثلاث, الأول
- generated: تم، بعطيك وابدأ بالأقرب.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_saudi_007 — saudi — support — FAIL

- prompt: متوتر شوي
- expected_terms: يهونها, اهدأ
- generated: تقدر، ابدأ بخطوة ولا توقف.
- guard_reason: passed
- semantic_match: False
- reason: missing_semantic_terms

## phase27_25_saudi_008 — saudi — thanks — PASS

- prompt: مشكور يا بعدي
- expected_terms: العفو, حاضر
- generated: العفو، حاضر بأي وقت.
- guard_reason: passed
- semantic_match: True
- reason: passed
