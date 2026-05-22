# AGENT_HANDOFF.md

## هذه وثيقة تسليم — للوكيل التالي الذي يكمل بناء SF.AI

> **قبل أن تفعل أي شيء، اقرأ هذه الوثيقة كاملة.** المالك (سامي) أعطى الإذن المتراكم لتنفيذ خطة بناء طويلة، وما تجده الآن هو منتصف الرحلة، لا بدايتها.

---

## 1. ما هو SF.AI؟

منصة ذكاء اصطناعي **سيادية معرفيًا** يبنيها سامي من الصفر. الفكرة المركزية:

> **نستخدم أدوات جاهزة. ولا نستخدم عقولًا جاهزة.**

- مسموح: PyTorch، MPS، BeautifulSoup، FastAPI، خوارزميات معروفة (BPE، AdamW، BM25).
- ممنوع: أي LLM خارجي (OpenAI/Claude/Gemini)، أي pretrained weights، أي embeddings جاهزة (sentence-transformers)، أي tokenizer vocabulary جاهز، أي LoRA فوق نموذج خارجي.

اقرأ [PROJECT_PRINCIPLES.md](../PROJECT_PRINCIPLES.md) للقاعدة الحاكمة و[SOVEREIGN_ACCELERATION.md](./SOVEREIGN_ACCELERATION.md) للفروق الدقيقة.
واقرأ [CURRENT_GOALS.md](./CURRENT_GOALS.md) قبل تحسين الشات أو اللغة.

---

## 2. الهدف النهائي للمستخدم (مهم جدًا)

سامي طلب صراحة:
- شاشة محادثة عربية مريحة يستخدمها بنفسه.
- توجيه دقيق للأسئلة داخل النظام.

الشاشة جاهزة الآن على `http://127.0.0.1:8123/ui/chat`. التوجيه حُسّن للرسائل اليومية الشائعة، ويبقى قابلًا للتوسيع لاحقًا.

---

## 3. الوضع الحالي للمشروع

### المراحل المكتملة

| المرحلة | الاسم | الحالة |
|---------|------|--------|
| Phase 0 | Project Governance & Execution Plan | ✅ |
| Phase 1 | Project Foundation (FastAPI + هيكل) | ✅ |
| Phase 2 | Core Brain Skeleton (Orchestrator + Router + Composer) | ✅ |
| Phase 3 | Language Understanding Layer (NLP عربي) | ✅ |
| Phase 3.5 | Mo3jam Saudi Dialect Importer | ✅ (بنية + dry-run، الزحف ينتظر) |
| Phase 3.6 | Saudi Seed v1 Lexicon (516 مدخل من تأليف سامي) | ✅ |
| Phase 4 | General Chat First (ChatModule نشط) | ✅ |
| Phase 5 | Dialogue Dataset Preparation | ✅ |
| Phase 5.5 | Sovereign Acceleration Layer (SF-BPE + torch + checkpoints) | ✅ |
| Phase 6 | Native SF.AI Small Language Model (بنية scaffolding) | ✅ |
| Phase 7 | Web Research (extractor + summarizer + citations) | ✅ (offline-ready) |
| Phase 8 | Local RAG Foundation (BM25 + HashingVectorStore + Hybrid) | ✅ |
| Phase 9 | Frontend Chat Interface (HTML+JS RTL) | ✅ |
| Phase 10 | Later Domains Skeleton | ✅ |
| Phase 11 | Sovereign Corpus Governance & Saudi/MSA Dialogue Pack | ✅ |
| Phase 12 | SF-BPE Tokenizer v1 Training & Audit | ✅ completed_with_limits |
| Phase 13 | Tiny LM Smoke Training | ✅ completed_with_limits |
| Phase 14 | SF-10M v0.1 Training Run | ✅ completed_with_limits |
| Phase 15 | Generator Adapter for ChatModule | ✅ completed_as_safe_adapter |
| Phase 16 | Evaluation/Safety/Style Harness | ✅ completed_lab_runtime_separate |
| Phase 17 | Local Memory/RAG Bridge into Chat | ✅ completed_local_bridge |
| Phase 18 | Data Expansion Loop v1 | ✅ completed_governed_loop |
| Phase 19 | SF-50M Candidate Training | readiness_gate_active_not_ready |
| Phase 20 | Domain Activation Gates | ✅ gates_active_no_auto_activation |
| Phase 21 | Generative Roadmap & Quality Targets | ✅ completed |
| Phase 22 | Gold Dialogue Corpus v2 | readiness_gate_active_not_ready |

