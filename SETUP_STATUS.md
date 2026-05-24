# SETUP_STATUS.md

## SF.AI — حالة الإعداد

هذا الملف يصف حالة الإعداد العامة للمشروع: الملفات الموجودة، الأدوات المطلوبة، وما لم يُجهَّز بعد.

---

## الحالة العامة

- **اسم المشروع:** SF.AI
- **الموقع:** `/Users/sami/workSF/SF.AI/`
- **الرحلة الحالية:** **Phase 27.93 / 30**
- **المرحلة الحالية:** **Phase 27.93 — Topic Objective Gate Encoding and Dry-Run Validation** (`PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION`; لا تدريب؛ runtime محجوب)
- **الهدف العام:** الوصول إلى نموذج لغوي سيادي مولّد، يبدأ من الصفر، ثم يربط توليده بالشات خلف router/safety/composer.
- **ملف القيادة الواحد:** `docs/SF_AI_MASTER_GUIDE.md` هو نقطة الدخول الأولى لأي Agent أو مهندس؛ بقية الملفات مراجع تفصيلية.
- **المرحلة التالية المقترحة:** Phase 27.94 — Topic Objective Data Pack Authoring؛ لا تدريب جديد قبل سد فجوة `الوفاء` السعودية.
- **استراتيجية العمل الملزمة:** Sovereign Practical Acceleration Strategy v2؛ `ENGINEERING_ROOT_CAUSE_GATE` قبل أي تدريب، و`NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS` قبل أي runtime.
- **تصحيح السيادة:** لا يوجد Open-Weight Lane؛ Qwen/open-weight/pretrained
  runtime ملغى وغير معتمد. التسريع السيادي = أدوات هندسية فقط داخل SF-native.
- **تفويض التكبير:** Auto-Advance Scaling Mandate؛ عند نجاح gate الحجم التالي ينتقل الوكيل تلقائيًا عبر `SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+`.
- **أدوات التسريع المحملة:** `tensorboard`, `tqdm`, `psutil`, `safetensors`, `rich` إضافة إلى `torch/numpy`; لا أوزان جاهزة ولا APIs خارجية.
- **القاموس/المسار اللغوي المتبع:** العربية الفصحى + اللهجة السعودية فقط؛ `Saudi Seed v1` مرجع خاص، و`safety_terms.yaml` محدث لفجوات المال/الدين/الأمن.
- **نتيجة Phase 12:** tokenizer v1 محفوظ في `artifacts/tokenizers/sf_bpe/v1/`، `vocab=261`, `merges=218`, `sf_origin=true`.
- **نتيجة Phase 13:** smoke training نجح: `loss 5.6638 → 4.7539`, checkpoint محلي في `artifacts/checkpoints/smoke_lm/sf-10m-step20`, وتقرير في `docs/PHASE13_SMOKE_TRAINING_REPORT.md`.
- **نتيجة Phase 14:** SF-10M v0.1 محدود نجح: `33/80` خطوة بسبب صغر corpus، eval loss `4.0777`, perplexity `59.01`, وتقرير في `docs/PHASE14_SF10M_V0_1_REPORT.md`.
- **نتيجة Phase 15:** أضيف `NativeGenerator` + `GenerationPolicy` + metadata في API/UI، لكن هذا adapter فقط؛ `SF-10M v0.1` خام وغير جاهز كحوار مقنع.
- **نتيجة Phase 16:** `make eval-phase16` نجح: `15/15`; التقرير يثبت أن النموذج خام ومكرر، والمختبر المحلي يبقى مفتوحًا للقياس.
- **نتيجة Phase 17:** أضيف `ChatRagBridge` و`ContextBuilder`; الشات يستطيع استخدام snippets محلية عند حقن `HybridRetriever`، ويعرض `rag=used/not_used`.
- **نتيجة Phase 18:** أضيف زر تصدير مراجعة من واجهة الشات + `scripts/prepare_dialogue_batch.py` + تقرير `artifacts/reports/dialogue_batch_report.json`; لا تدخل محادثات المستخدم إلى التدريب تلقائيًا.
- **حماية Phase 18:** ملفات `data/corpus/**/review/*.jsonl` مستثناة من git افتراضيًا؛ العينة الآمنة الوحيدة المسموحة هي `sample_review_export.jsonl`.
- **نتيجة Phase 19:** أضيفت بوابة `make phase19-readiness` و`GET /system/phase19-readiness`; القرار الحالي `NOT_READY_EXPAND_CORPUS_FIRST` لأن corpus الحالي 500 سجل فقط والحد الأدنى العملي 5000.
- **نتيجة Phase 20:** أضيفت بوابة `make phase20-gates` و`GET /system/phase20-gates`; لا مجال يتفعل تلقائيًا، و`chat` هو المجال النشط الوحيد.
- **تصحيح Phase 20:** أضيف `sf_ai/modules/productivity/` كسكيلتون كامل بعد أن كشفت البوابة وجوده في registry دون module/manifest.
- **نتيجة Phase 21:** أضيف `docs/GENERATIVE_ROADMAP.md` ومُدّدت الخطة إلى Phase 30؛ أول تدريب جودة مفيد اكتمل في Phase 24 بحدود، وأول هدف حوار مولّد مقنع صار مشروطًا بتنفيذ خطة Phase 27 ثم نجاح `SF-50M`.
- **مبدأ التكبير الرسمي:** `Progressive Scaling Strategy` — لا يتم رفع حجم النموذج إلا بعد نجاح المرحلة الحالية، والسلم الرسمي هو `SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+`.
- **نتيجة Phase 22:** أضيف `make phase22-readiness` و`make phase22-plan` و`make phase22-next-batch` و`make phase22-completion-gate` و`make phase22-review-intake` و`GET /system/phase22-readiness` و`GET /system/phase22-collection-plan` و`GET /system/phase22-next-batch` و`GET /system/phase22-completion-gate` و`GET /system/phase22-review-intake`; القرار الحالي `READY_FOR_PHASE23_TOKENIZER_V2` لأن corpus الحالي اكتمل 500/500. التوازن النهائي مكتمل: `msa=250`, `saudi=250`.
- **بوابة اكتمال Phase 22:** `make phase22-completion-gate` يرجع الآن `PHASE22_COMPLETE_READY_FOR_PHASE23`، ولا توجد نواقص تمنع الانتقال إلى Phase 23.
- **نتيجة Phase 23:** أضيف `artifacts/tokenizers/sf_bpe/v2/` و`make phase23-tokenizer-audit` و`GET /system/phase23-tokenizer-audit`; القرار الحالي `COMPLETED_READY_FOR_PHASE24`. v2: `vocab=4493`, `merges=4386`, `words_seen=23190`, `unique_words=2492`.
- **نتيجة Phase 24:** دُرّب `SF-10M v0.2` على tokenizer v2 وcorpus المتوازن 2000 خطوة: loss `8.4751 → 2.8256`, eval loss `2.5779`, perplexity `13.17`. القرار `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`: تحسن رقميًا لكنه لا يزال غير صالح للرد الواسع في الواجهة.
- **تقرير Phase 24:** `docs/PHASE24_SF10M_V0_2_REPORT.md`, `artifacts/reports/sf_10m_v0_2_training_report.json`, `artifacts/samples/sf_10m_v0_2_generations.md`.
- **Checkpoint Phase 24 المحلي:** `artifacts/checkpoints/sf_10m_v0_2/sf-10m-step2000`; ملفات checkpoints مستثناة من git حسب السياسة.
- **نتيجة Phase 25:** أضيف `GenerationGuard` وفلاغ `SF_GENERATOR_CANARY` ومسار `sf_10m_v0_2` guarded. التجربة الحقيقية حُجبت بـ `generation_guard:malformed_token` ورجع الرد إلى `template`. القرار `COMPLETED_GUARDED_CANARY_REAL_MODEL_BLOCKED`.
- **تقرير Phase 25:** `docs/PHASE25_GENERATED_CHAT_CANARY_REPORT.md`, `artifacts/reports/phase25_generation_canary_report.json`.
- **نتيجة Phase 26:** أضيفت بوابة `make phase26-readiness` و`GET /system/phase26-readiness`. القرار `NOT_READY_IMPROVE_SF10M_AND_CANARY`: لا تدريب `SF-50M` الآن؛ corpus الحالي بعد تنظيف الحوارات التشغيلية صار `5143` والحد العملي `5000`، وPhase 25 حجب النموذج الحقيقي، وruntime quality/hallucination/repetition gates غير ناجحة.
- **تقرير Phase 26:** `docs/PHASE26_SF50M_READINESS_REPORT.md`, `artifacts/reports/phase26_sf50m_readiness_report.json`.
- **نتيجة Phase 27:** أضيف `make phase27-dialogue-eval` و`GET /system/phase27-dialogue-eval`. suite متعدد الأدوار نجح `19/19`، لكنه أثبت أن الردود الحالية `template` وليست مولدًا مفتوحًا. بعد الدفعات الطبيعية وصل corpus إلى `5143`، والمتبقي إلى حد `5000` هو `0`.
- **تقرير Phase 27:** `docs/PHASE27_DIALOGUE_EVAL_V2_REPORT.md`, `eval/reports/dialogue_eval_v2.json`, `artifacts/reports/phase27_dialogue_eval_v2_report.json`.
- **دفعات توسعة Phase 27:** أضيف Batch 001 بإجمالي 50 سجلًا، ثم Batch 002 وBatch 003 الكبيرتان بإجمالي 1000 سجل، كل واحدة `250` فصيح + `250` سعودي. corpus الحالي صار `5143`: `msa=2549`, `saudi=2594`, والمتبقي إلى `5000` صار `0` سجلًا.
- **نتيجة Phase 27.5:** أضيف بث حواري كامل في `ChatDataset.iter_dialogue_texts()`، وأصبح `train_tiny_lm` يستخدم `--stream-format dialogue` افتراضيًا. دُرّب `SF-10M v0.4` على `5143` سجلًا، training loss `8.4662 → 1.4070`, eval loss `5.8267`, perplexity `339.24`. القرار `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`: النموذج تعلم الأدوار أفضل لكنه لا يرد بعد بجودة واجهة.
- **تقرير Phase 27.5:** `docs/PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md`, `artifacts/reports/sf_10m_v0_4_dialogue_format_report.json`, `artifacts/samples/sf_10m_v0_4_generations.md`.
- **نتيجة Phase 27.6:** أضيف `--loss-scope assistant` إلى التدريب والتقييم، ودُرّب `SF-10M v0.5` على رد المساعد فقط. training loss `8.4643 → 2.3513`, أفضل eval مقاس step2000: loss `6.5718`, perplexity `714.65`. القرار `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED`: الردود لا تزال مكررة وغير جاهزة للواجهة.
- **تقرير Phase 27.6:** `docs/PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md`, `artifacts/reports/sf_10m_v0_5_assistant_target_report.json`, `artifacts/samples/sf_10m_v0_5_generations.md`.
- **نتيجة Phase 27.7:** أضيف split ثابت `data/corpus/chat/splits/dialogue_split_v1.json` بعدد `train=4703` و`eval=540`، وأضيفت دفعة gold social من 100 سجل، وأصبح corpus `5243` (`msa=2599`, `saudi=2644`) بلا issues. أضيف canary prompt-aware لمنع الردود العربية الشكلية غير المتصلة بالسؤال. لا تدريب جديد في هذه المرحلة، وruntime المولّد لا يزال blocked.
- **تقرير Phase 27.7:** `docs/PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md`, `artifacts/reports/phase27_7_fixed_split_gold_social_canary_report.json`.
- **نتيجة Phase 27.8:** دُرّب `SF-10M v0.6` على `train split=4703` وقيس على `eval split=540`. أفضل eval: `step4000 loss=5.0227`, `perplexity=151.82`. canary حجب `10/10` عينات بسبب fragments مشوهة، لذلك runtime المولّد لا يزال blocked ولا يبدأ `SF-50M`.
- **تقرير Phase 27.8:** `docs/PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md`, `artifacts/reports/sf_10m_v0_6_split_training_report.json`, `artifacts/samples/sf_10m_v0_6_generations.md`.
- **نتيجة Phase 27.9:** أضيف `make phase27-generation-quality` وprompt suite `eval/prompts/generation_quality_v1.json`. نتيجة v0.6: `0/10` prompts passed، و`runtime_allowed=false` بسبب `model_artifact_fragment`.
- **تقرير Phase 27.9:** `docs/PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md`, `eval/reports/generation_quality_v1.json`, `artifacts/reports/generation_quality_v1_report.json`.
- **نتيجة Phase 27.10:** أضيفت دفعة short-response repair بعدد `300` سجل gold (`150` فصيح + `150` سعودي)، وأصبح corpus `5543` (`msa=2749`, `saudi=2794`, `gold=431`). دُرّب `SF-10M v0.7`: أفضل eval `loss=4.7512`, `perplexity=115.72`، لكن generation-quality بقي `0/10` بعد تشديد الحارس.
- **تقرير Phase 27.10:** `docs/PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md`, `artifacts/reports/sf_10m_v0_7_short_repair_report.json`, `artifacts/samples/sf_10m_v0_7_generations.md`.
- **نتيجة Phase 27.11:** شُغّل gold overfit probe على `16` ردًا قصيرًا (`msa=8`, `saudi=8`). وصل loss إلى شبه صفر، لكن clean-stop بقي `0/16`: `guard:repetition=6`, `overgenerates_after_expected=10`.
- **تقرير Phase 27.11:** `docs/PHASE27_11_OBJECTIVE_PROBE_REPORT.md`, `artifacts/reports/phase27_11_objective_probe_report.json`, `artifacts/samples/phase27_11_objective_probe_generations.md`.
- **نتيجة Phase 27.12:** أضيف `<eos>` كهدف نهاية رد مساعد، وdialect conditioning (`النطاق: فصحى/سعودي`). probe الحالي: `semantic_clean_pass=5/16`, `guard_pass=9/16`; لا تفعيل ولا SF-50M.
- **تقرير Phase 27.12:** `docs/PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md`, `artifacts/reports/phase27_12_eos_probe_report.json`, `artifacts/samples/phase27_12_eos_probe_generations.md`.
- **نتيجة Phase 27.13:** دُرّب `SF-10M v0.8` 6000 خطوة على split التدريب بصيغة boundary/EOS + dialect conditioning. أفضل eval: `loss=3.1875`, `perplexity=24.23`; generation-quality الصارم `3/10`, وruntime لا يزال محظورًا.
- **تقرير Phase 27.13:** `docs/PHASE27_13_SF10M_V08_REPORT.md`, `artifacts/reports/sf_10m_v0_8_boundary_eos_training_report.json`, `artifacts/reports/generation_quality_v1_v0_8_report.json`.
- **نتيجة Phase 27.14:** اعتُمدت أدوات جودة التدريب السيادية رسميًا: EOS/boundaries، sequence packing، local experiment tracker، data quality scanner، curriculum sampler، no-repeat controls، gold probes، checkpoint selector، local logs، tokenizer boundary audit. لا تدريب جديد ولا تفعيل runtime.
- **تقرير Phase 27.14:** `docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md`, `artifacts/reports/phase27_14_quality_tooling_decision_report.json`, `artifacts/reports/experiment_registry.jsonl`.
- **نتيجة Phase 27.15:** أضيفت 400 عينة gold اجتماعية/لغوية (`msa=200`, `saudi=200`) وno-repeat decoding. corpus صار `5943` بلا issues. دُرّب `SF-10M v0.10`: أفضل eval `loss=3.0452`, `perplexity=21.01`; canary الدلالي الصارم `0/10`, وruntime محظور.
- **تقرير Phase 27.15:** `docs/PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md`, `artifacts/reports/sf_10m_v0_10_social_lexical_curriculum_report.json`, `artifacts/reports/generation_quality_v1_v0_10_strict_report.json`.
- **نتيجة Phase 27.16:** أضيف `--packing-mode sample_isolated` إلى التدريب والتقييم لمنع عبور عينات الحوار داخل نفس نافذة causal context. دُرّب `SF-10M v0.11`: أفضل eval `loss=4.0573`, `perplexity=57.82`; canary: `step2000=2/10`, `step6000=0/10`, وruntime محظور.
- **تقرير Phase 27.16:** `docs/PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md`, `artifacts/reports/sf_10m_v0_11_sample_isolated_objective_report.json`, `artifacts/reports/generation_quality_v1_v0_11_step2000_report.json`, `artifacts/reports/generation_quality_v1_v0_11_step6000_report.json`.
- **نتيجة Phase 27.17:** شُغّل prompt-to-answer micro-probe على `32` زوجًا داخليًا (`msa=16`, `saudi=16`) داخل `artifacts/eval`. النتيجة: `passed=27/32`, `exact_clean=28/32`, `semantic=29/32`, `guard_passed=29/32`. القرار: breakthrough جزئي لكن runtime و`SF-50M` محظوران بسبب كسور لفظية.
- **تقرير Phase 27.17:** `docs/PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md`, `artifacts/reports/phase27_17_prompt_answer_micro_probe_report.json`, `artifacts/samples/phase27_17_prompt_answer_micro_probe_generations.md`.
- **نتيجة Phase 27.18:** أضيف hygiene audit لمصطلحات فشل 27.17 وحجب الكسور المرصودة. النتيجة: `terms_total=26`, `average_pieces=3.5385`, `aggressive_split_terms=5`, `roundtrip_failures=0`, `uncovered_bad_fragments=0`. القرار: runtime و`SF-50M` محظوران.
- **تقرير Phase 27.18:** `docs/PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md`, `artifacts/reports/phase27_18_tokenization_hygiene_report.json`.
- **نتيجة Phase 27.19:** أضيف repair probe مركز حول العبارات الخمس ودُرّب على `52` مثالًا داخليًا (`32` أساس + `20` repair). النتيجة بقيت `passed=27/32`, `exact_clean=28/32`, `semantic=28/32`, `guard_passed=29/32`. القرار: runtime و`SF-50M` محظوران.
- **تقرير Phase 27.19:** `docs/PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md`, `artifacts/reports/phase27_19_hygiene_repair_probe_report.json`, `artifacts/samples/phase27_19_hygiene_repair_probe_generations.md`.
- **نتيجة Phase 27.20:** أضيف دعم protected phrases داخل tokenizer نفسه، وأضيف `resources/tokenization/protected_phrases_phase27_20.txt`. العبارات الخمس انتقلت في strategy من `max_pieces=8` إلى `max_pieces=1` مع `all_roundtrip_ok=true`. القرار: runtime و`SF-50M` محظوران حتى tokenizer v3 + micro-probe.
- **تقرير Phase 27.20:** `docs/PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md`, `artifacts/reports/phase27_20_tokenizer_strategy_report.json`.
- **نتيجة Phase 27.21:** دُرّب tokenizer v3 (`vocab=4706`, `merges=4648`, `sf_origin=true`) وشُغّل micro-probe. النتيجة: `passed=25/32`, `exact_clean=26/32`, `semantic=30/32`, `guard_passed=31/32`. القرار: runtime و`SF-50M` محظوران.
- **تقرير Phase 27.21:** `docs/PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md`, `artifacts/reports/phase27_21_tokenizer_v3_micro_probe_report.json`, `artifacts/samples/phase27_21_tokenizer_v3_micro_probe_generations.md`.
- **نتيجة Phase 27.22:** أُصلح decode boundary بعد protected phrases وأزيل false-positive في guard. النتيجة تحسنت إلى `passed=29/32`, `exact_clean=29/32`, `semantic=30/32`, `guard_passed=32/32`, و`glued_left=0`. القرار: runtime و`SF-50M` محظوران.
- **تقرير Phase 27.22:** `docs/PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md`, `artifacts/reports/phase27_22_spacing_boundary_repair_report.json`, `artifacts/samples/phase27_22_spacing_boundary_repair_generations.md`.
- **نتيجة Phase 27.23:** أضيف semantic/lexical repair متوازن على tokenizer v3. النتيجة تحسنت إلى `passed=30/32`, `exact_clean=30/32`, `semantic=30/32`, `guard_passed=31/32`. بقي خللان lexical في `التعاون` و`الاحترام`. القرار: runtime و`SF-50M` محظوران.
- **تقرير Phase 27.23:** `docs/PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md`, `artifacts/reports/phase27_23_semantic_lexical_repair_report.json`, `artifacts/samples/phase27_23_semantic_lexical_repair_generations.md`.
- **نتيجة Phase 27.24:** أضيف tokenizer محدود `v4_min_lexical` لحماية `التعاون` و`الاحترام`. النتيجة وصلت إلى `passed=32/32`, `exact_clean=32/32`, `semantic=32/32`, `guard_passed=32/32`. القرار: runtime و`SF-50M` محظوران حتى canary أوسع.
- **تقرير Phase 27.24:** `docs/PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md`, `artifacts/reports/phase27_24_minimal_lexical_stabilization_report.json`, `artifacts/samples/phase27_24_minimal_lexical_stabilization_generations.md`.
- **نتيجة Phase 27.25:** شُغّل held-out generation canary على `16` prompt جديدًا دون تدريب. النتيجة `passed=8/16`, `semantic=8/16`, `guard_passed=15/16`. القرار: `FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME`؛ runtime و`SF-50M` محظوران.
- **تقرير Phase 27.25:** `docs/PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md`, `artifacts/reports/phase27_25_heldout_generation_canary_report.json`, `artifacts/samples/phase27_25_heldout_generation_canary_generations.md`.
- **نتيجة Phase 27.26–27.30:** أضيفت repair سلسلة للتعميم: 27.26 وصل `9/16`, 27.27 جعل held-out القديم `16/16` لكن shadow `9/16`, 27.28 رفع shadow إلى `12/16`, 27.29 أضاف topic conditioning لكنه حُجب بسبب leakage, و27.30 fresh mixed shadow أعطى `16/18`. القرار: runtime محظور.
- **تقرير Phase 27.26–27.30:** `docs/PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md`, وتقارير JSON لكل مرحلة داخل `artifacts/reports/`.
- **نتيجة Phase 27.31–27.33:** 27.31 أضاف natural intent/topic data ومرّر `natural_shadow=20/20` لكنه بقي محجوبًا. 27.32 أضاف balanced calibration ومرّر `calibration=12/12` لكنه بقي محجوبًا. 27.33 أضاف advice + micro stabilization ومرّر كل البوابات: `heldout=16/16`, `shadow=16/16`, `definition=6/6`, `fresh_mixed=18/18`, `natural=20/20`, `calibration=12/12`, `advice=4/4`, `micro=32/32`, بلا prompt leakage. القرار: جاهز لتصميم guarded runtime trial.
- **تقرير Phase 27.31–27.33:** `docs/PHASE27_31_TO_33_GENERATION_GATE_REPORT.md`, وتقارير JSON لكل مرحلة داخل `artifacts/reports/`.
- **نتيجة Phase 27.34:** أضيف `generator_trial=true` إلى `/chat/message` وزر `مولّد تجريبي` في `/ui/chat`. بوابة runtime المحروس مرّت `9/9` باستخدام `sf_10m_phase27_33` مع fallback للقالب، وبقيت الهوية والمجالات الحساسة على المسار الآمن.
- **تقرير Phase 27.34:** `docs/PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md`, `artifacts/reports/phase27_34_guarded_runtime_trial_report.json`.
- **نتيجة Phase 27.35:** اختبار حي على `/ui/chat` و`/chat/message` مرّ `10/10`: `ui_passed=true`, ردود المولّد `7/7`, تحكم template/safety `3/3`.
- **تقرير Phase 27.35:** `docs/PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md`, `artifacts/reports/phase27_35_live_ui_trial_observations_report.json`.
- **نتيجة Phase 27.36:** أضيف quality-floor للتجربة الحية: raw `chat.general` وموضوعات التعريف غير المثبتة لا تذهب للمولّد. triage الحي مرّ `27/27`: `18/18` مولّد، `5/5` quality-floor، `4/4` ضوابط.
- **تقرير Phase 27.36:** `docs/PHASE27_36_LIVE_UI_TRIAGE_REPORT.md`, `artifacts/reports/phase27_36_live_ui_triage_report.json`.
- **نتيجة Phase 27.37:** أضيف semantic topic guard وفتح موضوع `الصبر` بصيغ مثبتة فقط. التوسعة الحية مرّت `21/21`: `10/10` regression generated، `3/3` موضوع جديد، `5/5` quality-floor، `3/3` ضوابط.
- **تقرير Phase 27.37:** `docs/PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md`, `artifacts/reports/phase27_37_supported_topic_expansion_report.json`.
- **نتيجة Phase 27.38:** دُرّب probe مستهدف للموضوعات المحجوبة (`الصداقة/الصدق/التنظيم/الهدوء`) لكنه مرّ `6/20` فقط وظهر topic collapse نحو `الاحترام`. القرار: لا runtime switch.
- **تقرير Phase 27.38:** `docs/PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md`, `artifacts/reports/phase27_38_targeted_topic_curriculum_probe_report.json`.
- **نتيجة Phase 27.39:** دُرّب topic-isolation probe متوازن للموضوعات الثمانية. النتيجة `10/24`: تحسن جزئي، لكن بقيت كسور لفظية وتداخل محدود. القرار: لا runtime switch.
- **تقرير Phase 27.39:** `docs/PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md`, `artifacts/reports/phase27_39_topic_isolation_repair_report.json`.
- **نتيجة Phase 27.40:** أُنشئ tokenizer v5 في `artifacts/tokenizers/sf_bpe/v5_topic_terms`، ومرّ tokenizer/context probe `24/24` مع `max_pieces=1`. القرار: جاهز لتصميم فتح محروس، لا فتح تلقائي.
- **تقرير Phase 27.40:** `docs/PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md`, `artifacts/reports/phase27_40_tokenizer_context_repair_report.json`.
- **نتيجة Phase 27.41:** فُتح مرشح `sf_10m_phase27_40` اختياريًا داخل `generator_trial=true` فقط، ومرّت بوابة HTTP الحية `22/22`: `17/17` رد مولّد و`5/5` ضوابط template/safety. الافتراضي ما زال `template`.
- **تقرير Phase 27.41:** `docs/PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md`, `artifacts/reports/phase27_41_guarded_runtime_switch_report.json`.
- **نتيجة Phase 27.42:** وُسّعت probes الحية إلى `29/29`: المولد نجح في المسارات المثبتة، والحارس حجب ردودًا غير مطابقة مثل سؤال الحال/التخطيط وأعادها للقالب.
- **تقرير Phase 27.42:** `docs/PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md`, `artifacts/reports/phase27_42_live_ui_broader_probes_report.json`.
- **نتيجة Phase 27.43:** دُرّب مرشح weak-lane جديد `sf_10m_phase27_43` لكنه مرّ `10/16` فقط؛ القرار: لا runtime switch، وتبقى الواجهة على `sf_10m_phase27_40`.
- **تقرير Phase 27.43:** `docs/PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md`, `artifacts/reports/phase27_43_guarded_data_backed_expansion_report.json`.
- **نتيجة Phase 27.44–27.48:** أُنشئ tokenizer v6، ثم أُصلح conditioning لموضوعي `الوفاء/الشجاعة`. مرّ `sf_10m_phase27_47` offline `16/16` ثم live API `19/19`. زر `مولّد تجريبي` يستخدمه الآن، والافتراضي ما زال `template`.
- **تقرير Phase 27.44–27.48:** `docs/PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md`, `artifacts/reports/phase27_48_guarded_runtime_switch_report.json`.
- **نتيجة Phase 27.49:** وُسّعت probes الحية إلى `33/33`، وأُصلح كشف النصيحة لعبارة `وش تنصحني اسوي`.
- **تقرير Phase 27.49:** `docs/PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md`, `artifacts/reports/phase27_49_broader_live_ui_probes_report.json`.
- **نتيجة Phase 27.50:** تحولت الواجهة و`/chat/message` إلى generator-only lab: `7/7`، لا قوالب ظاهرة. غير المدعوم يرجع `generator_blocked` مع `response=""`.
- **تقرير Phase 27.50:** `docs/PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md`, `artifacts/reports/phase27_50_generator_only_ui_gate_report.json`.
- **نتيجة Phase 27.89:** أضيف ترتيب `--split-order family_round_robin` ومرّ dry-run: أول `1800` عينة موزعة `360` لكل عائلة، وكل نافذة `600` فيها `120` لكل عائلة.
- **نتيجة Phase 27.90:** تدريب SF-10M محدود بالـ round-robin رفع fresh shadow إلى `35/50`، لكنه لم يمر runtime لأن topic بقي `1/10`.
- **نتيجة Phase 27.91:** شُخص الفشل المتبقي: `topic=9/15` من الإخفاقات، و`topic_semantic_collapse=48%`; لا SF-50M لأن capacity وزنها `4%` فقط في هذا التشخيص.
- **نتيجة Phase 27.92:** صُمم إصلاح `topic_anchor_prompt_to_answer_objective_v1` لعائلة `topic` مع شرط `الموضوع المطلوب: <topic_term>` وبوابات `18/20`, `16/20`, `45/50`; القرار يسمح بترميز Phase 27.93 فقط، ولا يسمح بتدريب أو runtime.
- **تقرير Phase 27.92:** `docs/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_GATE_REPORT.md`, `artifacts/reports/phase27_92_topic_objective_repair_design_gate_report.json`, `artifacts/reports/PHASE27_92_TOPIC_OBJECTIVE_REPAIR_DESIGN_DECISION.json`, `artifacts/reports/phase27_92_topic_objective_repair_spec.json`.
- **نتيجة Phase 27.93:** أضيف سطر renderer `الموضوع المطلوب: <topic_term>` لعائلة `topic` فقط، ومرّ dry-run للـ renderer/masking/canary. التدريب بقي محجوبًا لأن `الوفاء` ناقص سعوديًا (`saudi_shortfall=10`, `total_shortfall=8`).
- **تقرير Phase 27.93:** `docs/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_REPORT.md`, `artifacts/reports/phase27_93_topic_objective_gate_encoding_report.json`, `artifacts/reports/PHASE27_93_TOPIC_OBJECTIVE_GATE_ENCODING_DECISION.json`, `eval/prompts/phase27_93_topic_objective_canary.json`.
- **مقارنة tokenizer v1/v2:** v1 كان `vocab=261`, `merges=218`, `words_seen=723`, سعودي فقط. v2 تدرب على `500` سجل متوازن: `msa=250`, `saudi=250`.
- **تحسن protected Saudi terms:** `average_tokens` انخفض من `4.0` في v1 إلى `2.3` في v2، ولا توجد `roundtrip_failures` أو `aggressive_split_terms`.
- **خطة batches الدقيقة:** `make phase22-plan` يعرض الآن `planned_batches=[]` لأن الجمع اكتمل.
- **مهمة batch التالية:** `make phase22-next-batch` يعرض الآن `NO_BATCHES_REMAINING_RECHECK_READINESS`; لا توجد دفعة أخرى داخل Phase 22.
- **دفعات فصحى معتمدة:** أضيف `data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl` بإجمالي 178 سجل فصيح `silver` مؤلفة/مراجعة بتفويض سامي، مع بطاقات provenance.
- **دفعات سعودية معتمدة:** أضيف `data/corpus/chat/jsonl/dialogue_batch_v2_saudi_001.jsonl` إلى `dialogue_batch_v2_saudi_007.jsonl` بإجمالي 170 سجلًا سعوديًا `silver` مؤلفة/مراجعة بتفويض سامي، وبذلك اكتمل حد السعودي مع seed/protected coverage إلى 200/200.
- **دفعات مرنة معتمدة:** أضيف `data/corpus/chat/jsonl/dialogue_batch_v2_flex_001.jsonl` إلى `dialogue_batch_v2_flex_004.jsonl` بإجمالي 100 سجل `silver` موزعة بين الفصحى والسعودية، فأصبح corpus Phase 22 مكتملًا عند 500/500، ثم بدأت توسعة Phase 27 إلى 5143 بعد التنظيف.
- **Seed مصطلحات فصحى تدريبي:** أضيف `data/corpus/chat/jsonl/protected_terms_msa_seed_v1.jsonl` وفيه 22 سجلًا فصيحًا `gold` لتغطية مصطلحات تشغيل/حوكمة/تدريب أساسية، مع بطاقة provenance.
- **فصل المستخدمين من الأساس:** كل export وcorpus record يحمل الآن `owner_user_id/created_by_user_id/target_user_id/user_scope`; المسار الحالي `sami-local` و`single_user` حتى لا تختلط محادثات المستخدمين عند التوسع لاحقًا.
- **بنك تأليف فصيح غير تدريبي:** أضيف `resources/phase22_authoring/msa_prompt_bank_v1.json` وفيه 80+ موضوعًا فصيحًا لتسهيل كتابة batches الفصحى؛ الملف `training_allowed=false` و`synthetic_llm_data=false` ولا يُنسخ إلى corpus.
- **Review intake الحالي:** `data/corpus/chat/review/sample_review_export.jsonl` مرشح للمراجعة فقط؛ الأداة read-only ولا تنقل أي شيء إلى التدريب.
- **بوابة جودة الحوار:** `phase22-review-intake` يعرض الآن `quality_score/quality_label/quality_blockers`; الجلسة المفيدة للتدريب تحتاج غالبًا 3 أدوار مستخدم + 3 ردود مساعد على الأقل وبدون ردود raw من `sf_10m_v0_1/sf_10m_v0_2`.
- **بوابة Phase 22 في الواجهة:** شاشة `/ui/chat` تعرض قراءة حية من `/system/phase22-readiness`: عدد corpus الحالي، المتبقي، حالة `msa/saudi`، وأن corpus v2 مكتمل من جهة البيانات.
- **مهمة الجمع الحالية:** endpoints Phase 22 بقيت داخلية للوكيل، لكن شاشة `/ui/chat` لم تعد تعرض جمع/تصدير/حفظ يدوي. الواجهة الآن لاختبار الحوار فقط.
- **حفظ المراجعة الداخلي:** `POST /chat/review-export` باقٍ كمسار داخلي محكوم عند الحاجة، وليس زرًا ظاهرًا للمستخدم في `/ui/chat`.
- **اعتماد البيانات:** الوكيل يؤلف/يراجع/يعتمد دفعات corpus مباشرة عند وضوح الجودة؛ لا يُطلب من سامي حفظ أو تصدير يدوي.
- **تصحيح تشغيل المولّد:** بعد Phase 27.50 لم تعد الواجهة تعرض القوالب. أي رد ظاهر من `/chat/message` يأتي من `sf_10m_phase27_47`، وغير المدعوم يرجع ردًا فارغًا بدل template.
- **مختبر سامي المحلي:** يمكن تشغيل المولّد الخام عبر `SF_ENABLE_NATIVE_GENERATOR=true` و`SF_NATIVE_GENERATOR_EXPERIMENTAL=true`، وتمكين الرسائل غير الحساسة من مجالات skeleton عبر `SF_LAB_GENERATION_FOR_NON_SENSITIVE=true` عند الاختبار فقط.
- **حماية التصدير:** إذا صدّرت جلسة تحتوي ردودًا من `sf_10m_v0_1/sf_10m_v0_2`، تضع الواجهة metadata واضحًا، و`phase22-review-intake` لا يعدّها candidate تدريب جودة.
- **واجهة الاختبار:** الواجهة الآن لاختبار المولد مباشرة. التشخيص يجب أن يبين `sf_10m_phase27_47` أو `generator_blocked`، وليس `template`.
- **تفويض التنفيذ:** سامي أعطى إذنًا صريحًا بمتابعة التدريب والاختبارات والمراحل المسجلة دون انتظار موافقات جديدة؛ استخدم flags المطلوبة مع توثيق كل تشغيل ولا تكسر قواعد السيادة/السلامة.
- **فحص Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/corpus-audit`
- **قرار Phase 12 من المتصفح/API:** `GET http://127.0.0.1:8123/system/phase12-readiness` يعرض أن tokenizer v1 اكتمل، وأن `msa + saudi` موجودتان حاليًا؛ tokenizer v2 أصبح جاهزًا في Phase 23.
- **قرار Phase 12 من الطرفية بدون restart:** `make phase12-readiness`، وهو read-only ويعرض نفس منطق القرار.
- **بوابات Phase 20 من الطرفية/API:** `make phase20-gates` أو `GET http://127.0.0.1:8123/system/phase20-gates`.
- **خطة جمع Phase 22:** `make phase22-plan` أو `GET http://127.0.0.1:8123/system/phase22-collection-plan`.
- **فحص ملفات review في Phase 22:** `make phase22-review-intake` أو `GET http://127.0.0.1:8123/system/phase22-review-intake`، ويشمل score جودة الحوار.
- **جرد المصادر الشامل:** `make source-inventory` أو `GET http://127.0.0.1:8123/system/source-inventory`
- **فحص السيرفر بدون تعطيل:** `make server-status`، وهو read-only ولا يعمل restart/stop.
- **تشغيل السيرفر المستقر:** `make server-start` يبدأه داخل `screen` فقط إذا كان متوقفًا.
- **المراجع المحلية الخاصة الموجودة:** 516 مدخل قاموس سعودي + 1032 مهمة لهجة سعودية، وهي مستثناة من الرفع وتحتاج تحويل/حوكمة قبل استخدامها كـ LM corpus.
- **طبقة الحوكمة الهندسية قبل Phase 12:** مكتملة في `docs/PROJECT_IDENTITY.md`, `docs/ENGINEERING_RULES.md`, `docs/AGENT_INSTRUCTIONS.md`, `docs/PROJECT_MAP.md`, `docs/PROJECT_LIFECYCLE.md`.
- **طبقة الدستور الهندسي واللغوي قبل Phase 12:** مكتملة في `docs/PROJECT_CONSTITUTION.md`, `docs/LANGUAGE_SEGMENTATION.md`, `docs/TOKENIZATION_POLICY.md`, `docs/DATASET_GOVERNANCE.md`, `docs/AGENT_ENGINEERING_RULES.md`.
- **موارد tokenization:** `resources/tokenization/protected_terms_saudi.txt`, `resources/tokenization/preferred_merges.txt`, `resources/tokenization/tokenization_rules.yaml`.
- **مصطلحات فصحى مرشحة:** أضيف `resources/tokenization/protected_terms_msa_candidate.txt` وفيه 138 مصطلحًا/عبارة فصيحة، و`resources/tokenization/preferred_merges_msa_candidate.txt` وفيه 101 merge مرشح؛ هذه موارد سياسة غير نشطة وليست corpus ولا vocab pretrained.
- **فحص tokenization قبل Phase 12:** `make tokenization-audit`، وهو read-only ولا يدرّب tokenizer.
- **نتيجة tokenization-audit الحالية:** 30/30 protected terms مغطاة في corpus الحالي؛ التغطية 100%.
- **فحص Phase 23 tokenizer:** `make phase23-tokenizer-audit`، وهو يكتب/يحدّث ملفات `tokenizer_config.json`, `provenance.json`, `audit_report.json` داخل `artifacts/tokenizers/sf_bpe/v2/`.
- **تقرير Phase 12:** `docs/PHASE12_TOKENIZER_V1_REPORT.md`، وحالته: `COMPLETED_WITH_LIMITS`.
- **تحسين اللغة الأخير:** التركيز الافتراضي الآن على العربية الفصحى + اللهجة السعودية فقط، مع إيقاف اللهجات الأخرى افتراضيًا.
- **تحسين المحادثة الأخير:** واجهة فاتحة أوضح للشات، خطوط أكبر، أزرار أوضح، لوحة تشخيص مقروءة، وتسمية عربية لـ `generator/rag/dispatch` بدون أزرار حفظ/تصدير يدوية.
- **خلفية:** بعد Phase 7 أضاف المستخدم قاموس سعودي تأليفي (Phase 3.6)، ثم أُكملت Phase 8 (RAG)، Phase 9 (الشاشة)، Phase 10 (هياكل المجالات).
- **آخر تحديث:** 2026-05-23

