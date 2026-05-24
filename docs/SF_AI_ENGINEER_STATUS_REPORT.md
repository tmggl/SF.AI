# SF.AI — تقرير شامل للمهندس

**تاريخ التقرير:** 2026-05-24
**الحالة الحالية:** Phase 27.79 / 30 — Objective/Curriculum/Decoding Repair Design
**المسار اللغوي:** العربية الفصحى + اللهجة السعودية فقط
**القاموس المرجعي:** Saudi Seed v1 + `safety_terms.yaml`
**قرار runtime الحالي:** المولد السيادي غير مفعّل للمحادثة الحرة؛ `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS` فعّالة.
**القرار الهندسي الحالي:** `PHASE27_79_REPAIR_DESIGN_DECISION`.

> تحديث ملزم: هذا التقرير يُقرأ الآن تحت **Sovereign Practical Acceleration Strategy v2**.
> أي تفاصيل تاريخية أقدم من Phase 27.78 تُعامل كسجل رحلة، لا كتعليمات حالية.

---

## 1. الملخص التنفيذي

SF.AI مشروع لبناء نظام ذكاء اصطناعي لغوي سيادي من الصفر. الفكرة ليست إنشاء واجهة فوق نموذج جاهز، ولا استخدام GPT/Claude/Gemini من الخلفية، ولا الاعتماد على pretrained tokenizer أو embeddings أو weights. القاعدة العليا:

> نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.

وصل المشروع إلى مرحلة متقدمة من البنية، الحوكمة، جمع corpus سيادي، تدريب tokenizer من الصفر، تدريب عدة نسخ صغيرة من نموذج `SF-10M`، بناء واجهة محادثة، بناء canary/eval/guards، وتثبيت استراتيجية تكبير تدريجي. لكنه لم يصل بعد إلى حوار مولّد مقنع داخل الواجهة.

Phase 27.78 أوقفت التجريب الأعمى وأصدرت root-cause gate رسميًا. Phase 27.79
حوّلت ذلك إلى تصميم objective/curriculum/decoding بلا تدريب. السبب الأكبر
الحالي ليس capacity، بل:

- family mixing: `22%`.
- objective: `18%`.
- curriculum: `16%`.
- weak generalization: `14%`.
- semantic routing: `10%`.
- capacity: `1%`.

لذلك القرار الهندسي الصحيح حاليًا:

- لا نعرض المولد للمستخدم كنجاح.
- لا ننتقل إلى `SF-50M` أو `SF-120M`.
- لا نفتح Phase 28.
- لا نبدأ أي تدريب جديد قبل تشفير gates.
- نكمل Phase 27.80: Repair Gate Encoding and Dry-Run Validation.

---

## 2. الهدف العام

الهدف النهائي هو بناء **نموذج لغوي سيادي مولّد** باسم SF.AI:

- يفهم العربية الفصحى.
- يفهم اللهجة السعودية.
- يتدرج من routing/templates إلى توليد لغوي حقيقي.
- يحافظ على فصل واضح بين runtime والتدريب.
- لا يستخدم أي عقل خارجي جاهز.
- يبني corpus/tokenizer/model/checkpoints/eval محليًا وبشفافية.

الهدف العملي الأقرب:

1. تشفير gates في Phase 27.80 حسب تصميم Phase 27.79.
2. تشغيل dry-run قبل أي تدريب جديد.
3. إثبات held-out dialogue quality وfamily stability وclean-stop وsemantic correctness.
4. بعد ذلك فقط إعادة النظر في runtime.
5. لا تفتح `SF-50M` إلا إذا صدر `SF-50M JUSTIFIED TRANSITION` مدعوم بالأدلة.

---

## 3. ما يعمل الآن

### الواجهة والـ API

الواجهة تعمل محليًا:

```text
http://127.0.0.1:8123/ui/chat
```

Endpoints الأساسية:

- `GET /health`
- `GET /system/status`
- `POST /chat/message`
- `GET /ui/chat`
- endpoints للتقارير والجاهزية حسب المراحل.

### الحوار الحالي

الحوار في الواجهة يعمل عبر:

