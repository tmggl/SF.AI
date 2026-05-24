# Phase 27.103 — Topic Prototype Contrastive Curriculum Pack

## الخلاصة

هذه مرحلة حزمة بيانات فقط: لا تدريب، لا runtime، لا tokenizer.

- status: `PHASE27_103_TOPIC_PROTOTYPE_CURRICULUM_PACK_READY_FOR_BOUNDED_TRAINING`
- decision: `ALLOW_PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_TRAINING`
- authored file: `data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl`
- records authored: `192`
- records per topic: `{'الوفاء': 24, 'التعاون': 24, 'الصبر': 24, 'الاحترام': 24, 'الهدوء': 24, 'الصدق': 24, 'الصداقة': 24, 'الشجاعة': 24}`
- records per dialect: `{'msa': 96, 'saudi': 96}`
- copy-anchor bad count: `0`
- wrong-topic leak count: `0`
- duplicate pair count: `0`
- training started: `False`
- phase27_104 training allowed: `True`
- runtime release: `False`
- next: `Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training`

## لماذا هذه الحزمة؟

Phase 27.102 أثبتت أن wrong-topic يجب أن يُحسب من نص الرد نفسه. هذه الحزمة تجعل رد المساعد يبدأ بالموضوع المطلوب، وتمنع تسرب موضوع آخر داخل رد المساعد.

## القرار

The pack is balanced across 8 topics and 2 dialects, every assistant answer copy-anchors the requested topic first, and no assistant answer leaks a different topic/prototype term. One bounded SF-10M repair may be planned next; runtime remains blocked.

## المحظور

- runtime release
- UI generator release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage
- template masking

## المسموح تاليًا

- one bounded SF-10M topic-prototype contrastive repair training
- must evaluate Phase 27.102 canary before any runtime decision
- must keep observed wrong-topic at 0 and copy-anchor at 16/16
