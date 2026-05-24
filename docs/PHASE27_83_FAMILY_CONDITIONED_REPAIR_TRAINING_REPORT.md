# Phase 27.83 — Family-conditioned SF-10M Bounded Repair Training

## الخلاصة

اكتمل تدريب الإصلاح المحدود، لكنه فشل في بوابة الحوار غير المرئي.

- status: `PHASE27_83_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_OBJECTIVE_CURRICULUM_FAILURE`
- runtime release: `False`
- best by canary: `sf-10m-step1200`
- best by eval loss: `sf-10m-step600`
- next: `Phase 27.84 — Objective/Curriculum Failure Diagnosis`

## Checkpoints

### sf-10m-step600

- fresh shadow: `7/60`
- eval loss: `3.7397`
- perplexity: `42.08`
- family summary: `{'followup': {'passed': 0, 'total': 12}, 'open_social': {'passed': 5, 'total': 12}, 'planning': {'passed': 1, 'total': 12}, 'support': {'passed': 1, 'total': 12}, 'topic': {'passed': 0, 'total': 12}}`
- sample: `عندما تريد الهدوءخفيف عن يومك.`

### sf-10m-step1200

- fresh shadow: `11/60`
- eval loss: `5.9248`
- perplexity: `374.19`
- family summary: `{'followup': {'passed': 0, 'total': 12}, 'open_social': {'passed': 1, 'total': 12}, 'planning': {'passed': 10, 'total': 12}, 'support': {'passed': 0, 'total': 12}, 'topic': {'passed': 0, 'total': 12}}`
- sample: `اكتب ثلاث وابدأ بالأهم وقت لاحقم، وابدأ بالأهم لمعشدقيقة.`

### sf-10m-step1800

- fresh shadow: `3/60`
- eval loss: `5.9722`
- perplexity: `392.39`
- family summary: `{'followup': {'passed': 0, 'total': 12}, 'open_social': {'passed': 0, 'total': 12}, 'planning': {'passed': 0, 'total': 12}, 'support': {'passed': 3, 'total': 12}, 'topic': {'passed': 0, 'total': 12}}`
- sample: `بعد ه. ه. ه. شيء أأأن تجيرة، وابدأ بشي بشي بشي عل عل عل إذا تجلوقت ثتجلس فيه واضح.`

## القرار

- لا تفعيل للواجهة.
- لا runtime release.
- لا SF-50M.
- لا tokenizer retrain الآن.
- المرحلة التالية تشخيص objective/curriculum failure بدل تدريب أعمى جديد.
