# PHASE_STATUS.md

## SF.AI — سجل حالة المراحل

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الرحلة الحالية:** **Phase 27.15 / 30**
- **المرحلة الحالية:** **Phase 27.15 — Social/Lexical Curriculum + No-Repeat Decoding**
- **حالة المرحلة الحالية:** **مكتملة؛ eval تحسن لكن canary الدلالي الصارم حجب التوليد**
- **المرحلة التالية المقترحة:** Phase 27.16 لإصلاح prompt-to-answer conditioning قبل أي تكبير إلى `SF-50M`.
- **القاموس/المسار اللغوي الحالي:** `msa + saudi` فقط؛ القاموس المتبع `Saudi Seed v1` مع `safety_terms.yaml`.
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
| Phase 22 | Gold Dialogue Corpus v2 | ✅ completed_ready_for_phase23 | ✅ |
| Phase 23 | Tokenizer v2 Retrain & Audit | ✅ completed_ready_for_phase24 | ✅ |
| Phase 24 | SF-10M v0.2 Quality Training | ✅ completed_with_limits_runtime_blocked | ✅ |
| Phase 25 | Generated Chat Canary v1 | ✅ completed_guarded_canary_real_model_blocked | ✅ |
| Phase 26 | SF-50M v0.1 Readiness | ✅ completed_not_ready_improve_sf10m_and_canary | ✅ |
| Phase 27 | Dialogue Evaluation v2 and corpus expansion plan | ✅ completed_baseline_pass_corpus_gate_passed | ✅ |
| Phase 27.5 | SF-10M Dialogue-Format Repair | ✅ completed_with_limits_runtime_blocked | ✅ |
| Phase 27.6 | SF-10M Assistant-Target Training | ✅ completed_with_limits_runtime_blocked | ✅ |
| Phase 27.7 | Fixed Split + Gold Social Canary | ✅ completed_quality_gate_runtime_blocked | ✅ |
| Phase 27.8 | SF-10M v0.6 Split Training | ✅ completed_with_numeric_improvement_runtime_blocked | ✅ |
| Phase 27.9 | Generation Quality Harness | ✅ completed_harness_blocks_v0_6_runtime | ✅ |
| Phase 27.10 | Short Response Repair | ✅ completed_numeric_improvement_generation_still_blocked | ✅ |
| Phase 27.11 | Objective/Decoding Diagnosis | ✅ completed_stop_boundary_missing_generation_blocked | ✅ |
| Phase 27.12 | Assistant Boundary/EOS Repair | ✅ completed_boundary_eos_partial_semantic_blocked | ✅ |
| Phase 27.13 | SF-10M v0.8 Boundary/EOS Wider Training | ✅ completed_eval_improved_generation_still_blocked | ✅ |
| Phase 27.14 | Sovereign Training Quality Tooling Decision | ✅ completed_tooling_adoption_decision_no_training | ✅ |
| Phase 27.15 | Social/Lexical Curriculum + No-Repeat Decoding | ✅ completed_eval_improved_strict_generation_blocked | ✅ |
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
- نتيجة `make phase12-readiness`: يعرض أن v1 اكتمل وأن `msa + saudi` موجودتان حاليًا؛ tokenizer v2 أصبح جاهزًا لاحقًا في Phase 23.
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
  - `preflight_pass=true` بعد توفر `msa + saudi`
  - `can_train_now=false` لأن tokenizer v1 مكتمل، وPhase 23 وفرت tokenizer v2 للمرحلة التالية
  - `missing_required_dialects=[]`
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
  - السبب: corpus الحالي بعد تنظيف الحوارات التشغيلية والتوسعة الطبيعية صار `5143` سجلًا وتجاوز الحد الأدنى العملي `5000`، لكن بوابات الجودة لم تمر.
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
  - تم توثيق أن التدريب الفعلي بدأ في Phase 13/14، وأن أول تدريب جودة مفيد سيأتي في Phase 24.
  - تم تحديد أن الحوار المولّد المقنع يحتاج تدرجًا: Phase 24 أعطت تحسنًا معمليًا، Phase 26 منعت SF-50M، وPhase 27 وضعت خطة corpus قبل أي قفزة.
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
  - القرار الحالي: `READY_FOR_PHASE23_TOKENIZER_V2`.
  - الموجود الحالي: 500 سجل تدريب جاهز: 250 `msa` و250 `saudi`.
  - المتبقي: 0 سجل للوصول إلى 500.
  - خطة الجمع الحالية: مكتملة؛ لا توجد batches متبقية في Phase 22.
  - أضيفت بوابة اكتمال صارمة: `phase22-completion-gate`، وقرارها الحالي `PHASE22_COMPLETE_READY_FOR_PHASE23`.
  - `phase22-plan` يعرض الآن `planned_batches=[]`.
  - `phase22-next-batch` يعرض الآن `NO_BATCHES_REMAINING_RECHECK_READINESS`.
  - أضيفت ثمان دفعات فصيحة معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl`، بإجمالي 178 سجلًا فصيحًا `silver` مؤلفة/مراجعة بتفويض سامي، مع بطاقات provenance.
  - أضيفت سبع دفعات سعودية معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_saudi_001.jsonl` إلى `dialogue_batch_v2_saudi_007.jsonl` بإجمالي 170 سجلًا سعوديًا `silver`، وأصبح الحد الأدنى السعودي مكتملًا مع seed/protected coverage.
  - أضيفت أربع دفعات مرنة معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_flex_001.jsonl` إلى `dialogue_batch_v2_flex_004.jsonl` بإجمالي 100 سجل `silver` موزعة بين الفصحى والسعودية.
  - أضيف seed مصطلحات فصحى تدريبي: `data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl` وفيه 22 سجلًا `gold` لتغطية مصطلحات تشغيل/حوكمة/تدريب أساسية.
  - أضيفت حقول فصل المستخدمين في schema/audit/UI/export/corpus: `owner_user_id`, `created_by_user_id`, `target_user_id`, `user_scope`.
  - المسار الحالي `sami-local` و`single_user`، والهدف منع خلط محادثات أو ذاكرة مستخدم مع مستخدم آخر عند التوسع لاحقًا.
  - أضيف بنك تأليف فصيح غير تدريبي في `resources/phase22_authoring/msa_prompt_bank_v1.json`: أكثر من 80 موضوعًا فصيحًا لبناء batches الفصحى، مع `training_allowed=false` و`synthetic_llm_data=false`.
  - review intake الحالي: ملف عينة واحد في `data/corpus/chat/review/` مرشح للمراجعة، ولا يدخل التدريب تلقائيًا.
  - أضيفت بوابة جودة داخل review intake: `quality_score`, `quality_label`, و`quality_blockers`.
  - أضيف مؤشر جودة التصدير داخل `/ui/chat` تاريخيًا، ثم أُخفي لاحقًا لأن الواجهة أصبحت لاختبار الحوار فقط والوكيل يتولى حفظ/اعتماد البيانات.
  - أضيفت لوحة بوابة Phase 22 داخل `/ui/chat`، تقرأ `/system/phase22-readiness` و`/system/phase22-collection-plan` وتعرض عدد corpus الحالي، المتبقي، وحالة `msa/saudi`، والمهمة التالية مباشرة.
  - أضيفت لوحة مهمة الجمع الحالية داخل `/ui/chat` تاريخيًا، ثم أُخفيت لاحقًا. endpoints Phase 22 باقية للوكيل فقط.
  - أضيف زر `موضوعات أخرى` داخل لوحة مهمة الجمع الحالية للتنقل في بنك التأليف الفصيح، مع `authoring_topic_count` في metadata.
  - أضيف endpoint `POST /chat/review-export` لحفظ review JSONL محليًا في `data/corpus/chat/review/` فقط، مع رفض `training_allowed=true`; الزر لم يعد ظاهرًا في `/ui/chat`.
  - القاعدة العملية الجديدة: ملف التصدير المفيد يجب أن يحتوي غالبًا 3 أدوار مستخدم + 3 ردود مساعد على الأقل، وبدون ردود raw من `sf_10m_v0_1/sf_10m_v0_2`.
  - القاعدة العملية الأحدث: الوكيل يستطيع تأليف/مراجعة/اعتماد دفعات Phase 22 مباشرة كـ `owner-delegated agent-authored` بدون انتظار حفظ أو تصدير من سامي، بشرط اكتمال `source/license/quality/training_allowed/user_scope/notes` ونجاح الاختبارات.
  - صححت تشغيل الواجهة المستقرة: `generator=template` افتراضيًا، أي قوالب ثابتة لا مولد؛ و`SF-10M` الخام يبقى مختبرًا صريحًا فقط.
  - أضيفت حماية export/review intake لتمييز أي جلسة تحتوي ردود `sf_10m_v0_1/sf_10m_v0_2` ومنع عدّها كـ candidate تدريب جودة.
  - أضيفت intents محددة لعبارات Phase 22 اليومية: اختبار الحوار الفصيح، الخطوة التالية، والفرق بين التدريب والتفعيل.
  - لا يوجد ناقص في Phase 22 حاليًا؛ الفصحى وصلت إلى 250، والسعودي وصل إلى 250، والمجموع 500.
  - لا تدريب جديد بدأ.
- بدأ وانتهى Phase 23 Tokenizer v2 Retrain & Audit:
  - أُعيد تدريب SF-BPE tokenizer من corpus Phase 22 المتوازن فقط.
  - artifact: `artifacts/tokenizers/sf_bpe/v2/`.
  - أضيف `make phase23-tokenizer-audit`.
  - أضيف `GET /system/phase23-tokenizer-audit`.
  - أضيف [PHASE23_TOKENIZER_V2_REPORT.md](./PHASE23_TOKENIZER_V2_REPORT.md).
  - القرار الحالي: `COMPLETED_READY_FOR_PHASE24`.
  - النتائج: `vocab=4493`, `merges=4386`, `words_seen=23190`, `unique_words=2492`.
  - corpus المستخدم: 500 سجل، `msa=250`, `saudi=250`, بدون issues.
  - مقارنة v1/v2: v1 كان `vocab=261`, `merges=218`, سعودي فقط؛ v2 صار متوازنًا وأوسع.
  - protected Saudi terms: متوسط tokens تحسن من `4.0` إلى `2.3`، ولا توجد roundtrip failures أو aggressive splits.
  - لا تدريب نموذج لغوي بدأ في Phase 23.
- بدأ وانتهى Phase 24 SF-10M v0.2 Quality Training:
  - tokenizer: `artifacts/tokenizers/sf_bpe/v2`.
  - corpus: `500` سجل، `msa=250`, `saudi=250`.
  - النموذج: `sf-10m`, random init, `7,444,992` parameters.
  - التدريب: `2000` خطوة، `epochs=25`, `seq_len=64`, `batch_size=4`.
  - loss: `8.4751 → 2.8256`.
  - eval: loss `2.5779`, perplexity `13.17`.
  - checkpoint المحلي: `artifacts/checkpoints/sf_10m_v0_2/sf-10m-step2000`، غير مرفوع إلى git.
  - القرار: `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`.
  - التوليد أقل تكرارًا من v0.1، لكنه ما زال غير متماسك ولا يصلح للواجهة كمساعد ذكي.
  - أضيف [PHASE24_SF10M_V0_2_REPORT.md](./PHASE24_SF10M_V0_2_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_2_training_report.json`.
  - أضيف `artifacts/samples/sf_10m_v0_2_generations.md`.
