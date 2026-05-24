# Phase 27.87 — Bounded Family-conditioned SF-10M Repair Training

## الخلاصة

اكتمل التدريب المقيّد بعد إصلاح renderer. لا يوجد runtime release من هذه المرحلة.

- status: `PHASE27_87_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_FAMILY_CONDITIONED_TRAINING_RESULT`
- runtime release: `False`
- best checkpoint: `sf-10m-step600`
- best fresh shadow: `10/50`
- runtime threshold: `45/50`
- next: `Phase 27.88 — Family-conditioned Training Result Diagnosis`

## Checkpoints

### sf-10m-step600

- fresh shadow: `10/50`
- family summary: `{'followup': {'passed': 1, 'total': 10}, 'open_social': {'passed': 9, 'total': 10}, 'planning': {'passed': 0, 'total': 10}, 'support': {'passed': 0, 'total': 10}, 'topic': {'passed': 0, 'total': 10}}`
- reason counts: `{'passed': 10, 'expected_terms_missing': 35, 'guard:planning_mismatch': 3, 'guard:advice_mismatch': 1, 'guard:support_mismatch': 1}`

### sf-10m-step1200

- fresh shadow: `10/50`
- family summary: `{'followup': {'passed': 0, 'total': 10}, 'open_social': {'passed': 0, 'total': 10}, 'planning': {'passed': 10, 'total': 10}, 'support': {'passed': 0, 'total': 10}, 'topic': {'passed': 0, 'total': 10}}`
- reason counts: `{'response_family_mismatch': 4, 'expected_terms_missing': 35, 'passed': 10, 'guard:support_mismatch': 1}`

### sf-10m-step1800

- fresh shadow: `7/50`
- family summary: `{'followup': {'passed': 0, 'total': 10}, 'open_social': {'passed': 0, 'total': 10}, 'planning': {'passed': 0, 'total': 10}, 'support': {'passed': 7, 'total': 10}, 'topic': {'passed': 0, 'total': 10}}`
- reason counts: `{'expected_terms_missing': 31, 'response_family_mismatch': 10, 'guard:too_short': 1, 'guard:advice_mismatch': 1, 'passed': 7}`

## القرار

- لا تفعيل للواجهة من هذه المرحلة.
- لا SF-50M.
- لا tokenizer retrain.
- أي انتقال لاحق يعتمد على تقرير التشخيص أو بوابة held-out إذا تجاوزت النتيجة الحد.