- NLP عربي rule-based.
- Router للمجال والنية.
- ChatModule.
- قوالب اجتماعية قصيرة.
- Composer للمجالات غير المفعلة أو الحساسة.
- metadata صادق يوضح: المجال، النية، الثقة، المسار، هل استخدمت الذاكرة أو المولد.

هذا مهم: **الواجهة الحالية ليست دليلًا على نجاح المولد**. لا يجوز استخدام
template masking لإخفاء ضعف المولد. أي runtime release يحتاج
`NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.

### البيانات

الوضع الحالي حسب السجلات:

```text
records_total = 5943
msa           = 2949
saudi         = 2994
train         = 5343
eval          = 600
```

كل corpus تدريبي يجب أن يحمل:

- `source`
- `license`
- `quality`
- `training_allowed`
- `language`
- `dialect`
- `owner_user_id`
- `created_by_user_id`
- `target_user_id`
- `user_scope`

يوجد فلتر يمنع إدخال محادثات تشغيلية أو هندسية أو خاصة بإدارة المشروع في corpus العام. أي حوار من نوع "التالي/اكمل/ارفع/phase/tokenizer/pytest/commit/readiness" يصنف training-forbidden.

### التدريب

بدأ التدريب الفعلي فعلًا منذ Phase 13. توجد:

- tokenizers سيادية مدربة محليًا.
- نماذج `SF-10M` متعددة.
- checkpoints محلية داخل `artifacts/checkpoints`.
- تقارير eval وgeneration samples داخل `artifacts/reports` و`artifacts/samples`.

لكن التدريب لم ينتج بعد محادثة حرة مقنعة.

---

## 4. ما لا يعمل بعد

المولد السيادي لا يعمل بجودة كافية للواجهة. آخر تشخيص:

- يستطيع حفظ بعض أزواج السؤال/الجواب في probes صغيرة.
- يفشل أحيانًا في clean-stop.
- ينتج كسورًا حرفية في عبارات عالية التجزئة.
- يخلط بعض ردود repair مع ردود أخرى.
- لا يمر canary الدلالي الصارم بعد.

أمثلة من Phase 27.19:

```text
prompt    : السلام عليكم
generated : وعليكالسلم، أهلًا بك.
reason    : greeting_mismatch
```

```text
prompt    : ما فائدة القراءة
generated : القراراءراءتفيد وتزيد المفردات.
reason    : malformed_token
```

لذلك: أي واجهة تظهر ردًا مولدًا مشوشًا لا تعد نجاحًا. هذا بالضبط سبب وجود `GenerationGuard`.

---

## 5. مبادئ المشروع الحاكمة

### Own the intelligence

الذكاء يجب أن يكون مملوكًا للمشروع:

- corpus موثق.
- tokenizer سيادي.
- model يبدأ من أوزان عشوائية.
- checkpoints محلية.
- eval واضح.

### No pretrained

ممنوع:

- pretrained weights.
- pretrained embeddings.
- pretrained tokenizer vocabulary.
- external LLM APIs.
- LoRA فوق نموذج خارجي.
- synthetic LLM data من مصادر خارجية أو غير موثقة.

### Arabic-first / Saudi-aware

النطاق الحالي:

- فصحى.
- سعودي.

لا تفعيل للهجات أخرى runtime/training قبل قرار صريح لاحق. المشروع كان فيه قدرة أولية على التعرف على لهجات أخرى، لكن المسار التدريبي الرسمي الآن محصور في `msa + saudi`.

### Runtime != Training

runtime يخدم المستخدم. training ينتج artifacts. لا يوجد request داخل الواجهة يبدأ تدريبًا أو يكتب checkpoint.

### No hidden shortcuts

لا download model. لا API خارجي مخفي. لا fallback غير موثق. لا "مساعد خارجي" تحت اسم داخلي.

### Progressive Scaling Strategy

لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.

السلم الرسمي:

```text
SF-10M -> SF-50M -> SF-120M -> SF-350M -> SF-700M -> SF-1B+
```

أي قفزة مثل 3B قبل corpus/eval/tokenizer قوي تعد خطأ هندسيًا.

---

## 6. المعمارية الحالية

### طبقة API

المسار:

```text
apps/api/
```

تحتوي على FastAPI routers:

- health.
- chat.
- system/status.
- corpus/readiness/eval endpoints.
- static UI.

### نواة النظام

المسار:

```text
sf_ai/core/
```

المكونات:

- `orchestrator`: يستقبل الرسالة ويجمع NLP + Router + Module/Composer.
- `router`: يحدد domain وintent.
- `semantic`: lexical/fuzzy/hashing scoring محلي.
- `index`: registry وdomain manifests.
- `composer`: يكتب ردود المجالات skeleton/safety.
- `nlp`: normalization، dialect mapping، typo correction، intent hints.
- `activation`: domain activation gates.

### الوحدات

المسار:

```text
sf_ai/modules/
```

الوضع:

- `chat`: المجال النشط الوحيد.
- `web`: offline-ready، ليس مفعلًا كبحث حر.
- `research`: offline-ready، ليس مفعلًا تلقائيًا.
- باقي المجالات skeleton أو safety-first.

### النماذج والتدريب

المسارات:

```text
sf_ai/models/
sf_ai/training/
artifacts/tokenizers/
artifacts/checkpoints/
```

تحتوي على:

- SF-BPE tokenizer.
- TinyTransformer / SF-10M scaffolding.
- train scripts.
- checkpoint metadata.
- training configs.
- generation/eval scripts.

### الذاكرة/RAG

المسارات:

```text
sf_ai/memory/
sf_ai/modules/chat/rag_bridge.py
```

يوجد RAG محلي مبني على:

- sparse retrieval.
- hashing vector store محلي.
- hybrid retriever.

لكنه ليس ذاكرة تلقائية مفتوحة في runtime الافتراضي.

---

## 7. الفرق بين البوت والقالب والمولد

هذه نقطة مهمة لأن الاختبار من الواجهة قد يسبب لبسًا.

### القالب

ملفات مثل:

```text
sf_ai/modules/chat/chat_patterns.py
```

هذه ردود ثابتة مخصصة للسلام، الشكر، القدرات، الهوية، إلخ. فائدتها:

- تعطي تجربة آمنة مؤقتة.
- تمنع عرض مخرجات مولد فاشلة.
- تساعد في اختبار الـ routing.

هي ليست "ذكاء مولد".

### الـ router

يقرر:

- هل الرسالة تحية؟
- هل هي سؤال عن القدرات؟
- هل هي مجال حساس؟
- هل هي coding/data/web/etc؟

### المولد

المولد هو checkpoint سيادي مدرب من الصفر. يوجد فعليًا في المشروع، لكن runtime يحجبه لأن الجودة لم تنجح بعد.

الحالة الحالية:

- المولد موجود.
- التدريب حصل.
- التقييم حصل.
- لكنه غير مقنع وغير آمن للواجهة اليومية.

---

## 8. حالة المراحل بدون تجاهل

| المرحلة | الاسم | الحالة الحالية |
|---------|------|----------------|
| Phase 0 | Project Governance & Execution Plan | مكتملة |
| Phase 1 | Project Foundation | مكتملة |
| Phase 2 | Core Brain Skeleton | مكتملة |
| Phase 3 | Language Understanding Layer | مكتملة |
| Phase 3.5 | Mo3jam Saudi Dialect Import | مكتملة كبنية + dry-run، لا زحف تلقائي |
| Phase 3.6 | Saudi Seed v1 Lexicon | مكتملة |
| Phase 4 | General Chat First | مكتملة |
| Phase 5 | Dialogue Dataset Preparation | مكتملة |
| Phase 5.5 | Sovereign Acceleration Layer | مكتملة |
| Phase 6 | Native SF.AI Small Language Model | مكتملة كبنية/scaffolding |
| Phase 7 | Web Research/Crawling/Extraction/Summarization | مكتملة offline-ready، permission-gated |
| Phase 8 | Local RAG Foundation | مكتملة |
| Phase 9 | Frontend Chat Interface | مكتملة |
| Phase 10 | Later Domains Skeleton | مكتملة |
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack | مكتملة |
| Governance Layer | Engineering Standards | مكتملة |
| Constitution Layer | Engineering & Linguistic Constitution | مكتملة |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | مكتملة مع قيود |
| Phase 13 | Tiny LM Smoke Training | مكتملة مع قيود |
| Phase 14 | SF-10M v0.1 Training Run | مكتملة مع قيود |
| Phase 15 | Generator Adapter for ChatModule | مكتملة كبنية آمنة |
| Phase 16 | Evaluation/Safety/Saudi-MSA Harness | مكتملة؛ runtime منفصل ومحجوب |
| Phase 17 | Local Memory/RAG Bridge into Chat | مكتملة |
| Phase 18 | Data Expansion Loop v1 | مكتملة |
| Phase 19 | SF-50M Candidate Training | gate active، غير جاهز |
| Phase 20 | Domain Activation Gates | مكتملة؛ لا تفعيل تلقائي |
| Phase 21 | Generative Roadmap & Quality Targets | مكتملة |
| Phase 22 | Gold Dialogue Corpus v2 | مكتملة |
| Phase 23 | Tokenizer v2 Retrain & Audit | مكتملة |
| Phase 24 | SF-10M v0.2 Quality Training | مكتملة مع حجب runtime |
| Phase 25 | Generated Chat Canary v1 | مكتملة؛ real model blocked |
| Phase 26 | SF-50M v0.1 Readiness | مكتملة؛ غير جاهز |
| Phase 27 | Dialogue Evaluation v2 + Corpus Expansion | مكتملة |
| Phase 27.5 | SF-10M Dialogue-Format Repair | مكتملة؛ runtime blocked |
| Phase 27.6 | SF-10M Assistant-Target Training | مكتملة؛ runtime blocked |
| Phase 27.7 | Fixed Split + Gold Social Canary | مكتملة؛ runtime blocked |
| Phase 27.8 | SF-10M v0.6 Split Training | تحسن رقمي؛ runtime blocked |
| Phase 27.9 | Generation Quality Harness | مكتملة؛ v0.6 blocked |
| Phase 27.10 | Short Response Repair | تحسن رقمي؛ generation blocked |
| Phase 27.11 | Objective/Decoding Diagnosis | كشفت نقص stop boundary/EOS |
| Phase 27.12 | Assistant Boundary/EOS Repair | تحسن جزئي؛ runtime blocked |
| Phase 27.13 | SF-10M v0.8 Boundary/EOS Wider Training | eval تحسن؛ generation blocked |
| Phase 27.14 | Sovereign Training Quality Tooling Decision | مكتملة |
| Phase 27.15 | Social/Lexical Curriculum + No-Repeat Decoding | eval تحسن؛ canary صارم فشل |
| Phase 27.16 | Prompt-to-Answer Objective Repair | sample isolation؛ runtime blocked |
| Phase 27.17 | Prompt-to-Answer Micro-Probe | breakthrough جزئي 27/32 |
| Phase 27.18 | Tokenization/Decoding Hygiene Repair | حددت blockers |
| Phase 27.19 | Hygiene Repair Corpus/Probe | repair examples لم تكف |
| Phase 27.20 | Tokenizer/Protected-Phrase Strategy | التالية المقترحة |
| Phase 28 | SF-120M v0.1 Candidate | مخططة فقط |
| Phase 29 | Runtime Hybrid Assistant v1 | مخططة |
| Phase 30 | Continuous Improvement Loop | مخططة |

---

## 9. نتائج التدريب المهمة

### Phase 13

أول smoke training:

```text
model params = 6,361,600
steps        = 20
first loss   = 5.6638
last loss    = 4.7539
eval loss    = 4.4346
```

الهدف كان إثبات أن pipeline يعمل، وليس جودة الحوار.

### Phase 14 — SF-10M v0.1

```text
steps completed = 33
first loss      = 5.6638
last loss       = 4.7535
eval loss       = 4.0777
perplexity      = 59.01
```

النتيجة: نموذج حقيقي لكنه مكرر وضعيف.

### Phase 24 — SF-10M v0.2

```text
steps       = 2000
loss        = 8.4751 -> 2.8256
eval loss   = 2.5779
perplexity  = 13.17
```

رقميًا تحسن جدًا، لكن التوليد لم يكن متماسكًا بما يكفي.

### Phase 27.8 — SF-10M v0.6

```text
best eval loss = 5.0227
perplexity     = 151.82
canary         = 0/10
```

### Phase 27.10 — SF-10M v0.7

```text
best eval loss = 4.7512
perplexity     = 115.72
generation     = 0/10 strict pass
```

### Phase 27.13 — SF-10M v0.8

```text
eval loss  = 3.1875
perplexity = 24.23
strict generation-quality = 3/10
```

تحسن رقمي لكنه غير كاف.

### Phase 27.15 — SF-10M v0.10

```text
eval loss  = 3.0452
perplexity = 21.01
strict semantic canary = 0/10
```

### Phase 27.16 — SF-10M v0.11

```text
best eval loss = 4.0573
perplexity     = 57.82
runtime        = blocked
```

### Phase 27.17/27.19 micro-probes

Phase 27.17:

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 29/32
guard_passed = 29/32
```