- بدأ وانتهى Phase 25 Generated Chat Canary v1:
  - أضيف `sf_ai/modules/chat/generation_guard.py`.
  - أضيف شرط `SF_GENERATOR_CANARY=true` فوق فلاغات المختبر السابقة.
  - حُدّث `NativeGenerator` إلى tokenizer v2 وcheckpoint `sf-10m-step2000`.
  - يضع canary metadata `generator=sf_10m_v0_2` عند النجاح فقط.
  - عند فشل guard يعود `ChatModule` إلى القالب ويضيف `native_generator:canary_blocked`.
  - التجربة الحقيقية على prompt: `اكتب رد قصير عن هدف SF.AI` حُجبت بسبب `generation_guard:malformed_token`.
  - القرار: `COMPLETED_GUARDED_CANARY_REAL_MODEL_BLOCKED`.
  - أضيف [PHASE25_GENERATED_CHAT_CANARY_REPORT.md](./PHASE25_GENERATED_CHAT_CANARY_REPORT.md).
  - أضيف `artifacts/reports/phase25_generation_canary_report.json`.
- بدأ وانتهى Phase 26 SF-50M v0.1 Readiness:
  - أضيف `sf_ai/training/phase26_readiness.py`.
  - أضيف `scripts/phase26_readiness.py` وهدف `make phase26-readiness`.
  - أضيف endpoint حي: `GET /system/phase26-readiness`.
  - القرار: `NOT_READY_IMPROVE_SF10M_AND_CANARY`.
  - `can_start_sf50m_training=false`.
  - corpus كان `500` سجل عند قرار Phase 26، ثم صار `5143` بعد تنظيف الحوارات التشغيلية والتوسعة الطبيعية؛ corpus gate صار ناجحًا.
  - tokenizer v2 جاهز، لكن runtime quality غير جاهزة لأن Phase 25 حجب `SF-10M v0.2`.
  - blockers: `phase24_runtime_quality_blocked`, `phase25_real_model_blocked`, `hallucination_checks_missing`, `repetition_checks_failed`.
  - أضيف [PHASE26_SF50M_READINESS_REPORT.md](./PHASE26_SF50M_READINESS_REPORT.md).
  - أضيف `artifacts/reports/phase26_sf50m_readiness_report.json`.
