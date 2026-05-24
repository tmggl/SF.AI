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
  القرار الحالي من Phase 27.100 يمنع التدريب الجديد ويطلب Phase 27.101 diagnosis، دون runtime.
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

- المراحل من Phase 0 حتى Phase 27.100 موثقة تاريخيًا. الحالة الحالية:
  `Phase 27.100 — Bounded Topic Binding Repair Training`
  اكتملت كتدريب مقيّد وأصدرت `PHASE27_100_BOUNDED_TOPIC_BINDING_REPAIR_DECISION`.
  Phase 27.81 أضافت دفعة `sf-ai-balanced-family-pack-v1`: `2500` سجل gold
  متوازن (`500` لكل family و`250/250` فصحى/سعودي). corpus الحالي `8453`
  (`msa=4199`, `saudi=4254`, `gold=3341`, `silver=5112`). Phase 27.83 درّبت
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
  known `13/16`, fresh `5/10`, copy-anchor `18/26`, wrong-topic `0`,
  topic-family `6/10`, all-family `37/50`. runtime و`SF-50M`
  وtokenizer retrain محجوبة.
- أول خطوة تالية: Phase 27.101 Topic Binding Repair Result Diagnosis.
- تفويض التكبير التلقائي معتمد، لكن مفعوله يبدأ فقط عندما تنجح gates؛
  حاليًا `SF-50M` ما زال محجوبًا لأن capacity وزنها `1%`.
