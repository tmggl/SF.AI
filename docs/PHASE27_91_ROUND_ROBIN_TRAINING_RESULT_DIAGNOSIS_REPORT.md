# Phase 27.91 — Round-Robin Training Result Diagnosis

## الخلاصة

هذه مرحلة تشخيص فقط. لا تدريب ولا runtime.

- status: `PHASE27_91_DIAGNOSED_TOPIC_COLLAPSE_NO_TRAINING`
- decision: `DESIGN_TOPIC_OBJECTIVE_REPAIR_GATE_BEFORE_ANY_TRAINING`
- best checkpoint: `sf-10m-step1800`
- failure count: `15`
- failure families: `{'open_social': 1, 'followup': 2, 'support': 3, 'topic': 9}`
- failure buckets: `{'open_social_eval_alias_gap': 1, 'followup_surface_artifact': 2, 'support_eval_alias_gap': 3, 'topic_semantic_collapse': 7, 'topic_repetition_collapse': 2}`
- runtime release: `False`
- training allowed: `False`
- next: `Phase 27.92 — Topic Objective Repair Design Gate`

## التشخيص

Phase 27.90 improved broad dialogue families, but the remaining failures are dominated by topic collapse: 9/15 failures are topic-family cases. This is not a capacity or tokenizer justification yet; the next step is a no-training topic-objective repair design gate.

## أوزان السبب الجذري

- `topic_semantic_collapse`: `48%`
- `topic_underlearning_after_round_robin`: `18%`
- `evaluation_alias_gap_support_open_social`: `12%`
- `surface_artifacts_followup`: `8%`
- `decoding_repetition`: `6%`
- `model_capacity`: `4%`
- `tokenizer`: `2%`
- `semantic_routing`: `2%`

## أمثلة الإخفاق

### open_social_05 — open_social_eval_alias_gap

- family: `open_social`
- reason: `expected_terms_missing`
- prompt: ابي كلام عادي بدون موضوع كبير
- response: وش المكان الذي تحب تجلس فيه إذا تبي تهدأ؟
- expected_any: `['نسولف', 'موضوع', 'خفيف']`

### followup_08 — followup_surface_artifact

- family: `followup`
- reason: `expected_terms_missing`
- prompt: تابع الشرح من النقطة الأخيرة
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالأهم قبل الأشياء الجانبية.
- expected_any: `['نكمل', 'بعدها', 'الفكرة']`

### followup_10 — followup_surface_artifact

- family: `followup`
- reason: `expected_terms_missing`
- prompt: أريد صياغة أبسط للفكرة
- response: أقصد أن تجعل الأمر أصغيرة، وابدأ بالأهم قبل الأشياء شيء قصيرة.
- expected_any: `['أبسط', 'الفكرة', 'خطوة']`

### support_02 — support_eval_alias_gap

- family: `support`
- reason: `expected_terms_missing`
- prompt: أحتاج جملة تهدئني
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- expected_any: `['تنفس', 'بهدوء', 'راحة']`

### support_04 — support_eval_alias_gap

- family: `support`
- reason: `expected_terms_missing`
- prompt: أنا مرتبك وأريد هدوءًا
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- expected_any: `['تنفس', 'هدوء', 'راحة']`

### support_06 — support_eval_alias_gap

- family: `support`
- reason: `expected_terms_missing`
- prompt: كيف أستعيد تركيزي بهدوء
- response: خذ نفس شوي واهدأ، بعدها ابدأ بشي واحد بسيط.
- expected_any: `['تنفس', 'خطوة', 'راحة']`

### topic_01 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: فسر الوفاء بجملة قصيرة
- response: معنى الامتة؛ : إنك تلاحظ ح حتى لو كنت خداع.
- expected_any: `['الوفاء']`

### topic_02 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: وش هو التعاون بين الناس
- response: معنى الهدوء: إنك إن البداية هل، ل، نبدأ بالك واضح.
- expected_any: `['التعاون']`

### topic_03 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: عرّف الصبر تعريفًا بسيطًا
- response: معنى الامتنان: إنك تنتواحدًا من ف.
- expected_any: `['الصبر']`

### topic_04 — topic_repetition_collapse

- family: `topic`
- reason: `guard:repeated_phrase`
- prompt: الاحترام كيف تفهمه
- response: معنى الهدوء: إنك إن كلامك وتشكر شي شي شي صار الصواب خداع.
- expected_any: `['الاحترام']`

### topic_06 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: الصدق وش فايدته
- response: معنى الهدوء: إنك إن البداية هل، وقت الحاجة.
- expected_any: `['الصدق']`

### topic_07 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: اشرح الصداقة دون إطالة
- response: معنى الهدوء: إنك تعرف كان ة؛ تحب تجلس فيه إذا ان.
- expected_any: `['الصداقة']`

### topic_08 — topic_repetition_collapse

- family: `topic`
- reason: `guard:repeated_phrase`
- prompt: الشجاعة متى تظهر
- response: معنى الهدوء: إنك إن كلامك وتشكر شي شي شي واضح وابدأ بالجزء وتشكر .
- expected_any: `['الشجاعة']`

### topic_09 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: أعطني معنى التعاون ببساطة
- response: معنى الهدوء: إنك تعرف ووقفة وقت الحاجة.
- expected_any: `['التعاون']`

### topic_10 — topic_semantic_collapse

- family: `topic`
- reason: `expected_terms_missing`
- prompt: وش معنى الوفاء باختصار
- response: معنى الهدوء: إنك تحب تجلهدف مشبدون إذا شي شي الهدوء؟
- expected_any: `['الوفاء']`

## القرار

- لا تدريب جديد قبل Phase 27.92 design gate.
- لا runtime.
- لا SF-50M.
- لا tokenizer retrain.
