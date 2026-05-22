# PHASE15_GENERATOR_ADAPTER_REPORT.md

## SF.AI — Phase 15 Generator Adapter for ChatModule

**Date:** 2026-05-22  
**Status:** COMPLETED_AS_SAFE_ADAPTER  
**Runtime generation:** disabled by default  
**Active chat output:** `template`

---

## الهدف

رفع مستوى مسار الشات من قوالب فقط إلى بنية جاهزة لاستقبال مولّد سيادي، بدون
استبدال الردود الحالية بنموذج Phase 14 الضعيف.

Phase 14 أثبت أن checkpoint السيادي يستطيع توليد نص غير فارغ، لكنه ما زال
متكررًا وصغير البيانات. لذلك Phase 15 لا تجعل النموذج يرد على المستخدم مباشرة؛
بل تثبت طبقة adapter/policy/metadata حتى يدخل التوليد لاحقًا بعد Phase 16.

---

## ما أُضيف

- `sf_ai/modules/chat/generation_policy.py`
  - يقرأ `SF_ENABLE_NATIVE_GENERATOR`.
  - يمنع التوليد افتراضيًا.
  - يمنع التوليد في:
    - المجالات غير `chat`.
    - المجالات غير النشطة أو skeleton.
    - المسارات الحساسة safety.
    - fallback routes.
    - الثقة المنخفضة.
    - نوايا الهوية والقدرات لأنها pinned ويجب أن تبقى دقيقة.

- `sf_ai/modules/chat/native_generator.py`
  - adapter lazy-load لـ:
    - tokenizer: `artifacts/tokenizers/sf_bpe/v1`
    - checkpoint: `artifacts/checkpoints/sf_10m_v0_1/sf-10m-step33`
  - يرفض العمل إذا غاب tokenizer أو checkpoint.
  - يستخدم `CheckpointManager.assert_sovereign`.
  - لا يحمل أي pretrained weights.

- `ChatModule`
  - يضيف metadata:
    - `generator:template`
    - `native_generator:disabled`
  - لا يستبدل القوالب بالتوليد بعد.

- API/UI
  - `POST /chat/message` يعيد حقل `generator`.
  - شاشة `/ui/chat` تعرض المولّد في سطر التشخيص وmeta الرسالة.

---

## لماذا لم نفعّل التوليد للمستخدم؟

لأن checkpoint الحالي:

- تدرب على corpus سعودي صغير جدًا.
- لا يملك MSA كفاية.
- يعطي توليدًا غير فارغ لكنه متكرر.
- لم يمر بعد Phase 16 evaluation/safety/style harness.

القرار الصحيح: **نبني الباب ولا نفتحه بعد**.

---

## شروط نجاح Phase 15

- التوليد يمكن تعطيله بالكامل عبر env flag.
- المجالات الحساسة/skeleton لا تصل إلى NativeGenerator.
- الردود الحالية لم تنكسر.
- UI/API يوضحان مصدر الرد: `template` الآن، و`sf_10m_v0_1` لاحقًا إذا فُعّل.
- الاختبارات تمر.

---

## نتيجة الاختبارات

```text
367 passed in 3.13s
```

---

## الخطوة التالية

Phase 16 — Evaluation, Safety, and Saudi/MSA Style Harness.

هدفها قياس النموذج قبل السماح له بالرد داخل الشات:

- prompts سعودية وفصحى.
- فحص تكرار/هلوسة/فراغ.
- safety prompts.
- style score.
- قرار gate واضح: هل يسمح بتفعيل `SF_ENABLE_NATIVE_GENERATOR` أم يبقى `template`.