---

## بيئة التطوير

### الجهاز
- **MacBook Air M4**
- **Memory:** 24GB
- **OS:** macOS (Darwin 24.6.0)
- **Shell:** zsh

### الأدوات المنصّبة الآن (Phase 1)
- **Python 3.14.5** على macOS / Apple Silicon (`pyproject.toml` يشترط ≥3.11).
- بيئة افتراضية محلية في `SF.AI/.venv/`.
- **fastapi 0.136**, **uvicorn 0.47** + uvloop + httptools + websockets.
- **pydantic 2.13**, **pydantic-settings 2.14**, **python-dotenv 1.2**, **PyYAML 6.0**.
- **httpx 0.28**.
- **pytest 9.0**, **pytest-asyncio 1.3**, **ruff 0.15**, **mypy 2.1**.

### الأدوات المنصّبة الإضافية (Phase 6)
- **PyTorch 2.12** مع دعم MPS (Apple Silicon) فعال.
- **numpy 2.4** (مطلوب من torch).
- **beautifulsoup4 4.14** + **lxml 6.1** (Phase 3.5 للاستيراد).

### الأدوات المخططة (تأتي في مراحلها)
- Apple MLX كإطار حساب اختياري (Phase 5.5/6).
- PostgreSQL (Phase 1+ docker-compose عند الحاجة).
- Redis (Phase 1+ docker-compose عند الحاجة).
- Qdrant (Phase 8).
- Scrapy / Playwright / BeautifulSoup / lxml (Phase 7).
- Next.js / React / TypeScript (Phase 9).
- Docker / docker-compose (متاح كـ skeleton، لم تُشغَّل الخدمات).

---

## الملفات الموجودة الآن (Phases 0–18 + Governance Layer)

```
SF.AI/
├── README.md                              Phase 1
├── PROJECT_PRINCIPLES.md                  Phase 0
├── SETUP_STATUS.md                        محدّث
├── .env.example / .gitignore              Phase 1 (+ runtime lexicon flags)
├── docker-compose.yml / Makefile          Phase 1 (+ targets Phase 3.5/5.5/6/12/18)
├── pyproject.toml                         Phase 1 (+ training extras: torch)
│
├── apps/
│   ├── api/
│   │   ├── main.py                        FastAPI + ui router
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── health.py                  GET /health
│   │   │   ├── chat.py                    POST /chat/message → Orchestrator
│   │   │   ├── system.py                  GET /system/status
│   │   │   └── ui.py                      GET /ui/chat  (Phase 9)
│   │   ├── static/
│   │   │   └── chat.html                  شاشة المحادثة RTL (Phase 9 + clear/timestamps/export)
│   │   └── schemas/{chat,system}.py
│   └── web/README.md                      placeholder for Next.js later
│
├── sf_ai/
│   ├── core/
│   │   ├── config.py, logging.py
│   │   ├── orchestrator/                  Phase 2 + NLP wiring Phase 3
│   │   ├── router/                        DomainRouter + IntentRouter (lens-aware)
│   │   ├── semantic/                      lexical + hashing + explorer
│   │   ├── index/                         CapabilityRegistry + default_registry.yaml
│   │   ├── planner/                       stub
│   │   ├── composer/                      ResponseComposer
│   │   └── nlp/                           Phase 3 — Arabic normalizer, dialect,
│   │                                       arabizi, typo, intent_detector, pipeline
│   ├── modules/
│   │   ├── chat/                          Phase 4 — active module + state + templates
│   │   ├── web/                           Phase 7 — ready_offline
│   │   └── research/                      Phase 7 — ready_offline
│   ├── memory/                            Phase 8 — sparse + vector + hybrid + LT
│   ├── tools/web/                         Phase 3.5 + Phase 7 — crawler, robots,
│   │                                       rate_limiter, extractors, mo3jam importer
│   ├── models/
│   │   ├── tokenizer/                     Phase 5.5 — char + SF-BPE + trainer
│   │   └── transformer/                   Phase 6 — TinyTransformer + RoPE + RMSNorm
│   ├── datasets/                          Phase 5 + Phase 3.6 + Phase 18 dialogue batches
│   └── training/                          Phase 5.5 + Phase 6 — device, schedules,
│                                           checkpoints, optimizers, train_*.py
│
├── resources/lexicons/
│   ├── *.yaml                             Phase 3 seed lexicons (18 ملف)
│   └── imported/
│       ├── mo3jam/                        Phase 3.5 destination (فارغ حتى الاستيراد)
│       └── saudi_seed_v1/                 Phase 3.6 — قاموسك (516 مدخل)
├── resources/tokenization/                Constitution Layer — protected terms + rules
│
├── data/corpus/
│   ├── chat/{raw,cleaned,jsonl,review}/   Phase 5/11/18 — governed chat corpus + review exports
│   └── dialects/saudi/
│       ├── raw/mo3jam/                    Phase 3.5
│       ├── jsonl/saudi_dialect_training_tasks_seed_v1.jsonl   Phase 3.6
│       ├── cleaned/, reports/
│
├── artifacts/{tokenizers,checkpoints,logs,reports}/   Phase 5.5+ outputs/reports
│
├── tests/                                 pytest suite — 649 تست / 88 ملف
│   ├── fixtures/
│   │   ├── mo3jam_listing_sample.html, mo3jam_term_sample.html
│   │   └── article_sample.html
│   └── test_*.py
│
├── sf_ai/modules/{coding,data,files,legal,medical,finance,education,
│                 religion,social,writing,translation,image,audio,
│                 security,business,ecommerce}/
│                                           Phase 10 — skeleton modules
│
├── scripts/
│   ├── check_env.sh
│   ├── validate_dataset.py                Phase 5
│   ├── train_bpe.py                       Phase 5.5
│   ├── run_chat_server.sh                 يشغّل API على 8123 ويفعّل Saudi Seed افتراضيًا
│   ├── prepare_dialogue_batch.py          Phase 18 — يحضر exports مراجعة إلى batch تدريبي محكوم
│   ├── phase19_readiness.py               Phase 19 — بوابة جاهزية SF-50M read-only
│   ├── phase20_gates.py                   Phase 20 — بوابات تفعيل المجالات read-only
│   └── import_mo3jam_saudi.py             Phase 3.5
│
└── docs/
    ├── EXECUTION_PLAN.md, PHASE_STATUS.md, ARCHITECTURE.md
    ├── PROJECT_IDENTITY.md, ENGINEERING_RULES.md, AGENT_INSTRUCTIONS.md
    ├── PROJECT_MAP.md, PROJECT_LIFECYCLE.md
    ├── CURRENT_GOALS.md                    الهدف العام وخارطة التوليد الحالية
    ├── DATA_IMPROVEMENT_LOOP.md           Phase 18 — دورة تحسين البيانات
    ├── PHASE19_READINESS_REPORT.md         Phase 19 — قرار جاهزية SF-50M
    ├── PHASE20_DOMAIN_ACTIVATION_GATES_REPORT.md  Phase 20 — بوابات المجالات
    ├── ROUTER.md, SEMANTIC_EXPLORER.md, LANGUAGE_UNDERSTANDING.md
    ├── DATASET_FORMAT.md, SOVEREIGN_ACCELERATION.md, TRAINING_PLAN.md
    ├── WEB_RESEARCH_PLAN.md, WEB_CRAWLING_POLICY.md, RAG_PLAN.md
    ├── CURRENT_GOALS.md                    أهداف اللغة والاختبار الحالية
    ├── SOURCE_DISCOVERY_MO3JAM.md         Phase 3.5
    ├── SOURCE_DISCOVERY_SAUDI_SEED.md     Phase 3.6
    └── LEXICON_STATS.md
```

