# AGENT_HANDOFF.md

## هذه وثيقة تسليم — للوكيل التالي الذي يكمل بناء SF.AI

> **قبل أن تفعل أي شيء، اقرأ أولًا [SF_AI_MASTER_GUIDE.md](./SF_AI_MASTER_GUIDE.md).**
> هذه الوثيقة صارت سجل تسليم تفصيلي، وليست نقطة الدخول الوحيدة. المالك (سامي)
> أعطى الإذن المتراكم لتنفيذ خطة بناء طويلة، وما تجده الآن هو منتصف الرحلة،
> لا بدايتها.

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
| Phase 22 | Gold Dialogue Corpus v2 | ✅ completed_ready_for_phase23 |
| Phase 23 | Tokenizer v2 Retrain & Audit | ✅ completed_ready_for_phase24 |
| Phase 24 | SF-10M v0.2 Quality Training | ✅ completed_with_limits_runtime_blocked |
| Phase 25 | Generated Chat Canary v1 | ✅ completed_guarded_canary_real_model_blocked |
| Phase 26 | SF-50M v0.1 Readiness | ✅ completed_not_ready_expand_corpus_and_improve_sf10m |
| Phase 27 | Dialogue Evaluation v2 + Corpus Expansion Plan | ✅ completed_baseline_pass_corpus_gate_passed |
| Phase 27.5 | SF-10M Dialogue-Format Repair | ✅ completed_with_limits_runtime_blocked |
| Phase 27.6 | SF-10M Assistant-Target Training | ✅ completed_with_limits_runtime_blocked |
| Phase 27.7 | Fixed Split + Gold Social Canary | ✅ completed_quality_gate_runtime_blocked |
| Phase 27.8 | SF-10M v0.6 Split Training | ✅ completed_with_numeric_improvement_runtime_blocked |
| Phase 27.9 | Generation Quality Harness | ✅ completed_harness_blocks_v0_6_runtime |
| Phase 27.10 | Short Response Repair | ✅ completed_numeric_improvement_generation_still_blocked |
| Phase 27.11 | Objective/Decoding Diagnosis | ✅ completed_stop_boundary_missing_generation_blocked |
| Phase 27.12 | Assistant Boundary/EOS Repair | ✅ completed_boundary_eos_partial_semantic_blocked |
| Phase 27.13 | SF-10M v0.8 Boundary/EOS Wider Training | ✅ completed_eval_improved_generation_still_blocked |
| Phase 27.14 | Sovereign Training Quality Tooling Decision | ✅ completed_tooling_adoption_decision_no_training |
| Phase 27.15 | Social/Lexical Curriculum + No-Repeat Decoding | ✅ completed_eval_improved_strict_generation_blocked |
| Phase 27.16 | Prompt-to-Answer Objective Repair | ✅ completed_objective_repair_runtime_blocked |
| Phase 27.17 | Prompt-to-Answer Micro-Probe | ✅ completed_micro_probe_breakthrough_runtime_blocked |
| Phase 27.18 | Tokenization/Decoding Hygiene Repair | ✅ completed_hygiene_audit_with_blockers |
| Phase 27.19 | Hygiene Repair Corpus/Probe | ✅ completed_repair_probe_still_runtime_blocked |
| Phase 27.20 | Tokenizer/Protected-Phrase Strategy | ✅ completed_ready_for_tokenizer_v3_runtime_blocked |
| Phase 27.21 | Tokenizer v3 Protected-Phrase Micro-Probe | ✅ completed_micro_probe_failed_runtime_blocked |
| Phase 27.22 | Spacing/Boundary Loss Repair | ✅ completed_partial_repair_runtime_blocked |
| Phase 27.23 | Semantic/Lexical Confusion Repair | ✅ completed_partial_repair_runtime_blocked |
| Phase 27.24 | Minimal Lexical Stabilization | ✅ completed_micro_probe_passed_runtime_blocked |
| Phase 27.25 | Held-out Generation Quality Canary | ✅ completed_heldout_canary_failed_runtime_blocked |
| Phase 27.26 | Held-out Objective Repair | ✅ completed_partial_runtime_blocked |
| Phase 27.27 | Broader Held-out Repair | ✅ completed_old_heldout_passed_shadow_blocked |
| Phase 27.28 | Intent-Conditioned Repair | ✅ completed_intent_conditioning_partial_runtime_blocked |
| Phase 27.29 | Topic-Conditioned Definition Repair | ✅ completed_topic_conditioning_leakage_blocked |
| Phase 27.30 | Fresh Mixed Shadow Canary | ✅ completed_16_of_18_runtime_blocked |
| Phase 27.31 | Natural Intent/Topic Dataset | ✅ completed_partial_runtime_blocked |
| Phase 27.32 | Balanced Natural Calibration | ✅ completed_partial_runtime_blocked |
| Phase 27.33 | Advice + Micro Stabilization | ✅ completed_all_generation_gates_passed_trial_design_ready |
| Phase 27.34 | Guarded Runtime Trial | ✅ completed_ready_for_ui_test |
| Phase 27.35 | Live UI Trial Observations | ✅ completed_ready_for_user_observation |
| Phase 27.36 | Live UI Triage | ✅ completed_quality_floor_active |
| Phase 27.37 | Supported Topic Expansion | ✅ completed_quality_gated |
| Phase 27.38 | Targeted Topic Curriculum/Probe | ✅ completed_partial_keep_current_runtime |
| Phase 27.39 | Topic-Isolation Repair | ✅ completed_partial_keep_current_runtime |
| Phase 27.40 | Tokenizer/Context Repair | ✅ completed_candidate_opened_in_guarded_trial |
| Phase 27.41 | Guarded Runtime Switch | ✅ completed_candidate_opened_in_guarded_trial |
| Phase 27.42 | Live UI Broader Probes | ✅ completed_live_ui_broader_probes_guarded |
| Phase 27.43 | Guarded Data-Backed Expansion | ✅ completed_partial_keep_phase27_40_runtime |
| Phase 27.44 | Tokenizer/Curriculum Repair | ✅ completed_partial_keep_phase27_40_runtime |
| Phase 27.45 | Semantic Topic Balance Repair | ✅ completed_partial_keep_phase27_40_runtime |
| Phase 27.46 | Core Dialogue Stabilization | ✅ completed_partial_keep_phase27_40_runtime |
| Phase 27.47 | New Topic Conditioning Repair | ✅ completed_ready_for_guarded_switch |
| Phase 27.48 | Guarded Runtime Switch for Phase 27.47 | ✅ completed_guarded_runtime_switch_phase27_47 |
| Phase 27.49 | Broader Live UI/API Probes | ✅ completed_broader_live_ui_probes_phase27_47 |
| Phase 27.50 | Generator-Only UI Lab Mode | ✅ completed_generator_only_ui_gate |
| Phase 27.51 | Open-Dialogue Generalization Audit | ✅ completed_failed_training_required |
| Phase 27.52 | Natural Dialogue Objective Repair | ✅ completed_partial_keep_phase27_47_runtime |
| Phase 27.53 | Natural Dialogue Diversity Expansion | ✅ completed_partial_keep_phase27_47_runtime |
| Phase 27.54 | Capacity/Objectivity Gate | ✅ completed_full_scaling_blocked_diagnostic_micro_probe_allowed |
| Phase 27.55 | Controlled SF-50M Diagnostic Micro-Probe | ✅ completed_diagnostic_capacity_signal_failed_full_sf50m_blocked |
| Phase 27.56 | Objective/Format/Tokenizer Diagnosis | ✅ completed_objective_format_tokenizer_diagnosis_runtime_blocked |
| Phase 27.57 | Tokenizer/Eval/Format Repair Pack | ✅ completed_repair_pack_ready_for_bounded_retraining_gate |
| Phase 27.58 | Tokenizer v7 Bounded Alignment Probe | ✅ failed_bounded_alignment_probe_runtime_blocked |
| Phase 27.59 | Bounded Alignment Repair | ✅ passed_bounded_alignment_repair_runtime_blocked |
| Phase 27.60 | Broader Natural-Dialogue Canary | ✅ failed_broader_natural_dialogue_canary_runtime_blocked |
| Phase 27.61 | Broader Generalization Repair | ✅ failed_broader_generalization_repair_runtime_blocked |
| Phase 27.62 | Family Balance Repair | ✅ failed_family_balance_repair_runtime_blocked |
| Phase 27.63 | Interleaved Family Curriculum | ✅ improved_interleaved_family_curriculum_runtime_blocked |
| Phase 27.64 | Topic Lexical/Tokenizer Inspection | ✅ completed_topic_lexical_inspection_tokenizer_v8_required_runtime_blocked |
| Phase 27.65 | Tokenizer v8 Topic Probe | ✅ passed_tokenizer_v8_topic_probe_ready_for_bounded_lm_topic_repair_runtime_blocked |
| Phase 27.66 | V8 Bounded Topic Repair | ✅ passed_v8_bounded_topic_repair_ready_for_fresh_shadow_canary_runtime_blocked |
| Phase 27.67 | Fresh Shadow Canary | ✅ failed_fresh_shadow_canary_runtime_blocked |
| Phase 27.68 | Shadow Failure Repair | ✅ passed_shadow_failure_repair_ready_for_new_fresh_shadow_runtime_blocked |
| Phase 27.69 | New Fresh Shadow Canary | ✅ strong_new_fresh_shadow_canary_runtime_blocked |
| Phase 27.70 | Open-Social Repair | ✅ failed_open_social_repair_runtime_blocked |
| Phase 27.71 | Candidate Selection and Stability Strategy | ✅ no_stable_candidate_runtime_blocked |
| Phase 27.72 | Stability-First Micro Repair | ✅ improved_stability_first_repair_runtime_blocked |
| Phase 27.73 | Open-Social Failure Inspection | ✅ completed_open_social_failure_inspection_runtime_blocked |
| Phase 27.74 | Open-Social Semantic-Collapse Repair | ✅ failed_open_social_semantic_collapse_repair_runtime_blocked |
| Phase 27.75 | Open-Social Strategy Inspection | ✅ completed_open_social_strategy_inspection_runtime_blocked |
| Phase 27.76 | Tokenizer v9 Open-Social Boundary Probe | ✅ passed_tokenizer_v9_open_social_boundary_probe_runtime_blocked |
| Phase 27.77 | V9 Bounded Open-Social LM Repair | ✅ failed_v9_bounded_open_social_lm_repair_runtime_blocked |
| Phase 27.78 | Engineering Root Cause Gate | ✅ phase27_78_engineering_decision_training_blocked |
| Phase 27.79 | Objective/Curriculum/Decoding Repair Plan | ✅ active_plan_training_blocked_until_gates |
| Phase 27.80 | Bounded Family-conditioned Repair Gate | ✅ gates_passed_bounded_training_allowed_next |
| Phase 27.81 | Execute Bounded SF-10M Family-conditioned Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.82 | Family-conditioned SF-10M Repair Training Decision | ✅ allows_phase27_83_bounded_training_no_runtime |
| Phase 27.83 | Family-conditioned SF-10M Bounded Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.84 | Objective/Curriculum Failure Diagnosis | ✅ diagnosed_family_signal_missing_no_training |
| Phase 27.85 | Explicit Family Conditioning Objective Design | ✅ renderer_gate_allowed_no_training |
| Phase 27.86 | Family Conditioning Renderer Gate | ✅ renderer_gate_passed_training_allowed_next_no_runtime |
| Phase 27.87 | Bounded Family-conditioned SF-10M Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.88 | Family-conditioned Training Result Diagnosis | ✅ diagnosed_sequential_curriculum_collapse_no_training |
| Phase 27.89 | Stratified Round-Robin Curriculum Sampler Gate | ✅ sampler_gate_passed_training_allowed_next_no_runtime |
| Phase 27.90 | Bounded SF-10M Round-Robin Curriculum Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.91 | Round-Robin Training Result Diagnosis | ✅ diagnosed_topic_collapse_no_training |
| Phase 27.92 | Topic Objective Repair Design Gate | ✅ topic_objective_repair_design_ready_no_training |
| Phase 27.93 | Topic Objective Gate Encoding and Dry-Run Validation | ✅ gate_passed_data_pack_required_no_training |
| Phase 27.94 | Topic Objective Data Pack Authoring | ✅ wafa_saudi_gap_closed_training_allowed_next_no_runtime |
| Phase 27.95 | Bounded Topic Objective Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.96 | Topic Objective Repair Result Diagnosis | ✅ diagnosed_topic_variable_binding_failure_no_training |
| Phase 27.97 | Topic Variable Binding Objective Design | ✅ topic_binding_objective_design_ready_no_training |
| Phase 27.98 | Topic Binding Gate Encoding and Metadata Audit | ✅ gate_encoded_data_repair_required_no_training |
| Phase 27.99 | Topic Metadata and Copy-Anchor Data Repair | ✅ metadata_copy_anchor_repaired_training_allowed_next |
| Phase 27.100 | Bounded Topic Binding Repair Training | ✅ trained_runtime_blocked_diagnosis_required |
| Phase 27.101 | Topic Binding Repair Result Diagnosis | ✅ diagnosed_metric_blind_spot_no_training |
| Phase 27.102 | Topic Prototype Contrastive Copy-Anchor Gate | ✅ gate_encoded_curriculum_pack_allowed_no_training |
| Phase 27.103 | Topic Prototype Contrastive Curriculum Pack | ✅ ready_for_bounded_training_no_runtime |
| Phase 27.104 | Bounded Topic Prototype Contrastive Repair Training | ✅ trained_topic_clean_all_family_regressed_runtime_blocked |
| Phase 27.105 | Raw UI Lab Result Diagnosis | ✅ diagnosed_raw_ui_lab_failures_no_training |
| Phase 27.106 | Social Subfamily + Topic Variant Objective Design | ✅ design_ready_gate_encoding_no_training |
| Phase 27.107 | Social Subfamily + Topic Variant Gate Encoding | ✅ gate_passed_data_pack_allowed_no_training |
| Phase 27.108 | Social Subfamily + Topic Variant Data Pack | ✅ data_pack_ready_for_audit_no_training |
| Phase 27.109 | Free Linguistic Resource Intake Gate | ✅ free_resource_intake_ready_no_training |
| Phase 27.110 | Licensed Ingestion Design | ✅ licensed_ingestion_design_ready_no_training |
| Phase 27.111 | Qabas Lexicon Bootstrap Design | ✅ qabas_bootstrap_design_ready_import_blocked |
| Phase 27.112 | Qabas Primary License Resolution Gate | ✅ qabas_reference_only_import_blocked |
| Phase 27.113 | Permissive Lexical Alternatives Intake Gate | ✅ permissive_lexical_alternatives_ready_no_import |
| Phase 27.114 | Arabic Ontology/Synonyms Source Cards | ✅ source_cards_ready_no_import |
| Phase 27.115 | Arabic Ontology/Synonyms Artifact Gate | ✅ artifact_gate_ready_no_import |
| Active Track | SF-native Objective/Curriculum/Decoding Acceleration Track | ✅ reanchored_at_phase27_79_no_training |

