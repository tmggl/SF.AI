# PROJECT_CONSTITUTION.md

## SF.AI Engineering & Linguistic Constitution

هذه الوثيقة هي الدستور الأعلى قبل Phase 12 وما بعدها. إذا تعارض أي تنفيذ
معها، تتوقف وتطلب توضيحًا من سامي.

## المبادئ العامة

### 1. Own the intelligence

SF.AI يملك مسار ذكائه:

- corpus موثق.
- tokenizer سيادي.
- model يبدأ من أوزان عشوائية.
- checkpoints محلية.
- eval واضح.

لا يدخل “عقل جاهز” في السلسلة.

### 2. No pretrained

ممنوع:

- pretrained weights.
- open-weight pretrained models.
- Qwen/Llama/Mistral/Gemma runtime أو أي بديل مشابه.
- pretrained embeddings.
- pretrained tokenizer vocab.
- external LLM APIs.
- LoRA فوق نموذج خارجي.
- synthetic LLM data من مصادر خارجية أو غير موثقة.

تفسير ملزم: **Sovereign Practical Acceleration** لا يعني Open-Weight Lane.
هو يعني استخدام أدوات هندسية وتشخيصية وتدريبية عامة فقط. العقل الأساسي،
الأوزان، tokenizer، corpus، behavior، runtime، alignment، وevaluation
تبقى سيادية داخل مسار SF-native.

تطبيق حالي: Phase 27.92 صممت إصلاح `topic-objective` بلا تدريب، وسمحت
فقط ببوابة Phase 27.93 الجافة. هذا يثبت أن التسريع العملي لا يعني تكبير
النموذج أو إدخال أوزان جاهزة قبل فهم السبب الجذري.
بعد Phase 27.93، حتى مع نجاح بوابة renderer/masking/canary، بقي التدريب
محجوبًا بسبب فجوة بيانات `الوفاء` السعودية؛ البيانات قبل الحجم.
بعد Phase 27.94، أُغلقت فجوة `الوفاء` السعودية ببيانات gold سيادية فقط؛
القرار لا يفتح حجمًا أكبر ولا runtime، بل يسمح بمرحلة تدريب إصلاح محدودة
على SF-10M تحت gates.

استثناء موثق: يجوز إدخال حوارات **owner-delegated agent-authored** في
corpus إذا كان سامي قد فوّض الوكيل صراحة بتأليفها واعتمادها، وكانت كل
سجلاتها تحمل `source/license/quality/training_allowed/notes` يشرح أنها
مؤلفة بتفويض المالك لمشروع SF.AI فقط. هذا ليس استدعاء LLM خارجي ولا
pretrained shortcut؛ هو تأليف تشغيلي شفاف داخل المشروع.

### 3. Arabic-first

العربية هي اللغة الأساسية للتجربة الأولى:

- كتابة الوثائق التشغيلية للمستخدم بالعربية الواضحة.
- corpus الأول عربي.
- tokenizer policy تراعي UTF-8 والعربية.
- eval الأول يقيس العربية قبل أي لغة أخرى.

### 4. Saudi-aware

SF.AI يجب أن يفهم اللهجة السعودية تدريجيًا بدون إفساد الفصحى:

- Saudi Seed v1 مرجع محلي خاص.
- المصطلحات السعودية الشائعة لها protected terms.
- اللهجات السعودية الداخلية توثق كـ metadata، ولا تتحول إلى runtime dialects جديدة بلا قرار.

### 5. Runtime ≠ Training

runtime يخدم المستخدم. training ينتج artifacts.

لا request من المستخدم داخل runtime يبدأ تدريبًا أو يكتب checkpoints.

### 6. No hidden shortcuts

لا shortcuts مخفية:

- لا API خارجي تحت اسم helper.
- لا model download.
- لا tokenizer جاهز.
- لا fallback غير موثق.

### 7. Safety-first

المجالات الحساسة لا تُفعّل بمجرد وجود module:

- medical
- legal
- finance
- security
- religion

