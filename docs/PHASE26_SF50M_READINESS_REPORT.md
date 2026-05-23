# PHASE26_SF50M_READINESS_REPORT.md

## SF.AI — Phase 26 SF-50M v0.1 Readiness

**Journey:** Phase 26 / 30  
**Language track:** `msa + saudi` only  
**Target model:** `sf-50m`  
**Status:** `NOT_READY_EXPAND_CORPUS_AND_IMPROVE_SF10M`

## الهدف

Phase 26 كان يمكن أن يكون تدريب `SF-50M`، لكن Phase 25 أثبتت أن
`SF-10M v0.2` لا يزال يُحجب في canary الحقيقي. لذلك نطبق مبدأ
Progressive Scaling Strategy: لا نكبر النموذج إلا بعد نجاح المرحلة الحالية.

هذه المرحلة أنشأت بوابة readiness/scaling، ولم تبدأ أي تدريب.

## القرار

```text
can_start_sf50m_training: false
recommended_action: DO_NOT_TRAIN_SF50M_YET_EXPAND_CORPUS_AND_REPEAT_SF10M_CANARY
```

## البوابات

```text
corpus_readiness      : false
tokenization_audit    : true
evaluation_suite      : true
safety_checks         : true
runtime_quality       : false
hallucination_checks  : false
repetition_checks     : false
resource_readiness    : true
```

## السبب

- corpus الحالي بعد Batch 003 صار `1550` سجلًا، والحد العملي لـ `SF-50M` هو `5000` سجل.
- `SF-10M v0.2` تحسن رقميًا، لكنه غير مسموح runtime.
- Phase 25 canary حجب النموذج الحقيقي بسبب `malformed_token`.
- لا توجد hallucination checks كافية لتوسيع الحجم.
- repetition checks لم تنجح كشرط جودة open-chat.

## ما أُضيف

- `sf_ai/training/phase26_readiness.py`
- `scripts/phase26_readiness.py`
- `make phase26-readiness`
- `GET /system/phase26-readiness`
- `artifacts/reports/phase26_sf50m_readiness_report.json`

## الخطوة التالية

لا نبدأ `SF-50M` الآن. المسار الصحيح:

1. توسيع corpus المحكوم من `1550` باتجاه `5000`.
2. الحفاظ على توازن `msa + saudi`.
3. إعادة تدريب `SF-10M` بعد التوسيع.
4. إعادة canary.
5. فتح `SF-50M` فقط إذا مرت gates.
