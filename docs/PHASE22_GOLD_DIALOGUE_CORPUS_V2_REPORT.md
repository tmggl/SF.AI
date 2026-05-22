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
- `GET /system/phase22-readiness`
- `sf_ai/datasets/phase22_readiness.py`

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

بعد التصدير، لا يدخل الملف التدريب حتى يُراجع ويُحضّر:

```bash
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
```

يعطيان:

- لا issues.
- `training_records >= 500`.
- لا `missing_required_dialects`.
- لا dialect shortfall.
- `can_start_phase23=true`.

حتى ذلك الوقت تبقى الخطوة الصحيحة: جمع ومراجعة بيانات حوار حقيقية.
