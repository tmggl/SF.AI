# SF-10M v0.4 Dialogue-Format Samples

**Journey:** Phase 27.5 / 30
**Language track:** `msa + saudi` only
**Lexicon track:** `Saudi Seed v1`
**Checkpoint:** `artifacts/checkpoints/sf_10m_v0_4/sf-10m-step4000`
**Verdict:** `runtime_blocked`

## Setup

```text
stream_format : dialogue
chat_prompt   : true
seq_len       : 64
max_tokens    : 48
eval_batches  : 20
loss          : 5.8267
perplexity    : 339.24
```

## Samples

### Prompt

```text
كيفك
```

### Output

```text
لا، الاعتذار الطرف الآخر.
```

### Prompt

```text
السلام عليكم
```

### Output

```text
لا، الجواب العملي: ابدأ بتحية بسيطًا.
```

### Prompt

```text
اشرح لي الماء
```

### Output

```text
لا، الاعتذار الطرف الآخر.
```

## Decision

النموذج تعلّم صيغة الأدوار أفضل من التدريب المسطح، لكنه لا يجيب إجابات مرتبطة
بالسؤال. لا يُفعّل في الواجهة، ولا يصلح كدليل على جاهزية `SF-50M`.
