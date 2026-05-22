# SOVEREIGN_ACCELERATION.md

## SF.AI — طبقة التسريع السيادي (Phase 5.5)

هدف هذه المرحلة: تسريع بناء SF.AI **دون كسر مبدأ السيادة المعرفية**.

> **القاعدة الفاصلة:**
> إذا كان الشيء يحتوي معرفة متعلمة من جهة خارجية → ممنوع.
> إذا كان الشيء أداة حساب أو تنظيم أو تدريب → مسموح.

---

## 1. أدوات التسريع مقابل العقول الجاهزة

| الفئة | تحمل معرفة خارجية؟ | الحكم |
|--------|---------------------|------|
| PyTorch (مكتبة حساب) | لا. tensor ops + autograd فقط. | ✅ مسموحة |
| PyTorch MPS backend | لا. تسريع GPU على Apple Silicon. | ✅ مسموحة |
| Apple MLX (إطار حساب) | لا. ابتكار Apple، لكن نستخدمه كأداة. | ✅ مسموحة بشرط عدم تنزيل نماذجه الجاهزة |
| BPE algorithm (الخوارزمية فقط) | لا. خوارزمية معروفة من الأدبيات. | ✅ مسموحة |
| AdamW optimizer | لا. خوارزمية رياضية. | ✅ مسموحة |
| Mixed precision | لا. تقنية حسابية. | ✅ مسموحة |
| Gradient accumulation/checkpointing | لا. أنماط حساب. | ✅ مسموحة |
| Architectures معروفة (Decoder-only, RoPE, ...) | لا. أوصاف معمارية. | ✅ مسموحة |
| **HuggingFace pretrained weights** | **نعم. وزن متعلم.** | ❌ ممنوعة |
| **sentence-transformers** | **نعم.** | ❌ ممنوعة |
| **GPT-2/Llama/Gemma/Phi/Mistral** | **نعم.** | ❌ ممنوعة |
| **OpenAI/Claude/Gemini APIs** | **نعم.** | ❌ ممنوعة |
| **HuggingFace tokenizers بـ vocabularies جاهزة** | **نعم.** | ❌ ممنوعة |
| **LoRA/Adapter فوق نموذج خارجي** | **نعم.** | ❌ ممنوعة |
| **synthetic data من LLM خارجي** | **نعم — معرفة متعلمة منعكسة.** | ❌ ممنوعة |

---

## 2. لماذا PyTorch و MLX لا يكسران السيادة

PyTorch و MLX **مكتبتا حساب**. تقدمان:
- `Tensor` و `Tensor.backward()` (calculus، لا معرفة).
- `nn.Linear`, `nn.LayerNorm`, ... (طبقات قابلة للتهيئة، أوزانها random عند الإنشاء).
- `optim.AdamW` (خوارزمية رياضية، لا تحمل معرفة).
- Device backends (`cpu`, `mps`, `cuda`).

عند إنشاء `nn.Linear(in_features, out_features)`، الأوزان تُهيَّأ بـ `kaiming_uniform_` أو ما يشبهه: **توزيع عشوائي**. صفر معرفة.

لو حمّلنا `torch.load("llama-7b.pt")`، عندها فقط تكسر السيادة — لأن الأوزان أصبحت متعلمة من جهة خارجية.

> **SF.AI يستخدم PyTorch كآلة حاسبة، ليس كنوع من المعرفة.**

---

## 3. لماذا pretrained weights تكسر السيادة

أوزان أي نموذج جاهز هي **معرفة متعلمة من بيانات خارجية لا نتحكم بمصدرها ولا نعرف كل ما فيها**. تحميلها يعني:
- إدخال معرفة لم نختر مصدرها.
- إدخال bias لا نملكه.
- اعتماد على Decision Boundary رسمها فريق غريب على مشروعنا.
- فقدان القدرة على شرح كل ما يقوله النموذج.

SF.AI يهدف لأن يكون مفهومًا في كل وزنة منه. كل وزنة جاءت من بياناتنا وقواعدنا، أو لم تأت إطلاقًا.

---

## 4. لماذا pretrained embeddings تكسر السيادة

