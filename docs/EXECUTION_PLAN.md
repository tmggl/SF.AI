# EXECUTION_PLAN.md

## SF.AI — خطة التنفيذ الكاملة على مراحل

هذه الخطة الرسمية لمشروع SF.AI. كل مرحلة محددة الأهداف والمخرجات وشروط النجاح. الانتقال بين المراحل يتطلب إذنًا صريحًا من المستخدم.

---

## المبدأ الأعلى للخطة

> **نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.**

- **الهدف العام النهائي:** بناء **نموذج لغوي سيادي مولّد** لـ SF.AI، يبدأ من الصفر، يفهم العربية الفصحى واللهجة السعودية، ويتحوّل تدريجيًا من routing/rules إلى توليد لغوي حقيقي داخل الشات.
- **الحالة الحالية:** الحوار العام يعمل الآن كـ rule-based router + templates + composer. هذا ليس LLM بعد.
- **التركيز اللغوي الحالي:** العربية الفصحى + اللهجة السعودية فقط. لا توسيع للهجات أخرى في runtime قبل إتقان هذا المسار.
- **الهدف التالي العملي:** تجهيز البيانات السيادية، تدريب tokenizer من الصفر، تدريب أول LM صغير، ثم ربطه بـ ChatModule بشكل آمن.
- **بقية المجالات:** موجودة skeleton فقط حتى لا تختلط القدرة المستقبلية بالقدرة الفعلية.

## Progressive Scaling Strategy

لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي:

```text
SF-10M → SF-50M → SF-120M → SF-350M → SF-700M → SF-1B+
```

قبل أي انتقال إلى حجم أكبر، يجب أن تمر Scaling Gates:

- corpus readiness.
- tokenization audit.
- evaluation suite.
- safety checks.
- runtime quality.
- hallucination checks.
- repetition checks.
- resource readiness.

لا يحق لأي Agent القفز إلى أحجام كبيرة مثل `3B` أو `1B+` قبل مرور الأحجام السابقة ونجاح gates الخاصة بها. البيانات أهم من الحجم في البداية؛ إذا كان الرد ضعيفًا، فالخطوة الأولى هي تحسين corpus/eval/tokenizer، لا تكبير النموذج.

---

## نظرة عامة على المراحل

| المرحلة | الاسم | الحالة |
|---------|------|---------|
| Phase 0 | Project Governance & Execution Plan | جارية |
| Phase 1 | Project Foundation | مكتملة |
| Phase 2 | Core Brain Skeleton | مكتملة |
| Phase 3 | Language Understanding Layer | مكتملة |
| Phase 4 | General Chat First | مكتملة |
| Phase 5 | Dialogue Dataset Preparation | مكتملة |
| Phase 5.5 | Sovereign Acceleration Layer | مكتملة |
| Phase 6 | Native SF.AI Small Language Model | مكتملة كبنية/Scaffolding، بلا تدريب فعلي |
| Phase 7 | Web Research, Crawling, Extraction, Summarization | مكتملة offline-ready، بلا crawling تلقائي |
| Phase 8 | Local RAG Foundation | مكتملة |
| Phase 9 | Frontend Chat Interface | مكتملة |
| Phase 10 | Later Domains Skeleton | مكتملة |
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack | مكتملة |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | مكتملة مع قيود |
| Phase 13 | Tiny LM Smoke Training (Overfit + Generation Sanity) | مكتملة مع قيود |
| Phase 14 | SF-10M v0.1 Training Run | مكتملة مع قيود |
| Phase 15 | Generator Adapter for ChatModule | مكتملة كبنية آمنة |
| Phase 16 | Evaluation, Safety, and Saudi/MSA Style Harness | مكتملة مع حجب runtime |
| Phase 17 | Local Memory/RAG Bridge into Chat | مكتملة كبنية bridge محلية |
| Phase 18 | Data Expansion Loop v1 | مكتملة كدورة بيانات محكومة |
| Phase 19 | SF-50M Candidate Training | بوابة جاهزية مفعلة؛ التدريب غير جاهز لصغر corpus |
| Phase 20 | Domain Activation Gates | مكتملة؛ لا تفعيل تلقائي |
| Phase 21 | Generative Roadmap & Quality Targets | مكتملة |
| Phase 22 | Gold Dialogue Corpus v2 | مكتملة؛ corpus 500/500 جاهز لـ Phase 23 |
| Phase 23 | Tokenizer v2 Retrain & Audit | مكتملة؛ v2 جاهز لـ Phase 24 |
| Phase 24 | SF-10M v0.2 Quality Training | مكتملة بحدود؛ runtime محظور |
| Phase 25 | Generated Chat Canary v1 | مكتملة كحماية؛ real model blocked |
| Phase 26 | SF-50M v0.1 Readiness | مكتملة؛ التدريب غير جاهز حسب scaling gates |
| Phase 27 | Dialogue Evaluation v2 + corpus expansion plan | مكتملة؛ baseline pass وcorpus gate ناجح |
| Phase 27.5 | SF-10M Dialogue-Format Repair | مكتملة بحدود؛ runtime محظور |
| Phase 27.6 | SF-10M Assistant-Target Training | مكتملة بحدود؛ runtime محظور |
| Phase 27.7 | Fixed Split + Gold Social Canary | مكتملة؛ split ثابت + canary أقوى، runtime محظور |
| Phase 27.8 | SF-10M v0.6 Split Training | مكتملة بتحسن رقمي؛ runtime محظور |
| Phase 27.9 | Generation Quality Harness | مكتملة؛ harness يحجب v0.6 آليًا |
| Phase 27.10 | Short Response Repair | مكتملة بتحسن رقمي؛ التوليد ما زال محظورًا |
| Phase 27.11 | Objective/Decoding Diagnosis | مكتملة؛ stop boundary/EOS مفقود |
| Phase 27.12 | Assistant Boundary/EOS Repair | مكتملة جزئيًا؛ runtime محظور |
| Phase 27.13 | SF-10M v0.8 Boundary/EOS Wider Training | مكتملة؛ eval تحسن والتوليد محظور |
| Phase 28 | SF-120M v0.1 Candidate | مخططة؛ أول قفزة بعد نجاح SF-50M |
| Phase 29 | Runtime Hybrid Assistant v1 | مخططة |
| Phase 30 | Continuous Improvement Loop | مخططة |

---

## Phase 0 — Project Governance & Execution Plan

### الأهداف
- إنشاء خطة التنفيذ الكاملة.
- إنشاء ملفات مبادئ المشروع.
- تحديد المراحل وشروط الانتقال بينها.
- تعريف السيادة المعرفية والفرق بين الأدوات الجاهزة والعقول الجاهزة.
- تجهيز سجل الحالة.
- فرض نظام موافقة صريحة بين المراحل.

### المخرجات
- `docs/EXECUTION_PLAN.md`
- `docs/PHASE_STATUS.md`
- `PROJECT_PRINCIPLES.md`
- `SETUP_STATUS.md`

### شروط النجاح
- خطة التنفيذ مكتوبة بالكامل.
- مبادئ المشروع موثقة.
- سجل حالة المراحل موجود.
- السيادة المعرفية موثقة.
- الفرق بين الأدوات والعقول الجاهزة موثق.
- طبقة التسريع السيادي محجوزة كمرحلة 5.5.
- الحوار العام محدد كهدف أول، والبحث ثانٍ.
- لا يوجد أي تنفيذ كود (لا backend, لا router, لا NLP, لا tokenizer, لا model).

### بعد المرحلة
توقف. اطلب الإذن للانتقال إلى Phase 1 بالعبارة:
> "اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"

---

## Phase 1 — Project Foundation

### الأهداف
- إنشاء هيكل المشروع الأساسي.
- إعداد Python backend.
- إعداد FastAPI مع endpoints حد أدنى.
- إعداد بنية الاختبارات.
- إعداد Docker compose (skeleton).
- إعداد ملفات البيئة (.env.example).
- إعداد توثيق أساسي.
- بدون أي ذكاء جاهز.

### الهيكل المطلوب

