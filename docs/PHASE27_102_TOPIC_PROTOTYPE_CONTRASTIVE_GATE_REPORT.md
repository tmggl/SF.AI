# Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate

## الخلاصة

هذه بوابة ترميز/تصميم فقط. لا تدريب ولا runtime.

- status: `PHASE27_102_GATE_ENCODED_CURRICULUM_PACK_ALLOWED_NO_TRAINING`
- decision: `ALLOW_PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_NO_TRAINING`
- reported wrong-topic: `0`
- observed wrong-topic: `8`
- copy-anchor: `18/26`
- canary prompts: `16`
- runtime release: `False`
- training allowed: `False`
- next: `Phase 27.103 — Topic Prototype Contrastive Curriculum Pack`

## القرار

The executable gate now catches the Phase 27.100 metric blind spot: reported wrong-topic was 0, but observed wrong-topic is 8. Future topic repair must pass observed wrong-topic=0 and copy-anchor gates before any runtime or scaling decision.

## البوابة الجديدة

- counted metric: `observed_wrong_topic_count` من نص الرد مباشرة.
- threshold: `observed_wrong_topic_count == 0`.
- copy-anchor: الموضوع المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا.
- لا يسمح `required_topic_missing` بإخفاء wrong-topic substitution.

## بدائل الموضوع المرصودة في 27.100

- `الصداقة`: `7`
- `الامتنان`: `1`

## المحظور

- new LM training
- runtime release
- UI generator release
- SF-50M transition
- tokenizer retrain
- pretrained/open-weight usage
- template masking

## المسموح تاليًا

- author a no-training topic prototype contrastive curriculum pack
- add rows that force requested-topic copy-anchor before prototype terms
- rerun gate before bounded training is allowed
