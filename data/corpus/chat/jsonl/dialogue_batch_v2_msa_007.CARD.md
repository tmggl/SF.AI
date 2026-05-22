# dialogue_batch_v2_msa_007

## Purpose

Seventh Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch adds practical MSA conversations about Phase 22 gates, provenance,
tokenization policy, corpus sovereignty, progressive scaling, runtime honesty,
and the distinction between fixed templates and a native generator.

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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v7`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Readiness vs completion gates.
- Source inventory and documentation discipline.
- Dependency documentation and project governance.
- Protected terms, preferred merges, UTF-8, and no pretrained vocab.
- Corpus sovereignty and Own the intelligence.
- Runtime vs training and lexicon/runtime mapping.
- Clear questioning, correction, and error acknowledgement.
- Progressive scaling and SF-10M to SF-50M gate expectations.
- Repetition, hallucination, runtime quality, and resource readiness.
- Runtime quality and resource readiness before model scaling.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_007.jsonl
make corpus-audit
make phase22-readiness
```
