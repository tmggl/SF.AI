# sf_ai/models/tokenizer

Sovereign tokenizers for SF.AI.

> **القاعدة الذهبية:** كل vocab يجب أن يُدرَّب من corpus SF.AI نفسه. لا يُحمَّل أي vocab/merges من نموذج خارجي.

## المكونات

| ملف | الغرض |
|-----|------|
| `tokenizer_config.py` | `TokenizerConfig` — `vocab_size`, `min_frequency`, `special_tokens`, `lowercase`, `byte_level` |
| `char_tokenizer.py` | `CharTokenizer` — character-level. للتجارب الأولى وSF-10M smoke tests |
| `bpe_tokenizer.py` | `BPETokenizer` — BPE نقي بـ Python يُدرَّب من الصفر |
| `train_bpe_tokenizer.py` | `train_bpe_from_corpus()` — يربط الـ BPE بـ Phase 5 ChatDataset |

## التشغيل

```bash
# تأكد أن corpus فيه بيانات (Phase 5 يضعها المستخدم).
python scripts/train_bpe.py \
    --corpus data/corpus/chat/jsonl \
    --out artifacts/tokenizers/sf_bpe/v1 \
    --vocab-size 8000
```

## شكل الناتج

```
artifacts/tokenizers/sf_bpe/v1/
├── vocab.json     # {token: id}
├── merges.txt     # قواعد الدمج بالترتيب
└── meta.json      # sf_origin: true + provenance + stats
```

## ضمانات السيادة

- `BPETokenizer.load(path)` يرفع `ValueError` إن لم يكن `meta.json.sf_origin == true`.
- `train_bpe_from_corpus()` يرفض البدء إن كان الـ corpus فارغًا.
- `training_meta` يسجل blake2b hash لكل ملف مصدر — يمكن لاحقًا التحقق من أن نفس البيانات أنتجت نفس الـ tokenizer.

## ما لا نفعله

- ❌ لا تنزيل GPT-2 / Llama / Gemma tokenizers.
- ❌ لا استخدام `tiktoken`, `tokenizers.from_pretrained`, أو أي vocab خارجي.
- ❌ لا توليد بيانات تدريب من LLM خارجي وحشرها في الـ corpus.

اقرأ [docs/SOVEREIGN_ACCELERATION.md](../../../docs/SOVEREIGN_ACCELERATION.md) للشرح الكامل.
