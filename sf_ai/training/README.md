# sf_ai/training

أدوات تدريب SF.AI السيادية.

## ما يعيش هنا

| ملف | وصف |
|-----|-----|
| `device.py` | `DeviceManager(preference)` → `DeviceInfo(name, available, notes)`. priority: auto → mps → cuda → cpu |
| `accelerators.py` | `AcceleratorConfig` (mixed_precision, grad_accum, grad_checkpointing, grad_clip) |
| `schedules.py` | `linear_warmup_cosine`, `inverse_sqrt`, `constant_with_warmup` |
| `optimizers.py` | `OptimizerSpec(name='adamw')` + lazy `build_optimizer(params, spec)` |
| `checkpoints.py` | `CheckpointManager` (sovereign-aware) + `CheckpointMetadata` + `SovereigntyError` |
| `training_config.py` | `TrainingConfig` immutable (sovereign locked True) |
| `train_tiny_lm.py` | **(Phase 6)** سكربت تدريب SF Native LM |
| `evaluate_tiny_lm.py` | **(Phase 6)** سكربت تقييم |
| `train_tokenizer.py` | **(Phase 5.5)** غلاف على `train_bpe_from_corpus` |
| `train_embeddings.py` | ملاحظة: embeddings مدمجة داخل النموذج |

## سير العمل الكامل (عندما يكون عند المستخدم بيانات)

```bash
# 1) درّب tokenizer من corpus السيادي.
python -m sf_ai.training.train_tokenizer \
    --corpus data/corpus/chat/jsonl \
    --out artifacts/tokenizers/sf_bpe/v1 \
    --vocab-size 8000

# 2) جرّب تدريب SF-10M بخطوات قليلة جدًا للتأكد من الـ pipeline.
python -m sf_ai.training.train_tiny_lm \
    --tokenizer artifacts/tokenizers/sf_bpe/v1 \
    --corpus data/corpus/chat/jsonl \
    --size sf-10m --steps 50 --batch-size 4 --seq-len 256 \
    --device auto

# 3) قيّم perplexity وأنتج عينة.
python -m sf_ai.training.evaluate_tiny_lm \
    --tokenizer artifacts/tokenizers/sf_bpe/v1 \
    --corpus data/corpus/chat/jsonl \
    --checkpoint-name sf-10m-step50 \
    --prompt "مرحبا"
```

## مبادئ
- **لا أوزان جاهزة**، لا load من checkpoint غير سيادي.
- **MPS أولًا** على Apple Silicon.
- **gradient_checkpointing + accumulation** عند الحاجة (24GB).
- **start small** (SF-10M)، توسع بعد التحقق.

التفاصيل في [docs/TRAINING_PLAN.md](../../docs/TRAINING_PLAN.md) و [docs/SOVEREIGN_ACCELERATION.md](../../docs/SOVEREIGN_ACCELERATION.md).
