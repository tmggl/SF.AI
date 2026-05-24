# Phase 27.86 — Family Conditioning Renderer Gate

## الخلاصة

هذه مرحلة gate فقط. لم يبدأ تدريب ولم يتغير runtime.

- status: `PHASE27_86_RENDERER_GATE_PASSED_TRAINING_ALLOWED_NEXT_NO_RUNTIME`
- gate passed: `True`
- decision: `ALLOW_PHASE27_87_BOUNDED_FAMILY_CONDITIONED_SF10M_REPAIR_TRAINING`
- training allowed for next phase: `True`
- runtime release allowed: `False`
- next: `Phase 27.87 — Bounded Family-conditioned SF-10M Repair Training`

## Family Lines

- `open_social` → `عائلة الحوار: سوالف`
- `followup` → `عائلة الحوار: متابعة`
- `planning` → `عائلة الحوار: تنظيم`
- `support` → `عائلة الحوار: دعم`
- `topic` → `عائلة الحوار: موضوع`

## Masking

- conditioning lines masked: `True`
- user line masked: `True`
- assistant content supervised: `True`

## القرار

الرندر الآن يضيف سطر عائلة الحوار العربي في مساري التدريب، وassistant-only loss يخفي سطور السياق عن الهدف.

لا يوجد runtime release من هذه المرحلة؛ المسموح فقط تدريب مقيّد في Phase 27.87.
