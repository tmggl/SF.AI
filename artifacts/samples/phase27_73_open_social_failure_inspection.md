# Phase 27.73 Open-Social Failure Inspection

## open_social_09

- dialect: `saudi`
- prompt: ودي بموضوع سوالف
- response: خلنا نبدأ بمها ببساطة: نوضح الفكرة خطوة بعدها.
- previous reason: `expected_terms_missing`
- guard before: `{'allowed': True, 'reason': 'passed'}`
- guard after: `{'allowed': False, 'reason': 'model_artifact_fragment', 'arabic_ratio': 1.0, 'repetition_ratio': 0.0}`
- diagnosis: model_artifact_fragment plus open_social family mismatch; guard gap fixed in Phase 27.73

## open_social_12

- dialect: `msa`
- prompt: لنختر موضوعًا صغيرًا
- response: التعاون مشاركة الجهد بين الناس.
- previous reason: `expected_terms_missing`
- guard before: `{'allowed': True, 'reason': 'passed'}`
- guard after: `{'allowed': True, 'reason': 'passed', 'arabic_ratio': 1.0, 'repetition_ratio': 0.0}`
- diagnosis: semantic family collapse: open_social prompt drifted into a topic definition response; needs targeted semantic-collapse repair

## Artifact Probe Results

- `model_artifact_fragment` / allowed=`False`: خلنا نبدأ بمها ببساطة: نوضح الفكرة خطوة بعدها.
- `model_artifact_fragment` / allowed=`False`: خلنا نبدأ بمالنبوضوح.
- `model_artifact_fragment` / allowed=`False`: نبدأ بمالحقيقة بوضوح.
- `model_artifact_fragment` / allowed=`False`: خلنا نبدأ بس الفة قصيرة وخفيفة.
- `model_artifact_fragment` / allowed=`False`: نختار موضوععن شيء خفيف.
- `model_artifact_fragment` / allowed=`False`: التعاون بمإنك تساعد غيرك.
