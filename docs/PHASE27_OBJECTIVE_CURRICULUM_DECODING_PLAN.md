# PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN

## القرار

- المرحلة: `Phase 27.79 — Objective/Curriculum/Decoding Repair Plan`
- المسار: `SF-native Objective/Curriculum/Decoding Acceleration Track`
- القاموس: `Saudi Seed v1`
- تدريب جديد: `false`
- tokenizer جديد: `false`
- SF-50M: `false`
- runtime release: `false`

## المشكلة الجذرية الحالية

Phase 27.104 fixed topic binding on the narrow prototype gate, but all-family quality regressed to 30/50. The model can follow the narrow topic objective, yet still loses stable dialogue-family behavior.

| العامل | هل هو مشكلة؟ | الوزن | الدليل |
|---|---:|---:|---|
| `objective` | `True` | `24%` | Previous objectives over-focus on topic copy/binding and do not teach family selection as a first-class behavior. |
| `family_mixing` | `True` | `22%` | All-family gate failed despite topic gates passing; family stability is not preserved. |
| `curriculum_order` | `True` | `18%` | Narrow scheduled views can improve one family while degrading broader dialogue behavior. |
| `decoding` | `True` | `14%` | Checkpoint judgment must use guarded decoding consistently before runtime decisions. |
| `semantic_routing` | `True` | `10%` | Fallback/general routing can hide family ambiguity and must be inspected in canaries. |
| `capacity` | `False` | `1%` | No evidence justifies SF-50M; errors track objective/curriculum/family behavior, not raw size. |
| `other` | `True` | `11%` | EOS, repetition, held-out separation, and runtime masking remain gate concerns. |

## Objective

- الاسم: `family_conditioned_assistant_only_objective_v2`
- loss: `assistant_text_and_eos_only`
- الصيغة:

```text
النطاق: سعودي
عائلة الحوار: تنظيم
المستخدم: كيف أنظم يومي؟
المساعد: اكتب ثلاث مهام، وابدأ بالأهم لمدة قصيرة. <eos>
```

القواعد:
- Treat dialogue family as explicit conditioning text.
- Train answer boundaries with mandatory <eos>.
- Keep user/context visible as input while masking them out of target loss.
- Reject project/operator dialogue contamination.

## Curriculum

- No long contiguous blocks from a single family.
- Every training window must cover all five required families.
- MSA/Saudi balance must stay close to 50/50.
- Held-out canaries must never enter training.
- Topic repair data must not drown open_social/followup/planning/support.

## Decoding Policy

- stop_at_eos
- no_repeat_ngram
- repetition_penalty
- known_fragment_blocklist
- topic_substitution_guard
- family_drift_guard
- template_masking_forbidden
- blocked rule: If guarded generation fails, return blocked metadata, not a fixed template.

## Contrastive Evaluation

- known_canary
- fresh_heldout_canary
- family_confusion_matrix
- topic_binding_canary
- open_social_canary
- followup_canary
- clean_stop_canary
- runtime_dry_run

## Checkpoint Selector

- held_out_dialogue_quality
- family_stability
- semantic_correctness
- clean_stop
- open_social_naturalness
- followup_continuity
- runtime_usability

## AMP/MPS

- `check_mps_support`: `True`
- `amp_allowed_after_smoke_test_only`: `True`
- `disable_amp_if_unstable`: `True`
- `purpose`: `reduce heat and speed training without changing behavioral goals`

## Logging

- train_loss
- eval_loss
- perplexity
- family_accuracy
- clean_stop_rate
- topic_binding_pass_rate
- canary_pass_rate
- blocked_reasons
- checkpoint_selected_or_rejected_reason

## Training Gate

- objective_renderer_ready
- assistant_only_loss_mask_verified
- round_robin_sampler_ready
- decoding_policy_ready
- contrastive_eval_ready
- checkpoint_selector_ready
- heldout_canary_ready
- corpus_audit_passed
- sensitive_scan_passed
- all_tests_passed
- mps_amp_smoke_logged

## Stop Criteria

- family_balance_gate_failed
- heldout_leakage_detected
- operator_contamination_detected
- semantic_routing_regression
- clean_stop_regression
- topic_substitution_regression
- amp_instability_detected

## Deferred Tools

- LoRA/QLoRA مؤجلة ومسموحة فقط على نماذج SF-native.
- DPO/ORPO/SimPO مؤجلة حتى توجد preference pairs محلية وسيادية.

## Next

- بوابات التنفيذ مرّت لاحقًا في Phase 27.80.
- التالي عند نجاح البوابات: `Phase 27.81 — Execute bounded SF-10M family-conditioned repair training`
- لا تفتح الواجهة إلا عند `RUNTIME_RELEASE_ALLOWED=true`.
