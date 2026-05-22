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
- pretrained embeddings.
- pretrained tokenizer vocab.
- external LLM APIs.
- LoRA فوق نموذج خارجي.
- synthetic LLM data من مصادر خارجية أو غير موثقة.

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
SF-10M → SF-50M → SF-120M → SF-350M → SF-700M → SF-1B+
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
