# PHASE_STATUS.md

## SF.AI — سجل حالة المراحل

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الرحلة الحالية:** **Phase 22 / 30**
- **المرحلة الحالية:** **Phase 22 — Gold Dialogue Corpus v2**
- **حالة المرحلة الحالية:** **بوابة جاهزية corpus v2 + review intake تعمل؛ corpus غير جاهز بعد (227/500، msa=197، saudi=30)**
- **المرحلة التالية المقترحة:** إكمال دفعات فصحى/سعودية محكومة يؤلفها/يراجعها الوكيل بتفويض موثق حتى تمر `make phase22-readiness`.
- **القاموس/المسار اللغوي الحالي:** `msa + saudi` فقط؛ تم تحديث `default_registry.yaml` و`safety_terms.yaml` لفجوات finance/religion/security.
- **تاريخ آخر تحديث:** 2026-05-23

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
| Phase 20 | Domain Activation Gates | ✅ gates_active_no_auto_activation | ✅ |
| Phase 21 | Generative Roadmap & Quality Targets | ✅ completed | ✅ |
| Phase 22 | Gold Dialogue Corpus v2 | readiness_gate_active_not_ready | ✅ |
| Phase 23 | Tokenizer v2 Retrain & Audit | مخططة | ✅ |
| Phase 24 | SF-10M v0.2 Quality Training | مخططة | ✅ |
| Phase 25 | Generated Chat Canary v1 | مخططة | ✅ |
| Phase 26 | SF-50M v0.1 Dialogue Model | مخططة | ✅ |
| Phase 27 | Dialogue Evaluation v2 | مخططة | ✅ |
| Phase 28 | SF-120M v0.1 Candidate | مخططة | ✅ |
| Phase 29 | Runtime Hybrid Assistant v1 | مخططة | ✅ |
| Phase 30 | Continuous Improvement Loop | مخططة | ✅ |

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
  - [protected_terms_msa_candidate.txt](../resources/tokenization/protected_terms_msa_candidate.txt)
  - [preferred_merges.txt](../resources/tokenization/preferred_merges.txt)
  - [preferred_merges_msa_candidate.txt](../resources/tokenization/preferred_merges_msa_candidate.txt)
  - [tokenization_rules.yaml](../resources/tokenization/tokenization_rules.yaml)
- أضيفت مصطلحات فصحى مرشحة غير نشطة: 138 protected terms candidate و101 preferred merges candidate. لا تُعد corpus ولا pretrained vocab، وتُفعّل فقط بعد تغطية corpus/audit.
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
  - بقي `ChatModule` على القوالب، ويصدر metadata `generator=template`; هذا ليس توليدًا ذكيًا.
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
  - docs: [PHASE16_RAG_BRIDGE_REPORT.md](./PHASE16_RAG_BRIDGE_REPORT.md)
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
- بدأ وانتهى Phase 20 Domain Activation Gates:
  - أضيف `make phase20-gates`.
  - أضيف `GET /system/phase20-gates`.
  - أضيف `sf_ai/core/activation/domain_activation_gates.py`.
  - أضيفت اختبارات Phase 20.
  - أُضيف `productivity` كسكيلتون كامل لأنه كان موجودًا في registry دون module/manifest.
  - القرار الحالي: `PHASE20_GATES_ACTIVE_NO_DOMAIN_AUTO_ACTIVATED`.
  - المجال النشط الوحيد: `chat`.
  - المرشحان للمراجعة الصريحة فقط: `web`, `research`.
  - بقية المجالات تبقى skeleton أو safety-first.
  - docs: [PHASE20_DOMAIN_ACTIVATION_GATES_REPORT.md](./PHASE20_DOMAIN_ACTIVATION_GATES_REPORT.md)
