# Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate

## الخلاصة

هذه مرحلة بوابة فقط: لا تدريب، لا runtime، لا تغيير في الواجهة.

- status: `PHASE27_89_STRATIFIED_ROUND_ROBIN_SAMPLER_GATE_PASSED_TRAINING_ALLOWED_NEXT`
- decision: `ALLOW_PHASE27_90_BOUNDED_SF10M_TRAINING_WITH_ROUND_ROBIN_SPLIT_ORDER`
- training allowed next: `True`
- runtime release: `False`
- required training flag: `--split-order family_round_robin`
- next: `Phase 27.90 — Bounded SF-10M Round-Robin Curriculum Repair Training`

## المقارنة

- sequential first 1800: `{'followup': 451, 'open_social': 444, 'planning': 452, 'support': 448, 'topic': 5}`
- round-robin first 1800: `{'open_social': 360, 'followup': 360, 'planning': 360, 'support': 360, 'topic': 360}`

## نوافذ family_round_robin

- `window_1` range `[1, 600]` counts `{'سوالف': 120, 'متابعة': 120, 'تنظيم': 120, 'دعم': 120, 'موضوع': 120}` dominant `open_social` share `0.2`
- `window_2` range `[601, 1200]` counts `{'سوالف': 120, 'متابعة': 120, 'تنظيم': 120, 'دعم': 120, 'موضوع': 120}` dominant `open_social` share `0.2`
- `window_3` range `[1201, 1800]` counts `{'سوالف': 120, 'متابعة': 120, 'تنظيم': 120, 'دعم': 120, 'موضوع': 120}` dominant `open_social` share `0.2`

## القرار

الترتيب الجديد يوزع عائلات الحوار داخل كل نافذة تدريبية بدل الكتل المتتابعة، لذلك يسمح فقط بتدريب SF-10M محدود في المرحلة التالية، مع استمرار حجب runtime.

## المحظور

- runtime release
- UI generator release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage

## المسموح لاحقًا

- one bounded SF-10M repair using --split-order family_round_robin
- save-window family-balance tracking
- held-out canary after training