- بدأ وانتهى Phase 27 Dialogue Evaluation v2 + Corpus Expansion Plan:
  - أضيف `eval/prompts/dialogue_v2.json`.
  - أضيف `sf_ai/evaluation/phase27.py`.
  - أضيف `scripts/phase27_dialogue_eval.py` وهدف `make phase27-dialogue-eval`.
  - أضيف endpoint حي: `GET /system/phase27-dialogue-eval`.
  - suite متعدد الأدوار: `7` سيناريوهات و`19` turn.
  - النتيجة: `19/19`, pass rate `100%`.
  - `generator_modes={'template': 19}`، أي لا يوجد حوار مولّد مفتوح بعد.
  - خطة corpus الأصلية: `500 → 5000`. بعد الدفعات الطبيعية صار corpus `5143` والمتبقي `0`.
  - القرار: baseline نجح، وcorpus gate نجح، لكن open generator غير جاهز.
  - Phase 28 محظورة حتى ينجح `SF-50M` في eval v2.
  - أضيف [PHASE27_DIALOGUE_EVAL_V2_REPORT.md](./PHASE27_DIALOGUE_EVAL_V2_REPORT.md).
  - أضيف `eval/reports/dialogue_eval_v2.json`.
  - أضيف `artifacts/reports/phase27_dialogue_eval_v2_report.json`.
