# Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit

## الخلاصة

هذه مرحلة بوابة فقط. لا تدريب ولا runtime.

- status: `PHASE27_98_TOPIC_BINDING_GATE_PASSED_TRAINING_ALLOWED_NEXT`
- decision: `ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING`
- encoded gate passed: `True`
- metadata ready: `True`
- copy-anchor ready: `True`
- sampler ready: `True`
- training allowed: `True`
- next: `Phase 27.100 — Bounded Topic Binding Repair Training`

## ما ثبت

- renderer يستطيع إنتاج target يبدأ بالموضوع المطلوب.
- assistant-only loss يبقي سطور السياق والطلب masked.
- canary contrastive جديد يغطي 26 حالة: 16 known و10 fresh.

## سبب منع التدريب

- total topic records: `510`
- explicit topic_term records: `510`
- missing topic_term records: `0`
- copy-anchor unknown topic: `0`
- copy-anchor bad: `0`

## القرار

Gate encoding, metadata, copy-anchor, and sampler readiness all passed.

## الملفات الأكثر احتياجًا لإصلاح metadata