---

## الـ Endpoints الفعالة

- `GET /` — معلومات root + رابط الـ UI.
- `GET /health` — فحص صحة (project + phase).
- `GET /system/status` — حالة المراحل + flags السيادة + قائمة المكونات، بما فيها Phase 19/20.
- `GET /system/corpus-audit` — جاهزية corpus قبل Phase 12.
- `GET /system/phase12-readiness` — قرار جاهزية Phase 12 مع بوابة الإذن.
- `GET /system/phase19-readiness` — قرار جاهزية Phase 19 قبل أي تدريب `SF-50M`.
- `GET /system/phase20-gates` — بوابات تفعيل المجالات؛ read-only ولا يفعّل مجالًا تلقائيًا.
- `GET /system/phase22-readiness` — بوابة جاهزية corpus v2 قبل Phase 23.
- `GET /system/phase23-tokenizer-audit` — تقرير tokenizer v2 قبل Phase 24.
- `GET /system/phase26-readiness` — قرار Phase 26 قبل أي تدريب `SF-50M`.
- `GET /system/phase27-dialogue-eval` — تقييم Phase 27 متعدد الأدوار + خطة corpus إلى 5000.
- `GET /system/phase22-collection-plan` — خطة جمع corpus v2 حسب العجز الحالي.
- `GET /system/phase22-review-intake` — فحص ملفات review exports قبل أي تحويل تدريبي.
- `GET /system/source-inventory` — جرد مصادر البيانات والمراجع.
- `POST /chat/message` — Orchestrator: NLP → Router → Module/Composer. يرجع domain/intent/confidence/signals/route_reason/response/requires_safety/status/fallback_used/dispatch/generator/debug.
- `GET /chat` → redirect (307) إلى `/ui/chat`.
- `GET /ui/chat` — **شاشة المحادثة العربية RTL** (Phase 9).

