# Phase 27.23 — Semantic/Lexical Confusion Repair

## القرار

```text
PARTIAL_SEMANTIC_LEXICAL_REPAIR_BLOCK_RUNTIME
```

هذه المرحلة شغّلت probe تدريبيًا داخليًا فقط. لم تُفعّل المولد في الواجهة.

## الهدف

إصلاح ما بقي بعد Phase 27.22:

1. خلط جواب `التعاون` بين الفصحى والسعودي.
2. تحريف كلمة `الاحترام`.
3. جواب `القراءة وش تفيد` الذي كان لا يذكر `كلماتك`.

## ما جُرّب

### محاولة مرفوضة

جُرّبت حماية عبارات أوسع عبر tokenizer v4، لكنها سببت answer collapse:

```text
passed = 8/32
```

القرار: لا يُستخدم tokenizer v4 للتشغيل أو التوسعة.

### المحاولة المعتمدة

استخدمنا tokenizer v3 لأنه وصل سابقًا إلى `29/32`، ثم أضفنا تدريبًا متوازنًا:

- تكرار قاعدة الـ 32 prompt/answer حتى لا ينسى النموذج الأسئلة التي كانت تنجح.
- أمثلة contrastive محدودة للفصحى/السعودي حول التعاون والاحترام والقراءة.
- لا corpus عام جديد، ولا بيانات تشغيلية، ولا pretrained.

## النتيجة

قبل Phase 27.23:

```text
passed       = 29/32
exact_clean  = 29/32
semantic     = 30/32
guard_passed = 32/32
```

بعد Phase 27.23:

```text
passed       = 30/32
exact_clean  = 30/32
semantic     = 30/32
guard_passed = 31/32
```

## ما تحسن

- جواب `القراءة وش تفيد` صار يمر ضمن الـ 32.
- أغلب الردود صارت exact clean على نفس canary.

## ما بقي يفشل

```text
prompt    : اشرح لي التعاون
expected  : التعاون يعني أن ننجز معًا بدل الانفراد.
generated : التعاعاون يعني أن ننجز معًا بدل الانفراد.
reason    : guard:malformed_token
```

```text
prompt    : ما معنى الاحترام
expected  : الاحترام تقدير الناس بالكلام والفعل.
generated : الاحتات. واترك الناس بالكلام والفعل.
reason    : missing_semantic_terms
```

## التشخيص

المشكلة لم تعد spacing عام ولا EOS. المتبقي lexical stability في كلمتين فصيحتين:

- `التعاون`
- `الاحترام`

التكبير إلى `SF-50M` الآن سيكبر هذا الخلل بدل حله.

## قرار runtime

```text
runtime_allowed = false
sf50m_allowed   = false
```

الواجهة تبقى على router/templates. المولد لم يصبح عقل الواجهة بعد.

## التالي

```text
Phase 27.24 — Minimal Lexical Stabilization
```

هدفها ليس توسيع corpus ولا تكبير النموذج، بل علاج lexical stability لكلمتي
`التعاون` و`الاحترام` بأضيق تغيير ممكن، ثم إعادة نفس canary.

## الملفات

- `scripts/phase27_23_semantic_lexical_repair.py`
- `artifacts/reports/phase27_23_semantic_lexical_repair_report.json`
- `artifacts/samples/phase27_23_semantic_lexical_repair_generations.md`