- بدأت توسعة corpus بعد Phase 27:
  - أضيف `dialogue_batch_v3_msa_001.jsonl` وفيه 25 سجل فصيح.
  - أضيف `dialogue_batch_v3_saudi_001.jsonl` وفيه 25 سجل سعودي.
  - أضيف `dialogue_batch_v3_msa_002.jsonl` وفيه 250 سجل فصيح.
  - أضيف `dialogue_batch_v3_saudi_002.jsonl` وفيه 250 سجل سعودي.
  - أضيف `dialogue_batch_v3_msa_003.jsonl` وفيه 250 سجل فصيح.
  - أضيف `dialogue_batch_v3_saudi_003.jsonl` وفيه 250 سجل سعودي.
  - أضيف `dialogue_batch_v4_msa_004.jsonl` وفيه 750 سجل فصيح طبيعي.
  - أضيف `dialogue_batch_v4_saudi_004.jsonl` وفيه 750 سجل سعودي طبيعي.
  - أضيف `dialogue_batch_v5_msa_005.jsonl` وفيه 750 سجل فصيح طبيعي.
  - أضيف `dialogue_batch_v5_saudi_005.jsonl` وفيه 750 سجل سعودي طبيعي.
  - أضيف `dialogue_batch_v6_msa_006.jsonl` وفيه 750 سجل فصيح طبيعي.
  - أضيف `dialogue_batch_v6_saudi_006.jsonl` وفيه 750 سجل سعودي طبيعي.
  - corpus بعد Batch 006 صار `5143`: `msa=2549`, `saudi=2594`.
  - المتبقي إلى هدف `5000` صار `0` سجلًا.
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md).
- بدأ وانتهى Phase 27.5 SF-10M Dialogue-Format Repair:
  - أضيف `ChatDataset.iter_dialogue_texts()` حتى يتدرب النموذج على حوار كامل بعلامات `المستخدم:` و`المساعد:` بدل رسائل منفصلة.
  - أصبح `train_tiny_lm` يستخدم `--stream-format dialogue` افتراضيًا، مع إبقاء `messages` للتشخيص.
  - أضيف `--chat-prompt` إلى `evaluate_tiny_lm`.
  - أضيف `extract_dialogue_reply()` لاستخراج رد المساعد فقط من النص المولّد.
  - دُرّب `SF-10M v0.4` على corpus الحالي `5143` سجلًا، `steps=4000`, `seq_len=64`, `batch_size=4`, `device=mps`.
  - loss التدريب انخفض من `8.4662` إلى `1.4070`.
  - eval على `20` batch: `loss=5.8267`, `perplexity=339.24`.
  - العينات صارت عربية قصيرة لكنها غير مرتبطة كفاية بالسؤال، مثل: `لا، الاعتذار الطرف الآخر.`
  - القرار: `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`.
  - لا يتم تفعيل `SF-10M v0.4` في الواجهة، ولا يبدأ `SF-50M` قبل إصلاح جودة الردود.
  - أضيف [PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md](./PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_4_dialogue_format_report.json`.
  - أضيف `artifacts/samples/sf_10m_v0_4_generations.md`.
- بدأ وانتهى Phase 27.6 SF-10M Assistant-Target Training:
  - أضيف `--loss-scope assistant` إلى `train_tiny_lm` و`evaluate_tiny_lm`.
  - أضيف `_encode_assistant_target_dialogue()` لتعليم رد المساعد فقط، مع masking لسياق المستخدم وعلامات الأدوار بقيمة `-100`.
  - دُرّب `SF-10M v0.5` على corpus الحالي `5143` سجلًا، `steps=4000`, `seq_len=64`, `batch_size=4`, `device=mps`.
  - loss التدريب انخفض من `8.4643` إلى `2.3513`.
  - أفضل checkpoint مقاس كان `sf-10m-step2000`: `eval loss=6.5718`, `perplexity=714.65`.
  - العينات بدأت بشكل عربي أوضح لكنها مكررة وغير مرتبطة كفاية بالسؤال.
  - القرار: `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`.
  - لا يتم تفعيل `SF-10M v0.5` في الواجهة، ولا يبدأ `SF-50M`.
  - أضيف [PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md](./PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_5_assistant_target_report.json`.
  - أضيف `artifacts/samples/sf_10m_v0_5_generations.md`.
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md).
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md).
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_004_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_004_REPORT.md).
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_005_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_005_REPORT.md).
  - أضيف [PHASE27_CORPUS_EXPANSION_BATCH_006_REPORT.md](./PHASE27_CORPUS_EXPANSION_BATCH_006_REPORT.md).
