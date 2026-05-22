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

- [docs/PROJECT_IDENTITY.md](./docs/PROJECT_IDENTITY.md) — هوية المشروع وحدوده.
- [docs/ENGINEERING_RULES.md](./docs/ENGINEERING_RULES.md) — قواعد الهندسة غير القابلة للكسر.
- [docs/AGENT_INSTRUCTIONS.md](./docs/AGENT_INSTRUCTIONS.md) — workflow أي Agent يعمل على المشروع.
- [docs/PROJECT_MAP.md](./docs/PROJECT_MAP.md) — خريطة المجلدات ومسؤولية كل مسار.
- [docs/PROJECT_LIFECYCLE.md](./docs/PROJECT_LIFECYCLE.md) — دورة الحياة من corpus إلى runtime.

---

## الهدف الحالي

- **الأولوية الحالية:** تجهيز المسار السيادي الآمن قبل تدريب Phase 12.
- **الشات الحالي:** runtime rule-based + routing، وليس LLM مولّدًا بعد.
- **البيانات الحالية:** seed صغير `20/20` يمر `corpus-audit`.
- **التدريب:** لم يبدأ، ولا يبدأ إلا بإذن صريح.

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
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit |

**لا انتقال بين المراحل بدون إذن صريح من المستخدم.**

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

ثم افتح:

```text
http://127.0.0.1:8123/ui/chat
```

### الـ Endpoints المتوفرة الآن

- `GET /health` — فحص صحة الخدمة.
- `GET /system/status` — حالة المراحل والمكونات.
- `GET /system/corpus-audit` — جاهزية corpus قبل Phase 12.
- `GET /system/source-inventory` — جرد مصادر البيانات والمراجع.
- `POST /chat/message` — رسالة إلى الـ Orchestrator.
- `GET /ui/chat` — شاشة المحادثة.

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
- لا تشغيل training أو crawling أو phase جديدة بدون إذن صريح.
- لا خلط بين `data/corpus/` و `resources/lexicons/`.

التفاصيل في [PROJECT_PRINCIPLES.md](./PROJECT_PRINCIPLES.md).

---

## الترخيص

سيُحدد لاحقًا.
