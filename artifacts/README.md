# artifacts/

نواتج البناء والتدريب الخاصة بـ SF.AI.

## الهيكل

```
artifacts/
├── tokenizers/         # vocab + merges من SF-BPE (Phase 5.5)
│   └── sf_bpe/         # المسار المخصص لـ SF native BPE
├── checkpoints/        # نقاط حفظ النموذج (Phase 6)
└── logs/               # سجلات التدريب والتشغيل
```

## قواعد

1. **كل** ملف tokenizer هنا يجب أن يكون من تدريب SF.AI فقط.
2. **لا تنزّل** هنا أي tokenizer جاهز من HuggingFace أو غيره.
3. **كل** checkpoint يجب أن يكون ناتج تدريب SF.AI فقط.
4. **لا تضع** أوزانًا جاهزة.
5. ملفات `.gitignore` تستثني المحتوى الثقيل افتراضيًا — يبقى الهيكل فقط.
