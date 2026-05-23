# Phase 27.11 Objective Probe Generations

## 0 — msa — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، أهلًا بك.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 1 — msa — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، أهلًا بك باختصار.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 2 — msa — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، أهلًا بك من فضلك.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 3 — msa — FAIL

- prompt: مرحبًا
- expected: مرحبًا بك، تفضل.
- generated: مرحبًا بك، تفضل. ل. ل. ل. ل. فضل من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 4 — msa — FAIL

- prompt: مرحبًا
- expected: مرحبًا بك، تفضل باختصار.
- generated: مرحبًا بك، تفضل. ل. ل. ل. ل. فضل من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 5 — msa — FAIL

- prompt: مرحبًا
- expected: مرحبًا بك، تفضل من فضلك.
- generated: مرحبًا بك، تفضل. ل. ل. ل. ل. فضل من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 6 — msa — FAIL

- prompt: صباح الخير
- expected: صباح النور، يومك سعيد.
- generated: صباح النور، يومك سعحياك الله من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 7 — msa — FAIL

- prompt: صباح الخير
- expected: صباح النور، يومك سعيد باختصار.
- generated: صباح النور، يومك سعحياك الله من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 8 — saudi — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، حياك الله.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 9 — saudi — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، حياك الله باختصار.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 10 — saudi — FAIL

- prompt: السلام عليكم
- expected: وعليكم السلام، حياك الله من فضلك.
- generated: وعليكم السلام، أهلًا بك. بك. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار. باختصار.
- reason: guard:repetition

## 11 — saudi — FAIL

- prompt: هلا
- expected: هلا بك، تفضل.
- generated: هلا بك، تفضل. ل. ل. فضل من فضلك. . . . . . . . . .
- reason: overgenerates_after_expected

## 12 — saudi — FAIL

- prompt: هلا
- expected: هلا بك، تفضل باختصار.
- generated: هلا بك، تفضل. ل. ل. فضل من فضلك. . . . . . . . . .
- reason: overgenerates_after_expected

## 13 — saudi — FAIL

- prompt: هلا
- expected: هلا بك، تفضل من فضلك.
- generated: هلا بك، تفضل. ل. ل. فضل من فضلك. . . . . . . . . .
- reason: overgenerates_after_expected

## 14 — saudi — FAIL

- prompt: صباح الخير
- expected: صباح النور، عسى يومك طيب.
- generated: صباح النور، يومك سعحياك الله من فضلك. . . . . . .
- reason: overgenerates_after_expected

## 15 — saudi — FAIL

- prompt: صباح الخير
- expected: صباح النور، عسى يومك طيب باختصار.
- generated: صباح النور، يومك سعحياك الله من فضلك. . . . . . .
- reason: overgenerates_after_expected
