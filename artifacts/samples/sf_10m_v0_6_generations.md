# SF-10M v0.6 Generation Samples

Checkpoint: `artifacts/checkpoints/sf_10m_v0_6/sf-10m-step4000`

Decision: `runtime_blocked`

The model improved numerically on the held-out eval split, but generated text
still contains malformed fragments. Canary blocks runtime use.

| Prompt | Canary | Reason | Sample |
|---|---|---|---|
| السلام عليكم | blocked | model_artifact_fragment | الأفضل تبدأ بهدوء: اطلب مها الطرورين بس... |
| كيفك | blocked | model_artifact_fragment | لا، الاعتذر وك، ورًا حاولت الطرورين... |
| وشلونك | blocked | model_artifact_fragment | لا، الزبدة: اطلب الطروري أخر عن التأخيارين... |
| شكرا | blocked | model_artifact_fragment | لا، الزبدة: اطلب الطروسبب حارين بس... |
| سعودي | blocked | model_artifact_fragment | لا، الزبدة: اشكر الطروسبب حارين... |
| أريد جوابا قصيرا | blocked | model_artifact_fragment | الأفضل تبدأ بهدوء: اذكر الطروسبب حارين... |
| اشرح لي الصبر بجملة واحدة | blocked | model_artifact_fragment | ابدأ بهالفكرة: اذكر الطروت الطرورين... |
| وش رايك أتعلم كل يوم شوي | blocked | model_artifact_fragment | الزبدة: اطلب الطروسبب حاية... |
| أنا متضايق اليوم | blocked | model_artifact_fragment | لا، الزبدة: اطلب رتًا لا ته... |
| قل لي نصيحة بسيطة | blocked | model_artifact_fragment | الأفضل تبدأ بهدوء: اطلب الطروسبب حارير... |

Summary: `allowed=0/10`.
