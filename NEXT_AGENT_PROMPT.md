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
- قبل أي تدريب جديد يجب وجود `ENGINEERING_ROOT_CAUSE_GATE` وقرار
  `PHASE27_79_REPAIR_DESIGN_DECISION` ثم gates ناجحة من Phase 27.80.
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

- المراحل من Phase 0 حتى Phase 27.79 موثقة تاريخيًا. الحالة الحالية:
  `Phase 27.80 — Repair Gate Encoding and Dry-Run Validation` شُغلت بلا تدريب
  وأصدرت `PHASE27_80_REPAIR_GATE_VALIDATION_DECISION`. النتيجة: gates فشلت
  بسبب family imbalance وfamily confusion، لذلك لا runtime switch ولا `SF-50M`
  ولا تدريب جديد. corpus الحالي `5943` (`msa=2949`, `saudi=2994`).
- أول خطوة تالية: Phase 27.80 remediation لتوازن
  `open_social/followup/planning/support/topic` قبل أي تدريب.
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
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وباب التوليد داخل الشات جُهّز في Phase 15. Phase 27.77 فشلت كتوليد على tokenizer v9 (`54/60`, `45/50`, `30/30`). Phase 27.78 شخّصت root cause: family mixing `22%`, objective `18%`, curriculum `16%`, weak generalization `14%`, semantic routing `10%`, capacity `1%`. Phase 27.79 صممت إصلاح objective/curriculum/decoding. الخطوة التالية هي Phase 27.80 لتشفير gates وتشغيل dry-run، لا تدريب ولا تكبير.
- تفويض سامي الأخير يعني أن حوار الوكيل المؤلف لخدمة corpus يمكن اعتماده كـ `owner-delegated agent-authored` مع `training_allowed=true` إذا حمل source/license/quality/notes كاملة، وبقي ضمن `msa + saudi` ودون أي مصدر خارجي أو pretrained data.
- كل export أو corpus record يجب أن يحمل user ownership. المسار الحالي: `owner_user_id=created_by_user_id=target_user_id=sami-local` و`user_scope=single_user`.

**هدف سامي الرئيسي الآن:**

> شاشة محادثة عربية مريحة، توجيه دقيق للأسئلة، بدون أي عقل أجنبي.

**أول ما تفعل بعد قراءة SF_AI_MASTER_GUIDE.md:**

1. شغّل الاختبارات للتأكد من سلامة الحالة:
   ```
   cd /Users/sami/workSF/SF.AI && .venv/bin/python -m pytest tests
   ```

2. تحقق من القسم 4 في AGENT_HANDOFF.md. مهمة "محادثة مريحة + توجيه دقيق" مكتملة، لكن مسار العمل الحالي هو Phase 27.80 بعد تصميم 27.79.

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
