# dialogue_batch_v2_msa_003

## Purpose

Third Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This batch continues the owner-delegated agent-side corpus path. Sami does not
need to save, export, or manually approve the dialogues; the agent authors,
reviews, validates, documents, and pushes only successful work.

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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v3`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Phase/batch numbering clarity.
- Phase 22 corpus gates and why training is still blocked.
- Template/generator honesty.
- MSA style quality.
- Lexicon versus corpus separation.
- User ownership and future multi-user safety.
- Testing, auditing, and push discipline.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_003.jsonl
make corpus-audit
make phase22-readiness
```
