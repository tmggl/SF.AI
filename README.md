# SF.AI

منصة ذكاء اصطناعي خاصة، تُبنى تدريجيًا، بسيادة معرفية كاملة قدر الإمكان.

> **نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.**

---

## ما هو SF.AI

- **ليس** chatbot بسيطًا.
- **ليس** wrapper فوق GPT أو Claude أو Gemini.
- **ليس** واجهة فوق نموذج جاهز.
- **هو** مشروع لبناء نظام ذكاء اصطناعي خاص بنا من الصفر، يبدأ بالحوار العام، ثم البحث في الويب والتلخيص، ثم مجالات أخرى لاحقًا.

اقرأ المبادئ الكاملة في [PROJECT_PRINCIPLES.md](./PROJECT_PRINCIPLES.md).

### وثائق الحوكمة قبل التدريب

قبل أي Phase جديدة، خصوصًا Phase 12 وما بعدها، اقرأ:

- [docs/PROJECT_CONSTITUTION.md](./docs/PROJECT_CONSTITUTION.md) — الدستور الهندسي واللغوي الأعلى.
- [docs/LANGUAGE_SEGMENTATION.md](./docs/LANGUAGE_SEGMENTATION.md) — سياسة الفصحى/السعودي وArabizi/code.
- [docs/TOKENIZATION_POLICY.md](./docs/TOKENIZATION_POLICY.md) — سياسة tokenizer وprotected terms.
- [docs/DATASET_GOVERNANCE.md](./docs/DATASET_GOVERNANCE.md) — قواعد dataset/provenance.
- [docs/AGENT_ENGINEERING_RULES.md](./docs/AGENT_ENGINEERING_RULES.md) — قواعد الوكلاء الهندسية واللغوية.
- [docs/PHASE12_PREFLIGHT_REPORT.md](./docs/PHASE12_PREFLIGHT_REPORT.md) — تقرير الجاهزية قبل Phase 12، لا يعني إذن تدريب.
- [docs/PROJECT_IDENTITY.md](./docs/PROJECT_IDENTITY.md) — هوية المشروع وحدوده.
- [docs/ENGINEERING_RULES.md](./docs/ENGINEERING_RULES.md) — قواعد الهندسة غير القابلة للكسر.
- [docs/AGENT_INSTRUCTIONS.md](./docs/AGENT_INSTRUCTIONS.md) — workflow أي Agent يعمل على المشروع.
- [docs/PROJECT_MAP.md](./docs/PROJECT_MAP.md) — خريطة المجلدات ومسؤولية كل مسار.
- [docs/PROJECT_LIFECYCLE.md](./docs/PROJECT_LIFECYCLE.md) — دورة الحياة من corpus إلى runtime.
- [docs/GENERATIVE_ROADMAP.md](./docs/GENERATIVE_ROADMAP.md) — خارطة الوصول إلى حوار مولّد مقنع بعد Phase 20.
- [docs/SCALING_STRATEGY.md](./docs/SCALING_STRATEGY.md) — استراتيجية التكبير التدريجي من SF-10M إلى SF-1B+.

---

## الهدف الحالي

