# Phase 27.79 — Objective/Curriculum/Decoding Repair Design

## الخلاصة

هذه مرحلة تصميم هندسي فقط. لم يبدأ تدريب جديد، ولم يتغير runtime،
ولم يُفتح `SF-50M`.

- status: `PHASE27_79_REPAIR_DESIGN_READY_NEXT_GATE_ENCODING_NO_TRAINING`
- decision id: `PHASE27_79_REPAIR_DESIGN_DECISION`
- source decision: `PHASE27_78_ENGINEERING_DECISION`
- language track: `msa, saudi`
- lexicon: `Saudi Seed v1`
- next phase: `Phase 27.80 — Repair Gate Encoding and Dry-Run Validation`

## القرار

- continue SF-10M: `True`
- new training allowed: `False`
- tokenizer retrain allowed: `False`
- runtime release allowed: `False`
- SF-50M justified transition: `False`

## Objective Design

- name: `family_conditioned_prompt_to_answer_objective_v1`
- loss scope: `assistant_answer_only_with_eos`

- single_answer_boundary
- explicit_family_condition
- explicit_dialect_condition
- topic_or_none_condition
- assistant_eos_required
- no_cross_sample_packing

## Curriculum Design

- لا دفعات كتلية من family واحدة.
- كل نافذة تدريب صغيرة يجب أن تحتوي open_social/followup/planning/support/topic.
- كل عائلة يجب أن تحتوي صيغًا مباشرة وغير مباشرة.
- held-out prompts لا تدخل التدريب.

## Decoding Design

- stop_at_eos
- max_answer_tokens_by_family
- no_repeat_ngram
- repetition_penalty
- family_allowed_terms_floor
- family_blocked_terms_soft_guard
- malformed_fragment_guard

## Phase 27.80 Gate Encoding Plan

- objective spec validator
- curriculum family-balance dry-run
- decoding policy config validator
- held-out/shadow canary manifest validator
- family confusion matrix builder
- operator-contamination regression scan

## Blocked Actions

- new LM training
- tokenizer retraining
- SF-50M full training
- runtime release
- template masking
- external/pretrained data or weights

## Regression Summary

- Phase 27.78 أثبتت أن capacity ليست السبب الأكبر.
- Phase 27.79 لا تحاول تحسين benchmark؛ هي تصمم الإصلاح قبل التنفيذ.
- أي تدريب لاحق يحتاج Phase 27.80 gates مكتوبة وناجحة.
