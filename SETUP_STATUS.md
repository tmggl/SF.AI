# SETUP_STATUS.md

## SF.AI — حالة الإعداد

هذا الملف يصف حالة الإعداد العامة للمشروع: الملفات الموجودة، الأدوات المطلوبة، وما لم يُجهَّز بعد.

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الموقع:** `/Users/sami/workSF/SF.AI/`
- **المرحلة الحالية:** **Phase 11 — Sovereign Corpus Governance & Saudi/MSA Dialogue Pack** (مكتملة كحوكمة؛ الشاشة شغّالة على http://127.0.0.1:8123/ui/chat)
- **الهدف العام:** الوصول إلى نموذج لغوي سيادي مولّد، يبدأ من الصفر، ثم يربط توليده بالشات خلف router/safety/composer.
- **المرحلة التالية المقترحة:** **Phase 12 — SF-BPE Tokenizer v1 Training & Audit** بعد وضع بيانات JSONL وموافقة صريحة.
- **بوابة Phase 12 الحالية:** `make corpus-audit` جاهز بنيويًا بعدد 30/30، لكن `make phase12-readiness` يمنع الانتقال لأن corpus الحالي سعودي فقط ويفتقد `msa`.
- **بوابة التدريب التنفيذية:** `make train-bpe` يرفض التشغيل بدون `--confirm-phase12-permission`، ولا يُستخدم هذا العلم إلا بعد إذن صريح ببدء Phase 12.
- **فحص Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/corpus-audit`
- **قرار Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/phase12-readiness` يعرض `can_train_now=false` و`missing_required_dialects=["msa"]` حتى إضافة فصحى مصرح بها ثم الإذن.
- **قرار Phase 12 من الطرفية بدون restart:** `make phase12-readiness`، وهو read-only ويعرض نفس منطق القرار.
- **جرد المصادر الشامل:** `make source-inventory` أو `GET http://127.0.0.1:8123/system/source-inventory`
- **فحص السيرفر بدون تعطيل:** `make server-status`، وهو read-only ولا يعمل restart/stop.
- **تشغيل السيرفر المستقر:** `make server-start` يبدأه داخل `screen` فقط إذا كان متوقفًا.
- **المراجع المحلية الخاصة الموجودة:** 516 مدخل قاموس سعودي + 1032 مهمة لهجة سعودية، وهي مستثناة من الرفع وتحتاج تحويل/حوكمة قبل استخدامها كـ LM corpus.
- **طبقة الحوكمة الهندسية قبل Phase 12:** مكتملة في `docs/PROJECT_IDENTITY.md`, `docs/ENGINEERING_RULES.md`, `docs/AGENT_INSTRUCTIONS.md`, `docs/PROJECT_MAP.md`, `docs/PROJECT_LIFECYCLE.md`.
- **طبقة الدستور الهندسي واللغوي قبل Phase 12:** مكتملة في `docs/PROJECT_CONSTITUTION.md`, `docs/LANGUAGE_SEGMENTATION.md`, `docs/TOKENIZATION_POLICY.md`, `docs/DATASET_GOVERNANCE.md`, `docs/AGENT_ENGINEERING_RULES.md`.
- **موارد tokenization:** `resources/tokenization/protected_terms_saudi.txt`, `resources/tokenization/preferred_merges.txt`, `resources/tokenization/tokenization_rules.yaml`.
- **فحص tokenization قبل Phase 12:** `make tokenization-audit`، وهو read-only ولا يدرّب tokenizer.
- **نتيجة tokenization-audit الحالية:** 30/30 protected terms مغطاة في corpus الحالي؛ التغطية 100%.
- **تقرير Phase 12 preflight:** `docs/PHASE12_PREFLIGHT_REPORT.md`، وحالته: corpus/tokenization جاهزان، لكن قرار Phase 12 النهائي موقوف بسبب نقص `msa` وإذن التدريب غير ممنوح.
- **تحسين اللغة الأخير:** التركيز الافتراضي الآن على العربية الفصحى + اللهجة السعودية فقط، مع إيقاف اللهجات الأخرى افتراضيًا.
- **تحسين المحادثة الأخير:** توجيه أدق للرسائل اليومية (`شكرا`، `تمام`، `لا`، `ساعدني`، `مش فاهم`، `من صنعك`) + `سعودي` + `عندي؟` + زر مسح المحادثة + timestamps.
- **خلفية:** بعد Phase 7 أضاف المستخدم قاموس سعودي تأليفي (Phase 3.6)، ثم أُكملت Phase 8 (RAG)، Phase 9 (الشاشة)، Phase 10 (هياكل المجالات).
- **آخر تحديث:** 2026-05-22

---

## بيئة التطوير

### الجهاز
- **MacBook Air M4**
- **Memory:** 24GB
- **OS:** macOS (Darwin 24.6.0)
- **Shell:** zsh

### الأدوات المنصّبة الآن (Phase 1)
- **Python 3.14.5** على macOS / Apple Silicon (`pyproject.toml` يشترط ≥3.11).
- بيئة افتراضية محلية في `SF.AI/.venv/`.
- **fastapi 0.136**, **uvicorn 0.47** + uvloop + httptools + websockets.
- **pydantic 2.13**, **pydantic-settings 2.14**, **python-dotenv 1.2**, **PyYAML 6.0**.
- **httpx 0.28**.
- **pytest 9.0**, **pytest-asyncio 1.3**, **ruff 0.15**, **mypy 2.1**.

### الأدوات المنصّبة الإضافية (Phase 6)
- **PyTorch 2.12** مع دعم MPS (Apple Silicon) فعال.
- **numpy 2.4** (مطلوب من torch).
- **beautifulsoup4 4.14** + **lxml 6.1** (Phase 3.5 للاستيراد).

### الأدوات المخططة (تأتي في مراحلها)
- Apple MLX كإطار حساب اختياري (Phase 5.5/6).
- PostgreSQL (Phase 1+ docker-compose عند الحاجة).
- Redis (Phase 1+ docker-compose عند الحاجة).
- Qdrant (Phase 8).
- Scrapy / Playwright / BeautifulSoup / lxml (Phase 7).
- Next.js / React / TypeScript (Phase 9).
- Docker / docker-compose (متاح كـ skeleton، لم تُشغَّل الخدمات).

---

## الملفات الموجودة الآن (Phases 0–11 + Governance Layer)

```
SF.AI/
├── README.md                              Phase 1
├── PROJECT_PRINCIPLES.md                  Phase 0
├── SETUP_STATUS.md                        محدّث
├── .env.example / .gitignore              Phase 1 (+ runtime lexicon flags)
├── docker-compose.yml / Makefile          Phase 1 (+ targets Phase 3.5/5.5/6/12 preflight)
├── pyproject.toml                         Phase 1 (+ training extras: torch)
│
├── apps/
│   ├── api/
│   │   ├── main.py                        FastAPI + ui router
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── health.py                  GET /health
│   │   │   ├── chat.py                    POST /chat/message → Orchestrator
│   │   │   ├── system.py                  GET /system/status
│   │   │   └── ui.py                      GET /ui/chat  (Phase 9)
│   │   ├── static/
│   │   │   └── chat.html                  شاشة المحادثة RTL (Phase 9 + clear/timestamps)
│   │   └── schemas/{chat,system}.py
│   └── web/README.md                      placeholder for Next.js later
│
├── sf_ai/
│   ├── core/
│   │   ├── config.py, logging.py
│   │   ├── orchestrator/                  Phase 2 + NLP wiring Phase 3
│   │   ├── router/                        DomainRouter + IntentRouter (lens-aware)
│   │   ├── semantic/                      lexical + hashing + explorer
│   │   ├── index/                         CapabilityRegistry + default_registry.yaml
│   │   ├── planner/                       stub
│   │   ├── composer/                      ResponseComposer
│   │   └── nlp/                           Phase 3 — Arabic normalizer, dialect,
│   │                                       arabizi, typo, intent_detector, pipeline
│   ├── modules/
│   │   ├── chat/                          Phase 4 — active module + state + templates
│   │   ├── web/                           Phase 7 — ready_offline
│   │   └── research/                      Phase 7 — ready_offline
│   ├── memory/                            Phase 8 — sparse + vector + hybrid + LT
│   ├── tools/web/                         Phase 3.5 + Phase 7 — crawler, robots,
│   │                                       rate_limiter, extractors, mo3jam importer
│   ├── models/
│   │   ├── tokenizer/                     Phase 5.5 — char + SF-BPE + trainer
│   │   └── transformer/                   Phase 6 — TinyTransformer + RoPE + RMSNorm
│   ├── datasets/                          Phase 5 + Phase 3.6 (saudi_seed loader)
│   └── training/                          Phase 5.5 + Phase 6 — device, schedules,
│                                           checkpoints, optimizers, train_*.py
│
├── resources/lexicons/
│   ├── *.yaml                             Phase 3 seed lexicons (18 ملف)
│   └── imported/
│       ├── mo3jam/                        Phase 3.5 destination (فارغ حتى الاستيراد)
│       └── saudi_seed_v1/                 Phase 3.6 — قاموسك (516 مدخل)
├── resources/tokenization/                Constitution Layer — protected terms + rules
│
├── data/corpus/
│   ├── chat/{raw,cleaned,jsonl}/          Phase 5/11 — first_dialogue_seed.jsonl + CARD
│   └── dialects/saudi/
│       ├── raw/mo3jam/                    Phase 3.5
│       ├── jsonl/saudi_dialect_training_tasks_seed_v1.jsonl   Phase 3.6
│       ├── cleaned/, reports/
│
├── artifacts/{tokenizers,checkpoints,logs}/   Phase 5.5+ outputs
│
├── tests/                                 pytest suite — 348 تست
│   ├── fixtures/
│   │   ├── mo3jam_listing_sample.html, mo3jam_term_sample.html
│   │   └── article_sample.html
│   └── test_*.py
│
├── sf_ai/modules/{coding,data,files,legal,medical,finance,education,
│                 religion,social,writing,translation,image,audio,
│                 security,business,ecommerce}/
│                                           Phase 10 — skeleton modules
│
├── scripts/
│   ├── check_env.sh
│   ├── validate_dataset.py                Phase 5
│   ├── train_bpe.py                       Phase 5.5
│   ├── run_chat_server.sh                 يشغّل API على 8123 ويفعّل Saudi Seed افتراضيًا
│   └── import_mo3jam_saudi.py             Phase 3.5
│
└── docs/
    ├── EXECUTION_PLAN.md, PHASE_STATUS.md, ARCHITECTURE.md
    ├── PROJECT_IDENTITY.md, ENGINEERING_RULES.md, AGENT_INSTRUCTIONS.md
    ├── PROJECT_MAP.md, PROJECT_LIFECYCLE.md
    ├── CURRENT_GOALS.md                    الهدف العام وخارطة التوليد الحالية
    ├── ROUTER.md, SEMANTIC_EXPLORER.md, LANGUAGE_UNDERSTANDING.md
    ├── DATASET_FORMAT.md, SOVEREIGN_ACCELERATION.md, TRAINING_PLAN.md
    ├── WEB_RESEARCH_PLAN.md, WEB_CRAWLING_POLICY.md, RAG_PLAN.md
    ├── CURRENT_GOALS.md                    أهداف اللغة والاختبار الحالية
    ├── SOURCE_DISCOVERY_MO3JAM.md         Phase 3.5
    ├── SOURCE_DISCOVERY_SAUDI_SEED.md     Phase 3.6
    └── LEXICON_STATS.md
```

---

## الـ Endpoints الفعالة

- `GET /` — معلومات root + رابط الـ UI.
- `GET /health` — فحص صحة (project + phase).
- `GET /system/status` — حالة المراحل + flags السيادة + قائمة المكونات، بما فيها Phase 10 skeleton modules.
- `GET /system/corpus-audit` — جاهزية corpus قبل Phase 12.
- `GET /system/phase12-readiness` — قرار جاهزية Phase 12 مع بوابة الإذن.
- `GET /system/source-inventory` — جرد مصادر البيانات والمراجع.
- `POST /chat/message` — Orchestrator: NLP → Router → Module/Composer. يرجع domain/intent/confidence/signals/route_reason/response/requires_safety/status/fallback_used/dispatch/debug.
- `GET /chat` → redirect (307) إلى `/ui/chat`.
- `GET /ui/chat` — **شاشة المحادثة العربية RTL** (Phase 9).

تشغيل (السيرفر شغّال حاليًا في `screen` detached باسم `sfai8123` على 8123):
```bash
bash scripts/run_chat_server.sh
```
فحص بدون تعطيل:
```bash
make server-status
```
تشغيل detached إذا كان متوقفًا:
```bash
make server-start
```
ثم زر `http://127.0.0.1:8123/ui/chat` أو `http://127.0.0.1:8123/docs`.

آخر تحقق حي:
- listener: `Python 75503` على `127.0.0.1:8123`
- `GET /health` → 200، `{"status":"ok","project":"SF.AI","phase":"Phase 11"}`
- `GET /system/status` يعرض `saudi_seed_v1_lexicon=active`
- `GET /system/corpus-audit` يعرض `READY_FOR_PHASE_12_TOKENIZER_TRAINING` بعدد 30/30
- smoke: `وشلونك` → `chat.smalltalk` بدون fallback، و`عندي سؤال` → دعوة مباشرة لكتابة السؤال.

> المنفذ 8000/8765 مشغول بمشروع آخر للمستخدم — استخدم 8123.

---

## نتائج الاختبارات (Phase 11 + Governance Layer)

```
353 passed in 2.18s
```

التغطية الحالية:
- `test_arabic_normalizer.py` — 16 tests
- `test_capability_registry.py` — 5 tests
- `test_chat_module.py` — 12 tests (Phase 4 + language polish)
- `test_conversation_state.py` — 8 tests (Phase 4)
- `test_corpus_governance.py` — Phase 11 corpus governance
- `test_dataset_validators.py` — 28 tests (Phase 5)
- `test_bpe_tokenizer.py` — 13 tests (Phase 5.5)
- `test_training_device.py` — 14 tests (Phase 5.5)
- `test_checkpoints.py` — 7 tests (Phase 5.5)
- `test_training_config.py` — 8 tests (Phase 5.5)
- `test_mo3jam_importer.py` — 13 tests (Phase 3.5)
- `test_tiny_transformer.py` — 26 tests (Phase 6)
- `test_web_extractor.py` — 18 tests (Phase 7)
- `test_research_summarizer.py` — 20 tests (Phase 7)
- `test_saudi_seed.py` — 15 tests (Phase 3.6)
- `test_rag_sparse_retrieval.py` — 14 tests (Phase 8)
- `test_chat_ui.py` — 4 tests (Phase 9)
- `test_dialect_mapper.py` — 7 tests
- `test_health.py` — API + module dispatch + safety + corpus/source inventory
- `test_intent_detector.py` — 7 tests
- `test_new_chat_intents.py` — 31 tests (thanks/help/affirmation/negation/confused/who_made_you/farewell/language_preference/clarification)
- `test_nlp_pipeline.py` — 9 tests
- `test_phase10_skeleton_domains.py` — 4 tests (Phase 10)
- `test_orchestrator.py` — 7 tests
- `test_response_composer.py` — 6 tests
- `test_router.py` — 8 tests
- `test_router_with_nlp.py` — 5 tests
- `test_semantic_explorer.py` — 10 tests
- `test_typo_corrector.py` — 5 tests

تشغيل: `make test`.

---

## خارطة النموذج اللغوي السيادي بعد Phase 11

- **Phase 11:** حوكمة وتجهيز بيانات حوار عربي/سعودي — مكتملة كحوكمة، وفيها corpus seed سعودي صغير 30/30؛ ما زالت الفصحى `msa` مطلوبة قبل Phase 12.
- **Governance Layer:** قواعد الهندسة والهوية وخريطة المشروع ودورة الحياة — مكتملة قبل Phase 12.
- **Phase 12:** تدريب SF-BPE tokenizer v1 من بيانات SF.AI فقط.
- **Phase 13:** تدريب smoke صغير لإثبات أن النموذج يتعلم ويولد نصًا خامًا.
- **Phase 14:** تدريب `SF-10M v0.1`.
- **Phase 15:** ربط checkpoint بـ `ChatModule` كمولّد اختياري.
- **Phase 16:** تقييم الجودة والسلامة والأسلوب السعودي/الفصيح.
- **Phase 17:** ربط Memory/RAG المحلي بالشات.
- **Phase 18:** دورة توسيع بيانات بإذن صريح.
- **Phase 19:** تدريب مرشح `SF-50M`.
- **Phase 20:** تفعيل المجالات skeleton عبر gates مستقلة.

أول توليد خام متوقع في Phase 13. أول توليد داخل شاشة الشات في Phase 15. الاستخدام اليومي الموثوق أكثر بعد Phase 16.

---

## ما هو محظور (تذكير دائم)

- ❌ لا OpenAI / Claude / Gemini APIs.
- ❌ لا أي LLM جاهز.
- ❌ لا pretrained weights / embeddings / tokenizer.
- ❌ لا Llama / Gemma / Phi / Mistral.
- ❌ لا sentence-transformers.
- ❌ لا HuggingFace pretrained.
- ❌ لا LoRA فوق نموذج خارجي.
- ❌ لا synthetic LLM data في corpus السيادي.
- ❌ لا API keys في الكود.
- ❌ لا تدريب فعلي قبل إذن صريح (Phase 6 جاهز scaffolding، لا أوزان مدرَّبة).
- ❌ لا crawling تلقائي. CrawlerBase يرفع `CrawlerPermissionError` بدون `permission_granted=True`.
- ❌ لا انتقال بين المراحل بدون إذن صريح.

---

## ما هو مسموح (تذكير دائم)

- ✅ Python / PyTorch / PyTorch MPS / Apple MLX (كأدوات حساب).
- ✅ FastAPI / Next.js / React / TypeScript.
- ✅ PostgreSQL / Redis / Qdrant (مع vectors محلية فقط).
- ✅ Scrapy / Playwright / BeautifulSoup / lxml.
- ✅ pandas / openpyxl.
- ✅ Docker / docker-compose.
- ✅ pytest / ruff / mypy.
- ✅ YAML / JSON / JSONL.
- ✅ Rule-based / lexical scoring / fuzzy matching محلي / hashing vectorizer محلي.
- ✅ BPE tokenizer مدرَّب من الصفر على بيانات SF.AI فقط.
- ✅ Random initialization، AdamW، schedulers، gradient accumulation/checkpointing، mixed precision.
- ✅ Architectures معروفة (Decoder-only Transformer, RoPE, RMSNorm, SwiGLU, weight tying) بدون أوزانها.

---

## بروتوكول الانتقال

> **"اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"**

لا انتقال بدون إذن صريح من المستخدم.
