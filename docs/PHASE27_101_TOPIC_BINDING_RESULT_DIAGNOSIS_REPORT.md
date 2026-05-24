# Phase 27.101 — Topic Binding Repair Result Diagnosis

## الخلاصة

هذه مرحلة تشخيص فقط. لم يبدأ تدريب جديد ولم يتغير runtime.

- status: `PHASE27_101_DIAGNOSED_COPY_ANCHOR_CURRICULUM_GAP_NO_TRAINING`
- decision: `DESIGN_TOPIC_PROTOTYPE_CONTRASTIVE_COPY_ANCHOR_GATE_BEFORE_ANY_TRAINING`
- best checkpoint: `sf-10m-step1800`
- known topic: `13/16`
- fresh topic: `5/10`
- copy-anchor: `18/26`
- reported wrong-topic count: `0`
- observed wrong-topic count: `8`
- topic-family: `6/10`
- all-family: `37/50`
- runtime release: `False`
- training allowed: `False`
- next: `Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate`

## التشخيص

Phase 27.100 improved topic binding but did not truly eliminate wrong-topic behavior. The report counted wrong-topic as zero through reason precedence, while direct response inspection finds prototype substitutions, mostly الصداقة. The best checkpoint misses copy-anchor on 8/26 contrastive cases, fresh-topic generalization remains 5/10, and topic-family is 6/10. This is an objective/evaluation/curriculum binding weakness, not evidence for SF-50M yet.

## إشارات التشخيص

- `known_gate_failed`: `True`
- `fresh_gate_failed`: `True`
- `copy_anchor_gate_failed`: `True`
- `wrong_topic_metric_blind_spot`: `True`
- `reported_wrong_topic_count`: `0`
- `observed_wrong_topic_count`: `8`
- `topic_prototype_attraction`: `True`
- `fresh_generalization_gap`: `True`
- `topic_family_gap`: `True`
- `all_family_gate_failed`: `True`
- `support_surface_gap`: `True`
- `open_social_surface_gap`: `True`
- `guard_blocked_topic_failures`: `0`

## أوزان السبب الجذري

- `copy_anchor_objective_underpowered`: `28%`
- `topic_prototype_attraction`: `20%`
- `fresh_topic_generalization_gap`: `16%`
- `topic_curriculum_term_balance`: `12%`
- `assistant_target_prefix_format_weak`: `9%`
- `decoding_surface_artifacts`: `6%`
- `support_open_social_secondary_regression`: `4%`
- `tokenizer`: `2%`
- `model_capacity`: `2%`
- `semantic_routing`: `1%`

## إخفاقات الموضوع

- `by_required_topic`: `{'الوفاء': 4, 'الاحترام': 2, 'التعاون': 1, 'الشجاعة': 1}`
- `response_topic_hits`: `{'الصداقة': 7, 'الامتنان': 1}`
- `wrong_topic_substitutions`: `{'الصداقة': 7, 'الامتنان': 1}`
- `by_reason`: `{'required_topic_missing': 8}`
- `by_section`: `{'known_topic_rows': 3, 'fresh_topic_rows': 5}`
- `by_dialect`: `{'msa': 3, 'saudi': 5}`

## القرار

- ممنوع: new LM training
- ممنوع: runtime release
- ممنوع: UI generator release
- ممنوع: SF-50M transition
- ممنوع: tokenizer retrain
- ممنوع: pretrained/open-weight usage
- ممنوع: keyword/template masking

## المسموح تاليًا

- design topic-prototype contrastive copy-anchor gate
- fix wrong-topic metric precedence before any training
- require per-topic forced copy-anchor rows before training
- separate known/fresh topic curriculum thresholds
- preserve observed wrong-topic zero-leak as a non-regression gate
- add support/open_social secondary regression checks
