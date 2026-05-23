# Phase 27.12 — Assistant Boundary/EOS Repair Probe Generations

## 0 — msa — PASS

- prompt: السلام عليكم
- expected: وعليكم السلام، أهلًا بك.
- generated: وعليكم السلام، أهلًا بك.
- reason: passed

## 1 — msa — FAIL

- prompt: مرحبًا
- expected: مرحبًا بك، تفضل.
- generated: صباح النور، عسى يومك طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 2 — msa — FAIL

- prompt: صباح الخير
- expected: صباح النور، يومك سعيد.
- generated: صباح النور، عسى يومك طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 3 — msa — FAIL

- prompt: مساء الخير
- expected: مساء النور، كيف أساعدك؟
- generated: صباح النور، عسى يومك طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 4 — msa — PASS

- prompt: كيف حالك؟
- expected: أنا بخير، شكرًا لسؤالك.
- generated: أنا بخير، شكرًا لسؤالك.
- reason: passed

## 5 — msa — PASS

- prompt: هل تفهمني؟
- expected: نعم، أفهمك. وضّح لي ما تريد.
- generated: نعم، أفهمك. وضّح لي ما تريد.
- reason: passed

## 6 — msa — FAIL

- prompt: أريد جوابًا قصيرًا.
- expected: حسنًا، سأجيب باختصار.
- generated: عليكم السلام، أهلًا بك.
- reason: missing_expected_terms

## 7 — msa — FAIL

- prompt: اشرح لي ببساطة.
- expected: ببساطة: ابدأ بخطوة صغيرة.
- generated: ببببخير، وش تحتاج؟
- reason: guard:malformed_token

## 8 — saudi — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، حياك الله.
- generated: وعليكم السلام، أهلًا بك.
- reason: overgenerates_after_expected

## 9 — saudi — FAIL

- prompt: هلا
- expected: هلا بك، تفضل.
- generated: طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 10 — saudi — PASS

- prompt: صباح الخير
- expected: صباح النور، عسى يومك طيب.
- generated: صباح النور، عسى يومك طيب.
- reason: passed

## 11 — saudi — FAIL

- prompt: مساء الخير
- expected: مساء النور، وش تحتاج؟
- generated: صباح النور، عسى يومك طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 12 — saudi — PASS

- prompt: كيفك؟
- expected: بخير الحمد لله، أنت كيفك؟
- generated: بخير الحمد لله، أنت كيفك؟
- reason: passed

## 13 — saudi — FAIL

- prompt: وشلونك؟
- expected: تمام، الله يسلمك.
- generated: بخير، شكرًا لسؤالك.
- reason: missing_expected_terms

## 14 — saudi — FAIL

- prompt: تفهم علي؟
- expected: إيه، أفهم عليك.
- generated: طة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة: ة:
- reason: guard:repetition

## 15 — saudi — FAIL

- prompt: أبي جواب قصير.
- expected: تم، بعطيك المختصر.
- generated: بخير الحمد للعليكم السلام، حيب.
- reason: missing_expected_terms
