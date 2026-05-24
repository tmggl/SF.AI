# CURRENT_GOALS.md

## الهدف العام النهائي

بناء **نموذج لغوي سيادي مولّد** لـ SF.AI:

- يبدأ من الصفر، بدون أوزان جاهزة.
- يتعلم من بيانات سامي المصرّح بها.
- يركز أولًا على العربية الفصحى واللهجة السعودية.
- يدخل شاشة المحادثة تدريجيًا خلف router/safety/composer.
- لا يتحول إلى "عقل أجنبي" ولا يعتمد على أي LLM خارجي.

## هدف المرحلة الحالية

تنفيذ إصلاح جودة `SF-10M` بعد اكتمال Phase 27 كـ Dialogue Evaluation v2
واكتمال corpus gate. Phase 27.5 أثبتت أن التدريب بصيغة الحوار أفضل من
تسطيح الرسائل، وPhase 27.6 أثبتت أن assistant-target يحسن تصميم الهدف،
ثم Phase 27.7 ثبتت split ثابتًا وcanary أقوى، وPhase 27.8 درّبت
`SF-10M v0.6` ووجدت تحسنًا رقميًا دون جاهزية runtime، وPhase 27.9 ثبتت
بوابة توليد آلية، وPhase 27.10 درّبت `SF-10M v0.7` بتحسن رقمي لكن توليد
محجوب. Phase 27.11 أثبتت أن المشكلة الآن في حدّ نهاية رد المساعد/EOS:
النموذج يحفظ بدايات الردود ثم يواصل التوليد.
Phase 27.12 أضافت EOS وconditioning للفصحى/السعودي وحققت تحسنًا جزئيًا.
Phase 27.13 درّبت `SF-10M v0.8` على split التدريب بهذه الصيغة؛ eval تحسن
إلى loss `3.1875` وperplexity `24.23`، لكن generation-quality الصارم بقي
`3/10` بسبب fragments ومطابقة اجتماعية ضعيفة. runtime ما زال محظورًا.
Phase 27.14 ثبّتت أدوات جودة التدريب السيادية كقرار رسمي، بدون تدريب جديد.
Phase 27.15 أضافت curriculum اجتماعي/لغوي وno-repeat decoding ودربت
`SF-10M v0.10`; eval تحسن إلى loss `3.0452` وperplexity `21.01`، لكن
canary الدلالي الصارم بقي `0/10`.
Phase 27.16 أضافت `sample_isolated` packing ودربت `SF-10M v0.11`; العزل
الهندسي نجح، لكن eval صار أسوأ من v0.10 وcanary بقي محجوبًا.
Phase 27.17 شغّلت prompt-answer micro-probe من 32 زوجًا، وحققت `27/32`
ردًا صحيحًا؛ الفشل المتبقي كسور لفظية/حروفية لا تسمح بتفعيل الواجهة.
Phase 27.18 حولت هذه الكسور إلى hygiene audit: `5` عبارات تتجزأ بقوة،
وكل الكسور المرصودة أصبحت محجوبة في الحارس.
Phase 27.19 اختبرت repair examples حول العبارات الخمس، لكن النتيجة بقيت
`27/32`، ما يعني أن الأمثلة وحدها لا تكفي.
Phase 27.20 أضافت دعم protected phrases داخل tokenizer نفسه؛ العبارات الخمس
صارت قابلة للحفظ كقطعة واحدة في tokenizer v3 القادم، لكن runtime ما زال
محجوبًا حتى micro-probe جديد.
Phase 27.21 درّبت tokenizer v3 وشغلت micro-probe. tokenizer نجح، لكن
المولد فشل `25/32` بسبب لصق spacing/boundary مثل `سواونخفف`.
Phase 27.22 أصلحت decode boundary وfalse-positive في الحارس؛ النتيجة صارت
`29/32` واختفت كل مشاكل اللصق، لكن بقيت 3 إخفاقات semantic/lexical.
Phase 27.23 أضافت repair متوازنًا على tokenizer v3؛ النتيجة صارت `30/32`
وبقي خللان lexical في `التعاون` و`الاحترام`.
Phase 27.24 أضافت tokenizer minimal لحماية الكلمتين المتبقيتين؛ النتيجة
صارت `32/32`.
Phase 27.25 اختبرت checkpoint نفسه على أسئلة held-out جديدة؛ النتيجة
`8/16` فقط. Phase 27.26–27.30 حسّنت المسار إلى fresh mixed shadow
`16/18` مع intent/topic conditioning. Phase 27.31–27.33 أكملت natural
intent/topic + balanced calibration + advice/micro stabilization، ووصلت إلى
كل البوابات المحلية كاملة: fresh mixed `18/18` وmicro `32/32` بلا تسريب.
الخطوة الحالية ليست تكبير النموذج كاملًا. Phase 27.50 جعل الواجهة و`/chat/message` مختبرًا مولّدًا فقط: لا قوالب ظاهرة، إما رد من `sf_10m_phase27_47` أو `generator_blocked` فارغ. Phase 27.51 أثبت أن checkpoint الحالي لا يعمم على حوار طبيعي مفتوح (`raw natural=1/20`). Phase 27.52 ضاعف تدريب `SF-10M` إلى `9200` خطوة ورفع المؤشر إلى `5/20` فقط. Phase 27.53 وسّع البيانات إلى `10,540` زوجًا فريدًا و`18,000` خطوة، لكن raw natural صار `2/36` مع خلط/fragments. Phase 27.54 منع التكبير الكامل. Phase 27.55 أثبت أن السعة وحدها غير كافية (`3/20` مقابل `4/20`). Phase 27.56 شخّص أن الإصلاح التالي يجب أن يكون tokenizer/eval/format. Phase 27.57 ثبت هذه الحزمة. Phase 27.58 درّب tokenizer v7 وprobe محدودًا؛ التوكنة نجحت لكن alignment فشل `4/15`. Phase 27.59 أصلح alignment المحدود ومرّ `15/15`. Phase 27.60 اختبر التعميم الأوسع وفشل `12/30`. Phase 27.61 حسّن إلى `18/30`، لكنه أظهر مشكلة توازن عائلات جديدة. Phase 27.62 تراجع إلى `10/30` بسبب ترتيب curriculum الكتلي. Phase 27.63 أصلح الترتيب إلى interleaved ورفع canary إلى `26/30`، وبقيت مشاكل topic lexical في `التعاون/الاحترام`. Phase 27.64 أثبت أن tokenizer v8 مطلوب لأن v7 رجّع هذين المصطلحين إلى قطع متعددة. Phase 27.65 درّب tokenizer v8 فقط ومرّر topic probe `8/8`. Phase 27.66 درّب LM repair محدودًا على tokenizer v8 ومرّر broader canary `30/30`. Phase 27.67 اختبر fresh shadow canary وفشل `30/50`. Phase 27.68 أصلح الفشل المعروف إلى `50/50` وحافظ على regression `30/30`. Phase 27.69 اختبر fresh shadow جديدًا ووصل `56/60` مع بقاء open_social فقط، لذلك runtime ما زال محجوبًا.