- بدأ وانتهى Phase 27.7 Fixed Split + Gold Social Canary:
  - أضيف split manifest ثابت: `data/corpus/chat/splits/dialogue_split_v1.json`.
  - طريقة split: `sha256_bucket` مع salt موثق ونسبة eval `0.10`.
  - counts: `train=4703`, `eval=540`.
  - dialects: train `saudi=2360`, `msa=2343`; eval `saudi=284`, `msa=256`.
  - أضيفت دفعة gold اجتماعية صغيرة: 100 سجل طبيعي (`50` فصيح + `50` سعودي).
  - corpus الحالي صار `5243`: `msa=2599`, `saudi=2644`; كل السجلات `training_ready`.
  - أضيف `--split-manifest` و`--split-name` إلى training/evaluation حتى يتدرب v0.6 على train فقط ويُقاس على eval held-out.
  - أضيف `GenerationGuard.inspect_for_prompt()` لمنع الردود العربية الشكلية غير المتصلة بالسؤال.
  - canary الآن يحجب mismatch في أسئلة اجتماعية شائعة مثل `كيفك` و`شكرا` و`السلام عليكم` وتفضيل `سعودي`.
  - القرار: `COMPLETED_QUALITY_GATE_RUNTIME_BLOCKED`.
  - لا يتم تفعيل أي checkpoint مولّد في الواجهة حتى ينجح v0.6 على split الثابت وcanary prompt-aware.
  - أضيف [PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md](./PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md).
  - أضيف `artifacts/reports/phase27_7_fixed_split_gold_social_canary_report.json`.
