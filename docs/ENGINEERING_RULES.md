# ENGINEERING_RULES.md

## قواعد الهندسة غير القابلة للكسر

هذه القواعد تحكم كل تعديل في SF.AI قبل Phase 12 وبعدها.

## 1. Runtime ≠ Training

runtime هو ما يخدم المستخدم الآن:

- API.
- Chat UI.
- Orchestrator.
- Router.
- Modules.
- Composer.

training هو ما ينتج artifacts لاحقًا:

- tokenizer artifacts.
- model checkpoints.
- eval reports.
- training logs.

ممنوع أن يكتب runtime داخل corpus أو checkpoints أو reports التدريبية.
وممنوع أن يبدأ training من runtime request.

## 2. لا pretrained

ممنوع:

- pretrained weights.
- pretrained embeddings.
- pretrained tokenizer vocabulary.
- external LLM APIs.
- sentence-transformers.
- HuggingFace pretrained models/tokenizers.
- LoRA فوق نموذج خارجي.

أي tokenizer أو checkpoint في SF.AI يجب أن يكون `sf_origin=true` أو موثقًا كـ artifact سيادي.

## 3. لا hidden shortcuts

ممنوع إضافة طريق مختصر مخفي يلتف حول الخطة، مثل:

- استدعاء LLM خارجي تحت اسم helper.
- تحميل model من الإنترنت.
- fallback ذكي غير موثق.
- dependency تضيف نموذجًا جاهزًا ضمنيًا.
- data generation من LLM خارجي.

أي shortcut مطلوب يجب أن يكون موثقًا ومصرّحًا ومرئيًا في docs.

## 4. لا phases بدون إذن

لا تبدأ مرحلة جديدة بسبب نجاح preflight.

مثال:

- `READY_FOR_PHASE_12_TOKENIZER_TRAINING` لا يعني بدء `make train-bpe`.
- إذن “التالي” لا يعني تدريبًا إذا كانت المرحلة التالية عالية الأثر.
- `make train-bpe` يجب أن يرفض التشغيل بدون `--confirm-phase12-permission`.
- التدريب، crawling، ونقل البيانات كلها تحتاج إذنًا صريحًا.

## 5. datasets منفصلة عن lexicons

المسارات:

```text
data/corpus/                 datasets/corpus
resources/lexicons/          lexicons/reference/runtime maps
```

القواعد:

- lexicon ليس corpus مباشرًا.
- corpus ليس lexicon runtime.
- تحويل lexicon إلى samples يحتاج script موثق وprovenance.
- أي ملف مشتق يجب أن يذكر مصدره في `provenance.source`.

## 6. checkpoints داخل artifacts فقط

كل مخرجات التدريب داخل:

```text
artifacts/
├── tokenizers/
├── checkpoints/
└── logs/
```

ممنوع وضع checkpoint داخل `sf_ai/` أو `data/` أو `resources/`.

## 7. corpus داخل data/corpus فقط

كل بيانات التدريب والحوار داخل:

```text
data/corpus/
```

لا تضع corpus داخل:

- `docs/`
- `tests/`
- `resources/lexicons/`
- `sf_ai/`

الاستثناء الوحيد: fixtures صغيرة جدًا للاختبارات داخل `tests/fixtures/`.

## 8. reports منفصلة

التقارير لا تختلط مع corpus ولا checkpoints.

المسارات المقبولة:

```text
data/corpus/**/reports/
artifacts/logs/
docs/
```

تقارير audit والتقييم يجب أن تكون قابلة للقراءة، ولا تحتوي أسرارًا.

## 9. tests إلزامية

كل تغيير غير تافه يحتاج اختبارًا أو تحديث اختبار.

قبل الرفع:

```bash
.venv/bin/python -m pytest tests
```

أي فشل اختبار يمنع commit/push حتى يُفهم سببه.

## 10. لا dependencies بلا توثيق

أي dependency جديدة يجب أن توثق:

- لماذا نحتاجها.
- هل تحمل نموذجًا جاهزًا أو بيانات جاهزة؟
- هل تحتاج شبكة؟
- هل تعمل offline؟
- هل تكسر السيادة المعرفية؟

التوثيق يكون في README أو docs المناسبة، والتثبيت في `pyproject.toml`.

## 11. Git hygiene

قبل push:

- شغّل الاختبارات.
- افحص الملفات الحساسة.
- لا ترفع `.env`.
- لا ترفع checkpoints أو vocab/merges إلا بإذن.
- لا ترفع payloads خاصة مستثناة في `.gitignore`.

الرسائل تكون عربية واضحة وتصف ما نجح فعليًا.

## 12. Server stability