الخطوة العملية الحالية:

- `make source-inventory` يعرض كل مصادر البيانات والمراجع المحلية، ويفرق بين corpus حواري وملفات مرجعية.
- `make corpus-audit` يفحص بيانات `data/corpus/chat/jsonl/`.
- Phase 12 tokenizer v1 اكتمل بإذن صريح من سامي، مع توثيق أنه Saudi-only ويحتاج `msa` قبل أي تشغيل جودة متوازن.
- Phase 14 SF-10M v0.1 اكتمل كتشغيل محدود وأثبت أن checkpoint يُقيّم ويولد نصًا غير فارغ.
- Phase 15 اكتمل كبنية Adapter: API/UI يعرضان مصدر الرد، ومختبر سامي المحلي يستطيع استخدام `sf_10m_v0_1`.
- Phase 16 اكتمل كبوابة evaluation/safety/style: `15/15`; النتيجة تؤكد أن النموذج الخام مكرر ويحتاج corpus أكبر.
- Phase 17 اكتمل كبنية Local RAG bridge: الشات يستطيع استخدام snippets محلية عند حقن `HybridRetriever`.
- Phase 18 اكتمل كدورة بيانات محكومة: الواجهة تصدر محادثة مراجعة محلية، و`prepare_dialogue_batch.py` يحول المعتمد فقط إلى JSONL تدريبي.
- Phase 19 بدأ كبوابة جاهزية: `make phase19-readiness` يقرر هل نبدأ SF-50M. القرار الحالي: لا، corpus صغير جدًا.
- Phase 20 اكتمل كبوابة تفعيل المجالات: `make phase20-gates` يمنع تفعيل skeleton domains بلا data/safety/tests/UI/fallback.
- Phase 21 اكتمل: تثبيت خارطة الوصول إلى حوار مولّد مقنع بعد Phase 20.
- Phase 22 اكتمل: corpus متوازن 500/500 (`msa=250`, `saudi=250`).
- Phase 23 اكتمل: tokenizer v2 جاهز (`vocab=4493`, `merges=4386`).
- Phase 24 اكتمل: `SF-10M v0.2` تدرّب 2000 خطوة، eval loss `2.5779`,
  perplexity `13.17`، لكنه غير صالح بعد كمسار رد واسع في الواجهة.
- Phase 25 اكتمل: canary guard حجب تجربة v0.2 الحقيقية ورجع إلى القالب.
- Phase 26 اكتمل: `make phase26-readiness` و`GET /system/phase26-readiness`
  قررا أن `SF-50M` غير جاهز الآن: corpus وصل إلى `1550` قبل تطبيق
  سياسة منع الحوارات التشغيلية، ثم صار `5143` سجلًا طبيعيًا فقط
  (`msa=2549`, `saudi=2594`) بعد حذف `907` سجلًا ممنوعًا ثم إضافة
  الدفعات الطبيعية. corpus gate تجاوز حد `5000`، لكن
  runtime quality/hallucination/repetition gates لم تمر.
- Phase 27 اكتمل: `make phase27-dialogue-eval` مرّر `19/19` turn في suite
  متعدد الأدوار، ووضع خطة توسعة دقيقة إلى `5000`.
- بدأ تنفيذ توسعة Phase 27: أضيفت Batches 001/002/003 ثم طُبقت سياسة
  `training_forbidden_operational_internal_dialogue`، ثم أضيفت Batches
  004/005/006 الطبيعية. الحالة الحالية: `5143` سجلًا تدريبيًا طبيعيًا
  (`msa=2549`, `saudi=2594`)، والمتبقي إلى `5000` هو `0`.
- Phase 27.5 اكتمل: أُعيد تدريب `SF-10M v0.4` بصيغة حوارية كاملة
  `المستخدم/المساعد` بدل رسائل مسطحة؛ training loss تحسّن إلى `1.4070`,
  لكن eval loss `5.8267` والردود لا تزال غير مرتبطة كفاية بالسؤال، لذلك
  runtime محظور.
- Phase 27.6 اكتمل: أُعيد تدريب `SF-10M v0.5` بخسارة على رد المساعد فقط؛
  training loss وصل `2.3513`, وأفضل eval مقاس كان step2000 عند loss `6.5718`,
  لكن الردود بقيت مكررة وضعيفة، لذلك runtime محظور.
- Phase 27.7 اكتمل: أضيف split ثابت `train=4703/eval=540`، و100 سجل gold
  social، وcanary prompt-aware. corpus الحالي `5243` (`msa=2599`, `saudi=2644`)
  وruntime المولّد لا يزال محظورًا حتى تدريب/تقييم `SF-10M v0.6`.
- Phase 27.8 اكتمل: دُرّب `SF-10M v0.6` على train split فقط، وأفضل eval كان
  `loss=5.0227`, `perplexity=151.82`. canary حجب `10/10` عينات، لذلك
  runtime محظور ولا يبدأ `SF-50M`.
- Phase 27.9 اكتمل: أضيف generation quality harness وprompt suite قصير؛
  نتيجة v0.6: `0/10` passed، والسبب `model_artifact_fragment`.
