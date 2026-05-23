# Phase 27.9 — Generation Quality Harness Report

## القرار

```text
COMPLETED_GENERATION_QUALITY_HARNESS_BLOCKING_V0_6
```

تم تثبيت بوابة جودة آلية للمولد الخام. هذه البوابة تقيس التوليد القصير
مباشرة من checkpoint، خارج واجهة الشات، ثم تمرر النص عبر canary.

## ما أضيف

- Prompt suite:
  - `eval/prompts/generation_quality_v1.json`
- Harness:
  - `sf_ai/evaluation/generation_quality.py`
- CLI:
  - `scripts/phase27_9_generation_quality_eval.py`
- Make target:
  - `make phase27-generation-quality`
- Reports:
  - `eval/reports/generation_quality_v1.json`
  - `artifacts/reports/generation_quality_v1_report.json`

## نتيجة `SF-10M v0.6`

```text
generator       = sf_10m_v0_6
checkpoint      = sf-10m-step4000
prompts         = 10
passed          = 0
failed          = 10
pass_rate       = 0.00%
runtime_allowed = false
primary reason  = model_artifact_fragment
```

## لماذا هذا مهم؟

perplexity تحسن في Phase 27.8، لكنه لم يضمن جودة الحوار. Phase 27.9 تجعل
القرار قابلًا للتكرار: أي checkpoint لا يمر من هذه البوابة لا يدخل الواجهة
ولا يفتح SF-50M.

## التالي

ابدأ إصلاح مصدر fragments:

- فحص decoding/tokenization حول الكلمات المشوهة.
- زيادة gold social القصير عالي الجودة.
- تجربة تدريب/تقييم أقصر على prompts اجتماعية قبل أي تكبير.
