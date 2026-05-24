# Phase 27.84 — Objective/Curriculum Failure Diagnosis

## الخلاصة

هذه مرحلة تشخيص فقط. لم يبدأ تدريب جديد ولم يتغير runtime.

- status: `PHASE27_84_DIAGNOSED_OBJECTIVE_CURRICULUM_FAILURE_NO_TRAINING`
- decision: `DESIGN_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_BEFORE_ANY_TRAINING`
- best checkpoint: `sf-10m-step1200`
- best fresh shadow: `11/60`
- runtime release: `False`
- next: `Phase 27.85 — Explicit Family Conditioning Objective Design`

## السبب الجذري

التوازن كان موجودًا في metadata، لكن عائلة الحوار لم تكن ظاهرة داخل نص التدريب.
النموذج رأى `النطاق: سعودي/فصحى` فقط، ولم يرَ إشارة مثل `العائلة: planning`.

## Root Cause Weights

- `objective_family_signal_missing`: `30%`
- `curriculum_sampling_not_family_conditioned_in_text`: `24%`
- `weak_generalization_after_bounded_repair`: `17%`
- `decoding_and_repetition_fragility`: `10%`
- `tokenizer_boundary_residual`: `7%`
- `semantic_routing`: `4%`
- `data_quality`: `4%`
- `model_capacity`: `4%`

## Evidence

- pack balanced: `True`
- family signal missing: `True`
- collapse after balanced data: `True`
- loss/quality mismatch: `True`
- malformed/repetitive count: `19`

## Blocked

- new LM training
- runtime release
- UI generator release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage

## Allowed Next Actions

- design explicit family conditioning line/token
- design stratified/interleaved family curriculum sampler
- define held-out canary thresholds for each family
- define decoding-only regression checks
