# NEXT_AGENT_PROMPT.md

## برومت جاهز للنسخ — للوكيل التالي

> **استخدام:** إذا فتح المستخدم سامي جلسة جديدة وأراد متابعة بناء SF.AI، يلصق المحتوى تحت السطر الفاصل في الشات.

---

أنت وكيل برمجي يكمل بناء مشروع SF.AI.

**قبل أي شيء، اقرأ كاملاً:**

```
/Users/sami/workSF/SF.AI/docs/SF_AI_MASTER_GUIDE.md
```

ثم استكشف:
- `/Users/sami/workSF/SF.AI/docs/AGENT_HANDOFF.md` — سجل التسليم التاريخي التفصيلي.
- `/Users/sami/workSF/SF.AI/PROJECT_PRINCIPLES.md` — المبادئ الحاكمة.
- `/Users/sami/workSF/SF.AI/docs/PHASE_STATUS.md` — أين نحن الآن.
- `/Users/sami/workSF/SF.AI/docs/EXECUTION_PLAN.md` — الخطة الكاملة على مراحل.

**القواعد الذهبية (لا تكسرها):**

1. لا تستورد أي LLM خارجي ولا أي pretrained weights/embeddings/tokenizer.
   لا Qwen ولا Llama ولا Mistral ولا Gemma ولا أي open-weight pretrained
   model داخل runtime أو التدريب الأساسي.
2. لا تشغّل crawler أو مصدر خارجي بدون provenance واضح واحترام بوابة permission.
3. لا تنتقل خارج المراحل المسجلة في الخطة بدون توثيق السبب.
4. كل قاموس مستورد له إذن موثَّق (انظر `docs/SOURCE_DISCOVERY_*.md`).
5. الرد بالعربية الواضحة. حازم في التنفيذ، شفاف في النتائج.
6. اتبع **Sovereign Practical Acceleration Strategy v2**: استخدم أدوات هندسية
   عامة مسموحة لتسريع العمل، ولا تدخل عقلًا جاهزًا أو بيانات خارجية.

**Sovereign Practical Acceleration Strategy v2:**

- مسموح: PyTorch، TensorBoard/logs محلية، schedulers، AMP/mixed precision،
  experiment tracking، advanced decoding، repetition control، curriculum tooling،
  held-out canary، shadow canary، family-conditioned dialogue، contrastive
  evaluation، semantic routing diagnostics، objective tracing، anti-collapse
  diagnostics، local RLHF-lite/DPO/ORPO/preference optimization، LoRA/QLoRA على
  أوزان SF.AI فقط، retrieval memory tooling، local vector retrieval، dialogue
  family balancing، EOS boundary tooling، checkpoint selector، tokenizer boundary audit.
- ممنوع: pretrained weights، pretrained vocab، pretrained tokenizer merges،
  open-weight pretrained models، Qwen/Llama/Mistral/Gemma runtime، external
  dialogue datasets، hidden hosted APIs، external reasoning services،
  project-workflow dialogue contamination، fake benchmark inflation، template masking.
- تفسير ملزم: التسريع السيادي يعني أدوات هندسية وتشخيصية وتدريبية، وليس
  Open-Weight Lane أو fine-tune فوق عقل جاهز.
- السيادة تبقى على corpus/tokenizer/behavior/runtime/alignment/evaluation
  وسلوك الحوار الفصيح والسعودي.
