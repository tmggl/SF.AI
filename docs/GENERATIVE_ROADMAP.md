# GENERATIVE_ROADMAP.md

## SF.AI — خارطة الوصول إلى حوار مولّد مقنع

**Journey:** Phase 21 / 30  
**Language track:** Arabic MSA + Saudi only  
**Lexicon track:** Saudi Seed v1 + governed MSA/Saudi corpus  
**Goal:** الانتقال من router/templates إلى نموذج لغوي سيادي مولّد يستطيع محاورة سامي بردود طبيعية.

---

## الحقيقة الحالية

SF.AI يملك الآن:

- `Router + NLP + templates` لردود اجتماعية مفهومة.
- `SF-10M v0.1` مولّد خام، سيادي، لكنه مكرر وضعيف.
- واجهة تعرض هل الرد `template` أو `sf_10m_v0_1`.
- corpus تدريبي صغير جدًا: `30` محادثة سعودية gold.

هذا يعني:

- نعم، بدأ التدريب الفعلي سابقًا في Phase 13/14.
- لا، لم نصل بعد إلى حوار مولّد مقنع.
- السبب ليس الكود فقط؛ السبب الأساسي هو صغر البيانات وضعف تغطية الفصحى/السعودي الحوارية.
- لا تطلب من سامي اختبار `chat_patterns.py` كأنه مولد؛ هذه قوالب ثابتة وليست نتيجة تدريب.

---

## متى نبدأ التدريب الفعلي؟

بدأ التدريب الفعلي بالفعل:

| المرحلة | ماذا حدث؟ | النتيجة |
|---------|-----------|---------|
| Phase 12 | تدريب tokenizer سيادي من الصفر | مكتمل بحدود؛ corpus سعودي صغير |
| Phase 13 | smoke LM training | أول نص خام غير فارغ |
| Phase 14 | SF-10M v0.1 | checkpoint حقيقي لكنه مكرر |

التدريب التالي المفيد يبدأ عند:

