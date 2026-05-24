# Phase 27.85 — Explicit Family Conditioning Objective Design

## الخلاصة

هذه مرحلة تصميم فقط. لم يبدأ تدريب ولم يتغير runtime.

- status: `PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_DESIGN_READY_NO_TRAINING`
- decision: `ALLOW_PHASE27_86_RENDERER_GATE_IMPLEMENTATION_NO_TRAINING`
- renderer implementation allowed: `True`
- training allowed: `False`
- next: `Phase 27.86 — Family Conditioning Renderer Gate`

## Conditioning Lines

- `النطاق: <msa|saudi rendered as فصحى|سعودي>`
- `عائلة الحوار: <سوالف|متابعة|تنظيم|دعم|موضوع>`

## Family Labels

- `open_social` → `سوالف`
- `followup` → `متابعة`
- `planning` → `تنظيم`
- `support` → `دعم`
- `topic` → `موضوع`

## Objective Rule

With loss_scope=assistant, both conditioning lines and user turns remain masked; only assistant content plus EOS are supervised.

## Canary Thresholds

- `per_family_min_pass`: `10`
- `overall_min_pass`: `55`
- `malformed_max`: `0`
- `repeated_phrase_max`: `0`
- `dominant_family_share_max`: `0.35`

## Blocked

- training before renderer/gate implementation
- runtime release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage
