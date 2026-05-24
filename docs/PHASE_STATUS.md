# PHASE_STATUS.md

## SF.AI — سجل حالة المراحل

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الرحلة الحالية:** **Phase 27.112 / 30**
- **المرحلة الحالية:** **Phase 27.112 — Qabas Primary License Resolution Gate**
- **حالة المرحلة الحالية:** **حُسم Qabas كـ reference-only؛ لا import فعلي بسبب ترخيص CC-BY-ND-4.0 وتضارب Masader؛ لا تدريب الآن**
- **المرحلة التالية المقترحة:** Phase 27.113 — Permissive Lexical Alternatives Intake Gate, no training.
- **التحول الاستراتيجي المعتمد:** **SF-native Objective/Curriculum/Decoding Acceleration Track** — تسريع هندسي فقط؛ `ENGINEERING_ROOT_CAUSE_GATE` قبل أي تدريب؛ `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- **تصحيح إلزامي:** لا يوجد Open-Weight Lane. أي Qwen/open-weight/pretrained
  runtime ملغى وغير معتمد. التسريع السيادي يعني أدوات هندسية وتشخيصية فقط
  ضمن مسار `SF-native`.
- **تفويض التكبير المعتمد:** **Auto-Advance Scaling Mandate** — عند نجاح gate الحجم التالي ينتقل الوكيل تلقائيًا عبر `SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+`.
- **القاموس/المسار اللغوي الحالي:** `msa + saudi` فقط؛ القاموس المتبع `Saudi Seed v1` مع `safety_terms.yaml`.
- **تاريخ آخر تحديث:** 2026-05-25

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
| Strategy Overlay | Sovereign Practical Acceleration Strategy v2 | ✅ adopted_engineering_root_cause_gate_required | ✅ |
| Scaling Mandate | Auto-Advance Scaling Mandate | ✅ adopted_gate_bound_auto_advance_to_1b | ✅ |
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
| Phase 27.16 | Prompt-to-Answer Objective Repair | ✅ completed_objective_repair_runtime_blocked | ✅ |
| Phase 27.17 | Prompt-to-Answer Micro-Probe | ✅ completed_micro_probe_breakthrough_runtime_blocked | ✅ |
| Phase 27.18 | Tokenization/Decoding Hygiene Repair | ✅ completed_hygiene_audit_with_blockers | ✅ |
| Phase 27.19 | Hygiene Repair Corpus/Probe | ✅ completed_repair_probe_still_runtime_blocked | ✅ |
| Phase 27.20 | Tokenizer/Protected-Phrase Strategy | ✅ completed_ready_for_tokenizer_v3_runtime_blocked | ✅ |
| Phase 27.21 | Tokenizer v3 Protected-Phrase Micro-Probe | ✅ completed_micro_probe_failed_runtime_blocked | ✅ |
| Phase 27.22 | Spacing/Boundary Loss Repair | ✅ completed_partial_repair_runtime_blocked | ✅ |
| Phase 27.23 | Semantic/Lexical Confusion Repair | ✅ completed_partial_repair_runtime_blocked | ✅ |
| Phase 27.24 | Minimal Lexical Stabilization | ✅ completed_micro_probe_passed_runtime_blocked | ✅ |
| Phase 27.25 | Held-out Generation Quality Canary | ✅ completed_heldout_canary_failed_runtime_blocked | ✅ |
| Phase 27.26 | Held-out Objective Repair | ✅ completed_partial_runtime_blocked | ✅ |
| Phase 27.27 | Broader Held-out Repair | ✅ completed_old_heldout_passed_shadow_blocked | ✅ |
| Phase 27.28 | Intent-Conditioned Repair | ✅ completed_intent_conditioning_partial_runtime_blocked | ✅ |
| Phase 27.29 | Topic-Conditioned Definition Repair | ✅ completed_topic_conditioning_leakage_blocked | ✅ |
| Phase 27.30 | Fresh Mixed Shadow Canary | ✅ completed_16_of_18_runtime_blocked | ✅ |
| Phase 27.31 | Natural Intent/Topic Dataset | ✅ completed_partial_runtime_blocked | ✅ |
| Phase 27.32 | Balanced Natural Calibration | ✅ completed_partial_runtime_blocked | ✅ |
| Phase 27.33 | Advice + Micro Stabilization | ✅ completed_all_generation_gates_passed_trial_design_ready | ✅ |
| Phase 27.34 | Guarded Runtime Trial | ✅ completed_ready_for_ui_test | ✅ |
| Phase 27.35 | Live UI Trial Observations | ✅ completed_ready_for_user_observation | ✅ |
| Phase 27.36 | Live UI Triage | ✅ completed_quality_floor_active | ✅ |
| Phase 27.37 | Supported Topic Expansion | ✅ completed_quality_gated | ✅ |
| Phase 27.38 | Targeted Topic Curriculum/Probe | ✅ completed_partial_keep_current_runtime | ✅ |
| Phase 27.39 | Topic-Isolation Repair | ✅ completed_partial_keep_current_runtime | ✅ |
| Phase 27.40 | Tokenizer/Context Repair | ✅ completed_candidate_opened_in_guarded_trial | ✅ |
| Phase 27.41 | Guarded Runtime Switch | ✅ completed_candidate_opened_in_guarded_trial | ✅ |
| Phase 27.42 | Live UI Broader Probes | ✅ completed_live_ui_broader_probes_guarded | ✅ |
| Phase 27.43 | Guarded Data-Backed Expansion | ✅ completed_partial_keep_phase27_40_runtime | ✅ |
| Phase 27.44 | Tokenizer/Curriculum Repair | ✅ completed_partial_keep_phase27_40_runtime | ✅ |
| Phase 27.45 | Semantic Topic Balance Repair | ✅ completed_partial_keep_phase27_40_runtime | ✅ |
| Phase 27.46 | Core Dialogue Stabilization | ✅ completed_partial_keep_phase27_40_runtime | ✅ |
| Phase 27.47 | New Topic Conditioning Repair | ✅ completed_ready_for_guarded_switch | ✅ |
| Phase 27.48 | Guarded Runtime Switch for Phase 27.47 | ✅ completed_guarded_runtime_switch_phase27_47 | ✅ |
| Phase 27.49 | Broader Live UI/API Probes | ✅ completed_broader_live_ui_probes_phase27_47 | ✅ |
| Phase 27.50 | Generator-Only UI Lab Mode | ✅ completed_generator_only_ui_gate | ✅ |
| Phase 27.51 | Open-Dialogue Generalization Audit | ✅ completed_failed_training_required | ✅ |
| Phase 27.52 | Natural Dialogue Objective Repair | ✅ completed_partial_keep_phase27_47_runtime | ✅ |
| Phase 27.53 | Natural Dialogue Diversity Expansion | ✅ completed_partial_keep_phase27_47_runtime | ✅ |
| Phase 27.54 | Capacity/Objectivity Gate | ✅ completed_full_scaling_blocked_diagnostic_micro_probe_allowed | ✅ |
| Phase 27.55 | Controlled SF-50M Diagnostic Micro-Probe | ✅ completed_diagnostic_capacity_signal_failed_full_sf50m_blocked | ✅ |
| Phase 27.56 | Objective/Format/Tokenizer Diagnosis | ✅ completed_objective_format_tokenizer_diagnosis_runtime_blocked | ✅ |
| Phase 27.57 | Tokenizer/Eval/Format Repair Pack | ✅ completed_repair_pack_ready_for_bounded_retraining_gate | ✅ |
| Phase 27.58 | Tokenizer v7 Bounded Alignment Probe | ✅ failed_bounded_alignment_probe_runtime_blocked | ✅ |
| Phase 27.59 | Bounded Alignment Repair | ✅ passed_bounded_alignment_repair_runtime_blocked | ✅ |
| Phase 27.60 | Broader Natural-Dialogue Canary | ✅ failed_broader_natural_dialogue_canary_runtime_blocked | ✅ |
| Phase 27.61 | Broader Generalization Repair | ✅ failed_broader_generalization_repair_runtime_blocked | ✅ |
| Phase 27.62 | Family Balance Repair | ✅ failed_family_balance_repair_runtime_blocked | ✅ |
| Phase 27.63 | Interleaved Family Curriculum | ✅ improved_interleaved_family_curriculum_runtime_blocked | ✅ |
| Phase 27.64 | Topic Lexical/Tokenizer Inspection | ✅ completed_topic_lexical_inspection_tokenizer_v8_required_runtime_blocked | ✅ |
| Phase 27.65 | Tokenizer v8 Topic Probe | ✅ passed_tokenizer_v8_topic_probe_ready_for_bounded_lm_topic_repair_runtime_blocked | ✅ |
| Phase 27.66 | V8 Bounded Topic Repair | ✅ passed_v8_bounded_topic_repair_ready_for_fresh_shadow_canary_runtime_blocked | ✅ |
| Phase 27.67 | Fresh Shadow Canary | ✅ failed_fresh_shadow_canary_runtime_blocked | ✅ |
| Phase 27.68 | Shadow Failure Repair | ✅ passed_shadow_failure_repair_ready_for_new_fresh_shadow_runtime_blocked | ✅ |
| Phase 27.69 | New Fresh Shadow Canary | ✅ strong_new_fresh_shadow_canary_runtime_blocked | ✅ |
| Phase 27.70 | Open-Social Repair | ✅ failed_open_social_repair_runtime_blocked | ✅ |
| Phase 27.71 | Candidate Selection and Stability Strategy | ✅ no_stable_candidate_runtime_blocked | ✅ |
| Phase 27.72 | Stability-First Micro Repair | ✅ improved_stability_first_repair_runtime_blocked | ✅ |
| Phase 27.73 | Open-Social Failure Inspection | ✅ completed_open_social_failure_inspection_runtime_blocked | ✅ |
| Phase 27.74 | Open-Social Semantic-Collapse Repair | ✅ failed_open_social_semantic_collapse_repair_runtime_blocked | ✅ |
| Phase 27.75 | Open-Social Strategy Inspection | ✅ completed_open_social_strategy_inspection_runtime_blocked | ✅ |
| Phase 27.76 | Tokenizer v9 Open-Social Boundary Probe | ✅ passed_tokenizer_v9_open_social_boundary_probe_runtime_blocked | ✅ |
| Phase 27.77 | V9 Bounded Open-Social LM Repair | ✅ failed_v9_bounded_open_social_lm_repair_runtime_blocked | ✅ |
| Phase 27.78 | Engineering Root Cause Gate | ✅ phase27_78_engineering_decision_training_blocked | ✅ |
| Phase 27.79 | Objective/Curriculum/Decoding Repair Plan | ✅ active_plan_training_blocked_until_gates | ✅ |
| Phase 27.80 | Bounded Family-conditioned Repair Gate | ✅ gates_passed_bounded_training_allowed_next | ✅ |
| Phase 27.81 | Execute Bounded SF-10M Family-conditioned Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.82 | Family-conditioned SF-10M Repair Training Decision | ✅ allows_phase27_83_bounded_training_no_runtime | ✅ |
| Phase 27.83 | Family-conditioned SF-10M Bounded Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.84 | Objective/Curriculum Failure Diagnosis | ✅ diagnosed_family_signal_missing_no_training | ✅ |
| Phase 27.85 | Explicit Family Conditioning Objective Design | ✅ renderer_gate_allowed_no_training | ✅ |
| Phase 27.86 | Family Conditioning Renderer Gate | ✅ renderer_gate_passed_training_allowed_next_no_runtime | ✅ |
| Phase 27.87 | Bounded Family-conditioned SF-10M Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.88 | Family-conditioned Training Result Diagnosis | ✅ diagnosed_sequential_curriculum_collapse_no_training | ✅ |
| Phase 27.89 | Stratified Round-Robin Curriculum Sampler Gate | ✅ sampler_gate_passed_training_allowed_next_no_runtime | ✅ |
| Phase 27.90 | Bounded SF-10M Round-Robin Curriculum Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.91 | Round-Robin Training Result Diagnosis | ✅ diagnosed_topic_collapse_no_training | ✅ |
| Phase 27.92 | Topic Objective Repair Design Gate | ✅ topic_objective_repair_design_ready_no_training | ✅ |
| Phase 27.93 | Topic Objective Gate Encoding and Dry-Run Validation | ✅ gate_passed_data_pack_required_no_training | ✅ |
| Phase 27.94 | Topic Objective Data Pack Authoring | ✅ wafa_saudi_gap_closed_training_allowed_next_no_runtime | ✅ |
| Phase 27.95 | Bounded Topic Objective Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.96 | Topic Objective Repair Result Diagnosis | ✅ diagnosed_topic_variable_binding_failure_no_training | ✅ |
| Phase 27.97 | Topic Variable Binding Objective Design | ✅ topic_binding_objective_design_ready_no_training | ✅ |
| Phase 27.98 | Topic Binding Gate Encoding and Metadata Audit | ✅ gate_encoded_data_repair_required_no_training | ✅ |
| Phase 27.99 | Topic Metadata and Copy-Anchor Data Repair | ✅ metadata_copy_anchor_repaired_training_allowed_next | ✅ |
| Phase 27.100 | Bounded Topic Binding Repair Training | ✅ trained_runtime_blocked_diagnosis_required | ✅ |
| Phase 27.101 | Topic Binding Repair Result Diagnosis | ✅ diagnosed_metric_blind_spot_no_training | ✅ |
| Phase 27.102 | Topic Prototype Contrastive Copy-Anchor Gate | ✅ gate_encoded_curriculum_pack_allowed_no_training | ✅ |
| Phase 27.103 | Topic Prototype Contrastive Curriculum Pack | ✅ ready_for_bounded_training_no_runtime | ✅ |
| Phase 27.104 | Bounded Topic Prototype Contrastive Repair Training | ✅ trained_topic_clean_all_family_regressed_runtime_blocked | ✅ |
| Phase 27.105 | Raw UI Lab Result Diagnosis | ✅ diagnosed_raw_ui_lab_failures_no_training | ✅ |
| Phase 27.106 | Social Subfamily + Topic Variant Objective Design | ✅ design_ready_gate_encoding_no_training | ✅ |
| Phase 27.107 | Social Subfamily + Topic Variant Gate Encoding | ✅ gate_passed_data_pack_allowed_no_training | ✅ |
| Phase 27.108 | Social Subfamily + Topic Variant Data Pack | ✅ data_pack_ready_for_audit_no_training | ✅ |
| Phase 27.109 | Free Linguistic Resource Intake Gate | ✅ free_resource_intake_ready_no_training | ✅ |
| Phase 27.110 | Licensed Ingestion Design | ✅ licensed_ingestion_design_ready_no_training | ✅ |
| Phase 27.111 | Qabas Lexicon Bootstrap Design | ✅ qabas_bootstrap_design_ready_import_blocked | ✅ |
| Phase 27.112 | Qabas Primary License Resolution Gate | ✅ qabas_reference_only_import_blocked | ✅ |
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
  - السلم الرسمي صار: `SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+`.
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
  - القاعدة العملية الجديدة: ملف التصدير المفيد يجب أن يحتوي غالبًا 3 أدوار مستخدم + 3 ردود مساعد على الأقل، وبدون ردود raw من `sf_10m_v0_1/sf_10m_v0_2/sf_10m_phase27_33`.
  - القاعدة العملية الأحدث: الوكيل يستطيع تأليف/مراجعة/اعتماد دفعات Phase 22 مباشرة كـ `owner-delegated agent-authored` بدون انتظار حفظ أو تصدير من سامي، بشرط اكتمال `source/license/quality/training_allowed/user_scope/notes` ونجاح الاختبارات.
  - صححت تشغيل الواجهة المستقرة: `generator=template` افتراضيًا، أي قوالب ثابتة لا مولد؛ و`SF-10M` الخام يبقى مختبرًا صريحًا فقط.
  - أضيفت حماية export/review intake لتمييز أي جلسة تحتوي ردود `sf_10m_v0_1/sf_10m_v0_2/sf_10m_phase27_33` ومنع عدّها كـ candidate تدريب جودة.
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
- بدأ وانتهى Phase 27.16 Prompt-to-Answer Objective Repair:
  - أضيف `--packing-mode packed|sample_isolated` إلى `train_tiny_lm` و`evaluate_tiny_lm`.
  - `sample_isolated` يمنع أن تعبر نافذة التدريب من عينة حوارية إلى عينة أخرى.
  - دُرّب `SF-10M v0.11` 6000 خطوة باستخدام `assistant` loss و`sample_isolated`.
  - أفضل eval: `sf-10m-step6000`, loss `4.0573`, perplexity `57.82`.
  - المقارنة: `v0.11` أسوأ رقميًا من `v0.10` رغم نظافة العزل.
  - canary: `step2000=2/10`, `step6000=0/10`, و`runtime_allowed=false`.
  - القرار: `COMPLETED_OBJECTIVE_REPAIR_RUNTIME_BLOCKED`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md](./PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md).
  - أضيف `artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json`.
- بدأ وانتهى Phase 27.17 Prompt-to-Answer Micro-Probe:
  - أضيف `scripts/phase27_17_prompt_answer_micro_probe.py`.
  - أضيف `make phase27-prompt-answer-probe`.
  - شُغّل probe داخلي على `32` زوج سؤال/جواب (`msa=16`, `saudi=16`) داخل `artifacts/eval`.
  - التدريب: `SF-10M`, `steps=2400`, `loss_scope=assistant`, `packing_mode=sample_isolated`.
  - النتيجة: `passed=27/32`, `exact_clean=28/32`, `semantic_match=29/32`, `guard_passed=29/32`.
  - الفشل المتبقي: كسور لفظية/حروفية مثل `وعليكأهلًا`, `التعاعاون`, `هوش تحتاجججبعيادة`.
  - القرار: `FAILED_PROMPT_ANSWER_MICRO_PROBE_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md](./PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md).
  - أضيف `artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json`.