| المرحلة | التدريب | شرط البدء |
|---------|---------|-----------|
| Phase 24 | `SF-10M v0.2` | 500 سجل حوار محكوم على الأقل |
| Phase 27.5 | `SF-10M v0.4` | إصلاح صيغة الحوار بعد corpus gate |
| Phase 27.6 | `SF-10M v0.5` | assistant-target training على رد المساعد فقط |
| Phase 27.7 | لا تدريب | fixed train/eval split + gold social + canary prompt-aware |
| Phase 27.8 | `SF-10M v0.6` | تحسن رقمي على eval؛ runtime blocked |
| Phase 27.9 | لا تدريب | Generation Quality Harness يحجب v0.6 |
| Phase 27.10 | `SF-10M v0.7` | short-response repair؛ تحسن رقمي وتوليد محظور |
| Phase 27.11 | `SF-10M probe` | gold overfit أثبت نقص stop boundary/EOS |
| Phase 27.12 | `SF-10M probe` | EOS + dialect conditioning؛ تحسن جزئي |
| Phase 27.13 | `SF-10M v0.8` | eval تحسن إلى ppl 24.23؛ generation-quality 3/10 ومحظور |
| Phase 27.14 | لا تدريب | اعتماد أدوات جودة التدريب السيادية |
| Phase 27.15 | `SF-10M v0.10` | curriculum + no-repeat؛ eval تحسن وcanary صارم 0/10 |
| Phase 27.16 | `SF-10M v0.11` | sample-isolated objective؛ runtime محظور |
| Phase 27.17 | `SF-10M micro-probe` | exact prompt-to-answer قبل أي تدريب واسع |
| Phase 27.18 | `SF-10M hygiene repair` | إصلاح كسور tokenization/decoding |
| Phase 27.19 | `SF-10M hygiene probe` | repair corpus/probe للمصطلحات المتكسرة |
| Phase 27.20 | `Tokenizer/protected phrases` | استراتيجية حماية العبارات قبل التدريب |
| Phase 27.21 | `Tokenizer v3 + micro-probe` | تدريب tokenizer v3 ثم اختبار probe قبل runtime |
| Phase 27.22 | `Spacing/boundary repair` | علاج لصق الكلمات قبل runtime |
| Phase 27.23 | `Semantic/lexical repair` | علاج الخلط الدلالي واللفظي المتبقي |
| Phase 27.24 | `Minimal lexical stabilization` | تثبيت ألفاظ فصيحة قليلة دون تكبير |
| Phase 27.25 | `Held-out generation canary` | فشل `8/16` على أسئلة جديدة؛ runtime محظور |
| Phase 27.26–27.30 | `Repair series` | تحسن إلى fresh mixed shadow `16/18`؛ runtime محظور |
| Phase 27.31–27.33 | `Natural generation gates` | كل البوابات المحلية مرّت؛ جاهز لتصميم guarded runtime trial |
| Phase 27.34 | `Guarded runtime trial` | زر مولّد تجريبي request-scoped مرّ `9/9` |
| Phase 27.35 | `Live UI trial observations` | السيرفر الحي والواجهة مرّا `10/10` |
| Phase 27.36 | `Live UI triage` | quality-floor active، وtriage مرّ `27/27` |
| Phase 27.37 | `Supported topic expansion` | موضوع `الصبر` فُتح خلف semantic guard ومرّ `21/21` |
| Phase 27.38 | `Targeted topic curriculum/probe` | probe جزئي `6/20`; لا runtime switch |
| Phase 27.39 | `Topic-isolation repair` | probe جزئي `10/24`; لا runtime switch |
| Phase 27.40 | `Tokenizer/context repair` | tokenizer v5 + probe `24/24`; المرشح فُتح لاحقًا في trial محروس |
| Phase 27.41 | `Guarded runtime switch` | `generator_trial=true` يستخدم `sf_10m_phase27_40`; HTTP gate `22/22` |
| Phase 27.42 | `Live UI broader probes` | broader HTTP gate `29/29`; misaligned generations blocked |
| Phase 27.43 | `Guarded data-backed expansion` | weak-lane candidate partial `10/16`; runtime stays on 27.40 |
| Phase 27.44 | `Tokenizer/curriculum repair` | tokenizer v6؛ partial `11/16`, weak-lane `6/6` |
| Phase 27.45 | `Semantic topic balance repair` | partial `9/16`; التوسيع العريض سبّب regression |
| Phase 27.46 | `Core dialogue stabilization` | partial `14/16`; بقي `الوفاء/الشجاعة` |
| Phase 27.47 | `New topic conditioning repair` | offline `16/16`; أصلح train/eval conditioning |
| Phase 27.48 | `Guarded runtime switch` | live API `19/19`; `generator_trial=true` يستخدم `sf_10m_phase27_47` |
| Phase 27.49 | `Broader live UI/API probes` | live API `33/33`; أصلح `وش تنصحني اسوي` |
| Phase 27.50 | `Generator-only UI lab` | لا قوالب في `/chat/message`; gate `7/7` |
| Phase 27.51 | `Open-dialogue generalization audit` | فشل مفيد: live `3/22`, raw natural `1/20`; التدريب مطلوب |
| Phase 27.52 | `Natural dialogue objective repair` | دبل تدريب SF-10M: `9200` خطوة؛ raw natural `5/20`; لا runtime switch |
| Phase 27.53 | `Natural dialogue diversity expansion` | `10,540` زوجًا و`18,000` خطوة؛ raw natural `2/36`; لا runtime switch |
| بعد نجاح SF-10M | `SF-50M v0.1` | نجاح جودة SF-10M/canary + إعادة Phase 26 readiness |
| Phase 28 | `SF-120M v0.1` | نجاح SF-50M + scaling gate |

---

## متى أصل إلى حوار مولّد يقنعني؟

توقع واقعي:

- **Phase 24:** أول تحسن واضح على SF-10M، لكنه قد يبقى متقطعًا.
- **Phase 25:** تجربة مولّد داخل الشات بشكل محكوم، مع fallback لو كرر أو هلوس.
- **Phase 26:** بوابة readiness رفضت SF-50M الآن.
- **Phase 27:** eval v2 مرّر التوجيه، ثم اكتمل corpus gate بعد التوسعة الطبيعية.
- **Phase 27.5:** `SF-10M v0.4` تعلّم صيغة الحوار أفضل، لكنه بقي غير جاهز للواجهة.
- **Phase 27.6:** `SF-10M v0.5` جرّب assistant-target، لكنه بقي مكررًا وغير جاهز للواجهة.
- **Phase 27.7:** ثبت split/canary قبل التدريب التالي، وأصبح القياس على eval held-out إلزاميًا.
- **Phase 27.8:** `SF-10M v0.6` تحسن رقميًا، لكن canary حجب 10/10 عينات بسبب fragments.
- **Phase 27.9:** صار لدينا harness آلي يقيس هذه المشكلة كشرط قبل runtime.
- **Phase 27.10:** short-response repair حسن eval إلى `4.7512` لكنه لم يصلح التوليد.
- **Phase 27.11:** gold overfit probe فشل `0/16 clean-stop`; المشكلة في توقف الرد لا في prefix فقط.
- **Phase 27.12:** EOS + dialect conditioning حسّن probe إلى `5/16` تطابق كامل و`9/16` بلا فشل guard، لكنه لا يكفي للواجهة.
- **Phase 27.13:** `SF-10M v0.8` حسّن eval إلى loss `3.1875`/ppl `24.23`، لكن generation-quality بقي `3/10` بعد تشديد guard، لذلك runtime محظور.
- **Phase 27.14:** اعتمدنا أدوات الجودة السيادية كسياسة تنفيذ: tracker محلي، checkpoint selector، probes، curriculum/no-repeat كمتطلبات قبل التفعيل.
- **Phase 27.15:** `SF-10M v0.10` حسّن eval إلى loss `3.0452`/ppl `21.01`، لكن canary الدلالي الصارم كشف أن الربط بين السؤال والجواب ما زال فاشلًا `0/10`.
- **Phase 27.16:** أضاف sample-isolated packing ودرب `SF-10M v0.11`; أفضل eval `4.0573`/ppl `57.82` وcanary بقي محجوبًا، لذلك لا runtime ولا SF-50M.
- **Phase 27.17:** prompt-answer micro-probe وصل إلى `27/32`، وهذا breakthrough جزئي، لكن الكسور اللفظية أبقت runtime محظورًا.
- **Phase 27.18:** hygiene audit حدد 5 عبارات تتجزأ بقوة، وكل الكسور المرصودة أصبحت محجوبة، لذلك التالي repair probe مركز.
- **Phase 27.19:** repair probe على 52 مثالًا بقي `27/32`؛ أمثلة repair وحدها لا تكفي، ويلزم قرار tokenizer/protected phrases.
- **Phase 27.20:** أضيف دعم protected phrases داخل tokenizer؛ العبارات الخمس صارت قابلة للحفظ كقطعة واحدة في tokenizer v3، لكن runtime ما زال محظورًا حتى retrain + micro-probe.
- **Phase 27.21:** tokenizer v3 نجح في protected phrases، لكن micro-probe فشل `25/32` بسبب spacing/boundary؛ runtime وSF-50M محظوران.
- **Phase 27.22:** spacing/boundary repair رفع micro-probe إلى `29/32` وأزال اللصق، لكن بقي semantic/lexical failure يمنع runtime.
- **Phase 27.23:** semantic/lexical repair رفع micro-probe إلى `30/32`، لكن بقيت كلمتا `التعاون` و`الاحترام` غير ثابتتين بما يكفي للواجهة.
- **Phase 27.24:** minimal lexical stabilization رفع micro-probe إلى `32/32`، لكن لا runtime قبل held-out canary.
- **Phase 27.25:** held-out canary فشل `8/16`: التعريفات نجحت، لكن التحية/النصيحة/التخطيط/الدعم لم تعمم بما يكفي، لذلك runtime وSF-50M محظوران.
- **Phase 27.26–27.30:** repair series أضاف intent/topic conditioning ورفع fresh mixed shadow إلى `16/18`، لكن الفشلين المتبقيين يمنعان runtime.
- **Phase 27.31–27.33:** natural intent/topic ثم balanced calibration ثم advice/micro stabilization رفعت البوابات إلى `fresh mixed 18/18`, `natural 20/20`, `calibration 12/12`, `advice 4/4`, `micro 32/32` بلا prompt leakage. التالي guarded runtime trial design، لا فتح افتراضي ولا SF-50M بعد.
- **Phase 27.34:** أضافت trial محروسًا في الواجهة/API عبر `generator_trial=true` ومرّت `9/9`. التالي جمع ملاحظات حية من الواجهة قبل أي تكبير.
- **Phase 27.35:** اختبرت السيرفر الحي والواجهة عبر HTTP: `10/10`، منها `7/7` ردود مولدة و`3/3` ضوابط template/safety.
- **Phase 27.36:** أضافت quality-floor يمنع raw `chat.general` وموضوعات التعريف غير المثبتة من المولّد، ومرّ triage الحي `27/27`.
- **Phase 27.37:** أضافت semantic topic guard وفتحت `الصبر` بصيغ مثبتة؛ التوسعة الحية مرّت `21/21`.
- **Phase 27.38:** دربت probe مستهدفًا للموضوعات المحجوبة، لكنه فشل `6/20` بسبب topic collapse نحو `الاحترام`; runtime لم يتغير.
- **Phase 27.39:** دربت topic-isolation probe متوازنًا. تحسن جزئيًا إلى `10/24`، لكنه كشف كسورًا لفظية في المصطلحات الجديدة؛ runtime لم يتغير.
- **Phase 27.40:** أنشأت tokenizer v5 محميًا ودربت probe متوازنًا مرّ `24/24`.
- **Phase 27.41:** فتحت `sf_10m_phase27_40` اختياريًا عبر `generator_trial=true`; البوابة الحية مرّت `22/22`.
- **Phase 27.42:** وسعت probes الواجهة ومرّت `29/29`; الردود غير المطابقة تُحجب بدل أن تظهر للمستخدم.
- **Phase 27.43:** دربت مرشح weak-lane لكنه مرّ `10/16` فقط؛ لا runtime switch.
- **Phase 27.44–27.48:** أنشأت tokenizer v6، أصلحت conditioning لموضوعي `الوفاء/الشجاعة`، وفتحت `sf_10m_phase27_47` داخل `generator_trial=true` بعد gate حي `19/19`.
- **Phase 27.49:** وسّعت probes الحية إلى `33/33` وأصلحت كشف النصيحة السعودية.
- **Phase 27.50:** ألغت القوالب من `/chat/message`: المولد أو لا رد.
- **Phase 27.51:** اختبرت الحوار الطبيعي بلا intent/topic conditioning؛ النتيجة فشلت بوضوح، لذلك لا يكفي توسيع keywords، والتالي تدريب هدف حواري طبيعي.
- **Phase 27.52:** ضاعفت التدريب داخل `SF-10M` إلى `9200` خطوة. تحسن المؤشر من `1/20` إلى `5/20` فقط، لذلك لا runtime switch ولا تكبير.
- **Phase 27.53:** وسّعت البيانات إلى `10,540` زوجًا فريدًا و`18,000` خطوة، لكن النتيجة `2/36` وكشفت خلط/fragments؛ لا runtime switch ولا تكبير تلقائي.
- **Phase 27.54:** Capacity/Objectivity Gate قبل أي تكبير.
- **Phase 28:** أول قفزة بعد SF-50M إذا أثبت 50M قيمة واضحة.
- **Phase 29:** إدخاله في الواجهة كتجربة يومية مع router/safety/memory.

