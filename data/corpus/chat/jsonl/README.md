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
python scripts/validate_dataset.py data/corpus/chat/jsonl/your_file.jsonl
```

ثم برمجيًا لفحص حوكمة التدريب:

```python
from sf_ai.datasets import audit_jsonl_file_for_training

report = audit_jsonl_file_for_training("data/corpus/chat/jsonl/your_file.jsonl")
print(report.summary())
```