- قبل أي تدريب جديد يجب وجود root-cause/decision gate حديث يسمح به صراحة.
  القرار الحالي هو `PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION`:
  المسار أُعيد تثبيته عند Phase 27.79، ومرّت بوابات Phase 27.80، ثم اكتمل
  تدريب Phase 27.81. Phase 27.105 أثبت أن الواجهة تستدعي المولد الحقيقي
  في raw lab، لكنه شخّص فشل social subfamilies وtopic variants؛ التالي
  Phase 27.106 design أضاف renderer signals، وPhase 27.107 مرّر gate؛
  Phase 27.108 كتب `480` سجل gold ومرّ corpus-audit؛ Phase 27.109 صنّف
  مصادر مجانية مثل Masader/Qabas/Tashkeela وسحب Masader metadata summary فقط؛
  Phase 27.110 صمم license matrix وحدد Qabas كمسار lexicon/topic فقط؛
  Phase 27.111 صمم Qabas bootstrap لكنه حجب الاستيراد بسبب تضارب الترخيص؛
  Phase 27.112 حسم Qabas كـ reference-only بسبب `CC-BY-ND-4.0`؛
  Phase 27.113 صنف البدائل وسمح فقط بـ source cards لـ Arabic Ontology وSynonyms.
  Phase 27.114 أنشأ source cards وlicense matrix، بلا import.
  Phase 27.115 حسم artifact gate: Arabic Ontology محجوب لأنه request-only،
  وSinaLab Synonyms مرصود لكن import محجوب حتى quarantine checksum/schema dry-run.
  Phase 27.116 نزّل SinaLab Synonyms في quarantine محلي git-ignored وسجل
  checksum/schema فقط دون import أو تدريب.
  Phase 27.117 فحص sample quality/dedupe بأرقام فقط دون raw terms أو corpus.
  Phase 27.118 صمم reference extraction كطبقة مرجعية فقط دون raw terms في git.
- لا runtime release بدون `NO_RUNTIME_RELEASE_WITHOUT_HELDOUT_SUCCESS`.
- لا تعتمد loss/perplexity/micro-probe وحدها؛ النجاح يعني held-out dialogue
  quality, runtime usability, clean-stop, semantic correctness, family
  stability, open_social naturalness, followup continuity, canary pass rate,
  وhuman conversation realism.
- **Auto-Advance Scaling Mandate:** إذا نجحت بوابة الحجم التالي، انتقل
  تلقائيًا دون انتظار موافقة جديدة عبر:
  `SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+`.
  لا تكبر عند فشل gate، ولا تقفز فوق السلم.

**الحالة الراهنة باختصار:**

