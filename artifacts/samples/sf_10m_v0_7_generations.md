# SF-10M v0.7 Generation Samples

Decision: `runtime_blocked`

`SF-10M v0.7` improved held-out eval loss, but generation quality still fails.

```text
eval loss = 4.7512
perplexity = 115.72
generation_quality = 0/10
```

Examples observed before strict blocking:

- `قل: أشكره على الدعوة، ياذكر السبب باختصار...`
- `ابدأ بهالفكرة: اذكر السبب باختصار. له زعج...`
- `إذا ما له موعد عج... خياهر...`

Blocked fragments include:

```text
الدعج
صعج
حياذكر
بععجه
الموقت
تزعريف
```
