# PROJECT_IDENTITY.md

## SF.AI — هوية المشروع

SF.AI مشروع لبناء نموذج لغوي سيادي مولّد ونظام تشغيل حوله. الهدف ليس
واجهة فوق عقل جاهز، ولا بوت قواعد دائم، بل انتقال من:

```text
runtime rules + routing
→ tokenizer سيادي
→ تدريب نموذج صغير
→ checkpoint محلي
→ تقييم
→ ربط آمن داخل الشات
```

## المبدأ الأعلى

> نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.

الأدوات مسموحة إذا كانت لا تنقل معرفة نموذجية جاهزة إلى SF.AI:

- Python
- PyTorch
- FastAPI
- pytest
- BeautifulSoup/lxml
- BM25
- BPE algorithm
- AdamW

العقول الجاهزة ممنوعة:

- LLM خارجي عبر API.
- pretrained weights.
- pretrained embeddings.
- pretrained tokenizer vocabulary.
- LoRA أو fine-tuning فوق نموذج خارجي.
- synthetic LLM data من مصدر خارجي أو مجهول داخل corpus السيادي.

## ما هو المشروع الآن؟

حاليًا SF.AI ليس LLM حر التوليد. هو:

- FastAPI runtime.
- Orchestrator.
- NLP عربي rule-based.
- Router/Intent detector.
- ChatModule بقوالب.
- Composer للردود والسafety.
- Corpus governance وpreflight لمرحلة التدريب.

## ما الذي نريد الوصول إليه؟

نريد نموذجًا لغويًا سياديًا:

- يبدأ من أوزان عشوائية.
- يتعلم من corpus موثّق ومصرّح.
- يركز أولًا على العربية الفصحى واللهجة السعودية.
- ينتج text generation محليًا.
- يدخل runtime فقط بعد eval/safety gates.

## الهوية اللغوية

الأولوية الحالية:

- العربية الفصحى.
- اللهجة السعودية.

غير مرغوب الآن:

- توسيع runtime إلى لهجات أخرى.
- خلط corpus غير موثّق.
- استخدام مصادر خارجية بلا إذن.

## حدود المشروع

SF.AI لا يدّعي القدرة قبل وجودها.

- المجالات غير المفعلة تبقى `skeleton_only`.
- المجالات الحساسة تبقى safety-first.
- التدريب لا يبدأ لمجرد وجود corpus جاهز.
- جاهزية `corpus-audit` تعني “يمكن البدء بإذن”، لا “بدأ التدريب”.
