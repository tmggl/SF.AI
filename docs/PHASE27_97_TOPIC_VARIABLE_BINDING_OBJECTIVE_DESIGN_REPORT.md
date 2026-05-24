# Phase 27.97 — Topic Variable Binding Objective Design

## الخلاصة

هذه مرحلة تصميم فقط. لا تدريب ولا runtime.

- status: `PHASE27_97_TOPIC_BINDING_OBJECTIVE_DESIGN_READY_NO_TRAINING`
- decision: `ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING`
- gate encoding allowed: `True`
- training allowed: `False`
- runtime release: `False`
- next: `Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit`

## Objective

- name: `topic_copy_contrastive_binding_objective_v1`
- target family: `topic`
- target terms: `['الوفاء', 'التعاون', 'الصبر', 'الاحترام', 'الهدوء', 'الصدق', 'الصداقة', 'الشجاعة']`

## Assistant Target Contract

- copy anchor: The assistant answer must copy the exact requested topic term inside the first 12 visible Arabic characters after the assistant role marker.
- single topic rule: For one-sentence topic answers, no other protected topic term may appear unless the requested topic also appears first.
- short answer rule: One compact sentence, 8-18 Arabic words, then EOS.

## Prefix Templates

- `معنى <topic_term>: <short explanation>`
- `<topic_term> يعني <short explanation>`
- `<topic_term> هو <short explanation>`

## Canary Design

- `known_topic_min`: `16/16`
- `fresh_topic_min`: `8/10`
- `contrastive_wrong_topic_max`: `0`
- `copy_anchor_min`: `26/26`
- `all_family_regression_min`: `45/50`
- `topic_family_min`: `8/10`
- `malformed_max`: `0`
- `repeated_phrase_max`: `0`

## Phase 27.98 Required Gates

- topic metadata audit proves explicit topic_term for every topic sample
- renderer can emit copy-anchor targets without unmasking condition lines
- contrastive canary covers all topic terms and wrong-topic substitutions
- sampler dry-run proves per-topic round-robin exposure
- no training is started in the gate-encoding phase

## Blocked

- LM training before Phase 27.98 gates
- runtime release
- UI generator release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage
- keyword/template masking
