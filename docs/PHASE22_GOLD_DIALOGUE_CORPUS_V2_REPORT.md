# PHASE22_GOLD_DIALOGUE_CORPUS_V2_REPORT.md

## SF.AI — Phase 22 Gold Dialogue Corpus v2

**Journey:** Phase 22 / 30  
**Status:** readiness gate active; corpus not ready  
**Language track:** Arabic MSA + Saudi only  
**Lexicon track:** Saudi Seed v1 as reference, not direct chat corpus  
**Training started:** no

---

## القرار الهندسي

Phase 22 لا يبدأ تدريب tokenizer أو نموذج.

هذه المرحلة تبني بوابة corpus v2 حتى نعرف بدقة:

- كم سجل حوار جاهز لدينا.
- كم ينقص للوصول إلى 500 سجل.
- هل يوجد توازن بين `msa` و`saudi`.
- هل السجلات gold/silver ومصرح بها للتدريب.
- هل يوجد أي كسر في الحوكمة.

---

## كيف تُضاف محادثات الوكيل الآن؟

دستور SF.AI يمنع `synthetic LLM data` من مصادر خارجية أو مجهولة.

بعد تصريح سامي بتاريخ 2026-05-23، حوار الوكيل المؤلف خصيصًا لهذا المشروع
يمكن دخوله corpus إذا كان **owner-delegated agent-authored** وموثقًا بالكامل:

- source واضح يبدأ بـ `sf-ai-owner-delegated-agent-authored-`.
- license واضح: `owner-approved-for-sf-ai-training`.
- quality افتراضيًا `silver`.
- training_allowed=true.
- owner_user_id/created_by_user_id/target_user_id واضحة.
- user_scope=single_user في المسار الحالي.
- notes تذكر التفويض وتؤكد عدم وجود dataset خارجي أو pretrained model data.

الطريق الصحيح:

```text
تأليف/اختبار محادثة ضمن msa أو saudi
→ توثيق source/license/quality/notes
→ corpus-audit
→ phase22-readiness
```

---

## بوابة Phase 22

أضيف:

- `make phase22-readiness`
- `make phase22-plan`
- `make phase22-next-batch`
- `make phase22-completion-gate`
- `make phase22-review-intake`
- `GET /system/phase22-readiness`
- `GET /system/phase22-collection-plan`
- `GET /system/phase22-next-batch`
- `GET /system/phase22-completion-gate`
- `GET /system/phase22-review-intake`
- `/ui/chat` يعرض لوحة بوابة Phase 22 الحية من `/system/phase22-readiness`.
- `/system/phase22-collection-plan` يرجع الآن `planned_batches` مفصلة لكل batch.
- `sf_ai/datasets/phase22_readiness.py`
- `sf_ai/datasets/phase22_review_intake.py`

القيم الحالية المتوقعة:

```text
training_records: 380
target_records: 500
remaining_records: 120
dialect_counts: {"msa": 200, "saudi": 180}
missing_required_dialects: []
status: NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2
can_start_phase23: false
synthetic_llm_data_allowed: false
completion_gate: PHASE22_INCOMPLETE_DO_NOT_ADVANCE
```

وخطة الجمع الحالية:

```text
remaining_records: 120
batch_size: 25
estimated_batches: 5
quota_by_dialect: {"saudi": 20}
flexible_records_after_minimums: 100
planned_batches: 5
next_batch: saudi_007, dialect=saudi, target_records=20
```

`phase22-next-batch` يعرض المهمة الفورية للتأليف/المراجعة:

- batch الحالي: `saudi_007`.
- الهدف: 20 سجلًا سعوديًا.
- يعرض checklist قبول قبل التحويل.
- يعرض موضوعات عامة تساعد التأليف/المراجعة؛ هذه الموضوعات ليست corpus ولا synthetic dialogue.
- يقرأ بنك موضوعات فصيح غير تدريبي من `resources/phase22_authoring/msa_prompt_bank_v1.json`.
- بعد التأليف المباشر: `validate_dataset.py` ثم `corpus-audit` ثم `phase22-readiness`. مسار `phase22-review-intake` و`prepare-dialogue-batch` يبقى اختياريًا للمواد القادمة من الواجهة فقط.
- شاشة `/ui/chat` تعرض هذه المهمة مباشرة وتضيف `phase22_next_batch` إلى `review_metadata` عند التصدير.