embeddings جاهزة (مثل sentence-transformers, OpenAI ada, ...) هي تمثيلات متعلمة لمعنى الكلمات. استخدامها يعني:
- ندفع بسيادة المعنى الدلالي إلى جهة خارجية.
- كل قرار retrieval/RAG يصبح محكومًا بـ embedding خارجي.
- الإجابة "هل النصان متشابهان؟" أصبحت إجابة LLM آخر، وليس إجابتنا.

SF.AI سيتعلم تمثيلاته من corpusه فقط (Phase 6+).

---

## 5. لماذا tokenizer الجاهز غير مسموح

الـ vocabulary في tokenizer جاهز يحمل قرارات معرفية:
- "أي subwords نختار."
- "كيف نقسم العربية."
- "ما الذي نعتبره token واحدًا."

vocabulary من GPT-2 مثلاً يميل بقوة نحو الإنجليزية ولا يفهم العربية جيدًا. لو استعرناه فقد دفعنا بقرار لغوي خارجي إلى صميم النظام.

السبيل الوحيد المقبول: **تدريب SF-BPE tokenizer من corpus SF.AI فقط** (Phase 5.5).

ملاحظة دقيقة: استخدام **مكتبة tokenizer كخوارزمية** (مثل `tokenizers` من HuggingFace) مسموح إذا دربناه من الصفر على بياناتنا. ما هو ممنوع هو استخدام vocab محفوظ من نموذج موجود.

في Phase 5.5 كتبنا BPE بأنفسنا بـ Python نقي — أبسط، أوضح، وأكثر سيادة. لا تبعية على مكتبات خارجية.

---

## 6. كيف ندرّب SF-BPE tokenizer من بياناتنا فقط

الخوارزمية (Phase 5.5):

1. **Pre-tokenize**: تقسيم النص على whitespace + بعض القواعد البسيطة.
2. **Initialize**: كل كلمة = tuple من characters + end-of-word marker.
3. **Count pairs**: حساب تكرار كل (token_i, token_{i+1}) عبر الـ corpus.
4. **Merge**: أكثر pair تكرارًا يُدمَج في token جديد.
5. **Repeat** حتى الوصول لـ `vocab_size` أو نفاد pairs.
6. **Save**:
   - `vocab.json`: `{token: id}`.
   - `merges.txt`: قواعد الدمج بالترتيب.
   - `meta.json`: مصدر البيانات، التاريخ، الإعدادات، `sf_origin: true`.

الناتج يُحفظ في `artifacts/tokenizers/sf_bpe/`.

**الـ data الوحيدة المسموح بها للتدريب:** `data/corpus/chat/jsonl/*.jsonl` (Phase 5) + أي corpus يوافق عليه المستخدم بنفسه.

---

## 7. كيف نحفظ checkpoints خاصة بـ SF.AI فقط

كل checkpoint في `artifacts/checkpoints/` يحمل metadata `meta.json` فيه:

```json
{
  "step": 12345,
  "epoch": 1,
  "model_name": "sf-10m",
  "created_at": "2026-05-22T12:34:56Z",
  "sf_origin": true,
  "training_data_hash": "...",
  "config_hash": "..."
}
```

`CheckpointManager.assert_sovereign(name)` يرفع `SovereigntyError` إذا:
- `sf_origin != true`، أو
- المصدر يشير إلى نموذج خارجي.

محاولة تحميل وزن غير سيادي عبر `CheckpointManager` تفشل بصراحة.

---

## 8. كيف نتأكد من random initialization

عند بناء `TinyTransformer` (Phase 6):
- كل `nn.Linear`/`nn.Embedding` يُهيَّأ بـ `torch.nn.init.kaiming_uniform_` أو `normal_(mean=0, std=0.02)`.
- لا `.load_state_dict()` من مصدر خارجي.
- اختبار وحدوي يتأكد أن أول forward pass على نموذج جديد ينتج logits بقيم معقولة (متوسط ≈ 0، std ≈ مرتبط بـ init scale)، **وليست** قيم نموذج مدرَّب.

