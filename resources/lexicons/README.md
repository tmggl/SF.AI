# resources/lexicons

قواميس YAML المستخدمة في طبقة فهم اللغة (NLP) والراوتر.

> **يُعبَّأ هذا المجلد في Phase 3 — Language Understanding Layer.**

الملفات المخططة:
- `domains.yaml`
- `intents.yaml`
- `arabic_normalization.yaml`
- `dialects_gulf.yaml`
- `dialects_common_arabic.yaml`
- `typo_patterns.yaml`
- `programming_terms.yaml`
- `data_terms.yaml`
- `files_terms.yaml`
- `web_terms.yaml`
- `legal_terms.yaml`
- `medical_terms.yaml`
- `finance_terms.yaml`
- `education_terms.yaml`
- `social_terms.yaml`
- `safety_terms.yaml`
- `stopwords_ar_en.yaml`
- `arabizi_map.yaml`

**قواعد:**
- لا حشو عشوائي. الجودة قبل الكمية.
- لا تكتب القواميس داخل ملفات Python.
- كل lexicon يحمل metadata: المصدر، اللهجة، التاريخ.
