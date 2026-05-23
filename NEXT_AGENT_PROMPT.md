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

- المراحل من Phase 0 حتى Phase 27 منتهية. Phase 22 Gold Dialogue Corpus v2 وصلت إلى `500/500` (`msa=250`, `saudi=250`)، وPhase 23 درّب tokenizer v2، وPhase 24 درّب `SF-10M v0.2`، وPhase 25 أضاف canary guard حجب النموذج الحقيقي ورجع للقالب، وPhase 26 رفض تدريب `SF-50M` الآن عبر بوابة readiness، وPhase 27 مرّر eval v2 baseline `19/19` ووضع خطة corpus إلى `5000`. بدأ تنفيذ التوسعة بإضافة Batch 001 ثم Batch 002 ثم Batch 003 الكبيرة: corpus الحالي `1550` (`msa=775`, `saudi=775`).
- استخدم `make phase22-review-intake` أو `GET /system/phase22-review-intake` قبل أي تحويل من `data/corpus/chat/review/` إلى corpus تدريبي.
- `phase22-review-intake` يحتوي بوابة جودة: راقب `quality_score/quality_label/quality_blockers`، ولا تحوّل جلسات قصيرة جدًا أو فيها ردود خام من `sf_10m_v0_1/sf_10m_v0_2` إلى corpus جودة.
- `/ui/chat` يحتوي مؤشر جودة تصدير محلي ويضيف `ui_quality_*` إلى metadata.
- سامي فوّض الوكيل أن يكون هو المشغّل: اختبر الواجهة/API بنفسك، ألّف وراجع واعتمد دفعات corpus بنفسك، احفظ review exports بنفسك عند الحاجة فقط، رتّب الملفات والتقارير بنفسك، ولا تطلب من سامي تنفيذ خطوات حفظ/تصدير/اعتماد أو نقل ملفات يمكن للوكيل تنفيذها. سامي يستلم النتيجة النهائية فقط.
- الواجهة المستقرة تعمل بـ `generator=template` افتراضيًا، أي قوالب ثابتة وليست مولدًا ذكيًا. لا تطلب من سامي اختبار `SF-10M v0.2` كحوار مقنع؛ هو تحسن معملي فقط حتى ينجح canary في Phase 25.
- شغّل الاختبارات كاملة بعد أي تعديل؛ آخر حالة موثقة بعد اكتمال Phase 27 يجب أن تكون كل الاختبارات ناجحة.
- السيرفر يعمل عادةً على `http://127.0.0.1:8123` (المنفذ 8000/8765 محجوز).
- شاشة المحادثة على `/ui/chat` — هي هدف سامي الرئيسي للتجريب.
- آخر تحسين مكتمل: التركيز على العربية الفصحى + السعودية فقط، توجيه الرسائل اليومية (`وشلونك`/`شكرا`/`تمام`/`لا`/`ساعدني`/`مش فاهم`/`من صنعك`/`سعودي`/`عندي؟`/`عندي سؤال`) + Phase 10 skeleton domains.
- قاموس Saudi Seed v1 (516 مدخل من تأليف سامي) في `resources/lexicons/imported/saudi_seed_v1/`.
- مصطلحات الفصحى المرشحة في `resources/tokenization/protected_terms_msa_candidate.txt` و`preferred_merges_msa_candidate.txt`; هي ليست corpus ولا pretrained vocab، بل موارد سياسة مرشحة لأي توسيع لاحق.
- اقرأ ملفات الحوكمة والدستور قبل أي تدريب: `PROJECT_CONSTITUTION`, `LANGUAGE_SEGMENTATION`, `TOKENIZATION_POLICY`, `DATASET_GOVERNANCE`, `AGENT_ENGINEERING_RULES`, ثم `PROJECT_IDENTITY`, `ENGINEERING_RULES`, `AGENT_INSTRUCTIONS`, `PROJECT_MAP`, `PROJECT_LIFECYCLE`.
- اقرأ `docs/PHASE12_TOKENIZER_V1_REPORT.md`, `docs/PHASE13_SMOKE_TRAINING_REPORT.md`, و`docs/PHASE14_SF10M_V0_1_REPORT.md`: artifacts موجودة، لكنها غير صالحة للشات أو الجودة اللغوية بعد.
- إذا كان السيرفر الحي لم يُعد تشغيله بعد، استخدم `make phase12-readiness` لنفس القرار بدون لمس السيرفر.
- الهدف العام: الوصول إلى نموذج لغوي سيادي مولّد. أول توليد خام في Phase 13، وباب التوليد داخل الشات جُهّز في Phase 15. Phase 27 أنهى eval v2 وخطة corpus؛ الخطوة التالية مواصلة توسعة corpus من `1550` إلى `5000` قبل أي `SF-50M`.
- تفويض سامي الأخير يعني أن حوار الوكيل المؤلف لخدمة corpus يمكن اعتماده كـ `owner-delegated agent-authored` مع `training_allowed=true` إذا حمل source/license/quality/notes كاملة، وبقي ضمن `msa + saudi` ودون أي مصدر خارجي أو pretrained data.
- كل export أو corpus record يجب أن يحمل user ownership. المسار الحالي: `owner_user_id=created_by_user_id=target_user_id=sami-local` و`user_scope=single_user`.

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
