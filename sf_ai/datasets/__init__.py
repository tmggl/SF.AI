"""sf_ai.datasets — dialogue dataset pipeline (Phase 5).

This package handles **input** only. It does not train, fetch, or generate
data. The user is responsible for placing dialogue files under
`data/corpus/chat/raw/` with documented provenance.

Public surface:
    Schemas       — ChatMessage, SimpleSample, StructuredSample, Provenance
    Validators    — validate_record, validate_jsonl_file
    Cleaners      — SampleCleaner (whitespace, control chars, optional NFC)
    Loaders       — iter_jsonl, iter_chat_samples
    ChatDataset   — high-level wrapper that combines the three
"""

from sf_ai.datasets.chat_dataset import ChatDataset, DatasetStats
from sf_ai.datasets.cleaners import SampleCleaner
from sf_ai.datasets.corpus_governance import (
    CorpusGovernanceReport,
    audit_jsonl_directory_for_training,
    audit_jsonl_file_for_training,
    audit_record_for_training,
)
from sf_ai.datasets.saudi_seed import (
    SaudiSeedEntry,
    SaudiSeedSafety,
    SaudiSeedStats,
    attribution_block as saudi_seed_attribution,
    iter_saudi_seed_entries,
    load_saudi_seed,
    saudi_seed_stats,
)
from sf_ai.datasets.loaders import iter_chat_samples, iter_jsonl
from sf_ai.datasets.schemas import (
    ChatMessage,
    Provenance,
    SampleType,
    SimpleSample,
    StructuredSample,
    parse_record,
)
from sf_ai.datasets.validators import (
    SampleIssue,
    ValidationReport,
    validate_jsonl_file,
    validate_record,
)

__all__ = [
    "ChatDataset",
    "ChatMessage",
    "CorpusGovernanceReport",
    "DatasetStats",
    "Provenance",
    "SampleCleaner",
    "SampleIssue",
    "SampleType",
    "SimpleSample",
    "StructuredSample",
    "SaudiSeedEntry",
    "SaudiSeedSafety",
    "SaudiSeedStats",
    "ValidationReport",
    "iter_chat_samples",
    "iter_jsonl",
    "iter_saudi_seed_entries",
    "load_saudi_seed",
    "parse_record",
    "audit_jsonl_directory_for_training",
    "audit_jsonl_file_for_training",
    "audit_record_for_training",
    "saudi_seed_attribution",
    "saudi_seed_stats",
    "validate_jsonl_file",
    "validate_record",
]