اقرأ التفاصيل في [PHASE_STATUS.md](./PHASE_STATUS.md) و [EXECUTION_PLAN.md](./EXECUTION_PLAN.md).

### الاختبارات

```
435 passed in 4.97s
```

شغّل: `cd /Users/sami/workSF/SF.AI && .venv/bin/python -m pytest tests`.

### السيرفر المحلي

يعمل في الخلفية على المنفذ **8123** (المنفذ 8000/8765 محجوز بمشروع آخر لسامي).

- Endpoint رئيسي: `POST /chat/message`.
- شاشة: `GET /ui/chat`.
- تشخيص: `GET /system/status`.
- Corpus preflight: `GET /system/corpus-audit`.
- Phase 12 decision: `GET /system/phase12-readiness`.
- Phase 22 readiness: `GET /system/phase22-readiness`.
- Phase 22 collection plan: `GET /system/phase22-collection-plan`.
- Phase 22 review intake: `GET /system/phase22-review-intake`.
- `/ui/chat` تعرض بوابة Phase 22 الحية وجودة التصدير؛ لا تعرض ذلك كدليل على وجود مولد جاهز.
- Source inventory: `GET /system/source-inventory`.

تشغيل يدوي:
```bash
cd /Users/sami/workSF/SF.AI
bash scripts/run_chat_server.sh
```

---

## 4. ما الذي كنت أعمل عليه حين توقفت

### مهمة "محادثة مريحة + توجيه دقيق" — اكتملت

ما **أتممته**:
1. ✅ Audit للتوجيه على رسائل شائعة (`شكرا`, `تمام`, `لا`, `ساعدني`, `مش فاهم`) → كانت تسقط في fallback.
2. ✅ أضفت 7 intents جديدة في [sf_ai/core/index/default_registry.yaml](../sf_ai/core/index/default_registry.yaml): `chat.farewell`, `chat.thanks`, `chat.affirmation`, `chat.negation`, `chat.help`, `chat.confused`, `chat.who_made_you`.
3. ✅ كتبت قوالب أقصر وأدفأ في [sf_ai/modules/chat/chat_patterns.py](../sf_ai/modules/chat/chat_patterns.py).
4. ✅ ربطت الـ intents الجديدة بـ ChatResponseBuilder و ChatModule.
5. ✅ حسّنت `ResponseComposer` بردود **مخصصة لكل مجال** بدل القالب العام (legal/medical/finance/security/religion ولكل skeleton domain نص خاص).
6. ✅ فعّلت Saudi Seed v1 افتراضيًا عبر [scripts/run_chat_server.sh](../scripts/run_chat_server.sh) و `make api`، بدون import-time side effects داخل `main.py`.
7. ✅ أضفت زر مسح المحادثة + timestamps في [apps/api/static/chat.html](../apps/api/static/chat.html).
8. ✅ أضفت اختبارات `tests/test_new_chat_intents.py` ووسّعت `test_intent_detector.py`.
9. ✅ حسّنت متابعة `وشلونك` لتتوجه بدون domain fallback، و`عندي سؤال` لتفتح سؤالًا بدل شرح سؤال سابق حتى داخل نفس الجلسة.
9. ✅ أعدت تشغيل السيرفر على 8123 وتحقق audit حي:
   - `شكرا` → `chat.thanks`
   - `تمام` → `chat.affirmation`
   - `لا` → `chat.negation`
   - `ساعدني` → `chat.help`
   - `مش فاهم` → `chat.confused`
   - `من صنعك` → `chat.who_made_you`
   - `وداعا` → `chat.farewell`
10. ✅ بعد ملاحظة سامي، حُصر الـ runtime على العربية الفصحى + اللهجة السعودية فقط، وأضيفت:
   - `سعودي` → `chat.language_preference`
   - `عندي؟` → `chat.clarification`

