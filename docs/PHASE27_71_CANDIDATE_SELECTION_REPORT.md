# Phase 27.71 — Candidate Selection and Stability Strategy

## الخلاصة

هذه مرحلة تقييم فقط. لا تدريب جديد ولا فتح runtime.

- status: `NO_STABLE_CANDIDATE_RUNTIME_BLOCKED`
- tokenizer: `artifacts/tokenizers/sf_bpe/v8_phase27_65`
- selected candidate: `phase27_68_shadow_failure_repair`
- runtime switch allowed: `False`
- next phase: `Phase 27.72 — stability-first curriculum/selection repair`

## نتائج المرشحين

### phase27_66_v8_bounded_topic_repair

- checkpoint: `artifacts/eval/phase27_66_v8_bounded_topic_repair/checkpoints/sf-10m-step6200`
- score: `104/140`
- Phase 27.69 fresh: `43/60`
- Phase 27.67 known: `31/50`
- Phase 27.60 regression: `30/30`

### phase27_68_shadow_failure_repair

- checkpoint: `artifacts/eval/phase27_68_shadow_failure_repair/checkpoints/sf-10m-step5600`
- score: `136/140`
- Phase 27.69 fresh: `56/60`
- Phase 27.67 known: `50/50`
- Phase 27.60 regression: `30/30`

### phase27_70_open_social_repair

- checkpoint: `artifacts/eval/phase27_70_open_social_repair/checkpoints/sf-10m-step240`
- score: `133/140`
- Phase 27.69 fresh: `55/60`
- Phase 27.67 known: `48/50`
- Phase 27.60 regression: `30/30`

## القرار

No candidate passed all three stability gates. Keep runtime blocked and move to a stability-first repair strategy instead of exposing the model.
