# SF-10M v0.1 Generations

Phase 14 generation sample from `sf-10m-step33`.

## Command

```bash
make eval-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v1 --corpus data/corpus/chat/jsonl --checkpoints artifacts/checkpoints/sf_10m_v0_1 --checkpoint-name sf-10m-step33 --size sf-10m --seq-len 16 --batch-size 2 --max-batches 5 --prompt وش --max-new-tokens 30 --device auto"
```

## Metrics

```text
batches=5
loss=4.0777
perplexity=59.01
```

## Generation

```text
وش               وأين المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى: المعنى:
```

## Notes

- This is not a usable chat model.
- The output is non-empty and UTF-8 valid.
- Repetition is expected because the current corpus is tiny and Saudi-only.
- This checkpoint must not replace ChatModule.
