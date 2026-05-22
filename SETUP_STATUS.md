# SETUP_STATUS.md

## SF.AI — حالة الإعداد

هذا الملف يصف حالة الإعداد العامة للمشروع: الملفات الموجودة، الأدوات المطلوبة، وما لم يُجهَّز بعد.

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الموقع:** `/Users/sami/workSF/SF.AI/`
- **الرحلة الحالية:** **Phase 22 / 30**
- **المرحلة الحالية:** **Phase 22 — Gold Dialogue Corpus v2** (بوابة corpus v2 تعمل؛ الشاشة شغّالة على http://127.0.0.1:8123/ui/chat)
- **الهدف العام:** الوصول إلى نموذج لغوي سيادي مولّد، يبدأ من الصفر، ثم يربط توليده بالشات خلف router/safety/composer.
- **المرحلة التالية المقترحة:** جمع ومراجعة محادثات فصحى/سعودية حقيقية حتى تمر `make phase22-readiness`.
- **القاموس/المسار اللغوي المتبع:** العربية الفصحى + اللهجة السعودية فقط؛ `Saudi Seed v1` مرجع خاص، و`safety_terms.yaml` محدث لفجوات المال/الدين/الأمن.
- **نتيجة Phase 12:** tokenizer v1 محفوظ في `artifacts/tokenizers/sf_bpe/v1/`، `vocab=261`, `merges=218`, `sf_origin=true`.
- **نتيجة Phase 13:** smoke training نجح: `loss 5.6638 → 4.7539`, checkpoint محلي في `artifacts/checkpoints/smoke_lm/sf-10m-step20`, وتقرير في `docs/PHASE13_SMOKE_TRAINING_REPORT.md`.
- **نتيجة Phase 14:** SF-10M v0.1 محدود نجح: `33/80` خطوة بسبب صغر corpus، eval loss `4.0777`, perplexity `59.01`, وتقرير في `docs/PHASE14_SF10M_V0_1_REPORT.md`.
- **نتيجة Phase 15:** أضيف `NativeGenerator` + `GenerationPolicy` + metadata في API/UI، لكن هذا adapter فقط؛ `SF-10M v0.1` خام وغير جاهز كحوار مقنع.
- **نتيجة Phase 16:** `make eval-phase16` نجح: `15/15`; التقرير يثبت أن النموذج خام ومكرر، والمختبر المحلي يبقى مفتوحًا للقياس.
- **نتيجة Phase 17:** أضيف `ChatRagBridge` و`ContextBuilder`; الشات يستطيع استخدام snippets محلية عند حقن `HybridRetriever`، ويعرض `rag=used/not_used`.
- **نتيجة Phase 18:** أضيف زر تصدير مراجعة من واجهة الشات + `scripts/prepare_dialogue_batch.py` + تقرير `artifacts/reports/dialogue_batch_report.json`; لا تدخل محادثات المستخدم إلى التدريب تلقائيًا.
- **حماية Phase 18:** ملفات `data/corpus/**/review/*.jsonl` مستثناة من git افتراضيًا؛ العينة الآمنة الوحيدة المسموحة هي `sample_review_export.jsonl`.
- **نتيجة Phase 19:** أضيفت بوابة `make phase19-readiness` و`GET /system/phase19-readiness`; القرار الحالي `NOT_READY_EXPAND_CORPUS_FIRST` لأن corpus الحالي 30 سجلًا فقط والحد الأدنى العملي 5000.
- **نتيجة Phase 20:** أضيفت بوابة `make phase20-gates` و`GET /system/phase20-gates`; لا مجال يتفعل تلقائيًا، و`chat` هو المجال النشط الوحيد.
- **تصحيح Phase 20:** أضيف `sf_ai/modules/productivity/` كسكيلتون كامل بعد أن كشفت البوابة وجوده في registry دون module/manifest.
- **نتيجة Phase 21:** أضيف `docs/GENERATIVE_ROADMAP.md` ومُدّدت الخطة إلى Phase 30؛ أول تدريب جودة مفيد قادم Phase 24، وأول هدف حوار مولّد مقنع Phase 26–28.
- **مبدأ التكبير الرسمي:** `Progressive Scaling Strategy` — لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية، والسلم الرسمي هو `SF-10M → SF-50M → SF-120M → SF-350M → SF-700M → SF-1B+`.
- **نتيجة Phase 22:** أضيف `make phase22-readiness` و`make phase22-plan` و`make phase22-next-batch` و`make phase22-review-intake` و`GET /system/phase22-readiness` و`GET /system/phase22-collection-plan` و`GET /system/phase22-next-batch` و`GET /system/phase22-review-intake`; القرار الحالي `NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2` لأن corpus الحالي 30/500 ويفتقد `msa`.
- **خطة batches الدقيقة:** `make phase22-plan` يعرض الآن `planned_batches`: `msa_001..msa_008`, `saudi_001..saudi_007`, `flex_001..flex_004` مع عدد السجلات وملف الإخراج وأمر التحويل المقترح.
- **مهمة batch التالية:** `make phase22-next-batch` يعرض الآن `msa_001` كالمهمة الفورية: 25 سجلًا فصيحًا، مع checklist قبول وموضوعات تأليف عامة وليست بيانات تدريب.
- **Review intake الحالي:** `data/corpus/chat/review/sample_review_export.jsonl` مرشح للمراجعة فقط؛ الأداة read-only ولا تنقل أي شيء إلى التدريب.
- **بوابة جودة الحوار:** `phase22-review-intake` يعرض الآن `quality_score/quality_label/quality_blockers`; الجلسة المفيدة للتدريب تحتاج غالبًا 3 أدوار مستخدم + 3 ردود مساعد على الأقل وبدون `sf_10m_v0_1`.
- **بوابة Phase 22 في الواجهة:** شاشة `/ui/chat` تعرض قراءة حية من `/system/phase22-readiness`: عدد corpus الحالي، المتبقي، نقص `msa/saudi`، وهل Phase 23 ما زالت محجوبة.
- **مهمة الجمع الحالية في الواجهة:** شاشة `/ui/chat` تعرض `msa_001` من `/system/phase22-next-batch` مع هدف 25 سجلًا وموضوعات تأليف عامة، وتضع `phase22_next_batch` داخل metadata عند التصدير.
- **مؤشر جودة التصدير في الواجهة:** شاشة `/ui/chat` تعرض score جودة محلي قبل التصدير وتضع `ui_quality_score/ui_quality_label/ui_quality_blockers` داخل metadata.
- **تصحيح تشغيل المولّد:** الواجهة المستقرة عادت إلى `generator=template` افتراضيًا؛ هذا يعني قوالب ثابتة لا توليدًا ذكيًا. `SF-10M` الخام لا يدخل ردود الشات إلا بفلاغات مختبر صريحة.
- **مختبر سامي المحلي:** يمكن تشغيل المولّد الخام عبر `SF_ENABLE_NATIVE_GENERATOR=true` و`SF_NATIVE_GENERATOR_EXPERIMENTAL=true`، وتمكين الرسائل غير الحساسة من مجالات skeleton عبر `SF_LAB_GENERATION_FOR_NON_SENSITIVE=true` عند الاختبار فقط.
- **حماية التصدير:** إذا صدّرت جلسة تحتوي ردودًا من `sf_10m_v0_1`، تضع الواجهة metadata واضحًا، و`phase22-review-intake` لا يعدّها candidate تدريب جودة.
- **واجهة الاختبار:** لا تستخدم الواجهة حاليًا لاختبار مولد مقنع؛ استخدمها فقط لجمع محادثات review أو لفحص التوجيه. التشخيص يبين `template` أو `sf_10m_v0_1`.
- **تفويض التنفيذ:** سامي أعطى إذنًا صريحًا بمتابعة التدريب والاختبارات والمراحل المسجلة دون انتظار موافقات جديدة؛ استخدم flags المطلوبة مع توثيق كل تشغيل ولا تكسر قواعد السيادة/السلامة.
- **فحص Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/corpus-audit`
- **قرار Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/phase12-readiness` يعرض أن tokenizer v1 اكتمل، مع بقاء `missing_required_dialects=["msa"]` قبل إعادة تدريب متوازن.
- **قرار Phase 12 من الطرفية بدون restart:** `make phase12-readiness`، وهو read-only ويعرض نفس منطق القرار.
- **بوابات Phase 20 من الطرفية/API:** `make phase20-gates` أو `GET http://127.0.0.1:8123/system/phase20-gates`.
- **خطة جمع Phase 22:** `make phase22-plan` أو `GET http://127.0.0.1:8123/system/phase22-collection-plan`.
- **فحص ملفات review في Phase 22:** `make phase22-review-intake` أو `GET http://127.0.0.1:8123/system/phase22-review-intake`، ويشمل score جودة الحوار.
- **جرد المصادر الشامل:** `make source-inventory` أو `GET http://127.0.0.1:8123/system/source-inventory`
- **فحص السيرفر بدون تعطيل:** `make server-status`، وهو read-only ولا يعمل restart/stop.
- **تشغيل السيرفر المستقر:** `make server-start` يبدأه داخل `screen` فقط إذا كان متوقفًا.
- **المراجع المحلية الخاصة الموجودة:** 516 مدخل قاموس سعودي + 1032 مهمة لهجة سعودية، وهي مستثناة من الرفع وتحتاج تحويل/حوكمة قبل استخدامها كـ LM corpus.
- **طبقة الحوكمة الهندسية قبل Phase 12:** مكتملة في `docs/PROJECT_IDENTITY.md`, `docs/ENGINEERING_RULES.md`, `docs/AGENT_INSTRUCTIONS.md`, `docs/PROJECT_MAP.md`, `docs/PROJECT_LIFECYCLE.md`.
- **طبقة الدستور الهندسي واللغوي قبل Phase 12:** مكتملة في `docs/PROJECT_CONSTITUTION.md`, `docs/LANGUAGE_SEGMENTATION.md`, `docs/TOKENIZATION_POLICY.md`, `docs/DATASET_GOVERNANCE.md`, `docs/AGENT_ENGINEERING_RULES.md`.
- **موارد tokenization:** `resources/tokenization/protected_terms_saudi.txt`, `resources/tokenization/preferred_merges.txt`, `resources/tokenization/tokenization_rules.yaml`.
- **فحص tokenization قبل Phase 12:** `make tokenization-audit`، وهو read-only ولا يدرّب tokenizer.
- **نتيجة tokenization-audit الحالية:** 30/30 protected terms مغطاة في corpus الحالي؛ التغطية 100%.
- **تقرير Phase 12:** `docs/PHASE12_TOKENIZER_V1_REPORT.md`، وحالته: `COMPLETED_WITH_LIMITS`.
- **تحسين اللغة الأخير:** التركيز الافتراضي الآن على العربية الفصحى + اللهجة السعودية فقط، مع إيقاف اللهجات الأخرى افتراضيًا.
- **تحسين المحادثة الأخير:** واجهة فاتحة أوضح للشات، خطوط أكبر، أزرار أوضح، لوحة تشخيص مقروءة، تسمية عربية لـ `generator/rag/dispatch`، وزر `تصدير` لمراجعة المحادثة.
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

## الملفات الموجودة الآن (Phases 0–18 + Governance Layer)

```
SF.AI/
├── README.md                              Phase 1
├── PROJECT_PRINCIPLES.md                  Phase 0
├── SETUP_STATUS.md                        محدّث
├── .env.example / .gitignore              Phase 1 (+ runtime lexicon flags)
├── docker-compose.yml / Makefile          Phase 1 (+ targets Phase 3.5/5.5/6/12/18)
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
│   │   │   └── chat.html                  شاشة المحادثة RTL (Phase 9 + clear/timestamps/export)
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
│   ├── datasets/                          Phase 5 + Phase 3.6 + Phase 18 dialogue batches
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
│   ├── chat/{raw,cleaned,jsonl,review}/   Phase 5/11/18 — governed chat corpus + review exports
│   └── dialects/saudi/
│       ├── raw/mo3jam/                    Phase 3.5
│       ├── jsonl/saudi_dialect_training_tasks_seed_v1.jsonl   Phase 3.6
│       ├── cleaned/, reports/
│
├── artifacts/{tokenizers,checkpoints,logs,reports}/   Phase 5.5+ outputs/reports
│
├── tests/                                 pytest suite — 423 تست / 48 ملف
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
│   ├── prepare_dialogue_batch.py          Phase 18 — يحضر exports مراجعة إلى batch تدريبي محكوم
│   ├── phase19_readiness.py               Phase 19 — بوابة جاهزية SF-50M read-only
│   ├── phase20_gates.py                   Phase 20 — بوابات تفعيل المجالات read-only
│   └── import_mo3jam_saudi.py             Phase 3.5
│
└── docs/
    ├── EXECUTION_PLAN.md, PHASE_STATUS.md, ARCHITECTURE.md
    ├── PROJECT_IDENTITY.md, ENGINEERING_RULES.md, AGENT_INSTRUCTIONS.md
    ├── PROJECT_MAP.md, PROJECT_LIFECYCLE.md
    ├── CURRENT_GOALS.md                    الهدف العام وخارطة التوليد الحالية
    ├── DATA_IMPROVEMENT_LOOP.md           Phase 18 — دورة تحسين البيانات
    ├── PHASE19_READINESS_REPORT.md         Phase 19 — قرار جاهزية SF-50M
    ├── PHASE20_DOMAIN_ACTIVATION_GATES_REPORT.md  Phase 20 — بوابات المجالات
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
- `GET /system/status` — حالة المراحل + flags السيادة + قائمة المكونات، بما فيها Phase 19/20.
- `GET /system/corpus-audit` — جاهزية corpus قبل Phase 12.
- `GET /system/phase12-readiness` — قرار جاهزية Phase 12 مع بوابة الإذن.
- `GET /system/phase19-readiness` — قرار جاهزية Phase 19 قبل أي تدريب `SF-50M`.
- `GET /system/phase20-gates` — بوابات تفعيل المجالات؛ read-only ولا يفعّل مجالًا تلقائيًا.
- `GET /system/phase22-readiness` — بوابة جاهزية corpus v2 قبل Phase 23.
- `GET /system/phase22-collection-plan` — خطة جمع corpus v2 حسب العجز الحالي.
- `GET /system/phase22-review-intake` — فحص ملفات review exports قبل أي تحويل تدريبي.
- `GET /system/source-inventory` — جرد مصادر البيانات والمراجع.
- `POST /chat/message` — Orchestrator: NLP → Router → Module/Composer. يرجع domain/intent/confidence/signals/route_reason/response/requires_safety/status/fallback_used/dispatch/generator/debug.
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

آخر تحقق حي بدون restart:
- السيرفر يعمل داخل `screen` detached باسم `sfai8123` على `127.0.0.1:8123`.
- الكود الحالي بعد Phase 22 يعرض `Phase 22`، وزر `تصدير` في الواجهة، و`generator` حسب flags التشغيل.
- `GET /system/corpus-audit` يعرض `READY_FOR_PHASE_12_TOKENIZER_TRAINING` بعدد 30/30
- `make server-status` read-only ولا يوقف السيرفر.

> المنفذ 8000/8765 مشغول بمشروع آخر للمستخدم — استخدم 8123.

---

## نتائج الاختبارات (حتى Phase 22 review intake)

```
423 passed in 4.43s
```

التغطية الحالية:
- `test_arabic_normalizer.py` — 16 tests
- `test_capability_registry.py` — 5 tests
- `test_chat_module.py` — 12 tests (Phase 4 + language polish)
- `test_chat_native_generator.py` — 15 tests (Phase 15 + lab routing)
- `test_chat_rag_bridge.py` — 6 tests (Phase 17)
- `test_phase16_eval_harness.py` — 3 tests (Phase 16)
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
- `test_chat_ui.py` — 4 tests (Phase 9 + export quality indicator)
- `test_dialogue_batch_preparation.py` — Phase 18 data loop
- `test_dialect_mapper.py` — 7 tests
- `test_health.py` — 11 tests (API + module dispatch + safety + readiness)
- `test_intent_detector.py` — 7 tests
- `test_new_chat_intents.py` — 38 tests (daily social + Phase 22 guidance prompts)
- `test_nlp_pipeline.py` — 9 tests
- `test_phase10_skeleton_domains.py` — 4 tests (Phase 10)
- `test_phase22_review_intake.py` — 7 tests (Phase 22 review exports + dialogue quality gate)
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
- **Phase 15:** ربط checkpoint ببنية `ChatModule` كمولّد اختياري، مع إبقاء runtime على القوالب.
- **Phase 16:** تقييم الجودة والسلامة والأسلوب السعودي/الفصيح — مكتمل، ومختبر سامي المحلي يستطيع تشغيل المولد الخام للتجربة.
- **Phase 17:** ربط Memory/RAG المحلي بالشات — مكتمل كبنية محلية اختيارية.
- **Phase 18:** دورة توسيع بيانات من اختبار سامي المباشر — مكتملة كتصدير مراجعة + batch preparation محكوم.
- **Phase 19:** بوابة جاهزية تدريب مرشح `SF-50M` — تعمل، وقرارها الحالي: وسّع corpus أولًا.
- **Phase 20:** بوابات تفعيل المجالات skeleton عبر gates مستقلة — تعمل، ولا تفعّل شيئًا تلقائيًا.

أول توليد خام حدث في Phase 13. Phase 15 جهّز الباب داخل الشات، وPhase 16 أثبت أن التوليد مكرر. مختبر سامي المحلي يعمل الآن، والجودة الاجتماعية الموثوقة تحتاج بيانات/تدريب أفضل.

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
- ❌ لا تدريب خارج الخطة أو بدون provenance؛ التفويض الحالي يغطي المراحل المسجلة فقط.
- ❌ لا crawling تلقائي. CrawlerBase يرفع `CrawlerPermissionError` بدون `permission_granted=True`.
- ❌ لا انتقال خارج الخطة المسجلة بدون توثيق وإذن واضح.

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

التفويض الحالي من سامي: استمر في المراحل المسجلة دون انتظار موافقة جديدة، مع رفع الناجح فقط، وفحص الحساسية، وتوثيق كل خطوة. لا تبدأ أي مصدر خارجي/زحف/اعتماد pretrained مهما كان التفويض عامًا.
