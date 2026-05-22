# قاموس بذرة للهجات السعودية — saudi_dialect_lexicon_full_seed_v1

هذا الملف مخصص للسعودية فقط، وفيه كلمات ومصطلحات وعبارات مع:

- المصطلح
- اللهجة/النطاق
- أماكن الاستخدام التقريبية
- المعنى بالفصحى
- مثال سعودي قصير
- درجة الثقة
- هل يحتاج مراجعة ناطق محلي
- حقول safety للتدريب

## الملفات

- `saudi_dialect_lexicon_full_seed_v1.json` الملف الأساسي الكامل.
- `saudi_dialect_lexicon_full_seed_v1.jsonl` كل مدخل في سطر مستقل.
- `saudi_dialect_training_tasks_seed_v1.jsonl` أمثلة مهام جاهزة للتحويل للتدريب.
- `saudi_dialect_lexicon_full_seed_v1.csv` نسخة CSV للاستيراد السريع.
- `validation_summary.json` ملخص العدّ والفحص.

## العدد

عدد المداخل: 516

## مهم جدًا

لم يتم نسخ قاعدة بيانات معجم أو تعريفاته. هذه بذرة أصلية/مؤلفة مع تصنيف واسع، وليست بديلًا عن مراجعة لغوية ميدانية.
إذا أضفت لاحقًا أي مدخل من Mo3jam بإذن مكتوب، ضع لكل مدخل:

`المصدر: معجم — اللهجة السعودية: https://ar.mo3jam.com/dialect/Saudi`

## تعليمات للإيجنت

1. استخدم JSON الأساسي للفهم والتصنيف.
2. استخدم JSONL للمهام التدريبية أو التحويل إلى صيغة مشروعك.
3. لا تدرّب توليديًا بشكل خام على المداخل ذات `sensitive_or_profane=true`.
4. المداخل ذات `confidence=medium` أو `confidence=low` يجب أن تذهب إلى human review.
5. يمكن توسيع الملف فقط بأمثلة أصلية أو مصادر مرخّصة.

## وسوم اللهجات

{
  "saudi_general": "سعودي عام",
  "najdi": "نجدي",
  "hijazi_urban": "حجازي حضري",
  "hijazi_rural_bedouin": "حجازي ريفي/بدوي",
  "eastern_shargawi": "شرقاوي/شرقي",
  "southern_asiri_bahawi": "جنوبي عسيري/باحي",
  "jizani_tihami": "جازاني/تهامي",
  "najrani": "نجراني",
  "northern_shamali": "شمالي",
  "bedouin_tribal": "بدوي/قبلي عابر للمناطق"
}
