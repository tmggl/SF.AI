# ARCHITECTURE.md

## SF.AI — البنية المعمارية العامة

> هذا ملف معماري حي. يُحدَّث مع كل مرحلة. الحالة الموثقة الآن: **Phase 2**.

---

## التدفق الكامل (الرؤية المستقبلية)

```
User
 ↓
Frontend (Phase 9)
 ↓
API (Phase 1+ — FastAPI)
 ↓
Language Understanding Layer (Phase 3)
 ↓
Orchestrator (Phase 2)
 ↓
Router (Phase 2 — Domain + Intent)
 ↓
Semantic Explorer (Phase 2 — local only)
 ↓
Global Capability Registry (Phase 2)
 ↓
Module (Phase 4: chat / Phase 7: web / Phase 7: research / ...)
 ↓
Tools / Memory / Dataset / Training
 ↓
Response Composer (Phase 2)
 ↓
Final Response
```

---

## ما هو فعّال الآن (Phase 2)

| المكون | الحالة | الملف |
|--------|--------|------|
| FastAPI app | active | [apps/api/main.py](../apps/api/main.py) |
| `/health` | active | [apps/api/routers/health.py](../apps/api/routers/health.py) |
| `/system/status` | active | [apps/api/routers/system.py](../apps/api/routers/system.py) |
| `/chat/message` | active (مبدئي) | [apps/api/routers/chat.py](../apps/api/routers/chat.py) |
| Orchestrator | active | [sf_ai/core/orchestrator/orchestrator.py](../sf_ai/core/orchestrator/orchestrator.py) |
| DomainRouter | active | [sf_ai/core/router/domain_router.py](../sf_ai/core/router/domain_router.py) |
| IntentRouter | active | [sf_ai/core/router/intent_router.py](../sf_ai/core/router/intent_router.py) |
| SemanticExplorer | active | [sf_ai/core/semantic/semantic_explorer.py](../sf_ai/core/semantic/semantic_explorer.py) |
| HashingVectorizer | active | [sf_ai/core/semantic/hashing_vectorizer.py](../sf_ai/core/semantic/hashing_vectorizer.py) |
| CapabilityRegistry | active | [sf_ai/core/index/capability_registry.py](../sf_ai/core/index/capability_registry.py) |
| ResponseComposer | active | [sf_ai/core/composer/response_composer.py](../sf_ai/core/composer/response_composer.py) |
| Planner | skeleton_only | [sf_ai/core/planner/planner.py](../sf_ai/core/planner/planner.py) |

---

## ما لم يُفعَّل بعد

| المكون | المرحلة |
|--------|----------|
| Arabic Normalizer / NLP Pipeline | Phase 3 |
| Typo Corrector / Dialect Mapper / Arabizi | Phase 3 |
| ChatModule (real) | Phase 4 |
| Dialogue dataset loaders | Phase 5 |
| BPE Tokenizer + Device Manager | Phase 5.5 |
| Tiny native transformer | Phase 6 |
| Web crawler / Article extractor | Phase 7 |
| Research summarizer | Phase 7 |
| RAG (Qdrant + sparse vectors) | Phase 8 |
| Next.js frontend | Phase 9 |

---

## القرارات المعمارية الجوهرية

### 1. السيادة المعرفية فوق كل قرار
- **لا** نموذج جاهز، **لا** أوزان مدربة سابقًا، **لا** API ذكاء خارجي.
- كل embedding/tokenizer/checkpoint مولَّد من SF.AI فقط.
- التفاصيل في [PROJECT_PRINCIPLES.md](../PROJECT_PRINCIPLES.md).

### 2. كل شيء قابل للاستبدال (Replaceable Interfaces)
- HashingVectorizer سيُستبدل بـ SF Native Encoder (Phase 6+).
- ResponseComposer's stock replies ستُستبدل بـ ChatModule + native LM (Phase 4 + Phase 6).
- البحث المعجمي سيُكمَّل بـ neural retrieval (Phase 8).

### 3. Domain-driven Routing بنقاط شفافة
- كل قرار توجيه يصاحبه `matched_signals` و `route_reason`.
- لا black-box: المستخدم يقدر يفسر كل قرار.
- وزن الإشارات موثق في [ROUTER.md](./ROUTER.md).

### 4. Capability Registry هو الـ source of truth
- المجالات، النوايا، حالة كل مجال، علم `requires_safety` — كله في YAML واحد.
- إضافة مجال جديد = إضافة دخول جديد في `default_registry.yaml` + ربما module جديد.

### 5. الحوار العام أولًا، ثم الويب
- Phase 4: ChatModule.
- Phase 7: web research + extraction + summarization rule-based.
- البقية مؤجَّلة عمدًا.

### 6. Safety-first للمجالات الحساسة
- `legal, medical, finance, security, religion` → `requires_safety=true`.
- لا توصية تخصصية قبل اكتمال طبقة السلامة.

---

## الاعتمادات الحالية

**Phase 2 يضيف:**
- `PyYAML` (لتحميل `default_registry.yaml`) — كان موجودًا منذ Phase 1.

**لا** اعتمادات ذكاء اصطناعي حتى الآن.
PyTorch وغيرها يدخلون في Phase 5.5 فقط، كأدوات حساب لا كنماذج جاهزة.