- Phase 27.10 اكتمل: أضيفت `300` عينة gold قصيرة ودُرّب `SF-10M v0.7`.
  أفضل eval `loss=4.7512`, `perplexity=115.72`، لكن generation-quality بقي
  `0/10` بعد تشديد الحارس.
- Phase 27.11 اكتمل: gold overfit probe فشل `0/16 clean-stop`; يجب إصلاح boundary/EOS.
- Phase 27.12 اكتمل جزئيًا: EOS + dialect conditioning؛ `5/16` تطابق كامل و`9/16` بلا فشل guard.
- Phase 27.13 اكتمل: `SF-10M v0.8` حسّن eval إلى ppl `24.23`، لكن generation-quality `3/10` وruntime محظور.
- Phase 27.14 اكتمل: اعتماد أدوات الجودة السيادية وملف تتبع التجارب المحلي.
- Phase 27.15 اكتمل: social/lexical curriculum + no-repeat؛ eval تحسن وruntime محظور.
- Phase 27.16 اكتمل: sample-isolated objective؛ runtime وSF-50M محظوران.
- Phase 27.17 اكتمل: prompt-answer micro-probe؛ `27/32` مع runtime محظور.
- Phase 27.18 اكتمل: tokenization/decoding hygiene audit؛ blockers محددة.
- Phase 27.19 اكتمل: hygiene repair probe؛ النتيجة بقيت `27/32`.

الجرد الحالي يرى:

- قاموس Saudi Seed v1 المحلي: 516 مدخل، مرجع لهجي خاص لا يُرفع.
- مهام اللهجة السعودية المشتقة: 1032 سجل، تصلح كمرشح tokenizer/تحويل لاحق، وليست chat corpus مباشرًا.
- `chat/jsonl`: يحتوي الآن 5943 سجل حوار محكوم. أول 500 استُخدمت لتدريب tokenizer v2، ثم بدأت توسعة Phase 27 بعد ذلك.
- `chat/splits`: يحتوي split ثابت `dialogue_split_v1.json` للتدريب/التقييم.
- `chat/review`: مخرجات مراجعة من واجهة الشات؛ ليست تدريبًا حتى تمر عبر `prepare_dialogue_batch.py` مع `--training-allowed`.

## سياسة اللغة الآن

- المدعوم افتراضيًا: **العربية الفصحى + اللهجة السعودية**.
- غير مرغوب الآن: توسيع runtime إلى المصري/الشامي/العراقي/لهجات أخرى.
- يمكن إبقاء ملفات اللهجات الأخرى كمواد خام مؤجلة، لكن لا تُحمّل افتراضيًا في `DialectMapper`.
- أي تحسين لغوي جديد يجب أن يخدم اختبار سامي المباشر على الشاشة.

## ما هو النظام الآن؟

SF.AI حاليًا:

- Router + NLP + قوالب ردود + Composer.
- ليس نموذج توليد حر.
- لا يستخدم LLM خارجيًا.
- لا يستخدم أوزان pretrained.
- لا يتعلم تلقائيًا من المحادثة الجارية.

## متى نصل إلى "نموذج ذكي يولّد"؟

البنية موجودة في Phase 5.5 و Phase 6:

- SF-BPE tokenizer جاهز للتدريب من الصفر.
- TinyTransformer scaffold جاهز.
- training loop/checkpoints/device manager موجودة.

الخارطة الرسمية أُضيفت إلى `docs/EXECUTION_PLAN.md` و[GENERATIVE_ROADMAP.md](./GENERATIVE_ROADMAP.md):

