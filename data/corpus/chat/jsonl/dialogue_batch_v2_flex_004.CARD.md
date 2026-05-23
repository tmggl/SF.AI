# dialogue_batch_v2_flex_004

## Purpose

Fourth and final flexible Phase 22 dialogue batch for SF.AI Gold Dialogue
Corpus v2.

This batch closes the 500-record Phase 22 corpus target. It focuses on
transition discipline after corpus completion: completion gates, no automatic
training, honest generator expectations, and clear reporting for the next
agent.

## Counts

- Records: 25
- Domain: chat
- Language: Arabic
- Dialects: `msa`, `saudi`
- MSA records: 13
- Saudi records: 12
- Quality: `silver`
- Training allowed: true
- User scope: `single_user`
- Owner user: `sami-local`
- Created by user: `sami-local`
- Target user: `sami-local`

## Provenance

- Source: `sf-ai-owner-delegated-agent-authored-flex-v4`
- License: `owner-approved-for-sf-ai-training`
- Authoring mode: owner-delegated agent-authored

## Scope

The records cover:

- Phase 22 completion semantics.
- Distinguishing corpus completion from generator success.
- Completion gate workflow.
- No automatic tokenizer/model training after corpus completion.
- Reporting expectations for future agents.
- MSA + Saudi-only language policy.
- Saudi Seed v1 as reference, not raw corpus.

## Safety

- No medical, legal, finance, security, or religious advice.
- No external dataset copied.
- No pretrained model output.
- No raw SF-10M output included.

## Validation

Run:

```bash
.venv/bin/python scripts/validate_dataset.py data/corpus/chat/jsonl/dialogue_batch_v2_flex_004.jsonl
make corpus-audit
make phase22-readiness
make phase22-completion-gate
```