### Phase 10 — Later Domains Skeleton — اكتملت

أضيفت هياكل المجالات:
`coding`, `data`, `files`, `legal`, `medical`, `finance`, `education`, `religion`, `social`, `writing`, `translation`, `image`, `audio`, `security`, `business`, `ecommerce`.

لكل مجال: `manifest.yaml`, `module.py`, `__init__.py`. كل المجالات بقيت `skeleton_only` و `allowed_tools: []`. المجالات الحساسة (`legal`, `medical`, `finance`, `security`, `religion`) عليها `requires_safety: true`.

### الهدف العام بعد تحديث الخطة

سامي أكد أن الهدف ليس بوت قواعد فقط، بل **نموذج لغوي سيادي مولّد**. لذلك أُضيفت Phase 11–20 في [EXECUTION_PLAN.md](./EXECUTION_PLAN.md). التفويض الحالي يسمح بمتابعة المراحل المسجلة دون انتظار موافقة جديدة، مع بقاء قواعد السيادة وفحص الحساسية.

### Phase 11 — اكتملت كحوكمة

أُضيفت وثائق وأدوات فحص corpus:
- [CORPUS_GOVERNANCE.md](./CORPUS_GOVERNANCE.md)
- [DIALOGUE_DATASET_RUBRIC.md](./DIALOGUE_DATASET_RUBRIC.md)
- [data/corpus/chat/jsonl/README.md](../data/corpus/chat/jsonl/README.md)
- `sf_ai/datasets/corpus_governance.py`
- `tests/test_corpus_governance.py`

تدريب tokenizer v1 اكتمل في Phase 12. Smoke LM training اكتمل في Phase 13، وSF-10M v0.1 المحدود اكتمل في Phase 14، لكنه خام ومكرر وغير جاهز لاختبار سامي كمولد حواري. Phase 15 أضاف `NativeGenerator` و`GenerationPolicy` وmetadata يوضح هل الرد `template` أو `sf_10m_v0_1`، لكنه لم يجعل المولد مقنعًا. Phase 16 أضاف prompt suites وeval report، ثم فُتح مختبر سامي المحلي للقياس والتطوير. Phase 17 أضاف `ChatRagBridge` و`ContextBuilder` كربط محلي اختياري مع `HybridRetriever`. Phase 18 أضاف دورة تحسين بيانات محكومة من واجهة الشات. Phase 19 أضاف بوابة جاهزية SF-50M وقراره الحالي: وسّع corpus أولًا. Phase 20 أضاف بوابات تفعيل المجالات، ولا يفعّل أي skeleton تلقائيًا. Phase 21 ثبت خارطة Phase 22–30 للوصول إلى حوار مولّد مقنع. Phase 22 أضاف بوابة Gold Dialogue Corpus v2: الوضع الحالي 280/500 (`msa=200`, `saudi=80`) ولا يزال غير جاهز.

### Phase 12 — preflight جاهز فقط

قبل Phase 12 أضيفت طبقة Governance & Engineering Standards. اقرأ:

- [PROJECT_CONSTITUTION.md](./PROJECT_CONSTITUTION.md)
- [LANGUAGE_SEGMENTATION.md](./LANGUAGE_SEGMENTATION.md)
- [TOKENIZATION_POLICY.md](./TOKENIZATION_POLICY.md)
- [DATASET_GOVERNANCE.md](./DATASET_GOVERNANCE.md)
- [AGENT_ENGINEERING_RULES.md](./AGENT_ENGINEERING_RULES.md)
- [PHASE12_PREFLIGHT_REPORT.md](./PHASE12_PREFLIGHT_REPORT.md)
- [PROJECT_IDENTITY.md](./PROJECT_IDENTITY.md)
- [ENGINEERING_RULES.md](./ENGINEERING_RULES.md)
- [AGENT_INSTRUCTIONS.md](./AGENT_INSTRUCTIONS.md)
- [PROJECT_MAP.md](./PROJECT_MAP.md)
- [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)

أُضيفت بوابة فحص قبل تدريب tokenizer:

```bash
make corpus-audit
```

وأضيف endpoint حي:

```text
GET /system/corpus-audit
GET /system/phase12-readiness
```

وللحصول على القرار نفسه بدون restart للسيرفر:

```bash
make phase12-readiness
```

هذه تستخدم `scripts/audit_training_corpus.py` وتجمع فحص كل ملفات `.jsonl` في `data/corpus/chat/jsonl/`.

بعد ملاحظة سامي أن الفحص السابق غير شامل، أُضيف جرد مصادر شامل:

```bash
make source-inventory
```

```text
GET /system/source-inventory
```

الجرد الحالي يميز بين:

- `chat_training_jsonl`: المصدر الحواري الرسمي، فارغ حاليًا.
- `saudi_dialect_training_tasks_seed_v1`: ملف محلي خاص فيه 1032 مهمة لهجة سعودية، مرشح tokenizer/تحويل لاحق، وليس chat corpus مباشرًا.
- `saudi_seed_v1_lexicon_reference`: قاموس سعودي محلي خاص فيه 516 مدخلًا، مرجع لهجي لا يرفع ولا يدخل كحوار مباشر.
- `mo3jam_saudi_import_slot`: موضع استيراد مؤجل permission-gated.

الوضع الحالي:

```text
status: READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

والسبب: أُضيف seed أول باسم `data/corpus/chat/jsonl/first_dialogue_seed.jsonl` فيه 20 محادثة سعودية gold، ثم `protected_terms_seed_v1.jsonl` فيه 10 محادثات لتغطية protected terms. يمر `make corpus-audit` بعدد `30/30`.

مع ذلك، لا تشغّل `make train-bpe` حتى بعد ظهور `corpus-audit`:

```text
status: READY_FOR_PHASE_12_TOKENIZER_TRAINING
```

تم تشغيل Phase 12 tokenizer v1 بإذن صريح من سامي على corpus صغير سابقًا. لا تعامل v1 كتشغيل لغوي متوازن؛ Phase 22 رفع corpus الحالي إلى 280 سجلًا فقط (`msa=200`, `saudi=80`) وما زال التوازن والعدد غير كافيين.

أضيفت بوابة تنفيذية فوق ذلك: `make train-bpe` و`scripts/train_bpe.py` يرفضان البدء بدون:

```text
--confirm-phase12-permission
```

سامي أعطى إذنًا صريحًا عامًا لمتابعة التدريب والاختبارات والمراحل المسجلة. استخدم هذا العلم عند الحاجة مع توثيق التشغيل.

تقرير preflight الحالي يقول:

```text
Phase 12 tokenizer v1: COMPLETED_WITH_LIMITS
vocab: 261
merges: 218
missing language balance: msa
```

### Phase 18 — Data Expansion Loop v1 — اكتملت

أضيفت طبقة تمنع التعلم الخفي من محادثات سامي، لكنها تجعل جمع البيانات أسهل:

- زر `تصدير` في [apps/api/static/chat.html](../apps/api/static/chat.html) يخرج JSONL محليًا للمراجعة.
- export يضع دائمًا `training_allowed=false`, `quality=needs_review`, `license=user-review-required`.
- [scripts/prepare_dialogue_batch.py](../scripts/prepare_dialogue_batch.py) يحول المراجعات إلى corpus تدريبي فقط عند تمرير `--training-allowed`.
- [sf_ai/datasets/dialogue_batch.py](../sf_ai/datasets/dialogue_batch.py) يفرض provenance/dialect/quality ويتخطى السجلات الحساسة افتراضيًا.
- التقرير الافتراضي: [artifacts/reports/dialogue_batch_report.json](../artifacts/reports/dialogue_batch_report.json).
- الوثيقة: [DATA_IMPROVEMENT_LOOP.md](./DATA_IMPROVEMENT_LOOP.md).

### Phase 19 — SF-50M Readiness Gate — تعمل

- `make phase19-readiness`
- `GET /system/phase19-readiness`
- القرار الحالي: `NOT_READY_EXPAND_CORPUS_FIRST`
- السبب: corpus الحالي 280 سجلًا فقط، والحد الأدنى العملي الحالي 5000 سجل محكوم مع توازن `msa + saudi`.
- مختبر سامي المحلي يسمح بتجربة المولد الخام على الرسائل غير الحساسة من مجالات skeleton عبر `SF_LAB_GENERATION_FOR_NON_SENSITIVE=true`.

### Phase 20 — Domain Activation Gates — تعمل

- `make phase20-gates`
- `GET /system/phase20-gates`
- القرار الحالي: `PHASE20_GATES_ACTIVE_NO_DOMAIN_AUTO_ACTIVATED`
- المجال النشط الوحيد: `chat`
- المرشحان لمراجعة صريحة فقط: `web`, `research`
- المجالات الحساسة تبقى محجوبة بسبب `safety_policy_missing` واختبارات التفعيل.
- أضيف `productivity` كسكيلتون كامل بعد أن كشفت البوابة أنه موجود في registry دون module/manifest.

### Phase 21 — Generative Roadmap — مكتملة

- `docs/GENERATIVE_ROADMAP.md`
- امتدت الخطة الرسمية إلى Phase 30.
- التدريب الفعلي بدأ في Phase 13/14، لكن أول تدريب جودة مفيد قادم هو Phase 24.
- أول فرصة لحوار قصير مولّد مقنع: Phase 26.
- الهدف الرسمي لحوار مولّد مستقر نسبيًا: Phase 28.

### Phase 22 — Gold Dialogue Corpus v2 — بوابة تعمل

- `make phase22-readiness`
- `make phase22-plan`
- `make phase22-next-batch`
- `make phase22-review-intake`
- `GET /system/phase22-readiness`
- `GET /system/phase22-collection-plan`
- `GET /system/phase22-next-batch`
- `GET /system/phase22-review-intake`
- القرار الحالي: `NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2`
- الموجود: 280 سجلًا: 200 `msa` و80 `saudi`
- الهدف: 500 سجل، مع 200 على الأقل لكل من `msa` و`saudi`
- خطة الجمع الحالية: 120 سعودي + 100 مرنة، نحو 9 batches بحجم 25
- المهمة الفورية الحالية: `saudi_003` عبر `make phase22-next-batch`
- أضيفت ثمان دفعات فصيحة معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl` مع بطاقات provenance.
- أضيف seed مصطلحات فصحى تدريبي: `data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl` وفيه 22 سجلًا `gold`; هذا corpus فعلي، وليس موردًا مرشحًا.
- بنك التأليف الفصيح: `resources/phase22_authoring/msa_prompt_bank_v1.json`، ملف مساعدة فقط وليس corpus، وحقوله `training_allowed=false` و`synthetic_llm_data=false`.
- مصطلحات الفصحى المرشحة: `resources/tokenization/protected_terms_msa_candidate.txt` و`resources/tokenization/preferred_merges_msa_candidate.txt`. هذه موارد سياسة غير نشطة، ليست corpus ولا vocab pretrained، وتُستخدم لتوجيه دفعات الفصحى القادمة قبل تفعيلها في tokenizer.
- حفظ review المحلي: `POST /chat/review-export` وزر `حفظ للمراجعة` في `/ui/chat` يكتبان إلى `data/corpus/chat/review/` فقط مع `training_allowed=false`.
- كل export/training record يحمل الآن user ownership:
  `owner_user_id`, `created_by_user_id`, `target_user_id`, `user_scope`.
