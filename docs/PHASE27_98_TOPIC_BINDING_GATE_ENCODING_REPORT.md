# Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit

## الخلاصة

هذه مرحلة بوابة فقط. لا تدريب ولا runtime.

- status: `PHASE27_98_TOPIC_BINDING_GATE_ENCODED_DATA_REPAIR_REQUIRED_NO_TRAINING`
- decision: `ALLOW_PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_DATA_REPAIR_NO_TRAINING`
- encoded gate passed: `True`
- metadata ready: `False`
- copy-anchor ready: `False`
- sampler ready: `False`
- training allowed: `False`
- next: `Phase 27.99 — Topic Metadata and Copy-Anchor Data Repair`

## ما ثبت

- renderer يستطيع إنتاج target يبدأ بالموضوع المطلوب.
- assistant-only loss يبقي سطور السياق والطلب masked.
- canary contrastive جديد يغطي 26 حالة: 16 known و10 fresh.

## سبب منع التدريب

- total topic records: `510`
- explicit topic_term records: `10`
- missing topic_term records: `500`
- copy-anchor unknown topic: `273`
- copy-anchor bad: `12`

## القرار

Gate encoding works, but corpus metadata/copy-anchor readiness is not strict enough for the Phase 27.97 objective.

## الملفات الأكثر احتياجًا لإصلاح metadata

- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_msa_010.jsonl`: `250`
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_saudi_010.jsonl`: `250`