اقرأ التفاصيل في [PHASE_STATUS.md](./PHASE_STATUS.md) و [EXECUTION_PLAN.md](./EXECUTION_PLAN.md).

### الاختبارات

```
راجع `docs/PHASE_STATUS.md` لآخر رقم اختبارات موثق.
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
- `/ui/chat` مخصصة لاختبار الحوار فقط. لا تعرض أزرار حفظ/تصدير أو مهام جمع؛ الوكيل يتولى ذلك داخليًا عند الحاجة.
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

### Sovereign Practical Acceleration Strategy v2 — معتمدة رسميًا

التحول الحالي لا يغيّر السيادة؛ يغيّر طريقة الاختصار الهندسي. لا نعيد
اختراع الأدوات الرياضية والهندسية العامة من الصفر، ونستخدم ما يسرّع
التشخيص والتدريب بشرط ألا يدخل عقل خارجي إلى المشروع.

المسموح:

- PyTorch وstandard Transformer engineering.
- TensorBoard أو CSV/JSON logs محلية.
- schedulers وAMP/mixed precision.
- advanced decoding وrepetition controls.
- curriculum tooling وdialogue-family balancing وfamily-conditioned dialogue.
- held-out canary وshadow canary.
- contrastive evaluation.
- semantic routing diagnostics.
- objective tracing وanti-collapse diagnostics.
- local RLHF-lite / DPO / ORPO / preference optimization.
- LoRA / QLoRA على أوزان SF.AI فقط.
- retrieval memory tooling وlocal vector retrieval.
- EOS boundary tooling.
- experiment tracking وoptimization tooling محليًا.
- checkpoint selector وtokenizer boundary audit.

الممنوع:

- pretrained weights/embeddings.
- pretrained vocab أو tokenizer merges.
- external dialogue datasets.
- hidden hosted APIs أو external reasoning services.
- أي contamination من حوارات إدارة المشروع أو أوامر الوكيل داخل corpus الحوار العام.
- fake benchmark inflation.
- template masking لإخفاء ضعف المولد.

قبل أي تدريب جديد: القرار الحالي هو
`PHASE27_115_ARABIC_ONTOLOGY_SYNONYMS_ARTIFACT_GATE_DECISION`. مرّت بوابات
Phase 27.80: objective renderer, assistant-only loss mask,
stratified round-robin curriculum, guarded decoding, contrastive eval,
checkpoint selector, held-out canary, corpus-audit, sensitive scan,
full tests, وMPS/AMP smoke. Phase 27.81 نفذ التدريب المحدود ورفع all-family
إلى `42/50` مع topic family `10/10`. Phase 27.105 فتح raw UI lab للمستخدم
المحلي فقط وأثبت أن الردود من `sf_10m_phase27_81`، لكنه شخّص فشل
social subfamilies وtopic variants. Phase 27.106 أضاف design/renderer
لـ `dialogue_subfamily` وtopic canonical variants. Phase 27.107 مرّر gate
encoding وسمح فقط بـ Phase 27.108 data pack، بلا تدريب. Phase 27.108 كتب
`480` سجل gold جديدًا ومرّ corpus-audit على `9125/9125` سجلًا بلا مشاكل؛
Phase 27.109 اعتمد مسار المصادر المجانية: Masader metadata، Qabas،
Tashkeela. Phase 27.110 صمم license matrix: Qabas مسموح كـ
lexicon/topic/protected-terms فقط، وTashkeela محجوبة للتدريب حتى حل
تضارب الترخيص. Phase 27.111 صمم Qabas bootstrap لكنه حجب import الفعلي
بسبب تضارب ترخيص Qabas بين Masader (`Apache-1.0`) وSinaLab (`CC-BY-ND-4.0`).
Phase 27.112 حسم Qabas كـ reference-only بسبب `CC-BY-ND-4.0`. لا يدخل أي
نص خارجي أو مدخلات Qabas إلى corpus قبل gate لاحق صريح. Phase 27.113 صنف
Arabic Ontology وSinaLab Synonyms كمرشحين source-card/license-matrix فقط،
وحجب Arabic WordNet 4.0 لأنه model-derived عبر Gemini. Phase 27.114 أنشأ
source cards وlicense matrix للمرشحين دون import أو تدريب. Phase 27.115 حسم
artifact gate: Arabic Ontology محجوب لأنه request-only بلا artifact مباشر،
وSinaLab Synonyms مرصود كـ artifact candidate لكن import محجوب حتى quarantine
checksum/schema dry-run.
لا تعتمد loss/perplexity/micro-probe وحدها؛
القرار يعتمد على held-out dialogue quality, runtime usability, clean-stop,
semantic correctness, family stability, open_social naturalness, followup
continuity, canary pass rate, وhuman conversation realism.

### Auto-Advance Scaling Mandate — معتمد رسميًا

سامي فوّض الوكيل: إذا نجحت بوابة الحجم التالي، ينتقل الوكيل تلقائيًا إلى
الحجم التالي دون انتظار موافقة جديدة، حتى الوصول إلى `SF-1B+`.

السلم الرسمي:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

هذا التفويض مقيد:

- لا تكبير إذا لم ينجح `ENGINEERING_ROOT_CAUSE_GATE`.
- لا تكبير إذا كان السبب objective/curriculum/decoding/family mixing.
- لا runtime بدون `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- لا pretrained ولا vocab جاهز ولا datasets خارجية.
- لا قفز فوق حجم في السلم.

