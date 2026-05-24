# PROJECT_MAP.md

## خريطة المشروع

هذه خريطة ملكية المجلدات. لا تضف ملفات خارج دور المجلد.

## الجذر

```text
README.md
PROJECT_PRINCIPLES.md
SETUP_STATUS.md
Makefile
pyproject.toml
docker-compose.yml
.env.example
.gitignore
```

الدور:

- تعريف المشروع.
- أوامر التشغيل.
- إعداد البيئة.
- سياسة التجاهل والحماية.
- `NEXT_AGENT_PROMPT.md` يجب أن يوجّه أي Agent إلى Phase 27.78 وStrategy v2.

## apps/

```text
apps/api/
apps/web/
```

الدور:

- runtime applications فقط.
- `apps/api` يحتوي FastAPI والـ routers والـ schemas والـ static chat UI.
- `apps/web` placeholder للواجهة المستقبلية.
- `/health` و`/system/status` يعكسان الحالة الحالية: `Phase 27.79`.

ممنوع:

- training code.
- checkpoints.
- corpus.

## sf_ai/core/

نواة runtime والعقل التنظيمي:

```text
sf_ai/core/orchestrator/
sf_ai/core/router/
sf_ai/core/nlp/
sf_ai/core/index/
sf_ai/core/composer/
sf_ai/core/semantic/
sf_ai/core/planner/
```

الدور:

- تحليل النص.
- اختيار domain/intent.
- orchestration.
- response composition.
- capability registry.

ممنوع:

- حفظ corpus.
- تحميل pretrained models.
- كتابة artifacts تدريب.

## sf_ai/modules/

مجالات القدرة:

```text
chat/
web/
research/
coding/
data/
files/
...
```

الدور:

- module لكل domain.
- active أو skeleton_only حسب manifest/status.
- المجالات الحساسة تحمل safety gates.

## sf_ai/datasets/

أدوات البيانات:

```text
schemas.py
validators.py
loaders.py
cleaners.py
corpus_governance.py
source_inventory.py
saudi_seed.py
```

الدور:

- قراءة وفحص corpus.
- حوكمة samples.
- جرد المصادر.
- تحميل المراجع الخاصة بشكل read-only.

ممنوع:

- تدريب.
- تغيير البيانات المصدرية تلقائيًا.

## sf_ai/models/

بنية النماذج السيادية:

```text
tokenizer/
transformer/
```

الدور:

- tokenizer implementation.
- transformer implementation.
- generation utilities.

ممنوع:

- pretrained vocab.
- pretrained weights.

## sf_ai/training/

أدوات التدريب:

```text
train_tiny_lm.py
evaluate_tiny_lm.py
checkpoints.py
training_config.py
device.py
```

الدور:

- training loops.
- eval.
- checkpoint metadata.
- device management.

لا تُشغّل إلا بإذن وبعد Phase 27.78:

- لا training جديد قبل `ENGINEERING_ROOT_CAUSE_GATE`.
- القرار الحالي `PHASE27_79_REPAIR_DESIGN_DECISION.new_training_allowed=false`.
- أي script تدريب يجب أن يبقى محجوبًا حتى تمر Phase 27.80 gates الواضحة.

## sf_ai/memory/

ذاكرة واسترجاع محلي:

```text
sparse_store.py
vector_store.py
retrieval.py
long_term.py
short_term.py
```

الدور:

- BM25.
- hashing vector store.
- hybrid retrieval.

## sf_ai/tools/

أدوات خارج runtime core:

```text
tools/web/
```

الدور:

- extractors.
- crawler base.
- robots policy.
- rate limiter.
- importers.

أي crawling يحتاج إذن.

## resources/

```text
resources/lexicons/
resources/tokenization/
```

الدور:

- lexicons.
- normalization maps.
- domain terms.
- imported lexicon references.
- protected terms.
- preferred tokenizer merges.
- tokenization policy rules.

هذه ليست corpus مباشرًا. تحويلها إلى samples يتم عبر scripts موثقة وprovenance.

بعد Phase 27.78:

- لا tokenizer version جديد من `resources/tokenization/` إلا إذا أثبت gate
  جديد أن tokenizer هو السبب الأكبر.
- الوزن الحالي للتوكنزر في root cause هو `4%` فقط.

## data/

```text
data/corpus/
data/indexes/
```

الدور:

- corpus.
- raw/cleaned/jsonl/reports.
- indexes محلية.

القواعد:

- التدريب يقرأ من هنا.
- ملفات JSONL الخاصة مستثناة افتراضيًا إلا بإذن.
- كل seed يحتاج README أو CARD.

## artifacts/

```text
artifacts/tokenizers/
artifacts/checkpoints/
artifacts/logs/
```

الدور:

- مخرجات training/eval.
- tokenizer artifacts.
- checkpoints.
- logs.

لا تُرفع artifacts الثقيلة أو الحساسة إلا بإذن.

## scripts/

الدور:

- أوامر تشغيل وفحص.
- importers.
- preflight.
- training command wrappers.

أي script جديد يجب أن يكون واضح الاسم، آمن افتراضيًا، ولا يبدأ high-impact action بدون flags صريحة.

## tests/

الدور:

- pytest coverage.
- fixtures صغيرة.
- ضمانات governance/runtime/training boundaries.

أي تغيير في behavior يحتاج اختبارًا.

## docs/

الدور:

- الخطة.
- الحالة.
- السياسات.
- handoff.
- architecture.
- reports قابلة للنشر.

لا تضع corpus خاصًا داخل docs.