```
SF.AI/
├── README.md
├── SETUP_STATUS.md
├── PROJECT_PRINCIPLES.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── pyproject.toml
│
├── apps/
│   ├── api/
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── chat.py
│   │   │   └── system.py
│   │   └── schemas/
│   │       ├── chat.py
│   │       └── system.py
│   └── web/
│       └── README.md
│
├── sf_ai/
│   ├── __init__.py
│   ├── core/
│   ├── modules/
│   ├── memory/
│   ├── tools/
│   ├── models/
│   ├── datasets/
│   └── training/
│
├── resources/
│   └── lexicons/
│
├── data/
│   ├── README.md
│   ├── corpus/
│   └── indexes/
│
├── artifacts/
│   ├── tokenizers/
│   ├── checkpoints/
│   └── logs/
│
├── tests/
├── scripts/
└── docs/
```

### شروط النجاح
- `/health` يعمل.
- `/system/status` يعمل.
- `pytest` يعمل (لو على اختبار health فقط).
- لا ذكاء جاهز.
- لا pretrained dependency.
- المشروع منظم وفق الهيكل.

### بعد المرحلة
Phase 16 اكتملت: prompt suites نجحت `15/15`. المسار اليومي العام بقي على القوالب لأن عينة SF-10M v0.1 مكررة، لكن مختبر سامي المحلي يستطيع تشغيل المولد الخام للتجربة. انتقل إلى Phase 17 لربط Memory/RAG المحلي بالشات.

---

## Phase 2 — Core Brain Skeleton

### الأهداف
بناء قلب النظام بدون نموذج لغوي جاهز.

### المكونات

```
sf_ai/core/
├── __init__.py
├── config.py
├── logging.py
├── orchestrator/
│   ├── orchestrator.py
│   └── types.py
├── router/
│   ├── intent_router.py
│   ├── domain_router.py
│   └── rules.py
├── semantic/
│   ├── semantic_explorer.py
│   ├── lexical_similarity.py
│   ├── hashing_vectorizer.py
│   └── types.py
├── index/
│   ├── capability_registry.py
│   ├── domain_manifest.py
│   └── default_registry.yaml
├── planner/
│   ├── planner.py
│   └── task_steps.py
└── composer/
    ├── response_composer.py
    └── styles.py
```

### الوظائف
- Orchestrator يستقبل الرسالة.
- Router يحدد domain و intent.
- SemanticExplorer يحسب similarity محلية (lexical / hashing / fuzzy).
- CapabilityRegistry يقرأ `default_registry.yaml`.
- ResponseComposer يرتب الرد.
- لا LLM. لا pretrained embeddings.

### Endpoint المطلوب

`POST /chat/message`

**Request:**
```json
{
  "message": "string",
  "session_id": "optional string"
}
```

**Response:**
```json
{
  "domain": "chat",
  "intent": "chat.general",
  "confidence": 0.82,
  "matched_signals": [],
  "route_reason": "...",
  "response": "..."
}
```

### بعد المرحلة
Phase 17 اكتملت كبنية bridge محلية: ChatModule يستطيع استخدام snippets من HybridRetriever عند حقنها، ويرد بوسم "من الذاكرة المحلية" مع المصدر. انتقل إلى Phase 18 لبناء دورة توسيع بيانات مضبوطة.

---

## Phase 3 — Language Understanding Layer

### الأهداف
بناء طبقة فهم النص قبل الراوتر — عربية أولًا، إنجليزية واعية.

### المكونات

```
sf_ai/core/nlp/
├── arabic_normalizer.py
├── text_cleaner.py
├── typo_corrector.py
├── dialect_mapper.py
├── arabizi_mapper.py
├── tokenizer.py
├── language_detector.py
├── intent_detector.py
├── pipeline.py
└── types.py

resources/lexicons/
├── domains.yaml
├── intents.yaml
├── arabic_normalization.yaml
├── dialects_gulf.yaml
├── dialects_common_arabic.yaml
├── typo_patterns.yaml
├── programming_terms.yaml
├── data_terms.yaml
├── files_terms.yaml
├── web_terms.yaml
├── legal_terms.yaml
├── medical_terms.yaml
├── finance_terms.yaml
├── education_terms.yaml
├── social_terms.yaml
├── safety_terms.yaml
├── stopwords_ar_en.yaml
└── arabizi_map.yaml
```

### وظائف الطبقة

1. **ArabicNormalizer**: إزالة التشكيل/التطويل، توحيد أ/إ/آ → ا داخليًا، توحيد ى/ي، معالجة ة/ه بحذر، توحيد الأرقام، تنظيف المسافات، الحفاظ على `original_text`.
2. **TextCleaner**: تنظيف رموز غير مهمة دون تدمير الأكواد. الحفاظ على `{} [] () ; : / \ . _ - = + * < >`.
3. **TypoCorrector**: fuzzy matching محلي. يرجع `corrections` مع `original / corrected / confidence / reason`. لا يصحح بقوة عند ثقة ضعيفة.
4. **DialectMapper**: الافتراضي الحالي فصحى + سعودي فقط. اللهجات الأخرى لا تُحمّل في runtime إلا بقرار صريح لاحق. يحول داخليًا إلى canonical meaning ولا يغيّر أسلوب المستخدم في الرد إلا عند الحاجة.
5. **ArabiziMapper**: `shlon → شلون`, `keef → كيف`, `abgha → ابغى`, `wen → وين`. لا يفسد مصطلحات البرمجة (`python, django, api, json, docker`).
6. **LanguageDetector**: `ar / en / mixed / code`.
7. **IntentDetector**: يقرأ `intents.yaml` و `domains.yaml`. يعطي hints فقط — لا يقرر وحده.
8. **NLP Pipeline**: دالة `analyze_user_text(text) -> NLPAnalysis` ترجع:
   - `original_text / cleaned_text / normalized_text / corrected_text`
   - `language / detected_dialect / tokens`
   - `corrections / aliases`
   - `domain_hints / intent_hints / safety_flags / confidence`

### تعديل الراوتر
Router يستخدم `NLPAnalysis` بدل النص الخام.

### نظام scoring
- exact phrase match: **+5**
- exact keyword match: **+3**
- normalized match: **+2.5**
- dialect alias match: **+2**
- typo corrected match: **+1.5**
- fuzzy match: **+1**
- safety term: يرفع safety flag ولا يكفي وحده لتحديد المجال.

### القواميس — الأهداف المبدئية
- **20 مجال**.
- **100+ intent**.
- 1500–3000 keyword/alias بجودة جيدة.
- 300–700 لهجة ومرادف.
- 300–700 أخطاء شائعة.
- أمثلة اختبار كافية.

**لا حشو. الأولوية للجودة والتنظيم.**

### المجالات

**كل المجالات (skeleton):**
chat, coding, data, files, web, research, legal, medical, finance, education, religion, social, productivity, writing, translation, image, audio, security, business, ecommerce.

**المفعّلة الآن:** `chat`.
**تُجهَّز لاحقًا:** `web`, `research`.
**بقية المجالات:** `status: skeleton_only`.

**المجالات الحساسة** (`legal, medical, finance, security, religion`):
- `requires_safety: true`
- `status: skeleton_only`

### بعد المرحلة
انتقل إلى Phase 4 لتفعيل أول مجال حوار عام فوق طبقة الفهم اللغوي.

---

## Phase 4 — General Chat First

**هذه أهم مرحلة حالية.**

### الأهداف
بناء أول طبقة حوار عام **بدون استخدام نموذج جاهز**.

### المكونات

```
sf_ai/modules/chat/
├── module.py
├── manifest.yaml
├── conversation_state.py
├── chat_patterns.py
├── chat_response_builder.py
└── prompts_or_formats.md
```

### المتطلبات
- `ChatModule` يستقبل `NLPAnalysis`.
- يفهم التحية والكلام العام والأسئلة البسيطة.
- يحافظ على session state بسيط (آخر N رسائل).
- لا يدّعي أنه نموذج قوي.
- لا ردود عشوائية ضخمة.
- لا LLM. لا نموذج جاهز.
- يوضح أن SF.AI في مرحلة بناء الحوار.
- قابل للربط لاحقًا مع نموذج SF.AI المدرّب.

### الأمثلة المدعومة
"مرحبا" / "هلا" / "السلام عليكم" / "وش اخبارك" / "ابي اسولف" / "كيف حالك" / "من انت" / "ايش تقدر تسوي" / "شلونك" / "ابي اتكلم معك" / "من صنعك" / "وش هدفك" / "انت بوت؟" / "انت نموذج؟"

### أمثلة ردود

**المستخدم:** "مرحبا"
**النظام:** "أهلًا، أنا SF.AI. أنا في مرحلة بناء الحوار العام الآن، وأستطيع حاليًا استقبال الكلام العام وتحليله وتوجيهه داخل النظام."

