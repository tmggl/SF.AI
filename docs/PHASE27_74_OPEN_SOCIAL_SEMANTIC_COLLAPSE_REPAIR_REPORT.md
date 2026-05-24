# Phase 27.74 — Open-Social Semantic-Collapse Repair

## الخلاصة

هذه مرحلة تدريب إصلاح ضيقة على انهيار `open_social` إلى تعريفات موضوعية. لا تفتح runtime تلقائيًا.

- status: `FAILED_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_RUNTIME_BLOCKED`
- tokenizer: `artifacts/tokenizers/sf_bpe/v8_phase27_65`
- init checkpoint: `artifacts/eval/phase27_72_stability_first_repair/checkpoints/sf-10m-step64`
- selected candidate: `gentle_48`
- checkpoint: `artifacts/eval/phase27_74_open_social_semantic_collapse_repair/gentle_48/checkpoints/sf-10m-step48`
- Phase 27.69 fresh: `56/60`
- Phase 27.67 known: `49/50`
- Phase 27.60 regression: `30/30`
- runtime switch allowed: `False`

## القرار

The targeted repair did not pass all gates. Keep runtime blocked and inspect the selected candidate failures before any UI/runtime change.

## التالي

Phase 27.75 — inspect Phase 27.74 failures and revise open_social strategy
