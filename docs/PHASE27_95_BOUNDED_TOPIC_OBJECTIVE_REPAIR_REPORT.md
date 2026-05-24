# Phase 27.95 — Bounded Topic Objective Repair Training

## الخلاصة

هذه مرحلة تدريب محدودة على SF-10M فقط. لا تفتح runtime أو الواجهة.

- status: `PHASE27_95_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_OBJECTIVE_REPAIR_RESULT`
- best checkpoint: `sf-10m-step1800`
- known topic: `10/16`
- fresh topic: `4/10`
- all family: `33/50`
- held-out gate allowed: `False`
- runtime release: `False`
- next: `Phase 27.96 — Topic Objective Repair Result Diagnosis`

## Checkpoints

### sf-10m-step600

- known topic: `4/16`
- fresh topic: `2/10`
- all family: `25/50`
- known reasons: `{'required_topic_missing': 12, 'passed': 4}`
- fresh reasons: `{'expected_terms_missing': 8, 'passed': 2}`

### sf-10m-step1200

- known topic: `7/16`
- fresh topic: `2/10`
- all family: `33/50`
- known reasons: `{'required_topic_missing': 9, 'passed': 7}`
- fresh reasons: `{'expected_terms_missing': 7, 'passed': 2, 'guard:repetition': 1}`

### sf-10m-step1800

- known topic: `10/16`
- fresh topic: `4/10`
- all family: `33/50`
- known reasons: `{'required_topic_missing': 6, 'passed': 10}`
- fresh reasons: `{'expected_terms_missing': 5, 'passed': 4, 'response_family_mismatch': 1}`

## القرار

Best checkpoint sf-10m-step1800 scored known=10/16, fresh_topic=4/10, all_family=33/50. Runtime remains blocked; a separate held-out gate is required if all gates pass.

محظور من هذه المرحلة: runtime release, UI generator release, SF-50M, tokenizer retrain, pretrained/open-weight usage.
