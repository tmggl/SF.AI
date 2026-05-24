# PROJECT_PRINCIPLES.md

## SF.AI — Sovereign AI Project Principles

هذه الوثيقة تحدد المبادئ الجوهرية لمشروع SF.AI. أي مرحلة، أي قرار معماري، أي إضافة، يجب أن تخضع لهذه المبادئ. لا توجد استثناءات.

---

## الرؤية الجوهرية

SF.AI ليس chatbot.
SF.AI ليس wrapper فوق GPT أو Claude أو Gemini.
SF.AI ليس واجهة فوق نموذج جاهز.

**SF.AI هو منصة ذكاء اصطناعي خاصة بنا، تُبنى تدريجيًا، بسيادة معرفية كاملة قدر الإمكان.**

المبدأ الأعلى:

> **نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.**

---

## المبادئ العامة (Core Principles)

1. **Own the intelligence.**
2. **No external LLM APIs.** ممنوع OpenAI / Claude / Gemini / أي API ذكاء خارجي.
3. **No pretrained AI dependency.**
4. **No pretrained model weights.**
5. **No pretrained embeddings.**
6. **No pretrained tokenizer vocabulary.**
7. **No LoRA over external base models.**
8. **No external synthetic LLM data in sovereign corpus.**
9. **Modular architecture.**
10. **Arabic-first, English-aware.**
11. **Dialogue first.** الحوار العام أولًا.
12. **Web research second.** البحث في الويب ثانيًا.
13. **Sovereign acceleration allowed.** التسريع السيادي مسموح (PyTorch, MPS, MLX كأدوات حساب فقط).
14. **Tools are allowed; ready-made minds are not.**
15. **Data-first.**
16. **Safety-first.**
17. **Expand gradually.**
18. **Every phase requires approval.** كل مرحلة تتطلب إذنًا صريحًا قبل البدء.
19. **No hidden shortcuts.**

---

## تعريف السيادة في SF.AI

يوجد نوعان من الاستقلال:

### 1. الاستقلال التشغيلي
التشغيل محلي، البيانات لا تخرج، لا يوجد API خارجي.

### 2. الاستقلال المعرفي
الأوزان، التدريب، tokenizer، embeddings، البيانات المستخدمة في بناء العقل — كلها من مشروع SF.AI.

**هدف SF.AI هو الاستقلال المعرفي، وليس فقط التشغيل المحلي.**

لذلك:
- ممنوع استخدام أي نموذج مدرّب مسبقًا، حتى لو كان مفتوح الأوزان ويعمل محليًا.
- لا يوجد مسار Local Prototype بنموذج جاهز.
- لا Llama, Gemma, Phi, Mistral, أو أي بديل مشابه.
- المسار الوحيد المقبول: SF Native Model مبني من الصفر.

تفسير ملزم: **Sovereign Practical Acceleration** يعني أدوات هندسية
وتشخيصية وتدريبية فقط. لا يعني Qwen، ولا Open-Weight Lane، ولا fine-tune
فوق عقل جاهز.

---

## الفرق بين "الأدوات الجاهزة" و"العقول الجاهزة"

### أدوات جاهزة (مسموحة)
هذه أدوات بناء وحساب وتنظيم. ليست عقولًا متعلمة.

- Python
- PyTorch
- PyTorch MPS (لتسريع Apple Silicon)
- Apple MLX (كإطار حساب فقط، لا نماذجه الجاهزة)
- FastAPI
- Next.js / React / TypeScript
- PostgreSQL
- Redis
- Qdrant (مع vectors من إنتاج SF.AI فقط)
- Scrapy / Playwright / BeautifulSoup / lxml
- pandas / openpyxl
- Docker / docker-compose
- pytest / ruff / mypy
- YAML / JSON / JSONL
- Rule-based systems
- Lexical scoring
- Fuzzy matching محلي
- Hashing vectorizer محلي
- BPE tokenizer **مدرّب من الصفر على بيانات SF.AI فقط**
- Random initialization للأوزان
- Checkpoints من تدريب SF.AI فقط
- Optimizers (AdamW, …)
- Schedulers
- Gradient accumulation / checkpointing
- Mixed precision (إذا كان مستقرًا)
- Architectures معروفة بدون أخذ أوزانها:
  - Decoder-only Transformer
  - Causal Attention
  - RoPE
  - RMSNorm
  - SwiGLU
  - Weight tying