بنك التأليف الفصيح:

- يحتوي 80+ موضوعًا فصيحًا لتغطية batches الفصحى.
- `training_allowed=false`.
- `synthetic_llm_data=false`.
- `corpus_record=false`.
- لا يُنسخ إلى `data/corpus/chat/jsonl`; هو دليل كتابة فقط.

`phase22-completion-gate` هو مانع الانتقال النهائي:

- يرجع حاليًا `PHASE22_INCOMPLETE_DO_NOT_ADVANCE`.
- يجمع readiness + collection plan + next batch في قرار واحد.
- لا يسمح بالانتقال إلى Phase 23 إلا بعد `PHASE22_COMPLETE_READY_FOR_PHASE23`.
- يذكر النواقص الحالية مثل `corpus_below_phase22_target`, `dialect_balance_below_minimum`, و`complete_next_batch:saudi_007`.

تفصيل batches الرسمي:

- `msa_001` إلى `msa_008` اكتملت: 178 سجل فصيح owner-delegated agent-authored.
- `protected_terms_msa_seed_v1` اكتمل: 22 سجلًا فصيحًا `gold` لتغطية مصطلحات التوكننة/الحوكمة.
- `msa_008` اكتملت: 3 سجلات فصيحة، وأصبح الحد الأدنى للفصحى مكتملًا.
- `saudi_001` إلى `saudi_006` اكتملت: 150 سجلًا سعوديًا owner-delegated agent-authored.
- `saudi_007`: تغطية سعودية، 20 سجلًا.
- `saudi_007`: تغطية سعودية، 20 سجلًا.
- `flex_001` إلى `flex_004`: 100 سجل مرن بعد اكتمال الحد الأدنى.

ومسار review intake الحالي:

```text
review_path: data/corpus/chat/review
review_files: 1
candidate_files: 1
average_quality_score: 60.0
synthetic_llm_data_allowed: false
status: REVIEW_EXPORTS_READY_FOR_MANUAL_REVIEW
```

أضيفت بوابة جودة للحوار داخل `phase22-review-intake`:

- `quality_score` من 0 إلى 100.
- `quality_label`: مثل `gold_candidate`, `silver_candidate`, `needs_more_turns_or_review`.
- `quality_blockers`: مثل قصر المحادثة أو وجود ردود `sf_10m_v0_1`.

وأضيف مؤشر جودة مباشر داخل شاشة `/ui/chat`:

- يعرض score قبل التصدير.
- يحذر إذا كانت الجلسة أقل من 3 أدوار منك و3 ردود من المساعد.
- يضع `ui_quality_score`, `ui_quality_label`, `ui_quality_blockers` في ملف export.

وأضيفت لوحة بوابة Phase 22 داخل الشاشة نفسها:

- تعرض عدد سجلات corpus الحالي مقابل هدف 500.
- تعرض المتبقي ونقص `msa/saudi`.
- توضّح أن Phase 23 لا تبدأ حتى تمر بوابة corpus.

وأضيفت لوحة مهمة الجمع الحالية داخل الشاشة نفسها:

- تعرض `saudi_007` وهدف 20 سجلًا.
- تعرض موضوعات تأليف عامة لا تُعد بيانات تدريب.
- تعرض زر `موضوعات أخرى` للتنقل في بنك الموضوعات الفصيح بدل حصر سامي في أول ثلاثة موضوعات.
- تربط export بالـ batch عبر `review_metadata.phase22_next_batch`.
- تضع `authoring_topic_count` داخل metadata حتى نعرف حجم بنك التأليف المعروض وقت التصدير.

وأضيف حفظ محلي للمراجعة:

