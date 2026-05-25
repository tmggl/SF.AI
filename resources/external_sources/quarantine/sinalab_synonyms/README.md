# SinaLab Synonyms Quarantine

This directory is for Phase 27.116 metadata-only artifact inspection.

- `raw/` may contain the downloaded `Synonyms Dataset.xlsx` artifact locally.
- Raw artifact files are ignored by git.
- Commit only manifests, checksums, schema summaries, reports, and decisions.
- Do not copy raw rows into `data/corpus`.
- Do not build tokenizer vocab or merges from this artifact.
- Do not start training from this artifact.