- استخدم `make phase22-review-intake` أو `GET /system/phase22-review-intake` قبل أي تحويل من `data/corpus/chat/review/` إلى corpus تدريبي.
- `phase22-review-intake` يحتوي بوابة جودة: راقب `quality_score/quality_label/quality_blockers`، ولا تحوّل جلسات قصيرة جدًا أو فيها ردود خام من `sf_10m_v0_1/sf_10m_v0_2` إلى corpus جودة.
- `/ui/chat` يحتوي مؤشر جودة تصدير محلي ويضيف `ui_quality_*` إلى metadata.
- سامي فوّض الوكيل أن يكون هو المشغّل: اختبر الواجهة/API بنفسك، ألّف وراجع واعتمد دفعات corpus بنفسك، احفظ review exports بنفسك عند الحاجة فقط، رتّب الملفات والتقارير بنفسك، ولا تطلب من سامي تنفيذ خطوات حفظ/تصدير/اعتماد أو نقل ملفات يمكن للوكيل تنفيذها. سامي يستلم النتيجة النهائية فقط.
- الواجهة المستقرة تعمل بـ `generator=template` افتراضيًا، أي قوالب ثابتة وليست مولدًا ذكيًا. لا تطلب من سامي اختبار `SF-10M v0.2` كحوار مقنع؛ هو تحسن معملي فقط حتى ينجح canary في Phase 25.
- شغّل الاختبارات كاملة بعد أي تعديل؛ آخر حالة موثقة بعد اكتمال Phase 27 يجب أن تكون كل الاختبارات ناجحة.
- السيرفر يعمل عادةً على `http://127.0.0.1:8123` (المنفذ 8000/8765 محجوز).
- شاشة المحادثة على `/ui/chat` — هي هدف سامي الرئيسي للتجريب.
- آخر تحسين مكتمل: التركيز على العربية الفصحى + السعودية فقط، توجيه الرسائل اليومية (`وشلونك`/`شكرا`/`تمام`/`لا`/`ساعدني`/`مش فاهم`/`من صنعك`/`سعودي`/`عندي؟`/`عندي سؤال`) + Phase 10 skeleton domains.
- قاموس Saudi Seed v1 (516 مدخل من تأليف سامي) في `resources/lexicons/imported/saudi_seed_v1/`.
- مصطلحات الفصحى المرشحة في `resources/tokenization/protected_terms_msa_candidate.txt` و`preferred_merges_msa_candidate.txt`; هي ليست corpus ولا pretrained vocab، بل موارد سياسة مرشحة لأي توسيع لاحق.
- اقرأ ملفات الحوكمة والدستور قبل أي تدريب: `PROJECT_CONSTITUTION`, `LANGUAGE_SEGMENTATION`, `TOKENIZATION_POLICY`, `DATASET_GOVERNANCE`, `AGENT_ENGINEERING_RULES`, ثم `PROJECT_IDENTITY`, `ENGINEERING_RULES`, `AGENT_INSTRUCTIONS`, `PROJECT_MAP`, `PROJECT_LIFECYCLE`.
- اقرأ `docs/PHASE12_TOKENIZER_V1_REPORT.md`, `docs/PHASE13_SMOKE_TRAINING_REPORT.md`, و`docs/PHASE14_SF10M_V0_1_REPORT.md`: artifacts موجودة، لكنها غير صالحة للشات أو الجودة اللغوية بعد.
- إذا كان السيرفر الحي لم يُعد تشغيله بعد، استخدم `make phase12-readiness` لنفس القرار بدون لمس السيرفر.
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وباب التوليد داخل الشات جُهّز في Phase 15. Phase 27.77 فشلت كتوليد على tokenizer v9 (`54/60`, `45/50`, `30/30`). Phase 27.78 شخّصت root cause: family mixing `22%`, objective `18%`, curriculum `16%`, weak generalization `14%`, semantic routing `10%`, capacity `1%`. Phase 27.79 صممت إصلاح objective/curriculum/decoding، Phase 27.80 شفّرت gates، Phase 27.81 أصلحت توازن family ببيانات gold، Phase 27.82 سمحت بتدريب مقيّد، Phase 27.83 أثبتت أن الإصلاح لم ينجح حواريًا (`11/60` best)، Phase 27.84 حددت أن family signal غائب من النص، Phase 27.85 صممت الإشارة، Phase 27.86 أثبتت renderer/masking، Phase 27.87 أثبتت أن التدريب ما زال منحازًا (`10/50` best)، Phase 27.88 حددت السبب: ترتيب stream متسلسل لا round-robin، Phase 27.89 ثبّتت sampler متوازنًا، Phase 27.90 حسّنت النتيجة إلى `35/50`، Phase 27.91 حددت أن المشكلة topic-specific، Phase 27.92 صممت إصلاح topic-objective، Phase 27.93 رمزت البوابة، Phase 27.94 سدّت فجوة `الوفاء` السعودية، Phase 27.95 أثبتت أن التدريب المحدود لم يكفِ، Phase 27.96 شخّصت السبب كخلل binding للموضوع، Phase 27.97 صممت objective copy/contrastive، Phase 27.98 منعت التدريب حتى إصلاح metadata، Phase 27.99 أصلحت metadata، وPhase 27.100 درّبت إصلاح ربط الموضوع لكنها لم تمر gates (`13/16`, `5/10`, `18/26`, `37/50`). التالي Phase 27.101 تشخيص بلا تدريب.
- تفويض سامي الأخير يعني أن حوار الوكيل المؤلف لخدمة corpus يمكن اعتماده كـ `owner-delegated agent-authored` مع `training_allowed=true` إذا حمل source/license/quality/notes كاملة، وبقي ضمن `msa + saudi` ودون أي مصدر خارجي أو pretrained data.
- كل export أو corpus record يجب أن يحمل user ownership. المسار الحالي: `owner_user_id=created_by_user_id=target_user_id=sami-local` و`user_scope=single_user`.

**هدف سامي الرئيسي الآن:**

> شاشة محادثة عربية مريحة، توجيه دقيق للأسئلة، بدون أي عقل أجنبي.

**أول ما تفعل بعد قراءة SF_AI_MASTER_GUIDE.md:**

1. شغّل الاختبارات للتأكد من سلامة الحالة:
   ```
   cd /Users/sami/workSF/SF.AI && .venv/bin/python -m pytest tests
   ```

2. تحقق من القسم 4 في AGENT_HANDOFF.md. مهمة "محادثة مريحة + توجيه دقيق" مكتملة، ومسار العمل الحالي هو Phase 27.101 بعد فشل runtime gates في 27.100.

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
