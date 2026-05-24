# TRAINING_PLAN.md

## SF.AI — خطة تدريب النموذج الأصيل (Phase 6+)

> **القاعدة الأولى:** كل وزن يتعلمه SF.AI يبدأ من **random init**، يتعلم من **corpus SF.AI**، ويُحفَظ في **artifacts/checkpoints/** بـ `sf_origin: true`.
> لا `from_pretrained`، لا تحميل من HuggingFace، لا LoRA فوق نموذج خارجي.

## القاعدة الحالية الأعلى — Strategy v2

ابتداءً من Phase 27.78:

```text
ENGINEERING_ROOT_CAUSE_GATE
PHASE27_78_ENGINEERING_DECISION
PHASE27_79_REPAIR_DESIGN_DECISION
```

هما شرط قبل أي تدريب جديد. القرار الحالي:

- `new_training_allowed=false`.
- `runtime_release_allowed=false`.
- `sf50m_justified_transition=false`.
- `tokenizer_retrain_allowed=false`.
- `continue_sf10m=true`.

أوزان السبب الحالية تقول إن المشكلة ليست capacity:

- family mixing `22%`.
- objective `18%`.
- curriculum `16%`.
- weak generalization `14%`.
- semantic routing `10%`.
- capacity `1%`.

Phase 27.79 صممت objective/curriculum/decoding gates. إذن Phase 27.80 يجب
أن يشفّر هذه البوابات ويشغّل dry-run، ولا يبدأ تدريبًا إلا بعد نجاحها.

حزمة التسريع الهندسي المحملة:

- `torch` و`numpy` للحساب.
- `tensorboard` لتتبع التجارب محليًا.
- `tqdm` لقياس تقدم التدريب/الفحوصات.
- `psutil` لمراقبة الموارد.
- `safetensors` لحفظ tensors بأمان لاحقًا.
- `rich` لتقارير CLI.

هذه أدوات فقط وليست pretrained weights أو vocab أو datasets.

---

## 1. لماذا نبدأ صغيرًا؟

نبدأ بـ **SF-10M** (≈10M parameter) قبل أي شيء آخر للأسباب التالية:

| القضية | لماذا تنكشف في SF-10M | لماذا تختفي في الـ 1B |
|---------|------------------------|---------------------|
| Tokenizer سيء (يقطّع كلمات عربية بشكل سيء) | تظهر فورًا في الـ loss curves و generations | يتعلم الـ 1B إخفاءها بحفظ كلمات كاملة |
| Data quality (تكرار / synthetic) | يدخل في loss سريعًا | الـ 1B "يبتلع" حتى السيء |
| Training loop bug | يكسر loss في خطوات قليلة | الـ 1B يكلف ساعات قبل الكشف |
| Repetition collapse | تظهر في الـ generation فورًا | تظهر متأخرة |
| Arabic quality (تشكيل، ة/ه) | واضحة في 10M | يضمنها 1B تلقائيًا |
| Device/precision issues (MPS NaN) | NaN يظهر مبكرًا | قد يخفى تحت scale |

**القاعدة:** لا توسعة قبل تحقق SF-10M، ولا تدريب جديد بعد Phase 27.78 قبل
قرار root-cause يسمح به.

---

## 2. لماذا لا نستخدم أوزانًا جاهزة؟

| السبب | التفصيل |
|-------|---------|
| **سيادة معرفية** | كل قرار يقوله النموذج يجب أن يُعزى إلى بيانات اخترناها. |
| **تتبع الـ bias** | bias الـ pretrained غير قابل للقياس عندنا. |
| **شرح القرار** | لا يمكن تفسير "لماذا قال هذا" إذا نصف الأوزان متعلمة من Reddit. |
| **استقلال التشغيل** | لا اعتماد runtime على repo غير لنا. |
| **اختصار وهمي** | LoRA فوق Gemma "أرخص" لكنه يخفي عقلًا غريبًا. |

اقرأ [SOVEREIGN_ACCELERATION.md](./SOVEREIGN_ACCELERATION.md) للتفاصيل الكاملة.

---

## 3. سلم النماذج (Model Ladder)

| اسم | d_model | n_heads | n_layers | params | استخدام |
|------|---------|---------|----------|--------|---------|
| SF-10M | 256 | 4 | 6 | ~10M | smoke test، تجربة الـ tokenizer و loop |
| SF-50M | 512 | 8 | 8 | ~50M | أول نموذج يعطي لغة عربية معقولة |
| SF-120M | 768 | 12 | 12 | ~120M | أول نموذج محادثة قابل للاستخدام |
| SF-350M | 1024 | 16 | 24 | ~350M | بداية الجدية |
| SF-700M | 1280 | 20 | 28 | ~700M | حد M4-24GB العملي |

> **لا نبدأ بـ 1B.** أي قفز > 2x بين الأحجام = إعادة فحص كاملة.

---

## 4. التوسع التدريجي

شروط الانتقال من حجم لحجم:

1. **الـ loss ينحدر بشكل منطقي** على validation set صغير (لا overfitting سريع).
2. **Perplexity لا تنفجر** على نصوص عربية مختلفة.
3. **Generation لا تكرر** (no repetition collapse، no loop).
4. **Arabic shape** صحيح (الحروف، تركيب الكلمة، ة/ه/أ/إ).
5. **Tokenizer كافٍ** (إذا الـ vocab صغير على البيانات، نوسعه أولًا).
6. **Hardware يحتمل** (M4 24GB يكفي حتى SF-700M بـ grad_checkpointing + accumulation).

عدم تحقق أي شرط → ابقَ في الحجم الحالي حتى يُحل.

بعد Phase 27.78، لا يكفي أن نرى ضعفًا في الردود لنكبر النموذج. يجب أن يثبت
gate رسمي أن capacity هي السبب الأكبر. الوزن الحالي لـ capacity هو `1%`،
لذلك `SF-50M` محجوب حتى إشعار هندسي معاكس.

عندما يثبت gate أن الحجم التالي مبرر وينجح، لا ينتظر الوكيل إذنًا جديدًا.
ينتقل تلقائيًا عبر:

```text
SF-10M → SF-50M → SF-100M-class/SF-120M → SF-350M → SF-700M → SF-1B+
```

`M100` تعني `SF-100M-class`، والمستوى المعماري الحالي لهذا slot هو
`SF-120M` ما لم يعتمد تقرير معماري لاحق `SF-100M`.

---

## 5. قياس الجودة (Evaluation)

في Phase 6 الإصدارات الأولى:

- **Loss / Perplexity** على corpus held-out صغير.
- **Generation manual review** على prompts قياسية (10–20 مُختارة).
- **Arabic letter quality:** هل النموذج يكتب حروف صحيحة؟
- **Dialect awareness:** هل يميز سعودي/مصري/شامي؟ (بعد تكامل قاموس Mo3jam في Phase 3.5)
- **Repetition rate:** كم من الـ generations تحوي تكرارًا؟

نضيف evaluations رسمية (TyDi-style benchmarks، Arabic LM benchmarks) **بعد** أن يصبح SF-50M على الأقل مستقرًا. قبل ذلك، benchmark على نموذج 10M = هدر.

المقاييس الرسمية الآن ليست loss/perplexity فقط. النجاح يحتاج:

- held-out dialogue quality.
- runtime usability.
- clean-stop.
- semantic correctness.
- family stability.
- open_social naturalness.
- followup continuity.
- canary pass rate.
- human conversation realism.

---

## 6. كيف نتجنب الهلوسة

الهلوسة في LLMs السبب الرئيسي لها: **حشر المعرفة في الأوزان**. SF.AI سيتجنبها عبر:

1. **حدود متواضعة على المحتوى.** SF-10M لا يدّعي معرفة الحقائق. هو نموذج **نمط لغوي**.
2. **RAG في Phase 8.** المعرفة المتخصصة (قانون، طب، مال) **لا تُحفَر في الأوزان**. تُسترجَع من مصادر موثقة (Phase 7 web research + Phase 8 RAG).
3. **Safety domains منفصلة.** المجالات الحساسة (legal/medical/finance/security/religion) ترد عبر الـ Composer بـ "ارجع للمختص" ولا تستدعي النموذج.
4. **Citations.** Phase 7 web research module يرفق مصادر مع كل إجابة بحثية.
5. **Honesty patterns.** Phase 4 ChatModule يقول صراحة "Phase X، قدراتي محدودة" بدلًا من اختراع.

---

## 7. RAG بدلًا من Knowledge Stuffing

**القاعدة:** SF.AI لا يحفظ مرجعًا في الأوزان إذا أمكنه استرجاعه.

| سؤال | المسار |
|------|--------|
| "ما عاصمة الصين؟" | استرجاع من مصدر (Phase 7/8) ← لا حفظ في الأوزان |
| "اشرح لي كلمة شلون" | قاموس Mo3jam (Phase 3.5) ← لا حفظ في الأوزان |
| "لخّص هذا المقال" | استخراج محلي + تلخيص rule-based ← لا توليد حر |
| "كيف حالك" | النموذج (chat) ← فعلًا حفظ |
| "اكتب لي رد ودود" | النموذج (kindly chat) ← فعلًا حفظ |

النموذج يتعلم **شكل اللغة**، النظام يأتي بـ **المحتوى**.

---

## 8. إعدادات التدريب المقترحة (SF-10M على M4-24GB)

| المتغير | القيمة |
|---------|--------|
| `device` | `mps` |
| `mixed_precision` | `false` بداية، فعّله بعد التحقق |
| `batch_size` | 4–8 |
| `seq_len` | 256–512 |
| `accumulation_steps` | 4–16 |
| `grad_checkpointing` | `true` |
| `optimizer` | AdamW |
| `lr` | 3e-4 |
| `min_lr` | 1e-5 |
| `warmup_steps` | 5–10% من total |
| `scheduler` | cosine with warmup |
| `weight_decay` | 0.1 |
| `grad_clip` | 1.0 |
| `seed` | 1337 (للتكرار) |

---

## 9. حدود Phase 6

Phase 6 الحالي يقدم:

- ✅ بنية النموذج جاهزة (TinyTransformer + RoPE + RMSNorm + SwiGLU + weight tying).
- ✅ سكربت training scaffold (`train_tiny_lm.py`).
- ✅ سكربت evaluation (`evaluate_tiny_lm.py`).
- ✅ Generation (greedy + sampling).
- ✅ Losses (CE + perplexity).
- ✅ Checkpoint manager integrated.
- ✅ Device auto-selection (mps فوق Mac).
- ✅ تصدير عدد المعاملات.
- ✅ Random init مُفعَّل بـ `init_std=0.02`.

Phase 6 لا يقدم (مقصود):

- ❌ بدء تدريب فعلي. ينتظر بيانات المستخدم.
- ❌ multi-GPU.
- ❌ KV cache (يأتي بعد تحقق التدريب).
- ❌ Flash Attention مخصص (نستخدم `scaled_dot_product_attention` المدمج).
- ❌ تدريب من checkpoint سابق (resume) — يضاف عند الحاجة.

---

## 10. ماذا يحدث عند تحقق SF-10M

- يُحفظ checkpoint بـ `sf_origin: true` و metadata كاملة.
- يُربط بـ Phase 4 ChatModule كـ **اختياري** (env var `SF_USE_NATIVE_LM=true`).
- ChatModule يستخدم النموذج لـ generation، يحتفظ بالـ templates fallback.
- Phase 7 (web research) يُبنى بشكل مستقل، لا يعتمد على النموذج.
- نقاش الانتقال إلى SF-50M بعد تجميع corpus أكبر + تحقق تشغيلي.

---

## 11. كيف لا نخدع أنفسنا

- لا "training يعمل" بدون تأكيد أن الـ loss ينحدر فعلًا على بيانات حقيقية.
- لا "النموذج يفهم العربية" بدون تقييم يدوي على عينات.
- لا "النموذج جاهز" قبل أن يخرج جملة عربية كاملة سليمة من توقعه.
- لا "نسخة 1B" قبل أن تكون 350M قد أنتجت محادثة مفهومة لمدة 3 أسطر متتالية.

أي ادعاء قبل ذلك = هلوسة بشرية، ليست هلوسة نموذج.
