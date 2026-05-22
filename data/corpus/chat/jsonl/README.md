# data/corpus/chat/jsonl

هذا هو مكان ملفات JSONL الجاهزة لمرحلة Phase 11 وما بعدها.

لا تضع هنا إلا بيانات:

- فصحى أو سعودية.
- مملوكة أو مرخّصة بوضوح.
- غير مولدة من LLM خارجي.
- تحتوي `provenance` كامل.

## مثال سجل تدريبي صالح

```json
{"domain":"chat","lang":"ar","messages":[{"role":"user","content":"وشلونك؟"},{"role":"assistant","content":"بخير، شكرًا لك."}],"provenance":{"source":"sami-authored","license":"user-provided","language":"ar","dialect":"saudi","quality":"gold"}}
```

## فحص الملف

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/your_file.jsonl
```

## فحص جاهزية التدريب قبل Phase 12

بعد وضع ملف أو أكثر بصيغة `.jsonl` في هذا المجلد:

```bash
make corpus-audit
```

إذا ظهر:

```text
status: READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

يمكن الانتقال إلى تدريب tokenizer بعد إذن صريح. إذا ظهر:

```text
status: NOT_READY_FOR_TRAINING
```

لا يبدأ التدريب بعد؛ أصلح الأخطاء التي يعرضها التقرير.

## فحص برمجي

```python
from sf_ai.datasets import audit_jsonl_directory_for_training, audit_jsonl_file_for_training

report = audit_jsonl_file_for_training("data/corpus/chat/jsonl/your_file.jsonl")
print(report.summary())

directory_report = audit_jsonl_directory_for_training("data/corpus/chat/jsonl")
print(directory_report.summary())
```
