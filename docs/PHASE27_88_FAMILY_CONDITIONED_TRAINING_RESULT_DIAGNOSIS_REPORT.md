# Phase 27.88 — Family-conditioned Training Result Diagnosis

## الخلاصة

هذه مرحلة تشخيص فقط. لا تدريب ولا runtime.

- status: `PHASE27_88_DIAGNOSED_SEQUENTIAL_CURRICULUM_COLLAPSE_NO_TRAINING`
- decision: `DESIGN_STRATIFIED_ROUND_ROBIN_CURRICULUM_BEFORE_ANY_TRAINING`
- training allowed: `False`
- runtime release: `False`
- sampler implementation allowed: `True`
- next: `Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate`

## الدليل

- first 1800 family counts: `{'متابعة': 451, 'سوالف': 444, 'تنظيم': 452, 'دعم': 448, 'موضوع': 5}`

### Checkpoint Windows

- `sf-10m-step600` range `[1, 600]` dominant `متابعة` share `0.7517` counts `{'متابعة': 451, 'سوالف': 149}`
- `sf-10m-step1200` range `[601, 1200]` dominant `تنظيم` share `0.5083` counts `{'سوالف': 295, 'تنظيم': 305}`
- `sf-10m-step1800` range `[1201, 1800]` dominant `دعم` share `0.7467` counts `{'تنظيم': 147, 'دعم': 448, 'موضوع': 5}`

### Alignment

- `sf-10m-step600` train dominant `followup` → pass dominant `open_social` aligned `False`
- `sf-10m-step1200` train dominant `planning` → pass dominant `planning` aligned `True`
- `sf-10m-step1800` train dominant `support` → pass dominant `support` aligned `True`

## Root Cause Weights

- `sequential_curriculum_ordering`: `38%`
- `checkpoint_recency_bias`: `22%`
- `topic_underexposure_before_step1800`: `16%`
- `family_condition_signal_not_interleaved`: `12%`
- `decoding`: `4%`
- `model_capacity`: `4%`
- `tokenizer`: `2%`
- `semantic_routing`: `2%`

## القرار

ترتيب stream التدريب متسلسل حسب عائلة الحوار: عائلة الموضوع تظهر 5 مرات فقط في أول 1800 عينة، والـ checkpoints اللاحقة تتبع آخر كتلة عائلية رآها النموذج. هذا خلل curriculum/sampling وليس مبررًا للقفز في الحجم.

لا نكبر إلى SF-50M ولا نعيد التدريب قبل بناء sampler متوازن و dry-run gate.
