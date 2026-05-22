# dialogue_batch_v2_msa_008

## Purpose

Eighth Phase 22 MSA dialogue batch for SF.AI Gold Dialogue Corpus v2.

This intentionally small batch closes the remaining MSA minimum shortfall
after `msa_007`: 197 MSA records became 200 MSA records. It does not attempt
to add filler. The next Phase 22 priority becomes Saudi dialogue coverage.

## Counts

- Records: 3
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

- Source: `sf-ai-owner-delegated-agent-authored-msa-v8`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Why a three-record MSA batch is sufficient.
- How the plan moves from MSA minimum coverage to Saudi coverage.
- How to judge the success of this small batch without claiming Phase 22 is complete.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_msa_008.jsonl
make corpus-audit
make phase22-readiness
```