`M100` في كلام سامي يعني `SF-100M-class`; التنفيذ المسجل حاليًا هو
`SF-120M` ما لم يعتمد تقرير معماري لاحق `SF-100M`.

### Phase 11 — اكتملت كحوكمة

أُضيفت وثائق وأدوات فحص corpus:
- [CORPUS_GOVERNANCE.md](./CORPUS_GOVERNANCE.md)
- [DIALOGUE_DATASET_RUBRIC.md](./DIALOGUE_DATASET_RUBRIC.md)
- [data/corpus/chat/jsonl/README.md](../data/corpus/chat/jsonl/README.md)
- `sf_ai/datasets/corpus_governance.py`
- `tests/test_corpus_governance.py`

تدريب tokenizer v1 اكتمل في Phase 12. Smoke LM training اكتمل في Phase 13، وSF-10M v0.1 المحدود اكتمل في Phase 14، لكنه خام ومكرر وغير جاهز لاختبار سامي كمولد حواري. Phase 15 أضاف `NativeGenerator` و`GenerationPolicy` وmetadata يوضح هل الرد `template` أو `sf_10m_v0_1`، لكنه لم يجعل المولد مقنعًا. Phase 16 أضاف prompt suites وeval report، ثم فُتح مختبر سامي المحلي للقياس والتطوير. Phase 17–27.104 موثقة تاريخيًا، وآخر دليل مهم أن Phase 27.104 نجحت في topic gates (`16/16`, wrong-topic `0`, fresh `9/10`) لكنها فشلت all-family `30/50`. الوضع الحالي `9125` (`msa=4535`, `saudi=4590`, `gold=4013`, `silver=5112`). المسار الحالي أُعيد تثبيته عند Phase 27.79 عبر `PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN`، ومرّت بوابات Phase 27.80، ثم اكتمل Phase 27.81 عبر `PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION`: all-family `42/50`. Phase 27.105 شخّص raw UI lab: المولد الحقيقي يعمل في الواجهة، لكن social subfamilies وtopic variants ضعيفة. Phase 27.106 أضاف `dialogue_subfamily` وrenderer line `نوع السوالف` وtopic canonical mapping مثل `الصداقه → الصداقة` و`الاخوه → الأخوة`. Phase 27.107 مرّر gate التنفيذية. Phase 27.108 كتب data pack ذهبيًا 480 سجلًا. Phase 27.109 صنّف مصادر مجانية جاهزة وسحب Masader metadata summary فقط. Phase 27.110 صمم إدخالًا مرخصًا: Qabas للـ lexicon/topic فقط، وتدريب Tashkeela محجوب. Phase 27.111 حجب import Qabas الفعلي بسبب تضارب الترخيص. Phase 27.112 أبقى Qabas reference-only. Phase 27.113 صنف بدائل lexical permissive بلا import. Phase 27.114 أنشأ source cards/license matrix. Phase 27.115 حسم artifact gate وfield mapping دون import أو تدريب. لا official runtime ولا SF-50M ولا tokenizer retrain؛ التالي Phase 27.116 Synonyms quarantine checksum/schema dry-run.

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