تشغيل (السيرفر شغّال حاليًا في `screen` detached باسم `sfai8123` على 8123):
```bash
bash scripts/run_chat_server.sh
```
فحص بدون تعطيل:
```bash
make server-status
```
تشغيل detached إذا كان متوقفًا:
```bash
make server-start
```
ثم زر `http://127.0.0.1:8123/ui/chat` أو `http://127.0.0.1:8123/docs`.

آخر تحقق حي بعد restart:
- السيرفر يعمل داخل `screen` detached باسم `sfai8123` على `127.0.0.1:8123`.
- الكود الحالي يعرض `Phase 27.93` في `/system/status` و`/health`; runtime المولّد العام لا يزال محجوبًا حتى نجاح gates.
- `GET /system/phase26-readiness` يرجع `can_start_sf50m_training=false`.
- `GET /system/corpus-audit` يعرض `READY_FOR_PHASE_12_TOKENIZER_TRAINING` بعدد 30/30
- `make server-status` read-only ولا يوقف السيرفر.

> المنفذ 8000/8765 مشغول بمشروع آخر للمستخدم — استخدم 8123.

---

## نتائج الاختبارات (حتى إكمال Phase 27.93)

```
649 passed in 94.62s (0:01:34)
```

التغطية الحالية:
- `test_arabic_normalizer.py` — 16 tests
- `test_capability_registry.py` — 5 tests
- `test_chat_module.py` — 12 tests (Phase 4 + language polish)
- `test_chat_native_generator.py` — 26 tests (Phase 15 + Phase 25 canary routing + Phase 27.37 semantic topic guard)
- `test_chat_rag_bridge.py` — 7 tests (Phase 17)
- `test_phase16_eval_harness.py` — 3 tests (Phase 16)
- `test_conversation_state.py` — 8 tests (Phase 4)
- `test_corpus_governance.py` — 10 tests (Phase 11 corpus governance)
- `test_dataset_validators.py` — 28 tests (Phase 5)
- `test_bpe_tokenizer.py` — 13 tests (Phase 5.5)
- `test_training_device.py` — 14 tests (Phase 5.5)
- `test_checkpoints.py` — 7 tests (Phase 5.5)
- `test_training_config.py` — 8 tests (Phase 5.5)
- `test_mo3jam_importer.py` — 13 tests (Phase 3.5)
- `test_tiny_transformer.py` — 26 tests (Phase 6)
- `test_web_extractor.py` — 18 tests (Phase 7)
- `test_research_summarizer.py` — 20 tests (Phase 7)
- `test_saudi_seed.py` — 15 tests (Phase 3.6)
- `test_rag_sparse_retrieval.py` — 14 tests (Phase 8)
- `test_chat_ui.py` — 7 tests (Phase 9 + export quality indicator)
- `test_dialogue_batch_preparation.py` — Phase 18 data loop
- `test_dialect_mapper.py` — 7 tests
- `test_health.py` — 12 tests (API + module dispatch + safety + readiness)
- `test_intent_detector.py` — 7 tests
- `test_new_chat_intents.py` — 40 tests (daily social + phase guidance prompts)
- `test_nlp_pipeline.py` — 9 tests
- `test_phase10_skeleton_domains.py` — 4 tests (Phase 10)
- `test_phase22_readiness.py` — 15 tests (Phase 22)
- `test_phase22_review_intake.py` — 8 tests (Phase 22 review exports + raw generator gate)
- `test_phase23_tokenizer_artifacts.py` — 6 tests (Phase 23 tokenizer v2)
- `test_phase24_sf10m_v0_2_report.py` — 3 tests (Phase 24 training report + runtime block)
- `test_phase25_generation_canary.py` — 6 tests (Phase 25 canary guard)
- `test_phase27_89_stratified_round_robin_curriculum_sampler_gate.py` — 2 tests (Phase 27.89 sampler gate)
- `test_phase27_90_bounded_round_robin_repair.py` — 2 tests (Phase 27.90 training result)
- `test_phase27_91_round_robin_training_result_diagnosis.py` — 2 tests (Phase 27.91 diagnosis)
- `test_phase27_92_topic_objective_repair_design_gate.py` — 2 tests (Phase 27.92 design gate)
- `test_phase27_93_topic_objective_gate_encoding.py` — 4 tests (Phase 27.93 renderer/gate)
- `test_orchestrator.py` — 7 tests
- `test_response_composer.py` — 6 tests
- `test_router.py` — 8 tests
- `test_router_with_nlp.py` — 5 tests
- `test_semantic_explorer.py` — 10 tests
- `test_typo_corrector.py` — 5 tests

