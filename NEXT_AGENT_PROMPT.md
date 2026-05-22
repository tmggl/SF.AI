# NEXT_AGENT_PROMPT.md

## برومت جاهز للنسخ — للوكيل التالي

> **استخدام:** إذا فتح المستخدم سامي جلسة جديدة وأراد متابعة بناء SF.AI، يلصق المحتوى تحت السطر الفاصل في الشات.

---

أنت وكيل برمجي يكمل بناء مشروع SF.AI.

**قبل أي شيء، اقرأ كاملاً:**

```
/Users/sami/workSF/SF.AI/docs/AGENT_HANDOFF.md
```

ثم استكشف:
- `/Users/sami/workSF/SF.AI/PROJECT_PRINCIPLES.md` — المبادئ الحاكمة.
- `/Users/sami/workSF/SF.AI/docs/PHASE_STATUS.md` — أين نحن الآن.
- `/Users/sami/workSF/SF.AI/docs/EXECUTION_PLAN.md` — الخطة الكاملة على مراحل.

**القواعد الذهبية (لا تكسرها):**

1. لا تستورد أي LLM خارجي ولا أي pretrained weights/embeddings/tokenizer.
2. لا تشغّل crawler أو مصدر خارجي بدون provenance واضح واحترام بوابة permission.
3. لا تنتقل خارج المراحل المسجلة في الخطة بدون توثيق السبب.
4. كل قاموس مستورد له إذن موثَّق (انظر `docs/SOURCE_DISCOVERY_*.md`).
5. الرد بالعربية الواضحة. حازم في التنفيذ، شفاف في النتائج.

**الحالة الراهنة باختصار:**

- المراحل من Phase 0 حتى Phase 21 منتهية؛ Phase 22 تعمل الآن كبوابة جاهزية وخطة جمع وreview intake لـ Gold Dialogue Corpus v2. قرار Phase 22 الحالي: `NOT_READY_BUILD_GOLD_DIALOGUE_CORPUS_V2` لأن corpus الحالي 30/500 ويفتقد `msa`. خطة الجمع الحالية: 200 فصحى + 170 سعودي + 100 مرنة. استخدم `make phase22-next-batch` لمعرفة المهمة الفورية؛ الحالية `msa_001`.
- استخدم `make phase22-review-intake` أو `GET /system/phase22-review-intake` قبل أي تحويل من `data/corpus/chat/review/` إلى corpus تدريبي.
- `phase22-review-intake` يحتوي بوابة جودة: راقب `quality_score/quality_label/quality_blockers`، ولا تحوّل جلسات قصيرة جدًا أو فيها ردود خام من `sf_10m_v0_1` إلى corpus جودة.
- `/ui/chat` يحتوي مؤشر جودة تصدير محلي ويضيف `ui_quality_*` إلى metadata.
- الواجهة المستقرة تعمل بـ `generator=template` افتراضيًا، أي قوالب ثابتة وليست مولدًا ذكيًا. تعرض الواجهة بوابة Phase 22 الحية وجودة التصدير لتجميع corpus؛ لا تطلب من سامي اختبار المولد كحوار مقنع الآن؛ `sf_10m_v0_1` خام ومكرر ولا يُفعل إلا كمختبر صريح.
- 423 اختبار يمر (`.venv/bin/python -m pytest tests`) وآخر تشغيل: `423 passed in 4.43s`.
- السيرفر يعمل عادةً على `http://127.0.0.1:8123` (المنفذ 8000/8765 محجوز).
- شاشة المحادثة على `/ui/chat` — هي هدف سامي الرئيسي للتجريب.
- آخر تحسين مكتمل: التركيز على العربية الفصحى + السعودية فقط، توجيه الرسائل اليومية (`وشلونك`/`شكرا`/`تمام`/`لا`/`ساعدني`/`مش فاهم`/`من صنعك`/`سعودي`/`عندي؟`/`عندي سؤال`) + Phase 10 skeleton domains.
- قاموس Saudi Seed v1 (516 مدخل من تأليف سامي) في `resources/lexicons/imported/saudi_seed_v1/`.
- اقرأ ملفات الحوكمة والدستور قبل أي تدريب: `PROJECT_CONSTITUTION`, `LANGUAGE_SEGMENTATION`, `TOKENIZATION_POLICY`, `DATASET_GOVERNANCE`, `AGENT_ENGINEERING_RULES`, ثم `PROJECT_IDENTITY`, `ENGINEERING_RULES`, `AGENT_INSTRUCTIONS`, `PROJECT_MAP`, `PROJECT_LIFECYCLE`.
- اقرأ `docs/PHASE12_TOKENIZER_V1_REPORT.md`, `docs/PHASE13_SMOKE_TRAINING_REPORT.md`, و`docs/PHASE14_SF10M_V0_1_REPORT.md`: artifacts موجودة، لكنها غير صالحة للشات أو الجودة اللغوية بعد.
- إذا كان السيرفر الحي لم يُعد تشغيله بعد، استخدم `make phase12-readiness` لنفس القرار بدون لمس السيرفر.
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وباب التوليد داخل الشات جُهّز في Phase 15. Phase 22 يجمع corpus حقيقيًا لا synthetic LLM data، حتى نصل لاحقًا إلى Phase 24 للتدريب المفيد.

**هدف سامي الرئيسي الآن:**

> شاشة محادثة عربية مريحة، توجيه دقيق للأسئلة، بدون أي عقل أجنبي.

**أول ما تفعل بعد قراءة AGENT_HANDOFF.md:**

1. شغّل الاختبارات للتأكد من سلامة الحالة:
   ```
   cd /Users/sami/workSF/SF.AI && .venv/bin/python -m pytest tests
   ```

2. تحقق من القسم 4 في AGENT_HANDOFF.md. مهمة "محادثة مريحة + توجيه دقيق" مكتملة، لكن اقرأ نتائج الـ audit قبل أي توسيع.

3. Phase 11 مكتملة كحوكمة وأداة فحص. شغّل:
   ```
   make source-inventory
   ```
   هذا يريك كل المراجع المحلية: chat corpus، ملف مهام اللهجة السعودية، قاموس Saudi Seed، وMo3jam slot.

4. ثم شغّل:
   ```
   make corpus-audit
   ```
   يوجد الآن seed سعودي صغير، وجرى تدريب tokenizer v1 وLM runs منه بإذن سامي. لا تعامله كجودة لغوية متوازنة ولا تربطه بالشات.

5. التفويض الحالي: سامي أعطى إذنًا صريحًا لمتابعة المراحل المسجلة والتدريب والاختبارات. لا تنتظر إذنًا جديدًا للمراحل المخططة، لكن لا تكسر قواعد السيادة أو فحص الحساسية أو provenance.

**أسلوب التواصل المتفق عليه:**

- عند إنهاء أي مرحلة: أعطِ ملخصًا عربيًا يتضمن رقم الرحلة، القاموس المتبع، الاختبارات، وهل تم الرفع.
- عند الشك في مصدر خارجي أو مخاطرة حساسة: **توقّف واسأل سامي**. لا تخمن.

---

ابدأ الآن.