تم تشغيل Phase 12 tokenizer v1 بإذن صريح من سامي على corpus صغير سابقًا. لا تعامل v1 كتشغيل لغوي متوازن؛ Phase 22 رفع corpus الحالي إلى 500 سجل (`msa=250`, `saudi=250`) ثم Phase 23 درّب tokenizer v2 في `artifacts/tokenizers/sf_bpe/v2/`.

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

- لا تعرض [apps/api/static/chat.html](../apps/api/static/chat.html) زر تصدير للمستخدم. أي review export يجب أن ينفذه الوكيل داخليًا إذا احتاجه.
- export يضع دائمًا `training_allowed=false`, `quality=needs_review`, `license=user-review-required`.
- [scripts/prepare_dialogue_batch.py](../scripts/prepare_dialogue_batch.py) يحول المراجعات إلى corpus تدريبي فقط عند تمرير `--training-allowed`.
- [sf_ai/datasets/dialogue_batch.py](../sf_ai/datasets/dialogue_batch.py) يفرض provenance/dialect/quality ويتخطى السجلات الحساسة افتراضيًا.
- التقرير الافتراضي: [artifacts/reports/dialogue_batch_report.json](../artifacts/reports/dialogue_batch_report.json).
- الوثيقة: [DATA_IMPROVEMENT_LOOP.md](./DATA_IMPROVEMENT_LOOP.md).

