# dialogue_batch_v2_msa_005

## Purpose

Fifth Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch adds practical MSA conversations about the project lifecycle,
runtime/training/tokenizer distinctions, readiness gates, corpus governance,
safe authoring, and the current MSA + Saudi language scope.

## Counts

- Records: 25
- Domain: chat
- Language: Arabic
- Dialect: `msa`
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-msa-v5`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Runtime versus training versus tokenizer.
- Phase 22 readiness and completion gates.
- Why corpus quality precedes model scaling.
- Review export versus training corpus.
- Avoiding sensitive-domain data in general chat corpus.
- Saudi Seed v1 as a reference lexicon, not direct chat corpus.
- MSA + Saudi language scope.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_005.jsonl
make corpus-audit
make phase22-readiness
```