- **Phase 11:** حوكمة وتجهيز corpus فصحى/سعودي.
- **Phase 12:** تدريب SF-BPE tokenizer v1.
- **Phase 13:** أول تدريب smoke صغير وإثبات أن النموذج يتعلم.
- **Phase 14:** تدريب `SF-10M v0.1`.
- **Phase 15:** ربط checkpoint ببنية `ChatModule` كمولّد اختياري دون تفعيل runtime.
- **Phase 16:** تقييم الجودة والسلامة والأسلوب — مكتمل، ومختبر سامي المحلي يشغّل المولد الخام للتجربة.
- **Phase 17:** إدخال Memory/RAG المحلي في الشات — مكتمل كبنية اختيارية.
- **Phase 18:** دورة توسيع بيانات مضبوطة — مكتملة كتصدير مراجعة + batch preparation.
- **Phase 19:** بوابة جاهزية مرشح أكبر `SF-50M`; تحتاج 5000 سجل محكوم تقريبًا قبل التدريب.
- **Phase 20:** بوابات تفعيل المجالات؛ المجال النشط الوحيد هو `chat`.
- **Phase 21:** خارطة الجودة والتدريب بعد Phase 20.
- **Phase 22:** توسيع corpus إلى 500 سجل حوار gold/silver — مكتمل.
- **Phase 23:** تدريب tokenizer v2 — مكتمل.
- **Phase 24:** تدريب `SF-10M v0.2`؛ اكتمل بحدود، runtime محظور.
- **Phase 25:** Canary داخل الشات للمولد مع fallback عند التكرار — مكتمل كحماية.
- **Phase 26:** بوابة readiness/scaling لـ `SF-50M` — اكتملت ورفضت التدريب الآن.
- **Phase 27:** تقييم حوار متعدد الأدوار + خطة توسيع corpus — مكتمل، وcorpus gate ناجح.
- **Phase 27.5:** إصلاح صيغة تدريب `SF-10M` إلى حوار كامل — مكتمل بحدود، runtime محظور.
- **Phase 27.6:** تدريب assistant-target على رد المساعد فقط — مكتمل بحدود، runtime محظور.
- **Phase 27.7:** split ثابت + gold social + canary أقوى — مكتمل كبوابة جودة، runtime محظور.
- **Phase 27.8:** تدريب `SF-10M v0.6` على split ثابت — مكتمل بتحسن رقمي، runtime محظور.
- **Phase 27.9:** harness جودة توليد آلي — مكتمل ويحجب v0.6، runtime محظور.
- **Phase 27.10:** short-response repair + `SF-10M v0.7` — مكتمل بتحسن رقمي، runtime محظور.
- **Phase 27.11:** objective/decoding probe — مكتمل؛ stop boundary مفقود، runtime محظور.
- **Phase 27.12:** assistant EOS/boundary repair — مكتمل جزئيًا، runtime محظور.
- **Phase 27.13:** SF-10M v0.8 wider training — مكتمل بتحسن eval، runtime محظور.
- **Phase 27.14:** Sovereign Training Quality Tooling — مكتمل بدون تدريب جديد.
- **Phase 27.15:** Social/Lexical Curriculum + No-Repeat Decoding — مكتمل، runtime محظور.
- **Phase 27.16:** Prompt-to-Answer Objective Repair — مكتمل، runtime محظور.
- **Phase 27.17:** Targeted micro-probe لأزواج سؤال/جواب — مكتمل جزئيًا، runtime محظور.
- **Phase 27.18:** Tokenization/Decoding Hygiene Repair — مكتمل، runtime محظور.
- **Phase 27.19:** Hygiene Repair Corpus/Probe — مكتمل، runtime محظور.
- **Phase 27.20:** Tokenizer/Protected-Phrase Strategy — مكتمل، runtime محظور.
- **Phase 27.21:** Tokenizer v3 protected-phrase retrain + micro-probe — مكتمل، runtime محظور.
- **Phase 27.22:** Spacing/Boundary Loss Repair — مكتمل جزئيًا، runtime محظور.
- **Phase 27.23:** Semantic/Lexical Confusion Repair — مكتمل جزئيًا، runtime محظور.
- **Phase 27.24:** Minimal Lexical Stabilization — مكتمل معمليًا، runtime محظور.
- **Phase 27.25:** Held-out Generation Quality Canary — مكتمل؛ فشل `8/16` وruntime محظور.
- **Phase 27.26:** Held-out Objective Repair — مكتمل؛ `9/16`.
- **Phase 27.27:** Broader Held-out Repair — مكتمل؛ old held-out `16/16`, shadow `9/16`.
- **Phase 27.28:** Intent-Conditioned Repair — مكتمل؛ shadow `12/16`.
- **Phase 27.29:** Topic-Conditioned Definition Repair — مكتمل؛ حُجب بسبب leakage.
- **Phase 27.30:** Fresh Mixed Shadow Canary — مكتمل؛ `16/18`, runtime محظور.
- **Phase 27.31:** Natural Intent/Topic Dataset — مكتمل جزئيًا؛ natural shadow `20/20`.
- **Phase 27.32:** Balanced Natural Calibration — مكتمل جزئيًا؛ calibration `12/12`.
- **Phase 27.33:** Advice + Micro Stabilization — مكتمل؛ كل بوابات التوليد المحلية مرّت.
- **Phase 27.34:** Guarded Runtime Trial — مكتمل؛ تجربة الواجهة المحروسة مرّت `9/9`.
- **Phase 27.35:** Live UI Trial Observations — مكتمل؛ live UI/API trial مرّ `10/10`.
- **Phase 27.36:** Live UI Triage — مكتمل؛ quality-floor active وtriage مرّ `27/27`.
- **Phase 27.37:** Supported Topic Expansion — مكتمل؛ موضوع `الصبر` مرّ `3/3` خلف semantic guard.
- **Phase 27.38:** Targeted Topic Curriculum/Probe — مكتمل جزئيًا؛ `6/20` ولا runtime switch.
- **Phase 27.39:** Topic-Isolation Repair — مكتمل جزئيًا؛ `10/24` ولا runtime switch.
- **Phase 27.40:** Tokenizer/Context Repair — مكتمل؛ `24/24` والمرشح فُتح لاحقًا في trial محروس.
- **Phase 27.41:** Guarded Runtime Switch — مكتمل؛ HTTP gate مرّ `22/22` و`generator_trial` يستخدم `sf_10m_phase27_40`.
- **Phase 27.42:** Live UI Broader Probes — مكتمل؛ HTTP gate مرّ `29/29` وحجب الردود غير المطابقة.
- **Phase 27.43:** Guarded Data-Backed Expansion — مكتمل جزئيًا؛ `10/16` ولا runtime switch.
- **Phase 27.44:** Tokenizer/Curriculum Repair for Weak-Lane Stability — مكتمل جزئيًا؛ `11/16`, weak-lane `6/6`.
- **Phase 27.45:** Semantic Topic Balance Repair — مكتمل جزئيًا؛ `9/16`, لا runtime switch.
- **Phase 27.46:** Core Dialogue Stabilization — مكتمل جزئيًا؛ `14/16`, بقيت موضوعات جديدة.
- **Phase 27.47:** New Topic Conditioning Repair — مكتمل؛ offline `16/16`.
- **Phase 27.48:** Guarded Runtime Switch — مكتمل؛ live API `19/19`, و`generator_trial` يستخدم `sf_10m_phase27_47`.
- **Phase 27.49:** Broader Live UI Probes — مكتمل؛ live API `33/33`.
- **Phase 27.50:** Generator-Only UI Lab Mode — مكتمل؛ لا قوالب في `/chat/message`, gate `7/7`.
- **Phase 27.51:** Open-Dialogue Generalization Audit — مكتمل؛ فشل مفيد، live `3/22`, raw natural `1/20`.
- **Phase 27.52:** Natural Dialogue Objective Repair — مكتمل جزئيًا؛ `9200` خطوة، raw natural `5/20`, لا runtime switch.
- **Phase 27.53:** Natural Dialogue Diversity Expansion — مكتمل جزئيًا؛ `10,540` زوجًا، raw natural `2/36`, لا runtime switch.
- **Phase 27.54:** Capacity/Objectivity Gate — مكتمل؛ التكبير الكامل ممنوع، والمسموح فقط micro-probe تشخيصي في Phase 27.55.
- **Phase 27.55:** Controlled SF-50M Diagnostic Micro-Probe — مكتمل؛ `SF-10M=3/20`, `SF-50M=4/20`, لا runtime ولا تدريب كامل.
- **Phase 27.56:** Objective/Format/Tokenizer Diagnosis — مكتمل؛ `SF-50M relaxed=9/20`, و9 splits حرجة في tokenizer.
- **Phase 27.57:** Tokenizer/Eval/Format Repair Pack — مكتمل؛ `18` عبارة محمية وتغطية `9/9`، ولا runtime.
- **Phase 27.58:** Tokenizer v7 Bounded Alignment Probe — مكتمل كتجربة؛ tokenizer نجح، probe فشل `4/15`، ولا runtime.
- **Phase 27.59:** Bounded Alignment Repair — مكتمل؛ repair محدود نجح `15/15`، ولا runtime.
- **Phase 27.60:** Broader Natural-Dialogue Canary — مكتمل كتقييم؛ فشل `12/30`، ولا runtime.
- **Phase 27.61:** Broader Generalization Repair — مكتمل كتدريب repair؛ تحسن إلى `18/30`، ولا runtime.
- **Phase 27.62:** Family Balance Repair — مكتمل كتجربة فاشلة؛ تراجع إلى `10/30`، ولا runtime.
- **Phase 27.63:** Interleaved Family Curriculum — مكتمل بتحسن إلى `26/30`، ولا runtime.
- **Phase 27.64:** Topic Lexical/Tokenizer Inspection — مكتمل؛ tokenizer v8 مطلوب، ولا runtime.
- **Phase 27.65:** Tokenizer v8 Topic Probe — مكتمل؛ topic terms `8/8`، ولا runtime.
- **Phase 27.66:** V8 Bounded Topic Repair — مكتمل؛ broader canary `30/30`، ولا runtime.
- **Phase 27.67:** Fresh Shadow Canary — مكتمل كتقييم؛ فشل `30/50`، ولا runtime.
- **Phase 27.68:** Shadow Failure Repair — مكتمل؛ known shadow `50/50` وregression `30/30`، ولا runtime.
- **Phase 27.69:** New Fresh Shadow Canary — مكتمل؛ strong `56/60`، ولا runtime.
- **Phase 28:** تدريب `SF-120M v0.1`؛ أول قفزة بعد نجاح `SF-50M`.
- **Phase 29:** Runtime Hybrid Assistant v1.
- **Phase 30:** Continuous Improvement Loop.

