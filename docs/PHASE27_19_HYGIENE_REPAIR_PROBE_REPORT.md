# Phase 27.19 — Hygiene Repair Corpus/Probe

## القرار

```text
FAILED_HYGIENE_REPAIR_PROBE_BLOCK_RUNTIME
```

هذه المرحلة اختبرت فرضية بسيطة: هل تكفي إضافة أمثلة repair مركزة حول
العبارات الخمس التي ظهرت في Phase 27.18؟

## الإعداد

```text
base_eval_records = 32
repair_records    = 20
train_records     = 52
model             = SF-10M
steps             = 3200
packing_mode      = sample_isolated
loss_scope        = assistant
```

## النتيجة

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 28/32
guard_passed = 29/32
```

النتيجة بقيت مثل Phase 27.17 تقريبًا. هذا يعني أن مجرد زيادة أمثلة حول
العبارات المتكسرة لا يكفي.

## أمثلة الفشل

```text
prompt    : السلام عليكم
generated : وعليكالسلم، أهلًا بك.
reason    : greeting_mismatch
```

```text
prompt    : اشرح لي التعاون
generated : التعاي واحد بسيط ولا تكثرها.
reason    : missing_semantic_terms
```

```text
prompt    : ما فائدة القراءة
generated : القراراءراءتفيد وتزيد المفردات.
reason    : malformed_token
```

## التشخيص

الفرضية التي فشلت:

> أمثلة repair إضافية وحدها تكفي لعلاج الكسور.

التشخيص الحالي:

- النموذج يستطيع حفظ/إنتاج معظم الأزواج.
- لكنه ما زال يخلط عبارات repair مع ردود أخرى.
- الكسور الحرفية حول العبارات عالية التجزئة باقية.

## القرار العملي

- لا تفعيل للمولد في `/ui/chat`.
- لا تدريب `SF-50M`.
- لا Phase 28.
- المرحلة التالية: Phase 27.20 — tokenizer/protected-phrase strategy قبل تدريب واسع.

## الملفات

- `scripts/phase27_19_hygiene_repair_probe.py`
- `artifacts/reports/phase27_19_hygiene_repair_probe_report.json`
- `artifacts/samples/phase27_19_hygiene_repair_probe_generations.md`