تشغيل: `make test`.

---

## خارطة النموذج اللغوي السيادي بعد Phase 11

- **Phase 11:** حوكمة وتجهيز بيانات حوار عربي/سعودي — مكتملة كحوكمة، وبدأت بـ seed صغير ثم توسعت لاحقًا عبر Phase 22 إلى 500 سجل متوازن.
- **Governance Layer:** قواعد الهندسة والهوية وخريطة المشروع ودورة الحياة — مكتملة قبل Phase 12.
- **Phase 12:** تدريب SF-BPE tokenizer v1 من بيانات SF.AI فقط.
- **Phase 13:** تدريب smoke صغير لإثبات أن النموذج يتعلم ويولد نصًا خامًا.
- **Phase 14:** تدريب `SF-10M v0.1`.
- **Phase 15:** ربط checkpoint ببنية `ChatModule` كمولّد اختياري، مع إبقاء runtime على القوالب.
- **Phase 16:** تقييم الجودة والسلامة والأسلوب السعودي/الفصيح — مكتمل، ومختبر سامي المحلي يستطيع تشغيل المولد الخام للتجربة.
- **Phase 17:** ربط Memory/RAG المحلي بالشات — مكتمل كبنية محلية اختيارية.
- **Phase 18:** دورة توسيع بيانات من اختبار سامي المباشر — مكتملة كتصدير مراجعة + batch preparation محكوم.
- **Phase 19:** بوابة جاهزية تدريب مرشح `SF-50M` — تعمل، وقرارها الحالي: وسّع corpus أولًا.
- **Phase 20:** بوابات تفعيل المجالات skeleton عبر gates مستقلة — تعمل، ولا تفعّل شيئًا تلقائيًا.
- **Phase 27.78:** بوابة `ENGINEERING_ROOT_CAUSE_GATE` — مكتملة، وأصدرت `PHASE27_78_ENGINEERING_DECISION`.
- **Phase 27.79:** تصميم إصلاح objective/curriculum/decoding — مكتمل، وأصدر `PHASE27_79_REPAIR_DESIGN_DECISION` بدون تدريب.
- **Phase 27.80:** تشفير بوابات الإصلاح + remediation — مكتملة؛ مرّت gates بعد balanced family view.
- **Phase 27.81:** تأليف حزمة عائلات الحوار المتوازنة — مكتملة؛ أضيف `2500` سجل gold وأصبح corpus `8443`.
- **Phase 27.82:** قرار تدريب الإصلاح العائلي — مكتمل؛ يسمح فقط بـ Phase 27.83 bounded SF-10M repair training، ولا يسمح بـ runtime أو SF-50M.
- **Phase 27.83:** تدريب إصلاح محدود لـ SF-10M — مكتمل كتشغيل، لكنه فشل حواريًا (`best=11/60`)؛ runtime وSF-50M محجوبان.
- **Phase 27.84:** تشخيص فشل objective/curriculum — مكتمل؛ family metadata لم تظهر داخل نص التدريب، ولذلك التوازن لم يصبح conditioning فعليًا.
- **Phase 27.85:** تصميم family conditioning الصريح — مكتمل؛ `عائلة الحوار: سوالف/متابعة/تنظيم/دعم/موضوع` كسياق masked عن loss.
- **Phase 27.86:** بوابة renderer — مكتملة؛ `render_dialogue_text` يطبع `عائلة الحوار` في مساري split/no-split، وassistant-only loss يخفي conditioning/user lines.
- **Phase 27.87:** تدريب SF-10M مقيّد بعد renderer — مكتمل؛ أفضل fresh shadow `10/50` فقط، runtime محجوب، والانحياز العائلي ما زال حاضرًا.
- **Phase 27.88:** تشخيص نتيجة التدريب — مكتمل؛ السبب curriculum/sampling متسلسل؛ `موضوع` ظهر 5 مرات فقط في أول 1800 عينة.
- **Phase 27.89:** بوابة sampler متوازن — مكتملة؛ `family_round_robin` يعطي `360` عينة لكل family في أول 1800، وكل نافذة 600 فيها `120` لكل family؛ runtime محجوب والتدريب المقيّد مسموح للمرحلة 27.90 فقط.
- **Phase 27.90:** تدريب SF-10M محدود بالـ round-robin — مكتمل؛ best fresh shadow = `35/50` عند `sf-10m-step1800`، تحسن قوي لكنه دون بوابة `45/50`؛ runtime محجوب والتشخيص مطلوب.
- **Phase 27.91:** تشخيص نتيجة round-robin — مكتمل؛ الإخفاقات المتبقية يهيمن عليها `topic`: `9/15`، والسبب الأكبر `topic_semantic_collapse=48%`.
- **Phase 27.92:** تصميم إصلاح topic-objective — مكتمل؛ يسمح فقط بترميز بوابة 27.93 الجافة، ولا يسمح بتدريب أو runtime.
- **Phase 27.93:** ترميز بوابة topic-objective — مكتمل؛ dry-run نجح، لكن data pack مطلوب قبل أي تدريب بسبب نقص `الوفاء` السعودي.

