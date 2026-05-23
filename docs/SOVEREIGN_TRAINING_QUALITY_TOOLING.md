# Sovereign Training Quality Tooling

## Decision

SF.AI adopts a local-only tooling layer for training quality. These tools are
allowed because they are deterministic engineering tools, not imported
intelligence:

- no external LLM,
- no pretrained weights,
- no pretrained embeddings,
- no pretrained tokenizer vocabulary,
- no cloud experiment tracker.

## Adopted Tools

| Tool | Decision | Current Status |
|---|---|---|
| Assistant EOS / stop boundary | adopted | implemented in Phase 27.12 |
| Sequence packing with boundaries | adopted | implemented through dialogue stream + role markers |
| Local experiment tracker | adopted | implemented in Phase 27.14 |
| Data quality scanner | adopted | corpus audit exists; semantic scanner next |
| Curriculum sampler | adopted | next repair phase |
| No-repeat decoding controls | adopted | next decoder repair |
| Gold-only micro probes | adopted | Phase 27.11/27.12 implemented |
| Checkpoint selector | adopted | Phase 27.13 used held-out eval + canary |
| Local logs | adopted | JSON reports + JSONL registry |
| Tokenizer boundary audit | adopted | policy audit exists; boundary audit required before tokenizer v3 |

## Mandatory Policy

- A checkpoint is never selected by latest step alone.
- Lower eval loss is not enough for runtime activation.
- Runtime generation stays blocked until generation-quality passes.
- SF-50M stays blocked until SF-10M passes scaling gates.
- Phase 28 stays blocked until SF-50M exists and passes gates.

## Local Artifacts

- `artifacts/reports/phase27_14_quality_tooling_decision_report.json`
- `artifacts/reports/experiment_registry.jsonl`

## Next Engineering Step

Phase 27.15 should implement targeted social/lexical curriculum plus decoder
no-repeat controls for SF-10M. The goal is not a prettier number; the goal is a
simple Arabic/Saudi reply that is understandable, socially aligned, and free of
broken fragments.