- المراحل من Phase 0 حتى Phase 27.118 موثقة تاريخيًا، لكن الحالة العملية
  الحالية هي:
  `Phase 27.118 — Synonyms Reference Extraction Design`
  ضمن `SF-native Objective/Curriculum/Decoding Acceleration Track`.
  التقرير الملزم: `docs/PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN.md`.
  القرار التنفيذي:
  `PHASE27_118_SINALAB_SYNONYMS_REFERENCE_EXTRACTION_DESIGN_DECISION`.
  Phase 27.104 تبقى الدليل السابق: تدريب محدود نجح topic-wise وفشل
  all-family، وليست إذن runtime.
  تاريخيًا أضيفت دفعة `sf-ai-balanced-family-pack-v1`: `2500` سجل gold
  متوازن (`500` لكل family و`250/250` فصحى/سعودي). corpus الحالي `9125`
  (`msa=4535`, `saudi=4590`, `gold=4013`, `silver=5112`). Phase 27.83 درّبت
  checkpoints `step600/1200/1800`، لكن best fresh shadow = `11/60` فقط.
  Phase 27.84 شخّصت السبب: `dialogue_family` موجودة في metadata لكنها لا تظهر
  داخل نص التدريب. Phase 27.85 صممت الصيغة، وPhase 27.86 أثبتت أن
  `render_dialogue_text` يطبع `عائلة الحوار: سوالف/متابعة/تنظيم/دعم/موضوع`
  في مساري no-split وsplit-manifest مع masking صحيح. Phase 27.87 درّبت
  SF-10M مقيّدًا بهذه الإشارة، لكن أفضل نتيجة fresh shadow = `10/50`.
  Phase 27.88 أثبتت أن السبب الأكبر sequential curriculum collapse:
  `موضوع` ظهر 5 مرات فقط في أول 1800 عينة. Phase 27.89 أضافت
  `--split-order family_round_robin` ومرّت dry-run: أول 1800 عينة = `360`
  لكل family، وكل نافذة 600 = `120` لكل family. Phase 27.90 درّبت SF-10M
  بهذا الترتيب: best fresh shadow = `35/50` عند `sf-10m-step1800`. Phase 27.91
  شخّصت الفشل المتبقي: `9/15` إخفاقًا من عائلة topic، و`topic_semantic_collapse=48%`.
  Phase 27.92 صممت objective مخصصًا: `topic_anchor_prompt_to_answer_objective_v1`
  مع شرط `الموضوع المطلوب: <topic_term>` وبوابات canary واضحة. Phase 27.93
  أضافت السطر فعليًا إلى renderer، ومرّت dry-run للـ renderer/masking/canary.
  Phase 27.94 أضافت `10` سجلات سعودية gold لموضوع `الوفاء` وأعادت البوابة:
  `training_data_ready=true`, `shortfalls={}`. Phase 27.95 دربت إصلاحًا
  محدودًا من أفضل checkpoint في 27.90، لكن النتائج لم تمر: known topic `10/16`,
  fresh topic `4/10`, all-family `33/50`. Phase 27.96 شخّصت السبب كخلل
  ربط متغير الموضوع: `wrong_topic_substitution_count=11`، وأكثر بديل خاطئ
  `الصداقة=6`. Phase 27.97 صممت objective
  `topic_copy_contrastive_binding_objective_v1`: ينسخ الموضوع المطلوب داخل
  أول 12 حرفًا عربيًا ظاهرًا من رد المساعد، ويمنع ذكر موضوع مجاور قبل المطلوب.
  Phase 27.98 رمّزت البوابة ووجدت أن `500` سجل topic لا تحمل `topic_term`
  صريحًا، ثم Phase 27.99 أصلحتها وأعادت بوابة 27.98 إلى `training_ready=true`.
  Phase 27.100 درّبت إصلاح ربط الموضوع، لكن best checkpoint لم يمر gates:
  known `13/16`, fresh `5/10`, copy-anchor `18/26`, reported wrong-topic `0`,
  topic-family `6/10`, all-family `37/50`. Phase 27.101 كشف blind spot:
  observed wrong-topic `8` (`الصداقة=7`, `الامتنان=1`). Phase 27.102 ثبّت
  بوابة observed wrong-topic/copy-anchor وcanary من 16 prompt. Phase 27.103 أضافت
  حزمة `192` سجلًا `gold` متوازنة مع wrong-topic leak=`0`. Phase 27.104 درّبت
  الحزمة تدريبًا محدودًا: prototype `16/16`, observed wrong-topic `0`,
  known `16/16`, fresh `9/10`, topic-family `9/10`, all-family `30/50`.
  Phase 27.81 درّبت من أفضل checkpoint في 27.104 إلى `sf-10m-step2000`:
  all-family `42/50`, topic family `10/10`, prototype `16/16`, known `16/16`,
  fresh `9/10`. Runtime و`SF-50M` وtokenizer retrain محجوبة.
  Phase 27.105 فتح raw UI lab محليًا فقط: `الصداقه` صارت تمر كموضوع
  normalized إلى المولد، لكن `السلام عليكم` و`الاخوه` تكشف أن social
  subfamilies وtopic variants تحتاج objective design.
  Phase 27.106 أضاف `dialogue_subfamily`, `topic_canonical`, `topic_variant`
  وrenderer line `نوع السوالف: ...`.
  Phase 27.107 مرّر gate التنفيذية وأثبت canary الرسمي. Phase 27.108
  أضاف `480` سجلًا gold، وصار corpus الحالي `9125` سجلًا
  (`msa=4535`, `saudi=4590`, `gold=4013`, `silver=5112`)، ومرّ
  `make corpus-audit` بلا مشاكل. Phase 27.109 صنّف مصادر مجانية جاهزة:
  Masader metadata، Qabas، Tashkeela، OSIAN، Arabic Learner Corpus، fr3on،
  ArSyra؛ ولم يدخل أي نص خارجي إلى corpus. Phase 27.110 صمم مصفوفة ترخيص:
  Qabas مسموح كـ lexicon/topic/protected-terms فقط، وتدريب Tashkeela محجوب.
  Phase 27.111 حجب import Qabas الفعلي بسبب تضارب `Apache-1.0` و`CC-BY-ND-4.0`.
  Phase 27.112 أبقى Qabas reference-only وفتح طريق البدائل permissive.
  Phase 27.113 صنف Arabic Ontology/Synonyms كمرشحين source-card فقط، وحجب
  Arabic WordNet 4.0 لأنه model-derived.
  Phase 27.114 أنشأ source cards وlicense matrix للمرشحين، ولا يوجد import.
  Phase 27.115 حسم artifact gate وfield mapping: Arabic Ontology محجوب،
  وSinaLab Synonyms مسموح فقط لـ quarantine checksum/schema dry-run.