### عقول جاهزة (ممنوعة منعًا باتًا)
هذه تحمل معرفة متعلمة من جهة خارجية.

- Pretrained model weights
- Pretrained embeddings
- Pretrained tokenizer vocabulary
- OpenAI / Claude / Gemini APIs
- Llama / Gemma / Phi / Mistral weights
- أي LLM جاهز
- أي embedding model جاهز
- sentence-transformers
- HuggingFace pretrained models
- LoRA / Adapter فوق نموذج خارجي
- Synthetic data مولدة من LLM خارجي داخل corpus السيادي

**القاعدة الفاصلة:**

> إذا كان الشيء يحتوي معرفة متعلمة من جهة خارجية → ممنوع.
> إذا كان الشيء أداة حساب أو تنظيم أو تدريب → مسموح.

---

## القواعد الصارمة (Strict Rules)

### ممنوع منعًا باتًا

1. لا OpenAI API.
2. لا Claude API.
3. لا Gemini API.
4. لا أي LLM جاهز.
5. لا أي pretrained model.
6. لا أي pretrained weights.
7. لا أي pretrained embeddings.
8. لا sentence-transformers.
9. لا HuggingFace pretrained models.
10. لا tokenizer vocabulary جاهز.
11. لا tokenizer تابع لنموذج جاهز.
12. لا تنزيل أي نموذج ذكاء اصطناعي جاهز.
13. لا LoRA / Adapter فوق base model خارجي.
14. لا بيانات مولدة من LLM خارجي داخل corpus السيادي.
15. لا يكون المشروع مجرد chatbot.
16. لا اعتماد runtime على ذكاء خارجي.
17. لا خلط النظام كله في ملف واحد.
18. لا تنفيذ كل المراحل دفعة واحدة.
19. لا انتقال من مرحلة لأخرى بدون تلخيص وإذن صريح من المستخدم.
20. لا بدء تدريب الآن.
21. لا زحف للويب الآن إلا بإذن صريح.
22. لا إضافة بيانات حوار كثيرة من عند الوكيل.
23. لا بيانات غير مصرح بها.
24. لا أسرار أو API keys في الكود.
25. لا تغيير اسم المشروع.
26. لا كتابة قواميس اللغة كاملة داخل ملفات Python.
27. لا حشو lexicons بمدخلات عشوائية للوصول إلى رقم.
28. لا ادّعاء أن النظام أصبح نموذجًا ذكيًا حقيقيًا قبل التدريب الفعلي.
29. لا أي اختصار يخالف مبدأ السيادة المعرفية.
30. لا دمج أي اعتماد خارجي على نماذج ذكاء اصطناعي داخل المشروع.

---

## نظام الموافقة بين المراحل

- كل مرحلة لها أهداف ومخرجات محددة في `docs/EXECUTION_PLAN.md`.
- حالة المراحل تُسجَّل في `docs/PHASE_STATUS.md`.
- بعد إنهاء أي مرحلة، الوكيل يتوقف ويكتب ملخصًا ويطلب الإذن.
- العبارة الإلزامية في نهاية كل مرحلة:

> **"اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"**

- لا يجوز للوكيل البدء في أي مرحلة لاحقة بدون موافقة صريحة من المستخدم.

---

## الالتزام

أي مساهمة في هذا المشروع — سواء من المستخدم أو من وكيل برمجي — تخضع لهذه المبادئ.

السيادة المعرفية ليست خيارًا. هي جوهر المشروع.