**المستخدم:** "من انت"
**النظام:** "أنا SF.AI، منصة ذكاء اصطناعي يتم بناؤها تدريجيًا. حاليًا أعمل على طبقة الحوار العام، وبعدها سيتم الانتقال إلى البحث في الويب والتلخيص."

**لا hardcoded سيئ.** الردود تمر عبر `ChatResponseBuilder` ثم `ResponseComposer`.

### بعد المرحلة
Phase 18 اكتملت. تفويض سامي الحالي يسمح بالمتابعة، لكن لا تدريب كبير بدون corpus كافٍ.

---

## Phase 5 — Dialogue Dataset Preparation

### الأهداف
تجهيز طريقة إدخال بيانات الحوار التي سيعطيها المستخدم.

### المكونات

```
sf_ai/datasets/
├── schemas.py
├── validators.py
├── cleaners.py
├── loaders.py
└── chat_dataset.py

data/corpus/chat/
├── raw/
├── cleaned/
└── jsonl/

docs/DATASET_FORMAT.md
```

### الصيغ المدعومة

**بسيطة:**
```json
{"text":"المستخدم: مرحبا\nالمساعد: أهلاً كيف حالك"}
```

**منظمة:**
```json
{
  "domain": "chat",
  "lang": "ar",
  "messages": [
    {"role": "user", "content": "مرحبا"},
    {"role": "assistant", "content": "أهلاً كيف حالك"}
  ]
}
```

### المتطلبات
- validator يتحقق من JSONL.
- cleaner ينظف النصوص.
- loader يقرأ الملفات.
- توثيق UTF-8 وprovenance ومصدر/ترخيص أي dataset.
- **لا تدريب الآن.** لا ملء dataset من الوكيل. الانتظار حتى يضع المستخدم البيانات.

### بعد المرحلة
انتقل إلى Phase 5.5 لبناء tokenizer/training infrastructure بدون تشغيل تدريب فعلي من هذه المرحلة.

---

## Phase 5.5 — Sovereign Acceleration Layer

### الأهداف
اختصار الطريق وتسريع بناء SF.AI **دون كسر السيادة المعرفية**.

> هذه المرحلة لا تستخدم أي نموذج جاهز ولا أي أوزان مدربة مسبقًا. الغرض منها تجهيز أدوات التدريب والتسريع لبناء أوزان SF.AI من الصفر.

### المسموح
- PyTorch، PyTorch MPS، Apple MLX (كإطار حساب).
- BPE Tokenizer مدرّب من الصفر على بيانات SF.AI فقط.
- Random initialization.
- Checkpoints من تدريب SF.AI فقط.
- AdamW وschedulers.
- Gradient accumulation / checkpointing.
- Mixed precision إذا كان مستقرًا.
- Qdrant محليًا مع vectors من SF.AI.
- Hashing / sparse lexical vectors محلية في البداية.
- Architectures معروفة (Decoder-only Transformer) بدون أوزانها.

### الممنوع
- pretrained weights/embeddings/tokenizer/vocab.
- Llama/Gemma/Phi/Mistral.
- sentence-transformers.
- LoRA فوق نموذج خارجي.
- Synthetic LLM data في corpus السيادي.
- أي API ذكاء خارجي.
- تنزيل أي نموذج/tokenizer جاهز.

### المخرجات

```
docs/SOVEREIGN_ACCELERATION.md

sf_ai/models/tokenizer/
├── char_tokenizer.py
├── bpe_tokenizer.py
├── train_bpe_tokenizer.py
├── tokenizer_config.py
└── README.md

sf_ai/training/
├── device.py
├── accelerators.py
├── checkpoints.py
├── schedules.py
├── optimizers.py
└── training_config.py

tests/
├── test_bpe_tokenizer.py
├── test_training_device.py
├── test_checkpoints.py
└── test_training_config.py
```

### Device Manager
يدعم: `cpu`, `mps` (إذا متاح), `cuda` (لاحقًا).
الأولوية: **Apple Silicon / MPS**.

### BPE Tokenizer
- قابل للتدريب من JSONL داخل `data/corpus`.
- لا يستخدم vocab جاهز.
- يحفظ vocab الناتج في `artifacts/tokenizers/sf_bpe/`.
- يسجل مصدر البيانات.
- يدعم العربية والإنجليزية والكود.
- UTF-8.
- لا يبدأ التدريب إلا بعد بيانات وإذن.

### بعد المرحلة
انتقل إلى Phase 6 لبناء نموذج صغير من الصفر وبنية تدريب سيادية.

---

## Phase 6 — Native SF.AI Small Language Model

### الأهداف
نموذج لغوي صغير خاص بـ SF.AI من الصفر.

> ليس نموذجًا جاهزًا. ليس fine-tuning. ليس LoRA. ليس adapter. **يبدأ من random initialization.**

### المكونات

```
sf_ai/models/transformer/
├── tiny_transformer.py
├── config.py
├── generation.py
├── attention.py
├── blocks.py
└── losses.py

sf_ai/training/
├── train_tiny_lm.py
├── evaluate_tiny_lm.py
├── train_tokenizer.py
├── train_embeddings.py
└── README.md
```

### المتطلبات
- PyTorch فقط (أو MLX كأداة حساب إذا ناسب).
- نموذج صغير من الصفر.
- دعم char tokenizer للتجارب التعليمية.
- دعم SF-BPE tokenizer للإصدار الجاد.
- لا pretrained. لا تحميل موديلات/datasets تلقائي. لا تشغيل تدريب الآن.
- scripts جاهزة بعد بيانات الحوار.
- model config واضح. save/load. generation/evaluation مبدئي. loss tracking. device selection من Phase 5.5.

### أحجام التدرج
- SF-10M → SF-50M → SF-120M → SF-350M → SF-700M → SF-1B+.
- **لا تبدأ بـ 1B أو 3B مباشرة.**

### `docs/TRAINING_PLAN.md` يجب أن يوضح
- لماذا نبدأ صغيرًا.
- لماذا لا نستخدم أوزان جاهزة.
- كيف نكبر النموذج تدريجيًا.
- كيف نقيس الجودة ونتجنب الهلوسة.
- كيف نستخدم RAG لاحقًا بدل حشر المعرفة في الأوزان.

### بعد المرحلة
انتقل إلى Phase 7 لبناء البحث/الاستخراج/التلخيص offline-ready بدون زحف تلقائي.

---

## Phase 7 — Web Research, Crawling, Extraction, Summarization

### الأهداف
- فهم طلب البحث، تخطيطه، جلب الصفحات بإذن، استخراج النصوص، ترتيب المصادر، تلخيص rule-based، تنظيم الرد، حفظ metadata.
- **بدون LLM جاهز.**

### المكونات

```
sf_ai/tools/web/
├── crawler_base.py
├── robots_policy.py
├── playwright_fetcher.py
├── scrapy_pipeline.py
├── html_extractor.py
├── article_extractor.py
├── rate_limiter.py
└── source_metadata.py

sf_ai/modules/web/
├── module.py
├── manifest.yaml
├── web_search_planner.py
├── web_result_ranker.py
└── web_response_builder.py

sf_ai/modules/research/
├── module.py
├── manifest.yaml
├── summarizer.py
├── citation_builder.py
└── response_organizer.py
```

### المتطلبات
- احترام `robots.txt`.
- rate limiting.
- عدم الزحف بدون إذن المستخدم.
- لا search API خارجي إلا بإذن صريح لاحقًا.
- الاعتماد مبدئيًا على URLs يحددها المستخدم.
- استخراج: `title / text / author / publish_date / url / source_domain / fetch_time`.
- تلخيص rule-based: استخراج الجمل الأهم، إزالة التكرار، ترتيب النقاط.
- citations داخلية.
- لا نموذج تلخيص جاهز. لا LLM. لا API ذكاء خارجي.
- **لا crawling فعلي الآن.**

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 8 — Local RAG Foundation

### الأهداف
RAG محلي لا يكسر السيادة.

### المكونات

```
sf_ai/memory/
├── short_term.py
├── long_term.py
├── vector_store.py
├── sparse_store.py
├── retrieval.py
└── schemas.py
```

### المتطلبات
- Qdrant محلي.
- vectors من إنتاج SF.AI فقط.
- بداية: lexical / hashing / sparse vectors + BM25-like scoring محلي.
- **لا OpenAI embeddings. لا SentenceTransformers. لا encoder جاهز.**
- interface قابل للاستبدال لاحقًا بـ SF custom embedding model.