- بدأ وانتهى Phase 21 Generative Roadmap:
  - أضيف [GENERATIVE_ROADMAP.md](./GENERATIVE_ROADMAP.md).
  - مُدّدت الخطة الرسمية إلى Phase 30.
  - تم توثيق أن التدريب الفعلي بدأ في Phase 13/14، لكن أول تدريب جودة مفيد قادم هو Phase 24.
  - تم تحديد أن أول فرصة لحوار قصير مولّد مقنع هي Phase 26، والهدف الرسمي للحوار المقنع المستقر هو Phase 28.
  - بقي المسار اللغوي `msa + saudi` فقط، وقاموس Saudi Seed v1 هو المرجع اللهجي الحالي.
  - أضيف مبدأ `Progressive Scaling Strategy`: لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية.
  - السلم الرسمي صار: `SF-10M → SF-50M → SF-120M → SF-350M → SF-700M → SF-1B+`.
  - أضيف تقرير [SCALING_STRATEGY.md](./SCALING_STRATEGY.md).
- بدأ Phase 22 Gold Dialogue Corpus v2 كبوابة جاهزية:
  - أضيف `make phase22-readiness`.
  - أضيف `make phase22-plan`.
  - أضيف `make phase22-next-batch`.
  - أضيف `make phase22-completion-gate`.
  - أضيف `make phase22-review-intake`.
  - أضيف `GET /system/phase22-readiness`.
  - أضيف `GET /system/phase22-collection-plan`.
  - أضيف `GET /system/phase22-next-batch`.
  - أضيف `GET /system/phase22-completion-gate`.
  - أضيف `GET /system/phase22-review-intake`.
  - أضيف `sf_ai/datasets/phase22_readiness.py`.
  - أضيف `sf_ai/datasets/phase22_review_intake.py`.
  - أضيف تقرير [PHASE22_GOLD_DIALOGUE_CORPUS_V2_REPORT.md](./PHASE22_GOLD_DIALOGUE_CORPUS_V2_REPORT.md).
  - القرار الحالي: `NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2`.
  - الموجود الحالي: 227 سجل تدريب جاهز: 197 `msa` و30 `saudi`.
  - المتبقي: 273 سجل للوصول إلى 500.
  - خطة الجمع الحالية: 3 فصحى + 170 سعودي + 100 مرنة، أي 11 batch تقديريًا و12 batch مخططًا بسبب الدفعات الجزئية.
  - أضيفت بوابة اكتمال صارمة: `phase22-completion-gate`، وقرارها الحالي `PHASE22_INCOMPLETE_DO_NOT_ADVANCE`.
  - أضيفت قائمة batches مفصلة داخل `phase22-plan`: `msa_008`، ثم `saudi_001` إلى `saudi_007`، ثم `flex_001` إلى `flex_004`، مع target records وأسماء ملفات وأوامر تحقق مباشرة.
  - أضيفت مهمة batch فورية داخل `phase22-next-batch`: المهمة الحالية `msa_008`، 3 سجلات فصيحة، مع checklist قبول وموضوعات تأليف لا تُعد بيانات تدريب.
  - أضيفت سبع دفعات فصيحة معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_007.jsonl`، بإجمالي 175 سجلًا `silver` مؤلفة/مراجعة بتفويض سامي، مع بطاقات provenance.
  - أضيف seed مصطلحات فصحى تدريبي: `data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl` وفيه 22 سجلًا `gold` لتغطية مصطلحات تشغيل/حوكمة/تدريب أساسية.
  - أضيفت حقول فصل المستخدمين في schema/audit/UI/export/corpus: `owner_user_id`, `created_by_user_id`, `target_user_id`, `user_scope`.
  - المسار الحالي `sami-local` و`single_user`، والهدف منع خلط محادثات أو ذاكرة مستخدم مع مستخدم آخر عند التوسع لاحقًا.
  - أضيف بنك تأليف فصيح غير تدريبي في `resources/phase22_authoring/msa_prompt_bank_v1.json`: أكثر من 80 موضوعًا فصيحًا لبناء batches الفصحى، مع `training_allowed=false` و`synthetic_llm_data=false`.
  - review intake الحالي: ملف عينة واحد في `data/corpus/chat/review/` مرشح للمراجعة، ولا يدخل التدريب تلقائيًا.
  - أضيفت بوابة جودة داخل review intake: `quality_score`, `quality_label`, و`quality_blockers`.
  - أضيف مؤشر جودة التصدير داخل `/ui/chat` حتى يعرف سامي قبل التصدير هل الجلسة قصيرة أو صالحة للمراجعة.
  - أضيفت لوحة بوابة Phase 22 داخل `/ui/chat`، تقرأ `/system/phase22-readiness` و`/system/phase22-collection-plan` وتعرض عدد corpus الحالي، المتبقي، ونقص `msa/saudi`، والمهمة التالية مباشرة.
  - أضيفت لوحة مهمة الجمع الحالية داخل `/ui/chat`، تقرأ `/system/phase22-next-batch` وتعرض `msa_008` وهدف 3 سجلات وموضوعات تأليف عامة؛ الواجهة مختبر اختياري وليست شرطًا على سامي لحفظ أو تصدير أي شيء.
  - أضيف زر `موضوعات أخرى` داخل لوحة مهمة الجمع الحالية للتنقل في بنك التأليف الفصيح، مع `authoring_topic_count` في metadata.
  - أضيف زر `حفظ للمراجعة` في `/ui/chat` وendpoint `POST /chat/review-export` لحفظ review JSONL محليًا في `data/corpus/chat/review/` فقط، مع رفض `training_allowed=true`.
  - القاعدة العملية الجديدة: ملف التصدير المفيد يجب أن يحتوي غالبًا 3 أدوار مستخدم + 3 ردود مساعد على الأقل، وبدون ردود `sf_10m_v0_1`.
  - القاعدة العملية الأحدث: الوكيل يستطيع تأليف/مراجعة/اعتماد دفعات Phase 22 مباشرة كـ `owner-delegated agent-authored` بدون انتظار حفظ أو تصدير من سامي، بشرط اكتمال `source/license/quality/training_allowed/user_scope/notes` ونجاح الاختبارات.
  - صححت تشغيل الواجهة المستقرة: `generator=template` افتراضيًا، أي قوالب ثابتة لا مولد؛ و`SF-10M` الخام يبقى مختبرًا صريحًا فقط.
  - أضيفت حماية export/review intake لتمييز أي جلسة تحتوي ردود `sf_10m_v0_1` ومنع عدّها كـ candidate تدريب جودة.
  - أضيفت intents محددة لعبارات Phase 22 اليومية: اختبار الحوار الفصيح، الخطوة التالية، والفرق بين التدريب والتفعيل.
  - الناقص الحاسم الآن: العدد والتوازن؛ الفصحى وصلت إلى 197/200، والسعودي ما زال 30/200.
  - لا تدريب جديد بدأ.

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
- اختبارات: 7 في `test_chat_ui.py` تشمل مؤشر جودة التصدير ولوحة بوابة Phase 22 ومهمة الجمع الحالية وحفظ review المحلي وفصل المستخدمين.

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
435 passed in 4.60s
```