- المسار الحالي `single_user` بمعرف `sami-local` حتى لا تختلط محادثات المستخدمين عند التوسع لاحقًا.
- بروتوكول سامي الجديد: الوكيل هو من يختبر الواجهة/API ويؤلف ويراجع ويعتمد دفعات corpus ويرتّب الملفات والتقارير. لا تطلب من سامي خطوات حفظ/تصدير/اعتماد يدوية إذا كنت تستطيع تنفيذها. سامي يستلم النتيجة النهائية ويقرر الاقتناع فقط.
- review intake الحالي: `data/corpus/chat/review/sample_review_export.jsonl` مرشح للمراجعة فقط؛ لا يدخل التدريب تلقائيًا.
- `phase22-review-intake` يعرض أيضًا `quality_score`, `quality_label`, و`quality_blockers`; لا تعتبر جلسة قوية للتدريب إلا إذا كانت متعددة الأدوار غالبًا 3 user + 3 assistant على الأقل.
- `/ui/chat` يعرض مؤشر جودة تصدير محليًا، ويضيف `ui_quality_score/ui_quality_label/ui_quality_blockers` إلى export metadata.
- الواجهة المستقرة يجب أن تعمل بـ `generator=template` افتراضيًا، وهذا يعني قوالب ثابتة لا مولدًا مقنعًا. لا تطلب من سامي اختبار المولد حتى Phase 24/25 على الأقل.
- أي export يحتوي ردود `sf_10m_v0_1` يجب أن يبقى review evidence فقط، و`phase22-review-intake` يميّزه ولا يعدّه candidate تدريب جودة.
- الممنوع: synthetic LLM data من مصدر خارجي أو مجهول.
- حوار الوكيل المؤلف بتفويض سامي يمكن أن يدخل corpus مباشرة إذا وُسم كـ `owner-delegated agent-authored` مع source/license/quality/notes كاملة، وبقي ضمن `msa + saudi`، ودون أي pretrained أو dataset خارجي.