الخلاصة:

> أول “مولّد حقيقي” بدأ في Phase 13، لكن أول “حوار مولّد يقنع سامي” صار مشروطًا بإصلاح جودة التوليد القصير على `SF-10M` ومروره من canary، أو نجاح `SF-50M` لاحقًا.

---

## مراحل ما بعد Phase 20

### Phase 21 — Generative Roadmap & Quality Targets

تثبيت خارطة الطريق، مقاييس الجودة، وتعريف معنى “مولّد مقنع”.

**النجاح:** كل Agent يعرف متى يدرب، متى يقيّم، ومتى يمنع runtime.

### Phase 22 — Gold Dialogue Corpus v2

توسيع corpus إلى 500 سجل على الأقل:

- فصحى + سعودي فقط.
- user-authored أو user-reviewed أو owner-delegated agent-authored فقط.
- لا synthetic LLM data من مصدر خارجي أو مجهول.
- كل سجل يحمل `source/license/quality/training_allowed/dialect`.

**النجاح:** `make corpus-audit` يمر، والتوازن اللغوي لا يفتقد `msa`.

### Phase 23 — Tokenizer v2 Retrain & Audit

إعادة تدريب tokenizer من corpus الأكبر.

**النجاح:** حماية الكلمات السعودية الشائعة، عدم كسر protected terms، وتحسن coverage.