- **الرحلة الحالية:** Phase 27 / 30 — Dialogue Evaluation v2 + Corpus Expansion Plan اكتملت كاختبار baseline وخطة بيانات.
- **الأولوية الحالية:** تنفيذ توسعة corpus من `643` إلى `5000` داخل `msa + saudi`; لا تدريب `SF-50M` ولا Phase 28 الآن.
- **الشات الحالي:** runtime rule-based + routing، وليس LLM مولّدًا بعد.
- **البيانات الحالية:** corpus موثق `643` سجلًا يمر `corpus-audit`: `344` سعودي + `299` فصحى. آخر tokenizer v2 وSF-10M v0.2 استُخدما corpus Phase 22 عند `500` سجل، والتوسعة الجديدة بدأت بعد Phase 27.
- **التدريب:** Phase 12 tokenizer v1 وPhase 13 smoke LM وPhase 14 SF-10M v0.1 وPhase 23 tokenizer v2 وPhase 24 SF-10M v0.2 اكتملت من بيانات SF.AI فقط.
- **المولّد:** `SF-10M v0.2` تحسّن رقميًا لكنه غير جاهز كحوار مقنع؛ Phase 25 أضاف canary guard يمنع الرد الضعيف ويرجع للقالب.
- **التقييم:** Phase 27 مرّر `19/19` turn في حوار متعدد الأدوار، لكنه أكد أن الردود ما زالت `template` وأن المولد غير جاهز.
- **الذاكرة المحلية:** Phase 17 أضاف ChatRagBridge اختياريًا؛ runtime الافتراضي لا يحمّل ذاكرة ولا يزحف ويب.
- **دورة البيانات:** Phase 18 أضاف تصدير مراجعة من الواجهة و`prepare_dialogue_batch.py`; وPhase 22 يعتمد الآن أيضًا دفعات مباشرة يؤلفها/يراجعها الوكيل بتفويض موثق، بدون انتظار حفظ أو تصدير من سامي.
- **جاهزية SF-50M:** Phase 26 أضاف `make phase26-readiness` و`GET /system/phase26-readiness`; القرار الحالي `NOT_READY_EXPAND_CORPUS_AND_IMPROVE_SF10M`.
- **بوابات المجالات:** Phase 20 أضاف `make phase20-gates` و`GET /system/phase20-gates`; المجال النشط الوحيد هو `chat`.
- **طريق التوليد المقنع:** لا تعرض `SF-10M v0.2` كنجاح حواري. Phase 27 نجح كاختبار توجيه وقوالب فقط، وقرر أن Phase 28 و`SF-50M` لا يبدآن قبل توسعة corpus وإصلاح canary.
- **Corpus v2:** Phase 22 أضاف `make phase22-readiness` و`make phase22-plan` و`make phase22-next-batch` و`make phase22-completion-gate` و`make phase22-review-intake`; الوضع الحالي 500/500، وفيه ثمان دفعات فصيحة `dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl` وسبع دفعات سعودية `dialogue_batch_v2_saudi_001.jsonl` إلى `dialogue_batch_v2_saudi_007.jsonl` وأربع دفعات مرنة `dialogue_batch_v2_flex_001.jsonl` إلى `dialogue_batch_v2_flex_004.jsonl` إضافة إلى seed فصيح للمصطلحات `protected_terms_msa_seed_v1.jsonl`. التوازن النهائي مكتمل (`msa=250`, `saudi=250`) ولا توجد دفعة تالية في Phase 22. الواجهة تعرض بوابة Phase 22 الحية وجودة التصدير كمختبر اختياري فقط، أما بناء corpus الحالي فتم مباشرة عبر الوكيل. `phase22-completion-gate` يرجع الآن `PHASE22_COMPLETE_READY_FOR_PHASE23`.
- **Tokenizer v2:** Phase 23 أضاف `artifacts/tokenizers/sf_bpe/v2/` و`make phase23-tokenizer-audit`; الحالة `COMPLETED_READY_FOR_PHASE24`, `vocab=4493`, `merges=4386`, وprotected Saudi terms تحسنت من متوسط 4.0 tokens في v1 إلى 2.3 في v2.
- **SF-10M v0.2:** Phase 24 درّب النموذج 2000 خطوة على tokenizer v2 وcorpus المتوازن: loss `8.4751 → 2.8256`, eval loss `2.5779`, perplexity `13.17`. القرار: `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED` لأن التوليد لا يزال غير متماسك.
- **Canary v1:** Phase 25 أضاف `GenerationGuard` و`SF_GENERATOR_CANARY`; التجربة الحقيقية على v0.2 حُجبت بـ `generation_guard:malformed_token` وبقي الرد من القالب.
- **قرار Phase 26:** `SF-50M` غير جاهز: corpus الحالي `643` فقط والحد العملي `5000`، وruntime quality/hallucination/repetition gates لم تنجح بعد. التقرير: [docs/PHASE26_SF50M_READINESS_REPORT.md](./docs/PHASE26_SF50M_READINESS_REPORT.md).
- **نتيجة Phase 27:** `make phase27-dialogue-eval` مرّر `19/19` turn في suite متعدد الأدوار، لكن كل الردود `template`، و`open_generator_ready=false`. بعد تنظيف الحوارات التشغيلية صارت خطة التوسعة: `4357` سجلًا إضافيًا، `9` دفعات كبيرة تقريبًا، بالتساوي `msa=2201` و`saudi=2156`. التقرير: [docs/PHASE27_DIALOGUE_EVAL_V2_REPORT.md](./docs/PHASE27_DIALOGUE_EVAL_V2_REPORT.md).
- **دفعات توسعة:** أضيفت Batch 001 بإجمالي 50 سجلًا، ثم Batch 002 وBatch 003 الكبيرتان بإجمالي 1000 سجل، كل واحدة `250` فصيح + `250` سعودي. التقارير: [docs/PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md), [docs/PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md), [docs/PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md).
- **تنظيف corpus:** أضيف فلتر يمنع الحوارات التشغيلية/الهندسية/الخاصة بسامي من التدريب؛ حُذف `907` سجلًا وبقي `643` سجلًا طبيعيًا. التقرير: [docs/CORPUS_OPERATIONAL_FILTER_REPORT.md](./docs/CORPUS_OPERATIONAL_FILTER_REPORT.md).
- **فصل المستخدمين:** كل export وcorpus record يحمل الآن `owner_user_id/created_by_user_id/target_user_id/user_scope`; المسار الحالي `sami-local` و`single_user` لتجهيز التوسع لاحقًا بدون خلط بيانات.
- **القاموس المتبع:** العربية الفصحى + السعودية فقط، مع `Saudi Seed v1` كمرجع خاص و`safety_terms.yaml` كبوابة حساسة.