### التوثيق
- RAG لا يكسر السيادة إذا embeddings محلية/من SF.AI.
- RAG يكسر السيادة إذا embeddings جاهزة.
- المعرفة المتخصصة تُسترجع من مصادر موثقة بدل حشرها في الأوزان.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 9 — Frontend Chat Interface

### الأهداف
واجهة بسيطة.

`apps/web/`:
- Next.js, React, TypeScript.
- RTL support.
- صفحة شات.
- input وعرض response.
- developer panel: `domain / intent / confidence / route_reason / nlp analysis مختصر / phase status`.
- تصميم بسيط.
- **لا اتصال بأي AI API خارجي.** اتصال فقط بـ backend المحلي.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 10 — Later Domains Skeleton

**لاحقًا فقط.**

### المجالات
coding, data, files, legal, medical, finance, education, religion, social, writing, translation, image, audio, security, business, ecommerce.

### المتطلبات
- skeleton فقط.
- كل module يحتوي: `manifest.yaml / module.py / status / allowed_tools / requires_safety / limitations`.
- المجالات الحساسة (`legal/medical/finance/security/religion`): `status: skeleton_only`, `requires_safety: true`.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## خارطة بناء النموذج اللغوي السيادي المولّد

هذه هي الخطة بعد Phase 10. الهدف منها نقل SF.AI من:

`Rule-based Router + Templates`

إلى:

`Sovereign Generative Language Model + Router + Safety + Memory`

بدون أي LLM خارجي، وبدون أي pretrained weights/tokenizer/embeddings.

### متى يظهر أول توليد فعلي؟

- **أول توليد خام للتجربة:** Phase 13، بعد تدريب smoke صغير جدًا للتأكد أن pipeline يتعلم.
- **أول باب توليد داخل شاشة الشات:** Phase 15 كبنية Adapter وmetadata، لكن التفعيل ينتظر Phase 16.
- **توليد مقبول للاستخدام اليومي:** بعد Phase 16، عندما يمر على اختبارات جودة وسلامة ولهجة.

---

## Phase 11 — Sovereign Corpus Governance & Saudi/MSA Dialogue Pack

### الهدف
تجهيز بيانات الحوار التي سيتعلم منها النموذج، مع حوكمة واضحة للمصدر والجودة.

### النطاق اللغوي
- العربية الفصحى.
- اللهجة السعودية.
- لا إدخال للهجات أخرى في بيانات التدريب الأساسية لهذه المرحلة.

### المسموح
- بيانات يكتبها سامي بنفسه.
- محادثات حقيقية يملك سامي حق استخدامها.
- JSONL محلي داخل `data/corpus/chat/jsonl/`.
- أمثلة instruction/dialogue قصيرة وواضحة.

### الممنوع
- أي بيانات مولدة من LLM خارجي.
- نسخ datasets من الإنترنت بدون إذن وترخيص واضح.
- خلط لهجات كثيرة قبل ضبط الفصحى/السعودي.
- تدريب النموذج قبل validation.

### المخرجات
```
docs/CORPUS_GOVERNANCE.md
docs/DIALOGUE_DATASET_RUBRIC.md
data/corpus/chat/jsonl/README.md
data/corpus/chat/jsonl/*.jsonl
artifacts/reports/corpus_v1_report.json
```

### شروط النجاح
- كل ملف JSONL يمر عبر validator.
- كل عينة لها `source`, `license`, `lang`, `dialect`, `quality`.
- لا توجد مصادر مجهولة.
- لا توجد عبارات حساسة غير موسومة.
- تقرير يوضح عدد المحادثات، عدد tokens التقريبي، نسبة فصحى/سعودي، وأخطاء التنسيق.

### بعد المرحلة
Phase 15 اكتملت كبنية آمنة دون تفعيل runtime. انتقل إلى Phase 16 لتقييم الجودة والسلامة والأسلوب قبل السماح للمولّد بالرد داخل الشات.

---

## Phase 12 — SF-BPE Tokenizer v1 Training & Audit

### الهدف
تدريب tokenizer سيادي من الصفر على بيانات SF.AI فقط.

### المخرجات
```
artifacts/tokenizers/sf_bpe/v1/
├── vocab.json
├── merges.txt
├── tokenizer_config.json
├── provenance.json
└── audit_report.json
```

### اختبارات الجودة
- تغطية جيدة للحروف العربية.
- تعامل صحيح مع المسافات والتشكيل وعلامات الترقيم.
- عدم تفتيت الكلمات السعودية الشائعة بشكل مبالغ.
- round-trip encode/decode.
- مقارنة token counts بين الفصحى والسعودي.

### أوامر متوقعة

قبل التدريب:

```bash
make source-inventory
make corpus-audit
```

`source-inventory` يشرح كل المصادر المحلية، بما فيها المراجع الخاصة مثل قاموس Saudi Seed وملف مهام اللهجة السعودية. أما `corpus-audit` فهو البوابة الصارمة لتدريب tokenizer من corpus حواري جاهز.

لا يبدأ التدريب إلا إذا ظهر:

```text
status: READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

ثم بعد إذن صريح:

```bash
make train-bpe ARGS="--confirm-phase12-permission --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"
```

### شروط النجاح
- tokenizer لا يستخدم vocab جاهز.
- provenance يثبت أنه تدرب على corpus محلي فقط.
- tests تمر.
- audit report مقروء.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 13 — Tiny LM Smoke Training

### الهدف
إثبات أن pipeline التدريبي يتعلم فعليًا من بيانات صغيرة جدًا.

هذه ليست نسخة للاستخدام. هي اختبار حياة للنموذج.

### المتطلبات
- حجم صغير جدًا: `SF-1M` أو `SF-3M`.
- overfit على عينة صغيرة مقصودة.
- خطوات قليلة.
- قياس loss قبل/بعد.
- توليد نص قصير من prompt معروف.

### المخرجات
```
artifacts/checkpoints/smoke_lm/
artifacts/reports/smoke_training_report.json
artifacts/samples/smoke_generations.md
```

### شروط النجاح
- loss ينخفض.
- checkpoint يحفظ ويُحمّل.
- generation لا يكون فارغًا أو مكسور الترميز.
- لا يُربط بالشات بعد.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 14 — SF-10M v0.1 Training Run

### الهدف
تدريب أول نموذج لغوي صغير قابل للتقييم: `SF-10M`.

### المتطلبات
- tokenizer من Phase 12.
- corpus validated من Phase 11.
- تدريب من random initialization.
- checkpoint metadata يحتوي:
  - `sf_origin=true`
  - tokenizer path
  - corpus manifest
  - config hash
  - training steps

### المخرجات
```
artifacts/checkpoints/sf_10m_v0_1/
artifacts/reports/sf_10m_training_report.json
artifacts/samples/sf_10m_generations.md
```

### شروط النجاح
- التدريب يكتمل بدون crash.
- loss curve محفوظة.
- عينات توليد محفوظة.
- النموذج لا يدّعي قدرات غير موجودة في prompts الاختبارية.
- لا يُستبدل ChatModule تلقائيًا حتى يمر Phase 15.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 15 — Generator Adapter for ChatModule

### الهدف
ربط checkpoint سيادي صغير بالشات كمولّد اختياري، مع بقاء router/safety/composer حوله.

### التصميم
```
User Message
  → NLPAnalysis
  → DomainRouter / IntentRouter
  → Safety checks
  → ChatModule
      → Template fallback OR NativeGenerator
  → ResponseComposer guardrails
  → Final response
