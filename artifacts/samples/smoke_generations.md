# Smoke Generations

Phase 13 smoke generation from `sf-10m-step20`.

## Command

```bash
make eval-lm ARGS="--tokenizer artifacts/tokenizers/sf_bpe/v1 --corpus data/corpus/chat/jsonl --checkpoints artifacts/checkpoints/smoke_lm --checkpoint-name sf-10m-step20 --size sf-10m --seq-len 16 --batch-size 2 --max-batches 5 --prompt وش --max-new-tokens 20 --device auto"
```

## Metrics

```text
batches=5
loss=4.4346
perplexity=84.32
```

## Generation

```text
وش                اللهجة/النطاق: اللهجة/النطاق: اللهجة/النطاق: اللهجة/النطاق: اللهجة/النطاق:
```

## Notes

- This is not a usable chat model.
- The generation is non-empty and UTF-8 valid.
- Repetition is expected from a 20-step smoke run over a tiny Saudi-only corpus.
- The checkpoint is not wired into ChatModule.