Phase 27.19:

```text
passed       = 27/32
exact_clean  = 28/32
semantic     = 28/32
guard_passed = 29/32
```

الاستنتاج: النموذج اقترب في probe صغير، لكن الكسور اللفظية ما زالت تحتاج علاج tokenizer/protected phrases.

---

## 10. لماذا لم نكبر إلى SF-50M؟

لأن Progressive Scaling Strategy يمنع تكبير النموذج قبل نجاح الجودة الحالية.

شروط الانتقال من `SF-10M` إلى `SF-50M`:

- corpus جاهز وموثق.
- tokenizer audit ناجح.
- evaluation suite ناجحة.
- safety checks ناجحة.
- runtime quality مقبولة.
- hallucination checks مقبولة.
- repetition checks مقبولة.
- resource readiness.

المشروع نجح في corpus readiness نسبيًا، ونجح في بناء tokenizer/eval/canary، لكنه فشل في runtime quality/repetition/semantic generation. لذلك التكبير الآن سيكبر المشكلة بدل حلها.

---

## 11. سياسة اللغة والبيانات

### النطاق الحالي

```text
language = ar
dialect  = msa | saudi
```

لا توجد لهجات أخرى في التدريب الحالي.

### Arabizi

Arabizi له normalization خاص، لكنه ليس بديلًا عن corpus العربي.

