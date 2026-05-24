# EXECUTION_PLAN.md

## SF.AI — خطة التنفيذ الكاملة على مراحل

هذه الخطة الرسمية لمشروع SF.AI. كل مرحلة محددة الأهداف والمخرجات وشروط النجاح. الانتقال بين المراحل يتطلب إذنًا صريحًا من المستخدم.

---

## المبدأ الأعلى للخطة

> **نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.**

- **الهدف العام النهائي:** بناء **نموذج لغوي سيادي مولّد** لـ SF.AI، يبدأ من الصفر، يفهم العربية الفصحى واللهجة السعودية، ويتحوّل تدريجيًا من routing/rules إلى توليد لغوي حقيقي داخل الشات.
- **تصحيح إلزامي:** Sovereign Practical Acceleration تعني تسريع الهندسة
  والتشخيص والتدريب فقط، ولا تعني Qwen/open-weight/pretrained runtime.
  أي Open-Weight Lane أو Qwen roadmap ملغى وغير معتمد.
- **الحالة الحالية:** الحوار العام يعمل الآن كـ rule-based router + templates + composer. هذا ليس LLM بعد.
- **التركيز اللغوي الحالي:** العربية الفصحى + اللهجة السعودية فقط. لا توسيع للهجات أخرى في runtime قبل إتقان هذا المسار.
- **الهدف التالي العملي:** تجهيز البيانات السيادية، تدريب tokenizer من الصفر، تدريب أول LM صغير، ثم ربطه بـ ChatModule بشكل آمن.
- **بقية المجالات:** موجودة skeleton فقط حتى لا تختلط القدرة المستقبلية بالقدرة الفعلية.

## Progressive Scaling Strategy

لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
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
| Phase 27.14 | Sovereign Training Quality Tooling Decision | مكتملة؛ أدوات جودة محلية دون تدريب |
| Phase 27.15 | Social/Lexical Curriculum + No-Repeat Decoding | مكتملة؛ eval تحسن وcanary صارم يحجب |
| Phase 27.16 | Prompt-to-Answer Objective Repair | مكتملة؛ sample isolation أضيف وruntime محظور |
| Phase 27.17 | Prompt-to-Answer Micro-Probe | مكتملة؛ 27/32 breakthrough وruntime محظور |
| Phase 27.18 | Tokenization/Decoding Hygiene Repair | مكتملة؛ blockers محددة وruntime محظور |
| Phase 27.19 | Hygiene Repair Corpus/Probe | مكتملة؛ أمثلة repair وحدها لم تكف |
| Phase 27.20 | Tokenizer/Protected-Phrase Strategy | مكتملة؛ دعم protected phrases جاهز لـ tokenizer v3 |
| Phase 27.21 | Tokenizer v3 Protected-Phrase Micro-Probe | مكتملة؛ tokenizer نجح وmicro-probe فشل 25/32 |
| Phase 27.22 | Spacing/Boundary Loss Repair | مكتملة جزئيًا؛ micro-probe تحسن إلى 29/32 |
| Phase 27.23 | Semantic/Lexical Confusion Repair | مكتملة جزئيًا؛ micro-probe تحسن إلى 30/32 |
| Phase 27.24 | Minimal Lexical Stabilization | مكتملة؛ micro-probe وصل إلى 32/32 |
| Phase 27.25 | Held-out Generation Quality Canary | مكتملة؛ فشل held-out `8/16` وruntime محظور |
| Phase 27.26 | Held-out Objective Repair | مكتملة؛ `9/16` وruntime محظور |
| Phase 27.27 | Broader Held-out Repair | مكتملة؛ old held-out `16/16`, shadow `9/16` |
| Phase 27.28 | Intent-Conditioned Repair | مكتملة؛ shadow `12/16` |
| Phase 27.29 | Topic-Conditioned Definition Repair | مكتملة؛ حُجبت بسبب shadow leakage |
| Phase 27.30 | Fresh Mixed Shadow Canary | مكتملة؛ فشل `16/18` وruntime محظور |
| Phase 27.31 | Natural Intent/Topic Dataset | مكتملة جزئيًا؛ natural shadow `20/20` وruntime محظور |
| Phase 27.32 | Balanced Natural Calibration | مكتملة جزئيًا؛ calibration `12/12` وruntime محظور |
| Phase 27.33 | Advice + Micro Stabilization | مكتملة؛ كل بوابات التوليد المحلية مرّت، جاهزة لتصميم guarded trial |
| Phase 27.34 | Guarded Runtime Trial | مكتملة؛ request-scoped UI generator trial مرّ `9/9` |
| Phase 27.35 | Live UI Trial Observations | مكتملة؛ live server UI/API trial مرّ `10/10` |
| Phase 27.36 | Live UI Triage | مكتملة؛ quality-floor active وtriage مرّ `27/27` |
| Phase 27.37 | Supported Topic Expansion | مكتملة؛ `الصبر` فُتح خلف semantic guard ومرّ `21/21` |
| Phase 27.38 | Targeted Topic Curriculum/Probe | مكتملة جزئيًا؛ `6/20` ولا runtime switch |
| Phase 27.39 | Topic-Isolation Repair | مكتملة جزئيًا؛ `10/24` ولا runtime switch |
| Phase 27.40 | Tokenizer/Context Repair | مكتملة؛ `24/24` والمرشح فُتح لاحقًا في trial محروس |
| Phase 27.41 | Guarded Runtime Switch | مكتملة؛ HTTP gate مرّ `22/22` و`generator_trial` يستخدم `sf_10m_phase27_40` |
| Phase 27.42 | Live UI Broader Probes | مكتملة؛ broader gate مرّ `29/29` وحجب الردود غير المطابقة |
| Phase 27.43 | Guarded Data-Backed Expansion | مكتملة جزئيًا؛ weak-lane candidate مرّ `10/16` ولا runtime switch |
| Phase 27.44 | Tokenizer/Curriculum Repair | مكتملة جزئيًا؛ tokenizer v6 وweak-lane `6/6` لكن الإجمالي `11/16` |
| Phase 27.45 | Semantic Topic Balance Repair | مكتملة جزئيًا؛ `9/16` ولا runtime switch |
| Phase 27.46 | Core Dialogue Stabilization | مكتملة جزئيًا؛ `14/16` ولا runtime switch |
| Phase 27.47 | New Topic Conditioning Repair | مكتملة؛ offline gate مرّ `16/16` |
| Phase 27.48 | Guarded Runtime Switch for Phase 27.47 | مكتملة؛ live API gate مرّ `19/19` و`generator_trial` يستخدم `sf_10m_phase27_47` |
| Phase 27.49 | Broader Live UI/API Probes | مكتملة؛ live API gate مرّ `33/33` وأصلح كشف النصيحة السعودية |
| Phase 27.50 | Generator-Only UI Lab Mode | مكتملة؛ `/chat/message` بلا قوالب، gate `7/7` |
| Phase 27.51 | Open-Dialogue Generalization Audit | مكتملة؛ فشل مفيد، live `3/22`, raw natural `1/20`, التدريب مطلوب |
| Phase 27.52 | Natural Dialogue Objective Repair | مكتملة جزئيًا؛ دبل تدريب `9200` خطوة، raw natural `5/20`, لا runtime switch |
| Phase 27.53 | Natural Dialogue Diversity Expansion | مكتملة جزئيًا؛ `10,540` زوجًا و`18,000` خطوة، raw natural `2/36`, لا runtime switch |
| Phase 27.54 | Capacity/Objectivity Gate | مكتملة؛ التكبير الكامل ممنوع، micro-probe تشخيصي فقط في Phase 27.55 |
| Phase 27.55 | Controlled SF-50M Diagnostic Micro-Probe | مكتملة؛ `SF-10M=3/20`, `SF-50M=4/20`, السعة وحدها غير كافية |
| Phase 27.56 | Objective/Format/Tokenizer Diagnosis | مكتملة؛ strict `4/20` وrelaxed `9/20`; إصلاح tokenizer/eval/format قبل التدريب |
| Phase 27.57 | Tokenizer/Eval/Format Repair Pack | مكتملة؛ `18` عبارة محمية، تغطية `9/9`, semantic alignment جاهز |
| Phase 27.58 | Tokenizer v7 Bounded Alignment Probe | مكتملة كتجربة؛ tokenizer نجح، probe فشل `4/15`, runtime محجوب |
| Phase 27.59 | Bounded Alignment Repair | مكتملة؛ repair محدود نجح `15/15`, runtime محجوب بانتظار canary أوسع |
| Phase 27.60 | Broader Natural-Dialogue Canary | مكتملة كتقييم؛ canary أوسع فشل `12/30`, runtime محجوب |
| Phase 27.61 | Broader Generalization Repair | مكتملة كتدريب repair؛ تحسن إلى `18/30`, runtime محجوب |
| Phase 27.62 | Family Balance Repair | مكتملة كتجربة فاشلة؛ تراجع إلى `10/30` بسبب ترتيب curriculum الكتلي |
| Phase 27.63 | Interleaved Family Curriculum | مكتملة بتحسن قوي؛ canary `26/30`, runtime محجوب |
| Phase 27.64 | Topic Lexical/Tokenizer Inspection | مكتملة كفحص؛ tokenizer v8 مطلوب لحماية `التعاون/الاحترام` |
| Phase 27.65 | Tokenizer v8 Topic Probe | مكتملة؛ tokenizer v8 نجح `8/8` topic terms, لا LM training |
| Phase 27.66 | V8 Bounded Topic Repair | مكتملة؛ LM repair محدود على tokenizer v8 نجح broader canary `30/30`, runtime محجوب |
| Phase 27.67 | Fresh Shadow Canary | مكتملة كتقييم؛ فشل `30/50`, runtime محجوب |
| Phase 27.68 | Shadow Failure Repair | مكتملة؛ known shadow `50/50` وregression `30/30`, runtime محجوب |
| Phase 27.69 | New Fresh Shadow Canary | مكتملة كتقييم؛ strong `56/60`, runtime محجوب |
| Phase 27.70 | Open-Social Repair | مكتملة كتجربة فاشلة؛ patch/fine-tune لم يتجاوز baseline، runtime محجوب |
| Phase 27.71 | Candidate Selection and Stability Strategy | مكتملة كتقييم؛ أفضل مرشح `phase27_68` بنتيجة `136/140`, runtime محجوب |
| Phase 27.72 | Stability-First Micro Repair | مكتملة بتحسن غير كاف؛ `138/140`, runtime محجوب |
| Phase 27.73 | Open-Social Failure Inspection | مكتملة كفحص وحارس؛ بقي semantic collapse، runtime محجوب |
| Phase 27.74 | Open-Social Semantic-Collapse Repair | فشلت كتدريب تشغيل؛ `56/60`, `49/50`, `30/30`, runtime محجوب |
| Phase 27.75 | Open-Social Strategy Inspection | مكتملة كفحص tokenizer/strategy؛ tokenizer v9 مطلوب |
| Phase 27.76 | Tokenizer v9 Open-Social Boundary Probe | مكتملة بنجاح tokenizer-only؛ LM repair مسموح تاليًا |
| Phase 27.77 | V9 Bounded Open-Social LM Repair | فشلت كتوليد؛ `54/60`, `45/50`, `30/30`, runtime محجوب |
| Phase 27.78 | Engineering Root Cause Gate | مكتملة؛ `PHASE27_78_ENGINEERING_DECISION`, لا تدريب ولا runtime ولا SF-50M |
| Phase 27.79 | Objective/Curriculum/Decoding Repair Design | مكتملة؛ `PHASE27_79_REPAIR_DESIGN_DECISION`, لا تدريب ولا runtime ولا SF-50M |
| Phase 27.80 | Repair Gate Encoding and Dry-Run Validation | مكتملة؛ gates مرّت بعد remediation، لا تدريب |
| Phase 27.81 | Balanced Family Pack Authoring | مكتملة؛ 2500 سجل gold متوازن، corpus=8443 |
| Phase 27.82 | Family-conditioned SF-10M Repair Training Decision | مكتملة؛ تسمح فقط بتدريب 27.83 المقيّد، لا runtime ولا SF-50M |
| Phase 27.83 | Family-conditioned SF-10M Bounded Repair Training | مكتملة؛ تدريب تم لكن runtime محجوب، best fresh shadow 11/60 |
| Phase 27.84 | Objective/Curriculum Failure Diagnosis | مكتملة؛ family signal missing في نص التدريب، لا تدريب |
| Scaling Mandate | Auto-Advance Scaling Mandate | معتمد؛ عند نجاح gate ننتقل للحجم التالي تلقائيًا حتى `SF-1B+` |
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
- SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+.
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