- بدأ وانتهى Phase 27.8 SF-10M v0.6 Split Training:
  - دُرّب `SF-10M v0.6` على `train split` فقط: `4703` سجلًا.
  - استُخدم `loss_scope=assistant`, `steps=4000`, `batch_size=4`, `seq_len=64`, `device=mps`.
  - loss التدريب: `8.4743 → 3.7460`، وأفضل logged train loss كان `2.7407`.
  - تقييم eval split المعزول (`540` سجلًا) أظهر أفضل checkpoint عند `step4000`: loss `5.0227`, perplexity `151.82`.
  - canary على 10 prompts اجتماعية/يومية حجب `10/10` بسبب fragments مولّدة مشوهة مثل `الطرو`, `حارين`, `استعجه`.
  - القرار: `COMPLETED_WITH_NUMERIC_IMPROVEMENT_RUNTIME_BLOCKED`.
  - لا يتم تفعيل `SF-10M v0.6` في الواجهة، ولا يبدأ `SF-50M`.
  - أضيف [PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md](./PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_6_split_training_report.json`.
  - أضيف `artifacts/samples/sf_10m_v0_6_generations.md`.
- بدأ وانتهى Phase 27.9 Generation Quality Harness:
  - أضيف `eval/prompts/generation_quality_v1.json` كـ prompt suite قصيرة فصحى/سعودية.
  - أضيف `sf_ai/evaluation/generation_quality.py`.
  - أضيف `scripts/phase27_9_generation_quality_eval.py`.
  - أضيف `make phase27-generation-quality`.
  - نتيجة `SF-10M v0.6`: `0/10` prompts passed، و`runtime_allowed=false`.
  - السبب الأساسي: `model_artifact_fragment`.
  - القرار: `COMPLETED_GENERATION_QUALITY_HARNESS_BLOCKING_V0_6`.
  - أضيف [PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md](./PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md).
  - أضيف `artifacts/reports/generation_quality_v1_report.json`.
- بدأ وانتهى Phase 27.10 Short Response Repair:
  - أضيفت دفعة إصلاح قصيرة `300` سجل gold: `150` فصيح + `150` سعودي.
  - corpus الحالي صار `5543`: `msa=2749`, `saudi=2794`, `gold=431`, `silver=5112`.
  - split الحالي: `train=4973`, `eval=570`.
  - أضيف `scripts/phase27_10_write_short_response_repair_batch.py`.
  - دُرّب `SF-10M v0.7` على split الجديد: loss `8.4840 → 3.1259`.
  - أفضل eval: `sf-10m-step4000`, loss `4.7512`, perplexity `115.72`.
  - بعد توسيع `GenerationGuard` للـ fragments الجديدة، `phase27-generation-quality` على v0.7 أعطى `0/10` و`runtime_allowed=false`.
  - القرار: `COMPLETED_NUMERIC_IMPROVEMENT_GENERATION_STILL_BLOCKED`.
  - أضيف [PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md](./PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_7_short_repair_report.json`.
  - أضيف `artifacts/samples/sf_10m_v0_7_generations.md`.
- بدأ وانتهى Phase 27.11 Objective/Decoding Diagnosis:
  - أضيف `scripts/phase27_11_objective_probe.py` و`make phase27-objective-probe`.
  - شُغّل gold overfit probe على `16` ردًا قصيرًا (`msa=8`, `saudi=8`).
  - وصل التدريب إلى loss شبه صفري على micro-corpus، لكن clean-stop بقي `0/16`.
  - الأسباب: `guard:repetition=6`, `overgenerates_after_expected=10`.
  - التشخيص: النموذج يحفظ بدايات الردود لكنه لا يتعلم نهاية رد المساعد.
  - القرار: `FAILED_GOLD_OVERFIT_PROBE_BLOCK_SCALING`.
  - أضيف [PHASE27_11_OBJECTIVE_PROBE_REPORT.md](./PHASE27_11_OBJECTIVE_PROBE_REPORT.md).
  - أضيف `artifacts/reports/phase27_11_objective_probe_report.json`.
  - أضيف `artifacts/samples/phase27_11_objective_probe_generations.md`.
- بدأ وانتهى Phase 27.12 Assistant Boundary/EOS Repair:
  - أضيف `<eos>` كهدف صريح بعد كل رد مساعد في `assistant-target` training.
  - `NativeGenerator` و`evaluate_tiny_lm` صارا يوقفان decoding عند `<eos>`.
  - أضيف dialect conditioning من provenance: `النطاق: فصحى` أو `النطاق: سعودي`.
  - probe الحالي أعطى `semantic_clean_pass=5/16`, `guard_pass=9/16`.
  - القرار: `COMPLETED_BOUNDARY_EOS_PARTIAL_SEMANTIC_BLOCKED`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md](./PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md).
  - أضيف `artifacts/reports/phase27_12_eos_probe_report.json`.
  - أضيف `artifacts/samples/phase27_12_eos_probe_generations.md`.
