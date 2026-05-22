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

- **الرحلة الحالية:** Phase 21 / 30 — خارطة الوصول إلى حوار مولّد مقنع مثبتة بعد Phase 20.
- **الأولوية الحالية:** اختبار مختبر سامي المحلي، تصدير محادثات مراجعة، وتكبير corpus المحكوم قبل تدريب SF-50M.
- **الشات الحالي:** runtime rule-based + routing، وليس LLM مولّدًا بعد.
- **البيانات الحالية:** seed سعودي صغير `30/30` يمر `corpus-audit`؛ ما زال `msa` مطلوبًا قبل تشغيل جودة لغوية متوازنة.
- **التدريب:** Phase 12 tokenizer v1 وPhase 13 smoke LM وPhase 14 SF-10M v0.1 اكتملت من بيانات SF.AI فقط، مع قيود موثقة.
- **المولّد:** Phase 15 أضاف NativeGenerator adapter، ومختبر سامي المحلي يفعّله للتجربة عبر flags التشغيل.
- **التقييم:** Phase 16 مرّر `15/15` prompt cases؛ الجودة اليومية لم تنضج بعد، لكن المختبر المحلي مفتوح للتجربة والتطوير.
- **الذاكرة المحلية:** Phase 17 أضاف ChatRagBridge اختياريًا؛ runtime الافتراضي لا يحمّل ذاكرة ولا يزحف ويب.
- **دورة البيانات:** Phase 18 أضاف تصدير مراجعة من الواجهة و`prepare_dialogue_batch.py`; لا تعلم تلقائي.
- **جاهزية SF-50M:** Phase 19 أضاف `make phase19-readiness`; القرار الحالي `NOT_READY_EXPAND_CORPUS_FIRST`.
- **بوابات المجالات:** Phase 20 أضاف `make phase20-gates` و`GET /system/phase20-gates`; المجال النشط الوحيد هو `chat`.
- **طريق التوليد المقنع:** Phase 24 هو أول تدريب جودة مفيد، Phase 26 أول فرصة لحوار قصير مقنع، وPhase 28 هدف الحوار المولّد المستقر.
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
| Phase 22 | Gold Dialogue Corpus v2 — planned |
| Phase 23 | Tokenizer v2 Retrain & Audit — planned |
| Phase 24 | SF-10M v0.2 Quality Training — planned |
| Phase 25 | Generated Chat Canary v1 — planned |
| Phase 26 | SF-50M v0.1 Dialogue Model — planned |
| Phase 27 | Dialogue Evaluation v2 — planned |
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
- لا synthetic LLM data في corpus السيادي.
- لا تشغيل crawling أو phase خارج الخطة بدون توثيق وإذن واضح؛ التفويض الحالي يسمح بمتابعة التدريب والمراحل المسجلة فقط مع فحص الحساسية.
- لا خلط بين `data/corpus/` و `resources/lexicons/`.
- لا تغيير في `resources/tokenization/` بدون توثيق واختبارات.

التفاصيل في [PROJECT_PRINCIPLES.md](./PROJECT_PRINCIPLES.md).

---

## الترخيص

سيُحدد لاحقًا.