```

### المتطلبات
- لا توليد للمجالات الحساسة.
- لا توليد للمجالات skeleton.
- max tokens محدود.
- temperature منخفضة افتراضيًا.
- fallback للقوالب عند ضعف الثقة أو فشل التوليد.
- إظهار metadata في UI: `generator=sf_10m_v0_1` أو `generator=template`.

### المخرجات
```
sf_ai/modules/chat/native_generator.py
sf_ai/modules/chat/generation_policy.py
tests/test_chat_native_generator.py
```

### شروط النجاح
- يمكن تعطيل التوليد env flag.
- لا يتجاوز safety.
- لا يكسر الردود الحالية.
- UI يوضح هل الرد من القالب أم من النموذج.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 16 — Evaluation, Safety, and Saudi/MSA Style Harness

### الهدف
قياس جودة النموذج قبل اعتباره مفيدًا في الحوار اليومي.

### حزم الاختبار
- تحيات ومحادثة قصيرة.
- أسئلة هوية وقدرات.
- فصحى مقابل سعودي.
- أسئلة حساسة: طب/قانون/مال/دين/أمن.
- أسئلة مجالات skeleton.
- أسئلة تتطلب قول "لا أعرف".
- اختبارات عدم الهلوسة.

### المخرجات
```
eval/prompts/saudi_msa_chat_v1.jsonl
eval/prompts/safety_v1.jsonl
eval/reports/sf_10m_eval_v1.json
docs/EVALUATION_PLAN.md
```

### شروط النجاح
- لا يعطي نصائح حساسة.
- لا يدّعي أنه مدرب على شيء غير موجود.
- لا يخلط لهجات غير مطلوبة.
- يمكن لسامي اختبار prompt suite يدويًا من الشاشة.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 17 — Local Memory/RAG Bridge into Chat

### الهدف
إدخال الذاكرة والاسترجاع المحلي في الشات بدون حشر المعرفة داخل الأوزان.

### القاعدة
- المعرفة المتغيرة أو الوثائقية تُسترجع من RAG.
- الأسلوب واللغة العامة يتعلمها النموذج.
- لا embeddings جاهزة.

### المخرجات
```
sf_ai/modules/chat/context_builder.py
sf_ai/modules/chat/rag_bridge.py
tests/test_chat_rag_bridge.py
```

### شروط النجاح
- ChatModule يستطيع أخذ snippets محلية من HybridRetriever.
- الرد يميز بين "من الذاكرة/المصدر" و"توليد عام".
- لا web crawling تلقائي.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

---

## Phase 18 — Data Expansion Loop v1

### الهدف
بناء دورة تحسين بيانات من اختبار سامي المباشر، بدون تعلم تلقائي خفي.

### القاعدة
- المحادثات لا تدخل التدريب تلقائيًا.
- سامي يختار ما يعتمد.
- كل عينة جديدة تمر validation وprovenance.

### المخرجات
```
apps/api/static/chat.html      # زر/وسم export لاحقًا إن أُذن
scripts/prepare_dialogue_batch.py
docs/DATA_IMPROVEMENT_LOOP.md
artifacts/reports/dialogue_batch_report.json
```

### شروط النجاح
- يمكن تحويل محادثات مختارة إلى JSONL تدريبي.
- لا يتم حفظ خاص أو حساس بدون قصد.
- dataset grows with quality tags.

### بعد المرحلة
Phase 18 اكتملت. تفويض سامي الحالي يسمح بالمتابعة، لكن لا تدريب كبير بدون corpus كافٍ.

---

## Phase 19 — SF-50M Candidate Training

### الهدف
توسيع النموذج من `SF-10M` إلى `SF-50M` فقط إذا أثبتت المراحل السابقة فائدة واضحة.

### شروط البدء
- corpus كافٍ؛ بوابة الجاهزية الحالية تطلب 5000 سجل محكوم على الأقل.
- tokenizer v1 مقبول.
- SF-10M اجتاز eval.
- الجهاز والوقت موثقان ضمن تفويض سامي الحالي، مع بقاء القرار الهندسي حسب الجاهزية.

### شروط النجاح
- تحسن ملموس في eval suite.
- لا تراجع في safety.
- لا استهلاك مفرط للجهاز بدون إذن.

### بعد المرحلة
بوابة Phase 19 أُضيفت عبر `make phase19-readiness`. القرار الحالي: لا تدريب `SF-50M` حتى يكبر corpus المحكوم ويتوازن `msa + saudi`.

---

## Phase 20 — Domain Activation Gates

### الهدف
تفعيل المجالات skeleton واحدًا واحدًا فقط بعد وجود نموذج/ذاكرة/سياسات كافية.

### القاعدة
- لا تفعيل جماعي.
- كل مجال له gate مستقل:
  - data readiness
  - safety policy
  - tests
  - UI indication
  - fallback path

### المجالات الحساسة
`legal`, `medical`, `finance`, `security`, `religion` تبقى safety-first، ولا تُفعّل للتخصص إلا بسياسات ومصادر واختبارات صارمة.

### بعد المرحلة
Phase 20 اكتملت كبوابة read-only. انتقل إلى Phase 21 لتثبيت خارطة الوصول إلى حوار مولّد مقنع.

---

## Phase 21 — Generative Roadmap & Quality Targets

### الهدف
تمديد الخطة بعد Phase 20 حتى يكون واضحًا لسامي متى يبدأ التدريب المفيد ومتى نتوقع حوارًا مولّدًا لا قالبًا.

### القاعدة
- لا نخلط بين `template` و`generator`.
- لا نعد بحوار ذكي قبل وجود corpus كافٍ.
- لا ندرّب نموذجًا أكبر لأن المستخدم متحمس فقط؛ ندرّبه عند جاهزية البيانات.
- المسار اللغوي الحالي: `msa + saudi` فقط.

### مخرجات المرحلة
- `docs/GENERATIVE_ROADMAP.md`
- تحديث `docs/EXECUTION_PLAN.md`
- تحديث `docs/PHASE_STATUS.md`
- تحديث `docs/CURRENT_GOALS.md`

### شروط النجاح
- يعرف أي Agent أن التدريب الفعلي بدأ في Phase 13/14 لكنه غير مقنع بعد.
- يعرف أي Agent أن أول تدريب جودة مفيد اكتمل في Phase 24، لكنه لم يفتح runtime واسع.
- يعرف أي Agent أن أول حوار مولّد مقنع مستهدف في Phase 26–28.
- يعرف أي Agent أن التكبير الرسمي تدريجي: `10M → 50M → 120M → 350M → 700M → 1B+`.
- يعرف سامي ماذا يكتب الآن لاختبار الفرق بين القالب والمولد.

### بعد المرحلة
انتقل إلى Phase 22: بناء corpus حواري gold v2.

---

## Phase 22 — Gold Dialogue Corpus v2

### الهدف
توسيع corpus من seed أولي صغير إلى 500 سجل حوار محكوم على الأقل، مع توازن فصحى/سعودي.

### شروط البيانات
- `dialect ∈ {msa, saudi}` فقط.
- `training_allowed=true`.
- `quality ∈ {gold, silver}` مع تفضيل gold.
- `source/license` إلزامية.
- لا synthetic LLM data من مصدر خارجي أو مجهول.
- owner-delegated agent-authored مسموح فقط إذا حمل source/license/quality/notes كاملة وتفويض سامي.
- لا بيانات حساسة أو خاصة إلا بعد مراجعة صريحة.

### شروط النجاح
- `make corpus-audit` يمر.
- `make phase22-readiness` يمر.
- `make phase22-completion-gate` يرجع `PHASE22_COMPLETE_READY_FOR_PHASE23`.
- `make source-inventory` يوضح مصدر كل batch.
- لا يوجد `missing_required_dialects=["msa"]`.
- لا synthetic LLM data من مصدر خارجي أو مجهول.
- 500 سجل حوار محكوم على الأقل.
- 200 سجل على الأقل لكل من `msa` و`saudi`.

### بعد المرحلة
انتقل إلى Phase 23.

---

## Phase 23 — Tokenizer v2 Retrain & Audit

### الهدف
إعادة تدريب SF-BPE tokenizer من corpus الأكبر والمتوازن.

### شروط النجاح
- no pretrained vocab.
- protected Saudi terms لا تُكسر aggressively.
- `tokenization-audit` يمر.
- مقارنة v1/v2 موثقة.

### نتيجة التنفيذ
- artifact: `artifacts/tokenizers/sf_bpe/v2/`.
- status: `COMPLETED_READY_FOR_PHASE24`.
- `vocab=4493`, `merges=4386`.
- corpus: `500` سجل، `msa=250`, `saudi=250`.
- protected Saudi terms: متوسط tokens تحسن من `4.0` إلى `2.3`.

### بعد المرحلة
انتقل إلى Phase 24.

---

## Phase 24 — SF-10M v0.2 Quality Training

### الهدف
أول تدريب جودة مفيد بعد corpus أكبر، وليس smoke فقط.

### شروط البدء
- 500 سجل حوار محكوم على الأقل.
- tokenizer v2 جاهز.
- eval prompts جاهزة.

### شروط النجاح
- loss/perplexity أفضل من SF-10M v0.1.
- عينات التوليد أقل تكرارًا من عينة “المعنى/وأين”.
- لا runtime واسع إلا بعد Phase 25.

### نتيجة التنفيذ

Phase 24 اكتملت بقرار:

```text
COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED
```

النتيجة الرقمية:

- tokenizer: `artifacts/tokenizers/sf_bpe/v2`.
- corpus: `500` سجل (`msa=250`, `saudi=250`).
- تدريب `SF-10M v0.2`: `2000` خطوة، `epochs=25`.
- loss: `8.4751 → 2.8256`.
- eval loss: `2.5779`.
- perplexity: `13.17`.

القرار العملي:

- التدريب نجح كتحسن معملي.
- التوليد ما زال غير متماسك.
- ممنوع تفعيله كمسار رد واسع في الشات.
- المرحلة التالية تبني canary صغيرًا مع fallback صارم.

التقرير:

- `docs/PHASE24_SF10M_V0_2_REPORT.md`
- `artifacts/reports/sf_10m_v0_2_training_report.json`
- `artifacts/samples/sf_10m_v0_2_generations.md`

### بعد المرحلة
انتقل إلى Phase 25.

---

## Phase 25 — Generated Chat Canary v1

### الهدف
تشغيل المولد داخل الشات على prompts آمنة فقط، مع fallback عند التكرار أو الضعف.

### شروط النجاح
- الواجهة تعرض بوضوح `generator=sf_10m_v0_2`.
- detector للتكرار يمنع الرد الرديء من الظهور كأنه نجاح.
- يمكن لسامي اختبار نفس prompts قبل/بعد التدريب.

### نتيجة التنفيذ

Phase 25 اكتملت بقرار:

```text
COMPLETED_GUARDED_CANARY_REAL_MODEL_BLOCKED
```

ما تحقق:

- أضيف `GenerationGuard`.
- أضيف شرط `SF_GENERATOR_CANARY=true` فوق فلاغات المختبر السابقة.
- حُدّث `NativeGenerator` إلى `sf_10m_v0_2`.
- إذا فشل canary، يعود `ChatModule` إلى القالب ويضيف:
  - `native_generator:canary_blocked`
  - `generation_guard:<reason>`

التجربة الحقيقية:

```text
prompt: اكتب رد قصير عن هدف SF.AI
decision: blocked
reason: malformed_token
fallback: template
```

القرار العملي:

- canary نجح كحماية.
- `SF-10M v0.2` لم ينجح كمحادثة مفتوحة.
- Phase 26 لا يبدأ كتدريب أكبر أعمى؛ يبدأ ببوابة readiness/scaling.

### بعد المرحلة
انتقل إلى Phase 26.

---

## Phase 26 — SF-50M v0.1 Readiness

### الهدف
تطبيق بوابة readiness/scaling قبل أي تدريب `SF-50M`. هذه المرحلة لا تبدأ تدريبًا؛
هي قرار هندسي يجيب: هل نكبر النموذج الآن أم نصلح البيانات والجودة أولًا؟

### شروط البدء
- `SF-10M v0.2` تحسن بوضوح على v0.1.
- corpus جاهز وفق Phase 19 أو قرار gate موثق.
- `tokenization-audit` يمر.
- evaluation/safety/repetition/hallucination checks تمر.
- الموارد جاهزة للتدريب والاستئناف.

### نتيجة التنفيذ
اكتملت Phase 26 بقرار:

```text
NOT_READY_IMPROVE_SF10M_AND_CANARY
can_start_sf50m_training=false
```

الأسباب:

- corpus كان `500` سجل عند قرار Phase 26، ثم صار `5143` بعد تنظيف الحوارات التشغيلية؛ الحد العملي لـ `SF-50M` هو `5000` سجل.
- `SF-10M v0.2` تحسن رقميًا لكنه بقي runtime-blocked.
- Phase 25 حجب تجربة النموذج الحقيقي بـ `generation_guard:malformed_token`.
- hallucination/repetition/runtime quality gates لم تنجح بعد.

### artifacts
- `sf_ai/training/phase26_readiness.py`
- `scripts/phase26_readiness.py`
- `make phase26-readiness`
- `GET /system/phase26-readiness`
- [PHASE26_SF50M_READINESS_REPORT.md](./PHASE26_SF50M_READINESS_REPORT.md)
- `artifacts/reports/phase26_sf50m_readiness_report.json`

### بعد المرحلة
انتقل إلى Phase 27: تقييم حوار v2 وخطة توسيع corpus قبل إعادة محاولة `SF-50M`.

---

## Phase 27 — Dialogue Evaluation v2 + Corpus Expansion Plan

### الهدف
تقييم حوار متعدد الأدوار بدل prompt واحد، وتحويل نتيجة Phase 26 إلى خطة بيانات
واضحة ترفع corpus من `500` باتجاه `5000` سجل داخل `msa + saudi`.

### محاور التقييم
- اجتماعي.
- سؤال/جواب.
- فصحى.
- سعودي.
- متابعة سياقية.
- رفض حساس.
- كشف تكرار.

### نتيجة التنفيذ

اكتملت Phase 27 بقرار:

```text
COMPLETED_DIALOGUE_EVAL_V2_BASELINE_PASS_CORPUS_GATE_PASSED
```

النتائج:

- suite متعدد الأدوار: `7` سيناريوهات، `19` turn.
- التوجيه الحالي نجح: `19/19`.
- كل الردود الحالية `template`، لذلك لا نعرضها كحوار مولّد ذكي.
- `open_generator_ready=false`.
- `can_reopen_sf50m_gate=false`.
- `can_start_phase28=false`.

خطة corpus:

```text
current_records      = 5143
target_records       = 5000
remaining_records    = 0
batches_needed_total = 9
needed_by_dialect    = msa=0, saudi=0
```

### artifacts

- `eval/prompts/dialogue_v2.json`
- `sf_ai/evaluation/phase27.py`
- `scripts/phase27_dialogue_eval.py`
- `make phase27-dialogue-eval`
- `GET /system/phase27-dialogue-eval`
- [PHASE27_DIALOGUE_EVAL_V2_REPORT.md](./PHASE27_DIALOGUE_EVAL_V2_REPORT.md)
- `eval/reports/dialogue_eval_v2.json`
- `artifacts/reports/phase27_dialogue_eval_v2_report.json`

### بعد المرحلة
لا تنتقل إلى Phase 28 الآن. بعد اكتمال توسعة corpus، نفّذ إصلاح جودة
`SF-10M` بصيغة حوارية قبل أي تكبير.

---

## Phase 27.5 — SF-10M Dialogue-Format Repair

### الهدف
إصلاح طريقة تدريب/تقييم `SF-10M` بعد اكتمال corpus gate عند `5143` سجلًا،
لأن التدريب السابق كان يسطّح الرسائل ولا يحفظ علاقة المستخدم بالمساعد.

### نتيجة التنفيذ

اكتملت Phase 27.5 بقرار:

```text
COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED
```

ما تحقق:

- أضيف بث حواري كامل عبر `ChatDataset.iter_dialogue_texts()`.
- أصبح `train_tiny_lm` يستخدم `--stream-format dialogue` افتراضيًا.
- أضيف `--chat-prompt` إلى `evaluate_tiny_lm`.
- أضيف استخراج رد المساعد من النص المولّد حتى لا تختلط علامات الأدوار بالرد.
- دُرّب `SF-10M v0.4` على corpus كامل بصيغة حوارية.

نتيجة التدريب:

```text
model      = sf-10m
params     = 7,444,992
records    = 5143
steps      = 4000
loss       = 8.4662 → 1.4070
eval loss  = 5.8267
perplexity = 339.24
```

قرار الجودة:

- النموذج تعلّم صيغة الأدوار أفضل من التدريب المسطح.
- الردود ما زالت غير مرتبطة كفاية بالسؤال.
- لا يتم تفعيل `SF-10M v0.4` في الواجهة.
- لا يبدأ `SF-50M` ولا Phase 28 حتى ينجح نموذج أصغر في canary حقيقي.

### artifacts

- [PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md](./PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md)
- `artifacts/reports/sf_10m_v0_4_dialogue_format_report.json`
- `artifacts/samples/sf_10m_v0_4_generations.md`

### بعد المرحلة
نفّذ assistant-target training/loss masking قبل التكبير، ثم canary حقيقي على
`SF-10M`. افتح `SF-50M` فقط إذا مرّت بوابات الجودة.

---

## Phase 27.6 — SF-10M Assistant-Target Training

### الهدف
جعل سياق المستخدم وعلامات الأدوار خارج الخسارة، وتدريب النموذج على رد
المساعد فقط.

### نتيجة التنفيذ

اكتملت Phase 27.6 بقرار:

```text
COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED
```

ما تحقق:

- أضيف `--loss-scope assistant` إلى `train_tiny_lm` و`evaluate_tiny_lm`.
- أضيف masking بقيمة `-100` لكل user/context/role-marker token.
- دُرّب `SF-10M v0.5` على corpus الحالي.

نتيجة التدريب:

```text
model      = sf-10m
params     = 7,444,992
records    = 5143
steps      = 4000
loss       = 8.4643 → 2.3513
best eval  = step2000 loss 6.5718, perplexity 714.65
```

قرار الجودة:

- الهدف الهندسي صار أصح من v0.4.
- الردود ما زالت مكررة وضعيفة.
- لا يتم تفعيل `SF-10M v0.5` في الواجهة.
- لا يبدأ `SF-50M` ولا Phase 28.

### artifacts

- [PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md](./PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md)
- `artifacts/reports/sf_10m_v0_5_assistant_target_report.json`
- `artifacts/samples/sf_10m_v0_5_generations.md`

### بعد المرحلة
ابنِ fixed train/eval split، وأضف gold social dialogue صغير عالي الجودة، وشدد
canary الصلة بالسؤال والتكرار قبل أي تكبير.

---

## Phase 27.7 — Fixed Split + Gold Social Canary

### الهدف
إغلاق فجوة تقييم مهمة قبل التدريب التالي: يجب ألا يقيس المشروع النموذج على
نفس تيار التدريب، ويجب ألا يسمح canary برد عربي شكلي لا يجيب السؤال.

### نتيجة التنفيذ

اكتملت Phase 27.7 بقرار:

```text
COMPLETED_QUALITY_GATE_RUNTIME_BLOCKED
```

ما تحقق:

- أضيف `sf_ai/datasets/splits.py` لبناء split ثابت من corpus الحوار.
- أضيف `scripts/build_dialogue_split.py` وهدف `make build-dialogue-split`.
- أضيف `data/corpus/chat/splits/dialogue_split_v1.json`.
- أضيف `--split-manifest` و`--split-name` إلى التدريب والتقييم.
- أضيفت دفعة gold social dialogue صغيرة: 100 سجل طبيعي من تأليف المشروع فقط.
- أضيف `GenerationGuard.inspect_for_prompt()` كحارس prompt-aware.

نتيجة corpus/split:

```text
records = 5243
train   = 4703
eval    = 540
msa     = 2599
saudi   = 2644
issues  = 0
```

قرار الجودة:

- التدريب التالي يجب أن يستخدم `split-name=train`.
- التقييم المقبول يجب أن يستخدم `split-name=eval`.
- لا يتم تفعيل أي checkpoint في الواجهة إلا إذا مر repetition/hallucination/runtime quality.
- `SF-50M` لا يبدأ قبل نجاح `SF-10M v0.6` على هذا split أو وجود مبرر جودة موثق.

### artifacts

- [PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md](./PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md)
- `artifacts/reports/phase27_7_fixed_split_gold_social_canary_report.json`
- `data/corpus/chat/splits/dialogue_split_v1.json`

### بعد المرحلة
درّب `SF-10M v0.6` على `train split` فقط بخسارة assistant-target، ثم قيّمه على
`eval split`، ثم شغّل canary prompt-aware قبل أي تشغيل واجهة أو قرار تكبير.

---

## Phase 27.8 — SF-10M v0.6 Split Training

### الهدف
تدريب `SF-10M v0.6` على `train split` فقط وقياسه على `eval split` المعزول
للحكم الحقيقي على جودة التوليد قبل أي تكبير.

### نتيجة التنفيذ

اكتملت Phase 27.8 بقرار:

```text
COMPLETED_WITH_NUMERIC_IMPROVEMENT_RUNTIME_BLOCKED
```

نتيجة التدريب والتقييم:

```text
train_records = 4703
eval_records  = 540
steps         = 4000
loss          = 8.4743 → 3.7460
best eval     = step4000 loss 5.0227, perplexity 151.82
canary        = 0/10 allowed
```

قرار الجودة:

- `SF-10M v0.6` أفضل رقميًا من v0.5 على eval split.
- التوليد ما زال يحتوي fragments مشوهة.
- canary يحجب النموذج عن الواجهة.
- لا يبدأ `SF-50M` حتى تُصلح جودة التوليد القصير.

### artifacts

- [PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md](./PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md)
- `artifacts/reports/sf_10m_v0_6_split_training_report.json`
- `artifacts/samples/sf_10m_v0_6_generations.md`

### بعد المرحلة
ابدأ إصلاح جودة التوليد القصير: eval suite آلي لعينات التوليد، gold social
أعلى، وفحص tokenizer/decoding قبل إعادة تدريب صغيرة.

---

## Phase 27.9 — Generation Quality Harness

### الهدف
تثبيت بوابة آلية تقيس التوليد الخام القصير خارج واجهة الشات، حتى لا يكون
قرار التفعيل قائمًا على perplexity أو الانطباع اليدوي فقط.

### نتيجة التنفيذ

اكتملت Phase 27.9 بقرار:

```text
COMPLETED_GENERATION_QUALITY_HARNESS_BLOCKING_V0_6
```

ما تحقق:

- أضيف prompt suite قصير `msa + saudi`.
- أضيف runner يحمّل checkpoint ويمرر المخرجات عبر canary prompt-aware.
- أضيف report JSON قابل للمقارنة بين checkpoints.

نتيجة `SF-10M v0.6`:

```text
prompts         = 10
passed          = 0
runtime_allowed = false
primary reason  = model_artifact_fragment
```

### artifacts

- [PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md](./PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md)
- `eval/prompts/generation_quality_v1.json`
- `eval/reports/generation_quality_v1.json`
- `artifacts/reports/generation_quality_v1_report.json`

### بعد المرحلة
أصلح fragments قبل أي تكبير: فحص tokenizer/decoding، ثم تدريب إصلاحي صغير
على gold social أو short-response corpus، ثم إعادة Phase 27.9.

---

## Phase 27.10 — Short Response Repair

### الهدف
اختبار ما إذا كانت دفعة gold قصيرة ومركزة تقلل fragments في `SF-10M` بدون
القفز إلى حجم أكبر.

### نتيجة التنفيذ

اكتملت Phase 27.10 بقرار:

```text
COMPLETED_NUMERIC_IMPROVEMENT_GENERATION_STILL_BLOCKED
```

ما تحقق:

- أضيفت `300` عينة gold قصيرة (`150` فصحى + `150` سعودي).
- أصبح corpus `5543` سجلًا، والـ gold `431`.
- دُرّب `SF-10M v0.7` على split الجديد.
- تم توسيع `GenerationGuard` للـ fragments التي ظهرت بعد v0.7.

نتيجة `SF-10M v0.7`:

```text
train = 4973
eval  = 570
loss  = 8.4840 → 3.1259
best eval = step4000 loss 4.7512, perplexity 115.72
generation_quality = 0/10
runtime_allowed = false
```

### artifacts

- [PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md](./PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md)
- `artifacts/reports/sf_10m_v0_7_short_repair_report.json`
- `artifacts/samples/sf_10m_v0_7_generations.md`

### بعد المرحلة
لا تكبير. افحص objective/batching/decoding؛ جرّب training comparison على gold-only
كمعمل، لا كتفعيل runtime.

---

## Phase 27.11 — Objective/Decoding Diagnosis

### الهدف
تحديد هل فشل `SF-10M` سببه نقص بيانات عام، أم خلل في هدف التدريب/حدود الرد/decoding.

### نتيجة التنفيذ

اكتملت Phase 27.11 بقرار:

```text
FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING
```

ما تحقق:

- أضيف `scripts/phase27_11_objective_probe.py`.
- أضيف `make phase27-objective-probe`.
- شُغّل probe على `16` ردًا gold قصيرًا فقط (`msa=8`, `saudi=8`).
- وصل التدريب إلى loss شبه صفري، لكن التوليد فشل `0/16 clean-stop`.

النتيجة:

```text
checkpoint = sf-10m-step1000
passed = 0/16
guard:repetition = 6
overgenerates_after_expected = 10
```

### التشخيص

النموذج يحفظ بدايات الردود، لكنه لا يعرف أين يتوقف. هذا يعني أن المرحلة
التالية يجب أن تضيف حدًا صريحًا لرد المساعد:

- assistant reply boundary
- EOS/stop token سيادي
- loss target يتعلم نهاية الرد
- decoding يتوقف عند الحد

### artifacts

- [PHASE27_11_OBJECTIVE_PROBE_REPORT.md](./PHASE27_11_OBJECTIVE_PROBE_REPORT.md)
- `artifacts/reports/phase27_11_objective_probe_report.json`
- `artifacts/samples/phase27_11_objective_probe_generations.md`

### بعد المرحلة
لا يبدأ `SF-50M`. نفّذ Phase 27.12 لإصلاح boundary/EOS ثم أعد probe وgeneration-quality.

---

## Phase 27.12 — Assistant Boundary/EOS Repair

### الهدف
إضافة حد نهاية صريح لرد المساعد، واستخدام نطاق لغوي واضح للفصحى والسعودي
قبل أي تكبير للنموذج.

### نتيجة التنفيذ

اكتملت Phase 27.12 بقرار:

```text
COMPLETED_BOUNDARY_EOS_PARTIAL_SEMANTIC_BLOCKED
```

ما تحقق:

- `assistant-target` صار يضيف `<eos>` بعد كل رد مساعد.
- `NativeGenerator` و`evaluate_tiny_lm` يوقفان decoding عند `<eos>`.
- التدريب الحواري صار يضيف conditioning من provenance:

```text
النطاق: فصحى
النطاق: سعودي
```

نتيجة probe:

```text
records = 16
semantic_clean_pass = 5/16
guard_pass = 9/16
runtime_allowed = false
```

### التشخيص

EOS حسّن التوقف ومنع جزءًا من الحشو، لكنه لم يحل جودة الرد بالكامل.
ما زال النموذج يحتاج تدريب `SF-10M v0.8` على corpus أوسع بنفس الصيغة قبل أي
محاولة `SF-50M`.

### artifacts

- [PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md](./PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md)
- `artifacts/reports/phase27_12_eos_probe_report.json`
- `artifacts/samples/phase27_12_eos_probe_generations.md`

### بعد المرحلة
نفّذ Phase 27.13: تدريب `SF-10M v0.8` بصيغة boundary/EOS + dialect conditioning
على train split، ثم eval وgeneration-quality. لا يبدأ `SF-50M`.

---

## Phase 27.13 — SF-10M v0.8 Boundary/EOS Wider Training

### الهدف
اختبار ما إذا كان إصلاح boundary/EOS وdialect conditioning يتحولان إلى جودة
توليد أفضل عند التدريب على corpus الأوسع، وليس فقط على gold probe صغير.

### نتيجة التنفيذ

اكتملت Phase 27.13 بقرار:

```text
COMPLETED_EVAL_IMPROVED_GENERATION_STILL_BLOCKED
```

ما تحقق:

- دُرّب `SF-10M v0.8` من الصفر 6000 خطوة على train split فقط.
- استخدم التدريب:
  - `stream_format=dialogue`
  - `loss_scope=assistant`
  - assistant `<eos>`
  - dialect conditioning: `النطاق: فصحى` / `النطاق: سعودي`
- أداة generation-quality صارت تمرر dialect للمولد.
- تم تشديد `GenerationGuard` ضد fragments v0.8.

نتيجة eval split:

```text
best_checkpoint = sf-10m-step6000
eval_loss       = 3.1875
perplexity      = 24.23
```

نتيجة generation-quality:

```text
passed          = 3/10
runtime_allowed = false
```

### التشخيص

هناك تحسن رقمي قوي مقارنة بـ v0.7، لكن الردود الخام ما زالت تكسر كلمات عربية
وتفشل في التحيات والشكر وتفضيل اللهجة السعودية. هذا يعني أن المشكلة لم تعد
boundary فقط؛ نحتاج إصلاح دلالي/لغوي موجه قبل أي تفعيل أو تكبير.

### artifacts

- [PHASE27_13_SF10M_V08_REPORT.md](./PHASE27_13_SF10M_V08_REPORT.md)
- `artifacts/reports/sf_10m_v0_8_boundary_eos_training_report.json`
- `artifacts/reports/generation_quality_v1_v0_8_report.json`

### بعد المرحلة
نفّذ Phase 27.14: semantic/lexical repair curriculum + stricter canary. لا يبدأ
`SF-50M` ولا Phase 28.

---

## Phase 28 — SF-120M v0.1 Candidate

### الهدف
تدريب أول قفزة بعد `SF-50M` فقط إذا أثبت `SF-50M` قيمة واضحة.

### شروط البدء
- نجاح `SF-50M v0.1` في Dialogue Evaluation v2.
- corpus أكبر وأكثر تنوعًا داخل `msa + saudi`.
- Scaling Gates كاملة.
- tokenizer حديث.
- eval v2 جاهز.

### شروط النجاح
- أول هدف رسمي لحوار مولّد مقنع ومستقر نسبيًا.
- تفوق واضح على SF-50M في الحوار القصير والمتعدد الأدوار.

### بعد المرحلة
انتقل إلى Phase 29.

---

## Phase 29 — Runtime Hybrid Assistant v1

### الهدف
دمج generator + router + safety + memory/RAG + fallback داخل تجربة يومية واحدة.

### شروط النجاح
- الرد الافتراضي في الأسئلة العامة مولّد عند الجودة الكافية.
- القوالب تبقى فقط للتحية/السلامة/الفشل، لا لإخفاء ضعف النموذج.
- الواجهة تظل صريحة: مولّد، قالب، ذاكرة، أو fallback.

### بعد المرحلة
انتقل إلى Phase 30.

---

## Phase 30 — Continuous Improvement Loop

### الهدف
تحويل اختبار سامي اليومي إلى دورة تحسين:

`UI test → export → review → corpus → training → eval → runtime`

وداخل هذه الدورة لا يُسمح بالانتقال إلى:

```text
SF-350M → SF-700M → SF-1B+
```

إلا بعد نجاح الأحجام السابقة في scaling gates.

### شروط النجاح
- كل تحسين قابل للقياس.
- لا بيانات تدخل التدريب تلقائيًا.
- لا نموذج يدخل runtime دون eval.

---

## ملفات التوثيق التي ستُكتب تدريجيًا

- `docs/ARCHITECTURE.md`
- `docs/EXECUTION_PLAN.md` ✓ (هذا الملف)
- `docs/PHASE_STATUS.md` ✓
- `docs/ROUTER.md`
- `docs/SEMANTIC_EXPLORER.md`
- `docs/LANGUAGE_UNDERSTANDING.md`
- `docs/DATASET_FORMAT.md`
- `docs/SOVEREIGN_ACCELERATION.md`
- `docs/TRAINING_PLAN.md`
- `docs/WEB_RESEARCH_PLAN.md`
- `docs/WEB_CRAWLING_POLICY.md`
- `docs/RAG_PLAN.md`
- `docs/NEXT_STEPS.md`

---

## المعمارية العامة (نظرة مستقبلية)

```
User
 ↓