السيرفر المحلي على `127.0.0.1:8123` يُعامل كخدمة حية أثناء العمل.

القواعد:

- افحصه عبر `make server-status`.
- إذا كان يعمل، لا تعمل restart.
- إذا كان متوقفًا، شغّله عبر `make server-start`.
- لا تستخدم `pkill` أو kill PID إلا بطلب صريح.
- لا تجعل tests أو scripts توقف السيرفر.
- أي script status يجب أن يكون read-only.

## 13. Progressive Scaling Strategy

لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي الوحيد:

```text
SF-10M
→ SF-50M
→ SF-120M
→ SF-350M
→ SF-700M
→ SF-1B+
```

ممنوع:

- القفز من `SF-10M` إلى `3B`.
- تدريب `SF-1B+` قبل نجاح الأحجام الأصغر.
- تبرير التكبير بضعف الردود فقط؛ ضعف الردود غالبًا يعني نقص بيانات أو تقييم.
- تشغيل تدريب أكبر دون تقرير scaling gate.

قبل أي حجم أكبر يجب توثيق:

- corpus readiness.
- tokenization audit.
- evaluation suite.
- safety checks.
- runtime quality.
- hallucination checks.
- repetition checks.
- resource readiness.

إذا فشل شرط واحد، الخطوة الصحيحة هي تحسين البيانات/التوكنزر/التقييم أو إعادة تدريب الحجم نفسه، لا تكبير النموذج.

## Naming Conventions

### الملفات والمجلدات

- Python packages/modules: `snake_case`.
- Scripts: فعل واضح + اسم الهدف، مثل `audit_training_corpus.py`.
- Docs: `UPPER_SNAKE_CASE.md` للوثائق الحاكمة، مثل `PROJECT_MAP.md`.
- Dataset seed: اسم وصفي + نوعه، مثل `first_dialogue_seed.jsonl`.
- Dataset card: نفس اسم الملف + `.CARD.md`.
- Reports: اسم المرحلة أو المصدر + `_report` أو `_audit`.

### الكود

- Classes: `PascalCase`.
- Functions: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Pydantic response schemas: تنتهي بـ `Response`.
- Dataclass reports: تنتهي بـ `Report`.
- Dataclass items: تنتهي بـ `Item`.

### المراحل والـ artifacts

- Tokenizer output: `artifacts/tokenizers/<name>/`.
- Checkpoint output: `artifacts/checkpoints/<run_id>/`.
- Logs/reports: `artifacts/logs/<run_id>/` أو `data/**/reports/`.
- Corpus files: `data/corpus/<domain>/jsonl/<name>.jsonl`.

### أسماء الحقول

- Dataset provenance يستخدم أسماء واضحة:
  - `source`
  - `license`
  - `language`
  - `dialect`
  - `quality`
  - `training_allowed`
  - `owner_user_id`
  - `created_by_user_id`
  - `target_user_id`
  - `user_scope`
  - `notes`

ممنوع استخدام أسماء غامضة مثل `data1`, `misc`, `tmp_final`, `new_file`.

## Architecture Rules

### Dependency direction

الاتجاه المسموح:

```text
apps → sf_ai.core / sf_ai.modules
sf_ai.modules → sf_ai.core contracts
sf_ai.training → sf_ai.models / sf_ai.datasets
sf_ai.datasets → schemas/validators/loaders only
```

الاتجاه الممنوع:

- `sf_ai.core` يعتمد على `apps`.
- runtime يعتمد على training scripts.
- datasets يعتمد على FastAPI.
- modules تكتب checkpoints.
- web tools تبدأ crawling من غير إذن.

### Boundaries

- Orchestrator ينسّق ولا يتدرب.
- Router يختار domain/intent ولا يولّد LLM.
- Composer يصيغ ردود safety/skeleton ولا يدّعي قدرة غير موجودة.
- ChatModule هو runtime module، وليس مكان training loop.
- Training modules تنتج artifacts فقط، ولا تغير runtime تلقائيًا.

### Configuration

- Flags التشغيل من environment أو launcher scripts.
- لا side effects عند import.
- لا network calls عند import.
- لا training/crawling عند import.

### Data flow

```text
User request → API → Orchestrator → NLP → Router → Module/Composer → Response
```

هذا runtime path.

```text
JSONL corpus → governance audit → tokenizer training → LM training → checkpoint → eval → runtime activation
```

هذا training lifecycle ولا يختلط بالruntime path.

### Failure mode

إذا شك النظام في القدرة:

- يصرح بالحدود.
- يرفض المجالات الحساسة بأمان.
- لا يخترع execution.
- لا يفعل fallback مخفي.