### تستطيع الآن العمل على:

- أكمل دفعات `saudi_003..saudi_007` ثم المرنة حتى تمر Phase 22 readiness، ثم أعد corpus-audit وPhase 19/20/22 gates.

---

## 5. القواعد التي يجب أن تتبعها بصرامة

### مع الكود

1. **لا تستورد أي pretrained model أو embedding** — حتى لو كان "محليًا" ومفتوحًا.
2. **CrawlerBase يرفع `CrawlerPermissionError`** بدون `permission_granted=True` — لا تكسر هذا.
3. **CheckpointMetadata.sf_origin = True** مقفل — لا تحاول تجاوزه.
4. **TrainingConfig.sovereign = True** مقفل — لا تحاول تجاوزه.
5. **أي مصدر بيانات خارجي جديد يحتاج توثيق provenance**. سامي أعطى تفويضًا عامًا للتأليف المحلي بالنيابة عنه، لكن لا تستخدم مصادر مجهولة أو LLM synthetic data خارجي.
6. **شفافية User-Agent** على أي crawl: `SF.AI Research Crawler - permission-gated`.
7. **rate-limit أدنى 2 ثوانٍ** بين الطلبات على نفس الـ domain.

### مع المستخدم

1. سامي يكتب بالعربية الفصحى أحيانًا وأخرى بلهجة سعودية. **رد بالعربية الواضحة.**
2. كن **حازمًا في التنفيذ، شفافًا في النتائج**. لا تتظاهر بأن شيئًا اكتمل قبل التحقق.
3. **لا تختصر القرارات المعمارية** — اشرح لماذا اخترت X بدل Y لو سامي سأل.
4. **استخدم Phase 0–9 كمرجع** — لا تخترع مراحل جديدة من فراغ.
5. التفويض الحالي: استمر في المراحل المسجلة دون انتظار موافقة جديدة، لكن عند الشك في مصدر خارجي أو مخاطرة حساسة → توقّف واسأل.

### مع الاختبارات

1. كل ملف اختبار جديد يضيف 100% من تغطيته على المحاولة الأولى — لا تحفظ الكود ثم تجرّب.
2. الاختبارات يجب أن **تعمل بدون شبكة**. استخدم fixtures محلية.
3. عند فشل تست واحد، **افهم السبب الجذري قبل التعديل**. لا تعطّل الاختبارات.

---

## 6. خارطة الملفات السريعة

