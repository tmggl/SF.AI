# Phase 27.75 Open-Social Strategy Inspection

- selected candidate: `gentle_48`
- failure total: `5`
- protected pack active: `True`
- next: Phase 27.76 — tokenizer v9 open_social boundary probe before LM repair

## Tokenization Probes

### word_salfah

- text: سالفة
- decoded: سالفة
- piece_count: `3`
- roundtrip_ok: `True`
- tokens: `['س', 'الف', 'ة</w>']`

### word_bisalfah

- text: بسالفة
- decoded: بس الفة
- piece_count: `3`
- roundtrip_ok: `False`
- tokens: `['بس', 'الف', 'ة</w>']`

### artifact_bis_alfah

- text: بس الفة
- decoded: بس الفة
- piece_count: `3`
- roundtrip_ok: `True`
- tokens: `['بس', 'الف', 'ة</w>']`

### word_sawalif

- text: سوالف
- decoded: سوالف
- piece_count: `1`
- roundtrip_ok: `True`
- tokens: `['سوالف</w>']`

### phrase_topic_an

- text: موضوعًا عن
- decoded: موضوعًا عن
- piece_count: `4`
- roundtrip_ok: `True`
- tokens: `['م', 'وضوع', 'ًا</w>', 'عن</w>']`

### phrase_topic_an_plain

- text: موضوع عن
- decoded: موضوع عن
- piece_count: `3`
- roundtrip_ok: `True`
- tokens: `['م', 'وضوع</w>', 'عن</w>']`

### artifact_topic_glue

- text: موضوعاموضوععن
- decoded: موضوعاموضوععن
- piece_count: `5`
- roundtrip_ok: `True`
- tokens: `['م', 'وضو', 'عام', 'وضوع', 'عن</w>']`

### phrase_light_talk

- text: كلام خفيف
- decoded: كلام خفيف
- piece_count: `2`
- roundtrip_ok: `True`
- tokens: `['كلام</w>', 'خفيف</w>']`

### sentence_salfah

- text: خلنا نبدأ بسالفة قصيرة وخفيفة
- decoded: خلنا نبدأ بس الفة قصيرة وخفيفة
- piece_count: `9`
- roundtrip_ok: `False`
- tokens: `['خلنا</w>', 'نبدأ</w>', 'بس', 'الف', 'ة</w>', 'قصيرة</w>', 'و', 'خفي', 'فة</w>']`

### sentence_topic

- text: نختار موضوعًا عن شيء خفيف
- decoded: نختار موضوعًا عن شيء خفيف
- piece_count: `9`
- roundtrip_ok: `True`
- tokens: `['ن', 'خت', 'ار</w>', 'م', 'وضوع', 'ًا</w>', 'عن</w>', 'شيء</w>', 'خفيف</w>']`
