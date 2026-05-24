# Phase 27.90 — Bounded SF-10M Round-Robin Curriculum Repair Training

## الخلاصة

اكتمل تقييم التدريب المقيّد بترتيب `family_round_robin`. هذه المرحلة لا تفتح runtime مباشرة.

- status: `PHASE27_90_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_ROUND_ROBIN_TRAINING_RESULT`
- runtime release: `False`
- held-out gate allowed: `False`
- best checkpoint: `sf-10m-step1800`
- best fresh shadow: `35/50`
- held-out threshold: `45/50`
- next: `Phase 27.91 — Round-Robin Training Result Diagnosis`

## Checkpoints

### sf-10m-step600

- fresh shadow: `26/50`
- family summary: `{'followup': {'passed': 5, 'total': 10}, 'open_social': {'passed': 4, 'total': 10}, 'planning': {'passed': 10, 'total': 10}, 'support': {'passed': 7, 'total': 10}, 'topic': {'passed': 0, 'total': 10}}`
- reason counts: `{'expected_terms_missing': 23, 'passed': 26, 'guard:malformed_token': 1}`

### sf-10m-step1200

- fresh shadow: `32/50`
- family summary: `{'followup': {'passed': 6, 'total': 10}, 'open_social': {'passed': 7, 'total': 10}, 'planning': {'passed': 10, 'total': 10}, 'support': {'passed': 7, 'total': 10}, 'topic': {'passed': 2, 'total': 10}}`
- reason counts: `{'guard:repeated_phrase': 2, 'passed': 32, 'expected_terms_missing': 15, 'response_family_mismatch': 1}`

### sf-10m-step1800

- fresh shadow: `35/50`
- family summary: `{'followup': {'passed': 8, 'total': 10}, 'open_social': {'passed': 9, 'total': 10}, 'planning': {'passed': 10, 'total': 10}, 'support': {'passed': 7, 'total': 10}, 'topic': {'passed': 1, 'total': 10}}`
- reason counts: `{'passed': 35, 'expected_terms_missing': 13, 'guard:repeated_phrase': 2}`

## القرار

- لا تفعيل مباشر للواجهة من هذه المرحلة.
- لا SF-50M.
- لا tokenizer retrain.
- إذا سمحت النتيجة ببوابة held-out، فالمرحلة التالية gate إضافية لا runtime مباشر.