---

## المراحل

كل المراحل موثقة في [docs/EXECUTION_PLAN.md](./docs/EXECUTION_PLAN.md).
الحالة الحالية في [docs/PHASE_STATUS.md](./docs/PHASE_STATUS.md).

| المرحلة | الاسم |
|---------|------|
| Phase 0 | Project Governance & Execution Plan |
| Phase 1 | Project Foundation |
| Phase 2 | Core Brain Skeleton |
| Phase 3 | Language Understanding Layer |
| Phase 4 | General Chat First |
| Phase 5 | Dialogue Dataset Preparation |
| Phase 5.5 | Sovereign Acceleration Layer |
| Phase 6 | Native SF.AI Small Language Model |
| Phase 7 | Web Research, Crawling, Extraction, Summarization |
| Phase 8 | Local RAG Foundation |
| Phase 9 | Frontend Chat Interface |
| Phase 10 | Later Domains Skeleton |
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack |
| Governance Layer | Engineering Standards قبل Phase 12 |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit — completed with limits |
| Phase 13 | Tiny LM Smoke Training — completed with limits |
| Phase 14 | SF-10M v0.1 Training Run — completed with limits |
| Phase 15 | Generator Adapter for ChatModule — completed as safe adapter |
| Phase 16 | Evaluation, Safety, and Saudi/MSA Style Harness — completed; lab runtime separate |
| Phase 17 | Local Memory/RAG Bridge into Chat — completed as local bridge |
| Phase 18 | Data Expansion Loop v1 — completed as governed loop |
| Phase 19 | SF-50M Readiness Gate — active, corpus too small for training |
| Phase 20 | Domain Activation Gates — active, no domain auto-activated |
| Phase 21 | Generative Roadmap & Quality Targets — completed |
| Phase 22 | Gold Dialogue Corpus v2 — completed, 500/500, ready for Phase 23 tokenizer v2 |
| Phase 23 | Tokenizer v2 Retrain & Audit — completed, ready for Phase 24 |
| Phase 24 | SF-10M v0.2 Quality Training — completed with limits; runtime blocked |
| Phase 25 | Generated Chat Canary v1 — completed as guarded canary; real model blocked |
| Phase 26 | SF-50M v0.1 Readiness — completed; training blocked by scaling gates |
| Phase 27 | Dialogue Evaluation v2 and corpus expansion plan — completed with corpus expansion required |
| Phase 28 | SF-120M v0.1 Candidate — planned |
| Phase 29 | Runtime Hybrid Assistant v1 — planned |
| Phase 30 | Continuous Improvement Loop — planned |

**تفويض التنفيذ الحالي:** سامي أعطى إذنًا صريحًا بمتابعة التدريب والاختبارات والمراحل المسجلة في الرحلة، مع بقاء قواعد السيادة والسلامة وفحص الحساسية قبل الرفع.

---

