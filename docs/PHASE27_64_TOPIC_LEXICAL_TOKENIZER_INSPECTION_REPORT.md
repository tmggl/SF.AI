# Phase 27.64 — Topic Lexical/Tokenizer Inspection

## الخلاصة

هذه مرحلة فحص فقط: لا تدريب، لا فتح واجهة، ولا تبديل runtime.

- status: `COMPLETED_TOPIC_LEXICAL_INSPECTION_TOKENIZER_V8_REQUIRED_RUNTIME_BLOCKED`
- Phase 27.63 canary: `26/30`
- tokenizer v8 required: `True`
- next tokenizer probe allowed: `True`

## المصطلحات الحرجة

- `التعاون` في tokenizer v7: `3` pieces, protected=`False`
- `الاحترام` في tokenizer v7: `4` pieces, protected=`False`

## التشخيص

- `التعاون` و`الاحترام` كانا single-piece في tokenizer v6، ثم تراجعا في tokenizer v7.
- فشل Phase 27.63 المتبقي متركز في topic وليس في open_social/planning/support.
- إضافة تدريب LM جديد قبل إصلاح tokenizer ستكرر نفس الانهيار اللفظي.

## القرار

Tokenizer v8 is required before another LM repair: v7 regressed critical topic terms that v6 protected as single pieces.

## التالي

Phase 27.65 — train tokenizer v8 with Phase 27.64 protected topic pack and rerun bounded topic probe