Frontend
 ↓
API
 ↓
Language Understanding Layer
 ↓
Orchestrator
 ↓
Router
 ↓
Semantic Explorer
 ↓
Global Capability Registry
 ↓
Module
 ↓
Tools / Memory / Dataset / Training
 ↓
Response Composer
 ↓
Final Response
```

---

## جهاز المستخدم

- **MacBook Air M4**, 24GB.
- استخدم PyTorch MPS إذا متاح، CPU fallback، CUDA لاحقًا.
- **لا تدريب ثقيل الآن. لا عمليات تستهلك الجهاز دون إذن.**

---

## أسلوب العمل داخل كل مرحلة

1. اقرأ `docs/EXECUTION_PLAN.md`.
2. اقرأ `docs/PHASE_STATUS.md`.
3. تأكد من المرحلة المسموح بها.
4. لا تنفذ مرحلة غير مصرح بها.
5. نفذ المطلوب فقط.
6. شغّل الاختبارات المتعلقة.
7. حدّث `docs/PHASE_STATUS.md`.
8. اكتب ملخصًا للمستخدم.
9. توقف واطلب الإذن:
   > "اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"

### صيغة ملخص نهاية المرحلة
- المرحلة المنفذة
- ما تم إنشاؤه
- ما تم تعديله
- الاختبارات
- النتيجة
- المشاكل
- المرحلة التالية المقترحة
- هل تسمح بالانتقال؟
