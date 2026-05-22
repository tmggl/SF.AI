# PHASE_STATUS.md

## SF.AI — سجل حالة المراحل

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الرحلة الحالية:** **Phase 19 / 20**
- **المرحلة الحالية:** **Phase 19 — SF-50M Readiness Gate**
- **حالة المرحلة الحالية:** **بوابة الجاهزية تعمل؛ تدريب SF-50M غير جاهز لأن corpus الحالي 30 سجلًا فقط ويفتقد msa**
- **المرحلة التالية المقترحة:** توسيع corpus عبر Phase 18 loop ثم إعادة `make phase19-readiness`.
- **القاموس/المسار اللغوي الحالي:** `msa + saudi` فقط؛ تم تحديث `default_registry.yaml` و`safety_terms.yaml` لفجوات finance/religion/security.
- **تاريخ آخر تحديث:** 2026-05-22

---

## جدول حالة المراحل

| المرحلة | الاسم | الحالة | الإذن |
|---------|------|--------|-------|
| Phase 0 | Project Governance & Execution Plan | ✅ | ✅ |
| Phase 1 | Project Foundation | ✅ | ✅ |
| Phase 2 | Core Brain Skeleton | ✅ | ✅ |
| Phase 3 | Language Understanding Layer | ✅ | ✅ |
| Phase 3.5 | Saudi Dialect Lexicon Import from Mo3jam | ✅ (بنية + dry-run) | ✅ |
| Phase 3.6 | Saudi Seed v1 Lexicon Integration (user-authored 516 entries) | ✅ | ✅ |
| Phase 4 | General Chat First | ✅ | ✅ |
| Phase 5 | Dialogue Dataset Preparation | ✅ | ✅ |
| Phase 5.5 | Sovereign Acceleration Layer | ✅ | ✅ |
| Phase 6 | Native SF.AI Small Language Model | ✅ (بنية + scaffolding) | ✅ |
| Phase 7 | Web Research, Crawling, Extraction, Summarization | ✅ (offline-ready) | ✅ |
| Phase 8 | Local RAG Foundation | ✅ | ✅ |
| Phase 9 | Frontend Chat Interface | ✅ | ✅ |
| Phase 10 | Later Domains Skeleton | ✅ | ✅ |
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack | ✅ | ✅ |
| Governance Layer | Engineering Standards قبل Phase 12 | ✅ | ✅ |
| Constitution Layer | Engineering & Linguistic Constitution قبل Phase 12 | ✅ | ✅ |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | ✅ completed_with_limits | ✅ |
| Phase 13 | Tiny LM Smoke Training | ✅ completed_with_limits | ✅ |
| Phase 14 | SF-10M v0.1 Training Run | ✅ completed_with_limits | ✅ |
| Phase 15 | Generator Adapter for ChatModule | ✅ completed_as_safe_adapter | ✅ |
| Phase 16 | Evaluation, Safety, and Saudi/MSA Style Harness | ✅ completed_lab_runtime_separate | ✅ |
| Phase 17 | Local Memory/RAG Bridge into Chat | ✅ completed_local_bridge | ✅ |
| Phase 18 | Data Expansion Loop v1 | ✅ completed_governed_loop | ✅ |
| Phase 19 | SF-50M Candidate Training | readiness_gate_active_not_ready | ✅ |
| Phase 20 | Domain Activation Gates | معلّقة | ⏳ |

---

## ما الجديد منذ Phase 7

### Phase 11 — Sovereign Corpus Governance & Saudi/MSA Dialogue Pack

- أضيفت [CORPUS_GOVERNANCE.md](./CORPUS_GOVERNANCE.md) لتحديد شروط دخول عينة إلى training pack.
- أضيفت [DIALOGUE_DATASET_RUBRIC.md](./DIALOGUE_DATASET_RUBRIC.md) لتعريف `gold/silver/bronze`.
- أضيف [data/corpus/chat/jsonl/README.md](../data/corpus/chat/jsonl/README.md) بمثال JSONL صالح.
- أضيفت `sf_ai/datasets/corpus_governance.py`:
  - `audit_record_for_training`
  - `audit_jsonl_file_for_training`
  - `audit_jsonl_directory_for_training`
  - `CorpusGovernanceReport`
- أضيف `scripts/audit_training_corpus.py` وهدف `make corpus-audit` كبوابة preflight قبل Phase 12.
- أضيف endpoint حي: `GET /system/corpus-audit` لعرض جاهزية corpus من المتصفح/API.
- أضيف inventory شامل للمصادر:
  - `make source-inventory`
  - `GET /system/source-inventory`
  - يفرّق بين chat corpus، وملف مهام اللهجة السعودية، وقاموس Saudi Seed الخاص، وموضع Mo3jam المؤجل.
