# Phase 27.100 — Bounded Topic Binding Repair Training

## الخلاصة

هذه مرحلة تدريب محدودة على SF-10M فقط. لا تفتح runtime أو الواجهة.

- status: `PHASE27_100_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_BINDING_REPAIR_RESULT`
- best checkpoint: `sf-10m-step1800`
- known topic: `13/16`
- fresh topic: `5/10`
- copy anchor: `18/26`
- wrong topic count: `0`
- topic family: `6/10`
- all family: `37/50`
- held-out gate allowed: `False`
- runtime release: `False`
- next: `Phase 27.101 — Topic Binding Repair Result Diagnosis`

## Checkpoints

### sf-10m-step600

- known topic: `2/16`
- fresh topic: `1/10`
- copy anchor: `3/26`
- all family: `19/50`
- known reasons: `{'required_topic_missing': 14, 'passed': 2}`
- fresh reasons: `{'required_topic_missing': 9, 'passed': 1}`

### sf-10m-step1200

- known topic: `8/16`
- fresh topic: `4/10`
- copy anchor: `12/26`
- all family: `34/50`
- known reasons: `{'required_topic_missing': 8, 'passed': 8}`
- fresh reasons: `{'required_topic_missing': 6, 'passed': 4}`

### sf-10m-step1800

- known topic: `13/16`
- fresh topic: `5/10`
- copy anchor: `18/26`
- all family: `37/50`
- known reasons: `{'required_topic_missing': 3, 'passed': 13}`
- fresh reasons: `{'required_topic_missing': 5, 'passed': 5}`

## القرار

Best checkpoint sf-10m-step1800 scored known=13/16, fresh_topic=5/10, copy_anchor=18/26, wrong_topic=0, topic_family=6/10, all_family=37/50. Runtime remains blocked; a separate held-out gate is required if all gates pass.

محظور من هذه المرحلة: runtime release, UI generator release, SF-50M, tokenizer retrain, pretrained/open-weight usage.
