# protected_terms_seed_v1.jsonl

## الغرض

Seed صغير لتغطية المصطلحات السعودية المحمية التي لم تظهر في
`first_dialogue_seed.jsonl` عند تشغيل `make tokenization-audit`.

هذا الملف لا يبدأ Phase 12 ولا يعطي إذنًا لتدريب tokenizer.

## المحتوى

- عدد السجلات: 10
- المجال: `chat`
- اللغة: `ar`
- اللهجة: `saudi`
- الجودة: `gold`
- `training_allowed`: `true`

## المصطلحات المغطاة

- `تكفين`
- `لا هنت`
- `الله لا يهينك`
- `سم`
- `أبشر`
- `حيّاك`
- `حياك`
- `يعطيك العافية`
- `ما قصرت`
- `الله يعافيك`

## المصدر

السجلات مشتقة من مرجع محلي مملوك للمشروع:

- `Saudi Seed v1`
- `resources/tokenization/protected_terms_saudi.txt`
- ملف المهام المحلي: `data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl`

لم تُستخدم أي بيانات من LLM خارجي، ولا أي corpus خارجي، ولا أوزان أو tokenizer جاهز.

## حالة الحوكمة

يجب أن يمر:

```bash
make corpus-audit
make tokenization-audit
```

ولا يبدأ التدريب إلا بإذن صريح منفصل.
