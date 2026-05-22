# DATASET_FORMAT.md

## SF.AI — صيغ بيانات الحوار

هذا المرجع الرسمي لصيغ بيانات الحوار المقبولة في `data/corpus/chat/`.

> **القاعدة:** UTF-8، JSONL (سطر واحد = سجل واحد). كل ملف يُفضَّل أن يصاحبه `provenance.json` يصف مصدره وترخيصه.

---

## محظورات السيادة المعرفية

قبل أي شيء — هذه الأنواع ممنوعة في corpus السيادي:

- ❌ **بيانات مولدة من LLM خارجي** (OpenAI / Claude / Gemini / Llama / ...). تكسر مبدأ "Own the intelligence".
- ❌ **بيانات بدون مصدر/ترخيص**.
- ❌ **معلومات شخصية حساسة**.
- ❌ **محتوى محمي بحقوق نشر بدون إذن**.

اقرأ [PROJECT_PRINCIPLES.md](../PROJECT_PRINCIPLES.md) للقائمة الكاملة.

---

## النوع 1 — SimpleSample

سطر واحد بحقل `text` يحوي نصًا مع علامات أدوار اختيارية:

```json
{"text": "المستخدم: مرحبا\nالمساعد: أهلاً كيف حالك"}
```

### علامات الأدوار المدعومة

| علامة بالعربية | بالإنجليزية |
|----------------|--------------|
| `المستخدم:` | `user:` |
| `المساعد:` | `assistant:` |
| `النظام:` | `system:` |

العلامات case-insensitive للإنجليزية. الأسطر بدون علامة تُلحَق بالدور السابق.

نص بدون أي علامة → يُعتبر سطرًا واحدًا من المستخدم.

---

## النوع 2 — StructuredSample

```json
{
  "domain": "chat",
  "lang": "ar",
  "messages": [
    {"role": "user", "content": "مرحبا"},
    {"role": "assistant", "content": "أهلاً كيف حالك"}
  ],
  "provenance": {
    "source": "https://example.com/dataset",
    "license": "CC-BY-4.0",
    "fetched_at": "2026-05-22",
    "language": "ar",
    "dialect": "msa",
    "quality": "gold",
    "notes": "ملاحظات اختيارية"
  }
}
```

### الحقول

| الحقل | إلزامي | القيم المقبولة |
|--------|--------|----------------|
| `messages` | نعم | قائمة من `{role, content}`. `role ∈ {user, assistant, system}`. `content` غير فارغ |
| `domain` | لا (الافتراضي `chat`) | اسم مجال من registry |
| `lang` | لا (الافتراضي `unknown`) | `ar / en / mixed / code / unknown` |
| `provenance` | اختياري لكن مُستحسَن | انظر أسفل |

### Provenance

كل الحقول اختيارية فرديًا لكن **يجب** ملء واحد على الأقل من `source` أو `license`:

```json
{
  "source": "string — رابط/اسم المصدر",
  "license": "SPDX id أو 'user-provided'",
  "fetched_at": "ISO 8601 date",
  "language": "ar / en / ...",
  "dialect": "msa / saudi / ...",
  "quality": "gold / silver / bronze",
  "notes": "اختياري"
}
```

في Phase 11، بيانات التدريب الأولى تقبل `dialect ∈ {msa, saudi}` فقط.

---

## التحقق

```bash
# ملف واحد
python scripts/validate_dataset.py data/corpus/chat/jsonl/my_file.jsonl

# مجلد كامل (يبحث *.jsonl تكراريًا)
python scripts/validate_dataset.py data/corpus/chat/jsonl
```

يعرض:
- عدد الأسطر الإجمالي.
- عدد العينات الصحيحة.
- المشاكل بالسطر مع snippet.
- إحصاءات: edges حسب الدور (user/assistant/system)، إجمالي الأحرف.

نوع المشكلة (`SampleIssue.kind`):
- `json` — JSON غير صحيح.
- `schema` — الحقول لا تطابق الـ schema.
- `encoding` — مشكلة UTF-8 أو ملف غير موجود.

---

## التنظيف (Cleaning)

`SampleCleaner` يفعل ما يلي على كل رسالة:

1. إزالة control chars (Cc).
2. إزالة format chars (Cf): RLM/LRM/ZWNJ/ZWJ/BOM.
3. **الحفاظ على** `{} [] () ; : / \ . _ - = + * < >` لتفادي إفساد الأكواد/الروابط.
4. (اختياري) `normalize=True` → ArabicNormalizer كامل (tashkeel/tatweel/alef/yaa/digits).

التنظيف **لا يحذف أي معنى دلالي**. الرسائل التي تصبح فارغة بالكامل بعد التنظيف تُسقَط من العينة المنظفة (Structured) أو تُسقَط العينة كاملة (Simple).

---

## التحميل البرمجي

```python
from sf_ai.datasets import ChatDataset, SampleCleaner

ds = ChatDataset(
    root="data/corpus/chat/jsonl",
    cleaner=SampleCleaner(normalize=False),  # normalize=True للتدريب
)

# الإحصاءات
print(ds.stats())

# Stream للعينات
for sample in ds.iter_samples():
    ...

# Stream لكل الرسائل (مسطّحًا)
for msg in ds.iter_messages():
    print(msg.role, msg.content)
```

> `iter_samples` و `iter_messages` كلاهما generator: يقرأ سطرًا سطرًا بدون تحميل الـ corpus بالكامل في الذاكرة.

---

## ما لم يُنفَّذ بعد (مقصود)

- ❌ تدريب — يأتي في Phase 5.5 (tokenizer) و Phase 6 (model).
- ❌ التحميل من قواعد بيانات — JSONL ملفات فقط في Phase 5.
- ❌ التقسيم train/val/test تلقائيًا — يأتي في Phase 6 حين يبدأ التدريب.
- ❌ Deduplication / quality scoring — Phase 6 سيضيفهم عند الحاجة.

---

## ملاحظة عن الحجم

الـ pipeline مصمَّم على الـ streaming. لا حد أعلى صريح لحجم الملف الواحد، لكن:

- ملفات > 100MB: قسّم لراحة `git`.
- corpus كامل > 1GB: ضع `.gitignore` ينفي الـ raw، يحتفظ بهيكل المجلدات و provenance.
