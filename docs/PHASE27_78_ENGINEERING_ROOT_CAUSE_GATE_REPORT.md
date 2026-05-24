# Phase 27.78 — Engineering Root Cause Gate

## الخلاصة

هذه المرحلة تعتمد `Sovereign Practical Acceleration Strategy v2`.
لم يبدأ تدريب جديد. لم يُدرّب tokenizer جديد. لم يُفتح runtime.

- status: `PHASE27_78_ENGINEERING_DECISION_READY_TRAINING_BLOCKED_RUNTIME_BLOCKED`
- decision id: `PHASE27_78_ENGINEERING_DECISION`
- source: `artifacts/reports/phase27_77_v9_bounded_open_social_lm_repair_report.json`
- failures analyzed: `11`
- fresh held-out: `54/60`
- known held-out: `45/50`
- regression: `30/30`

## أوزان الأسباب التقريبية

- `capacity`: `1%`
- `objective`: `18%`
- `curriculum`: `16%`
- `tokenizer`: `4%`
- `decoding`: `7%`
- `family_mixing`: `22%`
- `memorization`: `2%`
- `weak_generalization`: `14%`
- `EOS`: `4%`
- `repetition`: `2%`
- `semantic_routing`: `10%`

## القرار الهندسي

- continue SF-10M: `True`
- SF-50M justified transition: `False`
- change objective required: `True`
- reorganize dialogue families required: `True`
- curriculum change required: `True`
- tokenizer retrain allowed: `False`
- new training allowed: `False`
- runtime release allowed: `False`

## Runtime Decision

`NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS` فعّالة. لا يُفتح runtime
حتى تمر held-out quality وfamily stability وclean-stop وsemantic correctness.

## Allowed Actions

- objective tracing.
- curriculum diagnostics.
- family confusion analysis.
- decoding analysis and repetition profiling.
- EOS inspection.
- semantic routing diagnostics.
- contrastive evaluation and held-out/shadow canaries.

## Blocked Actions

- أي تدريب جديد قبل encoding gates.
- أي tokenizer version جديد قبل إثبات tokenizer كسبب أكبر.
- أي SF-50M transition الآن.
- أي template masking لإخفاء ضعف المولد.
- أي benchmark inflation لا ينعكس على runtime behavior.

## Regression Summary

- Phase 27.60 regression بقي `30/30`، وهذا يعني أن الفشل الحالي ليس انهيارًا عامًا.
- Phase 27.69 و27.67 ما زالت تفشل في family/semantic/followup/support.
- التكبير ممنوع لأن capacity ليست السبب الأكبر حسب الأدلة الحالية.
