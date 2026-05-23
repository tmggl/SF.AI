# Phase 27.13 — SF-10M v0.8 Boundary/EOS Wider Training

## Status

`completed_eval_improved_generation_still_blocked`

## Scope

- Language track: `msa + saudi` only.
- Lexicon track: `Saudi Seed v1`.
- Model: `SF-10M`.
- Tokenizer: `artifacts/tokenizers/sf_bpe/v2`.
- Corpus: `5543` governed dialogue records.
- Split: `train=4973`, `eval=570`.
- Runtime activation: **blocked**.

## What Changed

- Trained `SF-10M v0.8` from scratch on the train split.
- Used assistant-only loss.
- Used explicit assistant `<eos>` target from Phase 27.12.
- Used dialect conditioning from provenance:
  - `النطاق: فصحى`
  - `النطاق: سعودي`
- Passed dialect into generation-quality evaluation.
- Tightened `GenerationGuard` against malformed v0.8 fragments.

## Training Result

| checkpoint | eval loss | perplexity |
|---|---:|---:|
| `sf-10m-step1000` | 4.9942 | 147.56 |
| `sf-10m-step2000` | 4.8111 | 122.87 |
| `sf-10m-step3000` | 4.2635 | 71.06 |
| `sf-10m-step4000` | 3.8897 | 48.90 |
| `sf-10m-step5000` | 3.6128 | 37.07 |
| `sf-10m-step6000` | 3.1875 | 24.23 |

Best checkpoint: `sf-10m-step6000`.

## Generation Quality

`artifacts/reports/generation_quality_v1_v0_8_report.json`

- Passed: `3/10`
- Runtime allowed: `false`
- Main blockers:
  - `model_artifact_fragment`
  - `greeting_mismatch`
  - `thanks_mismatch`
  - `saudi_preference_mismatch`

## Decision

Do **not** activate `SF-10M v0.8` in chat runtime.

The model improved numerically, but still produces malformed Arabic fragments.
This is progress in training objective and loss, not yet progress enough for a
convincing user-facing generator.

## Next

Phase 27.14 should focus on targeted semantic/lexical repair:

- stricter lexical sanity checks,
- targeted short social replies,
- better stop/alignment behavior,
- generation-quality gate before runtime activation,
- no `SF-50M` until quality gates pass.
