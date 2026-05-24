# Phase 27.92 — Topic Objective Repair Design Gate

## الخلاصة

هذه مرحلة تصميم فقط. لا تدريب ولا runtime.

- status: `PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_READY_NO_TRAINING`
- decision: `ALLOW_PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_NO_TRAINING`
- topic gate encoding allowed: `True`
- training allowed: `False`
- runtime release: `False`
- next: `Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation`

## التصميم

- objective: `topic_anchor_prompt_to_answer_objective_v1`
- target family: `topic`
- target terms: `['الوفاء', 'التعاون', 'الصبر', 'الاحترام', 'الهدوء', 'الصدق', 'الصداقة', 'الشجاعة']`

### Conditioning Lines

- `النطاق: <فصحى|سعودي>`
- `عائلة الحوار: موضوع`
- `الموضوع المطلوب: <topic_term>`

### Answer Contract

- one short explanatory sentence
- include the requested topic term
- do not substitute another known topic term
- avoid malformed fragments
- avoid repeated words/phrases
- no project/operator language

### Canary Design

- `known_topic_canary_min`: `18/20`
- `fresh_topic_shadow_min`: `16/20`
- `all_family_regression_min`: `45/50`
- `topic_family_min`: `8/10`
- `malformed_max`: `0`
- `repeated_phrase_max`: `0`

## القرار

The next fix should target topic anchoring and anti-collapse objective design. Capacity remains a minor factor, so SF-50M is still blocked.

## محظور الآن

- training before Phase 27.93 gate encoding
- runtime release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage
