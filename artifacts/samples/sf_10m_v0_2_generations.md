# SF-10M v0.2 Generations

Phase 24 generation samples from `sf-10m-step2000`.

## Command

```bash
make eval-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v2 --corpus data/corpus/chat/jsonl --checkpoints artifacts/checkpoints/sf_10m_v0_2 --checkpoint-name sf-10m-step2000 --size sf-10m --seq-len 64 --batch-size 4 --max-batches 20 --prompt وش --max-new-tokens 80 --device auto"
```

## Metrics

```text
batches=20
loss=2.5779
perplexity=13.17
```

## Samples

### Greedy prompt: وش

```text
وش تقول لي إذا كان corpus 30/500، وفها وفها و؟ نعم، إذا كان تدريب جودة مولد ولا تدريب جودة مولد ولا تدريب جودة جودة تها في Phase 22 بعد اكتمال السعودي ما الذي يجعل الواجهة ليست 0، وش تسوي بعد اكتمال
```

### Sample prompt: مرحبا

```text
مرحبا corpus مقنعًا. ًا. ما الخطوة التالية النموذج لا يبحتى عن ي في هي السعودي لا بعندما متكرتمتة؟ لا، والمقبولمدرمنحوالواجهة ولا القيمة حوارات سعودية يزيد عدد corpus، هي كلمات تختار وشلون ترد إذا
```

### Sample prompt: اشرح

```text
اشرح ه ولما الفرق بين الردود النموذج في ثلاث thأخخرًا. بدل Phase 22؟ يعني هي داخل نموذج سجل corpus إلى يعني ما الفرق بين تدريب tokenizer v2 على الدرب؟ أذكر والأوضة؟ لا. الواجهة يجب أن الواجهة ن و
```

## Notes

- This checkpoint is sovereign and trained from random initialization.
- It is clearly better than the Phase 14 `المعنى/وأين` loop.
- It is still not a convincing chat model.
- It must not replace the stable ChatModule.
- Phase 25 may test it only as a canary behind repetition and incoherence fallback.
