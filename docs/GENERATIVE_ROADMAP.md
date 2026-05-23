# GENERATIVE_ROADMAP.md

## SF.AI — خارطة الوصول إلى حوار مولّد مقنع

**Journey:** Phase 21 / 30  
**Language track:** Arabic MSA + Saudi only  
**Lexicon track:** Saudi Seed v1 + governed MSA/Saudi corpus  
**Goal:** الانتقال من router/templates إلى نموذج لغوي سيادي مولّد يستطيع محاورة سامي بردود طبيعية.

---

## الحقيقة الحالية

SF.AI يملك الآن:

- `Router + NLP + templates` لردود اجتماعية مفهومة.
- `SF-10M v0.1` مولّد خام، سيادي، لكنه مكرر وضعيف.
- واجهة تعرض هل الرد `template` أو `sf_10m_v0_1`.
- corpus تدريبي صغير جدًا: `30` محادثة سعودية gold.

هذا يعني:

- نعم، بدأ التدريب الفعلي سابقًا في Phase 13/14.
- لا، لم نصل بعد إلى حوار مولّد مقنع.
- السبب ليس الكود فقط؛ السبب الأساسي هو صغر البيانات وضعف تغطية الفصحى/السعودي الحوارية.
- لا تطلب من سامي اختبار `chat_patterns.py` كأنه مولد؛ هذه قوالب ثابتة وليست نتيجة تدريب.

---

## متى نبدأ التدريب الفعلي؟

بدأ التدريب الفعلي بالفعل:

| المرحلة | ماذا حدث؟ | النتيجة |
|---------|-----------|---------|
| Phase 12 | تدريب tokenizer سيادي من الصفر | مكتمل بحدود؛ corpus سعودي صغير |
| Phase 13 | smoke LM training | أول نص خام غير فارغ |
| Phase 14 | SF-10M v0.1 | checkpoint حقيقي لكنه مكرر |

التدريب التالي المفيد يبدأ عند:

| المرحلة | التدريب | شرط البدء |
|---------|---------|-----------|
| Phase 24 | `SF-10M v0.2` | 500 سجل حوار محكوم على الأقل |
| بعد Phase 27 | `SF-50M v0.1` | توسعة corpus إلى 5000 + إعادة Phase 26 readiness |
| Phase 28 | `SF-120M v0.1` | نجاح SF-50M + scaling gate |

---

## متى أصل إلى حوار مولّد يقنعني؟

توقع واقعي:

- **Phase 24:** أول تحسن واضح على SF-10M، لكنه قد يبقى متقطعًا.
- **Phase 25:** تجربة مولّد داخل الشات بشكل محكوم، مع fallback لو كرر أو هلوس.
- **Phase 26:** بوابة readiness رفضت SF-50M الآن.
- **Phase 27:** eval v2 مرّر التوجيه، لكنه أثبت أن الردود لا تزال `template` وأن corpus يحتاج توسعة.
- **Phase 28:** أول قفزة بعد SF-50M إذا أثبت 50M قيمة واضحة.
- **Phase 29:** إدخاله في الواجهة كتجربة يومية مع router/safety/memory.

الخلاصة:

> أول “مولّد حقيقي” بدأ في Phase 13، لكن أول “حوار مولّد يقنع سامي” صار مشروطًا بتنفيذ خطة Phase 27 ثم نجاح `SF-50M`.

---

## مراحل ما بعد Phase 20

### Phase 21 — Generative Roadmap & Quality Targets

تثبيت خارطة الطريق، مقاييس الجودة، وتعريف معنى “مولّد مقنع”.

**النجاح:** كل Agent يعرف متى يدرب، متى يقيّم، ومتى يمنع runtime.

### Phase 22 — Gold Dialogue Corpus v2

توسيع corpus إلى 500 سجل على الأقل:

- فصحى + سعودي فقط.
- user-authored أو user-reviewed أو owner-delegated agent-authored فقط.
- لا synthetic LLM data من مصدر خارجي أو مجهول.
- كل سجل يحمل `source/license/quality/training_allowed/dialect`.

**النجاح:** `make corpus-audit` يمر، والتوازن اللغوي لا يفتقد `msa`.

### Phase 23 — Tokenizer v2 Retrain & Audit

إعادة تدريب tokenizer من corpus الأكبر.

**النجاح:** حماية الكلمات السعودية الشائعة، عدم كسر protected terms، وتحسن coverage.

### Phase 24 — SF-10M v0.2 Quality Training

أول تدريب جودة بعد corpus أكبر.

**النجاح:** loss/perplexity أفضل من v0.1، وعينات توليد أقل تكرارًا.

### Phase 25 — Generated Chat Canary v1

إدخال المولد في الشات فقط على prompts آمنة، مع detector للتكرار والردود الرديئة.

**النجاح:** الواجهة تريك رد مولّد حقيقي حين ينجح، وتسقط لقالب/توضيح حين يفشل.

### Phase 26 — SF-50M v0.1 Readiness

بوابة readiness قبل أي `SF-50M`.

**النتيجة:** `can_start_sf50m_training=false` حتى يتوسع corpus وتنجح جودة runtime.

### Phase 27 — Dialogue Evaluation v2

تقييم متعدد الأدوار + خطة توسعة corpus:

- اجتماعي.
- سؤال/جواب.
- فصحى.
- سعودي.
- رفض حساس.
- كشف تكرار.

**النتيجة:** baseline pass `19/19`، لكن `generator=template`. بعد أول دفعة توسعة بقي `4450` سجلًا قبل إعادة SF-50M gate.

### Phase 28 — SF-120M v0.1 Candidate

أول قفزة بعد نجاح SF-50M، لا قبل ذلك.

**النجاح:** أول هدف رسمي لحوار مولّد مقنع ومستقر نسبيًا.

### Phase 29 — Runtime Hybrid Assistant v1

دمج:

- generator
- router
- safety
- memory/RAG
- fallback

**النجاح:** الواجهة تصبح مساعدًا مولدًا، لا مجرد قوالب، مع تشخيص صادق.

### Phase 30 — Continuous Improvement Loop

دورة:

اختبار سامي → export → review → corpus → tokenizer/model عند الحاجة → eval → runtime.

**النجاح:** كل أسبوع/دورة يمكن قياس التحسن دون إدخال عقل خارجي.

---

## ماذا تكتب لتختبر الآن؟

للتأكد من فصل القالب عن المولد:

```text
كيفك
وين كنت
هل تفهم
وش رايك اليوم
اكتب لي رد قصير لصديق
```

المتوقع الآن:

- الأولى اجتماعية مفهومة غالبًا `template`.
- الأسئلة المفتوحة تكشف `SF-10M v0.1` الخام، وغالبًا ستظهر ضعيفة.

بعد Phase 24 نعيد نفس الاختبار، ونقيس هل صار المولد أقل تكرارًا.
