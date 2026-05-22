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
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack | التالية بإذن |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | معلّقة |
| Phase 13 | Tiny LM Smoke Training (Overfit + Generation Sanity) | معلّقة |
| Phase 14 | SF-10M v0.1 Training Run | معلّقة |
| Phase 15 | Generator Adapter for ChatModule | معلّقة |
| Phase 16 | Evaluation, Safety, and Saudi/MSA Style Harness | معلّقة |
| Phase 17 | Local Memory/RAG Bridge into Chat | معلّقة |
| Phase 18 | Data Expansion Loop v1 | معلّقة |
| Phase 19 | SF-50M Candidate Training | معلّقة |
| Phase 20 | Domain Activation Gates | معلّقة |

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
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
- SF-10M → SF-50M → SF-120M → SF-350M → SF-700M.
- **لا تبدأ بـ 1B مباشرة.**

### `docs/TRAINING_PLAN.md` يجب أن يوضح
- لماذا نبدأ صغيرًا.
- لماذا لا نستخدم أوزان جاهزة.
- كيف نكبر النموذج تدريجيًا.
- كيف نقيس الجودة ونتجنب الهلوسة.
- كيف نستخدم RAG لاحقًا بدل حشر المعرفة في الأوزان.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

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
- **أول توليد داخل شاشة الشات:** Phase 15، بعد وجود checkpoint صالح من Phase 14 وربطه بـ `ChatModule`.
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
توقف، ملخص، اطلب الإذن.

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
make train-bpe ARGS="--corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"
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
توقف، ملخص، اطلب الإذن.

---

## Phase 19 — SF-50M Candidate Training

### الهدف
توسيع النموذج من `SF-10M` إلى `SF-50M` فقط إذا أثبتت المراحل السابقة فائدة واضحة.

### شروط البدء
- corpus كافٍ.
- tokenizer v1 مقبول.
- SF-10M اجتاز eval.
- الجهاز والوقت مسموح بهما من سامي.

### شروط النجاح
- تحسن ملموس في eval suite.
- لا تراجع في safety.
- لا استهلاك مفرط للجهاز بدون إذن.

### بعد المرحلة
توقف، ملخص، اطلب الإذن.

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
توقف، ملخص، اطلب الإذن.

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