`TrainingConfig.sovereign` ثابت `True` ولا يمكن إيقافه. تغييره برمجيًا يفشل في `validate()`.

---

## 9. كيف نستخدم MacBook Air M4 24GB بأفضل شكل

التكوين الأمثل لجهاز المستخدم:

| المتغير | القيمة المقترحة | السبب |
|---------|------------------|-------|
| `device` | `mps` | M4 Neural Engine + GPU. CUDA غير متاح على Mac. |
| `mixed_precision` | `false` ابتداءً | MPS + bf16/fp16 لا يزال غير مستقر تمامًا على بعض ops. فعّله بعد التحقق. |
| `batch_size` | 4–8 | لتجنب OOM في 24GB unified memory. |
| `accumulation_steps` | 4–16 | يعوّض batch_size الصغير. |
| `grad_checkpointing` | `true` | يوفر memory مقابل ~25% slowdown. |
| `max_seq_len` | 256–1024 | يتدرج مع حجم النموذج. |
| نموذج البداية | `SF-10M` | للتجارب التعليمية + التحقق من tokenizer + data. |
| النموذج الواقعي الأول | `SF-50M` → `SF-120M` | بعد اكتمال corpus. |

تجنّب:
- ❌ تشغيل تدريب طويل بدون gradient checkpointing.
- ❌ batch sizes كبيرة بدون مراقبة `mps` memory.
- ❌ بدء التدريب قبل اختبار dataloader على عدد قليل من العينات (DataLoader smoke test).

---

## 10. لماذا لا يوجد اختصار سيادي في الأوزان الجاهزة

كثيرون يقترحون: "ابدأ بـ Gemma-2B واعمل LoRA على بياناتك العربية، أرخص وأسرع."

نرفض. لأن:
- الأوزان الأساسية ليست أوزاننا.
- بيانات تدريب Gemma لا نملكها ولا نعرفها بالكامل.
- أي bias فيها سيبقى داخل LoRA الذي ندربه.
- في النهاية: ما زلنا نعتمد على عقل جاهز.

الاختصار المقبول الوحيد: **بدء صغير** (SF-10M)، **بيانات نظيفة موثقة**، **توسعة تدريجية**. هذا اختصار في الجهد، لا في السيادة.

---

## 11. ما الأدوات التي تسرّع المشروع دون حمل معرفة خارجية

- **PyTorch / MPS** — حساب.
- **Apple MLX** — حساب (لا تنزّل نماذجه).
- **AdamW + cosine scheduler** — رياضيات.
- **BPE algorithm** — خوارزمية (مدرَّبة من بياناتنا).
- **Gradient checkpointing / mixed precision** — تقنيات.
- **Random init** بـ Kaiming/Normal — بداية عشوائية.
- **Datasets streaming** (Phase 5) — توفير ذاكرة.
- **Architectures**: Decoder-only + RoPE + RMSNorm + SwiGLU + weight tying — patterns معمارية معروفة. أوزانها سنتعلمها نحن.

كل هذه تختصر الجهد **الهندسي**، وليس الجهد **المعرفي**. العقل يظل ملك SF.AI.

---

## ما لا يحدث في Phase 5.5

- ❌ لا تدريب فعلي.
- ❌ لا تنزيل نماذج.
- ❌ لا تنزيل tokenizers.
- ❌ لا تنزيل بيانات تلقائية.
- ❌ لا أوزان متعلمة.

Phase 5.5 = **بنية** فقط. الكود جاهز لاستقبال البيانات + إعدادات التدريب + اختيار الجهاز + إدارة checkpoints. الانطلاق الفعلي يحتاج إذن صريح من المستخدم في مرحلة لاحقة.

---

## الـ pyproject extras

```bash
# Phase 1+ core (no torch):
pip install -e ".[dev]"

# Phase 5.5+ training (adds torch):
pip install -e ".[dev,training]"
```

كل الكود يعمل بدون `torch` ما لم تستدع وحدات training/optimizers التي تحتاجه فعليًا. اختيار الجهاز يتحول بشكل آمن إلى `cpu` إذا torch مفقود — مع تنبيه.