الرد الآمن أولًا حتى توجد gates واضحة.

### 8. Data provenance required

كل سجل training يجب أن يحتوي:

- `source`
- `license`
- `language`
- `dialect`
- `quality`
- `training_allowed`
- `owner_user_id`
- `created_by_user_id`
- `target_user_id`
- `user_scope`

لا corpus مجهول، ولا بيانات بلا حق استخدام.

### 8.1 Natural Dialogue Only

corpus الحوار العام يجب أن يعلّم SF.AI كلام البشر الطبيعي، لا طريقة إدارة
المشروع. لذلك يمنع نهائيًا إدخال:

- أوامر تشغيل مثل: `التالي`, `اكمل`, `ارفع`.
- مفردات هندسية/داخلية مثل: `phase`, `gates`, `corpus`, `tokenizer`,
  `pytest`, `commit`, `readiness`.
- أي حوار عن إدارة المشروع أو تشغيل الوكيل أو workflow داخلي.
- أي persona خاصة بسامي أو أسلوب إدارته للمشروع.

أي سجل من هذا النوع يصنّف:

```text
training_forbidden_operational_internal_dialogue
```

ويحذف من corpus التدريبية ولا يعامل كـ review-only.

### 9. User-Scoped Data

كل حوار يصدر من مستخدم محدد ويعود لمستخدم محدد. في الوضع الحالي:

```text
owner_user_id = sami-local
created_by_user_id = sami-local
target_user_id = sami-local
user_scope = single_user
```

لا يجوز تدريب أو تخصيص أو RAG لاحقًا على بيانات بلا مالك واضح. هذه القاعدة
موجودة الآن حتى يكون التوسع متعدد المستخدمين لاحقًا آمنًا، وحتى لا تختلط
ذاكرة أو corpus مستخدم بمستخدم آخر.

### Owner-Delegated Agent-Authored Data

عندما يصرّح سامي للوكيل بأن يعتمد أي حوار يؤلفه لخدمة الهدف، يصبح هذا
الحوار مقبولًا للتدريب بشرط:

- `source` يبدأ بـ `sf-ai-owner-delegated-agent-authored-`.
- `license=owner-approved-for-sf-ai-training`.
- `training_allowed=true`.
- `quality` لا تتجاوز `silver` إلا بعد مراجعة بشرية لاحقة.
- `dialect ∈ {msa, saudi}` في النطاق الحالي.
- `owner_user_id`, `created_by_user_id`, و`target_user_id` تشير إلى سامي في المسار الحالي.
- `user_scope=single_user`.
- `notes` تذكر التفويض وتاريخ المحادثة، وتؤكد عدم وجود corpus خارجي أو
  pretrained model data.

يظل ممنوعًا إدخال بيانات مولدة من LLM خارجي أو مصادر مجهولة أو نصوص منسوخة
بلا إذن.

### 10. Progressive Scaling Strategy

لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

أي انتقال إلى حجم أكبر يحتاج passing scaling gate:

- corpus readiness.
- tokenization audit.
- evaluation suite.
- safety checks.
- runtime quality.
- hallucination checks.
- repetition checks.
- resource readiness.

ممنوع على أي Agent القفز إلى حجم كبير لأن المستخدم متحمس أو لأن الجهاز يسمح. الحجم التالي يُفتح فقط إذا أثبت الحجم الحالي قيمة واضحة.

### 10.1 Auto-Advance Scaling Mandate

عندما تنجح بوابة الحجم التالي، ينتقل الوكيل تلقائيًا إلى الحجم التالي
دون انتظار موافقة جديدة من سامي، حتى نصل تدريجيًا إلى `SF-1B+`.

هذا التفويض لا يلغي القيود:

