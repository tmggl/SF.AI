# dialogue_batch_v2_msa_004

## Purpose

Fourth Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch adds natural MSA conversation patterns around clarification,
honest capability boundaries, UI/testing expectations, and phase-aware
execution. It complements the MSA protected-terms seed with more dialogue-like
examples.

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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v4`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Clarification and follow-up behavior.
- Honest distinction between template/runtime/generator.
- Phase-aware progress summaries.
- Corpus versus training explanations.
- Practical social response style in MSA.
- Phase 22 data-quality discipline.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_004.jsonl
make corpus-audit
make phase22-readiness
```