المعنى العملي:

- أول توليد خام: Phase 13.
- أول مسار مولّد داخل الشات: Phase 15 كبنية metadata، ثم مختبر محلي بعد Phase 16.
- أول تدريب جودة مفيد اكتمل في Phase 24 لكنه غير كافٍ للشات.
- أول فرصة لحوار قصير مولّد يقنعك: بعد إصلاح جودة التوليد القصير على `SF-10M` ومروره من canary، أو نجاح `SF-50M` لاحقًا في eval v2.
- أول قفزة أكبر بعد نجاح الحوار: Phase 28 مع `SF-120M`.

حتى يتم ذلك، يجب وصف النظام بأنه **مساعد rule-based ذكي في التوجيه** مع مولّد سيادي خام للتجربة الفردية فقط عند تشغيل flags التجريبية.

## رسائل اختبار مقترحة الآن

اكتب في الشاشة:

- `مرحبا`
- `وشلونك`
- `عندي؟`
- `عندي سؤال`
- `سعودي`
- `وش تقدر تسوي`
- `من صنعك`
- `شكرا`
- `لا`
- `ساعدني`
- `مش فاهم`
- `ابي اسوي كود`
- `عندي ألم في الراس`

المتوقع:

- الرسائل الاجتماعية تذهب إلى `chat`.
- `عندي؟` تذهب إلى `chat.clarification`.
- `عندي سؤال` تفتح المجال للسؤال مباشرة، ولا تشرح سؤالًا سابقًا.
- `سعودي` تذهب إلى `chat.language_preference`.
- البرمجة غير الحساسة تمر في مختبر التوليد عند تفعيل lab mode؛ المجالات الحساسة تبقى safety-first.