### Phase 24 — SF-10M v0.2 Quality Training

أول تدريب جودة بعد corpus أكبر.

**النجاح:** loss/perplexity أفضل من v0.1، وعينات توليد أقل تكرارًا.

### Phase 25 — Generated Chat Canary v1

إدخال المولد في الشات فقط على prompts آمنة، مع detector للتكرار والردود الرديئة.

**النجاح:** الواجهة تريك رد مولّد حقيقي حين ينجح، وتسقط لقالب/توضيح حين يفشل.

### Phase 26 — SF-50M v0.1 Readiness

بوابة readiness قبل أي `SF-50M`.

**النتيجة:** `can_start_sf50m_training=false` حتى يتوسع corpus وتنجح جودة runtime.

### Phase 27 — Dialogue Evaluation v2

تقييم متعدد الأدوار + خطة توسعة corpus:

- اجتماعي.
- سؤال/جواب.
- فصحى.
- سعودي.
- رفض حساس.
- كشف تكرار.

**النتيجة:** baseline pass `19/19`، لكن `generator=template`. بعد تنظيف الحوارات التشغيلية بقي `0` سجلًا قبل إعادة SF-50M gate.

### Phase 28 — SF-120M v0.1 Candidate

أول قفزة بعد نجاح SF-50M، لا قبل ذلك.

**النجاح:** أول هدف رسمي لحوار مولّد مقنع ومستقر نسبيًا.

### Phase 29 — Runtime Hybrid Assistant v1

دمج:

- generator
- router
- safety
- memory/RAG
- fallback

**النجاح:** الواجهة تصبح مساعدًا مولدًا، لا مجرد قوالب، مع تشخيص صادق.

### Phase 30 — Continuous Improvement Loop

دورة:

اختبار سامي → export → review → corpus → tokenizer/model عند الحاجة → eval → runtime.

**النجاح:** كل أسبوع/دورة يمكن قياس التحسن دون إدخال عقل خارجي.

---

## ماذا تكتب لتختبر الآن؟

للتأكد من فصل القالب عن المولد:

```text
كيفك
وين كنت
هل تفهم
وش رايك اليوم
اكتب لي رد قصير لصديق
```

المتوقع الآن:

- الأولى اجتماعية مفهومة غالبًا `template`.
- الأسئلة المفتوحة تكشف `SF-10M v0.1` الخام، وغالبًا ستظهر ضعيفة.

بعد Phase 24 نعيد نفس الاختبار، ونقيس هل صار المولد أقل تكرارًا.
