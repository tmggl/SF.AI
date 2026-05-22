# SF.AI Chat Review Exports

ضع هنا ملفات JSONL المصدّرة من شاشة الشات للمراجعة اليدوية.

هذه الملفات ليست corpus تدريبيًا مباشرة:

- يجب أن تبقى `training_allowed=false` عند التصدير من الواجهة.
- لا تدخل `data/corpus/chat/jsonl/` إلا عبر `scripts/prepare_dialogue_batch.py`.
- أي تحويل تدريبي يتطلب `--training-allowed` + `--quality` + `--dialect`.

مثال:

```bash
make phase22-review-intake

make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/sfai_chat_review.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v1.jsonl --quality silver --dialect saudi --training-allowed"
```

قبل أي تحويل، شغّل `make phase22-review-intake` أو افتح
`GET /system/phase22-review-intake` لمعرفة الملفات المرشحة والملاحظات.
