# SF-10M v0.5 Assistant-Target Samples

**Journey:** Phase 27.6 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Checkpoint root:** `artifacts/checkpoints/sf_10m_v0_5`
**Verdict:** `runtime_blocked`

## Setup

```text
stream_format : dialogue
loss_scope    : assistant
chat_prompt   : true
seq_len       : 64
max_tokens    : 48
```

## Samples

### checkpoint: sf-10m-step2000

```text
prompt: كيفك
loss: 6.5718
perplexity: 714.65
output: الزبدة: اطلب رر بخياها بخيا. ، وبخيا. ، بالموقت مطر: اكتب الز: قل الزبدة: اطلب رر ب
```

### checkpoint: sf-10m-step3000

```text
prompt: كيفك
loss: 7.8835
perplexity: 2653.10
output: الزبدة: ابدأ بهالفكرة: ابدأ بخيارير وت أخياري، وء. . ل تسأخير. الصورة. . . ت الصورة. . ك، وشأ
```

### checkpoint: sf-10m-step4000

```text
prompt: السلام عليكم
loss: 7.9360
perplexity: 2796.09
output: الأفضل أن تبدأ بهدوء: اذكر الطف. ت الطت الطت الطرف أن تبدأ بهدوء: اذكر الطروء: اذكر الطروء: ا
```

## Decision

Assistant-target training improved the objective design, but the generated
answers remain repetitive and weak. Do not enable this checkpoint in runtime.