- Phase 27.116 حسم quarantine checksum وschema dry-run؛ لا raw rows محفوظة
  ولا data/corpus ولا tokenizer ولا training.
- Phase 27.117 حسم sample quality/dedupe: `3010` candidate rows، `1697`
  unique normalized terms، بلا raw terms منشورة.
- Phase 27.118 حسم design: reference layer فقط، no raw terms in git، no corpus،
  no tokenizer، no training.
- أول خطوة تالية: Phase 27.119 — Synonyms Reference Extraction Dry-Run Counts, no training.
  لا تبدأ training ولا SF-50M ولا tokenizer retrain قبل هذه البوابة.
- تفويض التكبير التلقائي معتمد، لكن مفعوله يبدأ فقط عندما تنجح gates؛
  حاليًا `SF-50M` ما زال محجوبًا لأن capacity وزنها `1%`.
- استخدم `make phase22-review-intake` أو `GET /system/phase22-review-intake` قبل أي تحويل من `data/corpus/chat/review/` إلى corpus تدريبي.
- `phase22-review-intake` يحتوي بوابة جودة: راقب `quality_score/quality_label/quality_blockers`، ولا تحوّل جلسات قصيرة جدًا أو فيها ردود خام من `sf_10m_v0_1/sf_10m_v0_2` إلى corpus جودة.
- `/ui/chat` يحتوي مؤشر جودة تصدير محلي ويضيف `ui_quality_*` إلى metadata.
- سامي فوّض الوكيل أن يكون هو المشغّل: اختبر الواجهة/API بنفسك، ألّف وراجع واعتمد دفعات corpus بنفسك، احفظ review exports بنفسك عند الحاجة فقط، رتّب الملفات والتقارير بنفسك، ولا تطلب من سامي تنفيذ خطوات حفظ/تصدير/اعتماد أو نقل ملفات يمكن للوكيل تنفيذها. سامي يستلم النتيجة النهائية فقط.
- الواجهة المستقرة لا يجوز أن تعرض المولد لسامي إلا بعد نجاح held-out/all-family/runtime gates. بعد Phase 27.104 ما زال runtime محجوبًا؛ لا تطلب من سامي اختبار المولد كحوار مقنع حتى يصدر release decision صريح.
- شغّل الاختبارات كاملة بعد أي تعديل؛ آخر حالة موثقة بعد اكتمال Phase 27 يجب أن تكون كل الاختبارات ناجحة.
- السيرفر يعمل عادةً على `http://127.0.0.1:8123` (المنفذ 8000/8765 محجوز).
- شاشة المحادثة على `/ui/chat` — هي هدف سامي الرئيسي للتجريب.
- آخر تحسين مكتمل: التركيز على العربية الفصحى + السعودية فقط، توجيه الرسائل اليومية (`وشلونك`/`شكرا`/`تمام`/`لا`/`ساعدني`/`مش فاهم`/`من صنعك`/`سعودي`/`عندي؟`/`عندي سؤال`) + Phase 10 skeleton domains.
- قاموس Saudi Seed v1 (516 مدخل من تأليف سامي) في `resources/lexicons/imported/saudi_seed_v1/`.
- مصطلحات الفصحى المرشحة في `resources/tokenization/protected_terms_msa_candidate.txt` و`preferred_merges_msa_candidate.txt`; هي ليست corpus ولا pretrained vocab، بل موارد سياسة مرشحة لأي توسيع لاحق.
- اقرأ ملفات الحوكمة والدستور قبل أي تدريب: `PROJECT_CONSTITUTION`, `LANGUAGE_SEGMENTATION`, `TOKENIZATION_POLICY`, `DATASET_GOVERNANCE`, `AGENT_ENGINEERING_RULES`, ثم `PROJECT_IDENTITY`, `ENGINEERING_RULES`, `AGENT_INSTRUCTIONS`, `PROJECT_MAP`, `PROJECT_LIFECYCLE`.
- اقرأ `docs/PHASE12_TOKENIZER_V1_REPORT.md`, `docs/PHASE13_SMOKE_TRAINING_REPORT.md`, و`docs/PHASE14_SF10M_V0_1_REPORT.md`: artifacts موجودة، لكنها غير صالحة للشات أو الجودة اللغوية بعد.
- إذا كان السيرفر الحي لم يُعد تشغيله بعد، استخدم `make phase12-readiness` لنفس القرار بدون لمس السيرفر.
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وباب التوليد داخل الشات جُهّز في Phase 15. Phase 27.78 شخّصت root cause: family mixing `22%`, objective `18%`, curriculum `16%`, weak generalization `14%`, semantic routing `10%`, capacity `1%`. بعد سلسلة إصلاحات حتى Phase 27.104، نجحت topic gates لكنها فشلت all-family `30/50`. المسار الحالي أُعيد تثبيته عند Phase 27.79 بخطة `PHASE27_OBJECTIVE_CURRICULUM_DECODING_PLAN`; Phase 27.80 مرّرت البوابات التنفيذية؛ Phase 27.81 رفعت all-family إلى `42/50` لكنها لم تبلغ runtime gate.
- تفويض سامي الأخير يعني أن حوار الوكيل المؤلف لخدمة corpus يمكن اعتماده كـ `owner-delegated agent-authored` مع `training_allowed=true` إذا حمل source/license/quality/notes كاملة، وبقي ضمن `msa + saudi` ودون أي مصدر خارجي أو pretrained data.
- كل export أو corpus record يجب أن يحمل user ownership. المسار الحالي: `owner_user_id=created_by_user_id=target_user_id=sami-local` و`user_scope=single_user`.