```
apps/api/                       FastAPI app + routers + static chat UI
sf_ai/core/
  ├── orchestrator/             Orchestrator (يستدعي NLP → Router → Module/Composer)
  ├── router/                   DomainRouter + IntentRouter (lens-aware)
  ├── semantic/                 lexical + hashing + explorer
  ├── index/                    CapabilityRegistry (default_registry.yaml)
  ├── composer/                 ResponseComposer (per-domain replies)
  └── nlp/                      ArabicNormalizer, Dialect, Arabizi, Typo, IntentDetector
sf_ai/modules/
  ├── chat/                     ChatModule (الـ module الوحيد النشط فعليًا)
  ├── web/                      ready_offline — لم يُفعَّل
  └── research/                 ready_offline — لم يُفعَّل
sf_ai/memory/                   Phase 8 RAG (SparseStore + HashingVectorStore + Hybrid)
sf_ai/tools/web/                crawler_base + robots + rate_limiter + extractors
sf_ai/models/
  ├── tokenizer/                CharTokenizer + SF-BPE
  └── transformer/              TinyTransformer (random init، scaffolding للتدريب)
sf_ai/training/                 device + checkpoints + schedules + train_tiny_lm
sf_ai/datasets/                 schemas + validators + loaders + saudi_seed
resources/lexicons/             YAML lexicons (Phase 3) + imported/ (Phase 3.5/3.6)
data/corpus/                    حوار المستخدم + قاموس سعودي
docs/                           كل الوثائق الفنية
tests/                          435 اختبار، 48 ملف
scripts/                        CLI: run_chat_server, validate_dataset, train_bpe, import_mo3jam_saudi
```

---

## 7. كيف تفتح الشاشة وتختبر

```bash
# (السيرفر شغّال بالفعل، لكن لو احتجت تشغيله):
cd /Users/sami/workSF/SF.AI
bash scripts/run_chat_server.sh

# في المتصفح:
open http://127.0.0.1:8123/ui/chat

# اختبارات سريعة من CLI:
curl -s -X POST http://127.0.0.1:8123/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"شلونك","session_id":"test"}'
```

رسائل مفيدة للاختبار اليدوي:
| رسالة | المتوقع |
|--------|---------|
| `مرحبا` | chat.greeting, dispatch=module:chat |
| `شلونك` | chat.smalltalk, dialect=saudi, dispatch=module:chat |
| `عندي؟` | chat.clarification |
| `سعودي` | chat.language_preference |
| `من انت` | chat.identity |
| `من صنعك` | chat.who_made_you |
| `شكرا` | chat.thanks |
| `ساعدني` | chat.help |
| `عندي ألم في الراس` | domain=medical, requires_safety=true, رد آمن مخصص |
| `ابي اسوي كود` | domain=coding, skeleton_only, رد مخصص للبرمجة |

---

## 8. القرارات المعمارية الكبرى التي اتُّخذت

- **NLP قبل Router**: كل رسالة تمر بـ `analyze_user_text` ثم يستخدم Router عدسات مختلفة (original/normalized/canonical/corrected) لإصدار إشارات `phrase/normalized/dialect_alias/typo_corrected/fuzzy`.
- **Module dispatch**: الـ Orchestrator يدفع للـ Module المناسب فقط حين `domain.status == "active"` وغير `requires_safety`. غير ذلك → Composer.
- **القواميس المستوردة معزولة**: `imported/mo3jam/` و `imported/saudi_seed_v1/` خارج YAMLs الأصلية. تُحمَّل عبر env flags.
- **RAG غير مرتبط بـ ChatModule بعد**: HybridRetriever موجود لكن لا يُحقن تلقائيًا. ربطه قرار صريح لاحق.
- **Saudi Seed safety filter**: confidence=high + not sensitive + not requires_native_review = ~300 مدخل runtime-safe من أصل 516.

---

## 9. عبارات للتواصل مع المستخدم

- إنهاء أي مرحلة بملخص عربي واضح يتضمن رقم الرحلة، القاموس المتبع، الاختبارات، والرفع إن تم.
- التفويض الحالي يلغي انتظار الموافقة بين المراحل المسجلة، لكن لا يلغي قواعد: لا pretrained، لا مصادر مجهولة، لا بيانات حساسة، لا hidden shortcuts.
- عند البدء بمهمة كبيرة: اشرح في 3 أسطر **ما ستعمله** قبل التنفيذ.
- عند الفشل: قل بصراحة **ما لم يعمل**، لا تختبئ خلف "تم".

---

## 10. لو احتجت تتذكر شيئًا واحدًا فقط

> SF.AI = نظام ذكاء اصطناعي **سامي يفهمه بكل وزن فيه**. لا تُدخل عقلًا أجنبيًا إلى الأوزان. الأدوات نعم، العقول لا.

— نهاية وثيقة التسليم.
