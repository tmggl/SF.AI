# data/corpus/chat

أرشيف بيانات الحوار لـ SF.AI.

> **مهم:** هذا المجلد فارغ في Phase 5. لا يجوز لأي وكيل برمجي إضافة بيانات هنا تلقائيًا. المستخدم هو من يضع البيانات.

---

## الهيكل

```
data/corpus/chat/
├── raw/        # الملفات كما وردت من المصدر (UTF-8 plain / JSON / JSONL / TXT)
├── cleaned/    # بعد تشغيل SampleCleaner
└── jsonl/      # JSONL النهائي الجاهز للاستخدام
```

---

## الصيغ المدعومة

كل سطر في JSONL هو **سجل واحد**. تفاصيل كاملة في [docs/DATASET_FORMAT.md](../../../docs/DATASET_FORMAT.md).

### الصيغة البسيطة (SimpleSample)

```json
{"text": "المستخدم: مرحبا\nالمساعد: أهلاً كيف حالك"}
```

### الصيغة المنظمة (StructuredSample)

```json
{
  "domain": "chat",
  "lang": "ar",
  "messages": [
    {"role": "user", "content": "مرحبا"},
    {"role": "assistant", "content": "أهلاً كيف حالك"}
  ],
  "provenance": {
    "source": "اسم المصدر",
    "license": "user-provided",
    "language": "ar",
    "dialect": "msa"
  }
}
```

---

## كيف تضيف بيانات

1. ضع الملفات الخام في `raw/` مع `provenance.json` يصف:
   - المصدر.
   - تاريخ الجلب.
   - الترخيص.
   - اللغة / اللهجة.
2. شغّل `python scripts/validate_dataset.py data/corpus/chat/raw/your_file.jsonl`.
3. إذا تم التحقق بنجاح، انقل إلى `jsonl/` بعد التنظيف.

---

## محظورات

- ❌ بيانات مولدة من LLM خارجي (OpenAI/Claude/Gemini/أي LLM جاهز).
- ❌ بيانات بدون مصدر/ترخيص موثق.
- ❌ معلومات شخصية حساسة.
- ❌ تعديل ملفات الخام من قِبل أي وكيل برمجي.

كل ما تقع عليه من البيانات بهذه الصفات يُرفض ويُحذف.
