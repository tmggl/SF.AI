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

## لماذا لا أضيف 500 محادثة بنفسي؟

لأن دستور SF.AI يمنع `synthetic LLM data`.

أي محادثة يكتبها Agent/LLM لتدريب النموذج ستصبح بيانات مولدة من عقل خارجي، وهذا يخالف:

- Own the intelligence.
- No hidden shortcuts.
- Data provenance required.
- Progressive Scaling Strategy.

الطريق الصحيح:

```text
اختبار سامي الحقيقي
→ export من الواجهة
→ مراجعة سامي
→ prepare-dialogue-batch مع training_allowed
→ corpus-audit
→ phase22-readiness
```

---

## بوابة Phase 22

أضيف:

- `make phase22-readiness`
- `make phase22-plan`
- `make phase22-review-intake`
- `GET /system/phase22-readiness`
- `GET /system/phase22-collection-plan`
- `GET /system/phase22-review-intake`
- `sf_ai/datasets/phase22_readiness.py`
- `sf_ai/datasets/phase22_review_intake.py`

القيم الحالية المتوقعة:

```text
training_records: 30
target_records: 500
remaining_records: 470
dialect_counts: {"saudi": 30}
missing_required_dialects: ["msa"]
status: NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2
can_start_phase23: false
synthetic_llm_data_allowed: false
```

وخطة الجمع الحالية:

```text
remaining_records: 470
batch_size: 25
estimated_batches: 19
quota_by_dialect: {"msa": 200, "saudi": 170}
flexible_records_after_minimums: 100
```

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

القاعدة العملية للوصول إلى حوار مفيد للتدريب:

- لا تصدّر أقل من 3 أدوار منك و3 ردود من المساعد.
- لا تستخدم جلسة فيها `مولّد: نموذج SF-10M` كبيانات جودة.
- فضّل موضوعًا واحدًا واضحًا في كل جلسة.
- اجعل الردود التي توافق عليها أنت فقط تدخل corpus.

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

## ماذا يكتب سامي لاختبار وجمع corpus؟

اكتب محادثات طبيعية في الواجهة، ثم صدّرها:

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

لجمع ملف أعلى جودة، اجعل كل جلسة 3–6 أدوار. مثال بنية الجلسة:

```text
1. افتح موضوعًا واحدًا.
2. اطلب توضيحًا أو مثالًا.
3. اسأل متابعة قصيرة.
4. إن كان الرد مفهومًا، صدّر الجلسة للمراجعة.
```

بعد التصدير، لا يدخل الملف التدريب حتى يُراجع ويُحضّر:

```bash
make phase22-review-intake

make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_001.jsonl --quality silver --dialect saudi --training-allowed"
```

أو للفصحى:

```bash
make prepare-dialogue-batch ARGS="--input data/corpus/chat/review/<file>.jsonl --out data/corpus/chat/jsonl/dialogue_batch_v2_msa_001.jsonl --quality silver --dialect msa --training-allowed"
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