- لا تدريب أكبر قبل `ENGINEERING_ROOT_CAUSE_GATE`.
- لا تكبير إذا كان السبب الأكبر objective/curriculum/decoding/family mixing.
- لا runtime release بدون `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- لا pretrained ولا vocab جاهز ولا datasets خارجية.
- لا قفز فوق سلم الأحجام.

المقصود بـ `M100` في أوامر سامي هو مستوى `SF-100M-class`، والمستوى
المعماري المسجل حاليًا هو `SF-120M` ما لم يعتمد تقرير معماري لاحق حجمًا
دقيقًا باسم `SF-100M`.

### 11. Sovereign Practical Acceleration Strategy v2

SF.AI لا يعيد اختراع الأدوات الرياضية والهندسية العامة من الصفر. التسريع
المسموح هو تسريع هندسي سيادي: نستخدم أدوات التدريب والقياس والتحسين
العامة، ونحافظ على ملكية الذكاء نفسه.

السيادة الكاملة تبقى على:

- `corpus`.
- `tokenizer`.
- `behavior`.
- `runtime`.
- `alignment`.
- `evaluation`.
- سلوك الحوار العربي الفصيح والسعودي.

المسموح لأنه أدوات هندسية لا عقول جاهزة:

- PyTorch.
- AMP / mixed precision.
- TensorBoard محلي.
- schedulers.
- experiment tracking.
- advanced decoding.
- repetition control.
- curriculum tooling.
- held-out canary.
- shadow canary.
- family-conditioned dialogue.
- contrastive evaluation.
- semantic routing diagnostics.
- objective tracing.
- anti-collapse diagnostics.
- local RLHF-lite / DPO / ORPO / preference optimization.
- LoRA / QLoRA فوق أوزان SF.AI فقط، لا فوق نموذج خارجي.
- retrieval memory tooling.
- local vector retrieval.
- dialogue family balancing.
- EOS boundary tooling.
- checkpoint selector.
- tokenizer boundary audit.

الممنوع لأنه يكسر السيادة أو يلوث السلوك:

- pretrained weights.
- open-weight pretrained models.
- Qwen/Llama/Mistral/Gemma أو أي runtime فوق نموذج جاهز.
- pretrained vocab.
- pretrained tokenizer merges.
- hidden hosted APIs.
- external reasoning services.
- external dialogue datasets.
- project-workflow dialogue contamination داخل أي corpus تدريبية.
- fake benchmark inflation.
- template masking لإخفاء ضعف المولد.

لا يتم تكبير النموذج قبل فهم limit الحالي. التركيز الرسمي قبل أي `SF-50M`
هو:

- behavior.
- generalization.
- dialogue flow.
- clean-stop.
- open_social stability.

تُعد `tokenizer`, `EOS`, `dialogue-family balance`, و`decoding` أجزاء
أساسية من الذكاء، وليست تحسينات ثانوية. ولا يعتمد المشروع `loss` وحدها
كمؤشر نجاح؛ معيار النجاح الحقيقي هو held-out dialogue quality,
open_social stability, semantic correctness, clean-stop, وruntime usability.

قبل أي تدريب جديد يجب تنفيذ:

```text
ENGINEERING_ROOT_CAUSE_GATE
```

ويجب أن يجيب بوضوح عن وزن كل عامل:

- capacity.
- objective.
- curriculum.
- tokenizer.
- decoding.
- family mixing.
- memorization.
- weak generalization.
- EOS.
- repetition.
- semantic routing.

لا runtime release بدون:

```text
NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS
```

ومعايير النجاح الرسمية هي: held-out dialogue quality, runtime usability,
clean-stop, semantic correctness, family stability, open_social naturalness,
followup continuity, canary pass rate, وhuman conversation realism. ليست
`loss` ولا `perplexity` ولا micro-probe وحدها كافية.

## صلاحية الدستور

هذا الدستور يحكم:

- إضافة البيانات.
- تدريب tokenizer.
- تدريب model.
- ربط checkpoint بالruntime.
- عمل أي Agent على المشروع.

## متى يتغير؟

يتغير فقط بتحديث موثق في commit واضح، وبعد موافقة صريحة إذا كان التغيير يمس:

- pretrained policy.
- language scope.
- tokenizer policy.
- training gates.
- safety gates.
- scaling gates.