### Sovereign Practical Acceleration Strategy v2

من هذه النقطة فصاعدًا، يعتمد SF.AI مسار **تسريع سيادي عملي v2**: لا نعيد
اختراع الأدوات الرياضية والهندسية العامة من الصفر، لكن لا نستخدم أي عقل
جاهز أو corpus خارجي أو tokenizer جاهز.

السيادة تبقى كاملة على:

- `corpus`.
- `tokenizer`.
- `behavior`.
- `runtime`.
- `alignment`.
- `evaluation`.
- سلوك الحوار الفصيح والسعودي.

المسموح لتسريع الهندسة:

- PyTorch.
- AMP / mixed precision.
- TensorBoard محلي أو logs محلية.
- schedulers.
- standard Transformer engineering.
- experiment tracking محلي.
- advanced decoding.
- repetition control.
- curriculum tooling.
- held-out canary.
- shadow canary.
- family-conditioned dialogue.
- contrastive evaluation.
- semantic routing diagnostics.
- objective tracing.
- anti-collapse diagnostics.
- local RLHF-lite / DPO / ORPO / preference optimization.
- LoRA / QLoRA فوق أوزان SF.AI فقط.
- retrieval memory tooling.
- local vector retrieval.
- dialogue family balancing.
- EOS boundary tooling.
- checkpoint selector.
- tokenizer boundary audit.

الممنوع:

- pretrained weights.
- pretrained vocab.
- pretrained tokenizer merges.
- external dialogue datasets.
- hidden hosted APIs.
- external reasoning services.
- project-workflow dialogue contamination.
- fake benchmark inflation.
- template masking لإخفاء ضعف المولد.

القاعدة التنفيذية: لا تكبير نموذج قبل فهم limit الحالي. قبل أي تدريب جديد
يجب تنفيذ `ENGINEERING_ROOT_CAUSE_GATE` وإصدار
`PHASE27_78_ENGINEERING_DECISION` يزن capacity/objective/curriculum/
tokenizer/decoding/family mixing/memorization/weak generalization/EOS/
repetition/semantic routing. قبل أي Gate إلى
`SF-50M` يجب إصلاح وفهم: tokenizer, EOS, generalization,
dialogue-family balance, decoding, clean-stop, وopen_social stability.
ولا يعتمد القرار على `loss` وحدها؛ معيار النجاح هو held-out dialogue
quality, open_social stability, semantic correctness, clean-stop, وruntime
usability.

قاعدة runtime الرسمية:

```text
NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS
```

### Auto-Advance Scaling Mandate

سامي فوّض الوكيل رسميًا: عندما تنجح بوابة الحجم التالي، لا ينتظر الوكيل
موافقة جديدة، بل ينتقل إلى الحجم التالي في السلم حتى الوصول إلى `SF-1B+`.

السلم:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

هذا التفويض لا يسمح بالتكبير الأعمى:

- إذا فشل root-cause gate، لا تدريب أكبر.
- إذا كان السبب objective/curriculum/decoding/family balance، لا تكبير.
- إذا لم تنجح held-out/shadow canaries، لا runtime ولا تكبير.
- إذا لم تكن الموارد جاهزة، لا تكبير.
- إذا احتاجت الخطوة pretrained أو data خارجية، تُرفض.

`M100` في أمر سامي يعني مستوى `SF-100M-class`; التنفيذ الحالي يستخدم
`SF-120M` كمستوى معماري مسجل ما لم يصدر تقرير معماري يعتمد `SF-100M`
حرفيًا.

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
نفّذ Phase 27.14: تثبيت قرار أدوات جودة التدريب السيادية قبل semantic/lexical
repair. لا يبدأ `SF-50M` ولا Phase 28.

---

## Phase 27.14 — Sovereign Training Quality Tooling Decision

### الهدف
تحويل قائمة الأدوات المسموحة إلى سياسة تنفيذ رسمية قابلة للاختبار، بدون تدريب
جديد وبدون تفعيل runtime.

### نتيجة التنفيذ

اكتملت Phase 27.14 بقرار:

```text
COMPLETED_TOOLING_ADOPTION_DECISION_NO_TRAINING
```

الأدوات المعتمدة:

- Assistant EOS / stop boundary.
- Sequence packing with boundaries.
- Local experiment tracker.
- Data quality scanner.
- Curriculum sampler.
- No-repeat decoding controls.
- Gold-only micro probes.
- Checkpoint selector.
- Local JSON/JSONL logs.
- Tokenizer boundary audit.

ما أضيف:

- `sf_ai/training/experiment_tracker.py`
- `scripts/phase27_14_quality_tooling.py`
- `make phase27-quality-tooling`
- `docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md`
- `artifacts/reports/phase27_14_quality_tooling_decision_report.json`
- `artifacts/reports/experiment_registry.jsonl`

### قرار الحجب

```text
runtime_generator_enabled = false
training_started         = false
start_sf50m              = blocked
start_phase28            = blocked
```

### بعد المرحلة
نفّذ Phase 27.15: targeted social/lexical curriculum + decoder no-repeat controls
لـ `SF-10M`. لا يبدأ `SF-50M` ولا Phase 28.

---

## Phase 27.15 — Social/Lexical Curriculum + No-Repeat Decoding

### الهدف
إصلاح جزء من مشاكل الرد الاجتماعي والكسور اللفظية عبر بيانات gold موجهة
وقيود decoding محلية، ثم قياس صارم لا يقبل النص العربي الشكلي.

### نتيجة التنفيذ

اكتملت Phase 27.15 بقرار:

```text
COMPLETED_EVAL_IMPROVED_STRICT_GENERATION_BLOCKED
```

ما تحقق:

- أضيف no-repeat decoding:
  - `no_repeat_ngram_size=3`
  - `repetition_penalty=1.08`
- أضيفت 400 عينة gold:
  - `200` فصحى.
  - `200` سعودي.
  - حوار يومي طبيعي فقط.
- corpus أصبح:

```text
total_records  = 5943
training_ready = 5943
issues         = 0
```

- دُرّب `SF-10M v0.10`.
- أفضل eval:

```text
checkpoint = sf-10m-step6000
loss       = 3.0452
perplexity = 21.01
```

- تم تشديد `generation_quality_v1` بإضافة required semantic terms لكل prompt.
- بعد التشديد:

```text
passed          = 0/10
runtime_allowed = false
```

### التشخيص

البيانات والـ decoding حسّنا loss، لكن النموذج لا يربط prompt بالجواب الصحيح
بشكل كافٍ. المشكلة التالية ليست "زيادة بيانات" فقط، بل objective/conditioning
يربط السؤال بالرد.

### artifacts

- [PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md](./PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md)
- `artifacts/reports/sf_10m_v0_10_social_lexical_curriculum_report.json`
- `artifacts/reports/generation_quality_v1_v0_10_strict_report.json`

### بعد المرحلة
نفّذ Phase 27.16: prompt-to-answer conditioning/objective repair قبل أي بيانات
إضافية كبيرة أو scaling.

---

## Phase 27.16 — Prompt-to-Answer Objective Repair

### الهدف
إصلاح خلط العينات داخل training context قبل أي تكبير. المشكلة بعد Phase 27.15
ليست نقص بيانات فقط، بل أن النموذج يتعلم stream لغويًا ولا يربط السؤال بجواب
دقيق بما يكفي.

### نتيجة التنفيذ

اكتملت Phase 27.16 بقرار:

```text
COMPLETED_OBJECTIVE_REPAIR_RUNTIME_BLOCKED
```

ما تحقق:

- أضيف `--packing-mode` إلى `train_tiny_lm` و`evaluate_tiny_lm`.
- الوضع الجديد `sample_isolated` يمنع عبور نافذة التدريب من عينة حوار إلى أخرى.
- أضيفت اختبارات تثبت أن العزل لا يخلط حوارين داخل batch واحد.
- دُرّب `SF-10M v0.11` على:
  - `stream_format=dialogue`
  - `loss_scope=assistant`
  - `packing_mode=sample_isolated`
  - `steps=6000`

أفضل eval:

```text
checkpoint = sf-10m-step6000
loss       = 4.0573
perplexity = 57.82
```

canary:

```text
step2000 = 2/10, runtime_allowed=false
step6000 = 0/10, runtime_allowed=false
```

### التشخيص

العزل الهندسي صحيح، لكنه وحده لا يكفي. `v0.11` أسوأ رقميًا من `v0.10`
رغم أنه أنظف من ناحية objective. لا يتم تفعيل النموذج ولا تكبيره.

### artifacts

- [PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md](./PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md)
- `artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json`
- `artifacts/reports/generation_quality_v1_v0_11_step2000_report.json`
- `artifacts/reports/generation_quality_v1_v0_11_step6000_report.json`

### بعد المرحلة
نفّذ Phase 27.17: targeted micro-probe لأزواج سؤال/جواب قصيرة مع شرط
exact/semantic match قبل أي تدريب واسع أو `SF-50M`.

---

## Phase 27.17 — Prompt-to-Answer Micro-Probe

### الهدف
اختبار قدرة `SF-10M` على تعلم أزواج سؤال/جواب قصيرة ومحددة، بدل قياس
نص عربي عام. هذا probe داخلي ولا يضيف corpus عامة.

### نتيجة التنفيذ

اكتملت Phase 27.17 بقرار:

```text
FAILED_PROMPT_ANSWER_MICRO_PROBE_BLOCK_RUNTIME
```

ما تحقق:

- أضيف `scripts/phase27_17_prompt_answer_micro_probe.py`.
- أضيف `make phase27-prompt-answer-probe`.
- شُغّل probe من `32` زوجًا:
  - `16` فصحى.
  - `16` سعودي.
- التدريب بقي سياديًا:
  - `loss_scope=assistant`
  - `packing_mode=sample_isolated`
  - `steps=2400`