أول توليد خام حدث في Phase 13. Phase 15 جهّز الباب داخل الشات، وPhase 16 أثبت أن التوليد مكرر. Phase 27.78 غيّرت المنهج: لا مزيد من التدريب المتكرر قبل تشخيص root-cause. Phase 27.79 صممت إصلاح objective/curriculum/decoding/family balance. Phase 27.80 شفّرت البوابات، Phase 27.81 عالجت توازن family ببيانات gold، Phase 27.82 سمحت بتدريب مقيّد، Phase 27.83 أثبتت أن الإصلاح الحالي لا يكفي، Phase 27.84 حددت السبب، Phase 27.85 صممت الإشارة الصريحة، Phase 27.86 أثبتت أن الإشارة تظهر فعليًا داخل نص التدريب ومخفية عن loss، Phase 27.87 أثبتت أن التدريب المقيّد ما زال غير كافٍ للحوار العام، Phase 27.88 حددت أن ترتيب stream هو الخلل الأكبر، Phase 27.89 أصلحت بوابة الترتيب قبل أي تدريب جديد، Phase 27.90 رفعت النتيجة إلى `35/50`، Phase 27.91 أثبتت أن الضعف المتبقي topic-specific لا capacity عام، Phase 27.92 صممت إصلاح topic-objective، وPhase 27.93 أثبتت الترميز الجاف وحجبت التدريب بسبب فجوة بيانات محددة.

---

## ما هو محظور (تذكير دائم)

- ❌ لا OpenAI / Claude / Gemini APIs.
- ❌ لا أي LLM جاهز.
- ❌ لا pretrained weights / embeddings / tokenizer.
- ❌ لا Llama / Gemma / Phi / Mistral.
- ❌ لا sentence-transformers.
- ❌ لا HuggingFace pretrained.
- ❌ لا LoRA فوق نموذج خارجي.
- ❌ لا synthetic LLM data من مصدر خارجي أو مجهول في corpus السيادي؛ حوار الوكيل مسموح فقط كـ owner-delegated agent-authored مع provenance كامل.
- ❌ لا API keys في الكود.
- ❌ لا تدريب خارج الخطة أو بدون provenance؛ التفويض الحالي يغطي المراحل المسجلة فقط.
- ❌ لا crawling تلقائي. CrawlerBase يرفع `CrawlerPermissionError` بدون `permission_granted=True`.
- ❌ لا انتقال خارج الخطة المسجلة بدون توثيق وإذن واضح.
- ❌ لا تدريب جديد قبل gates ناجحة بعد `PHASE27_79_REPAIR_DESIGN_DECISION`.
- ❌ لا tokenizer جديد قبل إثبات tokenizer كسبب أكبر.
- ❌ لا `SF-50M` قبل `SF-50M JUSTIFIED TRANSITION`.
- ❌ لا template masking لإخفاء ضعف المولد.

---

## ما هو مسموح (تذكير دائم)

- ✅ Python / PyTorch / PyTorch MPS / Apple MLX (كأدوات حساب).
- ✅ FastAPI / Next.js / React / TypeScript.
- ✅ PostgreSQL / Redis / Qdrant (مع vectors محلية فقط).
- ✅ Scrapy / Playwright / BeautifulSoup / lxml.
- ✅ pandas / openpyxl.
- ✅ Docker / docker-compose.
- ✅ pytest / ruff / mypy.
- ✅ YAML / JSON / JSONL.
- ✅ Rule-based / lexical scoring / fuzzy matching محلي / hashing vectorizer محلي.
- ✅ BPE tokenizer مدرَّب من الصفر على بيانات SF.AI فقط.
- ✅ Random initialization، AdamW، schedulers، gradient accumulation/checkpointing، mixed precision.
- ✅ Architectures معروفة (Decoder-only Transformer, RoPE, RMSNorm, SwiGLU, weight tying) بدون أوزانها.
- ✅ أدوات Strategy v2 السيادية: TensorBoard المحلي، experiment tracking، advanced decoding، repetition control، held-out/shadow canaries، contrastive evaluation، objective tracing، anti-collapse diagnostics، local preference optimization على أوزان SF.AI فقط.
- ✅ عند نجاح بوابة التكبير، الانتقال التلقائي للحجم التالي حتى `SF-1B+` دون انتظار موافقة جديدة.

---

## بروتوكول الانتقال

التفويض الحالي من سامي: استمر في المراحل المسجلة دون انتظار موافقة جديدة، ومع نجاح بوابة التكبير انتقل تلقائيًا للحجم التالي حتى `SF-1B+`. ارفع الناجح فقط، افحص الحساسية، ووثّق كل خطوة. لا تبدأ أي مصدر خارجي/زحف/اعتماد pretrained مهما كان التفويض عامًا. بعد Phase 27.93 لا يوجد runtime release ولا SF-50M ولا tokenizer retrain ولا تدريب جديد؛ المطلوب Phase 27.94 لتأليف data pack موضوعي يسد فجوة `الوفاء` السعودية.