- نتيجة الجرد المحلي الحالي: 1548 سجلًا مرجعيًا خاصًا غير مرفوع (`1032` مهمة لهجة سعودية + `516` مدخل قاموس سعودي)، لكنها ليست chat corpus مباشرًا.
- أضيف `data/corpus/chat/jsonl/first_dialogue_seed.jsonl`: seed صغير فيه 20 محادثة سعودية `gold`، مشتقة من مرجع Saudi Seed المحلي، مع `source/license/training_allowed/quality`.
- أضيف `data/corpus/chat/jsonl/protected_terms_seed_v1.jsonl`: seed صغير فيه 10 محادثات سعودية `gold` لتغطية protected terms المتبقية.
- نتيجة الوضع الحالي بعد `make corpus-audit`: `READY_FOR_PHASE_12_TOKENIZER_TRAINING` بعدد `30/30`.
- نتيجة تدريب Phase 12: `artifacts/tokenizers/sf_bpe/v1`, `vocab=261`, `merges=218`, `sf_origin=true`.
- نتيجة `make phase12-readiness`: يعرض أن v1 اكتمل، مع استمرار `missing_required_dialects=msa` قبل أي إعادة تدريب متوازنة.
- أضيف حقل `provenance.quality` إلى schema.
- أضيف حقل `provenance.training_allowed` إلى schema، وصار شرطًا في corpus governance.
- قيود Phase 11: `domain=chat`, `lang=ar`, `dialect ∈ {msa, saudi}`, ووجود user+assistant وsource/license/quality/training_allowed.
- أضيفت طبقة Governance & Engineering Standards قبل Phase 12:
  - [PROJECT_IDENTITY.md](./PROJECT_IDENTITY.md)
  - [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
  - [AGENT_INSTRUCTIONS.md](./AGENT_INSTRUCTIONS.md)
  - [PROJECT_MAP.md](./PROJECT_MAP.md)
  - [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)
- أضيفت طبقة SF.AI Engineering & Linguistic Constitution قبل Phase 12:
  - [PROJECT_CONSTITUTION.md](./PROJECT_CONSTITUTION.md)
  - [LANGUAGE_SEGMENTATION.md](./LANGUAGE_SEGMENTATION.md)
  - [TOKENIZATION_POLICY.md](./TOKENIZATION_POLICY.md)
  - [DATASET_GOVERNANCE.md](./DATASET_GOVERNANCE.md)
  - [AGENT_ENGINEERING_RULES.md](./AGENT_ENGINEERING_RULES.md)
- أضيفت موارد tokenization:
  - [protected_terms_saudi.txt](../resources/tokenization/protected_terms_saudi.txt)
  - [preferred_merges.txt](../resources/tokenization/preferred_merges.txt)
  - [tokenization_rules.yaml](../resources/tokenization/tokenization_rules.yaml)
- أضيف `make tokenization-audit` لفحص policy/coverage قبل Phase 12 دون تدريب أو كتابة artifacts.
- نتيجة `make tokenization-audit ARGS="--show-missing"` الحالية:
  - protected terms total: 30
  - covered: 30
  - coverage: 100%
  - missing examples: none
- أضيف [PHASE12_TOKENIZER_V1_REPORT.md](./PHASE12_TOKENIZER_V1_REPORT.md) كتقرير تنفيذ Phase 12:
  - status: COMPLETED_WITH_LIMITS
  - vocab_size: 261
  - merges: 218
  - missing MSA remains documented
- أضيف `GET /system/phase12-readiness` كقرار API موحد:
  - `preflight_pass=false` حتى إضافة `msa`
  - `can_train_now=false` للتدريب المتوازن اللاحق
  - `missing_required_dialects=["msa"]`
  - `required_confirmation_flag=--confirm-phase12-permission`
- أضيف `make phase12-readiness` كقرار CLI مطابق للـ API بدون restart للسيرفر.
- بدأ وانتهى tokenizer training لPhase 12.
- بدأ وانتهى Phase 13 smoke LM training:
  - model: `sf-10m`
  - params: 6,361,600
  - steps: 20
  - first loss: 5.6638
  - last loss: 4.7539
  - eval loss: 4.4346
  - generation: non-empty, repetitive as expected
  - report: [PHASE13_SMOKE_TRAINING_REPORT.md](./PHASE13_SMOKE_TRAINING_REPORT.md)
- بدأ وانتهى Phase 14 SF-10M v0.1:
  - requested steps: 80
  - completed steps: 33
  - first loss: 5.6638
  - last loss: 4.7535
  - eval loss: 4.0777
  - perplexity: 59.01
  - generation: non-empty, repetitive as expected
  - report: [PHASE14_SF10M_V0_1_REPORT.md](./PHASE14_SF10M_V0_1_REPORT.md)
- بدأ وانتهى Phase 15 Generator Adapter:
  - أضيف `GenerationPolicy` لتعطيل التوليد افتراضيًا ومنع safety/skeleton/low-confidence routes.
  - أضيف `NativeGenerator` كـ lazy adapter يحمّل tokenizer/checkpoint السياديين فقط.
  - بقي `ChatModule` على القوالب، ويصدر metadata `generator=template`.
  - أضيف حقل `generator` إلى API وشاشة `/ui/chat`.
  - tests at completion: `367 passed`.
  - report: [PHASE15_GENERATOR_ADAPTER_REPORT.md](./PHASE15_GENERATOR_ADAPTER_REPORT.md)
- بدأ وانتهى Phase 16 Evaluation/Safety/Style Harness:
  - prompt suites:
    - `eval/prompts/saudi_msa_chat_v1.jsonl`
    - `eval/prompts/safety_v1.jsonl`
  - report: `eval/reports/sf_10m_eval_v1.json`
  - result: `15/15`, `PASS_WITH_RUNTIME_BLOCKED`
  - runtime activation: `false` بسبب تكرار عينة Phase 14.
  - سُمح لاحقًا بوضع تجربة فردي لسامي فقط عبر `SF_NATIVE_GENERATOR_EXPERIMENTAL=true` دون تغيير gate العام.
  - docs: [EVALUATION_PLAN.md](./EVALUATION_PLAN.md)
- بدأ وانتهى Phase 17 Local Memory/RAG Bridge:
  - أضيف `sf_ai/modules/chat/context_builder.py`.
  - أضيف `sf_ai/modules/chat/rag_bridge.py`.
  - `ChatModule` صار يقبل `rag_bridge` اختياريًا.
  - API/UI يعرضان `rag=used/not_used`.
  - تحسين واجهة `/ui/chat` إلى تصميم فاتح، خطوط أكبر، تشخيص أوضح، وتسميات عربية للـ generator/rag/dispatch.
  - لا web crawling تلقائي ولا embeddings جاهزة.
  - docs: [PHASE17_RAG_BRIDGE_REPORT.md](./PHASE17_RAG_BRIDGE_REPORT.md)
- بدأ وانتهى Phase 18 Data Expansion Loop v1:
  - أضيف زر `تصدير` في `/ui/chat` لإخراج JSONL محلي للمراجعة.
  - export يضع `training_allowed=false` و`quality=needs_review`.
  - أضيف `scripts/prepare_dialogue_batch.py`.
  - أضيف `sf_ai/datasets/dialogue_batch.py`.
  - أضيف `artifacts/reports/dialogue_batch_report.json`.
  - لا تدخل المحادثات التدريب تلقائيًا.
  - docs: [DATA_IMPROVEMENT_LOOP.md](./DATA_IMPROVEMENT_LOOP.md)
- بدأ Phase 19 كبوابة جاهزية قبل تدريب SF-50M:
  - أضيف `make phase19-readiness`.
  - أضيف `GET /system/phase19-readiness`.
  - القرار الحالي: `NOT_READY_EXPAND_CORPUS_FIRST`.
  - السبب: corpus الحالي `30` سجلًا فقط والحد الأدنى العملي الحالي `5000`.
  - أضيف lab bridge للرسائل غير الحساسة حتى يختبر سامي المولد الخام عبر مجالات skeleton داخل المختبر المحلي.
  - docs: [PHASE19_READINESS_REPORT.md](./PHASE19_READINESS_REPORT.md)

### Phase 3.6 — Saudi Seed v1 (تأليف المستخدم)

- نقل `saudi_dialect_lexicon_full_seed_v1` (516 مدخل) إلى `resources/lexicons/imported/saudi_seed_v1/`.
- مهام التدريب نقلت إلى `data/corpus/dialects/saudi/jsonl/saudi_dialect_training_tasks_seed_v1.jsonl`.
- Loader في [sf_ai/datasets/saudi_seed.py](../sf_ai/datasets/saudi_seed.py) مع safety filter (high confidence + not sensitive + not review-required → ~300 مدخل runtime-safe).
- DialectMapper يقبل القاموس عبر `ENABLE_SAUDI_SEED_V1_LEXICON=true` (خارج القواميس الأصلية).
- توثيق: [SOURCE_DISCOVERY_SAUDI_SEED.md](./SOURCE_DISCOVERY_SAUDI_SEED.md) + [LEXICON_STATS.md](./LEXICON_STATS.md).
- اختبارات: 15 في `test_saudi_seed.py`.

### Phase 8 — Local RAG Foundation

**`sf_ai/memory/`** — سيادي بالكامل:
- `schemas.py` — Document / Chunk / RetrievalResult.
- `long_term.py` — LongTermMemory + `chunk_text` (paragraph/sentence-aware).
- `sparse_store.py` — **BM25 نقي بـ Python** فوق tokenizer + ArabicNormalizer.
- `vector_store.py` — `HashingVectorStore` (سيادي، يستخدم BLAKE2b vectorizer من Phase 2) + `QdrantVectorStore` stub.
- `retrieval.py` — `HybridRetriever` يخلط sparse + vector بأوزان (0.7 / 0.3).
- `short_term.py` — re-export ConversationStore.

**اختبارات:** 14 في `test_rag_sparse_retrieval.py`. **توثيق:** [RAG_PLAN.md](./RAG_PLAN.md).

### Phase 9 — Frontend Chat Interface

- `apps/api/static/chat.html` — صفحة واحدة عربية RTL:
  - منطقة رسائل + خانة إدخال (Enter للإرسال، Shift+Enter لسطر جديد).
  - لوحة تشخيص جانبية: domain / intent / confidence / dispatch / route_reason / language / dialect / safety / fallback / signals / corrections / safety flags.
  - session_id محفوظ في localStorage.
  - زر مسح المحادثة يبدأ جلسة جديدة ويعيد لوحة التشخيص.
  - كل رسالة تعرض timestamp مختصر.
  - **لا CDNs، لا Node، لا build step** — تعمل من المتصفح مباشرة.
- `apps/api/routers/ui.py` — GET `/ui/chat` يخدم الـ HTML.
- `apps/api/main.py` — أضيف `ui.router`، و GET `/chat` redirect → `/ui/chat`.
- اختبارات: 4 في `test_chat_ui.py`.

### Phase 9 Polish — Comfortable Chat + Accurate Routing

- أضيفت intents يومية جديدة: `chat.thanks`, `chat.affirmation`, `chat.negation`, `chat.help`, `chat.confused`, `chat.who_made_you`, `chat.farewell`.
- أضيفت intent لتفضيل اللغة/اللهجة: `chat.language_preference`.
- أضيفت intent لاستيضاح المتابعة القصيرة: `chat.clarification` (مثل `عندي؟`).
- تمت مزامنة `default_registry.yaml` و `resources/lexicons/intents.yaml` حتى لا تعود `من صنعك` إلى `chat.identity`.
- `ChatModule` صار يرد بقوالب أقصر وأدفأ للحديث العام.
- `ResponseComposer` صار يعطي ردودًا مخصصة لكل مجال skeleton/safety بدل رسالة عامة.
- `scripts/run_chat_server.sh` يشغّل API على 8123 ويفعّل `ENABLE_SAUDI_SEED_V1_LEXICON=true` افتراضيًا بدون side effects داخل `main.py`.
- سياسة اللغة الحالية: **العربية الفصحى + اللهجة السعودية فقط**. اللهجات الأخرى غير محمّلة افتراضيًا، ويمكن تفعيلها لاحقًا عبر flag صريح.
- تنبيه واقعي: النظام الآن rule-based + routing، وليس نموذج توليد حر بعد. التوليد الذكي يحتاج تدريب SF native LM على بيانات سامي.
- ملف الأهداف الحالي: [CURRENT_GOALS.md](./CURRENT_GOALS.md).

**Audit حي بعد التحسين:**
```
شكرا       → chat/chat.thanks        fallback=False
تمام       → chat/chat.affirmation   fallback=False
لا         → chat/chat.negation      fallback=False
ساعدني     → chat/chat.help          fallback=False
مش فاهم    → chat/chat.confused      fallback=False
من صنعك    → chat/chat.who_made_you  fallback=False
وداعا      → chat/chat.farewell      fallback=False
سعودي      → chat/chat.language_preference
عندي؟      → chat/chat.clarification
وشلونك     → chat/chat.smalltalk        fallback=False
عندي سؤال  → chat/chat.clarification    response="تفضّل، وش سؤالك؟ ..."
```

**اختبار حي تم:**
```
GET  /health        → {"status":"ok","project":"SF.AI","phase":"Phase 11"}
GET  /ui/chat       → HTML chat UI (RTL Arabic)
GET  /system/corpus-audit → READY_FOR_PHASE_12_TOKENIZER_TRAINING, 30/30
POST /chat/message  ← {"message":"شلونك"} → domain=chat, intent=chat.smalltalk,
                     dialect=saudi, response="بخير، شكرًا لسؤالك. عندك أنت؟"
```

---

### Phase 10 — Later Domains Skeleton

أُضيفت هياكل المجالات اللاحقة بدون تفعيل تنفيذ فعلي:

`coding`, `data`, `files`, `legal`, `medical`, `finance`, `education`, `religion`, `social`, `writing`, `translation`, `image`, `audio`, `security`, `business`, `ecommerce`.

لكل مجال:
- `manifest.yaml` يصرّح `status: skeleton_only`.
- `module.py` يرث من `SkeletonDomainModule` ولا ينفّذ عملًا فعليًا.
- `__init__.py` يصدّر كلاس المجال.
- `allowed_tools: []` حتى لا توجد أدوات تشغيل مفعّلة.
- `limitations` واضحة تمنع الوعد بقدرات غير موجودة.

المجالات الحساسة (`legal`, `medical`, `finance`, `security`, `religion`) مضبوطة على:
- `requires_safety: true`
- `status: skeleton_only`

الـ Orchestrator ما زال لا يفعّل أي Module غير `chat`; المجالات المؤجلة تذهب إلى `ResponseComposer` برسائل آمنة/صريحة.

## نتائج الاختبارات

```
388 passed in 2.92s
```

| ملف | عدد |
|------|------|
| test_arabic_normalizer.py | 16 |
| test_bpe_tokenizer.py | 13 |
| test_capability_registry.py | 5 |
| test_chat_module.py | 12 |
| test_chat_native_generator.py | 9 (Phase 15 + lab mode) |
| test_chat_rag_bridge.py | 6 (Phase 17) |
| test_chat_ui.py | 4 (Phase 9/19 status) |
| test_checkpoints.py | 7 |
| test_conversation_state.py | 8 |
| test_corpus_governance.py | 6 (Phase 11) |
| test_dataset_validators.py | 28 |
| test_dialogue_batch_preparation.py | 3 (Phase 18) |
| test_dialect_mapper.py | 7 |
| test_health.py | 8 |
| test_intent_detector.py | 7 |
| test_mo3jam_importer.py | 13 |
| test_new_chat_intents.py | 31 (Phase 9 polish) |
| test_nlp_pipeline.py | 9 |
| test_orchestrator.py | 7 |
| test_phase10_skeleton_domains.py | 4 (Phase 10) |
| test_phase16_eval_harness.py | 3 (Phase 16) |
| test_phase19_readiness.py | 2 (Phase 19) |
| test_rag_sparse_retrieval.py | 14 (Phase 8) |
| test_research_summarizer.py | 20 |
| test_response_composer.py | 6 |
| test_router.py | 8 |
| test_router_with_nlp.py | 5 |
| test_saudi_seed.py | 15 (Phase 3.6) |
| test_semantic_explorer.py | 10 |
| test_tiny_transformer.py | 26 |
| test_training_config.py | 8 |
| test_training_device.py | 14 |
| test_typo_corrector.py | 5 |
| test_web_extractor.py | 18 |
| **Total** | **388** |

---

## الشاشة جاهزة للتجريب

السيرفر يعمل **الآن** في الخلفية على المنفذ 8123.

افتح في المتصفح:
```
http://127.0.0.1:8123/ui/chat
```

أمثلة جرّبها:
- `مرحبا` → chat.greeting
- `شلونك` → dialect=saudi، intent=chat.smalltalk
- `عندي؟` → chat.clarification
- `سعودي` → chat.language_preference
- `من انت` → chat.identity (يشرح السيادة المعرفية)
- `وش تقدر تسوي` → chat.capability
- `عندي ألم في الراس` → domain=medical, requires_safety=true (رد آمن)
- `ابحث في الويب` → domain=web (skeleton_only ⇒ رسالة "غير مفعّل بعد")

اللوحة الجانبية تعرض **كل قرار توجيه** + الإشارات + التصحيحات.

لتشغيل السيرفر يدويًا في المستقبل:
```bash
cd /Users/sami/workSF/SF.AI
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8123
```

أو الأفضل:
```bash
make api
```

> ملاحظة: المنفذ 8000/8765 مشغول بمشروع آخر للمستخدم، لذلك نستخدم 8123.

---

## بروتوكول الانتقال

التفويض الحالي من سامي: استمر في المراحل المسجلة دون انتظار موافقات جديدة، مع توثيق رقم الرحلة، القاموس المتبع، نتائج الاختبارات، وفحص الحساسية قبل أي رفع.
