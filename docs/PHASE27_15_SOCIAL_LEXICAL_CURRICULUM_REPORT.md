# Phase 27.15 — Social/Lexical Curriculum + No-Repeat Decoding

## Status

`completed_eval_improved_strict_generation_blocked`

## Scope

- Language track: `msa + saudi`.
- Lexicon track: `Saudi Seed v1`.
- Model trained: `SF-10M v0.10`.
- Runtime activation: **blocked**.
- SF-50M: **blocked**.

## What Was Added

- No-repeat decoding controls:
  - `no_repeat_ngram_size=3`
  - `repetition_penalty=1.08`
- A targeted curriculum batch:
  - `200` MSA gold records.
  - `200` Saudi gold records.
  - everyday social/lexical prompts only.
  - no project operations, no agent workflow, no engineering commands.
- Stricter generation-quality suite:
  - every prompt now requires semantic terms, not just Arabic-looking text.

## Corpus

```text
total_records  = 5943
training_ready = 5943
issues         = 0
msa            = 2949
saudi          = 2994
gold           = 831
silver         = 5112
```

Split:

```text
train = 5343
eval  = 600
```

## Training Result

`SF-10M v0.10` reached the best eval loss so far:

| checkpoint | eval loss | perplexity |
|---|---:|---:|
| `sf-10m-step1000` | 4.9944 | 147.59 |
| `sf-10m-step2000` | 5.0831 | 161.28 |
| `sf-10m-step3000` | 4.3987 | 81.34 |
| `sf-10m-step4000` | 4.0198 | 55.69 |
| `sf-10m-step5000` | 3.7826 | 43.93 |
| `sf-10m-step6000` | 3.0452 | 21.01 |

## Generation Quality

After strengthening the semantic canary:

```text
passed          = 0/10
runtime_allowed = false
```

This is the correct decision. A lower eval loss is not enough; the raw answers
still fail prompt alignment and produce occasional broken fragments.

## Decision

Do not activate `SF-10M v0.10`.

Do not start `SF-50M`.

Phase 27.16 should focus on prompt-to-answer conditioning/objective repair
before adding more data or scaling.
