# first_dialogue_seed.jsonl

## الغرض

Seed صغير جدًا لاختبار بوابة حوكمة corpus قبل Phase 12.

هذا الملف لا يعني بدء التدريب، ولا يعطي إذنًا لتشغيل tokenizer training. آخر توجيه من سامي:

> لا تبدأ Phase 12 الآن. شغّل corpus-audit فقط.

## المحتوى

- عدد السجلات: 20
- المجال: `chat`
- اللغة: `ar`
- اللهجة: `saudi`
- الجودة: `gold`
- `training_allowed`: `true`
- `user_scope`: `single_user`
- `owner_user_id`: `sami-local`
- `target_user_id`: `sami-local`

## المصدر

السجلات مشتقة من مرجع محلي مملوك للمشروع:

- `Saudi Seed v1`
- ملف المهام المحلي: `data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl`

لم تُستخدم أي بيانات من LLM خارجي، ولا أي corpus خارجي، ولا أوزان أو tokenizer جاهز.

## حالة الحوكمة

آخر نتيجة متوقعة:

```text
make corpus-audit
total_records   : 20
training_ready  : 20
issues          : 0
status          : READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

## القيود

- هذا seed صغير جدًا، لا يصلح وحده لتدريب نموذج مفيد.
- يصلح فقط لاختبار مسار Phase 12 preflight.
- لا يبدأ `make train-bpe` إلا بعد إذن صريح جديد من سامي.
