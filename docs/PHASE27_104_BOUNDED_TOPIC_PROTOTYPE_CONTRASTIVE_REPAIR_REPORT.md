# Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training

## الخلاصة

هذه مرحلة تدريب محدودة على SF-10M فقط. لا تفتح runtime أو الواجهة.

- status: `PHASE27_104_TRAINED_RUNTIME_BLOCKED_DIAGNOSIS_REQUIRED`
- decision: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_PROTOTYPE_REPAIR_RESULT`
- best checkpoint: `sf-10m-step1200`
- prototype canary: `16/16`
- prototype observed wrong-topic: `0`
- known topic: `16/16`
- fresh topic: `9/10`
- topic family: `9/10`
- all family: `30/50`
- held-out gate allowed: `False`
- runtime release: `False`
- next: `Phase 27.105 — Topic Prototype Repair Result Diagnosis`

## Training View

- source pack: `data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl`
- view file: `artifacts/eval/phase27_104_topic_prototype_contrastive_repair/curriculum_view/jsonl/phase27_103_schedule_view.jsonl`
- records: `192`
- adjacent same topic: `0`

## Checkpoints

### sf-10m-step400

- prototype: `14/16`
- prototype wrong-topic: `1`
- known topic: `16/16`
- fresh topic: `8/10`
- all family: `32/50`
- prototype reasons: `{'required_topic_missing': 1, 'passed': 14, 'guard:repeated_phrase': 1}`

### sf-10m-step800

- prototype: `14/16`
- prototype wrong-topic: `0`
- known topic: `14/16`
- fresh topic: `8/10`
- all family: `27/50`
- prototype reasons: `{'passed': 14, 'guard:malformed_token': 1, 'guard:repeated_phrase': 1}`

### sf-10m-step1200

- prototype: `16/16`
- prototype wrong-topic: `0`
- known topic: `16/16`
- fresh topic: `9/10`
- all family: `30/50`
- prototype reasons: `{'passed': 16}`

## القرار

Best checkpoint sf-10m-step1200 scored prototype=16/16 with observed_wrong_topic=0, known=16/16, fresh=9/10, topic_family=9/10, all_family=30/50. Runtime remains blocked.