### Phase 19 — SF-50M Readiness Gate — تعمل

- `make phase19-readiness`
- `GET /system/phase19-readiness`
- القرار الحالي: `READY_FOR_SF50M_TRAINING` من زاوية Phase 19 القديمة فقط.
- تنبيه: Phase 26 هي البوابة الأحدث والأقوى، وما زالت تمنع `SF-50M` بسبب جودة runtime/canary لا بسبب corpus.
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
- التدريب الفعلي بدأ في Phase 13/14، وأول تدريب جودة مفيد اكتمل في Phase 24 مع منع runtime الواسع.
- أول فرصة لحوار قصير مولّد مقنع: بعد fixed split + gold social dialogue + canary أقوى على SF-10M، أو نجاح SF-50M لاحقًا.
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
- القرار الحالي: `READY_FOR_PHASE23_TOKENIZER_V2`
- الموجود: 500 سجلًا: 250 `msa` و250 `saudi`
- الهدف: 500 سجل، مع 200 على الأقل لكل من `msa` و`saudi`
- خطة الجمع الحالية: مكتملة، ولا توجد batches متبقية.
- المهمة الفورية الحالية: corpus gate اكتمل؛ انتقل إلى تحسين `SF-10M` وإعادة canary بدل إضافة دفعات جديدة عشوائيًا.
- الدفعات المرنة المكتملة: `data/corpus/chat/jsonl/dialogue_batch_v2_flex_001.jsonl` إلى `dialogue_batch_v2_flex_004.jsonl` بإجمالي 100 سجل.
- أضيفت ثمان دفعات فصيحة معتمدة: `data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl` مع بطاقات provenance.
- أضيف seed مصطلحات فصحى تدريبي: `data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl` وفيه 22 سجلًا `gold`; هذا corpus فعلي، وليس موردًا مرشحًا.
- بنك التأليف الفصيح: `resources/phase22_authoring/msa_prompt_bank_v1.json`، ملف مساعدة فقط وليس corpus، وحقوله `training_allowed=false` و`synthetic_llm_data=false`.
- مصطلحات الفصحى المرشحة: `resources/tokenization/protected_terms_msa_candidate.txt` و`resources/tokenization/preferred_merges_msa_candidate.txt`. هذه موارد سياسة غير نشطة، ليست corpus ولا vocab pretrained، وتُستخدم لتوجيه دفعات الفصحى القادمة قبل تفعيلها في tokenizer.
- حفظ review المحلي: `POST /chat/review-export` باقٍ كأداة داخلية تكتب إلى `data/corpus/chat/review/` فقط مع `training_allowed=false`، لكنه غير ظاهر في `/ui/chat`.
- كل export/training record يحمل الآن user ownership:
  `owner_user_id`, `created_by_user_id`, `target_user_id`, `user_scope`.