- بدأ وانتهى Phase 27.18 Tokenization/Decoding Hygiene Repair:
  - أضيف `resources/tokenization/hygiene_terms_phase27_18.txt`.
  - أضيف `scripts/phase27_18_hygiene_audit.py`.
  - أضيف `make phase27-hygiene-audit`.
  - أضيفت كسور Phase 27.17 إلى `GenerationGuard`.
  - نتيجة audit: `terms_total=26`, `average_pieces=3.5385`, `roundtrip_failures=0`.
  - `aggressive_split_terms=5`: `وعليكم السلام`, `نفسًا هادئًا`, `نشتغل سوا`, `القراءة تفيد`, `تقدّر الناس`.
  - `uncovered_bad_fragments=0`: كل الكسور المرصودة أصبحت محجوبة.
  - القرار: `COMPLETED_HYGIENE_AUDIT_WITH_BLOCKERS`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md](./PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md).
  - أضيف `artifacts/reports/phase27_18_tokenization_hygiene_report.json`.
- بدأ وانتهى Phase 27.19 Hygiene Repair Corpus/Probe:
  - أضيف `scripts/phase27_19_hygiene_repair_probe.py`.
  - أضيف `make phase27-hygiene-repair-probe`.
  - شُغّل repair probe داخلي على `52` مثالًا (`32` أساس + `20` repair).
  - التدريب: `SF-10M`, `steps=3200`, `loss_scope=assistant`, `packing_mode=sample_isolated`.
  - النتيجة بقيت: `passed=27/32`, `exact_clean=28/32`, `semantic_match=28/32`, `guard_passed=29/32`.
  - التشخيص: أمثلة repair وحدها لا تكفي؛ نحتاج استراتيجية tokenizer/protected-phrase.
  - القرار: `FAILED_HYGIENE_REPAIR_PROBE_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md](./PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md).
  - أضيف `artifacts/reports/phase27_19_hygiene_repair_probe_report.json`.
- بدأ وانتهى Phase 27.20 Tokenizer/Protected-Phrase Strategy:
  - أضيف دعم `protected_terms` داخل `TokenizerConfig` و`BPETokenizer`.
  - أضيف حفظ `protected_terms/protected_joiner` داخل `meta.json`.
  - أضيف `resources/tokenization/protected_phrases_phase27_20.txt`.
  - أضيف `scripts/phase27_20_tokenizer_strategy.py`.
  - أضيف `make phase27-tokenizer-strategy`.
  - العبارات الخمس: `وعليكم السلام`, `نفسًا هادئًا`, `نشتغل سوا`, `القراءة تفيد`, `تقدّر الناس`.
  - tokenizer v2 الحالي: `max_pieces=8`.
  - استراتيجية protected phrase الجديدة: `max_pieces=1`, `all_single_piece=true`, `all_roundtrip_ok=true`.
  - القرار: `COMPLETED_PROTECTED_PHRASE_STRATEGY_READY_FOR_TOKENIZER_V3`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md](./PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md).
  - أضيف `artifacts/reports/phase27_20_tokenizer_strategy_report.json`.
- بدأ وانتهى Phase 27.21 Tokenizer v3 Protected-Phrase Micro-Probe:
  - دُرّب tokenizer v3 سيادي في `artifacts/tokenizers/sf_bpe/v3`.
  - `vocab_size=4706`, `merges=4648`, `sf_origin=true`.
  - protected phrases بقيت `max_pieces=1` و`all_roundtrip_ok=true`.
  - دُرّب probe داخلي `SF-10M` على tokenizer v3: `steps=3200`, `packing_mode=sample_isolated`.
  - النتيجة: `passed=25/32`, `exact_clean=26/32`, `semantic=30/32`, `guard_passed=31/32`.
  - أسباب الفشل: `not_exact_clean=4`, `missing_semantic_terms=2`, `guard:model_artifact_fragment=1`.
  - التشخيص: المشكلة انتقلت إلى لصق spacing/boundary مثل `سواونخفف`, `تفيدوتوسع`, `هادئًاوابدأ`.
  - القرار: `FAILED_TOKENIZER_V3_MICRO_PROBE_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md](./PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md).
  - أضيف `artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json`.
- بدأ وانتهى Phase 27.22 Spacing/Boundary Loss Repair:
  - أصلح `BPETokenizer.decode` لإضافة word boundary بعد protected phrase token.
  - أصلح `GenerationGuard` حتى لا يحجب tanween صحيح مثل `وقتًا`.
  - أعيد تقييم checkpoint Phase 27.21 نفسه دون تدريب جديد.
  - النتيجة تحسنت من `25/32` إلى `29/32`.
  - `exact_clean=29/32`, `semantic=30/32`, `guard_passed=32/32`.
  - اختفت كل markers الملتحمة: `سواونخفف`, `تفيدوتوسع`, `هادئًاوابدأ`.
  - بقيت 3 إخفاقات: تعاون فصيح، احترام، وقراءة سعودي.
  - القرار: `PARTIAL_SPACING_BOUNDARY_REPAIR_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md](./PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md).
  - أضيف `artifacts/reports/phase27_22_spacing_boundary_repair_report.json`.
- بدأ وانتهى Phase 27.23 Semantic/Lexical Confusion Repair:
  - جُرّبت محاولة tokenizer v4 أوسع ورُفضت لأنها سببت answer collapse (`8/32`).
  - اعتُمد tokenizer v3 مع تدريب repair متوازن: قاعدة 32 مكررة + أمثلة contrastive محدودة.
  - النتيجة تحسنت من `29/32` إلى `30/32`.
  - `exact_clean=30/32`, `semantic=30/32`, `guard_passed=31/32`.
  - بقي خللان lexical: `التعاون` و`الاحترام`.
  - القرار: `PARTIAL_SEMANTIC_LEXICAL_REPAIR_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - أضيف [PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md](./PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md).
  - أضيف `artifacts/reports/phase27_23_semantic_lexical_repair_report.json`.
- بدأ وانتهى Phase 27.24 Minimal Lexical Stabilization:
  - أضيف tokenizer محدود `artifacts/tokenizers/sf_bpe/v4_min_lexical`.
  - protected terms الحالية: عبارات Phase 27.20 الخمس + `التعاون` + `الاحترام`.
  - دُرّب micro-probe داخلي متوازن `5600` خطوة.
  - النتيجة وصلت إلى `passed=32/32`, `exact_clean=32/32`, `semantic=32/32`, `guard_passed=32/32`.
  - القرار: `PASSED_MINIMAL_LEXICAL_STABILIZATION_HOLD_RUNTIME_FOR_CANARY`.
  - لا تفعيل runtime ولا تدريب `SF-50M` حتى held-out canary أوسع.
  - أضيف [PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md](./PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md).
  - أضيف `artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json`.