### code

الكود منفصل عن الحوار. لا نخلط تعليمات البرمجة أو إدارة المشروع في corpus الحوار العام.

### corpus الطبيعي فقط

المسموح:

- سوالف يومية.
- فصحى طبيعية.
- سعودي طبيعي.
- سؤال وجواب عام.
- شرح يومي غير هندسي.

الممنوع:

- حوارات تشغيل المشروع.
- تعليمات agent.
- phase/gates/tokenizer/corpus/commit/pytest.
- Persona خاصة بسامي.
- أي نمط من محادثات التطوير الحالية.

---

## 12. سياسة السلامة

المجالات الحساسة:

- medical.
- legal.
- finance.
- security.
- religion.

هذه لا تعطى كخبرة تخصصية في runtime. Composer يعطي ردودًا آمنة أو يحيل لمختص. وجود domain أو module لا يعني أنه مفعل.

Crawler/web:

- لا crawling تلقائي.
- `CrawlerBase` permission-gated.
- robots/rate limit محترمان.
- web/research offline-ready فقط حتى قرار تفعيل واضح.

---

## 13. خريطة الملفات المهمة

```text
README.md
PROJECT_PRINCIPLES.md
SETUP_STATUS.md
docs/EXECUTION_PLAN.md
docs/PHASE_STATUS.md
docs/PROJECT_CONSTITUTION.md
docs/GENERATIVE_ROADMAP.md
docs/SCALING_STRATEGY.md
docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md
docs/PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md
```

