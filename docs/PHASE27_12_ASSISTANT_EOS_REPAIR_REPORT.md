# Phase 27.12 — Assistant Boundary/EOS Repair Report

## القرار

```text
COMPLETED_BOUNDARY_EOS_PARTIAL_SEMANTIC_BLOCKED
```

هذه مرحلة إصلاح هندسي لمشكلة Phase 27.11. لم نكبر النموذج ولم نستخدم
أي أوزان أو tokenizer خارجي. استخدمنا `<eos>` السيادي الموجود داخل
tokenizer، ثم جعلناه هدفًا صريحًا في تدريب رد المساعد، وجعلنا decoder
يتوقف عنده.

## ما أضيف

- `assistant-target` training صار يضيف `<eos>` بعد كل رد مساعد.
- `NativeGenerator` صار يمرر `eos_token_id` إلى greedy/sample decoding.
- `evaluate_tiny_lm` صار يستخدم `eos_token_id`.
- أضيف conditioning نصي بسيط من provenance:

```text
النطاق: فصحى
النطاق: سعودي
```

هذا conditioning سيادي ومصدره corpus نفسه، والغرض منه منع خلط إجابات
الفصحى والسعودي عند تشابه السؤال.

## نتيجة probe

```text
records              = 16
semantic_clean_pass  = 5/16
guard_pass           = 9/16
status               = FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING
```

التحسن واضح مقارنة بـ Phase 27.11:

- قبل EOS: `0/16 clean-stop`.
- بعد EOS + conditioning: `5/16` تطابق كامل، و`9/16` بلا فشل guard.

لكن النتيجة لا تكفي للتفعيل أو التكبير.

## التشخيص

EOS أصلح جزءًا من مشكلة التوقف، لكنه لم يحل كل شيء:

- لا يزال يوجد خلط بين ردود فصحى وسعودية في prompts مشتركة.
- micro-corpus صغير جدًا، وبعض الأمثلة ما زالت تتنافس على صيغ متقاربة.
- نحتاج تدريب v0.8 على corpus أوسع بنفس صيغة boundary + dialect conditioning.

## القرار العملي

- لا يتم تفعيل المولد في الواجهة.
- لا يبدأ `SF-50M`.
- المرحلة التالية يجب أن تكون `SF-10M v0.8` بتنسيق:
  - dialect conditioning
  - assistant `<eos>` target
  - eval split ثابت
  - generation-quality canary

## الملفات

- `sf_ai/training/train_tiny_lm.py`
- `sf_ai/modules/chat/native_generator.py`
- `sf_ai/training/evaluate_tiny_lm.py`
- `sf_ai/datasets/chat_dataset.py`
- `scripts/phase27_11_objective_probe.py`
- `artifacts/reports/phase27_12_eos_probe_report.json`
- `artifacts/samples/phase27_12_eos_probe_generations.md`
