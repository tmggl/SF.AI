# PHASE25_GENERATED_CHAT_CANARY_REPORT.md

## SF.AI — Phase 25 Generated Chat Canary v1

**Journey:** Phase 25 / 30  
**Language track:** `msa + saudi` only  
**Candidate generator:** `sf_10m_v0_2`  
**Status:** `COMPLETED_GUARDED_CANARY_REAL_MODEL_BLOCKED`

## الهدف

Phase 25 لا تجعل `SF-10M v0.2` مساعدًا جاهزًا. الهدف هو بناء canary صغير
داخل مسار الشات: نجرب المولد فقط في وضع مختبري، ثم نمنع الرد إذا ظهر تكرار،
تجزئة، أو آثار corpus.

## ما أُضيف

- `GenerationGuard` في `sf_ai/modules/chat/generation_guard.py`.
- تحديث `GenerationPolicy` ليطلب ثلاثة شروط قبل أي canary:
  - `SF_ENABLE_NATIVE_GENERATOR=true`
  - `SF_NATIVE_GENERATOR_EXPERIMENTAL=true`
  - `SF_GENERATOR_CANARY=true`
- تحديث `NativeGenerator` افتراضيًا إلى:
  - tokenizer: `artifacts/tokenizers/sf_bpe/v2`
  - checkpoint: `artifacts/checkpoints/sf_10m_v0_2/sf-10m-step2000`
  - generator metadata: `sf_10m_v0_2`
- تحديث `ChatModule` ليعيد الرد للقالب عند فشل guard.
- تحديث واجهة الشات لتعرض `Canary SF-10M v0.2` عند نجاح canary فقط.
- تحديث review intake حتى تعتبر `sf_10m_v0_2` raw generator output، وليس بيانات تدريب جودة.

## تجربة النموذج الحقيقي

تم تشغيل canary محليًا على `SF-10M v0.2`:

```text
prompt: اكتب رد قصير عن هدف SF.AI
generator attempted: sf_10m_v0_2
guard decision: blocked
reason: malformed_token
fallback: template
```

الرد النهائي بقي مفهومًا لأن القالب استُخدم:

```text
وصلتك. أنا محدود الآن، لكن قل لي وش تبي بالضبط وأنا أمشي معك خطوة خطوة.
```

## القرار

```text
Phase 25: COMPLETED_GUARDED_CANARY_REAL_MODEL_BLOCKED
Canary infrastructure: PASS
SF-10M v0.2 open-chat quality: FAIL
Broad runtime activation: NO
```

المرحلة نجحت كحماية هندسية، لكنها أثبتت أن النموذج نفسه لا يزال غير صالح
كمساعد محادثة مفتوح. لا يبدأ تدريب أكبر بشكل أعمى؛ Phase 26 يجب أن يبدأ
ببوابة scaling/readiness واضحة قبل أي `SF-50M`.