النتيجة:

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 29/32
guard_passed = 29/32
```

### التشخيص

هذا أول proof واضح أن النموذج يستطيع ربط سؤال بجواب داخل micro-context.
لكن الفشل المتبقي ليس بسيطًا للواجهة؛ توجد كسور لفظية/حروفية:

```text
وعليكأهلًا السم، أهلًا بك.
التعاعاون يعني أن ننجز معًا بدل الانفراد.
هوش تحتاجججبعيادة.
```

### القرار

- لا runtime.
- لا `SF-50M`.
- لا Phase 28.
- التالي Phase 27.18: tokenization/decoding hygiene repair.

### artifacts

- [PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md](./PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md)
- `artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json`
- `artifacts/samples/phase27_17_prompt_answer_micro_probe_generations.md`

### بعد المرحلة
نفّذ Phase 27.18 لإصلاح الكسور اللفظية قبل أي تدريب واسع.

---

## Phase 27.18 — Tokenization/Decoding Hygiene Repair

### الهدف
تحويل فشل Phase 27.17 من ملاحظات يدوية إلى بوابة قياس واضحة: ما الكلمات
التي تتجزأ بقوة؟ وهل الحارس يمنع الكسور المرصودة؟

### نتيجة التنفيذ

اكتملت Phase 27.18 بقرار:

```text
COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS
```

ما تحقق:

- أضيف ملف مصطلحات hygiene:
  - `resources/tokenization/hygiene_terms_phase27_18.txt`
- أضيف audit:
  - `scripts/phase27_18_hygiene_audit.py`
  - `make phase27-hygiene-audit`
- أضيفت كسور Phase 27.17 إلى `GenerationGuard`.

نتيجة audit:

```text
terms_total             = 26
average_pieces          = 3.5385
aggressive_split_terms  = 5
roundtrip_failures      = 0
uncovered_bad_fragments = 0
```

المصطلحات الخمسة التي تتجزأ بقوة:

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
```

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.19: hygiene repair corpus/probe موجه لهذه المصطلحات.

### artifacts

- [PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md](./PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md)
- `artifacts/reports/phase27_18_tokenization_hygiene_report.json`

---

## Phase 27.19 — Hygiene Repair Corpus/Probe

### الهدف
اختبار هل تكفي أمثلة repair مركزة حول عبارات Phase 27.18 الخمس لعلاج
كسور micro-probe بدون تغيير tokenizer أو decoding.

### نتيجة التنفيذ

اكتملت Phase 27.19 بقرار:

```text
FAILED_HYGIENE_REPAIR_PROBE_BLOCK_RUNTIME
```

ما تحقق:

- أضيف `scripts/phase27_19_hygiene_repair_probe.py`.
- أضيف `make phase27-hygiene-repair-probe`.
- شُغّل تدريب داخلي:
  - `32` زوجًا أساسيًا.
  - `20` زوج repair.
  - `52` مثال تدريب إجمالًا.

النتيجة:

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 28/32
guard_passed = 29/32
```

### التشخيص

الفرضية التي اختبرناها فشلت: زيادة أمثلة repair وحدها لا تكفي. بعض الردود
ما زالت تخلط بين عبارات أو تكسر كلمات عالية التجزئة.

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.20: tokenizer/protected-phrase strategy.

### artifacts

- [PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md](./PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md)
- `artifacts/reports/phase27_19_hygiene_repair_probe_report.json`
- `artifacts/samples/phase27_19_hygiene_repair_probe_generations.md`

---

## Phase 27.20 — Tokenizer/Protected-Phrase Strategy

### الهدف

تحويل تشخيص Phase 27.18/27.19 إلى دعم حقيقي داخل tokenizer:

- حماية العبارات الخمس عالية التجزئة.
- منع كسرها بشكل عدواني في tokenizer v3 القادم.
- عدم تفعيل runtime أو تكبير النموذج قبل micro-probe جديد.

### نتيجة التنفيذ

اكتملت Phase 27.20 بقرار:

```text
COMPLETED_PROTECTED_PHRASE_STRATEGY_READY_FOR_TOKENIZER_V3
```

ما تحقق:

- أضيف `protected_terms` إلى `TokenizerConfig`.
- صار `BPETokenizer` يحفظ protected phrases في `meta.json`.
- أضيف ملف:
  - `resources/tokenization/protected_phrases_phase27_20.txt`
- أضيف:
  - `scripts/phase27_20_tokenizer_strategy.py`
  - `make phase27-tokenizer-strategy`

### العبارات المحمية

```text
وعليكم السلام
نفسًا هادئًا
نشتغل سوا
القراءة تفيد
تقدّر الناس
```

### القياس

```text
tokenizer v2 max_pieces = 8
protected strategy max_pieces = 1
all_roundtrip_ok = true
```

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.21: tokenizer v3 protected-phrase retrain + micro-probe.

### artifacts

- [PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md](./PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md)
- `artifacts/reports/phase27_20_tokenizer_strategy_report.json`

---

## Phase 27.21 — Tokenizer v3 Protected-Phrase Micro-Probe

### الهدف

تدريب tokenizer v3 بالعبارات المحمية، ثم إعادة micro-probe لمعرفة هل
تحسن تمثيل العبارات يكفي لفتح طريق المولد.

### نتيجة التنفيذ

اكتملت Phase 27.21 بقرار:

```text
FAILED_TOKENIZER_V3_MICRO_PROBE_BLOCK_RUNTIME
```

ما تحقق:

- tokenizer v3 سيادي: `artifacts/tokenizers/sf_bpe/v3`.
- `vocab_size=4706`, `merges=4648`, `sf_origin=true`.
- protected phrases: `max_pieces=1`, `all_roundtrip_ok=true`.
- micro-probe: `passed=25/32`, `exact_clean=26/32`, `semantic=30/32`.

### التشخيص

المشكلة لم تعد فقط protected phrases. الفشل الحالي spacing/boundary:

```text
سواونخفف
تفيدوتوسع
هادئًاوابدأ
```

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.22: spacing/boundary loss repair.

### artifacts

- [PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md](./PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md)
- `artifacts/tokenizers/sf_bpe/v3/`
- `artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json`
- `artifacts/samples/phase27_21_tokenizer_v3_micro_probe_generations.md`

---

## Phase 27.22 — Spacing/Boundary Loss Repair

### الهدف

علاج لصق الكلمات بعد protected phrases وإزالة false positive في الحارس قبل
أي تدريب جديد.

### نتيجة التنفيذ

اكتملت Phase 27.22 بقرار:

```text
PARTIAL_SPACING_BOUNDARY_REPAIR_BLOCK_RUNTIME
```

ما تحقق:

- `BPETokenizer.decode` يضيف word boundary بعد protected phrase token.
- `GenerationGuard` لم يعد يحجب tanween صحيح مثل `وقتًا`.
- أعيد تقييم checkpoint Phase 27.21 نفسه دون تدريب جديد.

النتيجة:

```text
passed       = 29/32
exact_clean  = 29/32
semantic     = 30/32
guard_passed = 32/32
glued_left   = 0
```

### التشخيص

إصلاح spacing نجح. المتبقي semantic/lexical confusion:

- `التعانشتغل` بدل جواب فصيح عن التعاون.
- `الاحتردم` بدل `الاحترام`.
- جواب القراءة السعودي لا يذكر `كلماتك`.

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.23: semantic/lexical confusion repair.

### artifacts

- [PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md](./PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md)
- `artifacts/reports/phase27_22_spacing_boundary_repair_report.json`
- `artifacts/samples/phase27_22_spacing_boundary_repair_generations.md`

---

## Phase 27.23 — Semantic/Lexical Confusion Repair

### الهدف

علاج إخفاقات Phase 27.22 الدلالية/اللفظية المتبقية دون تفعيل runtime ودون
تكبير النموذج.

### نتيجة التنفيذ

اكتملت Phase 27.23 بقرار:

```text
PARTIAL_SEMANTIC_LEXICAL_REPAIR_BLOCK_RUNTIME
```

ما تحقق:

- جُرّبت محاولة tokenizer v4 أوسع ورُفضت لأنها سببت answer collapse.
- اعتُمد tokenizer v3 لأنه وصل سابقًا إلى `29/32`.
- أضيف training repair متوازن: قاعدة 32 مكررة + أمثلة contrastive محدودة.

النتيجة:

```text
passed       = 30/32
exact_clean  = 30/32
semantic     = 30/32
guard_passed = 31/32
```

### التشخيص

تحسن `القراءة وش تفيد`، لكن بقي lexical instability في الفصحى:

- `التعاون`
- `الاحترام`

### القرار

- لا runtime.
- لا `SF-50M`.
- التالي Phase 27.24: minimal lexical stabilization.

### artifacts

- [PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md](./PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md)
- `artifacts/reports/phase27_23_semantic_lexical_repair_report.json`
- `artifacts/samples/phase27_23_semantic_lexical_repair_generations.md`

---

## Phase 27.24 — Minimal Lexical Stabilization

### الهدف

تثبيت آخر كلمتين فصيحتين فشلتا في Phase 27.23:

- `التعاون`
- `الاحترام`

دون توسعة corpus عام ودون تكبير النموذج.

### نتيجة التنفيذ

اكتملت Phase 27.24 بقرار:

```text
PASSED_MINIMAL_LEXICAL_STABILIZATION_HOLD_RUNTIME_FOR_CANARY
```

ما تحقق:

- أضيف `artifacts/tokenizers/sf_bpe/v4_min_lexical`.
- الحماية اقتصرت على عبارات Phase 27.20 الخمس + `التعاون` + `الاحترام`.
- دُرّب micro-probe داخلي متوازن.

النتيجة:

```text
passed       = 32/32
exact_clean  = 32/32
semantic     = 32/32
guard_passed = 32/32
```

### القرار

- لا runtime بعد.
- لا `SF-50M`.
- التالي Phase 27.25: held-out generation-quality canary.

### artifacts

- [PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md](./PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md)
- `artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json`
- `artifacts/samples/phase27_24_minimal_lexical_stabilization_generations.md`
- `artifacts/tokenizers/sf_bpe/v4_min_lexical/`

---

## Phase 27.25 — Held-out Generation Quality Canary

### الهدف

اختبار checkpoint Phase 27.24 على أسئلة جديدة غير موجودة في micro-probe
الأصلي، للتأكد من أن نجاح `32/32` ليس حفظًا ضيقًا فقط.

لا تدريب جديد في هذه المرحلة.

### نتيجة التنفيذ

اكتملت Phase 27.25 بقرار:

```text
FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME
```

النتيجة:

```text
passed       = 8/16
semantic     = 8/16
guard_passed = 15/16
```

نجح المولد في عائلة التعريفات القريبة مثل `التعاون` و`الاحترام`
و`القراءة`، وفشل في تعميم التحية الفصيحة والنصيحة والتخطيط والدعم.

### القرار

- لا runtime.
- لا تجربة محدودة في الواجهة.
- لا `SF-50M`.
- التالي Phase 27.26: held-out objective repair and generalization training.

### artifacts

- [PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md](./PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md)
- `artifacts/reports/phase27_25_heldout_generation_canary_report.json`
- `artifacts/samples/phase27_25_heldout_generation_canary_generations.md`

---

## Phase 27.26–27.30 — Repair Series Toward Runtime

### الهدف

علاج فشل Phase 27.25 تدريجيًا دون تكبير النموذج ودون فتح الواجهة قبل
fresh canary نظيف.

### نتيجة التنفيذ

```text
Phase 27.26 = held-out 9/16, micro 32/32
Phase 27.27 = old held-out 16/16, shadow 9/16
Phase 27.28 = intent-conditioned shadow 12/16
Phase 27.29 = topic-conditioned definitions passed, but blocked by shadow leakage
Phase 27.30 = fresh mixed shadow 16/18
```

### القرار

- لا runtime.
- لا تجربة محدودة في الواجهة.
- لا `SF-50M`.
- التالي Phase 27.31: broader natural intent/topic dataset.

### artifacts

- [PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md](./PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md)
- `artifacts/reports/phase27_26_heldout_objective_repair_report.json`
- `artifacts/reports/phase27_27_broader_heldout_repair_report.json`
- `artifacts/reports/phase27_28_intent_conditioned_repair_report.json`
- `artifacts/reports/phase27_29_topic_conditioned_definition_repair_report.json`
- `artifacts/reports/phase27_30_fresh_mixed_shadow_canary_report.json`

---

## Phase 27.31–27.33 — Natural Generation Gate Series

### الهدف

إكمال فجوات Phase 27.30 بدون فتح runtime مبكرًا:

- توسيع الشكر وسؤال الحال الطبيعي.
- موازنة intent/topic حتى لا تسحب بيانات الشكر بقية المسارات.
- تثبيت advice + micro-probe قبل أي تجربة واجهة.

### نتيجة التنفيذ

```text
Phase 27.31 = natural shadow 20/20, micro 32/32, fresh mixed 15/18
Phase 27.32 = definition 6/6, calibration 12/12, fresh mixed 16/18, micro 29/32
Phase 27.33 = heldout 16/16, shadow 16/16, definition 6/6,
              fresh mixed 18/18, natural 20/20, calibration 12/12,
              advice 4/4, micro 32/32, leakage none