- بدأ وانتهى Phase 27.13 SF-10M v0.8 Boundary/EOS Wider Training:
  - دُرّب `SF-10M v0.8` من الصفر 6000 خطوة على train split فقط.
  - استخدم التدريب `assistant` loss و`dialogue` stream و`<eos>` وdialect conditioning.
  - أفضل checkpoint: `sf-10m-step6000`.
  - eval split: loss `3.1875`, perplexity `24.23`.
  - أداة generation-quality تمرر dialect الآن إلى المولد، وتم تشديد `GenerationGuard` ضد fragments v0.8.
  - generation-quality الصارم: `3/10`, `runtime_allowed=false`.
  - القرار: `COMPLETED_EVAL_IMPROVED_GENERATION_STILL_BLOCKED`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_13_SF10M_V08_REPORT.md](./PHASE27_13_SF10M_V08_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_8_boundary_eos_training_report.json`.
  - أضيف `artifacts/reports/generation_quality_v1_v0_8_report.json`.
- بدأ وانتهى Phase 27.14 Sovereign Training Quality Tooling Decision:
  - اعتُمدت 10 أدوات جودة محلية بدون أي تدريب جديد.
  - أضيف `LocalExperimentTracker` لتسجيل التجارب في JSONL محلي.
  - أضيف `make phase27-quality-tooling`.
  - أضيف تقرير قرار الأدوات: `artifacts/reports/phase27_14_quality_tooling_decision_report.json`.
  - أضيف سجل التجارب المحلي: `artifacts/reports/experiment_registry.jsonl`.
  - القرار: `COMPLETED_TOOLING_ADOPTION_DECISION_NO_TRAINING`.
  - runtime المولد و`SF-50M` وPhase 28 ما زالت محظورة حتى تنجح بوابات الجودة.
  - التالي وقتها: Phase 27.15 لإصلاح social/lexical curriculum وdecoder no-repeat controls.
- بدأ وانتهى Phase 27.15 Social/Lexical Curriculum + No-Repeat Decoding:
  - أضيف no-repeat decoding إلى `GenerationConfig`.
  - أضيفت 400 عينة gold اجتماعية/لغوية: `msa=200`, `saudi=200`.
  - corpus الحالي: `5943` سجلًا، `issues=0`.
  - split الحالي: `train=5343`, `eval=600`.
  - دُرّب `SF-10M v0.10` 6000 خطوة.
  - أفضل eval: `sf-10m-step6000`, loss `3.0452`, perplexity `21.01`.
  - تم تشديد `generation_quality_v1` ليطلب required semantic terms لكل prompt.
  - canary الدلالي الصارم: `0/10`, `runtime_allowed=false`.
  - القرار: `COMPLETED_EVAL_IMPROVED_STRICT_GENERATION_BLOCKED`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md](./PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_10_social_lexical_curriculum_report.json`.
  - أضيف `artifacts/reports/generation_quality_v1_v0_10_strict_report.json`.

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
- اختبارات: `test_chat_ui.py` يثبت أن `/ui/chat` للاختبار فقط بلا أزرار حفظ/تصدير، مع بقاء endpoint المراجعة الداخلي وفصل المستخدمين.

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
GET  /health        → {"status":"ok","project":"SF.AI","phase":"Phase 27.15"}
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
495 passed in 16.81s
```

| ملف | عدد |
|------|------|
| test_arabic_normalizer.py | 16 |
| test_bpe_tokenizer.py | 13 |
| test_capability_registry.py | 5 |
| test_chat_module.py | 12 |
| test_chat_native_generator.py | 16 (Phase 15 + Phase 25 canary mode) |
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
| test_new_chat_intents.py | 38 (Phase 9/19 social polish + phase guidance) |
| test_nlp_pipeline.py | 9 |
| test_orchestrator.py | 7 |
| test_phase10_skeleton_domains.py | 4 (Phase 10) |
| test_phase16_eval_harness.py | 3 (Phase 16) |
| test_phase19_readiness.py | 2 (Phase 19) |
| test_phase20_domain_activation_gates.py | 6 (Phase 20) |
| test_phase22_readiness.py | 15 (Phase 22) |
| test_phase22_review_intake.py | 8 (Phase 22 + raw generator gate) |
| test_phase23_tokenizer_artifacts.py | 6 (Phase 23) |
| test_phase24_sf10m_v0_2_report.py | 3 (Phase 24) |
| test_phase25_generation_canary.py | 5 (Phase 25) |
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