## هيكل المشروع

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
│   ├── api/                       # FastAPI backend
│   └── web/                       # Next.js frontend (لاحقًا)
│
├── sf_ai/                         # نواة المشروع
│   ├── core/                      # orchestrator, router, semantic, composer, ...
│   ├── modules/                   # chat, web, research, ...
│   ├── memory/                    # short/long term, vector store
│   ├── tools/                     # web, files, data tools
│   ├── models/                    # tokenizer, transformer (لاحقًا)
│   ├── datasets/                  # data loaders & validators
│   └── training/                  # training tools (لاحقًا)
│
├── resources/lexicons/            # YAML lexicons
├── resources/tokenization/         # protected terms + tokenizer policy resources
├── data/                          # corpus & indexes
├── artifacts/                     # tokenizers, checkpoints, logs
├── tests/                         # pytest tests
├── scripts/                       # operational scripts
└── docs/                          # documentation + governance
```

---

## التشغيل المحلي (Phase 11)

> المراحل 0–11 مكتملة. شاشة المحادثة العربية تعمل محليًا، مع NLP rule-based وتوجيه سيادي بدون أي نموذج خارجي. التركيز اللغوي الحالي: العربية الفصحى + اللهجة السعودية فقط.

### المتطلبات
- Python 3.11+
- (اختياري) Docker + docker-compose

### التنصيب

```bash
pip install -e ".[dev]"
```

### تشغيل الـ API

```bash
make api
# أو
bash scripts/run_chat_server.sh
```

لفحص السيرفر بدون إيقافه أو إعادة تشغيله:

```bash
make server-status
```

لتشغيله بشكل detached إذا كان متوقفًا فقط:

```bash
make server-start
```

ثم افتح:

```text
http://127.0.0.1:8123/ui/chat
```

### الـ Endpoints المتوفرة الآن

- `GET /health` — فحص صحة الخدمة.
- `GET /system/status` — حالة المراحل والمكونات.
- `GET /system/corpus-audit` — جاهزية corpus قبل Phase 12.
- `GET /system/phase12-readiness` — قرار Phase 12 كامل: preflight + بوابة الإذن.
- `GET /system/source-inventory` — جرد مصادر البيانات والمراجع.
- `POST /chat/message` — رسالة إلى الـ Orchestrator.
- `GET /ui/chat` — شاشة المحادثة.

### فحوصات ما قبل Phase 12

```bash
make source-inventory
make corpus-audit
make tokenization-audit
make phase12-readiness
```

هذه الفحوصات لا تبدأ تدريبًا ولا تكتب artifacts.

حتى بعد نجاح الفحوصات، يرفض تدريب tokenizer البدء بدون إذن Phase 12 الصريح:

```bash
make train-bpe ARGS="--confirm-phase12-permission --corpus data/corpus/chat/jsonl --out artifacts/tokenizers/sf_bpe/v1"
```

لا تستخدم هذا العلم إلا بعد موافقة سامي الواضحة على بدء Phase 12.

تقرير الجاهزية الرسمي:

```text
docs/PHASE12_PREFLIGHT_REPORT.md
```

### الاختبارات

```bash
make test
# أو
pytest
```

---

## المحظورات الجوهرية

- لا OpenAI / Claude / Gemini APIs.
- لا أي نموذج جاهز / pretrained weights / pretrained embeddings / pretrained tokenizer.
- لا Llama / Gemma / Phi / Mistral / sentence-transformers / HuggingFace pretrained.
- لا LoRA فوق نموذج خارجي.
- لا synthetic LLM data من مصدر خارجي أو مجهول في corpus السيادي؛ يسمح فقط بحوار owner-delegated agent-authored إذا حمل provenance كاملًا وتفويض سامي.
- لا تشغيل crawling أو phase خارج الخطة بدون توثيق وإذن واضح؛ التفويض الحالي يسمح بمتابعة التدريب والمراحل المسجلة فقط مع فحص الحساسية.
- لا خلط بين `data/corpus/` و `resources/lexicons/`.
- لا تغيير في `resources/tokenization/` بدون توثيق واختبارات.

التفاصيل في [PROJECT_PRINCIPLES.md](./PROJECT_PRINCIPLES.md).

---

## الترخيص

سيُحدد لاحقًا.
