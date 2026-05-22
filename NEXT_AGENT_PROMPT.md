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
2. لا تشغّل crawler ولا تدريب فعلي بدون إذن صريح من سامي.
3. لا تنتقل بين مراحل الخطة بدون موافقة صريحة.
4. كل قاموس مستورد له إذن موثَّق (انظر `docs/SOURCE_DISCOVERY_*.md`).
5. الرد بالعربية الواضحة. حازم في التنفيذ، شفاف في النتائج.

**الحالة الراهنة باختصار:**

- المراحل من Phase 0 حتى Phase 11 منتهية، ومعها طبقة Governance & Engineering Standards قبل Phase 12. الخطة الرسمية تمتد إلى Phase 20 لبناء النموذج اللغوي السيادي المولّد.
- 351 اختبار يمر (`.venv/bin/python -m pytest tests`).
- السيرفر يعمل عادةً على `http://127.0.0.1:8123` (المنفذ 8000/8765 محجوز).
- شاشة المحادثة على `/ui/chat` — هي هدف سامي الرئيسي للتجريب.
- آخر تحسين مكتمل: التركيز على العربية الفصحى + السعودية فقط، توجيه الرسائل اليومية (`وشلونك`/`شكرا`/`تمام`/`لا`/`ساعدني`/`مش فاهم`/`من صنعك`/`سعودي`/`عندي؟`/`عندي سؤال`) + Phase 10 skeleton domains.
- قاموس Saudi Seed v1 (516 مدخل من تأليف سامي) في `resources/lexicons/imported/saudi_seed_v1/`.
- اقرأ ملفات الحوكمة والدستور قبل أي تدريب: `PROJECT_CONSTITUTION`, `LANGUAGE_SEGMENTATION`, `TOKENIZATION_POLICY`, `DATASET_GOVERNANCE`, `AGENT_ENGINEERING_RULES`, ثم `PROJECT_IDENTITY`, `ENGINEERING_RULES`, `AGENT_INSTRUCTIONS`, `PROJECT_MAP`, `PROJECT_LIFECYCLE`.
- اقرأ `docs/PHASE12_PREFLIGHT_REPORT.md`: إذا كان `Training permission: NOT GRANTED` فلا تبدأ التدريب حتى لو كانت الفحوصات PASS. ويمكنك فحص القرار الحي من API عبر `GET /system/phase12-readiness`؛ إذا كان `can_train_now=false` فتوقف قبل التدريب.
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وأول توليد داخل الشات في Phase 15، والاستخدام اليومي بعد Phase 16.

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
   يوجد الآن `first_dialogue_seed.jsonl` صغير، وقد يعطي التقرير `READY_FOR_PHASE_12_TOKENIZER_TRAINING`. لا تبدأ التدريب رغم ذلك إلا إذا أعطى سامي إذنًا صريحًا جديدًا. آخر توجيه منه كان: لا تبدأ Phase 12 الآن، شغّل corpus-audit فقط.

5. بوابة التدريب التنفيذية:
   ```
   make train-bpe
   ```
   يرفض التشغيل بدون `--confirm-phase12-permission`. لا تمرر هذا العلم إلا بعد إذن صريح واضح من سامي ببدء Phase 12.

**أسلوب التواصل المتفق عليه:**

- إنهاء أي مرحلة بعبارة:
  > "اكتملت المرحلة الحالية. هل تسمح لي بالانتقال إلى المرحلة التالية؟"

- عند الشك في إذن أو قرار: **توقّف واسأل سامي**. لا تخمن.

---

ابدأ الآن.
