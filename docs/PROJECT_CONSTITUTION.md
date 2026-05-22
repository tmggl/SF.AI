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
- synthetic LLM data.

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

لا corpus مجهول، ولا بيانات بلا حق استخدام.

### 9. Progressive Scaling Strategy

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
