# CORPUS_GOVERNANCE.md

## SF.AI — حوكمة Corpus التدريب السيادي

هذه الوثيقة تخص Phase 11. هدفها تجهيز corpus يصلح لتدريب نموذج لغوي سيادي مولّد، لا مجرد تشغيل validator شكلي.

---

## الهدف

تجهيز بيانات حوار فصحى/سعودية يملك سامي حق استخدامها، وتكون كافية لتدريب tokenizer ثم أول نموذج SF.AI صغير من الصفر.

---

## النطاق اللغوي الحالي

مسموح في pack الأول:

- `msa` — العربية الفصحى.
- `saudi` — اللهجة السعودية.

غير مقبول في pack الأول:

- `egyptian`
- `levantine`
- `iraqi`
- `gulf` كوسم عام. استخدم `saudi` إذا كانت اللهجة سعودية.
- `mixed` إلا إذا قُسّمت العينة أو وُسمت للمراجعة خارج التدريب.

---

## الصيغة التدريبية المفضلة

استخدم `StructuredSample`:

```json
{
  "domain": "chat",
  "lang": "ar",
  "messages": [
    {"role": "user", "content": "وشلونك؟"},
    {"role": "assistant", "content": "بخير، شكرًا لك."}
  ],
  "provenance": {
    "source": "sami-authored",
    "license": "user-provided",
    "language": "ar",
    "dialect": "saudi",
    "quality": "gold",
    "notes": "حوار قصير من تأليف سامي"
  }
}
```

---

## الحقول المطلوبة للتدريب

كل سجل يدخل training pack يجب أن يحتوي:

| الحقل | مطلوب | القيم |
|-------|--------|-------|
| `domain` | نعم | `chat` في Phase 11 |
| `lang` | نعم | `ar` |
| `messages` | نعم | على الأقل رسالة `user` ورسالة `assistant` |
| `provenance.source` | نعم | مثل `sami-authored` أو اسم مصدر موثّق |
| `provenance.license` | نعم | مثل `user-provided` |
| `provenance.language` | نعم | `ar` |
| `provenance.dialect` | نعم | `msa` أو `saudi` |
| `provenance.quality` | نعم | `gold`, `silver`, `bronze` |

---

## مستويات الجودة

- `gold`: مكتوب أو معتمد يدويًا من سامي، واضح، طبيعي، بلا حساسية، مناسب للتدريب.
- `silver`: جيد لكن يحتاج مراجعة أسلوبية بسيطة لاحقًا.
- `bronze`: صالح بنيويًا لكنه ضعيف لغويًا أو قصير جدًا؛ لا يبدأ به التدريب الجاد إلا إذا احتجنا الحجم.

لا تدخل `needs_review` أو `unknown` في training pack.

---

## ممنوعات corpus

- بيانات مولدة من LLM خارجي.
- بيانات بلا مصدر أو ترخيص.
- معلومات شخصية حساسة.
- نصوص محمية بحقوق نشر بدون إذن.
- لهجات خارج الفصحى/السعودي في pack الأول.
- ردود assistant تدّعي قدرات غير مفعّلة.
- نصائح طبية/قانونية/مالية/دينية/أمنية تخصصية.

---

## أداة الحوكمة

برمجيًا:

```python
from sf_ai.datasets import audit_jsonl_file_for_training

report = audit_jsonl_file_for_training("data/corpus/chat/jsonl/train_v1.jsonl")
print(report.summary())
```

القاعدة:

- `validate_jsonl_file` يتحقق أن JSONL صحيح.
- `audit_jsonl_file_for_training` يتحقق أنه مناسب للتدريب السيادي.

---

## شرط الانتقال إلى Phase 12

لا ننتقل إلى تدريب tokenizer حتى يوجد:

- ملف JSONL واحد على الأقل في `data/corpus/chat/jsonl/`.
- كل السجلات training-ready في governance audit.
- تقرير corpus يوضح عدد العينات وتوزيع `msa/saudi` وتوزيع الجودة.
- موافقة صريحة من سامي.
