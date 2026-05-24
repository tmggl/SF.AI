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

## الحالة الحالية الملزمة

المسار الحالي الرسمي:

```text
Phase 27.78 — Engineering Root Cause Gate
Sovereign Practical Acceleration Strategy v2
PHASE27_78_ENGINEERING_DECISION
```

القرار الحالي:

- لا تدريب جديد.
- لا tokenizer جديد.
- لا runtime release.
- لا انتقال إلى `SF-50M`.
- التالي: `Phase 27.79 — Objective/Curriculum/Decoding Repair Design`.

سبب القرار:

- family mixing: `22%`.
- objective: `18%`.
- curriculum: `16%`.
- weak generalization: `14%`.
- semantic routing: `10%`.
- capacity: `1%`.

أي Agent جديد يجب أن يقرأ:

- [docs/PHASE_STATUS.md](./docs/PHASE_STATUS.md)
- [docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md](./docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md)
- [artifacts/reports/PHASE27_78_ENGINEERING_DECISION.json](./artifacts/reports/PHASE27_78_ENGINEERING_DECISION.json)

قبل أي تدريب جديد يجب وجود `ENGINEERING_ROOT_CAUSE_GATE` وقرار يسمح به.
قبل أي runtime release يجب نجاح `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.

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
- [docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md](./docs/PHASE27_78_ENGINEERING_ROOT_CAUSE_GATE_REPORT.md) — قرار root-cause الحالي الذي يمنع التدريب الأعمى والتكبير.
- [docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md](./docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md) — قرار أدوات جودة التدريب المحلية.
- [docs/SF_AI_ENGINEER_STATUS_REPORT.md](./docs/SF_AI_ENGINEER_STATUS_REPORT.md) — تقرير شامل يمكن تقديمه لمهندس خارجي لفهم الهدف والحالة والخطة.
- [docs/PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md](./docs/PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md) — تقرير فتح `sf_10m_phase27_47` في المسار التجريبي المحروس.
- [docs/PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md](./docs/PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md) — تقرير توسيع اختبارات الواجهة/API الحية إلى `33/33`.
- [docs/PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md](./docs/PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md) — تقرير تحويل الواجهة إلى مختبر مولّد فقط بلا قوالب.
- [docs/PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md](./docs/PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md) — تقرير يثبت أن الحوار الطبيعي المفتوح يحتاج تدريبًا جديدًا، لا توسيع كلمات مفتاحية.
- [docs/PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md](./docs/PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md) — تقرير دبل تدريب `SF-10M` الآمن وسبب عدم فتح checkpoint الجديد.
- [docs/PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md](./docs/PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md) — تقرير توسعة `10,540` زوجًا حواريًا ولماذا لم يكفِ ذلك داخل `SF-10M`.
- [docs/PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md](./docs/PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md) — بوابة قرار تمنع التكبير الكامل وتسمح فقط بmicro-probe تشخيصي مضبوط.
- [docs/PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md](./docs/PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md) — micro-probe قارن `SF-10M` و`SF-50M` وأبقى التكبير الكامل محجوبًا.
- [docs/PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md](./docs/PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md) — تشخيص objective/format/tokenizer قبل أي تدريب جديد.
- [docs/PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md](./docs/PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md) — حزمة إصلاح tokenizer/eval/format قبل إعادة التدريب.
- [docs/PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md](./docs/PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md) — tokenizer v7 نجح في الحماية، لكن bounded alignment probe فشل `4/15`.
- [docs/PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md](./docs/PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md) — إصلاح alignment محدود نجح `15/15` والواجهة بقيت محجوبة.
- [docs/PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md](./docs/PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md) — canary طبيعي أوسع فشل `12/30` وكشف ضعف التعميم.
- [docs/PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md](./docs/PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md) — repair أوسع حسّن النتيجة إلى `18/30` لكنه فشل توازن العائلات.
- [docs/PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md](./docs/PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md) — تجربة توازن عائلات تراجعت إلى `10/30` وكشفت أثر ترتيب curriculum.
- [docs/PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md](./docs/PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md) — interleaved curriculum رفع canary إلى `26/30` مع بقاء runtime محجوبًا.
- [docs/PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md](./docs/PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md) — فحص يثبت أن tokenizer v8 مطلوب لحماية `التعاون/الاحترام`.
- [docs/PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md](./docs/PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md) — tokenizer v8 نجح: critical `2/2`, topic terms `8/8`.
- [docs/PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md](./docs/PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md) — LM repair محدود على tokenizer v8 نجح broader canary `30/30` مع بقاء runtime محجوبًا.
- [docs/PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md](./docs/PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md) — fresh shadow canary بأسئلة غير مرئية فشل `30/50`، لذلك runtime محجوب.
- [docs/PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md](./docs/PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md) — إصلاح فشل 27.67 مرّر known shadow `50/50` وregression `30/30` مع بقاء runtime محجوبًا.
- [docs/PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md](./docs/PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md) — fresh shadow جديد بعد الإصلاح وصل `56/60` لكن بقي open_social، لذلك runtime محجوب.
- [docs/PHASE27_70_OPEN_SOCIAL_REPAIR_REPORT.md](./docs/PHASE27_70_OPEN_SOCIAL_REPAIR_REPORT.md) — إصلاح open_social/fine-tune لم يتجاوز baseline، لذلك runtime محجوب.
- [docs/PHASE27_71_CANDIDATE_SELECTION_REPORT.md](./docs/PHASE27_71_CANDIDATE_SELECTION_REPORT.md) — اختيار مرشح: `phase27_68` هو الأفضل `136/140` لكنه ليس مستقرًا كفاية للواجهة.
- [docs/PHASE27_72_STABILITY_FIRST_REPAIR_REPORT.md](./docs/PHASE27_72_STABILITY_FIRST_REPAIR_REPORT.md) — micro-repair من أفضل مرشح رفع النتيجة إلى `138/140` مع بقاء runtime محجوبًا.

---

## الهدف الحالي

- **الرحلة الحالية:** Phase 27.78 / 30 — Engineering Root Cause Gate.
- **الأولوية الحالية:** Phase 27.79 Objective/Curriculum/Decoding Repair Design؛ لا تدريب قبل تشفير gates، ولا runtime قبل held-out success.
- **الشات الحالي:** `/chat/message` والواجهة يعملان كمختبر مولّد فقط؛ أي رد ظاهر يجب أن يكون من `SF-10M Phase 27.47`، وإذا حُجب المولد ترجع الاستجابة فارغة بدل قالب.
- **البيانات الحالية:** corpus موثق `5943` سجلًا يمر `corpus-audit`: `2994` سعودي + `2949` فصحى. Phase 27.15 أضاف social/lexical curriculum، والـ split الحالي `train=5343`, `eval=600`.
- **التدريب:** محجوب حاليًا بقرار `PHASE27_78_ENGINEERING_DECISION`. Phase 12 tokenizer v1 وPhase 13 smoke LM وPhase 14 SF-10M v0.1 وPhase 23 tokenizer v2 وPhase 24 SF-10M v0.2 اكتملت من بيانات SF.AI فقط.
- **المولّد:** `/chat/message` والواجهة يستخدمان Phase 27.47 `sf-10m-step4600` مباشرة في المختبر المحلي؛ لا زر ولا مفتاح تبديل، وغير المدعوم يرجع `generator_blocked` مع رد فارغ بدل أي قالب. Phase 27.52 و27.53 دربتا مرشحين جديدين، لكنهما لم يمرا بوابة الحوار المفتوح، لذلك لم يُفتحا في runtime.
- **التقييم:** Phase 27 مرّر `19/19` turn في حوار متعدد الأدوار، لكنه أكد أن الردود ما زالت `template` وأن المولد غير جاهز.
- **الذاكرة المحلية:** Phase 17 أضاف ChatRagBridge اختياريًا؛ runtime الافتراضي لا يحمّل ذاكرة ولا يزحف ويب.
- **دورة البيانات:** Phase 18 أضاف تصدير مراجعة من الواجهة و`prepare_dialogue_batch.py`; وPhase 22 يعتمد الآن أيضًا دفعات مباشرة يؤلفها/يراجعها الوكيل بتفويض موثق، بدون انتظار حفظ أو تصدير من سامي.
- **جاهزية SF-50M:** محجوبة الآن. Phase 27.78 وزن capacity بـ `1%` فقط؛ لا يفتح `SF-50M` إلا عبر `SF-50M JUSTIFIED TRANSITION`.
- **بوابات المجالات:** Phase 20 أضاف `make phase20-gates` و`GET /system/phase20-gates`; المجال النشط الوحيد هو `chat`.
- **طريق التوليد المقنع:** لا تعرض `SF-10M v0.2` أو `SF-10M v0.4` أو `SF-10M v0.5` أو `SF-10M v0.6` كنجاح حواري. v0.6 تحسن رقميًا لكن canary حجبه.
- **Corpus v2:** Phase 22 أضاف `make phase22-readiness` و`make phase22-plan` و`make phase22-next-batch` و`make phase22-completion-gate` و`make phase22-review-intake`; الوضع الحالي 500/500، وفيه ثمان دفعات فصيحة `dialogue_batch_v2_msa_001.jsonl` إلى `dialogue_batch_v2_msa_008.jsonl` وسبع دفعات سعودية `dialogue_batch_v2_saudi_001.jsonl` إلى `dialogue_batch_v2_saudi_007.jsonl` وأربع دفعات مرنة `dialogue_batch_v2_flex_001.jsonl` إلى `dialogue_batch_v2_flex_004.jsonl` إضافة إلى seed فصيح للمصطلحات `protected_terms_msa_seed_v1.jsonl`. التوازن النهائي مكتمل (`msa=250`, `saudi=250`) ولا توجد دفعة تالية في Phase 22. الواجهة الآن للاختبار فقط ولا تعرض حفظ/تصدير يدوي؛ بناء corpus يتم عبر الوكيل والتقارير الداخلية. `phase22-completion-gate` يرجع الآن `PHASE22_COMPLETE_READY_FOR_PHASE23`.
- **Tokenizer v2:** Phase 23 أضاف `artifacts/tokenizers/sf_bpe/v2/` و`make phase23-tokenizer-audit`; الحالة `COMPLETED_READY_FOR_PHASE24`, `vocab=4493`, `merges=4386`, وprotected Saudi terms تحسنت من متوسط 4.0 tokens في v1 إلى 2.3 في v2.
- **SF-10M v0.2:** Phase 24 درّب النموذج 2000 خطوة على tokenizer v2 وcorpus المتوازن: loss `8.4751 → 2.8256`, eval loss `2.5779`, perplexity `13.17`. القرار: `COMPLETED_WITH_LIMITS_RUNTIME_BLOCKED` لأن التوليد لا يزال غير متماسك.
- **Canary v1:** Phase 25 أضاف `GenerationGuard` و`SF_GENERATOR_CANARY`; التجربة الحقيقية على v0.2 حُجبت بـ `generation_guard:malformed_token` وبقي الرد من القالب.
- **قرار Phase 26:** `SF-50M` غير جاهز رغم أن corpus الحالي `5143` تجاوز الحد العملي `5000`; المانع الآن runtime quality/hallucination/repetition gates. التقرير: [docs/PHASE26_SF50M_READINESS_REPORT.md](./docs/PHASE26_SF50M_READINESS_REPORT.md).
- **نتيجة Phase 27:** `make phase27-dialogue-eval` مرّر `19/19` turn في suite متعدد الأدوار، لكن كل الردود `template`، و`open_generator_ready=false`. بعد تنظيف الحوارات التشغيلية واكتمال الدفعات الطبيعية صارت خطة التوسعة: `0` سجلًا إضافيًا و`0` دفعات، بالتساوي `msa=0` و`saudi=0`. التقرير: [docs/PHASE27_DIALOGUE_EVAL_V2_REPORT.md](./docs/PHASE27_DIALOGUE_EVAL_V2_REPORT.md).
- **دفعات توسعة:** أضيفت Batch 001 بإجمالي 50 سجلًا، ثم Batch 002 وBatch 003 الكبيرتان بإجمالي 1000 سجل، كل واحدة `250` فصيح + `250` سعودي. التقارير: [docs/PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_001_REPORT.md), [docs/PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_002_REPORT.md), [docs/PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md](./docs/PHASE27_CORPUS_EXPANSION_BATCH_003_REPORT.md).
- **تنظيف corpus:** أضيف فلتر يمنع الحوارات التشغيلية/الهندسية/الخاصة بسامي من التدريب؛ حُذف `907` سجلًا قديمًا، ثم وصلت التوسعة الطبيعية إلى `5143` سجلًا. التقرير: [docs/CORPUS_OPERATIONAL_FILTER_REPORT.md](./docs/CORPUS_OPERATIONAL_FILTER_REPORT.md).
- **نتيجة Phase 27.5:** دُرّب `SF-10M v0.4` بصيغة حوارية كاملة على `5143` سجلًا: training loss `8.4662 → 1.4070`، لكن eval loss `5.8267` وperplexity `339.24` والردود غير مرتبطة كفاية بالسؤال. القرار: runtime blocked. التقرير: [docs/PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md](./docs/PHASE27_5_SF10M_DIALOGUE_FORMAT_REPORT.md).
- **نتيجة Phase 27.6:** دُرّب `SF-10M v0.5` بخسارة على رد المساعد فقط: training loss `8.4643 → 2.3513`; أفضل eval مقاس step2000: loss `6.5718`, perplexity `714.65`. الردود ما زالت مكررة، لذلك runtime blocked. التقرير: [docs/PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md](./docs/PHASE27_6_SF10M_ASSISTANT_TARGET_REPORT.md).
- **نتيجة Phase 27.7:** أضيف split ثابت `train=4703/eval=540`، و100 سجل gold social، وcanary prompt-aware. لا تدريب جديد في هذه المرحلة؛ runtime المولد لا يزال blocked. التقرير: [docs/PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md](./docs/PHASE27_7_FIXED_SPLIT_GOLD_SOCIAL_CANARY_REPORT.md).
- **نتيجة Phase 27.8:** دُرّب `SF-10M v0.6` على train split فقط، وأفضل eval كان step4000: loss `5.0227`, perplexity `151.82`. canary حجب `10/10` عينات بسبب fragments مشوهة، لذلك runtime blocked. التقرير: [docs/PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md](./docs/PHASE27_8_SF10M_V0_6_SPLIT_TRAINING_REPORT.md).
- **نتيجة Phase 27.9:** أضيف `make phase27-generation-quality` وprompt suite قصير؛ `SF-10M v0.6` فشل `0/10` بسبب `model_artifact_fragment`. التقرير: [docs/PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md](./docs/PHASE27_9_GENERATION_QUALITY_HARNESS_REPORT.md).
- **نتيجة Phase 27.10:** أضيفت 300 عينة gold قصيرة ودُرّب `SF-10M v0.7`; أفضل eval: loss `4.7512`, perplexity `115.72`. بعد تشديد الحارس بقي generation-quality `0/10`، لذلك runtime blocked. التقرير: [docs/PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md](./docs/PHASE27_10_SHORT_RESPONSE_REPAIR_REPORT.md).
- **نتيجة Phase 27.11:** probe ذهبي صغير (`16` ردًا) وصل إلى loss شبه صفري لكنه فشل `0/16 clean-stop`; النموذج يحفظ بدايات الردود ثم يواصل بتكرار/حشو. القرار: إصلاح boundary/EOS قبل أي SF-50M. التقرير: [docs/PHASE27_11_OBJECTIVE_PROBE_REPORT.md](./docs/PHASE27_11_OBJECTIVE_PROBE_REPORT.md).
- **نتيجة Phase 27.12:** أضيف `<eos>` هدفًا صريحًا لرد المساعد، وconditioning للفصحى/السعودي من provenance. probe الحالي: `5/16` تطابق كامل و`9/16` بلا فشل guard؛ التحسن لا يكفي للتفعيل. التقرير: [docs/PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md](./docs/PHASE27_12_ASSISTANT_EOS_REPAIR_REPORT.md).
- **نتيجة Phase 27.13:** دُرّب `SF-10M v0.8` على split التدريب بصيغة boundary/EOS + dialect conditioning. أفضل eval: loss `3.1875`, perplexity `24.23`، لكن generation-quality الصارم بقي `3/10` بسبب fragments، لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_13_SF10M_V08_REPORT.md](./docs/PHASE27_13_SF10M_V08_REPORT.md).
- **نتيجة Phase 27.14:** اعتُمدت طبقة `Sovereign Training Quality Tooling`: 10 أدوات محلية، منها EOS/boundaries، tracker، data scanner، curriculum، no-repeat controls، gold probes، checkpoint selector. لا تدريب جديد ولا تفعيل runtime. التقرير: [docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md](./docs/SOVEREIGN_TRAINING_QUALITY_TOOLING.md).
- **نتيجة Phase 27.15:** أضيفت 400 عينة gold اجتماعية/لغوية، وأضيف no-repeat decoding. دُرّب `SF-10M v0.10`; أفضل eval: loss `3.0452`, perplexity `21.01`. بعد تشديد canary الدلالي بقي `0/10`، لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md](./docs/PHASE27_15_SOCIAL_LEXICAL_CURRICULUM_REPORT.md).
- **نتيجة Phase 27.16:** أضيف `sample_isolated` packing لمنع اختلاط العينات داخل causal context، ودُرّب `SF-10M v0.11`. أفضل eval: loss `4.0573`, perplexity `57.82`، وcanary بقي محجوبًا (`step2000=2/10`, `step6000=0/10`). القرار: runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md](./docs/PHASE27_16_PROMPT_TO_ANSWER_OBJECTIVE_REPORT.md).
- **نتيجة Phase 27.17:** شُغّل micro-probe من 32 زوج سؤال/جواب فصحى وسعودي. النتيجة: `passed=27/32`, `exact_clean=28/32`, `semantic=29/32`. الفشل المتبقي كسور لفظية/حروفية، لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md](./docs/PHASE27_17_PROMPT_ANSWER_MICRO_PROBE_REPORT.md).
- **نتيجة Phase 27.18:** أضيف hygiene audit بعد micro-probe. النتيجة: `terms_total=26`, `average_pieces=3.5385`, `aggressive_split_terms=5`, `roundtrip_failures=0`, و`uncovered_bad_fragments=0`. القرار: runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md](./docs/PHASE27_18_TOKENIZATION_DECODING_HYGIENE_REPORT.md).
- **نتيجة Phase 27.19:** أضيف repair probe مركز حول العبارات الخمس، ودُرّب على `52` مثالًا داخليًا. النتيجة بقيت `passed=27/32`, `exact_clean=28/32`, `semantic=28/32`; لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md](./docs/PHASE27_19_HYGIENE_REPAIR_PROBE_REPORT.md).
- **نتيجة Phase 27.20:** أضيف دعم protected phrases داخل `BPETokenizer` وملف `protected_phrases_phase27_20.txt`. العبارات الخمس التي وصلت إلى `max_pieces=8` في v2 صارت قابلة للحفظ كقطعة واحدة في استراتيجية v3 (`max_pieces=1`, `all_roundtrip_ok=true`). runtime و`SF-50M` محظوران حتى تدريب tokenizer v3 وmicro-probe. التقرير: [docs/PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md](./docs/PHASE27_20_TOKENIZER_PROTECTED_PHRASE_STRATEGY_REPORT.md).
- **نتيجة Phase 27.21:** دُرّب tokenizer v3 في `artifacts/tokenizers/sf_bpe/v3` (`vocab=4706`, `merges=4648`) ثم شُغّل micro-probe. protected phrases نجحت، لكن probe فشل `25/32` بسبب لصق spacing/boundary مثل `سواونخفف` و`تفيدوتوسع`; لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md](./docs/PHASE27_21_TOKENIZER_V3_MICRO_PROBE_REPORT.md).
- **نتيجة Phase 27.22:** أُصلح decode boundary وfalse-positive في الحارس، فتحسن micro-probe من `25/32` إلى `29/32` واختفت كل مشاكل اللصق (`glued_left=0`). بقيت 3 إخفاقات semantic/lexical، لذلك runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md](./docs/PHASE27_22_SPACING_BOUNDARY_REPAIR_REPORT.md).
- **نتيجة Phase 27.23:** أضيف semantic/lexical repair متوازن على tokenizer v3. تحسن micro-probe إلى `30/32`; بقي خللان lexical في `التعاون` و`الاحترام`. runtime و`SF-50M` محظوران. التقرير: [docs/PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md](./docs/PHASE27_23_SEMANTIC_LEXICAL_REPAIR_REPORT.md).
- **نتيجة Phase 27.24:** أضيف tokenizer minimal `v4_min_lexical` بحماية `التعاون` و`الاحترام` فقط فوق عبارات v3 الأصلية. وصل micro-probe إلى `32/32`; runtime ما زال محظورًا حتى Phase 27.25 held-out canary. التقرير: [docs/PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md](./docs/PHASE27_24_MINIMAL_LEXICAL_STABILIZATION_REPORT.md).
- **نتيجة Phase 27.25:** شُغّل held-out generation canary على `16` سؤالًا جديدًا فصيحًا/سعوديًا دون تدريب جديد. النتيجة `8/16`: التعريفات القريبة نجحت، لكن التحية الفصيحة والنصيحة والتخطيط والدعم فشلت دلاليًا. القرار: `FAILED_HELDOUT_GENERATION_CANARY_BLOCK_RUNTIME`; الواجهة تبقى على القوالب حتى Phase 27.26. التقرير: [docs/PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md](./docs/PHASE27_25_HELDOUT_GENERATION_CANARY_REPORT.md).
- **نتيجة Phase 27.26–27.30:** تحسن المولد من `8/16` إلى `16/18` على fresh mixed shadow بعد intent/topic conditioning، لكنه بقي محجوبًا بسبب فشلين في الشكر وسؤال الحال السعودي. التقرير: [docs/PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md](./docs/PHASE27_26_TO_30_REPAIR_SERIES_REPORT.md).
- **نتيجة Phase 27.31–27.33:** أضيفت natural intent/topic data ثم balanced calibration ثم advice/micro stabilization. النتيجة النهائية في Phase 27.33: كل بوابات التوليد المحلية مرّت بلا تسريب، والحالة صارت `ready for guarded runtime trial design`. التقرير: [docs/PHASE27_31_TO_33_GENERATION_GATE_REPORT.md](./docs/PHASE27_31_TO_33_GENERATION_GATE_REPORT.md).
- **نتيجة Phase 27.34:** أضيف زر `مولّد تجريبي` وحقل `generator_trial=true` في `/chat/message`. بوابة runtime المحروس مرّت `9/9`، والهوية/الطب بقيت على القوالب الآمنة. التقرير: [docs/PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md](./docs/PHASE27_34_GUARDED_RUNTIME_TRIAL_REPORT.md).
- **نتيجة Phase 27.35:** اختبار حي عبر HTTP على `/ui/chat` و`/chat/message` مرّ `10/10`: الواجهة تعرض الزر، وطلبات trial تستخدم `sf_10m_phase27_33`, والتحكم الآمن بقي template/composer. التقرير: [docs/PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md](./docs/PHASE27_35_LIVE_UI_TRIAL_OBSERVATIONS_REPORT.md).
- **نتيجة Phase 27.36:** أضيف quality-floor للتجربة الحية: raw `chat.general` وموضوعات التعريف غير المثبتة لا تذهب للمولّد. triage الحي مرّ `27/27`: `18/18` مولّد، `5/5` quality-floor، `4/4` ضوابط. التقرير: [docs/PHASE27_36_LIVE_UI_TRIAGE_REPORT.md](./docs/PHASE27_36_LIVE_UI_TRIAGE_REPORT.md).
- **نتيجة Phase 27.37:** أضيف semantic topic guard وفتح موضوع `الصبر` بصيغ مثبتة فقط. التوسعة الحية مرّت `21/21`: `10/10` regression generated، `3/3` موضوع جديد، `5/5` quality-floor، `3/3` ضوابط. التقرير: [docs/PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md](./docs/PHASE27_37_SUPPORTED_TOPIC_EXPANSION_REPORT.md).
- **نتيجة Phase 27.38:** دُرّب probe مستهدف للموضوعات المحجوبة (`الصداقة/الصدق/التنظيم/الهدوء`) لكنه مرّ `6/20` فقط وظهر topic collapse نحو `الاحترام`. القرار: لا runtime switch. التقرير: [docs/PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md](./docs/PHASE27_38_TARGETED_TOPIC_CURRICULUM_PROBE_REPORT.md).
- **نتيجة Phase 27.39:** دُرّب topic-isolation probe متوازن للموضوعات الثمانية. تحسن جزئيًا إلى `10/24`، لكنه كشف كسورًا لفظية في `الصداقة/الصدق/التنظيم` وتسربًا محدودًا، لذلك لا runtime switch. التقرير: [docs/PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md](./docs/PHASE27_39_TOPIC_ISOLATION_REPAIR_REPORT.md).
- **نتيجة Phase 27.40:** أُنشئ tokenizer v5 محمي للموضوعات الجديدة، ومرّ probe السياق `24/24` (`regression/new_topic/heldout/isolation` كلها كاملة). التقرير: [docs/PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md](./docs/PHASE27_40_TOKENIZER_CONTEXT_REPAIR_REPORT.md).
- **نتيجة Phase 27.41:** فُتح مرشح `sf_10m_phase27_40` في مسار `generator_trial=true` فقط، ومرّت بوابة HTTP الحية `22/22`: `17/17` رد مولّد و`5/5` ضوابط قالب/سلامة. التقرير: [docs/PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md](./docs/PHASE27_41_GUARDED_RUNTIME_SWITCH_REPORT.md).
- **نتيجة Phase 27.42:** وُسّعت probes الحية إلى `29/29`: الردود المثبتة بقيت مولّدة، والردود غير المطابقة حُجبت وعادت للقالب. التقرير: [docs/PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md](./docs/PHASE27_42_LIVE_UI_BROADER_PROBES_REPORT.md).
- **نتيجة Phase 27.43:** دُرّب مرشح weak-lane جديد لكنه فشل جزئيًا `10/16`; لا runtime switch، والواجهة بقيت على `sf_10m_phase27_40`. التقرير: [docs/PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md](./docs/PHASE27_43_GUARDED_DATA_BACKED_EXPANSION_REPORT.md).
- **نتيجة Phase 27.44–27.48:** tokenizer v6 ثم إصلاح conditioning لموضوعي `الوفاء/الشجاعة`; مرّ `sf_10m_phase27_47` offline `16/16` ثم live API `19/19`. زر `مولّد تجريبي` يستخدمه الآن، والافتراضي لا يزال القالب الآمن. التقرير: [docs/PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md](./docs/PHASE27_44_TO_48_RUNTIME_SWITCH_REPORT.md).
- **نتيجة Phase 27.49:** وسّعنا probes الحية إلى `33/33`، وأصلحنا كشف النصيحة السعودية لعبارة `وش تنصحني اسوي`. التقرير: [docs/PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md](./docs/PHASE27_49_BROADER_LIVE_UI_PROBES_REPORT.md).
- **نتيجة Phase 27.50:** أُزيل زر `مولّد تجريبي`، وأصبح `/chat/message` مولّدًا فقط: `7/7`، بلا قوالب في الواجهة. التقرير: [docs/PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md](./docs/PHASE27_50_GENERATOR_ONLY_UI_GATE_REPORT.md).
- **نتيجة Phase 27.51:** اختبار open-dialogue كشف أن live API نجح `3/22` وأن raw checkpoint بلا conditioning نجح `1/20` فقط على prompts طبيعية؛ التالي تدريب/إصلاح هدف حواري لا keyword expansion. التقرير: [docs/PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md](./docs/PHASE27_51_OPEN_DIALOGUE_GENERALIZATION_AUDIT_REPORT.md).
- **نتيجة Phase 27.52:** دبل تدريب آمن داخل `SF-10M`: `9200` خطوة و`6400` سجل داخلي، لكن held-out raw natural وصل `5/20` فقط؛ لا runtime switch. التقرير: [docs/PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md](./docs/PHASE27_52_NATURAL_DIALOGUE_OBJECTIVE_REPAIR_REPORT.md).
- **نتيجة Phase 27.53:** توسعة كبيرة: `10,540` زوجًا فريدًا و`18,000` خطوة، لكن raw natural وصل `2/36` فقط مع خلط/fragments؛ لا runtime switch. التقرير: [docs/PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md](./docs/PHASE27_53_NATURAL_DIALOGUE_DIVERSITY_EXPANSION_REPORT.md).
- **نتيجة Phase 27.54:** بوابة السعة/الهدف: زيادة البيانات وحدها لم تساعد، والتكبير الكامل إلى `SF-50M` ممنوع. المسموح فقط Phase 27.55 كmicro-probe تشخيصي مقارنة بـ`SF-10M`، بلا runtime. التقرير: [docs/PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md](./docs/PHASE27_54_CAPACITY_OBJECTIVITY_GATE_REPORT.md).
- **نتيجة Phase 27.55:** micro-probe مضبوط: `SF-10M=3/20`, `SF-50M=4/20`, delta=1. السعة وحدها لم تحل الحوار المفتوح، لذلك لا runtime ولا تدريب `SF-50M` كامل. التقرير: [docs/PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md](./docs/PHASE27_55_SF50M_DIAGNOSTIC_MICRO_PROBE_REPORT.md).
- **نتيجة Phase 27.56:** التشخيص وجد أن `SF-50M` يرتفع إلى `9/20` إذا أزلنا شرط overlap، لكن بقي `9` expected-missing و`9` splits حرجة في tokenizer؛ التالي إصلاح tokenizer/eval/format قبل التدريب. التقرير: [docs/PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md](./docs/PHASE27_56_OBJECTIVE_FORMAT_TOKENIZER_DIAGNOSIS_REPORT.md).
- **نتيجة Phase 27.57:** أضيفت حزمة إصلاح قبل التدريب: `18` عبارة محمية، تغطية `9/9` للعبارات الحرجة، semantic alignment بلا overlap، و5 قواعد لمنع خلط عائلات الردود. التقرير: [docs/PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md](./docs/PHASE27_57_TOKENIZER_EVAL_FORMAT_REPAIR_PACK_REPORT.md).
- **نتيجة Phase 27.58:** دُرّب tokenizer v7 مع `53` مصطلحًا/عبارة محمية ونجحت عبارات 27.57 كقطعة واحدة، لكن probe المولّد فشل `4/15`; لا runtime ولا UI. التقرير: [docs/PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md](./docs/PHASE27_58_TOKENIZER_BOUNDED_ALIGNMENT_PROBE_REPORT.md).
- **نتيجة Phase 27.59:** دُرّب repair محدود لعائلات الردود على tokenizer v7 ونجح `15/15`; لا runtime ولا UI حتى يمر canary أوسع. التقرير: [docs/PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md](./docs/PHASE27_59_BOUNDED_ALIGNMENT_REPAIR_REPORT.md).
- **نتيجة Phase 27.60:** اختبرنا checkpoint 27.59 بدون تدريب جديد على canary أوسع؛ النتيجة `12/30` فقط، لذلك لا runtime ولا UI. التقرير: [docs/PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md](./docs/PHASE27_60_BROADER_NATURAL_DIALOGUE_CANARY_REPORT.md).
- **نتيجة Phase 27.61:** repair أوسع رفع canary من `12/30` إلى `18/30`; نجحت `planning/support`، لكن `open_social/followup/topic` فشلت. التقرير: [docs/PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md](./docs/PHASE27_61_BROADER_GENERALIZATION_REPAIR_REPORT.md).
- **نتيجة Phase 27.62:** توازن العائلات بالعدد فقط تراجع إلى `10/30` لأن ترتيب corpus الكتلي سحب النموذج إلى open-social. التقرير: [docs/PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md](./docs/PHASE27_62_FAMILY_BALANCE_REPAIR_REPORT.md).
- **نتيجة Phase 27.63:** interleaved curriculum رفع canary إلى `26/30`; نجحت `open_social/planning/support` كاملة وبقيت مشاكل `topic` في `التعاون/الاحترام`. التقرير: [docs/PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md](./docs/PHASE27_63_INTERLEAVED_FAMILY_CURRICULUM_REPORT.md).
- **نتيجة Phase 27.64:** فحص tokenizer أثبت أن `التعاون` صارت `3` قطع و`الاحترام` صارت `4` قطع في v7 بعدما كانتا single-piece في v6؛ القرار tokenizer v8 قبل أي LM repair. التقرير: [docs/PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md](./docs/PHASE27_64_TOPIC_LEXICAL_TOKENIZER_INSPECTION_REPORT.md).
- **نتيجة Phase 27.65:** tokenizer v8 نجح: `التعاون/الاحترام=2/2` single-piece ومحميتين، وكل topic terms `8/8` single-piece، وboundary probes `6/6`. التقرير: [docs/PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md](./docs/PHASE27_65_TOKENIZER_V8_TOPIC_PROBE_REPORT.md).
- **نتيجة Phase 27.66:** LM repair محدود على tokenizer v8 نجح broader canary كاملًا `30/30` على followup/open_social/planning/support/topic، لكن checkpoint بقي محجوبًا عن الواجهة حتى fresh shadow canary. التقرير: [docs/PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md](./docs/PHASE27_66_V8_BOUNDED_TOPIC_REPAIR_REPORT.md).
- **نتيجة Phase 27.67:** fresh shadow canary من `50` سؤالًا جديدًا فشل `30/50`: open_social `4/10`, followup `4/10`, planning `7/10`, support `6/10`, topic `9/10`. القرار: لا واجهة ولا runtime؛ نصلح التعميم أولًا. التقرير: [docs/PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md](./docs/PHASE27_67_FRESH_SHADOW_CANARY_REPORT.md).
- **نتيجة Phase 27.68:** إصلاح موجّه لفشل 27.67 نجح على known shadow `50/50` وحافظ على regression `30/30`. القرار: لا واجهة بعد؛ نحتاج Phase 27.69 بأسئلة fresh جديدة لا يراها التدريب. التقرير: [docs/PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md](./docs/PHASE27_68_SHADOW_FAILURE_REPAIR_REPORT.md).
- **نتيجة Phase 27.69:** fresh shadow جديد `60` سؤالًا، novelty `60/60`، النتيجة `56/60`: planning/support/topic `12/12`، followup `12/12`، open_social `8/12`. القرار: لا واجهة؛ Phase 27.70 يركز على open_social. التقرير: [docs/PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md](./docs/PHASE27_69_NEW_FRESH_SHADOW_CANARY_REPORT.md).
- **نتيجة Phase 27.70:** جُرّب repair/fine-tune سيادي من checkpoint 27.68 مع open_social/stability، لكن لم يتجاوز baseline: fresh `55/60`, known `48/50`, regression `30/30`. القرار: لا واجهة ولا SF-50M؛ التالي Phase 27.71 لاختيار candidate واستراتيجية ثبات قبل أي runtime. التقرير: [docs/PHASE27_70_OPEN_SOCIAL_REPAIR_REPORT.md](./docs/PHASE27_70_OPEN_SOCIAL_REPAIR_REPORT.md).
- **نتيجة Phase 27.71:** قورنت مرشحات tokenizer v8: `phase27_66=104/140`, `phase27_68=136/140`, `phase27_70=133/140`. أفضل مرشح هو `phase27_68` لكنه لا يمر كل gates، لذلك لا واجهة ولا runtime. التالي Phase 27.72 stability-first repair. التقرير: [docs/PHASE27_71_CANDIDATE_SELECTION_REPORT.md](./docs/PHASE27_71_CANDIDATE_SELECTION_REPORT.md).
- **نتيجة Phase 27.72:** micro-repair سيادي صغير من `phase27_68` حسّن fresh إلى `58/60` وحافظ على known `50/50` وregression `30/30`. بقي فشلان open_social، لذلك runtime محجوب. التالي Phase 27.73 لفحص الفشلين. التقرير: [docs/PHASE27_72_STABILITY_FIRST_REPAIR_REPORT.md](./docs/PHASE27_72_STABILITY_FIRST_REPAIR_REPORT.md).
- **نتيجة Phase 27.73:** فحصنا فشلَي `open_social`: `open_social_09` كان شظية مولّد وجرى سد فجوة الحارس، و`open_social_12` بقي semantic collapse إلى تعريف موضوع. لا تدريب جديد ولا runtime. التالي Phase 27.74 إصلاح دلالي ضيق. التقرير: [docs/PHASE27_73_OPEN_SOCIAL_FAILURE_INSPECTION_REPORT.md](./docs/PHASE27_73_OPEN_SOCIAL_FAILURE_INSPECTION_REPORT.md).
- **نتيجة Phase 27.74:** جرّبنا ثلاثة مرشحين إصلاحيين من checkpoint 27.72. أفضل مرشح `gentle_48` حقق `56/60` fresh و`49/50` known و`30/30` regression، أي تراجع عن baseline؛ لا runtime ولا UI. التقرير: [docs/PHASE27_74_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_REPORT.md](./docs/PHASE27_74_OPEN_SOCIAL_SEMANTIC_COLLAPSE_REPAIR_REPORT.md).
- **نتيجة Phase 27.75:** فحصنا فشل 27.74 ووجدنا 5 إخفاقات كلها `open_social` بسبب `model_artifact_fragment`. tokenizer v8 يعيد `بسالفة` كـ `بس الفة`، وأضيفت حزمة حماية `protected_phrases_phase27_75.txt`. التالي tokenizer v9 probe. التقرير: [docs/PHASE27_75_OPEN_SOCIAL_STRATEGY_INSPECTION_REPORT.md](./docs/PHASE27_75_OPEN_SOCIAL_STRATEGY_INSPECTION_REPORT.md).
- **نتيجة Phase 27.76:** درّبنا tokenizer v9 فقط، بدون LM. مرّ `open_social` roundtrip `17/17`، وحزمة 27.75 كقطعة واحدة `15/15`، وبقي runtime محجوبًا. التالي Phase 27.77 تدريب LM محدود على tokenizer v9. التقرير: [docs/PHASE27_76_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_REPORT.md](./docs/PHASE27_76_TOKENIZER_V9_OPEN_SOCIAL_BOUNDARY_PROBE_REPORT.md).
- **نتيجة Phase 27.77:** درّبنا SF-10M محدودًا من الصفر على tokenizer v9. أزال tokenizer fragments لكنه خلط عائلات الردود؛ fresh `54/60`, known `45/50`, regression `30/30`. لا runtime ولا UI. التقرير: [docs/PHASE27_77_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_REPORT.md](./docs/PHASE27_77_V9_BOUNDED_OPEN_SOCIAL_LM_REPAIR_REPORT.md).
- **فصل المستخدمين:** كل export وcorpus record يحمل الآن `owner_user_id/created_by_user_id/target_user_id/user_scope`; المسار الحالي `sami-local` و`single_user` لتجهيز التوسع لاحقًا بدون خلط بيانات.
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
| Phase 22 | Gold Dialogue Corpus v2 — completed, 500/500, ready for Phase 23 tokenizer v2 |
| Phase 23 | Tokenizer v2 Retrain & Audit — completed, ready for Phase 24 |
| Phase 24 | SF-10M v0.2 Quality Training — completed with limits; runtime blocked |
| Phase 25 | Generated Chat Canary v1 — completed as guarded canary; real model blocked |
| Phase 26 | SF-50M v0.1 Readiness — completed; training blocked by scaling gates |
| Phase 27 | Dialogue Evaluation v2 and corpus expansion plan — completed; corpus gate passed |
| Phase 27.5 | SF-10M Dialogue-Format Repair — completed with limits; runtime blocked |
| Phase 27.6 | SF-10M Assistant-Target Training — completed with limits; runtime blocked |
| Phase 27.7 | Fixed Split + Gold Social Canary — completed quality gate; runtime blocked |
| Phase 27.8 | SF-10M v0.6 Split Training — numeric improvement; runtime blocked |
| Phase 27.9 | Generation Quality Harness — completed; v0.6 blocked |
| Phase 27.10 | Short Response Repair — numeric improvement; runtime blocked |
| Phase 27.11 | Objective/Decoding Diagnosis — stop boundary missing; scaling blocked |
| Phase 27.12 | Assistant Boundary/EOS Repair — partial improvement; runtime blocked |
| Phase 27.13 | SF-10M v0.8 Boundary/EOS Wider Training — eval improved; generation blocked |
| Phase 27.14 | Sovereign Training Quality Tooling Decision — adopted local quality tools |
| Phase 27.15 | Social/Lexical Curriculum + No-Repeat Decoding — eval improved; strict generation blocked |
| Phase 27.16 | Prompt-to-Answer Objective Repair — sample isolation added; runtime blocked |
| Phase 27.17 | Prompt-to-Answer Micro-Probe — 27/32 breakthrough; runtime blocked |
| Phase 27.18 | Tokenization/Decoding Hygiene Repair — blockers identified; runtime blocked |
| Phase 27.19 | Hygiene Repair Corpus/Probe — examples alone did not improve; runtime blocked |
| Phase 27.20 | Tokenizer/Protected-Phrase Strategy — protected phrase support ready for tokenizer v3; runtime blocked |
| Phase 27.21 | Tokenizer v3 Protected-Phrase Micro-Probe — tokenizer succeeded; probe failed 25/32; runtime blocked |
| Phase 27.22 | Spacing/Boundary Loss Repair — improved to 29/32; runtime blocked |
| Phase 27.23 | Semantic/Lexical Confusion Repair — improved to 30/32; runtime blocked |
| Phase 27.24 | Minimal Lexical Stabilization — micro-probe passed 32/32; runtime blocked |
| Phase 27.25 | Held-out Generation Quality Canary — failed 8/16; runtime blocked |
| Phase 27.26 | Held-out Objective Repair — improved to 9/16; runtime blocked |
| Phase 27.27 | Broader Held-out Repair — old held-out 16/16, shadow 9/16; runtime blocked |
| Phase 27.28 | Intent-Conditioned Repair — shadow improved to 12/16; runtime blocked |
| Phase 27.29 | Topic-Conditioned Definition Repair — blocked by shadow leakage |
| Phase 27.30 | Fresh Mixed Shadow Canary — failed 16/18; runtime blocked |
| Phase 27.31 | Natural Intent/Topic Dataset — natural shadow 20/20, runtime blocked |
| Phase 27.32 | Balanced Natural Calibration — calibration 12/12, runtime blocked |
| Phase 27.33 | Advice + Micro Stabilization — all local generation gates passed; guarded trial design ready |
| Phase 27.34 | Guarded Runtime Trial — request-scoped UI generator trial passed 9/9 |
| Phase 27.35 | Live UI Trial Observations — live server UI/API trial passed 10/10 |
| Phase 27.36 | Live UI Triage — quality floor active; live triage passed 27/27 |
| Phase 27.37 | Supported Topic Expansion — الصبر added behind semantic guard; live gate passed 21/21 |
| Phase 27.38 | Targeted Topic Curriculum/Probe — partial 6/20; runtime stays on 27.33 |
| Phase 27.39 | Topic-Isolation Repair — partial 10/24; tokenizer/context repair next |
| Phase 27.40 | Tokenizer/Context Repair — passed 24/24; candidate opened in guarded trial |
| Phase 27.41 | Guarded Runtime Switch — live HTTP gate passed 22/22; generator_trial uses sf_10m_phase27_40 |
| Phase 27.42 | Live UI Broader Probes — broader HTTP gate passed 29/29; misaligned generations blocked |
| Phase 27.43 | Guarded Data-Backed Expansion — weak-lane candidate partial 10/16; runtime stays on phase27_40 |
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
- لا synthetic LLM data من مصدر خارجي أو مجهول في corpus السيادي؛ يسمح فقط بحوار owner-delegated agent-authored إذا حمل provenance كاملًا وتفويض سامي.
- لا تشغيل crawling أو phase خارج الخطة بدون توثيق وإذن واضح؛ التفويض الحالي يسمح بمتابعة التدريب والمراحل المسجلة فقط مع فحص الحساسية.
- لا خلط بين `data/corpus/` و `resources/lexicons/`.
- لا تغيير في `resources/tokenization/` بدون توثيق واختبارات.

التفاصيل في [PROJECT_PRINCIPLES.md](./PROJECT_PRINCIPLES.md).

---

## الترخيص

سيُحدد لاحقًا.