- زر `حفظ للمراجعة` في `/ui/chat`.
- endpoint: `POST /chat/review-export`.
- يحفظ JSONL داخل `data/corpus/chat/review/` فقط.
- يرفض أي payload فيه `training_allowed=true`.
- يحفظ دائمًا بحالة `saved_for_manual_review_only`.
- هذا المسار اختياري للتشخيص أو التجارب؛ سامي لا يحتاج إلى حفظ أو تصدير يدوي كي تتقدم Phase 22، لأن الوكيل يؤلف ويراجع ويعتمد الدفعات مباشرة عند وضوح الجودة.

القاعدة العملية للوصول إلى حوار مفيد للتدريب:

- لا تعتمد جلسة قصيرة جدًا كبيانات تدريب؛ فضّل 3 أدوار مستخدم و3 ردود مساعد على الأقل.
- لا تستخدم جلسة فيها `مولّد: نموذج SF-10M` كبيانات جودة.
- فضّل موضوعًا واحدًا واضحًا في كل جلسة.
- اجعل الردود المؤلفة/المعتمدة بتفويض واضح فقط تدخل corpus.

---

## أهداف Phase 22

الهدف الأدنى:

- 500 سجل حوار محكوم.
- `msa` و`saudi` موجودان.
- 200 سجل على الأقل لكل من `msa` و`saudi`.
- `quality ∈ {gold, silver}`.
- `training_allowed=true`.
- source/license موجودان.

---

## كيف يجمع المشروع corpus الآن؟

المسار الأساسي منذ تفويض سامي الأخير:

```text
الوكيل يؤلف دفعة msa/saudi مباشرة
→ يوسمها كـ owner-delegated agent-authored
→ يثبت owner_user_id/created_by_user_id/target_user_id/user_scope
→ يشغل validate_dataset.py
→ يشغل corpus-audit + phase22-readiness + tests
→ يحدّث التقارير ويرفع فقط إذا نجح كل شيء
```

الواجهة تبقى مختبرًا اختياريًا فقط. لا يُطلب من سامي حفظ أو تصدير أو اعتماد ملفات يدوية.

أمثلة مفيدة للتجربة الاختيارية في الواجهة:

```text
خلنا نسولف شوي
وش رايك في التعلم اليومي؟
اشرح لي الفرق بين القالب والمولد
اكتب لي رد قصير لصديق
رتب لي فكرة مشروع صغير
```

للفصحى:

```text
أريد أن أختبر قدرتك على الحوار العربي الفصيح.
اشرح لي خطوتنا التالية باختصار.
ما الفرق بين تدريب النموذج وتفعيل النموذج؟
```

لو استخدم الوكيل الواجهة كاختبار اختياري، فالجلسة الأقوى تكون 3–6 أدوار:

```text
1. افتح موضوعًا واحدًا.
2. اطلب توضيحًا أو مثالًا.
3. اسأل متابعة قصيرة.
4. إن كان الرد مفهومًا، يحفظها الوكيل للمراجعة بنفسه عند الحاجة.
```

لو وُجد ملف review اختياري، لا يدخل التدريب حتى يُراجع ويُحضّر. أما الدفعات المباشرة فيكفي تحقق schema/audit/tests:

```bash
make phase22-review-intake

make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_001.jsonl --quality silver --dialect saudi --training-allowed"
```

أو للدفعة السعودية التالية:

```bash
make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_saudi_007.jsonl --quality silver --dialect saudi --training-allowed"
```

وللمسار المباشر:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_saudi_007.jsonl
make corpus-audit
make phase22-readiness
```

---

## متى ننتقل إلى Phase 23؟

فقط عندما:

```bash
make corpus-audit
make phase22-readiness
make phase22-plan
make phase22-review-intake
```

يعطيان:

- لا issues.
- `training_records >= 500`.
- لا `missing_required_dialects`.
- لا dialect shortfall.
- `can_start_phase23=true`.
- `quality_label` لمعظم ملفات review يكون `silver_candidate` أو `gold_candidate`.

حتى ذلك الوقت تبقى الخطوة الصحيحة: جمع ومراجعة بيانات حوار حقيقية.