**هدف سامي الرئيسي الآن:**

> شاشة محادثة عربية مريحة، توجيه دقيق للأسئلة، بدون أي عقل أجنبي.

**أول ما تفعل بعد قراءة SF_AI_MASTER_GUIDE.md:**

1. شغّل الاختبارات للتأكد من سلامة الحالة:
   ```
   cd /Users/sami/workSF/SF.AI && .venv/bin/python -m pytest tests
   ```

2. تحقق من القسم 4 في AGENT_HANDOFF.md. مهمة "محادثة مريحة + توجيه دقيق" مكتملة، ومسار العمل الحالي هو Phase 27.81 تدريب محدود مكتمل، والتالي Phase 27.82 diagnosis، بلا runtime ولا SF-50M.

3. Phase 11 مكتملة كحوكمة وأداة فحص. شغّل:
   ```
   make source-inventory
   ```
   هذا يريك كل المراجع المحلية: chat corpus، ملف مهام اللهجة السعودية، قاموس Saudi Seed، وMo3jam slot.

4. ثم شغّل:
   ```
   make corpus-audit
   ```
   يوجد الآن seed سعودي صغير، وجرى تدريب tokenizer v1 وLM runs منه بإذن سامي. لا تعامله كجودة لغوية متوازنة ولا تربطه بالشات.

5. التفويض الحالي: سامي أعطى إذنًا صريحًا لمتابعة التنفيذ والاختبارات. لا تنتظر إذنًا جديدًا، لكن اتبع SPA v2: لا تضف تدريبًا إلا بعد gate واضح، ولا تكبر النموذج إلا إذا صدر `SF-50M JUSTIFIED TRANSITION`.

**أسلوب التواصل المتفق عليه:**

- عند إنهاء أي مرحلة: أعطِ ملخصًا عربيًا يتضمن رقم الرحلة، القاموس المتبع، الاختبارات، وهل تم الرفع.
- عند الشك في مصدر خارجي أو مخاطرة حساسة: **توقّف واسأل سامي**. لا تخمن.

---

ابدأ الآن.