- بدأ وانتهى Phase 27.25 Held-out Generation Quality Canary:
  - لم يدرّب نموذجًا جديدًا؛ اختبر checkpoint Phase 27.24 على `16` prompt جديدًا.
  - النتيجة: `passed=8/16`, `semantic=8/16`, `guard_passed=15/16`.
  - نجحت التعريفات القريبة، وفشلت التحية الفصيحة والنصيحة والتخطيط والدعم.
  - القرار: `FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - التالي Phase 27.26 held-out objective repair and generalization training.
  - أضيف [PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md](./PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md).
  - أضيف `artifacts/reports/phase27_25_heldout_generation_canary_report.json`.
- بدأ وانتهى Phase 27.26–27.30 Repair Series:
  - Phase 27.26: held-out تحسن إلى `9/16`, micro-probe بقي `32/32`.
  - Phase 27.27: held-out القديم صار `16/16`, لكن shadow بقي `9/16`.
  - Phase 27.28: intent conditioning رفع shadow إلى `12/16`.
  - Phase 27.29: topic conditioning أصلح التعريفات لكنه حُجب بسبب `shadow_prompt_leakage`.
  - Phase 27.30: fresh mixed shadow بلا تدريب أعطى `16/18`.
  - الفشل المتبقي: الشكر الفصيح `شكرًا لمساعدتك` وسؤال الحال السعودي `كيفك اليوم`.
  - القرار: `FAILED_FRESH_MIXED_SHADOW_BLOCK_RUNTIME`.
  - لا تفعيل runtime ولا تدريب `SF-50M`.
  - التالي Phase 27.31 broader natural intent/topic dataset.
  - أضيف [PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md](./PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md).
- بدأ وانتهى Phase 27.31–27.33 Natural Generation Gate Series:
  - Phase 27.31: natural intent/topic dataset؛ natural shadow `20/20` وmicro `32/32`، لكن fresh mixed `15/18`.
  - Phase 27.32: balanced natural calibration؛ definition `6/6` وcalibration `12/12`، لكن fresh mixed `16/18` وmicro `29/32`.
  - Phase 27.33: advice + micro stabilization؛ heldout `16/16`, shadow `16/16`, definition `6/6`, fresh mixed `18/18`, natural shadow `20/20`, calibration `12/12`, advice `4/4`, micro `32/32`.
  - prompt leakage: none.
  - القرار: `PASSED_ADVICE_MICRO_STABILIZATION_READY_FOR_GUARDED_TRIAL_DESIGN`.
  - لا تفعيل افتراضي للواجهة بعد؛ التالي Phase 27.34 guarded runtime trial design.
  - أضيف [PHASE27_31_TO_33_GENERATION_GATE_REPORT.md](./PHASE27_31_TO_33_GENERATION_GATE_REPORT.md).
- بدأ وانتهى Phase 27.34 Guarded Runtime Trial:
  - أضيف حقل `generator_trial=true` إلى `/chat/message`.
  - أضيف زر `مولّد تجريبي` في `/ui/chat`.
  - مسار التجربة يستخدم `sf_10m_phase27_33` مع `GenerationGuard` وfallback للقالب.
  - بوابة runtime المحروس مرّت `9/9`: سبعة prompts مولدة + تحكمان template/safety.
  - القرار: `PASSED_GUARDED_RUNTIME_TRIAL_READY_FOR_UI_TEST`.
  - التالي Phase 27.35 live UI trial observations.
  - أضيف [PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md](./PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md).
- بدأ وانتهى Phase 27.35 Live UI Trial Observations:
  - فُحص `/ui/chat` حيًا وتأكد وجود زر `مولّد تجريبي` وإرسال `generator_trial`.
  - فُحص `/chat/message` حيًا: `10/10` passed.
  - ردود المولّد: `7/7` عبر `sf_10m_phase27_33`.
  - تحكم template/safety: `3/3`.
  - القرار: `PASSED_LIVE_UI_TRIAL_READY_FOR_USER_OBSERVATION`.
  - التالي Phase 27.36 collect/triage live UI observations.
  - أضيف [PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md](./PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md).
- بدأ وانتهى Phase 27.36 Live UI Triage:
  - أضيف quality-floor للتجربة الحية: raw `chat.general` وموضوعات التعريف غير المثبتة لا تذهب للمولّد.
  - فُحص `/chat/message` حيًا: `27/27` passed.
  - ردود المولّد المثبتة: `18/18`.
  - quality-floor blocks: `5/5`.
  - تحكم template/safety: `4/4`.
  - القرار: `PASSED_LIVE_UI_TRIAGE_QUALITY_FLOOR_ACTIVE`.
  - التالي Phase 27.37 expand supported generator intents/topics.
  - أضيف [PHASE27_36_LIVE_UI_TRIAGE_REPORT.md](./PHASE27_36_LIVE_UI_TRIAGE_REPORT.md).
- بدأ وانتهى Phase 27.37 Supported Topic Expansion:
  - أضيف semantic topic guard بعد التوليد.
  - فُتح موضوع `الصبر` بصيغ مثبتة فقط.
  - فُحص `/chat/message` حيًا: `21/21` passed.
  - regression generated: `10/10`.
  - new topic: `3/3`.
  - quality-floor blocks: `5/5`.
  - تحكم template/safety: `3/3`.
  - القرار: `PASSED_SUPPORTED_TOPIC_EXPANSION_QUALITY_GATED`.
  - التالي Phase 27.38 targeted topic curriculum/probe للموضوعات المحجوبة.
  - أضيف [PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md](./PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md).
- بدأ وانتهى Phase 27.38 Targeted Topic Curriculum/Probe:
  - دُرّب checkpoint مستهدف: `sf-10m-step2400`.
  - الاختبار: `6/20` فقط.
  - regression: `6/8`.
  - new_topic: `0/8`.
  - heldout: `0/4`.
  - التشخيص: topic collapse نحو `الاحترام`، وخسارة `التعاون` و`الصبر` في المرشح.
  - القرار: `runtime_switch_allowed=false`; يبقى runtime التجريبي على مرشح Phase 27.33 + فتح `الصبر` المحروس من 27.37.
  - التالي Phase 27.39 repair failed targeted topics.
  - أضيف [PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md](./PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md).
- بدأ وانتهى Phase 27.39 Topic-Isolation Repair:
  - دُرّب checkpoint مستهدف: `sf-10m-step6400`.
  - الاختبار: `10/24` بعد تصحيح القياس.
  - regression: `4/8`.
  - new_topic: `2/8`.
  - heldout: `1/4`.
  - isolation: `3/4`.
  - التشخيص: topic collapse تحسن جزئيًا، لكن بقيت كسور لفظية في `الصداقة/الصدق/التنظيم` وتسرب محدود بين الموضوعات.
  - القرار: `runtime_switch_allowed=false`; يبقى runtime التجريبي على مرشح Phase 27.33 + فتح `الصبر` المحروس من 27.37.
  - التالي Phase 27.40 tokenizer/context repair for topic isolation.
  - أضيف [PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md](./PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.40 Tokenizer/Context Repair:
  - أُنشئ tokenizer v5: `artifacts/tokenizers/sf_bpe/v5_topic_terms`.
  - protected terms: `max_pieces=1`, `all_roundtrip_ok=true`.
  - دُرّب checkpoint مستهدف: `sf-10m-step6400`.
  - الاختبار: `24/24`.
  - regression: `8/8`.
  - new_topic: `8/8`.
  - heldout: `4/4`.
  - isolation: `4/4`.
  - القرار: المرشح `sf_10m_phase27_40` جاهز لتصميم فتح محروس، ثم فُتح في Phase 27.41 داخل `generator_trial=true` فقط.
  - التالي Phase 27.42 live UI observation and broader guarded probes.
  - أضيف [PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md](./PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.41 Guarded Runtime Switch:
  - مسار `generator_trial=true` صار يستخدم tokenizer v5 + checkpoint `sf-10m-step6400`.
  - المرشح المفتوح اختياريًا هو `sf_10m_phase27_40`.
  - فُحص `/chat/message` حيًا عبر HTTP: `22/22` passed.
  - generated lanes: `17/17`.
  - template/safety controls: `5/5`.
  - runtime الافتراضي ما زال `template`؛ لا فتح عام ولا `SF-50M`.
  - التالي Phase 27.42 live UI observation and broader guarded probes.
  - أضيف [PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md](./PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md).
- بدأ وانتهى Phase 27.42 Live UI Broader Probes:
  - أضيف حارس alignment أوسع لسؤال الحال والتخطيط والنصيحة والدعم.
  - صُحح false-positive في safety: `ما فائدة القراءة` لم تعد تُحجب كمال/استثمار.
  - فُحص `/chat/message` حيًا: `29/29` passed.
  - generated lanes: `20/20`.
  - guarded fallback / quality-floor / controls: `9/9`.
  - أمثلة حُجبت عمدًا: `وش اخبارك` و`نظم وقتي` عندما أعطى المولد ردًا غير مطابق.
  - القرار: تجربة الواجهة أوسع وأكثر أمانًا، لكن الافتراضي لا يزال `template` ولا `SF-50M`.
  - التالي Phase 27.43 guarded data-backed expansion.
  - أضيف [PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md](./PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md).
- بدأ وانتهى Phase 27.43 Guarded Data-Backed Expansion:
  - دُرّب مرشح `sf_10m_phase27_43` على tokenizer v5 لمعالجة weak lanes.
  - checkpoint محلي: `artifacts/eval/phase27_43_guarded_data_backed_expansion/checkpoints/sf-10m-step4800`.
  - الاختبار: `10/16`.
  - weak_lane: `4/6`.
  - regression: `6/8`.
  - new_topic: `0/2`.
  - التشخيص: البيانات وحدها سببت انجرافًا؛ بعض social/advice prompts صارت تعريفات، و`الوفاء/الشجاعة` انهارت إلى موضوعات قديمة.
  - القرار: لا runtime switch؛ الواجهة تبقى على `sf_10m_phase27_40` داخل `generator_trial=true`.
  - التالي Phase 27.44 tokenizer/curriculum repair for weak-lane stability.
  - أضيف [PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md](./PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md).
- بدأ وانتهى Phase 27.44 Tokenizer/Curriculum Repair:
  - أُنشئ tokenizer v6 في `artifacts/tokenizers/sf_bpe/v6_weak_lane_terms`.
  - protected phrases وصلت إلى `max_pieces=1` مع roundtrip صحيح.
  - الاختبار: `11/16`; weak-lane نجح `6/6` لكن regressions بقيت جزئية.
  - القرار: لا runtime switch.
- بدأ وانتهى Phase 27.45 Semantic Topic Balance Repair:
  - حاولنا موازنة تعريفات الموضوعات بعد خلط 27.44.
  - الاختبار: `9/16`.
  - القرار: التجربة تراجعت، لا runtime switch.
- بدأ وانتهى Phase 27.46 Core Dialogue Stabilization:
  - ركزنا على نواة حوار صغيرة بدل توسعة واسعة.
  - الاختبار: `14/16`; كل weak-lane وregressions نجحت، وبقي `الوفاء/الشجاعة`.
  - القرار: لا runtime switch حتى إصلاح conditioning.
- بدأ وانتهى Phase 27.47 New Topic Conditioning Repair:
  - أصلحنا سجلات التدريب لتضيف `المصطلح: الوفاء` و`المصطلح: الشجاعة`.
  - الاختبار offline: `16/16`.
  - المرشح: `sf_10m_phase27_47`, checkpoint `sf-10m-step4600`, tokenizer v6.
  - القرار: جاهز لبوابة runtime محروسة.
- بدأ وانتهى Phase 27.48 Guarded Runtime Switch:
  - فُتح `sf_10m_phase27_47` في `generator_trial=true` فقط.
  - الاختبار live API: `19/19`.
  - الافتراضي ما زال `template`، والحالات العامة/الحساسة تبقى على fallback.
  - التالي Phase 27.49 broader live UI probes.
  - أضيف [PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md](./PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md).
- بدأ وانتهى Phase 27.49 Broader Live UI/API Probes:
  - وسّعنا live API gate إلى `33` حالة.
  - اكتشفنا أن `وش تنصحني اسوي` كانت تسقط إلى `chat.general`.
  - أضيفت جذور `نصح/تنصح` إلى مسار كشف النصيحة وحارس alignment.
  - النتيجة بعد الإصلاح: `33/33`.
  - التالي Phase 27.50 targeted natural-prompt expansion plan.
  - أضيف [PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md](./PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md).
- بدأ وانتهى Phase 27.50 Generator-Only UI Lab Mode:
  - أزيل زر `مولّد تجريبي` من الواجهة.
  - `/chat/message` أصبح يستخدم مسار المولد دائمًا.
  - إذا رجع المسار الداخلي إلى template، يخفي API القالب ويعيد `response=""` مع `generator=generator_blocked`.
  - الاختبار الحي: `7/7`.
  - smoke: `وش الاخبار/علومك/نظم وقتي` مولّدة، و`من أنت/ما معنى الكرم` بلا رد بدل قالب.
  - التالي Phase 27.51 open-dialogue generalization audit.
  - أضيف [PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md](./PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md).
- بدأ وانتهى Phase 27.51 Open-Dialogue Generalization Audit:
  - أضيفت بوابة `make phase27-open-dialogue-generalization-audit`.
  - اختبرت live API وraw checkpoint بلا intent/topic conditioning على prompts طبيعية غير محفوظة.
  - النتيجة: `FAILED_OPEN_DIALOGUE_GENERALIZATION_AUDIT_TRAINING_REQUIRED`.
  - live API: `3/22`.
  - raw checkpoint: `3/22`، وnatural raw prompts: `1/20`.
  - السبب الجذري: `sf_10m_phase27_47` ما زال يخلط جملًا محفوظة ولا يعمم على الحوار المفتوح.
  - القرار: لا `SF-50M` ولا Phase 28؛ التالي Phase 27.52 Natural Dialogue Objective Repair.
  - أضيف [PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md](./PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md).
- بدأ وانتهى Phase 27.52 Natural Dialogue Objective Repair:
  - أضيف `make phase27-natural-dialogue-objective-repair`.
  - دُرّب `SF-10M` فقط، بدون تكبير حجم، وبدون intent/topic keyword lanes.
  - ميزانية التدريب: `9200` خطوة، أي `2.00x` مقارنة بـ Phase 27.47.
  - checkpoint محلي: `artifacts/eval/phase27_52_natural_dialogue_objective_repair/checkpoints/sf-10m-step9200`.
  - train records: `6400` من `40` زوجًا فريدًا مؤلفًا داخل المشروع.
  - نتيجة held-out raw natural: `5/20` بدل `1/20`.
  - التحسن: topic `3/4`, planning `2/4`.
  - الفشل: followup `0/4`, open_social `0/4`, support `0/4`.
  - القرار: لا runtime switch؛ لا `SF-50M` ولا Phase 28؛ التالي Phase 27.53 لتوسيع تنوع الحوار بدل زيادة الخطوات فقط.
  - أضيف [PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md](./PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.53 Natural Dialogue Diversity Expansion:
  - أضيف `make phase27-natural-dialogue-diversity-expansion`.
  - ولّد `10,540` سجلًا فريدًا: `5,270` فصحى و`5,270` سعودي.
  - السجلات اجتازت governance audit، ولا تحتوي حوار تشغيل/مشروع.
  - دُرّب `SF-10M` فقط، بدون تكبير حجم، على `18,000` خطوة.
  - checkpoint محلي: `artifacts/eval/phase27_53_natural_dialogue_diversity_expansion/checkpoints/sf-10m-step18000`.
  - نتيجة held-out raw natural: `2/36`.
  - السبب الجذري الظاهر: خلط أجزاء من ردود مختلفة وفقدان ارتباط prompt بالرد، مع fragments مثل `نقدر نًا`.
  - القرار: لا runtime switch؛ لا `SF-50M` ولا Phase 28 تلقائيًا؛ التالي Phase 27.54 Capacity/Objectivity Gate.
  - أضيف [PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md](./PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md).
- بدأ وانتهى Phase 27.54 Capacity/Objectivity Gate:
  - أضيف `make phase27-capacity-objectivity-gate`.
  - لم يبدأ أي تدريب جديد، ولم تُنشأ corpus أو checkpoints.
  - قرأ التقارير `27.51/27.52/27.53` وقارن المسار: `1/20` ثم `5/20` ثم `2/36`.
  - الاستنتاج: زيادة البيانات وحدها لم تساعد، والتكبير الكامل الآن سيكون قفزة عمياء.
  - القرار: لا runtime switch؛ لا تدريب `SF-50M` كامل؛ لا Phase 28.
  - المسموح التالي: Phase 27.55 micro-probe تشخيصي مضبوط فقط، يقارن `SF-50M` ضد `SF-10M` بنفس البيانات والتقييم، ولا يفتح runtime.
  - أضيف [PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md](./PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md).
- بدأ وانتهى Phase 27.55 Controlled SF-50M Diagnostic Micro-Probe:
  - أضيف `make phase27-sf50m-diagnostic-micro-probe`.
  - دُرّب `SF-10M` و`SF-50M` من الصفر على نفس corpus التشخيصي: `6400` سجل من `40` زوجًا فريدًا.
  - ميزانية التدريب: `700` خطوة لكل نموذج، tokenizer v6، sample-isolated، assistant loss.
  - النتيجة: `SF-10M=3/20`, `SF-50M=4/20`, delta=`1`.
  - القرار: السعة وحدها لم تثبت حل الحوار المفتوح؛ لا runtime switch، لا تدريب `SF-50M` كامل، ولا Phase 28.
  - التالي: Phase 27.56 objective/format/tokenizer diagnosis قبل أي محاولة سعة جديدة.
  - أضيف [PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md](./PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md).
- بدأ وانتهى Phase 27.56 Objective/Format/Tokenizer Diagnosis:
  - أضيف `make phase27-objective-format-tokenizer-diagnosis`.
  - لم يبدأ تدريب جديد ولم يتغير runtime.
  - شخّص تقرير Phase 27.55 من أربع زوايا: capacity، objective/format، eval، tokenizer.
  - النتيجة: `SF-50M strict=4/20` لكنه يصبح `9/20` عند تجاهل شرط overlap؛ هذا يكشف عيبًا في gate الحالي.
  - بقي `9` expected-missing و`11` response-family confusion في `SF-50M`.
  - tokenizer v6 يكسر `9` مصطلحات/عبارات حوارية حرجة، منها `نسولف` و`طمني` و`الي تحب`.
  - القرار: لا runtime، لا `SF-50M` كامل، ولا تدريب جديد قبل إصلاح tokenizer/eval/format.
  - التالي: Phase 27.57 tokenizer/eval/format repair pack.
  - أضيف [PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md](./PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md).
- بدأ وانتهى Phase 27.57 Tokenizer/Eval/Format Repair Pack:
  - أضيف `make phase27-tokenizer-eval-format-repair-pack`.
  - أضيف `resources/tokenization/protected_phrases_phase27_57.txt` وفيه `18` عبارة محمية.
  - غطت الحزمة `9/9` من العبارات الحرجة التي كشفها Phase 27.56.
  - أضيفت `resources/evaluation/semantic_alignment_phase27_57.json` لتعطيل prompt-overlap واستبداله بـ semantic alignment.
  - أضيفت `resources/dialogue_format/response_families_phase27_57.json` وفيها `5` قواعد تمنع خلط عائلات الردود.
  - القرار: يسمح فقط بتدريب محدود في Phase 27.58، ولا runtime switch ولا `SF-50M` كامل.
  - أضيف [PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md](./PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md).
- بدأ وانتهى Phase 27.58 Tokenizer v7 Bounded Alignment Probe:
  - أضيف `make phase27-tokenizer-bounded-alignment-probe`.
  - دُرّب tokenizer v7 في `artifacts/tokenizers/sf_bpe/v7_phase27_58`.
  - استخدم `53` مصطلحًا/عبارة محمية، وحافظ على عبارات Phase 27.57 كقطعة واحدة (`max_pieces=1`).
  - دُرّب probe محدود `SF-10M` لمدة `7600` خطوة داخل `artifacts/eval/phase27_58_tokenizer_bounded_alignment_probe`.
  - النتيجة: `4/15` فقط؛ فشلت `open_social=0/3` و`followup=0/3` وبقي خلط في `topic`.
  - القرار: لا runtime switch، لا فتح UI، لا `SF-50M`، ولا Phase 28.
  - التالي: Phase 27.59 إصلاح عائلات `open_social/followup/topic` قبل أي توسيع.
  - أضيف [PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md](./PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md).
- بدأ وانتهى Phase 27.59 Bounded Alignment Repair:
  - أضيف `make phase27-bounded-alignment-repair`.
  - استخدم tokenizer v7 من Phase 27.58 بدون إعادة بنائه.
  - دُرّب repair probe محدود `SF-10M` لمدة `6400` خطوة على `24` زوج إصلاح و`2880` سجل تدريب.
  - النتيجة: `15/15` في بوابة alignment المحدودة.
  - نجحت العائلات: `open_social=3/3`, `followup=3/3`, `planning=3/3`, `support=3/3`, `topic=3/3`.
  - القرار: لا runtime switch ولا UI بعد؛ النجاح يسمح فقط بـ Phase 27.60 canary أوسع.
  - أضيف [PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md](./PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.60 Broader Natural-Dialogue Canary:
  - أضيف `make phase27-broader-natural-dialogue-canary`.
  - لم يبدأ تدريب جديد؛ قيّم checkpoint Phase 27.59 فقط.
  - النتيجة: `12/30`.
  - التوزيع: `open_social=5/6`, `followup=3/6`, `planning=2/6`, `support=0/6`, `topic=2/6`.
  - الفشل المتكرر: collapse إلى عبارات مثل `خفيف عن يومك` خارج سياقها، وفشل دعم/موضوعات/تخطيط.
  - القرار: لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.
  - التالي: Phase 27.61 إصلاح generalization الطبيعي خصوصًا `support/topic/planning`.
  - أضيف [PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md](./PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md).
- بدأ وانتهى Phase 27.61 Broader Generalization Repair:
  - أضيف `make phase27-broader-generalization-repair`.
  - دُرّب repair محدود على tokenizer v7 لمدة `8200` خطوة.
  - النتيجة تحسنت من `12/30` إلى `18/30`.
  - نجحت `planning=6/6` و`support=6/6`.
  - تراجعت/فشلت `open_social=2/6`, `followup=3/6`, `topic=1/6`.
  - القرار: لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.
  - التالي: Phase 27.62 إصلاح توازن العائلات ومنع انجذاب الموضوعات/السوالف إلى `الوفاء` أو الدعم.
  - أضيف [PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md](./PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.62 Family Balance Repair:
  - أضيف `make phase27-family-balance-repair`.
  - دُرّب repair محدود متوازن بالعدد على tokenizer v7 لمدة `7800` خطوة.
  - النتيجة تراجعت إلى `10/30`.
  - نجحت `open_social=6/6` لكن تضررت `support=0/6` و`planning=1/6`.
  - التشخيص: توازن العدد وحده لا يكفي؛ ترتيب corpus الكتلي تسبب في انجذاب النموذج لعائلة واحدة.
  - القرار: لا runtime switch، لا UI، لا `SF-50M`، ولا Phase 28.
  - أضيف [PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md](./PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.63 Interleaved Family Curriculum:
  - أضيف `make phase27-interleaved-family-curriculum`.
  - أعيدت كتابة curriculum بترتيب round-robin بين العائلات مع LR أخف وخطوات أقل (`5600`).
  - النتيجة تحسنت إلى `26/30`.
  - نجحت `open_social=6/6`, `planning=6/6`, `support=6/6`, و`followup=5/6`.
  - بقيت مشاكل `topic` في `التعاون` و`الاحترام` مع مؤشرات lexical/tokenization collapse.
  - القرار: لا runtime switch ولا فتح واجهة؛ التالي Phase 27.64 لفحص حماية التوكنة للمصطلحات الموضوعية قبل تدريب جديد.
  - أضيف [PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md](./PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md).
- بدأ وانتهى Phase 27.64 Topic Lexical/Tokenizer Inspection:
  - أضيف `resources/tokenization/protected_phrases_phase27_64.txt`.
  - أضيف `make phase27-topic-lexical-tokenizer-inspection`.
  - لم يبدأ أي تدريب.
  - أثبت الفحص أن `التعاون` في tokenizer v7 = `3` قطع وغير محمية، و`الاحترام` = `4` قطع وغير محمية.
  - كلا المصطلحين كانا single-piece في tokenizer v6، لذلك v7 أحدث regression في موضوعات حرجة.
  - القرار: tokenizer v8 مطلوب قبل أي LM repair جديد؛ لا runtime switch ولا UI ولا `SF-50M`.
  - أضيف [PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md](./PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md).
- بدأ وانتهى Phase 27.65 Tokenizer v8 Topic Probe:
  - أضيف `make phase27-tokenizer-v8-topic-probe`.
  - دُرّب tokenizer v8 فقط في `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
  - لا تدريب LM في هذه المرحلة.
  - النتيجة: critical terms `2/2`, topic terms `8/8`, boundary roundtrip `6/6`.
  - `التعاون` و`الاحترام` صارتا single-piece ومحميتين.
  - القرار: يسمح فقط بـ Phase 27.66 bounded LM topic repair على tokenizer v8؛ لا runtime switch ولا UI ولا `SF-50M`.
  - أضيف [PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md](./PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md).