```

### القرار

- `SF-10M` صار جاهزًا لتصميم تجربة runtime محروسة.
- لا تفعيل افتراضي للواجهة بعد.
- لا `SF-50M` ولا Phase 28 قبل نجاح تجربة الواجهة الفعلية.
- التالي Phase 27.34: guarded runtime trial design.

### artifacts

- [PHASE27_31_TO_33_GENERATION_GATE_REPORT.md](./PHASE27_31_TO_33_GENERATION_GATE_REPORT.md)
- `artifacts/reports/phase27_31_natural_intent_topic_dataset_report.json`
- `artifacts/reports/phase27_32_balanced_natural_calibration_report.json`
- `artifacts/reports/phase27_33_advice_micro_stabilization_report.json`

---

## Phase 27.34 — Guarded Runtime Trial

### الهدف

تجربة `SF-10M Phase 27.33` من مسار الواجهة/API نفسه، مع بقاء التفعيل request-scoped وليس افتراضيًا مخفيًا.

### نتيجة التنفيذ

```text
generator_trial=true
candidate_generator = sf_10m_phase27_33
guarded_runtime_trial = 9/9
```

### القرار

- تجربة الواجهة مسموحة الآن عبر زر `مولّد تجريبي`.
- fallback إلى القالب يبقى حاضرًا.
- الهوية والمجالات الحساسة تبقى template/composer.
- لا `SF-50M` ولا Phase 28 قبل ملاحظات واجهة ناجحة.
- التالي Phase 27.35: live UI trial observations.

### artifacts

- [PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md](./PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md)
- `artifacts/reports/phase27_34_guarded_runtime_trial_report.json`
- `artifacts/samples/phase27_34_guarded_runtime_trial_generations.md`

---

## Phase 27.35 — Live UI Trial Observations

### الهدف

اختبار السيرفر الحي على `127.0.0.1:8123` بدل الاكتفاء بمسار داخلي:

- `/ui/chat` يعرض زر `مولّد تجريبي`.
- `/chat/message` يستقبل `generator_trial=true`.
- `sf_10m_phase27_33` يرد في الحالات المناسبة.
- default وsafety controls تبقى template/composer.

### نتيجة التنفيذ

```text
ui_passed = true
cases = 10/10
generator = 7/7
controls = 3/3
```

### القرار

- مسموح لسامي بتجربة المولّد من الواجهة الآن.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.36: collect/triage live UI observations.

### artifacts

- [PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md](./PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md)
- `artifacts/reports/phase27_35_live_ui_trial_observations_report.json`
- `artifacts/samples/phase27_35_live_ui_trial_observations.md`

---

## Phase 27.36 — Live UI Triage

### الهدف

توسيع اختبار الواجهة الحية بعد فتح زر `مولّد تجريبي`، وتصنيف المسارات
المسموحة للمولّد مقابل المسارات التي يجب حجبها بجدار جودة.

### نتيجة التنفيذ

```text
cases = 27/27
generated = 18/18
quality_floor = 5/5
controls = 4/4
```

### القرار

- يستمر زر `مولّد تجريبي`، لكن داخل proven lanes فقط.
- raw `chat.general` وموضوعات التعريف غير المثبتة تُحجب عن المولّد.
- الافتراضي يبقى template.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.37: expand supported generator intents/topics.

### artifacts

- [PHASE27_36_LIVE_UI_TRIAGE_REPORT.md](./PHASE27_36_LIVE_UI_TRIAGE_REPORT.md)
- `artifacts/reports/phase27_36_live_ui_triage_report.json`
- `artifacts/samples/phase27_36_live_ui_triage.md`

---

## Phase 27.37 — Supported Topic Expansion

### الهدف

توسيع نطاقات المولّد بموضوع جديد فقط إذا نجح دلاليًا خلف guard، دون تدريب
جديد ودون فتح `chat.general`.

### نتيجة التنفيذ

```text
cases = 21/21
generated = 10/10
new_topic = 3/3
quality_floor = 5/5
controls = 3/3
```

### القرار

- فُتح موضوع `الصبر` بصيغ مثبتة:
  - `ما معنى الصبر`
  - `الصبر وش يعني`
  - `وش المقصود بالصبر`
- أضيف semantic topic guard لحجب الردود التي لا تحمل معنى الموضوع.
- بقيت `الصداقة` و`الصدق` و`التنظيم` و`الهدوء` محجوبة.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.38: targeted topic curriculum/probe للموضوعات المحجوبة.

### artifacts

- [PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md](./PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md)
- `artifacts/reports/phase27_37_supported_topic_expansion_report.json`
- `artifacts/samples/phase27_37_supported_topic_expansion.md`

---

## Phase 27.38 — Targeted Topic Curriculum/Probe

### الهدف

تدريب probe صغير على موضوعات التعريف المحجوبة (`الصداقة`, `الصدق`,
`التنظيم`, `الهدوء`) دون تكبير النموذج.

### نتيجة التنفيذ

```text
checkpoint = sf-10m-step2400
cases = 6/20
regression = 6/8
new_topic = 0/8
heldout = 0/4
runtime_switch_allowed = false
```

### القرار

- لا نبدّل runtime.
- يبقى زر `مولّد تجريبي` على مرشح Phase 27.33 مع فتح `الصبر` المحروس.
- سبب الحجب: topic collapse نحو `الاحترام` وخسارة `التعاون`/`الصبر` في المرشح.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.39: repair failed targeted topics.

### artifacts

- [PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md](./PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md)
- `artifacts/reports/phase27_38_targeted_topic_curriculum_probe_report.json`
- `artifacts/samples/phase27_38_targeted_topic_curriculum_probe.md`

---

## Phase 27.39 — Topic-Isolation Repair

### الهدف

إصلاح خلط موضوعات التعريف عبر curriculum متوازن يحاسب النموذج على فصل
`التعاون/الصبر/الاحترام/القراءة/الصداقة/الصدق/التنظيم/الهدوء`.

### نتيجة التنفيذ

```text
checkpoint = sf-10m-step6400
cases = 10/24
regression = 4/8
new_topic = 2/8
heldout = 1/4
isolation = 3/4
runtime_switch_allowed = false
```

### القرار

- لا نبدّل runtime.
- يبقى زر `مولّد تجريبي` على مرشح Phase 27.33 مع فتح `الصبر` المحروس.
- سبب الحجب: كسور لفظية في المصطلحات الجديدة وتسرب موضوعي محدود.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.40: tokenizer/context repair for topic isolation.

### artifacts

- [PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md](./PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md)
- `artifacts/reports/phase27_39_topic_isolation_repair_report.json`
- `artifacts/samples/phase27_39_topic_isolation_repair.md`

---

## Phase 27.40 — Tokenizer/Context Repair

### الهدف

حماية مصطلحات التعريف التي تكسرت في Phase 27.39، ثم إعادة probe بميزان
لا يخسر المسارات الاجتماعية.

### نتيجة التنفيذ

```text
tokenizer = artifacts/tokenizers/sf_bpe/v5_topic_terms
max_pieces = 1
checkpoint = sf-10m-step6400
cases = 24/24
regression = 8/8
new_topic = 8/8
heldout = 4/4
isolation = 4/4
runtime_switch_allowed = true
```

### القرار

- لا نبدّل runtime تلقائيًا داخل هذه المرحلة.
- المرشح `sf_10m_phase27_40` جاهز لتصميم فتح محروس.
- لا `SF-50M` ولا Phase 28 حتى ينجح الاختبار الحي.
- التالي Phase 27.41: guarded runtime switch design.

### artifacts

- [PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md](./PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md)
- `artifacts/tokenizers/sf_bpe/v5_topic_terms/`
- `artifacts/reports/phase27_40_tokenizer_context_repair_report.json`
- `artifacts/samples/phase27_40_tokenizer_context_repair.md`

## Phase 27.41 — Guarded Runtime Switch

### الهدف

ربط مرشح Phase 27.40 بمسار الواجهة/API الاختياري فقط، مع بقاء runtime
الافتراضي على القالب الآمن، وإثبات ذلك عبر HTTP حي.

### نتيجة التنفيذ

```text
request_flag = generator_trial=true
candidate_generator = sf_10m_phase27_40
tokenizer = artifacts/tokenizers/sf_bpe/v5_topic_terms
checkpoint = sf-10m-step6400
live_http_cases = 22/22
generated_lanes = 17/17
template_safety_controls = 5/5
runtime_default = template
sf50m_allowed = false
```

### القرار

- الواجهة تستطيع اختبار المولد الحقيقي عند تفعيل زر `مولّد تجريبي`.
- أي prompt خارج المسارات المثبتة يعود إلى القالب/fallback.
- لا تدريب جديد في هذه المرحلة.
- لا `SF-50M` ولا Phase 28 بعد.
- التالي Phase 27.42: live UI observation and broader guarded probes.

### artifacts

- [PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md](./PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md)
- `artifacts/reports/phase27_41_guarded_runtime_switch_report.json`
- `artifacts/samples/phase27_41_guarded_runtime_switch.md`

## Phase 27.42 — Live UI Broader Probes

### الهدف

توسيع اختبار الواجهة/API الحي بعد فتح `sf_10m_phase27_40`، مع إضافة حارس
alignment يمنع الردود غير المطابقة من المرور كمخرجات مولدة.

### نتيجة التنفيذ

```text
request_flag = generator_trial=true
candidate_generator = sf_10m_phase27_40
live_http_cases = 29/29
generated_lanes = 20/20
guarded_fallback_quality_controls = 9/9
runtime_default = template
sf50m_allowed = false
```

### القرار

- تجربة الواجهة أوسع وأكثر أمانًا.
- `ما فائدة القراءة` لم تعد تُحجب كمالية/استثمار.
- `وش اخبارك` و`نظم وقتي` يرجعان للقالب إذا أعطى المولد ردًا غير مطابق.
- لا تدريب جديد ولا تكبير.
- التالي Phase 27.43: guarded data-backed expansion.

### artifacts

- [PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md](./PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md)
- `artifacts/reports/phase27_42_live_ui_broader_probes_report.json`
- `artifacts/samples/phase27_42_live_ui_broader_probes.md`

## Phase 27.43 — Guarded Data-Backed Expansion

### الهدف

تدريب مرشح SF-10M صغير على أمثلة موجهة للمسارات الضعيفة التي كشفها 27.42،
مع عدم تبديل الواجهة إلا إذا اجتاز البوابة كاملة.

### نتيجة التنفيذ

```text
candidate_generator = sf_10m_phase27_43
checkpoint = sf-10m-step4800
cases = 10/16
weak_lane = 4/6
regression = 6/8
new_topic = 0/2
runtime_switch_allowed = false
sf50m_allowed = false
```

### القرار

- لا runtime switch.
- الواجهة تبقى على `sf_10m_phase27_40`.
- `الوفاء/الشجاعة` تحتاج tokenizer/curriculum repair بدل إضافة أمثلة فقط.
- التالي Phase 27.44: tokenizer/curriculum repair for weak-lane stability.

### artifacts

- [PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md](./PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md)
- `artifacts/reports/phase27_43_guarded_data_backed_expansion_report.json`
- `artifacts/samples/phase27_43_guarded_data_backed_expansion.md`

## Phase 27.44–27.48 — Tokenizer/Conditioning Repair and Guarded Switch

### الهدف

إصلاح المسارات الضعيفة بدون تكبير النموذج: tokenizer v6 يحمي العبارات
السعودية والمفاهيم، ثم نواة حوار صغيرة تثبت أن `SF-10M` يستطيع الرد
بشكل مفهوم داخل نطاق ضيق قبل أي توسعة.

### نتيجة التنفيذ

```text
phase27_44 = 11/16, tokenizer v6 max_pieces=1
phase27_45 = 9/16
phase27_46 = 14/16
phase27_47 = 16/16 offline
phase27_48 = 19/19 live API
candidate_generator = sf_10m_phase27_47
runtime_default = template
request_flag = generator_trial=true
sf50m_allowed = false
```

### القرار

- فُتح `sf_10m_phase27_47` فقط عند تفعيل `generator_trial=true`.
- الافتراضي ما زال القالب الآمن.
- لا `SF-50M` ولا Phase 28 قبل Phase 27.49 broader live UI probes.

### artifacts

- [PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md](./PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md)
- `artifacts/reports/phase27_44_tokenizer_curriculum_repair_report.json`
- `artifacts/reports/phase27_47_new_topic_conditioning_repair_report.json`
- `artifacts/reports/phase27_48_guarded_runtime_switch_report.json`

## Phase 27.49 — Broader Live UI/API Probes

### الهدف

توسيع اختبار `generator_trial=true` على السيرفر الحي للتأكد من أن
`sf_10m_phase27_47` لا ينجح فقط في gate صغير، بل يصمد أمام صيغ فصحى وسعودية
أكثر في سؤال الحال، الشكر، النصيحة، التخطيط، الدعم، والتعريفات المثبتة.

### نتيجة التنفيذ

```text
candidate_generator = sf_10m_phase27_47
cases = 33/33
generated_social = 7/7
generated_task = 8/8
generated_definition = 11/11
controls = 7/7
runtime_default = template
sf50m_allowed = false
```

### ملاحظة إصلاح

فشل الاختبار أولًا في `وش تنصحني اسوي` لأنها سقطت إلى `chat.general`.
أضيفت جذور `نصح/تنصح` إلى كشف intent وحارس alignment، ثم مرّت البوابة `33/33`.

### القرار

- يبقى المولد مفتوحًا فقط عند `generator_trial=true`.
- لا `SF-50M` ولا Phase 28.
- التالي Phase 27.50: targeted natural-prompt expansion plan.

### artifacts

- [PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md](./PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md)
- `artifacts/reports/phase27_49_broader_live_ui_probes_report.json`
- `artifacts/samples/phase27_49_broader_live_ui_probes.md`

## Phase 27.50 — Generator-Only UI Lab Mode

### الهدف

تصحيح تجربة الواجهة: لا زر مولّد، لا `generator_trial=false`، ولا قوالب ظاهرة
في `/chat/message`. إذا لم يستطع المولد الرد، يكون الناتج فارغًا مع metadata
صريح بدل إظهار template.

### نتيجة التنفيذ

```text
runtime_default = generator_only_lab
candidate_generator = sf_10m_phase27_47
template_answers_allowed = false
cases = 7/7
```

### القرار

- الواجهة الآن لاختبار المولد فقط.
- `من أنت` و`ما معنى الكرم` لا تعرض قوالب؛ ترجع `generator_blocked` وردًا فارغًا.
- التالي Phase 27.51: targeted natural-prompt expansion plan.

### artifacts

- [PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md](./PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md)
- `artifacts/reports/phase27_50_generator_only_ui_gate_report.json`
- `artifacts/samples/phase27_50_generator_only_ui_gate.md`

---

## Phase 27.51 — Open-Dialogue Generalization Audit

### الهدف
إثبات هل `sf_10m_phase27_47` يستطيع الحوار الطبيعي خارج المسارات المحروسة، أو أنه ما زال يعتمد على memorized lanes وtopic/intent conditioning.

### ما تم
- أضيف `scripts/phase27_51_open_dialogue_generalization_audit.py`.
- أضيف هدف `make phase27-open-dialogue-generalization-audit`.
- شُغّل الاختبار على:
  - live API generator-only.
  - raw checkpoint بلا intent/topic conditioning.
- شملت العينات follow-up, open social, topic discussion, planning, support.

### النتيجة
- الحالة: `FAILED_OPEN_DIALOGUE_GENERALIZATION_AUDIT_TRAINING_REQUIRED`.
- live API: `3/22`.
- raw checkpoint: `3/22`.
- raw natural prompts: `1/20`.

### القرار
لا نعدّ Phase 27.47 حوارًا ذكيًا عامًا. لا `SF-50M` ولا Phase 28.

التالي:

**Phase 27.52 — Natural Dialogue Objective Repair**

الهدف القادم تدريب/إصلاح هدف حواري طبيعي، لا إضافة كلمات مفتاحية ولا توسيع whitelist.

### artifacts
- [PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md](./PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md)
- `artifacts/reports/phase27_51_open_dialogue_generalization_audit.json`
- `artifacts/samples/phase27_51_open_dialogue_generalization_audit.md`

---

## Phase 27.52 — Natural Dialogue Objective Repair

### الهدف
تنفيذ قفزة تدريب آمنة داخل `SF-10M` فقط: دبل خطوات مقارنة بـ Phase 27.47، مع منع تكبير النموذج أو فتح runtime قبل بوابة حوار مفتوح.

### ما تم
- أضيف `scripts/phase27_52_natural_dialogue_objective_repair.py`.
- أضيف `make phase27-natural-dialogue-objective-repair`.
- دُرّب `SF-10M` على `6400` سجل داخلي مبني من `40` زوجًا فريدًا.
- لا intent/topic system lines في التدريب؛ فقط نطاق `فصحى/سعودي` من provenance.
- التدريب: `9200` خطوة، `2.00x` مقارنة بـ Phase 27.47.

### النتيجة
- الحالة: `PARTIAL_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_KEEP_PHASE27_47_RUNTIME`.
- held-out raw natural: `5/20`.
- topic: `3/4`.
- planning: `2/4`.
- followup/open_social/support: `0/4` لكل مسار.

### القرار
لا يتم فتح `sf_10m_phase27_52` في الواجهة. لا `SF-50M` ولا Phase 28.

التالي:

**Phase 27.53 — Natural Dialogue Diversity Expansion**

الهدف القادم زيادة عدد الأزواج الفريدة والتنوع الحواري بدل زيادة الخطوات وحدها.

### artifacts
- [PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md](./PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md)
- `artifacts/reports/phase27_52_natural_dialogue_objective_repair_report.json`
- `artifacts/samples/phase27_52_natural_dialogue_objective_repair.md`
- checkpoint محلي غير مرفوع: `artifacts/eval/phase27_52_natural_dialogue_objective_repair/checkpoints/sf-10m-step9200/state.pt`

---

## Phase 27.53 — Natural Dialogue Diversity Expansion

### الهدف
تنفيذ توسعة كبيرة للحوار الطبيعي العام داخل `SF-10M`: آلاف الأزواج الفريدة بدل تكرار أمثلة قليلة.

### ما تم
- أضيف `scripts/phase27_53_natural_dialogue_diversity_expansion.py`.
- أضيف `make phase27-natural-dialogue-diversity-expansion`.
- وُلد `10,540` سجلًا فريدًا:
  - `5,270` فصحى.
  - `5,270` سعودي.
- السجلات اجتازت governance audit وتستبعد حوار المشروع والتشغيل.
- التدريب: `18,000` خطوة، `batch_size=2`, `seq_len=80`.

### النتيجة
- الحالة: `PARTIAL_NATURAL_DIALOGUE_DIVERSITY_KEEP_PHASE27_47_RUNTIME`.
- held-out raw natural: `2/36`.
- ظهرت مشاكل خلط/fragments رغم توسعة البيانات.

### القرار
لا يتم فتح `sf_10m_phase27_53` في الواجهة. لا Phase 28 ولا تكبير تلقائي.

التالي:

**Phase 27.54 — Capacity/Objectivity Gate**

الهدف القادم تحديد هل الفشل بسبب سعة `SF-10M` أم بسبب الهدف/التوكنة/أسلوب البيانات قبل أي تدريب أكبر.

### artifacts
- [PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md](./PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md)
- `artifacts/reports/phase27_53_natural_dialogue_diversity_expansion_report.json`
- `artifacts/samples/phase27_53_natural_dialogue_diversity_expansion.md`
- checkpoint محلي غير مرفوع: `artifacts/eval/phase27_53_natural_dialogue_diversity_expansion/checkpoints/sf-10m-step18000/state.pt`

---

## Phase 27.54 — Capacity/Objectivity Gate

### الهدف
منع القفز العشوائي إلى حجم أكبر بعد فشل Phase 27.53، وتحديد القرار الرسمي قبل أي `SF-50M`.

### ما تم
- أضيف `scripts/phase27_54_capacity_objectivity_gate.py`.
- أضيف `make phase27-capacity-objectivity-gate`.
- لم يبدأ أي تدريب جديد ولم تُنشأ checkpoints.
- قورنت نتائج Phase 27.51–27.53:
  - Phase 27.51: raw natural `1/20`.
  - Phase 27.52: raw natural `5/20`.
  - Phase 27.53: raw natural `2/36`.

### النتيجة
- الحالة: `COMPLETED_CAPACITY_OBJECTIVITY_GATE_FULL_SCALING_BLOCKED_DIAGNOSTIC_MICRO_PROBE_ALLOWED`.
- زيادة البيانات وحدها لم تساعد داخل `SF-10M`.
- العائق قد يكون سعة أو objective/format/tokenization، لذلك لا يجوز تدريب `SF-50M` كامل كقفزة مباشرة.

### القرار
- لا runtime switch.
- لا `SF-50M` full training.
- لا Phase 28.
- المسموح فقط: Phase 27.55 controlled diagnostic micro-probe يقارن `SF-50M` ضد `SF-10M` بنفس corpus/eval، ولا يفتح runtime إلا بعد gate جديد.

### artifacts
- [PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md](./PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md)
- `artifacts/reports/phase27_54_capacity_objectivity_gate_report.json`

---

## Phase 27.55 — Controlled SF-50M Diagnostic Micro-Probe

### الهدف
اختبار أثر السعة وحدها قبل أي تدريب `SF-50M` كامل، بمقارنة `SF-10M` و`SF-50M` على نفس corpus/eval.

### ما تم
- أضيف `scripts/phase27_55_sf50m_diagnostic_micro_probe.py`.
- أضيف `make phase27-sf50m-diagnostic-micro-probe`.
- دُرّب نموذجان عشوائيان سياديان من الصفر:
  - `SF-10M` baseline.
  - `SF-50M` diagnostic candidate.
- نفس البيانات: `6400` سجل من `40` زوجًا فريدًا.
- نفس التقييم: `20` prompt held-out طبيعي.
- runtime لم يتغير.

### النتيجة
- `SF-10M`: `3/20`.
- `SF-50M`: `4/20`.
- delta: `1`.

### القرار
السعة وحدها لم تثبت أنها تحل الحوار المفتوح. لا runtime switch، لا تدريب `SF-50M` كامل، ولا Phase 28.

التالي:

**Phase 27.56 — objective/format/tokenizer diagnosis before another capacity attempt**

### artifacts
- [PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md](./PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md)
- `artifacts/reports/phase27_55_sf50m_diagnostic_micro_probe_report.json`
- `artifacts/samples/phase27_55_sf50m_diagnostic_micro_probe.md`
- checkpoints محلية غير مرفوعة: `artifacts/eval/phase27_55_sf50m_diagnostic_micro_probe/`

---

## Phase 27.56 — Objective/Format/Tokenizer Diagnosis

### الهدف
تشخيص سبب فشل Phase 27.55 قبل أي تدريب جديد: هل المشكلة في السعة، أو objective/format، أو tokenizer، أو eval.

### ما تم
- أضيف `scripts/phase27_56_objective_format_tokenizer_diagnosis.py`.
- أضيف `make phase27-objective-format-tokenizer-diagnosis`.
- لم يبدأ تدريب جديد.
- قرأ التقرير والعينات من Phase 27.55، ودقق:
  - strict pass.
  - relaxed semantic pass بدون شرط overlap.
  - expected-term failures.
  - response-family confusion.
  - tokenization splits للمصطلحات السعودية/الحوارية.

### النتيجة
- capacity delta من 27.55 بقي `1`.
- `SF-50M strict`: `4/20`.
- `SF-50M relaxed`: `9/20`.
- `expected_terms_missing`: `9`.
- `response_family_confusion`: `11`.
- critical tokenizer splits: `9`.

### القرار
لا runtime switch، لا `SF-50M` كامل، ولا تدريب جديد قبل إصلاح tokenizer/eval/format.

التالي:

**Phase 27.57 — tokenizer/eval/format repair pack**

### artifacts
- [PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md](./PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md)
- `artifacts/reports/phase27_56_objective_format_tokenizer_diagnosis_report.json`

---

## Phase 27.57 — Tokenizer/Eval/Format Repair Pack

### الهدف
إصلاح أدوات التمثيل والقياس قبل أي تدريب جديد، بناءً على تشخيص Phase 27.56.

### ما تم
- أضيف `scripts/phase27_57_tokenizer_eval_format_repair_pack.py`.
- أضيف `make phase27-tokenizer-eval-format-repair-pack`.
- أضيفت عبارات tokenizer محمية:
  - `resources/tokenization/protected_phrases_phase27_57.txt`
- أضيفت قواعد semantic alignment:
  - `resources/evaluation/semantic_alignment_phase27_57.json`
- أضيفت خريطة response families:
  - `resources/dialogue_format/response_families_phase27_57.json`
- حُدث `tokenization_rules.yaml` ليضم protected phrases الجديدة.

### النتيجة
- protected phrases: `18`.
- critical coverage: `9/9`.
- prompt overlap required: `false`.
- forbidden family collapses: `5`.

### القرار
الحزمة جاهزة لتدريب محدود في Phase 27.58، لكنها لا تفتح runtime ولا تسمح بتدريب `SF-50M` كامل.

التالي:

**Phase 27.58 — retrain tokenizer with Phase 27.57 protected phrases and run bounded format/alignment probe**

### artifacts
- [PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md](./PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md)
- `artifacts/reports/phase27_57_tokenizer_eval_format_repair_pack_report.json`

---

## Phase 27.58 — Tokenizer v7 Bounded Alignment Probe

### الهدف
تنفيذ التدريب المحدود الذي سمحت به Phase 27.57: tokenizer جديد يحمي العبارات الحوارية، ثم probe صغير يقيس عائلات الردود بلا فتح واجهة.

### ما تم
- أضيف `scripts/phase27_58_tokenizer_bounded_alignment_probe.py`.
- أضيف `make phase27-tokenizer-bounded-alignment-probe`.
- دُرّب tokenizer v7:
  - `artifacts/tokenizers/sf_bpe/v7_phase27_58`
  - protected terms/phrases: `53`
  - Phase 27.57 phrases بقيت `max_pieces=1`.
- دُرّب probe محدود `SF-10M`:
  - `7600` خطوة.
  - corpus مؤقت داخل `artifacts/eval/phase27_58_tokenizer_bounded_alignment_probe/corpus`.
  - checkpoint داخل `artifacts/eval/phase27_58_tokenizer_bounded_alignment_probe/checkpoints`.
- شُغّل alignment probe على `15` حالة موزعة على:
  - `open_social`
  - `followup`
  - `planning`
  - `support`
  - `topic`

### النتيجة
- pass: `4/15`.
- `open_social`: `0/3`.
- `followup`: `0/3`.
- `planning`: `2/3`.
- `support`: `1/3`.
- `topic`: `1/3`.

### القرار
التوكنة تحسنت، لكن objective/alignment ما زال ضعيفًا. لا runtime switch، لا UI، لا SF-50M، ولا Phase 28.

التالي:

**Phase 27.59 — inspect Phase 27.58 failures and repair bounded alignment**

### artifacts
- [PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md](./PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md)
- `artifacts/reports/phase27_58_tokenizer_bounded_alignment_probe_report.json`
- `artifacts/samples/phase27_58_tokenizer_bounded_alignment_probe.md`

---

## Phase 27.59 — Bounded Alignment Repair

### الهدف
إصلاح فشل Phase 27.58 في عائلات `open_social/followup/topic` بدون فتح runtime وبدون تكبير النموذج.

### ما تم
- أضيف `scripts/phase27_59_bounded_alignment_repair.py`.
- أضيف `make phase27-bounded-alignment-repair`.
- استُخدم tokenizer v7:
  - `artifacts/tokenizers/sf_bpe/v7_phase27_58`
- دُرّب probe محدود `SF-10M`:
  - `6400` خطوة.
  - `24` زوج إصلاح.
  - `2880` سجل تدريب داخل corpus مؤقت.
- أُعيدت بوابة alignment نفسها على `15` حالة.

### النتيجة
- pass: `15/15`.
- `open_social`: `3/3`.
- `followup`: `3/3`.
- `planning`: `3/3`.
- `support`: `3/3`.
- `topic`: `3/3`.

### القرار
هذا نجاح معملي محدود، وليس فتح واجهة. لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.

التالي:

**Phase 27.60 — broader natural-dialogue canary using tokenizer v7 + Phase 27.59 repair**

### artifacts
- [PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md](./PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md)
- `artifacts/reports/phase27_59_bounded_alignment_repair_report.json`
- `artifacts/samples/phase27_59_bounded_alignment_repair.md`

---

## Phase 27.60 — Broader Natural-Dialogue Canary

### الهدف
اختبار checkpoint Phase 27.59 على أسئلة طبيعية أوسع من بوابة `15/15` لمعرفة هل الإصلاح يعمم أم لا.

### ما تم
- أضيف `scripts/phase27_60_broader_natural_dialogue_canary.py`.
- أضيف `make phase27-broader-natural-dialogue-canary`.
- لا تدريب جديد.
- قُيّم checkpoint:
  - `artifacts/eval/phase27_59_bounded_alignment_repair/checkpoints/sf-10m-step6400`
- استخدم canary من `30` حالة موزعة على:
  - `open_social`
  - `followup`
  - `planning`
  - `support`
  - `topic`

### النتيجة
- pass: `12/30`.
- `open_social`: `5/6`.
- `followup`: `3/6`.
- `planning`: `2/6`.
- `support`: `0/6`.
- `topic`: `2/6`.

### القرار
Phase 27.59 نجحت معمليًا لكنها لم تعمم بما يكفي. لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.

التالي:

**Phase 27.61 — inspect Phase 27.60 failures and repair broader natural-dialogue generalization**

### artifacts
- [PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md](./PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md)
- `artifacts/reports/phase27_60_broader_natural_dialogue_canary_report.json`
- `artifacts/samples/phase27_60_broader_natural_dialogue_canary.md`

---

## Phase 27.61 — Broader Generalization Repair

### الهدف
إصلاح الفشل الأكبر في Phase 27.60، خصوصًا `support/topic/planning`، مع الحفاظ على توازن `open_social/followup`.

### ما تم
- أضيف `scripts/phase27_61_broader_generalization_repair.py`.
- أضيف `make phase27-broader-generalization-repair`.
- دُرّب repair محدود `SF-10M` على tokenizer v7:
  - `8200` خطوة.
  - `36` زوج إصلاح.
  - `3960` سجل تدريب مؤقت.
- أُعيد canary Phase 27.60 نفسه.

### النتيجة
- pass: `18/30` بدل `12/30`.
- `planning`: `6/6`.
- `support`: `6/6`.
- `followup`: `3/6`.
- `open_social`: `2/6`.
- `topic`: `1/6`.

### القرار
تحسن جزئي حقيقي، لكنه ليس نجاحًا. لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.

التالي:

**Phase 27.62 — inspect Phase 27.61 family-balance failures and repair open_social/followup/topic**

### artifacts
- [PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md](./PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md)
- `artifacts/reports/phase27_61_broader_generalization_repair_report.json`
- `artifacts/samples/phase27_61_broader_generalization_repair.md`

---

## Phase 27.62 — Family Balance Repair

### الهدف
اختبار ما إذا كان توازن عائلات الرد بالعدد يكفي لإصلاح `open_social/followup/topic`.

### ما تم
- أضيف `scripts/phase27_62_family_balance_repair.py`.
- أضيف `make phase27-family-balance-repair`.
- صُحح معيار `topic` في `resources/evaluation/semantic_alignment_phase27_57.json` ليشمل `التعاون/الصبر/الاحترام`.
- دُرّب repair محدود `SF-10M` على tokenizer v7:
  - `7800` خطوة.
  - `6000` سجل تدريب مؤقت.
  - توازن عددي بين العائلات.

### النتيجة
- pass: `10/30`.
- `open_social`: `6/6`.
- `planning`: `1/6`.
- `support`: `0/6`.
- `topic`: `1/6`.

### القرار
فشل مفيد: ترتيب corpus الكتلي جعل النموذج ينجذب إلى عائلة واحدة. لا runtime switch ولا UI.

التالي:

**Phase 27.63 — interleaved family curriculum**

### artifacts
- [PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md](./PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md)
- `artifacts/reports/phase27_62_family_balance_repair_report.json`
- `artifacts/samples/phase27_62_family_balance_repair.md`

---

## Phase 27.63 — Interleaved Family Curriculum

### الهدف
إصلاح ترتيب curriculum بتداخل round-robin بين عائلات الرد، مع LR أخف وخطوات أقل.

### ما تم
- أضيف `scripts/phase27_63_interleaved_family_curriculum.py`.
- أضيف `make phase27-interleaved-family-curriculum`.
- دُرّب repair محدود `SF-10M` على tokenizer v7:
  - `5600` خطوة.
  - `4500` سجل تدريب مؤقت.
  - ترتيب interleaved بين `followup/open_social/planning/support/topic`.
- أجري decoding sweep لاحقًا وأظهر أن تقليل `max_new_tokens` لا يحل إلا حالة واحدة تقريبًا.

### النتيجة
- pass: `26/30`.
- `open_social`: `6/6`.
- `planning`: `6/6`.
- `support`: `6/6`.
- `followup`: `5/6`.
- `topic`: `3/6`.

### القرار
تحسن قوي، لكنه لا يكفي لفتح الواجهة. الفشل المتبقي يتركز في lexical/tokenization collapse لكلمتي `التعاون` و`الاحترام`.

التالي:

**Phase 27.64 — inspect topic lexical failures and plan tokenizer v8 protection**

### artifacts
- [PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md](./PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md)
- `artifacts/reports/phase27_63_interleaved_family_curriculum_report.json`
- `artifacts/samples/phase27_63_interleaved_family_curriculum.md`

---

## Phase 27.64 — Topic Lexical/Tokenizer Inspection

### الهدف
فحص فشل `topic` المتبقي بعد Phase 27.63 وتحديد هل السبب يحتاج tokenizer v8 قبل أي تدريب LM جديد.

### ما تم
- أضيف `resources/tokenization/protected_phrases_phase27_64.txt`.
- أضيف `scripts/phase27_64_topic_lexical_tokenizer_inspection.py`.
- أضيف `make phase27-topic-lexical-tokenizer-inspection`.
- حُدّث `tokenization_rules.yaml` ليضيف protected pack الجديد ضمن active paths للـ tokenizer القادم.
- حُدّث topic markers في response families لتشمل `التعاون/الصبر/الاحترام`.

### النتيجة
- لا تدريب جديد.
- Phase 27.63 بقي `26/30`.
- `التعاون` في tokenizer v7: `3` pieces, protected=false.
- `الاحترام` في tokenizer v7: `4` pieces, protected=false.
- كلاهما كان single-piece ومحميًا في tokenizer v6.

### القرار
tokenizer v8 مطلوب قبل أي LM repair جديد. لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.

التالي:

**Phase 27.65 — train tokenizer v8 with Phase 27.64 protected topic pack and rerun bounded topic probe**

### artifacts
- [PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md](./PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md)
- `artifacts/reports/phase27_64_topic_lexical_tokenizer_inspection_report.json`
- `resources/tokenization/protected_phrases_phase27_64.txt`

---

## Phase 27.65 — Tokenizer v8 Topic Probe

### الهدف
تدريب tokenizer v8 فقط بحماية Phase 27.64، ثم التأكد من سلامة مصطلحات topic قبل أي LM repair.

### ما تم
- أضيف `scripts/phase27_65_tokenizer_v8_topic_probe.py`.
- أضيف `make phase27-tokenizer-v8-topic-probe`.
- دُرّب tokenizer v8 في `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
- لم يبدأ أي تدريب LM.

