# LANGUAGE_SEGMENTATION.md

## سياسة تقسيم اللغة في SF.AI

## النطاق الحالي

النطاق الحالي فقط:

- `msa`: العربية الفصحى.
- `saudi`: اللهجة السعودية العامة وما يرتبط بها كـ metadata داخل Saudi Seed.

لا تفعيل للهجات أخرى في runtime أو training قبل قرار صريح.

## لماذا هذا مهم؟

خلط اللهجات مبكرًا يسبب:

- router signals مضللة.
- tokenizer merges غير مستقرة.
- model style غير مضبوط.
- eval ضعيف.

لذلك نبدأ بفصحى + سعودي، ثم نوسع لاحقًا بقرار وقياسات.

## Tags إلزامية

أي سجل corpus يجب أن يحتوي:

```json
{
  "provenance": {
    "language": "ar",
    "dialect": "msa أو saudi"
  }
}
```

القيم المقبولة حاليًا للتدريب الأول:

- `msa`
- `saudi`

## Arabizi

Arabizi ليس لهجة مستقلة. هو طريقة كتابة.

القواعد:

- يعالج عبر normalization خاص.
- لا يخلط مع `dialect`.
- لا يدخل training pack الأول إلا إذا وُسم بوضوح واحتوى provenance.
- تحويل Arabizi إلى عربي يجب أن يكون موثقًا وقابلًا للاختبار.

## Code

الكود ليس حوارًا عربيًا.

القواعد:

- `code` tag منفصل عن `ar`.
- لا يدخل corpus chat العربي الأول.
- tokenizer قد يدعم code لاحقًا عبر corpus منفصل وpolicy منفصلة.
- code samples لا توضع داخل Saudi/MSA chat seed إلا إذا كان المجال coding مفعّلًا بقرار.

## Lexicons مقابل corpus

`resources/lexicons/` مراجع لغوية.

`data/corpus/` بيانات تدريب.

القاموس السعودي لا يدخل training كحوار مباشر إلا بعد:

1. تحويل موثق.
2. provenance كامل.
3. dialect tag.
4. corpus audit.
5. إذن صريح إذا كان سيستخدم في training.

## Runtime language scope

runtime الحالي يحمّل:

- Arabic normalizer.
- Saudi-aware mapping.
- MSA/Saudi route hints.

لا تضف Egyptian/Levantine/Iraqi runtime mappings إلا بقرار صريح وتحديث docs/tests.
