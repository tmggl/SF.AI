# Phase 27.81 — Balanced Family Pack

هذه مرحلة تأليف بيانات فقط، بلا تدريب.

- total records: `2500`
- open_social/followup/planning/support/topic: `500` لكل عائلة
- dialect per family: `250 msa + 250 saudi`
- training allowed by this phase: `false`

## Generated Files

- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_open_social_msa_010.jsonl`: 250 msa open_social
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_open_social_saudi_010.jsonl`: 250 saudi open_social
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_followup_msa_010.jsonl`: 250 msa followup
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_followup_saudi_010.jsonl`: 250 saudi followup
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_planning_msa_010.jsonl`: 250 msa planning
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_planning_saudi_010.jsonl`: 250 saudi planning
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_support_msa_010.jsonl`: 250 msa support
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_support_saudi_010.jsonl`: 250 saudi support
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_msa_010.jsonl`: 250 msa topic
- `data/corpus/chat/jsonl/dialogue_batch_v10_balanced_topic_saudi_010.jsonl`: 250 saudi topic

## Next

Run corpus audit, rebuild dialogue split, and rerun Phase 27.80 repair gates.