### النتيجة
- critical terms: `2/2`.
- topic terms: `8/8`.
- boundary roundtrip: `6/6`.
- `التعاون` و`الاحترام` صارتا single-piece ومحميتين.
- vocab: `4965`.

### القرار
نجح tokenizer v8. المسموح التالي فقط: bounded LM topic repair على v8، ثم broader canary. لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.

التالي:

**Phase 27.66 — bounded LM topic repair on tokenizer v8, then broader canary**

### artifacts
- [PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md](./PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md)
- `artifacts/reports/phase27_65_tokenizer_v8_topic_probe_report.json`
- `artifacts/tokenizers/sf_bpe/v8_phase27_65/`

## Phase 27.66 — V8 Bounded Topic Repair

### الهدف
تدريب إصلاح LM محدود على tokenizer v8 بعد نجاح حماية المصطلحات الموضوعية، ثم إعادة broader natural-dialogue canary. هذه ليست قفزة حجم ولا تفتح runtime.

### ما نُفّذ
- أضيف `scripts/phase27_66_v8_bounded_topic_repair.py`.
- أضيف `make phase27-v8-bounded-topic-repair`.
- استُخدم tokenizer v8 من `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
- دُرّب `SF-10M` لمدة `6200` خطوة على curriculum interleaved مع topic emphasis pack لـ `التعاون/الاحترام`.

### النتيجة
- broader canary: `30/30`.
- family summary: followup `6/6`, open_social `6/6`, planning `6/6`, support `6/6`, topic `6/6`.
- checkpoint: `artifacts/eval/phase27_66_v8_bounded_topic_repair/checkpoints/sf-10m-step6200`.

### القرار
نجح الإصلاح معمليًا، لكن runtime يبقى محجوبًا. المسموح التالي فقط: fresh shadow canary بأسئلة غير مرئية قبل أي فتح واجهة أو تغيير runtime.

التالي:

**Phase 27.67 — fresh shadow canary with unseen natural prompts**

### artifacts
- [PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md](./PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md)
- `artifacts/reports/phase27_66_v8_bounded_topic_repair_report.json`
- `artifacts/samples/phase27_66_v8_bounded_topic_repair.md`

## Phase 27.67 — Fresh Shadow Canary

### الهدف
اختبار checkpoint Phase 27.66 على أسئلة طبيعية غير مرئية وغير مطابقة لعبارات Phase 27.60 أو curriculum Phase 27.66. هذه مرحلة تقييم فقط، لا تدريب ولا runtime.

### ما نُفّذ
- أضيف `scripts/phase27_67_fresh_shadow_canary.py`.
- أضيف `make phase27-fresh-shadow-canary`.
- أُنشئ canary من `50` prompt فصيح/سعودي، `10` لكل عائلة: open_social, followup, planning, support, topic.
- أضيف فحص novelty داخلي ضد canary القديم وrepair curriculum.

### النتيجة
- novelty: `50/50`.
- fresh shadow canary: `30/50`.
- family summary: open_social `4/10`, followup `4/10`, planning `7/10`, support `6/10`, topic `9/10`.
- أبرز الفشل: انجراف open_social/followup إلى topic أو open_social، وانجراف support/planning في بعض الحالات.

### القرار
فشل التعميم على prompts غير مرئية. لا runtime switch، لا UI، لا SF-50M. Phase 27.68 يجب أن يكون إصلاحًا موجّهًا للفشل قبل أي مراجعة runtime.

التالي:

**Phase 27.68 — inspect Phase 27.67 failures and repair before runtime**

### artifacts
- [PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md](./PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md)
- `artifacts/reports/phase27_67_fresh_shadow_canary_report.json`
- `artifacts/samples/phase27_67_fresh_shadow_canary.md`

## Phase 27.68 — Shadow Failure Repair

### الهدف
إصلاح فشل Phase 27.67 في عائلات open_social/followup/support/topic مع الحفاظ على canary Phase 27.60. هذه مرحلة تدريب محدودة، وليست فتح runtime.

### ما نُفّذ
- أضيف `scripts/phase27_68_shadow_failure_repair.py`.
- أضيف `make phase27-shadow-failure-repair`.
- دُرّب `SF-10M` على tokenizer v8 لمدة `5600` خطوة.
- أضيفت أمثلة طبيعية مؤلفة محليًا فقط لإزالة انجراف open_social/followup/support/topic.
- عُدّل `GenerationGuard` ليطابق prompt triggers على مستوى الكلمات حتى لا يخلط `مرتبك` مع `رتب`.

### النتيجة
- Phase 27.67 known shadow: `50/50`.
- Phase 27.60 regression: `30/30`.
- checkpoint: `artifacts/eval/phase27_68_shadow_failure_repair/checkpoints/sf-10m-step5600`.

### القرار
نجح إصلاح الفشل المعروف، لكن لا يسمح بفتح الواجهة؛ لأن Phase 27.68 رأى فشل 27.67 أثناء التدريب. المسموح التالي فقط: fresh shadow canary جديد بأسئلة غير مرئية بعد الإصلاح.

التالي:

**Phase 27.69 — new fresh shadow canary with unseen prompts after repair**

### artifacts
- [PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md](./PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md)
- `artifacts/reports/phase27_68_shadow_failure_repair_report.json`
- `artifacts/samples/phase27_68_shadow_failure_repair.md`

## Phase 27.69 — New Fresh Shadow Canary

### الهدف
اختبار checkpoint Phase 27.68 على prompts جديدة لم تظهر في Phase 27.60 أو Phase 27.67 أو curriculum الإصلاح. هذه مرحلة تقييم فقط، لا تدريب ولا runtime.

### ما نُفّذ
- أضيف `scripts/phase27_69_new_fresh_shadow_canary.py`.
- أضيف `make phase27-new-fresh-shadow-canary`.
- أُنشئ canary جديد من `60` prompt، `12` لكل عائلة: open_social, followup, planning, support, topic.
- أضيف فحص novelty ضد canary وrepair prompts السابقة.

### النتيجة
- novelty: `60/60`.
- new fresh shadow: `56/60`.
- family summary: followup `12/12`, open_social `8/12`, planning `12/12`, support `12/12`, topic `12/12`.
- الفشل المتبقي محصور في open_social: انجراف إلى تعريف `التعاون` أو fragment في `موضوع/سوالف`.

### القرار
النتيجة قوية لكنها ليست كاملة. لا runtime switch ولا UI. Phase 27.70 يجب أن يكون إصلاحًا ضيقًا لـ open_social فقط، مع regression على 27.60/27.67/27.69.

التالي:

**Phase 27.70 — inspect Phase 27.69 open_social failures and repair before runtime** — اكتملت كتجربة فاشلة، ثم **Phase 27.71 — Candidate Selection and Stability Strategy** اختارت `phase27_68` كأفضل مرشح `136/140` مع بقاء runtime محجوبًا، ثم **Phase 27.72 — Stability-First Micro Repair** حسّنت النتيجة إلى `138/140` مع بقاء فشلين open_social، ثم **Phase 27.73 — Open-Social Failure Inspection** سدّت فجوة حارس الشظايا وشخّصت semantic collapse المتبقي، ثم **Phase 27.74 — Open-Social Semantic-Collapse Repair** جرّبت ثلاثة مرشحين من checkpoint 27.72 لكنها تراجعت إلى `56/60` fresh و`49/50` known، ثم **Phase 27.75 — Open-Social Strategy Inspection** أثبتت أن tokenizer v8 يفك `بسالفة` إلى `بس الفة` وأن tokenizer v9 مطلوب قبل LM repair جديد، ثم **Phase 27.76 — Tokenizer v9 Open-Social Boundary Probe** مرّت tokenizer-only (`17/17`, `15/15`)، ثم **Phase 27.77 — V9 Bounded Open-Social LM Repair** فشلت كتوليد بسبب خلط العائلات (`54/60`, `45/50`, `30/30`).

التالي الرسمي الآن:

**Phase 27.78 — Engineering Root Cause Gate**

### Sovereign Practical Acceleration Strategy v2 داخل Phase 27.78

Phase 27.78 ليست تكبيرًا ولا تدريبًا أعمى. هدفها إصدار
`PHASE27_78_ENGINEERING_DECISION` قبل أي تدريب جديد:

- فحص خلط عائلات الردود في Phase 27.77.
- فصل `open_social`, `followup`, `planning`, `support`, و`topic` في
  التقييم والتدريب.
- تثبيت curriculum training بدل التدريب العريض العشوائي.
- اعتماد no-repeat/repetition controls رسميًا داخل runtime المرشح.
- إبقاء held-out canary دائمًا قبل أي runtime release.
- فصل general assistant dialogue عن operator/workflow dialogue.
- وزن الأسباب: capacity/objective/curriculum/tokenizer/decoding/family
  mixing/memorization/weak generalization/EOS/repetition/semantic routing.

### نتيجة Phase 27.78

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يُفتح Gate لـ `SF-50M`.
- مصدر الفحص: `artifacts/reports/phase27_77_v9_bounded_open_social_lm_repair_report.json`.
- مجموع الفشل المتبقي: `11`.
- decision id: `PHASE27_78_ENGINEERING_DECISION`.
- أوزان الأسباب التقريبية:
  - family mixing `22%`.
  - objective `18%`.
  - curriculum `16%`.
  - weak generalization `14%`.
  - semantic routing `10%`.
  - decoding `7%`.
  - tokenizer `4%`.
  - EOS `4%`.
  - memorization `2%`.
  - repetition `2%`.
  - capacity `1%`.
- القرار: نستمر على `SF-10M`، ونمنع `SF-50M` الآن، ونغيّر objective/curriculum/family balance/decoding قبل أي تدريب.
- التالي: `Phase 27.79 — Objective/Curriculum/Decoding Repair Design`, no training until gates are encoded.

**Phase 27.79 — Objective/Curriculum/Decoding Repair Design**

### نتيجة Phase 27.79

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يُفتح `SF-50M`.
- أُنتج `PHASE27_79_REPAIR_DESIGN_DECISION`.
- objective المقترح: `family_conditioned_prompt_to_answer_objective_v1`.
- curriculum المقترح: `interleaved_family_curriculum_v2`.
- decoding المقترح: `semantic_guarded_decoding_v1`.
- التالي: `Phase 27.80 — Repair Gate Encoding and Dry-Run Validation`, بلا تدريب.

### متطلبات Phase 27.80

- objective spec validator.
- curriculum family-balance dry-run.
- decoding policy config validator.
- held-out/shadow canary manifest validator.
- family confusion matrix builder.
- operator-contamination regression scan.

### نتيجة Phase 27.80

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لا يوجد Qwen/open-weight/pretrained path.
- `objective_spec_validator`: نجح.
- `decoding_policy_config_validator`: نجح.
- `heldout_shadow_canary_manifest_validator`: نجح.
- `operator_contamination_regression_scan`: نجح (`0` hits).
- `curriculum_family_balance_dry_run`: فشل بسبب imbalance واضح:
  `open_social=3208`, `followup=1795`, `planning=424`, `support=364`,
  `topic=152`.
- `family_confusion_matrix_builder`: فشل؛ diagonal rate = `0.5351`.
- القرار: لا تدريب، لا tokenizer retrain، لا runtime، لا SF-50M. التالي
  remediation داخل Phase 27.80 لتوازن family قبل أي تدريب.

### نتيجة Phase 27.80 remediation

- لم يبدأ تدريب جديد.
- أضيفت خريطة family لكل corpus في
  `artifacts/eval/phase27_80_family_balance_remediation/family_manifest.jsonl`.
- أضيف config لمنهج balanced curriculum في
  `artifacts/eval/phase27_80_family_balance_remediation/balanced_curriculum_config.json`.
- أضيفت quota authoring plan في
  `artifacts/eval/phase27_80_family_balance_remediation/authoring_quota_plan.json`.
- القرار: يلزم 639 سجلًا قبل أي تدريب:
  - planning: 155 فصحى.
  - support: 85 فصحى + 51 سعودي.
  - topic: 188 فصحى + 160 سعودي.
- التالي: `Phase 27.81 — Balanced Family Pack Authoring`, بلا تدريب.

### نتيجة Phase 27.81

- لم يبدأ تدريب جديد.
- أضيفت دفعة `sf-ai-balanced-family-pack-v1`: `2500` سجل gold.
- التوزيع: `open_social=500`, `followup=500`, `planning=500`,
  `support=500`, `topic=500`.
- كل family موزعة `250 msa + 250 saudi`.
- corpus الحالي: `8443` سجلًا، `issues=0`, `gold=3331`, `silver=5112`.
- أعيد بناء split: `train=7595`, `eval=848`.
- أعيد تشغيل Phase 27.80 repair gates ومرّت:
  `PHASE27_80_GATES_PASSED_NO_TRAINING`.
- التالي: `Phase 27.82 — Family-conditioned SF-10M repair training decision`.

### نتيجة Phase 27.82

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يدرّب tokenizer جديد.
- أضيف `make phase27-family-conditioned-training-decision`.
- فحص القرار:
  - Phase 27.80 gates passed.
  - Phase 27.81 pack ready.
  - corpus ready: `8443`, issues=`0`.
  - tokenizer v9 sovereign ready.
  - init checkpoint `sf-10m-step6200` sovereign ready.
- القرار الرسمي: `PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION`.
- المسموح التالي فقط: `Phase 27.83 — Family-conditioned SF-10M bounded repair training`.
- محظور: runtime release، SF-50M، tokenizer retrain، pretrained/open-weight.
- خطة 27.83 محفوظة في:
  `artifacts/reports/phase27_82_family_conditioned_training_decision/phase27_83_training_plan.json`.

### الممنوع حتى بعد نتيجة Phase 27.83

- أي LM training جديد قبل تشخيص Phase 27.84.
- tokenizer retraining.
- runtime release.
- SF-50M full training.
- template masking.

### نتيجة Phase 27.83

- دُرّب `SF-10M` إصلاحًا محدودًا حسب خطة Phase 27.82.
- استخدم tokenizer v9 وcheckpoint `sf-10m-step6200` من Phase 27.77.
- checkpoints الناتجة: `step600`, `step1200`, `step1800`.
- fresh shadow:
  - `step600`: `7/60`.
  - `step1200`: `11/60`، الأفضل بالcanary لكنه منحاز للتخطيط.
  - `step1800`: `3/60`، تراجع واضح.
- eval loss لا يطابق جودة runtime: `step600` loss أقل لكنه ليس أفضل حواريًا.
- القرار: `BLOCK_RUNTIME_DIAGNOSE_OBJECTIVE_CURRICULUM_FAILURE`.
- التالي: `Phase 27.84 — Objective/Curriculum Failure Diagnosis`.
- محظور الآن: runtime release، SF-50M، tokenizer retrain، وأي تدريب جديد قبل التشخيص.

### نتيجة Phase 27.84

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- شُخّص فشل Phase 27.83 رغم توازن بيانات Phase 27.81.
- الدليل الحاسم: `dialogue_family/prompt_family/answer_family` موجودة في metadata
  لكنها لا تُrender داخل نص التدريب.
- النص المرئي للنموذج يحتوي `النطاق: سعودي/فصحى` فقط.
- السبب الأعلى وزنًا:
  - `objective_family_signal_missing=30%`
  - `curriculum_sampling_not_family_conditioned_in_text=24%`
  - `weak_generalization_after_bounded_repair=17%`
  - `model_capacity=4%`
- القرار: `DESIGN_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_BEFORE_ANY_TRAINING`.
- التالي: `Phase 27.85 — Explicit Family Conditioning Objective Design`.
- محظور الآن: أي تدريب جديد، runtime release، SF-50M، tokenizer retrain.

### نتيجة Phase 27.73
- لم يبدأ تدريب جديد.
- `open_social_09` كان يمر الحارس رغم fragment مثل `بمها`؛ أضيفت fragments إلى `GenerationGuard` وتُحجب الآن كـ `model_artifact_fragment`.
- `open_social_12` ينهار دلاليًا إلى تعريف `التعاون` بدل فتح سالفة؛ هذا يحتاج repair تدريبي ضيق، لا مجرد حارس.
- القرار: لا runtime switch ولا UI بالمولّد ولا SF-50M ولا Phase 28 قبل Phase 27.74.

### نتيجة Phase 27.74
- بدأ تدريب إصلاح ضيق على `open_social` من checkpoint 27.72.
- جرّب ثلاثة مرشحين: `gentle_48`, `balanced_72`, `focused_96`.
- أفضل مرشح كان `gentle_48`: `56/60` fresh، `49/50` known، `30/30` regression.
- النتيجة أسوأ من baseline 27.72، لذلك لا runtime ولا UI.
- سبب الفشل الجديد: fragments في open_social مثل `بس الفة`, `موضوعاموضوععن`, `أكموضوع`.
- القرار: Phase 27.75 يجب أن يكون inspection/strategy لا تدريب أعمى.

### نتيجة Phase 27.75
- لم يبدأ تدريب جديد.
- فحصنا إخفاقات أفضل مرشح 27.74: 5/5 إخفاقات كلها `open_social` وكلها `model_artifact_fragment`.
- tokenizer v8 يعيد `بسالفة` كـ `بس الفة`، وهذا يفسر شظية `خلنا نبدأ بس الفة`.
- أضيفت حزمة `resources/tokenization/protected_phrases_phase27_75.txt` إلى قواعد tokenization.
- القرار: لا LM-only repair جديد على tokenizer v8؛ التالي tokenizer v9 boundary probe.

### نتيجة Phase 27.76
- درّبنا tokenizer v9 فقط من corpus السيادي المحلي مع protected pack 27.75.
- لا LM training ولا runtime switch.
- `open_social` roundtrip: `17/17`.
- protected pack single-piece: `15/15`.
- topic terms single-piece: `8/8`، والحرجة `التعاون/الاحترام` protected `2/2`.
- القرار: Phase 27.77 مسموح كتدريب LM محدود على tokenizer v9 فقط، مع بقاء runtime محجوبًا حتى تمر بوابات التوليد.

### نتيجة Phase 27.77
- بدأ تدريب LM محدود على tokenizer v9 من الصفر، لأن vocab v9 لا يطابق checkpoints v8.
- النتيجة: Phase 27.69 fresh `54/60`, Phase 27.67 known `45/50`, Phase 27.60 regression `30/30`.
- tokenizer fragments اختفت كسبب رئيسي، لكن ظهر خلط عائلات: topic يجيب بموضوع آخر، followup ينجرف إلى open_social، وبعض support تعثر في guard.
- القرار: لا runtime ولا UI؛ Phase 27.78 أصبحت بوابة root-cause لا تدريبًا.

### artifacts
- [PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md](./PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md)
- `artifacts/reports/phase27_69_new_fresh_shadow_canary_report.json`
- `artifacts/samples/phase27_69_new_fresh_shadow_canary.md`
- [PHASE27_73_OPEN_SOCIAL_FAILURE_INSPECTION_REPORT.md](./PHASE27_73_OPEN_SOCIAL_FAILURE_INSPECTION_REPORT.md)
- `artifacts/reports/phase27_73_open_social_failure_inspection_report.json`
- `artifacts/samples/phase27_73_open_social_failure_inspection.md`
- [PHASE27_74_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_REPORT.md](./PHASE27_74_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_REPORT.md)
- `artifacts/reports/phase27_74_open_social_semantic_collapse_repair_report.json`
- `artifacts/samples/phase27_74_open_social_semantic_collapse_repair.md`
- [PHASE27_75_OPEN_SOCIAL_STRATEGY_INSPECTION_REPORT.md](./PHASE27_75_OPEN_SOCIAL_STRATEGY_INSPECTION_REPORT.md)
- `artifacts/reports/phase27_75_open_social_strategy_inspection_report.json`
- `artifacts/samples/phase27_75_open_social_strategy_inspection.md`
- [PHASE27_76_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_REPORT.md](./PHASE27_76_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_REPORT.md)
- `artifacts/reports/phase27_76_tokenizer_v9_open_social_boundary_probe_report.json`
- `artifacts/samples/phase27_76_tokenizer_v9_open_social_boundary_probe.md`
- [PHASE27_77_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_REPORT.md](./PHASE27_77_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_REPORT.md)
- `artifacts/reports/phase27_77_v9_bounded_open_social_lm_repair_report.json`
- `artifacts/samples/phase27_77_v9_bounded_open_social_lm_repair.md`

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