مصادر اللغة/tokenization:

```text
resources/lexicons/
resources/tokenization/
data/corpus/chat/jsonl/
```

التدريب والآثار:

```text
artifacts/tokenizers/
artifacts/checkpoints/
artifacts/reports/
artifacts/samples/
```

الكود:

```text
apps/api/
sf_ai/core/
sf_ai/modules/chat/
sf_ai/models/
sf_ai/training/
sf_ai/datasets/
tests/
scripts/
```

---

## 14. كيف يشغل المهندس المشروع

من جذر المشروع:

```bash
cd /Users/sami/workSF/SF.AI
make api
```

أو:

```bash
bash scripts/run_chat_server.sh
```

ثم:

```text
http://127.0.0.1:8123/ui/chat
```

فحوص سريعة:

```bash
curl -s http://127.0.0.1:8123/health
curl -s http://127.0.0.1:8123/system/status
.venv/bin/python -m pytest tests
```

---

## 15. كيف يختبر المهندس بصدق

لا يختبر `chat_patterns.py` على أنه مولد.

للتأكد من الـ routing:

```text
اهلا
وشلونك
وش تقدر تسوي
من صنعك
ساعدني
شكرا
```

المتوقع: ردود مفهومة غالبًا من القوالب.

لاختبار سبب حجب المولد، يرجع إلى:

```text
docs/PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md
artifacts/reports/phase27_19_hygiene_repair_probe_report.json
artifacts/samples/phase27_19_hygiene_repair_probe_generations.md
```

ويلاحظ أن المولد لم يمر بعد، رغم وجود تدريب حقيقي.

---

## 16. المرحلة التالية المقترحة

### Phase 27.20 — Tokenizer/Protected-Phrase Strategy

هدفها:

- حماية عبارات سعودية/فصحى شائعة من التجزئة العدوانية.
- مراجعة protected terms وpreferred merges.
- اختبار أثر tokenization على micro-probe.
- عدم تدريب نموذج كبير.
- عدم الانتقال إلى `SF-50M`.

السبب:

Phase 27.19 أثبتت أن زيادة أمثلة repair وحدها لا تكفي. المشكلة تحتاج إصلاحًا في تمثيل العبارات أو استراتيجية tokenizer/decoding قبل التدريب الواسع.

---

## 17. المخاطر الحالية

1. **وهم النجاح من الواجهة**
   القوالب قد تبدو جيدة، لكنها ليست المولد.

2. **تكبير مبكر للنموذج**
   الانتقال إلى 50M أو أكبر قبل علاج quality سيزيد التكلفة ولا يضمن حلًا.

3. **تلوث corpus**
   إدخال حوارات تشغيلية من محادثات التطوير سيعلم النموذج أسلوب إدارة المشروع بدل الكلام الطبيعي.

4. **تجزئة لغوية سيئة**
   بعض العبارات السعودية/الفصحى تتكسر وتنتج fragments.

5. **خلط runtime/training**
   يجب ألا يتحول اختبار الواجهة إلى تدريب أو حفظ تلقائي.

---

## 18. الخلاصة الهندسية

SF.AI ليس مجرد بوت قوالب، لكنه حاليًا يستخدم القوالب في الواجهة لأن المولد السيادي لم ينجح بعد في الجودة. المسار الصحيح ليس إنكار ذلك ولا عرضه مبكرًا، بل الاستمرار في بناء السلسلة السيادية:

```text
corpus -> tokenizer -> training -> checkpoint -> eval -> guard -> runtime
```

الإنجاز الحقيقي حتى الآن:

- المشروع صار لديه بنية كاملة.
- لديه corpus محكوم.
- لديه tokenizer سيادي.
- لديه نماذج مدربة من الصفر.
- لديه eval/canary/guards تمنع خداع المستخدم.
- لديه خطة تكبير تدريجية صارمة.

ما ينقص:

- إصلاح tokenization/protected phrases.
- اجتياز micro-probes وgeneration-quality.
- فتح `SF-50M` فقط بعد نجاح `SF-10M`.
- ثم بناء runtime hybrid حقيقي في Phase 29.

هذا مشروع في منتصف طريق بناء نموذج لغوي سيادي، وليس chatbot جاهزًا بعد.