- بدأ وانتهى Phase 27.66 V8 Bounded Topic Repair:
  - أضيف `make phase27-v8-bounded-topic-repair`.
  - استُخدم tokenizer v8 من `artifacts/tokenizers/sf_bpe/v8_phase27_65`.
  - دُرّب `SF-10M` إصلاحًا محدودًا `6200` خطوة، وليس تكبير حجم.
  - النتيجة: broader canary `30/30`، وكل العائلات `6/6`.
  - القرار: يسمح فقط بـ Phase 27.67 fresh shadow canary؛ لا runtime switch ولا UI ولا `SF-50M`.
  - أضيف [PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md](./PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.67 Fresh Shadow Canary:
  - أضيف `make phase27-fresh-shadow-canary`.
  - لا تدريب جديد في هذه المرحلة.
  - اختُبر checkpoint Phase 27.66 على `50` سؤالًا جديدًا غير مطابق للتدريب/canary السابق.
  - novelty: `50/50`.
  - النتيجة: `30/50` فقط.
  - family summary: open_social `4/10`, followup `4/10`, planning `7/10`, support `6/10`, topic `9/10`.
  - القرار: لا runtime switch ولا UI؛ Phase 27.68 يجب أن يصلح انجراف العائلات قبل أي فتح واجهة.
  - أضيف [PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md](./PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md).
- بدأ وانتهى Phase 27.68 Shadow Failure Repair:
  - أضيف `make phase27-shadow-failure-repair`.
  - دُرّب `SF-10M` إصلاحًا محدودًا على tokenizer v8 لمدة `5600` خطوة.
  - أضيف إصلاح للحارس حتى لا يطابق أجزاء الكلمات مثل `مرتبك` ← `رتب`.
  - النتيجة: known shadow Phase 27.67 صار `50/50`.
  - regression Phase 27.60 بقي `30/30`.
  - القرار: لا runtime switch ولا UI؛ المسموح التالي Phase 27.69 fresh shadow جديد بأسئلة غير مرئية بعد الإصلاح.
  - أضيف [PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md](./PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md).
- بدأ وانتهى Phase 27.69 New Fresh Shadow Canary:
  - أضيف `make phase27-new-fresh-shadow-canary`.
  - لا تدريب جديد في هذه المرحلة.
  - اختُبر checkpoint Phase 27.68 على `60` prompt جديدًا.
  - novelty: `60/60`.
  - النتيجة: `56/60`.
  - family summary: followup `12/12`, open_social `8/12`, planning `12/12`, support `12/12`, topic `12/12`.
  - القرار: لا runtime switch ولا UI؛ Phase 27.70 يركز على فشل open_social فقط.
  - أضيف [PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md](./PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md).

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
GET  /health        → {"status":"ok","project":"SF.AI","phase":"Phase 27.50"}
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
696 passed in 84.74s (0:01:24)
```

| التحقق | النتيجة |
|------|------|
| full pytest suite | `696 passed in 84.74s (0:01:24)` |
| focused Phase 27.81/API/UI tests | `79 passed in 18.40s` |
| `make corpus-audit` | `9125` records, `issues=0` |
| `make phase27-dialogue-eval` | `19/19`, `open_generator_ready=false` |

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

## Phase 27.82 — Family-conditioned SF-10M Repair Training Decision

- أضيف `make phase27-family-conditioned-training-decision`.
- لم يبدأ تدريب جديد، ولم يتغير runtime، ولم يدرّب tokenizer جديد.
- القرار الرسمي: `PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION`.
- النتيجة: يسمح فقط بـ `Phase 27.83 — Family-conditioned SF-10M bounded repair training`.
- المسموح في 27.83: تدريب إصلاح محدود لـ `SF-10M` باستخدام tokenizer v9 وcheckpoint
  `sf-10m-step6200` من Phase 27.77، objective مساعد فقط، وfamily-conditioned curriculum.
- المحظور: runtime release، `SF-50M`, tokenizer retrain، pretrained/open-weight.
- التقارير:
  - [PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION.md](./PHASE27_82_FAMILY_CONDITIONED_TRAINING_DECISION.md)
  - `artifacts/reports/phase27_82_family_conditioned_training_decision_report.json`
  - `artifacts/reports/phase27_82_family_conditioned_training_decision/phase27_83_training_plan.json`

---

## Phase 27.83 — Family-conditioned SF-10M Bounded Repair Training

- نُفّذ تدريب إصلاح محدود لـ `SF-10M` حسب خطة Phase 27.82.
- الجهاز: Apple Silicon MPS؛ التدريب اكتمل في نحو `58.2s`.
- checkpoints المحلية:
  - `sf-10m-step600`
  - `sf-10m-step1200`
  - `sf-10m-step1800`
- أفضل fresh shadow:
  - `step600`: `7/60`, eval loss `3.7397`.
  - `step1200`: `11/60`, eval loss `5.9248`.
  - `step1800`: `3/60`, eval loss `5.9722`.
- القرار: `BLOCK_RUNTIME_DIAGNOSE_OBJECTIVE_CURRICULUM_FAILURE`.
- لا واجهة مولّدة، لا runtime release، لا SF-50M، لا tokenizer retrain.
- التالي: Phase 27.84 لتشخيص سبب فشل objective/curriculum بدل تدريب جديد أعمى.
- التقارير:
  - [PHASE27_83_FAMILY_CONDITIONED_REPAIR_TRAINING_REPORT.md](./PHASE27_83_FAMILY_CONDITIONED_REPAIR_TRAINING_REPORT.md)
  - `artifacts/reports/phase27_83_family_conditioned_repair_training_report.json`
  - `artifacts/samples/phase27_83_family_conditioned_repair_training.md`

---

## Phase 27.84 — Objective/Curriculum Failure Diagnosis

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- شُخّص فشل Phase 27.83 من تقارير fresh shadow وبيانات corpus.
- السبب الأكبر: `dialogue_family` موجودة في metadata، لكنها لا تظهر داخل نص التدريب.
- النص الذي يراه النموذج حاليًا يحتوي `النطاق: سعودي/فصحى` فقط، ولا يحتوي مثلًا `العائلة: planning`.
- أوزان السبب:
  - `objective_family_signal_missing=30%`
  - `curriculum_sampling_not_family_conditioned_in_text=24%`
  - `weak_generalization_after_bounded_repair=17%`
  - `decoding_and_repetition_fragility=10%`
  - `model_capacity=4%`
- القرار: لا SF-50M، لا runtime، لا tokenizer retrain، ولا تدريب جديد قبل تصميم family conditioning صريح.
- التالي: Phase 27.85 — Explicit Family Conditioning Objective Design.
- التقارير:
  - [PHASE27_84_OBJECTIVE_CURRICULUM_FAILURE_DIAGNOSIS_REPORT.md](./PHASE27_84_OBJECTIVE_CURRICULUM_FAILURE_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_84_objective_curriculum_failure_diagnosis_report.json`

---

## Phase 27.85 — Explicit Family Conditioning Objective Design

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- صُممت صيغة conditioning صريحة تظهر داخل نص التدريب:
  - `النطاق: فصحى/سعودي`
  - `عائلة الحوار: سوالف/متابعة/تنظيم/دعم/موضوع`
- mapping العائلات:
  - `open_social → سوالف`
  - `followup → متابعة`
  - `planning → تنظيم`
  - `support → دعم`
  - `topic → موضوع`
- قاعدة objective: أسطر conditioning وسطر المستخدم تبقى masked مع `loss_scope=assistant`; الهدف فقط رد المساعد + EOS.
- القرار: يسمح فقط بـ Phase 27.86 لتنفيذ renderer gate، ولا يسمح بتدريب جديد.
- التقارير:
  - [PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_DESIGN_REPORT.md](./PHASE27_85_EXPLICIT_FAMILY_CONDITIONING_OBJECTIVE_DESIGN_REPORT.md)
  - `artifacts/reports/phase27_85_explicit_family_conditioning_objective_design_report.json`
  - `artifacts/reports/phase27_85_family_conditioning_objective_spec.json`

---

## Phase 27.86 — Family Conditioning Renderer Gate

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- أضيفت حقول family إلى `Provenance`: `dialogue_family`, `prompt_family`, `answer_family`.
- أصبح renderer المشترك في dataset/training يطبع سياق التدريب بهذا الشكل:
  - `النطاق: فصحى/سعودي`
  - `عائلة الحوار: سوالف/متابعة/تنظيم/دعم/موضوع`
  - `المستخدم: ...`
  - `المساعد: ...`
- تم توحيد مسار no-split ومسار split-manifest عبر `render_dialogue_text`.
- gate أثبت أن:
  - كل العائلات الخمس تظهر بسطر عربي مستقل.
  - مساري split/no-split يخرجان `عائلة الحوار: ...`.
  - `loss_scope=assistant` يخفي سطور conditioning وسطر المستخدم عن loss.
  - رد المساعد + EOS فقط هما الهدف supervised.
- القرار: يسمح فقط بـ Phase 27.87 لتدريب SF-10M مقيّد بإشارة family، ولا يسمح بـ runtime أو SF-50M أو tokenizer جديد.
- التقارير:
  - [PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_REPORT.md](./PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_REPORT.md)
  - `artifacts/reports/phase27_86_family_conditioning_renderer_gate_report.json`
  - `artifacts/reports/PHASE27_86_FAMILY_CONDITIONING_RENDERER_GATE_DECISION.json`

---

## Phase 27.87 — Bounded Family-conditioned SF-10M Repair Training

- بدأ واكتمل تدريب مقيّد لـ `SF-10M` بعد نجاح renderer gate.
- لم يتغير runtime ولم تُفتح الواجهة للمولد الجديد.
- التدريب استخدم:
  - tokenizer: `artifacts/tokenizers/sf_bpe/v9_phase27_76`
  - init checkpoint: `phase27_77_v9_bounded_open_social_lm_repair/checkpoints/sf-10m-step6200`
  - `loss_scope=assistant`
  - `packing_mode=sample_isolated`
  - `split=train`
  - renderer الجديد الذي يضيف `عائلة الحوار`.
- checkpoints المحلية:
  - `sf-10m-step600`
  - `sf-10m-step1200`
  - `sf-10m-step1800`
- التقييم العائلي مع نفس family conditioning:
  - step600: `10/50`، منحاز إلى `open_social`.
  - step1200: `10/50`، منحاز إلى `planning`.
  - step1800: `7/50`، منحاز إلى `support`.
- القرار: runtime محجوب؛ لا SF-50M؛ لا tokenizer retrain؛ لا تدريب جديد قبل تشخيص سبب الانحياز.
- التالي: Phase 27.88 — Family-conditioned Training Result Diagnosis.
- التقارير:
  - [PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_REPORT.md](./PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_87_bounded_family_conditioned_repair_report.json`
  - `artifacts/reports/PHASE27_87_BOUNDED_FAMILY_CONDITIONED_REPAIR_DECISION.json`
  - `artifacts/samples/phase27_87_bounded_family_conditioned_repair.md`

---

## Phase 27.88 — Family-conditioned Training Result Diagnosis

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- شُخّص سبب فشل Phase 27.87 كخلل curriculum/sampling لا كخلل سعة.
- الدليل من أول 1800 عينة تدريب:
  - `متابعة=451`
  - `سوالف=444`
  - `تنظيم=452`
  - `دعم=448`
  - `موضوع=5`
- نوافذ checkpoints:
  - step600: يغلب عليها `متابعة` بنسبة `0.7517`.
  - step1200: يغلب عليها `تنظيم` بنسبة `0.5083` ونتيجة التوليد انحازت إلى planning.
  - step1800: يغلب عليها `دعم` بنسبة `0.7467` ونتيجة التوليد انحازت إلى support.
- أوزان السبب:
  - sequential curriculum ordering: `38%`
  - checkpoint recency bias: `22%`
  - topic underexposure before step1800: `16%`
  - family condition signal not interleaved: `12%`
  - capacity: `4%`
- القرار: لا SF-50M، لا runtime، لا tokenizer retrain، ولا تدريب جديد قبل بناء sampler round-robin متوازن و dry-run gate.
- التالي: Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate.
- التقارير:
  - [PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_REPORT.md](./PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_88_family_conditioned_training_result_diagnosis_report.json`
  - `artifacts/reports/PHASE27_88_FAMILY_CONDITIONED_TRAINING_RESULT_DIAGNOSIS_DECISION.json`

---

## Phase 27.89 — Stratified Round-Robin Curriculum Sampler Gate

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- أضيف ترتيب تدريب جديد داخل `train_tiny_lm`: `--split-order family_round_robin`.
- `iter_split_samples_round_robin_by_family` يوزع العائلات الخمس المعلّمة أولًا بالتناوب، ثم يترك العينات غير الموسومة إلى آخر stream.
- نتيجة dry-run لأول 1800 عينة:
  - `open_social=360`
  - `followup=360`
  - `planning=360`
  - `support=360`
  - `topic=360`
- كل نافذة 600 عينة تحتوي:
  - `120` من كل عائلة.
  - dominant share = `0.20`.
  - missing families = `[]`.
- القرار: `ALLOW_PHASE27_90_BOUNDED_SF10M_TRAINING_WITH_ROUND_ROBIN_SPLIT_ORDER`.
- المسموح التالي: تدريب SF-10M محدود فقط باستخدام `--split-order family_round_robin`.
- المحظور الآن: runtime release، UI generator release، SF-50M، tokenizer retrain، pretrained/open-weight usage.
- التقارير:
  - [PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_REPORT.md](./PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_REPORT.md)
  - `artifacts/reports/phase27_89_stratified_round_robin_curriculum_sampler_gate_report.json`
  - `artifacts/reports/PHASE27_89_STRATIFIED_ROUND_ROBIN_CURRICULUM_SAMPLER_GATE_DECISION.json`

---

## Phase 27.90 — Bounded SF-10M Round-Robin Curriculum Repair Training

- بدأ تدريب محدود مسموح فقط بعد gate 27.89.
- الأمر استخدم `--split-order family_round_robin` مع tokenizer v9 وcheckpoint `sf-10m-step6200` من Phase 27.77.
- التدريب:
  - steps: `1800`
  - save_every: `600`
  - seq_len: `96`
  - batch_size: `1`
  - loss_scope: `assistant`
  - packing_mode: `sample_isolated`
- loss: `10.0272 → 1.0993`.
- التقييم fresh shadow:
  - `sf-10m-step600`: `26/50`
  - `sf-10m-step1200`: `32/50`
  - `sf-10m-step1800`: `35/50` best
- ملخص أفضل checkpoint:
  - open_social: `9/10`
  - followup: `8/10`
  - planning: `10/10`
  - support: `7/10`
  - topic: `1/10`
- القرار: `BLOCK_RUNTIME_DIAGNOSE_ROUND_ROBIN_TRAINING_RESULT`.
- سبب الحجب: النتيجة `35/50` أقل من بوابة held-out/runtime `45/50`، وtopic ما زال ضعيفًا جدًا.
- المحظور الآن: runtime release، UI generator release، SF-50M، tokenizer retrain.
- التالي: Phase 27.91 — Round-Robin Training Result Diagnosis.
- التقارير:
  - [PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_REPORT.md](./PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_90_bounded_round_robin_repair_report.json`
  - `artifacts/reports/PHASE27_90_BOUNDED_ROUND_ROBIN_REPAIR_DECISION.json`
  - `artifacts/samples/phase27_90_bounded_round_robin_repair.md`

---

## Phase 27.91 — Round-Robin Training Result Diagnosis

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- شُخّص best checkpoint من Phase 27.90: `sf-10m-step1800`.
- إخفاقات `15/50` توزعت كالتالي:
  - topic: `9`
  - support: `3`
  - followup: `2`
  - open_social: `1`
- buckets:
  - `topic_semantic_collapse=7`
  - `topic_repetition_collapse=2`
  - `support_eval_alias_gap=3`
  - `followup_surface_artifact=2`
  - `open_social_eval_alias_gap=1`
- أوزان السبب:
  - topic semantic collapse: `48%`
  - topic underlearning after round-robin: `18%`
  - evaluation alias gap: `12%`
  - followup surface artifacts: `8%`
  - decoding repetition: `6%`
  - capacity: `4%`
- القرار: `DESIGN_TOPIC_OBJECTIVE_REPAIR_GATE_BEFORE_ANY_TRAINING`.
- المحظور الآن: training, runtime release, SF-50M, tokenizer retrain.
- التالي: Phase 27.92 — Topic Objective Repair Design Gate.
- التقارير:
  - [PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_REPORT.md](./PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_91_round_robin_training_result_diagnosis_report.json`
  - `artifacts/reports/PHASE27_91_ROUND_ROBIN_TRAINING_RESULT_DIAGNOSIS_DECISION.json`

---

## Phase 27.92 — Topic Objective Repair Design Gate

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- حُوّل تشخيص Phase 27.91 إلى تصميم objective محدد لعائلة `topic`.
- الهدف المصمم: `topic_anchor_prompt_to_answer_objective_v1`.
- صيغة conditioning المطلوبة في المرحلة التالية:
  - `النطاق: <فصحى|سعودي>`
  - `عائلة الحوار: موضوع`
  - `الموضوع المطلوب: <topic_term>`
- عقد رد المساعد: جملة قصيرة، تذكر الموضوع المطلوب داخل الجملة الأولى، ولا تستبدله بموضوع آخر، ولا تكرر أو تنتج كسورًا لفظية.
- مصطلحات الموضوع المستهدفة: `الوفاء`, `التعاون`, `الصبر`, `الاحترام`, `الهدوء`, `الصدق`, `الصداقة`, `الشجاعة`.
- بوابات canary المطلوبة قبل أي runtime:
  - known topic: `18/20`
  - fresh topic shadow: `16/20`
  - all-family regression: `45/50`
  - topic family minimum: `8/10`
  - malformed/repetition: `0`
- القرار: `ALLOW_PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_NO_TRAINING`.
- المحظور الآن: training, runtime release, SF-50M, tokenizer retrain, pretrained/open-weight usage.
- التالي: Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation.
- التقارير:
  - [PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_GATE_REPORT.md](./PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_GATE_REPORT.md)
  - `artifacts/reports/phase27_92_topic_objective_repair_design_gate_report.json`
  - `artifacts/reports/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION.json`
  - `artifacts/reports/phase27_92_topic_objective_repair_spec.json`

---

## Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- أضيف إلى renderer سطر سياقي لعائلة `topic` فقط:
  - `الموضوع المطلوب: <topic_term>`
- السطر الجديد يضاف بعد `عائلة الحوار: موضوع` وقبل `المستخدم:`.
- أثبتت البوابة أن assistant-only loss يخفي سطر النطاق والعائلة والموضوع والمستخدم عن الهدف، ويبقي رد المساعد فقط supervised.
- أضيف canary manifest في:
  - `eval/prompts/phase27_93_topic_objective_canary.json`
- يغطي canary الموضوعات الثمانية بالفصحى والسعودي:
  - `الوفاء`, `التعاون`, `الصبر`, `الاحترام`, `الهدوء`, `الصدق`, `الصداقة`, `الشجاعة`
- dry-run passed: `true`.
- بعد Phase 27.94 أصبح training data ready: `true`.
- قبل Phase 27.94 كان سبب الحجب: نقص `الوفاء` سعوديًا؛ أُغلق الآن.
- القرار الحالي بعد إعادة تشغيل البوابة: `ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING`.
- المحظور الآن: runtime release, SF-50M, tokenizer retrain, pretrained/open-weight usage.
- التالي: Phase 27.95 — Bounded Topic Objective Repair Training.
- التقارير:
  - [PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_REPORT.md](./PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_REPORT.md)
  - `artifacts/reports/phase27_93_topic_objective_gate_encoding_report.json`
  - `artifacts/reports/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION.json`
  - `eval/prompts/phase27_93_topic_objective_canary.json`

---

## Phase 27.94 — Topic Objective Data Pack Authoring

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يدرّب tokenizer جديد.
- أضيفت حزمة سيادية صغيرة لسد فجوة `الوفاء` السعودية:
  - `data/corpus/chat/jsonl/dialogue_batch_v11_topic_objective_wafa_saudi_011.jsonl`
  - `10` سجلات `gold`
  - dialect: `saudi`
  - dialogue_family/topic_term: `topic` / `الوفاء`
- corpus الحالي بعد الحزمة:
  - total: `8453`
  - dialects: `msa=4199`, `saudi=4254`
  - quality: `gold=3341`, `silver=5112`
  - split: `train=7603`, `eval=850`
- أعيد بناء split manifest:
  - `data/corpus/chat/splits/dialogue_split_v1.json`
- أعيد تشغيل Phase 27.93 gate بعد الحزمة:
  - dry-run passed: `true`
  - training data ready: `true`
  - shortfalls: `{}`
  - `الوفاء`: total=`22`, `msa=12`, `saudi=10`
- القرار الرسمي: `PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_DECISION`.
- القرار الهندسي: `ALLOW_PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_TRAINING`.
- المحظور في 27.94: runtime release, UI generator release, SF-50M transition,
  tokenizer retrain, pretrained/open-weight usage.
- التقرير:
  - [PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_REPORT.md](./PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_REPORT.md)
  - `artifacts/reports/phase27_94_topic_objective_data_pack_report.json`
  - `artifacts/reports/PHASE27_94_TOPIC_OBJECTIVE_DATA_PACK_DECISION.json`

---

## Phase 27.95 — Bounded Topic Objective Repair Training

- بدأ وانتهى تدريب SF-10M مقيّد.
- لا runtime release.
- لا UI generator release.
- لا SF-50M.
- لا tokenizer retrain.
- أضيف تطابق prompt بين التدريب والتقييم:
  - `NativeGenerator(family_conditioning=True)` يضيف الآن `الموضوع المطلوب: <topic>` لعائلة `topic` فقط.
- إعداد التدريب:
  - tokenizer: `artifacts/tokenizers/sf_bpe/v9_phase27_76`
  - init checkpoint: `artifacts/eval/phase27_90_round_robin_curriculum_repair/checkpoints/sf-10m-step1800`
  - steps: `1800`
  - seq_len: `96`
  - loss_scope: `assistant`
  - packing_mode: `sample_isolated`
  - split_order: `family_round_robin`
- النتيجة:
  - best checkpoint: `sf-10m-step1800`
  - known topic: `10/16`، والبوابة المطلوبة `16/16`
  - fresh topic: `4/10`، والبوابة المطلوبة `8/10`
  - all-family regression: `33/50`، والبوابة المطلوبة `45/50`
- القرار: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_OBJECTIVE_REPAIR_RESULT`.
- التالي: Phase 27.96 — Topic Objective Repair Result Diagnosis.
- التقارير:
  - [PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_REPORT.md](./PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_95_bounded_topic_objective_repair_report.json`
  - `artifacts/reports/PHASE27_95_BOUNDED_TOPIC_OBJECTIVE_REPAIR_DECISION.json`
  - `artifacts/samples/phase27_95_bounded_topic_objective_repair.md`

---

## Phase 27.96 — Topic Objective Repair Result Diagnosis

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يدرّب tokenizer جديد.
- شُخّصت نتيجة Phase 27.95 بعد فشل البوابات.
- الإشارة الأساسية:
  - topic failures تمر من الحارس: `guard_blocked_topic_failures=0`.
  - النموذج يستبدل الموضوع المطلوب بموضوعات مجاورة: `wrong_topic_substitution_count=11`.
  - أكثر بديل خاطئ: `الصداقة=6`.
- أوزان السبب الجذري:
  - `topic_variable_binding_failure=34%`
  - `assistant_target_copy_objective_weak=22%`
  - `topic_family_balance_residual=14%`
  - `model_capacity=3%`
- القرار: `DESIGN_TOPIC_COPY_CONTRASTIVE_OBJECTIVE_BEFORE_ANY_TRAINING`.
- التالي: Phase 27.97 — Topic Variable Binding Objective Design.
- المحظور الآن: training, runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage, keyword/template masking.
- التقارير:
  - [PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_REPORT.md](./PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_96_topic_objective_result_diagnosis_report.json`
  - `artifacts/reports/PHASE27_96_TOPIC_OBJECTIVE_RESULT_DIAGNOSIS_DECISION.json`

---

## Phase 27.97 — Topic Variable Binding Objective Design

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- صُمم objective جديد باسم:
  - `topic_copy_contrastive_binding_objective_v1`
- قاعدة الرد الجديدة:
  - يجب أن ينسخ رد المساعد الموضوع المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا.
  - قوالب الهدف المسموحة: `معنى <topic_term>:`, `<topic_term> يعني`, `<topic_term> هو`.
  - أي موضوع محمي آخر داخل رد topic يصبح فشلًا إذا لم يظهر الموضوع المطلوب أولًا.
- canary المطلوب:
  - `known_topic_min=16/16`
  - `fresh_topic_min=8/10`
  - `contrastive_wrong_topic_max=0`
  - `copy_anchor_min=26/26`
  - `all_family_regression_min=45/50`
- القرار: `ALLOW_PHASE27_98_TOPIC_BINDING_GATE_ENCODING_NO_TRAINING`.
- التالي: Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit.
- المحظور الآن: training, runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage, keyword/template masking.
- التقارير:
  - [PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_REPORT.md](./PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_REPORT.md)
  - `artifacts/reports/phase27_97_topic_variable_binding_objective_design_report.json`
  - `artifacts/reports/PHASE27_97_TOPIC_VARIABLE_BINDING_OBJECTIVE_DESIGN_DECISION.json`
  - `artifacts/reports/phase27_97_topic_variable_binding_objective_spec.json`

---

## Phase 27.98 — Topic Binding Gate Encoding and Metadata Audit

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يتغير tokenizer.
- رُمزت بوابة 27.97:
  - renderer يستطيع إنتاج target يبدأ بالموضوع المطلوب.
  - assistant-only loss يبقي سطور السياق والطلب masked.
  - canary contrastive جديد يغطي `26` حالة (`16` known + `10` fresh).
- نتيجة metadata قبل الإصلاح:
  - total topic records: `510`
  - explicit `topic_term`: `10`
  - missing `topic_term`: `500`
  - لذلك التدريب محجوب؛ لا يجوز الاعتماد على inference داخل training gate.
- القرار الأول: `ALLOW_PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_DATA_REPAIR_NO_TRAINING`.
- بعد Phase 27.99، أعيد تشغيل البوابة وصارت:
  - `training_ready=true`
  - `metadata_ready=true`
  - `copy_anchor_ready=true`
  - `missing_topic_term_records=0`
  - القرار المحدث: `ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING`
- التالي: Phase 27.100 — Bounded Topic Binding Repair Training.
- المحظور الآن: training, runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage, keyword/template masking.
- التقارير:
  - [PHASE27_98_TOPIC_BINDING_GATE_ENCODING_REPORT.md](./PHASE27_98_TOPIC_BINDING_GATE_ENCODING_REPORT.md)
  - `artifacts/reports/phase27_98_topic_binding_gate_encoding_report.json`
  - `artifacts/reports/PHASE27_98_TOPIC_BINDING_GATE_ENCODING_DECISION.json`
  - `eval/prompts/phase27_98_topic_binding_contrastive_canary.json`

---

## Phase 27.99 — Topic Metadata and Copy-Anchor Data Repair

- لم يبدأ تدريب جديد.
- لم يتغير runtime.
- لم يتغير tokenizer.
- أصلحت المرحلة ملفي topic من Phase 27.81:
  - `dialogue_batch_v10_balanced_topic_msa_010.jsonl`
  - `dialogue_batch_v10_balanced_topic_saudi_010.jsonl`
- أضيف `provenance.topic_term` إلى `500` سجل topic.
- تأكد copy-anchor لكل سجلات topic:
  - `missing_topic_term_records=0`
  - `copy_anchor_bad=0`
  - `unknown_topic=0`
- القرار: `ALLOW_PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_TRAINING`.
- التالي: Phase 27.100 — Bounded Topic Binding Repair Training.
- المحظور الآن: runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage.
- التقارير:
  - [PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_REPORT.md](./PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_99_topic_metadata_copy_anchor_repair_report.json`
  - `artifacts/reports/PHASE27_99_TOPIC_METADATA_COPY_ANCHOR_REPAIR_DECISION.json`

---

## Phase 27.100 — Bounded Topic Binding Repair Training

الحالة: **مكتملة كتدريب مقيّد؛ runtime محجوب والتشخيص مطلوب.**

- المسار: `Sovereign Practical Acceleration Strategy v2`.
- السيادة: `SF-native only`; لا pretrained/open-weight/Qwen.
- القاموس/المسار: `Saudi Seed v1`, `msa + saudi`.
- الهدف: تدريب إصلاح محدود على `SF-10M` لربط الموضوع المطلوب بالرد.
- objective: `topic_copy_contrastive_binding_objective_v1`.
- init checkpoint:
  `artifacts/eval/phase27_90_round_robin_curriculum_repair/checkpoints/sf-10m-step1800`.
- tokenizer: `artifacts/tokenizers/sf_bpe/v9_phase27_76`.
- أفضل checkpoint: `sf-10m-step1800`.
- النتائج:
  - known topic: `13/16`
  - fresh topic: `5/10`
  - copy-anchor: `18/26`
  - wrong-topic count: `0`
  - topic family: `6/10`
  - all-family: `37/50`
- القرار: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_BINDING_REPAIR_RESULT`.
- التالي: Phase 27.101 — Topic Binding Repair Result Diagnosis.
- المحظور الآن: runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage.
- التقارير:
  - [PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_REPORT.md](./PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_100_bounded_topic_binding_repair_report.json`
  - `artifacts/reports/PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_DECISION.json`

---

## Phase 27.101 — Topic Binding Repair Result Diagnosis

الحالة: **مكتملة كتشخيص فقط؛ لا تدريب ولا runtime.**

- المسار: `Sovereign Practical Acceleration Strategy v2`.
- السيادة: `SF-native only`; لا pretrained/open-weight/Qwen.
- القاموس/المسار: `Saudi Seed v1`, `msa + saudi`.
- المصدر: Phase 27.100 best checkpoint `sf-10m-step1800`.
- النتائج التي شُخّصت:
  - known topic: `13/16`
  - fresh topic: `5/10`
  - copy-anchor: `18/26`
  - reported wrong-topic count: `0`
  - observed wrong-topic count: `8`
  - topic-family: `6/10`
  - all-family: `37/50`
- التشخيص:
  - `wrong_topic_metric_blind_spot=true`
  - `topic_prototype_attraction=true`
  - بدائل الموضوع المرصودة: `الصداقة=7`, `الامتنان=1`
- أوزان السبب الجذري الأعلى:
  - `copy_anchor_objective_underpowered=28%`
  - `topic_prototype_attraction=20%`
  - `fresh_topic_generalization_gap=16%`
- القرار: `DESIGN_TOPIC_PROTOTYPE_CONTRASTIVE_COPY_ANCHOR_GATE_BEFORE_ANY_TRAINING`.
- التالي: Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate.
- المحظور الآن: runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage, وأي تدريب جديد قبل 27.102.
- التقارير:
  - [PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_REPORT.md](./PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_101_topic_binding_result_diagnosis_report.json`
  - `artifacts/reports/PHASE27_101_TOPIC_BINDING_RESULT_DIAGNOSIS_DECISION.json`

---

## Phase 27.102 — Topic Prototype Contrastive Copy-Anchor Gate

الحالة: **مكتملة كبوابة تصميم/ترميز فقط؛ لا تدريب ولا runtime.**

- المسار: `Sovereign Practical Acceleration Strategy v2`.
- السيادة: `SF-native only`; لا pretrained/open-weight/Qwen.
- القاموس/المسار: `Saudi Seed v1`, `msa + saudi`.
- الهدف: تثبيت metric لا يسمح لـ `required_topic_missing` بإخفاء
  wrong-topic substitution.
- البوابة الجديدة:
  - counted metric: `observed_wrong_topic_count`
  - threshold: `observed_wrong_topic_count == 0`
  - copy-anchor: الموضوع المطلوب داخل أول 12 حرفًا عربيًا ظاهرًا
  - canary prompts: `16`
- أعادت البوابة قراءة 27.100:
  - reported wrong-topic: `0`
  - observed wrong-topic: `8`
  - copy-anchor: `18/26`
  - substitutions: `الصداقة=7`, `الامتنان=1`
- القرار: `ALLOW_PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_NO_TRAINING`.
- التالي: Phase 27.103 — Topic Prototype Contrastive Curriculum Pack.
- المحظور الآن: runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage, وأي تدريب جديد قبل 27.103.
- التقارير:
  - [PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_REPORT.md](./PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_REPORT.md)
  - `artifacts/reports/phase27_102_topic_prototype_contrastive_gate_report.json`
  - `artifacts/reports/PHASE27_102_TOPIC_PROTOTYPE_CONTRASTIVE_GATE_DECISION.json`
  - `eval/prompts/phase27_102_topic_prototype_contrastive_canary.json`

---

## Phase 27.103 — Topic Prototype Contrastive Curriculum Pack

**الحالة:** مكتملة كحزمة بيانات/curriculum فقط. لا تدريب ولا runtime.

- أضيفت حزمة:
  `data/corpus/chat/jsonl/dialogue_batch_v12_topic_prototype_contrastive_012.jsonl`
- records: `192`
- التوزيع: `8` موضوعات × `2` لهجات (`msa`, `saudi`) × `12` سجلًا.
- الجودة: `gold=192`, المصدر محلي سيادي، `training_allowed=true`.
- corpus بعد الحزمة:
  - total: `8645`
  - dialects: `msa=4295`, `saudi=4350`
  - quality: `gold=3533`, `silver=5112`
  - split: `train=7777`, `eval=868`
- quality gates:
  - copy-anchor bad count: `0`
  - wrong-topic leak count: `0`
  - duplicate pair count: `0`
  - adjacent same-topic in curriculum schedule: `0`
- القرار: `ALLOW_PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_TRAINING`.
- التالي: Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training.
- المحظور الآن: runtime release, UI generator release, SF-50M,
  tokenizer retrain, pretrained/open-weight usage، وtemplate masking.
- التقارير:
  - [PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_REPORT.md](./PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_REPORT.md)
  - `artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_pack_report.json`
  - `artifacts/reports/PHASE27_103_TOPIC_PROTOTYPE_CONTRASTIVE_CURRICULUM_PACK_DECISION.json`
  - `artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_manifest.json`
  - `artifacts/reports/phase27_103_topic_prototype_contrastive_curriculum_schedule.json`

---

## Phase 27.104 — Bounded Topic Prototype Contrastive Repair Training

**الحالة:** مكتملة كتدريب محدود. لا runtime ولا UI generator release.

- التدريب بدأ من:
  `artifacts/eval/phase27_100_topic_binding_repair/checkpoints/sf-10m-step1800`
- استخدم view مؤقتًا مرتبًا من حزمة 27.103:
  `artifacts/eval/phase27_104_topic_prototype_contrastive_repair/curriculum_view/jsonl/phase27_103_schedule_view.jsonl`
- training config:
  - steps: `1200`
  - lr: `8e-05`
  - loss_scope: `assistant`
  - packing_mode: `sample_isolated`
- أفضل checkpoint: `sf-10m-step1200`
- النتيجة:
  - prototype canary: `16/16`
  - observed wrong-topic: `0`
  - known topic: `16/16`
  - fresh topic: `9/10`
  - topic family: `9/10`
  - all family: `30/50`
- القرار: `BLOCK_RUNTIME_DIAGNOSE_TOPIC_PROTOTYPE_REPAIR_RESULT`.
- السبب: إصلاح topic نجح، لكنه لم يمر all-family gate المطلوبة `45/50`.
- التالي التاريخي كان Phase 27.105، لكن أمر re-anchor الحالي يجعل التالي
  العملي Phase 27.80 المشروط ببوابات objective/curriculum/decoding.
- التقارير:
  - [PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_REPORT.md](./PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_REPORT.md)
  - `artifacts/reports/phase27_104_bounded_topic_prototype_contrastive_repair_report.json`
  - `artifacts/reports/PHASE27_104_BOUNDED_TOPIC_PROTOTYPE_CONTRASTIVE_REPAIR_DECISION.json`
  - `artifacts/samples/phase27_104_bounded_topic_prototype_contrastive_repair.md`

---

## Active Re-Anchor — Phase 27.79 Objective/Curriculum/Decoding Repair Plan

**الحالة:** المسار الحالي الحاكم بعد أمر سامي الصريح. لا يبدأ أي تدريب جديد
حتى تمر بوابات objective/curriculum/decoding.

- التقرير الملزم: [PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.md](./PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.md)
- JSON: `artifacts/reports/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.json`
- المسار: `SF-native Objective/Curriculum/Decoding Acceleration Track`.
- المصدر: نتيجة 27.104، حيث نجح topic binding لكن فشل all-family `30/50`.
- القرار التاريخي: `PLAN_READY_TRAINING_BLOCKED_UNTIL_GATES_PASS`.
- التدريب الجديد: اكتمل في Phase 27.81 بعد مرور بوابات 27.80.
- tokenizer retrain: محجوب.
- `SF-50M`: محجوب.
- runtime release: محجوب.
- نتيجة البوابات: مرّت في Phase 27.80 عبر
  `PHASE27_80_BOUNDED_FAMILY_CONDITIONED_REPAIR_GATE_DECISION`.
- نتيجة التدريب: اكتملت في Phase 27.81 عبر
  `PHASE27_81_BOUNDED_FAMILY_CONDITIONED_REPAIR_TRAINING_DECISION`.
- أضيف raw lab single-user لاختبار المولد مباشرة من الواجهة بدون قوالب.
- نتيجة Phase 27.105: المولد مؤكد أنه يجيب من `sf_10m_phase27_81`،
  لكنه يخلط social subfamilies ويفشل في بعض bare-topic/unknown-topic prompts.
- نتيجة Phase 27.106: أضيف renderer design لـ `نوع السوالف:
  تحية/سؤال حال/فتح سالفة/شكر/هوية/قدرات`، وأضيف topic variant canonical
  mapping مثل `الصداقه → الصداقة` و`الاخوه → الأخوة`.
- نتيجة Phase 27.107: مرّت gate التنفيذية، وأضيف canary من أسلوب اختبار
  الواجهة الخام، والتالي data pack لا training.
- التالي: Phase 27.108 — Social Subfamily + Topic Variant Data Pack.
- سبب الحجب: لا يزال `السلام عليكم` يعود كسالفة عامة، و`الاخوه` غير مغطاة،
  ولا يوجد family/subfamily objective كافٍ لتحية/هوية/قدرات/فتح سالفة.

---

## Phase 27.105 — Raw UI Lab Result Diagnosis

**الحالة:** مكتملة كتقييم حي غير تدريبي. raw lab يعمل للمستخدم المحلي فقط،
ولا يمثل إطلاقًا رسميًا.

- المولد المستخدم: `sf_10m_phase27_81`.
- checkpoint: `sf-10m-step2000`.
- نتيجة مباشرة:
  - `الصداقه` بعد normalization → رد صحيح عن الصداقة.
  - `نظم وقتي` → رد تنظيم بسيط.
  - `السلام عليكم` → فشل social subfamily، يرد بسالفة عامة.
  - `الاخوه` → غير مغطاة كموضوع، تنهار إلى general.
- إصلاح غير تدريبي:
  - bare known topics تُحوّل إلى `intent=definition`.
  - bare known topics تُمرّر للمولد بصيغة canonical مثل `الصداقة`.
  - `كيف الحال` تُعامل كـ smalltalk.
  - planning/support/advice لها أولوية قبل bare-topic detection.
- القرار: `PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_DECISION`.
- المحظور: training جديد، runtime release رسمي، SF-50M، tokenizer retrain،
  pretrained/open-weight، أو template masking.
- التقارير:
  - [PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_REPORT.md](./PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_REPORT.md)
  - `artifacts/reports/phase27_105_raw_ui_lab_result_diagnosis_report.json`
  - `artifacts/reports/PHASE27_105_RAW_UI_LAB_RESULT_DIAGNOSIS_DECISION.json`

---

## Phase 27.106 — Social Subfamily + Topic Variant Objective Design

**الحالة:** مكتملة كتصميم وتنفيذ renderer. لا تدريب ولا runtime release رسمي.

- أضيفت حقول provenance:
  - `dialogue_subfamily`
  - `topic_canonical`
  - `topic_variant`
- أضيف renderer line لعائلة السوالف:
  - `نوع السوالف: تحية`
  - `نوع السوالف: سؤال حال`
  - `نوع السوالف: فتح سالفة`
  - `نوع السوالف: شكر`
  - `نوع السوالف: هوية`
  - `نوع السوالف: قدرات`
- أضيف canonical mapping للموضوعات اليومية:
  - `الصداقه` → `الصداقة`
  - `الاخوه` → `الأخوة`
  - `الشجاعه` → `الشجاعة`
- القرار: `PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_DECISION`.
- التالي: Phase 27.107 — بوابة تتحقق من renderer/masking/canary قبل أي
  تدريب محدود.
- التقارير:
  - [PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_REPORT.md](./PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_REPORT.md)
  - `artifacts/reports/phase27_106_social_subfamily_topic_variant_design_report.json`
  - `artifacts/reports/PHASE27_106_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DESIGN_DECISION.json`

---

## Phase 27.107 — Social Subfamily + Topic Variant Gate Encoding

**الحالة:** مكتملة كبوابة تنفيذية. لا تدريب.

- gate status: `PHASE27_107_GATE_PASSED_DATA_PACK_ALLOWED_NO_TRAINING`.
- القرار: `PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_DECISION`.
- canary:
  `artifacts/reports/phase27_107_social_subfamily_topic_variant_canary.json`
- يغطي canary:
  - `السلام عليكم` → greeting.
  - `كيف الحال` → smalltalk.
  - `خلنا نسولف` → open_chat.
  - `من أنت` → identity.
  - `وش تقدر تسوي` → capability.
  - `الصداقه` → الصداقة.
  - `الاخوه` → الأخوة.
- التالي المسموح: Phase 27.108 data pack فقط.
- المحظور: training، runtime release رسمي، SF-50M، tokenizer retrain،
  pretrained/open-weight.
- التقارير:
  - [PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_REPORT.md](./PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_REPORT.md)
  - `artifacts/reports/phase27_107_social_subfamily_topic_variant_gate_report.json`
  - `artifacts/reports/PHASE27_107_SOCIAL_SUBFAMILY_TOPIC_VARIANT_GATE_DECISION.json`
  - `artifacts/reports/phase27_107_social_subfamily_topic_variant_canary.json`

---

## Phase 27.108 — Social Subfamily + Topic Variant Data Pack

**الحالة:** مكتملة كحزمة بيانات. لا تدريب.

- status: `PHASE27_108_DATA_PACK_READY_FOR_AUDIT_NO_TRAINING`.
- القرار: `PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION`.
- أضيفت `480` سجلًا gold:
  - `360` social subfamily records.
  - `120` topic variant records.
- التوازن:
  - `msa=240`
  - `saudi=240`
  - `30` سجلًا لكل social subfamily في كل لهجة.
  - `30` سجلًا لكل topic canonical في كل لهجة.
- الملفات:
  - `data/corpus/chat/jsonl/dialogue_batch_v14_social_subfamily_msa_014.jsonl`
  - `data/corpus/chat/jsonl/dialogue_batch_v14_social_subfamily_saudi_014.jsonl`
  - `data/corpus/chat/jsonl/dialogue_batch_v14_topic_variants_msa_014.jsonl`
  - `data/corpus/chat/jsonl/dialogue_batch_v14_topic_variants_saudi_014.jsonl`
- نتيجة `make corpus-audit`:
  - `total_records=9125`
  - `training_ready=9125`
  - `issues=0`
  - `gold=4013`
  - `silver=5112`
- التالي المسموح بعد حجب Qabas كـ reference-only: Phase 27.113 permissive lexical alternatives intake gate، بلا تدريب.
- المحظور: training، runtime release رسمي، SF-50M، tokenizer retrain،
  pretrained/open-weight.
- التقارير:
  - [PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_REPORT.md](./PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_REPORT.md)
  - `artifacts/reports/phase27_108_social_subfamily_topic_variant_data_pack_report.json`
  - `artifacts/reports/PHASE27_108_SOCIAL_SUBFAMILY_TOPIC_VARIANT_DATA_PACK_DECISION.json`

---

## Phase 27.109 — Free Linguistic Resource Intake Gate

**الحالة:** مكتملة كبوابة مصادر. لا تدريب ولا إدخال نصوص خارجية في corpus.

- status: `PHASE27_109_FREE_RESOURCE_INTAKE_READY_NO_TRAINING`.
- القرار: `PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION`.
- الهدف: اختصار الطريق بمصادر لغوية جاهزة ومجانية دون كسر السيادة.
- المرشحون:
  - `Masader`: فهرس metadata عربي، مسموح للاكتشاف والترخيص فقط.
  - `Qabas`: معجم عربي ضخم مرشح للكلمات/الموضوعات/protected terms.
  - `Tashkeela`: corpus فصيح مشكول مرشح بعد gate ترخيص وتنظيف.
  - `OSIAN`: مقيّد non-commercial، eval/vocabulary-only حتى قرار ترخيص.
  - `Arabic Learner Corpus`: مرشح لاستخراج أخطاء وتقييم robustness.
  - `fr3on Arabic Dialect Corpus`: مرشح vocabulary/eval للهجة بعد privacy/provenance gate.
  - `ArSyra`: محجوب حتى اختيار مسار ترخيص واضح.
- تم سحب metadata من Masader:
  - `resources/external_sources/masader_datasets_index_summary.json`
  - `file_count=1000`
  - لا نصوص تدريب خارجية دخلت `data/corpus`.
- الملفات:
  - `resources/external_sources/free_linguistic_resources_manifest.json`
  - `artifacts/reports/phase27_109_free_linguistic_resource_intake_gate_report.json`
  - `artifacts/reports/PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_DECISION.json`
  - [PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_REPORT.md](./PHASE27_109_FREE_LINGUISTIC_RESOURCE_INTAKE_GATE_REPORT.md)
- التالي: Phase 27.110 — Qabas/Masader/Tashkeela Licensed Ingestion Design.
- المحظور: external training text import، pretrained vocab، tokenizer merges،
  runtime release، SF-50M.

## Phase 27.110 — Licensed Ingestion Design

**الحالة:** مكتملة كبوابة تصميم. لا تدريب ولا إدخال نصوص خارجية في corpus.

- status: `PHASE27_110_LICENSED_INGESTION_DESIGN_READY_NO_TRAINING`.
- القرار: `PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION`.
- القرار الهندسي: `ALLOW_PHASE27_111_QABAS_LEXICON_BOOTSTRAP_NO_TRAINING`.
- الهدف: تحويل قائمة المصادر المجانية إلى lanes مرخّصة واضحة قبل أي سحب/تنظيف/تدريب.
- تم سحب metadata محلية مختارة من Masader لعشرة مصادر إلى:
  - `resources/external_sources/selected_masader_metadata/`
- نتيجة مصفوفة الترخيص:
  - `Qabas`: مسموح للمرحلة التالية كتصميم lexicon/topic/protected-terms فقط، وليس tokenizer vocab.
  - `Tashkeela`: محجوبة للتدريب حتى حل تعارض الترخيص بين metadata والورقة/المصدر الأساسي.
  - `Sadeed Tashkeela`: eval-only حتى مراجعة سلسلة الترخيص.
  - `SaudiNewsNet` و`OSIAN`: non-commercial، vocabulary/eval-only.
  - `Saudi Novel Corpus`: محجوب حتى معرفة الترخيص.
  - `Arabic Learner Corpus`: custom/with-fee، خارج free lane.
  - مصادر Twitter/telephone/open-domain dialect: محجوبة حتى privacy/provenance/license gates.
- الملفات:
  - `resources/external_sources/phase27_110_licensed_ingestion_design.json`
  - `resources/external_sources/phase27_110_license_matrix.json`
  - `resources/external_sources/selected_masader_metadata/`
  - `artifacts/reports/phase27_110_licensed_ingestion_design_report.json`
  - `artifacts/reports/PHASE27_110_LICENSED_INGESTION_DESIGN_DECISION.json`
  - [PHASE27_110_LICENSED_INGESTION_DESIGN_REPORT.md](./PHASE27_110_LICENSED_INGESTION_DESIGN_REPORT.md)
- التالي: Phase 27.111 — Qabas Lexicon Bootstrap Design, no training.
- المحظور: external training text import، pretrained vocab، tokenizer merges،
  runtime release، SF-50M، وإدخال أي مصدر غير مرخص في corpus.

## Phase 27.111 — Qabas Lexicon Bootstrap Design

**الحالة:** مكتملة كتصميم. لا import فعلي من Qabas ولا تدريب.

- status: `PHASE27_111_QABAS_BOOTSTRAP_DESIGN_READY_IMPORT_BLOCKED`.
- القرار: `PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION`.
- القرار الهندسي: `BLOCK_QABAS_IMPORT_ALLOW_PHASE27_112_LICENSE_RESOLUTION_GATE`.
- الهدف: تصميم كيف نستفيد من Qabas لاحقًا كـ lexicon/topic/protected-terms
  دون تحويله إلى tokenizer vocab جاهز أو corpus تدريبي.
- نتيجة التحقق:
  - Masader metadata تعرض Qabas بترخيص `Apache-1.0`.
  - صفحة SinaLab resources تعرض Qabas بترخيص `CC-BY-ND-4.0`.
  - لهذا السبب حُظر إدخال أي raw Qabas entries حتى Phase 27.112.
- المسموح الآن:
  - source card.
  - field mapping design.
  - dedupe/quality/license gates.
  - placeholder فقط في `resources/lexicons/imported/qabas_bootstrap/README.md`.
- الممنوع الآن:
  - إدخال `qabas*.jsonl` في `data/corpus`.
  - إدخال Qabas كـ tokenizer vocab أو merges.
  - إنشاء candidate terms/topics فعلية قبل حل الترخيص.
  - training/runtime release/SF-50M.
- الملفات:
  - `resources/external_sources/qabas_source_card_phase27_111.json`
  - `resources/external_sources/phase27_111_qabas_lexicon_bootstrap_design.json`
  - `resources/lexicons/imported/qabas_bootstrap/README.md`
  - `artifacts/reports/phase27_111_qabas_lexicon_bootstrap_design_report.json`
  - `artifacts/reports/PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_DECISION.json`
  - [PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_REPORT.md](./PHASE27_111_QABAS_LEXICON_BOOTSTRAP_DESIGN_REPORT.md)
- التالي: Phase 27.112 — Qabas Primary License Resolution Gate, no training.

## Phase 27.112 — Qabas Primary License Resolution Gate

**الحالة:** مكتملة كبوابة ترخيص. Qabas reference-only؛ لا import ولا تدريب.

- status: `PHASE27_112_QABAS_REFERENCE_ONLY_IMPORT_BLOCKED`.
- القرار: `PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION`.
- القرار الهندسي: `BLOCK_QABAS_IMPORT_REFERENCE_ONLY_OPEN_PHASE27_113_PERMISSIVE_LEXICAL_ALTERNATIVES`.
- الأدلة:
  - Masader metadata تعرض `Apache-1.0`.
  - صفحة SinaLab resources الأساسية تعرض Qabas بترخيص `CC-BY-ND-4.0`.
  - صفحة Qabas/About لا تعرض رخصة artifact قابلة للحسم.
- نتيجة الحسم:
  - `no_derivatives_detected=true`.
  - `license_conflict_unresolved=true`.
  - `qabas_raw_entry_import_allowed=false`.
  - `qabas_reference_only_allowed=true`.
- المسموح:
  - استخدام Qabas كمرجع metadata/source-discovery فقط.
  - الاستفادة من معرفة وجوده لاختيار بدائل مرخصة بوضوح.
- الممنوع:
  - raw Qabas entries.
  - أي `qabas*.jsonl` داخل `data/corpus`.
  - Qabas كـ tokenizer vocab أو merges.
  - training/runtime release/SF-50M.
- الملفات:
  - `resources/external_sources/phase27_112_qabas_license_evidence.json`
  - `artifacts/reports/phase27_112_qabas_primary_license_resolution_gate_report.json`
  - `artifacts/reports/PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_DECISION.json`
  - [PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_REPORT.md](./PHASE27_112_QABAS_PRIMARY_LICENSE_RESOLUTION_GATE_REPORT.md)
- التالي: Phase 27.113 — Permissive Lexical Alternatives Intake Gate, no training.

---

## بروتوكول الانتقال

التفويض الحالي من سامي: استمر في المراحل المسجلة دون انتظار موافقات جديدة، مع توثيق رقم الرحلة، القاموس المتبع، نتائج الاختبارات، وفحص الحساسية قبل أي رفع.