| ملف | عدد |
|------|------|
| test_arabic_normalizer.py | 16 |
| test_bpe_tokenizer.py | 13 |
| test_capability_registry.py | 5 |
| test_chat_module.py | 12 |
| test_chat_native_generator.py | 14 (Phase 15 + lab mode) |
| test_chat_rag_bridge.py | 7 (Phase 17) |
| test_chat_ui.py | 7 (Phase 9/19 status + export quality indicator) |
| test_checkpoints.py | 7 |
| test_conversation_state.py | 8 |
| test_corpus_governance.py | 10 (Phase 11) |
| test_dataset_validators.py | 28 |
| test_dialogue_batch_preparation.py | 3 (Phase 18) |
| test_dialect_mapper.py | 7 |
| test_generative_roadmap.py | 4 (Phase 21 + scaling strategy) |
| test_health.py | 11 |
| test_intent_detector.py | 7 |
| test_mo3jam_importer.py | 13 |
| test_new_chat_intents.py | 38 (Phase 9/19 social polish + Phase 22 guidance) |
| test_nlp_pipeline.py | 9 |
| test_orchestrator.py | 7 |
| test_phase10_skeleton_domains.py | 4 (Phase 10) |
| test_phase16_eval_harness.py | 3 (Phase 16) |
| test_phase19_readiness.py | 2 (Phase 19) |
| test_phase20_domain_activation_gates.py | 6 (Phase 20) |
| test_phase22_readiness.py | 15 (Phase 22) |
| test_phase22_review_intake.py | 7 (Phase 22) |
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
| **Total** | **423** |

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