- المسار الحالي `single_user` بمعرف `sami-local` حتى لا تختلط محادثات المستخدمين عند التوسع لاحقًا.
- بروتوكول سامي الجديد: الوكيل هو من يختبر الواجهة/API ويؤلف ويراجع ويعتمد دفعات corpus ويرتّب الملفات والتقارير. لا تطلب من سامي خطوات حفظ/تصدير/اعتماد يدوية إذا كنت تستطيع تنفيذها. سامي يستلم النتيجة النهائية ويقرر الاقتناع فقط.
- review intake الحالي: `data/corpus/chat/review/sample_review_export.jsonl` مرشح للمراجعة فقط؛ لا يدخل التدريب تلقائيًا.
- `phase22-review-intake` يعرض أيضًا `quality_score`, `quality_label`, و`quality_blockers`; لا تعتبر جلسة قوية للتدريب إلا إذا كانت متعددة الأدوار غالبًا 3 user + 3 assistant على الأقل.
- `/ui/chat` لم يعد يعرض مؤشر جودة التصدير. قياس جودة أي review export مسؤولية أدوات الوكيل الداخلية.
- الواجهة الحالية بعد Phase 27.50 تعمل كمختبر مولّد فقط: لا تعرض template في `/chat/message`. إذا ظهر `template` في الواجهة فهذا regression يجب إصلاحه فورًا.
- أي export يحتوي ردود `sf_10m_v0_1/sf_10m_v0_2/sf_10m_phase27_33` يجب أن يبقى review evidence فقط، و`phase22-review-intake` يميّزه ولا يعدّه candidate تدريب جودة.
- الممنوع: synthetic LLM data من مصدر خارجي أو مجهول.
- حوار الوكيل المؤلف بتفويض سامي يمكن أن يدخل corpus مباشرة إذا وُسم كـ `owner-delegated agent-authored` مع source/license/quality/notes كاملة، وبقي ضمن `msa + saudi`، ودون أي pretrained أو dataset خارجي.

### تستطيع الآن العمل على:

- لا تفتح Phase 28 الآن. ابدأ بإصلاح fixed split وgold social dialogue وcanary، ثم أعد `make phase26-readiness`.

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
8. **Sovereign Practical Acceleration Strategy v2** معتمدة: استخدم أدوات
   هندسية عامة لتقليل الوقت، لكن لا تستخدم pretrained أو datasets خارجية
   أو hosted reasoning، ولا تبدأ تدريبًا قبل `ENGINEERING_ROOT_CAUSE_GATE`.

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
tests/                          راجع `docs/PHASE_STATUS.md` لآخر رقم موثق
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
