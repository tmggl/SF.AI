# PHASE_STATUS.md

## SF.AI — سجل حالة المراحل

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **المرحلة الحالية:** **Phase 11 — Sovereign Corpus Governance & Saudi/MSA Dialogue Pack**
- **حالة المرحلة الحالية:** **مكتملة كحوكمة وأدوات فحص؛ لا توجد بيانات تدريب فعلية بعد**
- **المرحلة التالية المقترحة:** Phase 12 — SF-BPE Tokenizer v1 Training & Audit
- **جاهزية Phase 12 الآن:** preflight audit جاهز؛ التدريب ينتظر JSONL صالح + إذن صريح.
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
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | ⏳ التالية بعد بيانات وموافقة | ⏳ |
| Phase 13 | Tiny LM Smoke Training | معلّقة | ⏳ |
| Phase 14 | SF-10M v0.1 Training Run | معلّقة | ⏳ |
| Phase 15 | Generator Adapter for ChatModule | معلّقة | ⏳ |
| Phase 16 | Evaluation, Safety, and Saudi/MSA Style Harness | معلّقة | ⏳ |
| Phase 17 | Local Memory/RAG Bridge into Chat | معلّقة | ⏳ |
| Phase 18 | Data Expansion Loop v1 | معلّقة | ⏳ |
| Phase 19 | SF-50M Candidate Training | معلّقة | ⏳ |
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
- نتيجة الوضع الحالي: `NOT_READY_FOR_TRAINING` لأن `data/corpus/chat/jsonl/` لا يحتوي ملفات JSONL تدريبية بعد.
- أضيف حقل `provenance.quality` إلى schema.
- قيود Phase 11: `domain=chat`, `lang=ar`, `dialect ∈ {msa, saudi}`, ووجود user+assistant وsource/license/quality.
- لم تُضف أي بيانات تدريب، ولم يبدأ tokenizer أو LM training.

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
GET  /health        → {"status":"ok","project":"SF.AI","phase":"Phase 10"}
GET  /ui/chat       → HTML chat UI (RTL Arabic)
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
332 passed in 2.40s
```

| ملف | عدد |
|------|------|
| test_arabic_normalizer.py | 16 |
| test_bpe_tokenizer.py | 13 |
| test_capability_registry.py | 5 |
| test_chat_module.py | 12 |
| test_chat_ui.py | 4 (Phase 9) |
| test_checkpoints.py | 7 |
| test_conversation_state.py | 8 |
| test_corpus_governance.py | 6 (Phase 11) |
| test_dataset_validators.py | 28 |
| test_dialect_mapper.py | 7 |
| test_health.py | 7 |
| test_intent_detector.py | 7 |
| test_mo3jam_importer.py | 13 |
| test_new_chat_intents.py | 31 (Phase 9 polish) |
| test_nlp_pipeline.py | 9 |
| test_orchestrator.py | 7 |
| test_phase10_skeleton_domains.py | 4 (Phase 10) |
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
| **Total** | **332** |

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

> **"اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"**
